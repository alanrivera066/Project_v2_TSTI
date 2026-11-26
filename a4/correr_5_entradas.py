"""A4 · Pasos 3 y 5: corre el agente de v2-revisor sobre las MISMAS 5 entradas y guarda salidas y trazas.

    python a4/correr_5_entradas.py --version 1     # primera ejecución, sin las 2 mejoras
    python a4/correr_5_entradas.py --version 2     # después de las 2 mejoras (mismas 5 entradas)

Necesita tu llave de Gemini en .env (LLM_PROVIDER=gemini). Guarda bitacora/a4/v<N>.json.
"""
import argparse
import json
import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[1]
sys.path[:0] = [str(RAIZ / "src"), str(RAIZ)]

from finnorte import agente_servicio, herramientas  # noqa: E402
from finnorte.validador_revisor import validar_plan_revisor  # noqa: E402

ENTRADAS = ["usuarios.py", "transferencias.py", "reportes.py", "tokens.py", "limites.py"]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--version", type=int, choices=[1, 2], required=True)
    v = ap.parse_args().version
    herramientas.USAR_INSTRUCCIONES = herramientas.MOSTRAR_LINEA = (v == 2)   # las 2 mejoras
    resultados = []
    for nombre in ENTRADAS:
        ruta = f"datos/v2-revisor/codigo/{nombre}"
        tarea = f"Revisa {ruta} con el linter y publica la revisión con el estado que corresponda."
        out = agente_servicio.iniciar(tarea, "a4-script", herramientas.herramientas_revisor(),
                                      ejecutor=herramientas.ejecutar_agente_revisor, validador=validar_plan_revisor)
        resultados.append({"entrada": ruta, **out})
        estados = " → ".join(f"{p['herramienta'] or p['accion']}:{p['estado']}" for p in out["pasos"])
        print(f"{nombre:18} | validador {'OK ' if out['validador']['ok'] else 'NO '} | pendientes {len(out['pendientes'])} | {estados}")
        for h in out["validador"]["hallazgos"]:
            print(f"{'':18}   ↳ {h}")
    destino = RAIZ / "bitacora" / "a4" / f"v{v}.json"
    destino.parent.mkdir(parents=True, exist_ok=True)
    destino.write_text(json.dumps(resultados, ensure_ascii=False, indent=2, default=str), encoding="utf-8")
    print(f"\nGuardado en {destino.relative_to(RAIZ)}. Traza del agente: bitacora/trazas.jsonl")


if __name__ == "__main__":
    main()
