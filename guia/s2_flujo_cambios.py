"""Guía S2 · Flujo de 4 etapas: solicitud de cambio → análisis → plan → checklist → nota.

    python guia/s2_flujo_cambios.py                    # con tu proveedor (.env)
    python guia/s2_flujo_cambios.py --plan-version 1   # fija la versión de cambio_plan (para comparar v1 vs v2)
    LLM_PROVIDER=fake python guia/s2_flujo_cambios.py  # sin red: respuestas de demostración

Qué hace
  1. Corre el flujo con 3 solicitudes (una clara, una ambigua y una de riesgo bajo).
  2. Valida cada salida contra su esquema JSON (y reintenta si falla).
  3. Imprime la matriz de trazabilidad: solicitud → etapa → artefacto → validación.
  4. Repite la solicitud 1 tres veces para ver la consistencia del riesgo asignado.
"""
import json
import os
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))


def _aviso_pendiente(tipo, valor, tb):
    """Si falta implementar una función del laboratorio, muestra un aviso claro en lugar del error largo."""
    if issubclass(tipo, NotImplementedError):
        print(f"\n✗ Falta implementar una función: {valor}.\n  Revisa el manual del laboratorio y corre las pruebas (pytest -q) antes de este script.")
        return
    sys.__excepthook__(tipo, valor, tb)


sys.excepthook = _aviso_pendiente

from finnorte import llm
from finnorte.config import config
from finnorte.pipeline import Etapa, Pipeline
from finnorte.retrieval import guardar_resultados


# Sin red (LLM_PROVIDER=fake): respuestas de demostración para ver el flujo completo.
_DEMO = {
    "analizar": {"titulo": "Idempotencia en transferencias", "componentes": ["pagos-api"], "tipo": "funcionalidad",
                 "riesgo": "alto", "justificacion_riesgo": "Toca movimiento de dinero", "preguntas_abiertas": []},
    "plan": {"estrategia": "canary", "pasos": ["5 %", "50 %", "100 %"], "reversa": "Desactivar la bandera y revertir",
             "aprobaciones": ["líder técnico", "operaciones"], "ventana": "martes 22:00"},
    "checklist": {"checklist": [{"punto": "Prueba con llave repetida", "origen": "analisis.componentes", "responsable": "qa"},
                                {"punto": "Reversa probada", "origen": "plan.reversa", "responsable": "ops"},
                                {"punto": "Canary observado 30 min", "origen": "plan.pasos", "responsable": "ops"}]},
    "nota": {"titulo": "Transferencias más seguras", "que_cambia": "Se evitan cobros duplicados",
             "impacto_usuario": "Ninguno visible", "fecha_estimada": "NO ESPECIFICADO", "contacto": "equipo de ingeniería"},
}


def _demo(prompt, sistema):
    if "Solicitud de cambio" in prompt:
        return json.dumps(_DEMO["analizar"])
    if "Reglas del plan" in prompt:
        return json.dumps(_DEMO["plan"])
    if "verificarse con un sí/no" in sistema:
        return json.dumps(_DEMO["checklist"])
    if "notas de liberación" in sistema:
        return json.dumps(_DEMO["nota"])
    return "{}"


if config().llm_proveedor == "fake":
    print("(Modo sin red: respuestas de demostración. Con tu llave verás respuestas reales.)\n")
    llm.fake.responder = _demo


def checklist_cubre_reversa(salida, previas):
    """Regla de negocio (código, no modelo): riesgo alto ⇒ el checklist incluye la reversa."""
    if previas.get("analizar", {}).get("riesgo") == "alto":
        if not any(i.get("origen", "").startswith("plan.reversa") for i in salida.get("checklist", [])):
            return ["Riesgo alto sin punto de checklist para la reversa (plan.reversa)"]
    return []


import argparse

from finnorte import prompts as _prompts

def _version_de(prompt_usado: str):
    """El pipeline registra el prompt como «id.vN»; si no trae versión, toma la más reciente."""
    import re as _re
    m = _re.search(r"\.v(\d+)", prompt_usado)
    vs = _prompts.versiones(prompt_usado.split(".")[0])
    return int(m.group(1)) if m else (max(vs) if vs else None)


_ap = argparse.ArgumentParser(description="Guía S2 · flujo de solicitudes de cambio")
_ap.add_argument("--plan-version", type=int, default=None, help="versión de cambio_plan (por defecto la más reciente)")
_ap.add_argument("--salida", default=None, help="nombre del archivo en bitacora/ (por defecto s2_trazabilidad_<versión>)")
_ap.add_argument("--continuar", action="store_true", help="Recuperar los casos y repeticiones ya guardados tras un error de red")
_ap.add_argument("--directorio", default="bitacora/lab2_comun_nuevo", help="Carpeta nueva para no sobrescribir evidencia histórica")
_args = _ap.parse_args()
os.environ["FINNORTE_DIR_TRAZAS"] = str(Path(__file__).resolve().parents[1] / _args.directorio)

