"""Agente con herramientas (T10): el modelo PROPONE una acción en JSON; tu código decide y la ejecuta.

Funciona igual con cualquier proveedor porque no depende del "function calling" nativo:
el modelo responde
  {"accion": "usar", "herramienta": "nombre", "argumentos": {...}, "razon": "..."}
o
  {"accion": "responder", "respuesta": "...", "fuentes": [...]}

Reglas que el código hace cumplir (no el modelo):
- Solo herramientas registradas; argumentos validados contra su esquema.
- Herramientas marcadas `sensible=True` requieren confirmación humana.
- Máximo de pasos para evitar bucles; todo queda en la bitácora.
"""
from __future__ import annotations

import json
from dataclasses import dataclass, field
from typing import Any, Callable

import jsonschema

from . import llm, trazas


@dataclass
class Herramienta:
    nombre: str
    descripcion: str
    esquema: dict                      # JSON Schema de los argumentos
    funcion: Callable[..., Any]
    sensible: bool = False             # requiere confirmación humana


@dataclass
class Paso:
    n: int
    propuesta: dict
    resultado: Any = None
    estado: str = ""                   # ejecutada | rechazada | pendiente | invalida | repetida | fallida | respuesta


@dataclass
class ResultadoAgente:
    respuesta: str
    fuentes: list
    pasos: list[Paso] = field(default_factory=list)
    terminado: bool = True


def _catalogo(herrs: dict[str, Herramienta]) -> str:
    return "\n".join(f"- {h.nombre}: {h.descripcion}. Argumentos (JSON Schema): {json.dumps(h.esquema, ensure_ascii=False)}"
                     + (" [SENSIBLE: requiere confirmación]" if h.sensible else "") for h in herrs.values())


SISTEMA_AGENTE = """Eres un asistente de ingeniería de FinNorte que resuelve tareas en pasos.
En cada turno devuelve SOLO un JSON con una de dos formas:
{{"accion": "usar", "herramienta": "<nombre>", "argumentos": {{...}}, "razon": "<por qué>"}}
{{"accion": "responder", "respuesta": "<respuesta final>", "fuentes": ["<id>", ...]}}
Herramientas disponibles:
{catalogo}
No inventes herramientas ni resultados. Si una herramienta falla, decide si reintentar o responder con lo que tienes."""


def ejecutar_agente(tarea: str, herramientas: list[Herramienta], confirmar: Callable[[Herramienta, dict], bool] | None = None,
                    max_pasos: int = 5, contexto: str = "") -> ResultadoAgente:
    herrs = {h.nombre: h for h in herramientas}
    sistema = SISTEMA_AGENTE.format(catalogo=_catalogo(herrs))
    historial: list[dict] = []
    pasos: list[Paso] = []
    mensaje = f"Tarea: {tarea}" + (f"\n\nContexto:\n{contexto}" if contexto else "")
    ya_usadas: set[str] = set()                       # detector de repeticiones: herramienta + argumentos

    for n in range(1, max_pasos + 1):
        r = llm.generar(mensaje, sistema, json=True, historial=historial, etiqueta=f"a4/agente/paso{n}")
        propuesta = r.datos if isinstance(r.datos, dict) else {}
        historial += [{"rol": "user", "texto": mensaje}, {"rol": "model", "texto": r.texto}]
        paso = Paso(n, propuesta)
        pasos.append(paso)

        # 1) El modelo decidió terminar
        if propuesta.get("accion") == "responder":
            paso.estado = "respuesta"
            trazas.registrar("agente", paso=n, estado="respuesta")
            return ResultadoAgente(str(propuesta.get("respuesta", "")), list(propuesta.get("fuentes") or []), pasos)

        # 2) El código revisa la propuesta y decide qué pasa
        paso.estado, mensaje = _revisar_y_ejecutar(propuesta, herrs, confirmar, ya_usadas, paso)
        trazas.registrar("agente", paso=n, herramienta=propuesta.get("herramienta"),
                         argumentos=propuesta.get("argumentos"), estado=paso.estado)

    # 3) Tope de pasos: se corta para evitar ciclos
    return ResultadoAgente("Se alcanzó el máximo de pasos sin terminar; se requiere revisión humana.", [], pasos,
                           terminado=False)


