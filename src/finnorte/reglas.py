"""Validaciones del Lab 2. Compilar comprueba sintaxis; nunca ejecuta el archivo recibido."""
from __future__ import annotations

import ast
import json
import re
from dataclasses import replace
from functools import partial

from .pipeline import Pipeline

REGLAS_SEC = {f"SEC-{i:02}" for i in range(1, 11)}
REVISION_VALIDADORES = "lab2-revision-4"
_SENSIBLE = re.compile(r"clabe|curp|password|passwd|api_key|token|correo|email|telefono|tarjeta", re.I)
_NIVELES_LOG = {"debug", "info", "warning", "warn", "error", "exception", "critical", "log"}


def _enmascarado(nodo):
    if isinstance(nodo, ast.Subscript) and isinstance(nodo.slice, ast.Slice):
        inicio = nodo.slice.lower
        if (nodo.slice.upper is None and nodo.slice.step is None and isinstance(inicio, ast.UnaryOp)
                and isinstance(inicio.op, ast.USub) and isinstance(inicio.operand, ast.Constant)
                and isinstance(inicio.operand.value, int) and 1 <= inicio.operand.value <= 4):
            return True
    if isinstance(nodo, ast.Call):
        nombre = getattr(nodo.func, "id", getattr(nodo.func, "attr", ""))
        return bool(re.search(r"enmascar|redact|anonimiz|mask", nombre, re.I))
    return False


def _sensible_sin_mascara(nodo):
    if _enmascarado(nodo):
        return False
    if isinstance(nodo, ast.Name):
        return bool(_SENSIBLE.search(nodo.id))
    if isinstance(nodo, ast.Subscript) and isinstance(nodo.slice, ast.Constant):
        if isinstance(nodo.slice.value, str) and _SENSIBLE.search(nodo.slice.value):
            return True
    if isinstance(nodo, ast.Constant) and isinstance(nodo.value, str):
        return bool(re.search(r"(?<!\d)\d{18}(?!\d)", nodo.value))
    return any(_sensible_sin_mascara(hijo) for hijo in ast.iter_child_nodes(nodo))


def registros_del_codigo(codigo):
    """Heurística estática acotada, sin ejecutar Python. No es un detector universal de PII.

    Reconoce print y métodos habituales de logging, incluso llamadas multilínea.
    Solo exige cobertura para nombres/campos sensibles o CLABE literal reconocibles;
    los últimos cuatro caracteres y funciones explícitas de enmascarado se excluyen.
    """
    try:
        arbol = ast.parse(codigo)
    except SyntaxError:
        return []
    registros = []
    for nodo in ast.walk(arbol):
        if not isinstance(nodo, ast.Call):
            continue
        f = nodo.func
        es_log = (isinstance(f, ast.Name) and f.id in {"print", "log"}) or (
            isinstance(f, ast.Attribute) and f.attr in _NIVELES_LOG)
        if es_log:
            valores = [*nodo.args, *(k.value for k in nodo.keywords)]
            registros.append({"inicio": nodo.lineno, "fin": nodo.end_lineno or nodo.lineno,
                              "sensible": any(_sensible_sin_mascara(a) for a in valores)})
    return registros


def _identidad(hallazgo):
    return hallazgo["id"], hallazgo["regla"], hallazgo["linea"]


def validar_detectar(salida, previas, *, codigo):
    errores = []
    vistos = set()
    ubicaciones = set()
    total = len(codigo.splitlines())
    registros = registros_del_codigo(codigo)
    for h in salida["hallazgos"]:
        if not 1 <= h["linea"] <= total:
            errores.append(f"La línea {h['linea']} no existe; el archivo tiene {total} líneas")
        if h["regla"] not in REGLAS_SEC:
            errores.append(f"Regla no permitida: {h['regla']}")
        if h["regla"] == "SEC-03" and 1 <= h["linea"] <= total:
            if not any(r["inicio"] <= h["linea"] <= r["fin"] for r in registros):
                errores.append(f"SEC-03 en línea {h['linea']} no corresponde a print o logging")
        if h["id"] in vistos or (h["regla"], h["linea"]) in ubicaciones:
            errores.append("Hay hallazgos duplicados por id o por regla y línea")
        vistos.add(h["id"])
        ubicaciones.add((h["regla"], h["linea"]))
    for r in registros:
        if r["sensible"] and not any(h["regla"] == "SEC-03" and r["inicio"] <= h["linea"] <= r["fin"]
                                    for h in salida["hallazgos"]):
            errores.append(f"Falta SEC-03: registro con dato sensible sin enmascarar en línea {r['inicio']}")
    return errores