FLUJO = Pipeline([
    Etapa("analizar", "cambio_analizar"),
    Etapa("plan", "cambio_plan", version=_args.plan_version, usa=["analizar"]),
    Etapa("checklist", "cambio_checklist", usa=["analizar", "plan"], validar=checklist_cubre_reversa),
    Etapa("nota", "cambio_nota", usa=["analizar", "plan"]),
], nombre="cambios")

SOLICITUDES = {
    "CHG-1": "Agregar validación de Idempotency-Key al endpoint POST /v1/transferencias de pagos-api para evitar cobros duplicados.",
    "CHG-2": "Mejorar el servicio de notificaciones.",
    "CHG-3": "Cambiar el texto del pie de página del portal de desarrolladores.",
}
matriz = []
_v = _args.plan_version or max(_prompts.versiones("cambio_plan"))
_nombre_salida = _args.salida or f"s2_trazabilidad_plan_v{_v}"
_ruta_matriz = config().dir_trazas / f"{_nombre_salida}.json"
if _ruta_matriz.exists() and not _args.continuar:
    _ap.error("Ya existe evidencia en esa carpeta; usa --continuar o un --directorio nuevo.")
if _args.continuar and _ruta_matriz.exists():
    matriz = json.loads(_ruta_matriz.read_text(encoding="utf-8"))
    matriz = [f for f in matriz if "modelo" in f and "artefacto" in f]
    if any(f.get("modelo") != config().llm_modelo or f.get("proveedor") != config().llm_proveedor for f in matriz):
        _ap.error("La matriz anterior usa otro modelo; no se pueden mezclar ejecuciones.")
todo_ok = True
for cid, sol in SOLICITUDES.items():
    anteriores = [f for f in matriz if f["solicitud"] == cid]
    if len(anteriores) == 4 and all(f["valida"] and "artefacto" in f for f in anteriores):
        print(f"{cid}: cuatro etapas recuperadas de la evidencia guardada")
        continue
    matriz = [f for f in matriz if f["solicitud"] != cid]
    res = FLUJO.ejecutar({"solicitud": sol})
    todo_ok = todo_ok and res.ok and len(res.etapas) == 4
    print(f"\n{cid}: {'OK' if res.ok else 'FALLÓ'} · US${res.costo_usd:.5f} · {res.latencia_ms:.0f} ms")
    for e in res.etapas:
        print(f"  {e.nombre:10s} {e.prompt:22s} intentos={e.intentos} {'OK' if e.ok else 'ERROR ' + '; '.join(e.errores[:2])}")
        matriz.append({"solicitud": cid, "etapa": e.nombre, "prompt": e.prompt, "version": _version_de(e.prompt),
                       "valida": e.ok, "intentos": e.intentos, "errores": e.errores[:2],
                       "artefacto": e.salida, "proveedor": config().llm_proveedor,
                       "modelo": config().llm_modelo, "demo": config().llm_proveedor == "fake"})
    if res.ok:
        print("  riesgo:", res.salidas["analizar"]["riesgo"], "· preguntas abiertas:", res.salidas["analizar"]["preguntas_abiertas"])
    guardar_resultados(_nombre_salida, matriz)

_ruta_consistencia = config().dir_trazas / f"s2_consistencia_plan_v{_v}.json"
guardadas = []
if _args.continuar and _ruta_consistencia.exists():
    guardadas = json.loads(_ruta_consistencia.read_text(encoding="utf-8"))
    if any(r.get("modelo") != config().llm_modelo for r in guardadas):
        _ap.error("Las repeticiones anteriores usan otro modelo.")
for n in range(len(guardadas), 3):
    r = FLUJO.ejecutar({"solicitud": SOLICITUDES["CHG-1"]})
    guardadas.append({"repeticion": n + 1, "riesgo": r.salidas.get("analizar", {}).get("riesgo"),
                      "flujo_completo": r.ok and len(r.etapas) == 4, "etapas": r.bitacora(),
                      "proveedor": config().llm_proveedor, "modelo": config().llm_modelo,
                      "demo": config().llm_proveedor == "fake"})
    guardar_resultados(f"s2_consistencia_plan_v{_v}", guardadas)
riesgos = [r["riesgo"] for r in guardadas]
todo_ok = todo_ok and all(r["flujo_completo"] for r in guardadas)
print("\nConsistencia de CHG-1 en 3 ejecuciones:", riesgos)
_v = _args.plan_version or max(_prompts.versiones("cambio_plan"))
print("Matriz guardada en", guardar_resultados(_args.salida or f"s2_trazabilidad_plan_v{_v}", matriz))
if not todo_ok:
    sys.exit(1)