def _revisar_y_ejecutar(propuesta: dict, herrs: dict[str, Herramienta], confirmar, ya_usadas: set[str],
                        paso: Paso) -> tuple[str, str]:
    """Devuelve (estado del paso, mensaje para el modelo). Aquí decide el código, no el modelo."""
    nombre = propuesta.get("herramienta", "")
    h = herrs.get(nombre)
    if propuesta.get("accion") != "usar" or h is None:
        return "invalida", f"Acción inválida. Solo puedes usar {sorted(herrs)} o responder."

    args = propuesta.get("argumentos") or {}
    errores = [e.message for e in jsonschema.Draft202012Validator(h.esquema).iter_errors(args)]
    if errores:
        return "invalida", f"Argumentos inválidos para {nombre}: {errores[:3]}. Corrígelos."

    firma = nombre + json.dumps(args, sort_keys=True, ensure_ascii=False)
    if firma in ya_usadas:
        return "repetida", f"Ya usaste {nombre} con esos argumentos. Usa el resultado anterior o responde."

    if h.sensible:
        decision = confirmar(h, args) if confirmar else False   # sin quien confirme = no se ejecuta
        if decision is None:
            return "pendiente", f"{nombre} quedó PENDIENTE de autorización humana. No la repitas; responde avisando."
        if decision is not True:
            return "rechazada", f"La persona NO autorizó {nombre}. No la ejecutes; responde explicando."

    ya_usadas.add(firma)
    try:
        paso.resultado = h.funcion(**args)
    except Exception as e:                    # la falla regresa al modelo para que se recupere o escale
        paso.resultado = {"error": str(e)}
        return "fallida", f"La herramienta {nombre} falló: {e}. Corrige el argumento o responde que no se pudo."
    return "ejecutada", f"Resultado de {nombre}: {json.dumps(paso.resultado, ensure_ascii=False, default=str)[:3000]}"


# ═════════════════════ A4 · herramientas de la variante v2-revisor ═════════════════════
import subprocess  # noqa: E402
import sys  # noqa: E402

from .config import RAIZ  # noqa: E402

CARPETA_PERMITIDA = RAIZ / "datos"          # control: solo se revisan archivos de datos/
TIEMPO_MAX_S = 30                           # límite: el linter no puede tardar más de 30 s
# Traducción fija de las reglas de ruff (familia S = bandit) a las reglas SEC del corpus
RUFF_A_SEC = {"S105": "SEC-01", "S106": "SEC-01", "S107": "SEC-01",
              "S608": "SEC-02",
              "S110": "SEC-05", "S112": "SEC-05", "S113": "SEC-05",
              "S303": "SEC-06", "S324": "SEC-06", "S311": "SEC-06",
              "S301": "SEC-09", "S307": "SEC-09", "S506": "SEC-09", "S602": "SEC-09", "S603": "SEC-09",
              "S604": "SEC-09", "S605": "SEC-09"}
REVISIONES: list[dict] = []                 # revisiones publicadas (simulado, como el ticket del caso guía)

# Mejora 2 (A4, paso 5): el linter devuelve el texto de cada línea y las fuentes exactas (ids sec-XX) que se deben citar.
MOSTRAR_LINEA = True

# Mejora 1 (A4, paso 5): instrucciones propias de v2-revisor que se agregan al prompt del agente.
INSTRUCCIONES_REVISOR = """Eres el revisor de código de FinNorte (variante v2-revisor).
1. Primero usa correr_linter con la ruta EXACTA que dio la persona.
2. Solo menciona reglas SEC y líneas que aparezcan en el resultado del linter; no inventes otras.
3. Si el linter encontró hallazgos, el estado es cambios_requeridos; si no encontró nada, aprobado.
4. Si la tarea pide publicar, propone publicar_revision una sola vez; si la herramienta falla, responde que no se pudo.
5. En "fuentes" pon SOLO los ids de reglas que da el linter (por ejemplo "sec-06"), nunca la ruta del archivo.
   Si no hubo hallazgos, "fuentes" va vacío: []."""