def validar_explicar(salida, previas):
    originales = previas["detectar"]["hallazgos"]
    recibidas = salida["hallazgos"]
    if sorted(map(_identidad, originales)) != sorted(map(_identidad, recibidas)):
        return ["La explicación debe conservar todos los ids, reglas y líneas, sin agregar ni quitar hallazgos"]
    originales_por_id = {h["id"]: h for h in originales}
    errores = [f"La explicación cambió la descripción original de {h['id']}"
               for h in recibidas if h["descripcion"] != originales_por_id[h["id"]]["descripcion"]]
    for h in recibidas:
        if h["regla"] not in h["explicacion"]:
            errores.append(f"La explicación de {h['id']} debe identificar su regla SEC")
        if not re.search(rf"\b(?:l[ií]nea\s*:?\s*|L\s*){h['linea']}\b", h["explicacion"], re.I):
            errores.append(f"La explicación de {h['id']} no identifica la línea {h['linea']}; el texto debe ser trazable por sí solo")
        if re.search(r"\bsk_live_[A-Za-z0-9_-]{4,}", h["explicacion"]):
            errores.append(f"La explicación de {h['id']} reproduce una credencial sk_live completa; usa una referencia enmascarada")
        if re.search(r"(?<!\d)\d{18}(?!\d)", h["explicacion"]):
            errores.append(f"La explicación de {h['id']} reproduce 18 dígitos completos; no muestres la CLABE completa")
    return errores


def validar_parche(salida, previas, *, codigo):
    esperados = previas["explicar"]["hallazgos"]
    errores = []
    if sorted(map(_identidad, esperados)) != sorted(map(_identidad, salida["parches"])):
        errores.append("Debe haber un parche por hallazgo, conservando id, regla y línea original")
    if not esperados and salida["codigo_corregido"] != codigo:
        errores.append("Sin hallazgos se debe conservar exactamente el código original")
    try:
        compile(salida["codigo_corregido"], "<parche-no-ejecutado>", "exec")
    except (SyntaxError, ValueError, TypeError) as error:
        errores.append(f"El código corregido no compila: {error}")
    return errores




class FlujoRevisor(Pipeline):
    """Vincula los validadores al archivo real de cada ejecución, sin estado global compartido.

    El modelo recibe líneas numeradas por código. Los validadores reciben el original,
    no una copia inventada por el modelo. La interfaz sigue siendo ejecutar(entrada).
    """

    def ejecutar(self, entrada, detener_en_error=True):
        codigo = entrada["entrada"]
        if not isinstance(codigo, str):
            raise TypeError("entrada debe contener el código Python como texto")
        etapas = []
        for etapa in self.etapas:
            validador = etapa.validar
            if etapa.nombre == "detectar":
                validador = partial(validar_detectar, codigo=codigo)
            elif etapa.nombre == "parche":
                validador = partial(validar_parche, codigo=codigo)
            etapas.append(replace(etapa, validar=validador))
        valores = {**entrada, "codigo_original": codigo,
                   "codigo_original_json": json.dumps(codigo, ensure_ascii=False),
                   "senales_codigo": json.dumps([{"regla": "SEC-03", "linea": r["inicio"],
                       "motivo": "registro con campo sensible reconocible sin enmascarar"}
                       for r in registros_del_codigo(codigo) if r["sensible"]], ensure_ascii=False),
                   "entrada": "\n".join(f"{n}: {linea}" for n, linea in enumerate(codigo.splitlines(), 1))}
        return Pipeline(etapas, nombre=self.nombre).ejecutar(valores, detener_en_error)
