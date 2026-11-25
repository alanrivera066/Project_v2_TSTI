"""Detección y enmascaramiento de datos personales (T11).

Detecta con patrones: correo, teléfono MX, CURP, RFC, CLABE (18 dígitos), tarjeta (Luhn)
y bloques marcados como CONFIDENCIAL. Es un detector de juguete: mide su tasa de aciertos
con tus propios casos antes de confiar en él (por ejemplo, no ve direcciones en texto libre).
"""
from __future__ import annotations

import re

PATRONES = {
    "CORREO": r"[\w.+-]+@[\w-]+\.[\w.-]+",
    "CURP": r"\b[A-Z][AEIOUX][A-Z]{2}\d{6}[HM][A-Z]{5}[A-Z0-9]\d\b",
    "RFC": r"\b[A-ZÑ&]{3,4}\d{6}[A-Z0-9]{3}\b",
    "CLABE": r"\b\d{18}\b",
    "TARJETA": r"\b(?:\d[ -]?){13,19}\b",
    "TELEFONO": r"(?<!\d)(?:\+?52[ -]?)?(?:\d{2}[ -]?\d{4}[ -]?\d{4}|\d{3}[ -]?\d{3}[ -]?\d{4})(?!\d)",
}
BLOQUE_CONF = re.compile(r"\[CONFIDENCIAL\].*?\[/CONFIDENCIAL\]", re.S)


def _luhn(numero: str) -> bool:
    d = [int(c) for c in re.sub(r"\D", "", numero)][::-1]
    if not 13 <= len(d) <= 19:
        return False
    s = sum(x if i % 2 == 0 else (x * 2 - 9 if x * 2 > 9 else x * 2) for i, x in enumerate(d))
    return s % 10 == 0


def detectar(texto: str) -> list[tuple[str, str]]:
    """Lista de (tipo, valor) encontrados."""
    hallazgos = [("CONFIDENCIAL", m.group(0)[:40] + "…") for m in BLOQUE_CONF.finditer(texto)]
    for tipo, patron in PATRONES.items():
        for m in re.finditer(patron, texto):
            valor = m.group(0).strip()
            if tipo == "TARJETA" and not _luhn(valor):
                continue
            if tipo == "TARJETA" and len(re.sub(r"\D", "", valor)) == 18:
                continue  # es CLABE
            hallazgos.append((tipo, valor))
    return hallazgos


def enmascarar(texto: str) -> tuple[str, dict[str, str]]:
    """Reemplaza PII por marcadores <TIPO_n>. Devuelve (texto_enmascarado, mapa marcador→valor)."""
    mapa = {}
    intervalos = [(m.start(), m.end(), "CONFIDENCIAL") for m in BLOQUE_CONF.finditer(texto)]
    for tipo, patron in PATRONES.items():
        for m in re.finditer(patron, texto):
            if tipo == "TARJETA" and (not _luhn(m.group()) or len(re.sub(r"\D", "", m.group())) == 18):
                continue
            intervalos.append((m.start(), m.end(), tipo))
    elegidos = []
    for ini, fin, tipo in sorted(intervalos, key=lambda x: (x[0], -(x[1]-x[0]))):
        if not elegidos or ini >= elegidos[-1][1]:
            elegidos.append((ini, fin, tipo))
    for ini, fin, tipo in reversed(elegidos):
        marcador = f"<{tipo}_{len(mapa) + 1}>"
        mapa[marcador] = texto[ini:fin]
        texto = texto[:ini] + marcador + texto[fin:]
    return texto, mapa


def contiene_pii(texto: str) -> bool:
    return bool(detectar(texto))
