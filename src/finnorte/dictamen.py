"""Etapa 4: dictamen. El modelo redacta; el código decide si el reporte es fiel."""
from __future__ import annotations

import re
import unicodedata

AVISO_FALLIDA = "REVISIÓN FALLIDA: {motivo}. No se emite dictamen; se requiere revisión humana."
_CAMPOS_HALLAZGO = ("regla", "linea", "descripcion", "explicacion")
_AFIRMA_CIERRE = re.compile(
    r"\b(?:ya\s+)?(?:se\s+corrigi|fue\s+corregid|fueron\s+corregid|qued[oó]\s+corregid|ya\s+est[aá]\s+corregid"
    r"|se\s+aplic|fue\s+aplicad|es\s+seguro|está\s+aprobad|esta\s+aprobad)", re.I)
# Palabras neutras del reporte. Las de contenido deben venir de los datos recibidos.
_VOCABULARIO_REPORTE = {"encontro", "encontraron", "identifico", "identificaron", "identificado", "identificados",
                        "hallazgo", "hallazgos", "regla", "reglas", "linea", "lineas", "codigo", "fuente", "analizado",
                        "parche", "parches", "propuesta", "propuestas", "propuesto", "propuestos", "requiere",
                        "requieren", "revision", "humana", "incumple", "incumplen", "relacionado", "relacionada",
                        "relacionados", "relacionadas", "estos", "estas", "mismo", "misma", "contra", "total"}


def _palabras(texto):
    limpio = "".join(c for c in unicodedata.normalize("NFD", texto.lower()) if unicodedata.category(c) != "Mn")
    return {p for p in re.findall(r"[a-z]{5,}", limpio)}


def _texto_recibido(esperados, cambios):
    return " ".join([h[c] for h in esperados for c in ("descripcion", "explicacion")] + list(cambios.values()))


def _datos_ajenos(resumen, esperados, cambios):
    errores = []
    reglas = {h["regla"] for h in esperados}
    lineas = {h["linea"] for h in esperados}
    ids = {h["id"] for h in esperados}
    for regla in sorted(set(re.findall(r"\bSEC-\d{2}\b", resumen)) - reglas):
        errores.append(f"El resumen menciona {regla}, que no está en los hallazgos recibidos")
    for hallazgo in sorted(set(re.findall(r"\bH[1-9]\d*\b", resumen)) - ids):
        errores.append(f"El resumen menciona {hallazgo}, que no está en los hallazgos recibidos")
    for texto in re.findall(r"\bl[ií]neas?\s*:?\s*(\d+)\b", resumen, re.I):
        if int(texto) not in lineas:
            errores.append(f"El resumen menciona la línea {texto}, que no está en los hallazgos recibidos")
    if re.search(r"\bsk_live_[A-Za-z0-9_-]{4,}", resumen) or re.search(r"(?<!\d)\d{18}(?!\d)", resumen):
        errores.append("El resumen reproduce una credencial o 18 dígitos; usa una referencia enmascarada")
    if _AFIRMA_CIERRE.search(resumen):
        errores.append("El resumen presenta una propuesta como aplicada o aprobada; los parches son propuestas")
    if esperados:
        for regla in sorted(reglas - set(re.findall(r"\bSEC-\d{2}\b", resumen))):
            errores.append(f"El resumen omite {regla}")
        if str(len(esperados)) not in re.findall(r"\d+", resumen):
            errores.append(f"El resumen no indica el total de {len(esperados)} hallazgos")
        ajenas = _palabras(resumen) - _palabras(_texto_recibido(esperados, cambios)) - _VOCABULARIO_REPORTE
        if ajenas:
            errores.append("El resumen agrega texto que no está en los datos recibidos: " + ", ".join(sorted(ajenas)))
    return errores


def validar_dictamen(salida, previas):
    """Compara el reporte con las salidas reales de explicar y parche, campo por campo."""
    esperados = {h["id"]: h for h in previas["explicar"]["hallazgos"]}
    cambios = {p["id"]: p["cambio"] for p in previas["parche"]["parches"]}
    recibidos = salida["hallazgos"]
    ids = [h["id"] for h in recibidos]
    errores = []
    for repetido in sorted({i for i in ids if ids.count(i) > 1}):
        errores.append(f"{repetido} aparece más de una vez en el reporte")
    for faltante in sorted(set(esperados) - set(ids)):
        errores.append(f"El reporte omite {faltante}")
    for inventado in sorted(set(ids) - set(esperados)):
        errores.append(f"El reporte inventa {inventado}; no existe en explicar")
    for h in recibidos:
        original = esperados.get(h["id"])
        if original is None:
            continue
        for campo in _CAMPOS_HALLAZGO:
            if h[campo] != original[campo]:
                errores.append(f"{h['id']}: cambió {campo}; debe copiarse exacto")
        if h.get("fuente") != original.get("fuente"):
            errores.append(f"{h['id']}: cambió fuente; debe copiarse exacta")
        if h["id"] not in cambios:
            errores.append(f"{h['id']}: no tiene parche en la etapa anterior")
        elif h["cambio"] != cambios[h["id"]]:
            errores.append(f"{h['id']}: cambió cambio; debe copiarse exacto")
    if salida["total_hallazgos"] != len(esperados):
        errores.append(f"total_hallazgos es {salida['total_hallazgos']}; se recibieron {len(esperados)}")
    if salida["estado"] != ("con_hallazgos" if esperados else "sin_hallazgos"):
        errores.append(f"estado {salida['estado']} no coincide con {len(esperados)} hallazgos recibidos")
    if not esperados and salida["resumen"] != "sin hallazgos":
        errores.append('Sin hallazgos, resumen debe ser exactamente "sin hallazgos"')
    return errores + _datos_ajenos(salida["resumen"], list(esperados.values()), cambios)


def reporte_final(resultado):
    """Texto para quien revisa: hallazgos, «sin hallazgos» o aviso de revisión fallida.

    Lo arma el programa, no el modelo, y solo con un dictamen que pasó la validación.
    """
    fallida = next((e for e in resultado.etapas if not e.ok), None)
    if fallida is not None:
        return AVISO_FALLIDA.format(motivo=f"la etapa {fallida.nombre} no pasó la validación")
    dictamen = resultado.salidas.get("dictamen")
    if not isinstance(dictamen, dict):
        return AVISO_FALLIDA.format(motivo="el flujo terminó sin dictamen")
    if dictamen["estado"] == "sin_hallazgos":
        return "sin hallazgos"
    lineas = [dictamen["resumen"], ""]
    for h in dictamen["hallazgos"]:
        lineas += [f"{h['id']} · {h['regla']} · línea {h['linea']}: {h['descripcion']}",
                   f"  Explicación: {h['explicacion']}", f"  Parche propuesto: {h['cambio']}"]
        if h.get("fuente"):
            lineas.append(f"  Fuente: {h['fuente']}")
    return "\n".join(lineas)
