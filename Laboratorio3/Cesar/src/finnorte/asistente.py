"""Caso guía de los viernes: «Pregúntale al Manual de Ingeniería de FinNorte».

Es el ejemplo resuelto que construimos juntos en clase (corpus común en corpus/comun/).
Tu equipo construye lo mismo para SU variante en src/finnorte/variante.py.

    from finnorte.asistente import Asistente
    a = Asistente.crear()                                  # indexa corpus/comun
    a.responder("¿Cada cuánto se rotan los secretos?")     # dict listo para evaluación
"""
from __future__ import annotations

import time
from dataclasses import dataclass

from . import controles, llm, prompts, trazas
from .config import RAIZ
from .retrieval import Indice, contexto_para_prompt


@dataclass
class OpcionesAsistente:
    version_prompt: int | None = None   # None = la más reciente
    usar_rag: bool = True
    k: int = 4
    umbral: float = 0.35               # calíbralo con tus casos (T6): depende del proveedor de embeddings
    controles: bool = True             # citas + abstención + clasificación + saneo
    autocritica: bool = False          # una llamada extra por respuesta


class Asistente:
    def __init__(self, indice: Indice | None, opciones: OpcionesAsistente | None = None, prompt_id: str = "responder"):
        self.indice = indice
        self.op = opciones or OpcionesAsistente()
        self.prompt_id = prompt_id

    @classmethod
    def crear(cls, carpeta=RAIZ / "corpus" / "comun", **opciones) -> "Asistente":
        return cls(Indice.desde_carpeta(carpeta), OpcionesAsistente(**opciones))

    def responder(self, pregunta: str | dict) -> dict:
        if isinstance(pregunta, dict):
            pregunta = pregunta.get("pregunta", "")
        t0 = time.perf_counter()
        costo = 0.0
        recuperados = self.indice.buscar(pregunta, k=self.op.k) if self.op.usar_rag and self.indice else []
        salida = {"respuesta": controles.RESPUESTA_ABSTENCION, "fuentes": [], "abstuvo": True, "errores_citas": []}
        if self.op.controles:
            recuperados = controles.filtrar_clasificacion(recuperados)
            if self.op.usar_rag and controles.debe_abstenerse(recuperados, self.op.umbral):
                return self._cerrar(salida, pregunta, t0, costo, recuperados)
        p = prompts.cargar(self.prompt_id, self.op.version_prompt)
        valores = {"pregunta": pregunta, "contexto": contexto_para_prompt(recuperados) or "(sin contexto)"}
        sistema, usuario = p.render(**{k: valores[k] for k in p.variables})
        r = llm.generar(usuario, sistema, json=p.salida_json, etiqueta=p.nombre)
        costo = r.costo_usd
        from .pipeline import validar_esquema
        if p.salida_json and (not isinstance(r.datos, dict) or validar_esquema(r.datos, p.esquema)):
            salida["errores_citas"] = ["Salida JSON inválida"]
            return self._cerrar(salida, pregunta, t0, costo, recuperados)
        datos = r.datos if p.salida_json else {"respuesta": r.texto, "fuentes": [], "abstuvo": False}
        fuentes = datos.get("fuentes", [])
        errores = controles.verificar_citas(fuentes, recuperados)
        if self.op.controles and errores and not datos.get("abstuvo"):
            salida["errores_citas"] = errores
            return self._cerrar(salida, pregunta, t0, costo, recuperados)
        if self.op.controles and self.op.autocritica:
            revision = controles.autocritica(str(datos.get("respuesta", "")), valores["contexto"], pregunta)
            if not revision["soportada"]:
                salida["errores_citas"] = revision["problemas"]
                return self._cerrar(salida, pregunta, t0, costo, recuperados)
        texto = str(datos.get("respuesta", ""))
        if self.op.controles:
            texto, _ = controles.sanear_salida(texto)
        salida = {"respuesta": texto, "fuentes": fuentes, "abstuvo": bool(datos.get("abstuvo", False)),
                  "errores_citas": errores}
        return self._cerrar(salida, pregunta, t0, costo, recuperados)

    def _cerrar(self, salida: dict, pregunta: str, t0: float, costo: float, recuperados) -> dict:
        salida["latencia_ms"] = round((time.perf_counter() - t0) * 1000, 1)
        salida["costo_usd"] = costo
        salida["recuperados"] = [(r.fragmento.id, round(r.puntaje, 3)) for r in recuperados]
        trazas.registrar("respuesta", pregunta=pregunta[:200], abstuvo=salida["abstuvo"], fuentes=salida["fuentes"],
                         latencia_ms=salida["latencia_ms"], costo_usd=round(costo, 6))
        return salida
