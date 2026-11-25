"""Controles contra errores del modelo (T5, T6, T11).

Cada control es una función pura y probable con pytest. Combínalos en tu flujo:
- verificar_citas: toda fuente citada debe existir entre los fragmentos recuperados.
- debe_abstenerse: si la recuperación no alcanza el umbral, no se llama al modelo.
- autocritica: una segunda llamada revisa la respuesta contra el contexto (cuesta otra llamada).
- filtrar_clasificacion: nunca pasar documentos confidenciales al prompt.
- sanear_salida: quita enlaces/imágenes externas y PII antes de mostrar (T11).
- opcional: usa un control del Avance 2 sin que tu motor truene mientras no lo implementas.
"""
from __future__ import annotations

import re
from typing import Iterable

from . import llm, pii
from .retrieval import Resultado

def opcional(funcion, *args, por_defecto, **kwargs):
    """Llama a un control que quizá aún no implementas (p. ej. los del Avance 2).

    Si la función todavía lanza NotImplementedError, devuelve `por_defecto` y tu flujo sigue.
    Ejemplo: respuesta, avisos = controles.opcional(controles.sanear_salida, respuesta, por_defecto=(respuesta, []))
    """
    try:
        return funcion(*args, **kwargs)
    except NotImplementedError:
        return por_defecto


RESPUESTA_ABSTENCION = "No encuentro esa información en la documentación disponible. Te sugiero consultarlo con el área responsable."


def verificar_citas(fuentes_citadas: Iterable[str], recuperados: list[Resultado]) -> list[str]:
    """Errores por citas inventadas o ausentes. Acepta 'doc#n' o solo 'doc'."""
    validas = {v for r in recuperados for v in (r.fragmento.id, r.fragmento.doc_id)}
    fuentes = [str(f).strip().removeprefix("doc:") for f in (fuentes_citadas or [])]
    errores = [f"Cita no recuperada: {f}" for f in fuentes if f not in validas]
    if recuperados and not fuentes:
        errores.append("La respuesta no cita ninguna fuente")
    return errores


def debe_abstenerse(recuperados: list[Resultado], umbral: float) -> bool:
    """True si no hay contexto suficiente para responder."""
    return not recuperados or recuperados[0].puntaje < umbral


def filtrar_clasificacion(recuperados: list[Resultado], permitidas=("publica", "interna")) -> list[Resultado]:
    return [r for r in recuperados if r.fragmento.clasificacion in permitidas
            and str(r.fragmento.meta.get("vigente", "si")).lower() not in ("no", "false", "obsoleto")]


def sanear_salida(texto: str, dominios_permitidos=("finnorte.mx",)) -> tuple[str, list[str]]:
    """Quita imágenes/enlaces a dominios ajenos y enmascara PII. Devuelve (texto, avisos)."""
    from urllib.parse import urlsplit
    avisos = []
    def limpiar_url(m):
        host = (urlsplit(m.group(0)).hostname or "").lower()
        if any(host == d or host.endswith("." + d) for d in dominios_permitidos):
            return m.group(0)
        avisos.append("Se eliminó una URL externa")
        return "<URL_ELIMINADA>"
    texto = re.sub(r"!\[[^\]]*\]\([^)]*\)", "<IMAGEN_ELIMINADA>", texto)
    if "<IMAGEN_ELIMINADA>" in texto:
        avisos.append("Se eliminó una imagen")
    texto = re.sub(r"https?://[^\s<>\"')]+", limpiar_url, texto)
    texto, mapa = pii.enmascarar(texto)
    if mapa:
        avisos.append("Se enmascararon datos personales")
    return texto, avisos


def autocritica(respuesta: str, contexto: str, pregunta: str) -> dict:
    """Pide al modelo que verifique su propia respuesta contra el contexto. Devuelve
    {"soportada": bool, "problemas": [...]}; si el JSON falla, asume no soportada."""
    sistema = ("Eres un verificador estricto. Solo juzgas si cada afirmación de la RESPUESTA está respaldada "
               "por el CONTEXTO. No uses conocimiento externo.")
    usuario = (f"CONTEXTO:\n{contexto}\n\nPREGUNTA: {pregunta}\n\nRESPUESTA:\n{respuesta}\n\n"
               'Devuelve JSON: {"soportada": true|false, "problemas": ["afirmación sin respaldo", ...]}')
    r = llm.generar(usuario, sistema, json=True, temperatura=0.0, etiqueta="control/autocritica")
    d = r.datos if isinstance(r.datos, dict) else {}
    return {"soportada": bool(d.get("soportada", False)), "problemas": list(d.get("problemas", []))}
