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
            if etapa.reintentos < 0:
                raise ValueError("reintentos no puede ser negativo")
            p = prompts.cargar(etapa.prompt, etapa.version)
            valores = dict(entrada)
            for nombre in etapa.usa:
                if nombre not in salidas:
                    raise ValueError(f"{etapa.nombre}: la dependencia {nombre!r} no se ejecutó")
                valor = salidas[nombre]
                valores[nombre] = valor if isinstance(valor, str) else json.dumps(
                    valor, ensure_ascii=False, indent=2)
            sistema, usuario = p.render(**{v: valores.get(v, "") for v in p.variables})
            inicio = time.perf_counter()
            costo = 0.0
            errores = []
            for intentos in range(1, etapa.reintentos + 2):
                consulta = usuario
                if intentos > 1:
                    consulta += ("\nLa respuesta anterior no cumplió el formato o la regla de negocio.\n"
                                 + "\n".join(errores[:5]) + "\nDevuelve solo el JSON corregido.")
                r = llm.generar(consulta, sistema, json=p.salida_json,
                                temperatura=etapa.temperatura,
                                etiqueta=f"{self.nombre}/{etapa.nombre}/{p.nombre}")
                costo += r.costo_usd
                salida = r.datos if p.salida_json else r.texto
                errores = validar_esquema(salida, p.esquema)
                if p.salida_json and salida is None and not errores:
                    errores = ["La salida no es JSON válido"]
                errores_esquema = list(errores)
                errores_negocio = []
                if not errores and etapa.validar is not None:
                    errores_negocio = etapa.validar(salida, salidas)
                    errores = errores_negocio
                trazas.registrar("intento_etapa", flujo=self.nombre, etapa=etapa.nombre,
                                 prompt=p.nombre, intento=intentos, ok=not errores,
                                 errores=errores, errores_esquema=errores_esquema,
                                 errores_negocio=errores_negocio,
                                 validador_evaluado=not errores_esquema and etapa.validar is not None,
                                 salida=salida, proveedor=r.proveedor, modelo=r.modelo)
                if not errores:
                    break
            res = ResultadoEtapa(etapa.nombre, p.nombre, not errores, salida, errores,
                                 intentos, (time.perf_counter() - inicio) * 1000, costo)
            resultados.append(res)
            salidas[etapa.nombre] = res.salida
            trazas.registrar("etapa", flujo=self.nombre, etapa=res.nombre, prompt=res.prompt, ok=res.ok,
                             errores=res.errores, intentos=res.intentos, latencia_ms=res.latencia_ms,
                             costo_usd=round(res.costo_usd, 6))
            if not res.ok and detener_en_error:
                break
        return ResultadoFlujo(entrada, salidas, resultados)
