"""A4 · Validador de la variante v2-revisor (lógica tradicional, sin IA).

Comprueba, en cada respuesta:
  1. Cada hallazgo cita una regla SEC que existe en corpus/v2-revisor.
  2. Cada hallazgo apunta a una línea que existe en el código.
  3. limites.py debe tener cero hallazgos (es el archivo limpio de referencia).
  4. Sin información externa: las fuentes citadas existen en el corpus y el resumen de una
     revisión solo menciona reglas que el linter encontró.
Devuelve una lista de problemas; lista vacía = todo bien.
"""
from __future__ import annotations

import re
from pathlib import Path

from .config import RAIZ


def reglas_existentes() -> set[str]:
    return {p.name[:6].upper() for p in (RAIZ / "corpus" / "v2-revisor").glob("sec-*.md")}


def validar_hallazgos(codigo: str, hallazgos: list[dict], archivo: str = "", fuentes: list[str] = ()) -> list[str]:
    problemas = []
    reglas = reglas_existentes()
    total_lineas = len(codigo.splitlines())
    for h in hallazgos:
        if h.get("regla") not in reglas:
            problemas.append(f"Regla inexistente: {h.get('regla')}")
        linea = h.get("linea")
        if not isinstance(linea, int) or not 1 <= linea <= total_lineas:
            problemas.append(f"Línea inexistente: {linea} (el código tiene {total_lineas})")
    if Path(archivo).name == "limites.py" and hallazgos:
        problemas.append(f"limites.py debe tener 0 hallazgos y tiene {len(hallazgos)}")
    ids_corpus = {r.lower() for r in reglas}
    for f in fuentes:
        if f.removeprefix("doc:").split("#")[0].lower() not in ids_corpus:
            problemas.append(f"Fuente que no está en el corpus: {f}")
    return problemas


def validar_plan_revisor(resultado, propuestas: list[tuple[str, dict]]) -> list[str]:
    """Validador del agente: una revisión solo se ofrece para publicar si el linter revisó ESE archivo
    en esta ejecución, sus hallazgos pasan validar_hallazgos y el dictamen es coherente con ellos."""
    linter = {p.propuesta.get("argumentos", {}).get("ruta"): p.resultado for p in resultado.pasos
              if p.propuesta.get("herramienta") == "correr_linter" and p.estado == "ejecutada"}
    problemas = []
    for nombre, args in propuestas:
        if nombre != "publicar_revision":
            continue
        ruta = args.get("ruta")
        if ruta not in linter:
            problemas.append(f"{ruta} no pasó por correr_linter en esta ejecución")
            continue
        hallazgos = linter[ruta]["hallazgos"]
        codigo = (RAIZ / ruta).read_text(encoding="utf-8")
        problemas += validar_hallazgos(codigo, hallazgos, ruta)
        if args.get("estado") == "aprobado" and hallazgos:
            problemas.append(f"Se quiere aprobar {ruta} pero el linter encontró {len(hallazgos)} hallazgos")
        encontradas = {h["regla"] for h in hallazgos}
        externas = set(re.findall(r"SEC-\d{2}", args.get("resumen", ""))) - encontradas
        if externas:
            problemas.append(f"El resumen menciona reglas que el linter no encontró: {sorted(externas)}")
    fuentes = getattr(resultado, "fuentes", []) or []
    problemas += validar_hallazgos("", [], fuentes=fuentes)
    return problemas
