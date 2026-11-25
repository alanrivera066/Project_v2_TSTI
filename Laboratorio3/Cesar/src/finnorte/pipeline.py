"""Flujos encadenados (T4): la salida de cada etapa es la entrada de la siguiente.

    flujo = Pipeline([
        Etapa("analizar",  prompt="analizar_requisito"),
        Etapa("casos",     prompt="generar_casos", usa=["analizar"]),
        Etapa("revisar",   prompt="revisar_casos", usa=["analizar", "casos"]),
    ])
    res = flujo.ejecutar({"requisito": "El sistema deberá…"})
    res.salidas["casos"], res.ok, res.bitacora

Cada etapa: renderiza su prompt con la entrada y las salidas previas → llama al modelo →
valida la salida contra el esquema JSON → si no es válida, reintenta con el error (control, T5).
"""
from __future__ import annotations

import json
import time
from dataclasses import dataclass, field
from typing import Any, Callable

import jsonschema

from . import llm, prompts, trazas


@dataclass
class Etapa:
    nombre: str
    prompt: str                      # id del prompt en prompts/
    version: int | None = None       # None = la más reciente
    usa: list[str] = field(default_factory=list)   # salidas previas que necesita
    validar: Callable[[Any, dict], list[str]] | None = None   # validación extra (reglas de negocio)
    reintentos: int = 1
    temperatura: float = 0.2


@dataclass
class ResultadoEtapa:
    nombre: str
    prompt: str
    ok: bool
    salida: Any
    errores: list[str]
    intentos: int
    latencia_ms: float
    costo_usd: float


@dataclass
class ResultadoFlujo:
    entrada: dict
    salidas: dict
    etapas: list[ResultadoEtapa]

    @property
    def ok(self) -> bool:
        return all(e.ok for e in self.etapas)

    @property
    def costo_usd(self) -> float:
        return sum(e.costo_usd for e in self.etapas)

    @property
    def latencia_ms(self) -> float:
        return sum(e.latencia_ms for e in self.etapas)

    def bitacora(self) -> list[dict]:
        return [e.__dict__ for e in self.etapas]


def validar_esquema(datos: Any, esquema: dict | None) -> list[str]:
    """Lista de errores de esquema (vacía si es válido)."""
    if esquema is None:
        return []
    if datos is None:
        return ["La salida no es JSON válido"]
    v = jsonschema.Draft202012Validator(esquema)
    return [f"{'/'.join(map(str, e.path)) or '(raíz)'}: {e.message}" for e in v.iter_errors(datos)]


class Pipeline:
    def __init__(self, etapas: list[Etapa], nombre: str = "flujo"):
        self.etapas = etapas
        self.nombre = nombre

    def ejecutar(self, entrada: dict, detener_en_error: bool = True) -> ResultadoFlujo:
        salidas: dict = {}
        resultados: list[ResultadoEtapa] = []
        for etapa in self.etapas:
            t0 = time.perf_counter()
            costo, salida, errores, intentos = 0.0, None, [], 0
            contexto = {**entrada, **{n: salidas[n] for n in etapa.usa if n in salidas}}
            faltantes = [n for n in etapa.usa if n not in salidas]
            if faltantes:
                errores = [f"Dependencias ausentes: {faltantes}"]
            else:
                try:
                    p = prompts.cargar(etapa.prompt, etapa.version)
                    valores = {k: json.dumps(contexto[k], ensure_ascii=False) if isinstance(contexto[k], (dict, list))
                               else contexto[k] for k in p.variables if k in contexto}
                    sistema, usuario = p.render(**valores)
                    esquema = p.esquema
                    for intentos in range(1, etapa.reintentos + 2):
                        consulta = usuario
                        if errores:
                            consulta += "\nLa salida anterior no cumplió el formato o las reglas: " + "; ".join(errores)
                        respuesta = llm.generar(consulta, sistema, json=p.salida_json,
                                                temperatura=etapa.temperatura, etiqueta=f"{self.nombre}/{p.nombre}")
                        costo += respuesta.costo_usd
                        salida = respuesta.datos if p.salida_json else respuesta.texto
                        errores = validar_esquema(salida, esquema)
                        if p.salida_json and salida is None and not errores:
                            errores = ["La salida no es JSON válido"]
                        if not errores and etapa.validar:
                            errores = etapa.validar(salida, contexto)
                        trazas.registrar("intento_etapa", flujo=self.nombre, etapa=etapa.nombre,
                                         intento=intentos, errores=errores)
                        if not errores:
                            break
                except (llm.LLMError, KeyError, ValueError, FileNotFoundError) as exc:
                    errores = [f"{type(exc).__name__}: {exc}"]
            res = ResultadoEtapa(etapa.nombre, f"{etapa.prompt}.v{etapa.version or 'latest'}",
                                 not errores, salida, errores, intentos,
                                 round((time.perf_counter() - t0) * 1000, 1), costo)
            resultados.append(res)
            salidas[etapa.nombre] = res.salida
            trazas.registrar("etapa", flujo=self.nombre, etapa=res.nombre, prompt=res.prompt, ok=res.ok,
                             errores=res.errores, intentos=res.intentos, latencia_ms=res.latencia_ms,
                             costo_usd=round(res.costo_usd, 6))
            if not res.ok and detener_en_error:
                break
        return ResultadoFlujo(entrada, salidas, resultados)