def _ruta_segura(ruta: str):
    archivo = (RAIZ / ruta).resolve()
    if CARPETA_PERMITIDA.resolve() not in archivo.parents:
        raise ValueError(f"Solo se permiten archivos dentro de datos/: {ruta}")
    if archivo.suffix != ".py" or not archivo.is_file():
        raise FileNotFoundError(f"No existe el archivo Python {ruta}")
    return archivo


def correr_linter(ruta: str) -> dict:
    """Corre ruff (reglas de seguridad S) sobre un archivo. Lee el texto; NUNCA ejecuta el código revisado."""
    archivo = _ruta_segura(ruta)
    proc = subprocess.run([sys.executable, "-m", "ruff", "check", "--isolated", "--select", "S",
                           "--output-format", "json", str(archivo)],
                          capture_output=True, text=True, timeout=TIEMPO_MAX_S)
    salida = json.loads(proc.stdout or "[]")
    hallazgos = [{"regla_ruff": h["code"], "regla": RUFF_A_SEC.get(h["code"], "SIN-REGLA"),
                  "linea": h["location"]["row"], "mensaje": h["message"]} for h in salida]
    resultado = {"ruta": ruta, "total": len(hallazgos), "hallazgos": hallazgos}
    if MOSTRAR_LINEA:                       # Mejora 2: formato de salida más útil para el modelo
        lineas = archivo.read_text(encoding="utf-8").splitlines()
        for h in hallazgos:
            h["codigo_linea"] = lineas[h["linea"] - 1].strip()[:200]
        resultado["fuentes"] = sorted({h["regla"].lower() for h in hallazgos if h["regla"].startswith("SEC")})
    return resultado


def publicar_revision(ruta: str, estado: str, resumen: str) -> dict:
    """SENSIBLE: publica el dictamen de la revisión (simulado). Solo corre si una persona lo autoriza."""
    r = {"folio": f"REV-{len(REVISIONES) + 1:03d}", "ruta": ruta, "estado": estado, "resumen": resumen}
    REVISIONES.append(r)
    trazas.registrar("revision_publicada", **r)
    return r


USAR_INSTRUCCIONES = True                  # Mejora 1 activa (a4/correr_5_entradas.py --version 1 la apaga)


def ejecutar_agente_revisor(tarea: str, herramientas: list[Herramienta], confirmar=None, max_pasos: int = 5):
    """Mi ejecutor con las instrucciones de v2-revisor como contexto (se conecta en api/producto.py)."""
    return ejecutar_agente(tarea, herramientas, confirmar=confirmar, max_pasos=max_pasos,
                           contexto=INSTRUCCIONES_REVISOR if USAR_INSTRUCCIONES else "")


def herramientas_revisor() -> list[Herramienta]:
    ruta = {"type": "string", "pattern": r"^datos/[\w/.-]+\.py$", "maxLength": 200}
    return [
        Herramienta("correr_linter", "Revisa un archivo Python de datos/ con ruff (reglas de seguridad) sin ejecutarlo",
                    {"type": "object", "required": ["ruta"], "additionalProperties": False,
                     "properties": {"ruta": ruta}},
                    correr_linter),
        Herramienta("publicar_revision", "Publica el dictamen de la revisión de un archivo",
                    {"type": "object", "required": ["ruta", "estado", "resumen"], "additionalProperties": False,
                     "properties": {"ruta": ruta, "estado": {"enum": ["aprobado", "cambios_requeridos"]},
                                    "resumen": {"type": "string", "minLength": 10, "maxLength": 500}}},
                    publicar_revision, sensible=True),
    ]
