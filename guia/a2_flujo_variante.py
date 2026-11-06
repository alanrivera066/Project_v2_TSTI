"""Lab 2: tres archivos, tres repeticiones y matriz generada por código.

Sin --demo usa el proveedor real de .env. --demo solo comprueba el mecanismo con
respuestas preparadas; escribe en bitacora/demo y no sustituye la medición con Gemini.
"""
import argparse
import hashlib
import json
import os
import sys
from datetime import datetime, timezone
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(RAIZ / "src"))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--v1", action="store_true", help="Fijar la versión inicial de todos los prompts")
    parser.add_argument("--demo", action="store_true", help="Respuestas preparadas; no mide calidad de IA")
    parser.add_argument("--continuar", action="store_true", help="Recuperar los casos guardados si el proveedor interrumpió la ejecución")
    parser.add_argument("--salida", default="bitacora/publicacion_lab2/flujo", help="Carpeta nueva para conservar las matrices anteriores")
    args = parser.parse_args()
    if args.demo:
        os.environ.update(LLM_PROVIDER="fake", LLM_MODEL="fake-1",
                          FINNORTE_DIR_TRAZAS=str(RAIZ / "bitacora" / "demo"))

    from finnorte import llm, trazas
    from finnorte import prompts
    from finnorte.reglas import REVISION_VALIDADORES
    from finnorte.config import config
    from finnorte.variante import FLUJO, FLUJO_V1, leer_entrada

    cfg = config()
    if not args.demo:
        os.environ["FINNORTE_DIR_TRAZAS"] = str(RAIZ / args.salida)
        cfg = config()
    if cfg.llm_proveedor == "fake" and not args.demo:
        parser.error("Configura Gemini en .env o usa --demo para probar sin conexión.")
    if cfg.llm_proveedor == "gemini" and not cfg.gemini_key:
        parser.error("Falta GEMINI_API_KEY en .env. No pegues la llave en el chat ni en GitHub.")

    entradas = ["transferencias.py", "tokens.py", "limites.py"]
    flujo = FLUJO_V1 if args.v1 else FLUJO
    huella = {"validadores": REVISION_VALIDADORES, "prompts": {},
              "codigo": {n: hashlib.sha256((RAIZ / "src/finnorte" / n).read_bytes()).hexdigest()
                         for n in ("reglas.py", "pipeline.py", "dictamen.py")},
              "entradas": {n: hashlib.sha256((RAIZ / "datos/v2-revisor/codigo" / n).read_bytes()).hexdigest()
                           for n in entradas}}
    for etapa in flujo.etapas:
        p = prompts.cargar(etapa.prompt, etapa.version)
        ruta_prompt = RAIZ / "prompts" / f"{p.nombre}.md"
        huella["prompts"][p.nombre] = hashlib.sha256(ruta_prompt.read_bytes()).hexdigest()
    cfg.dir_trazas.mkdir(parents=True, exist_ok=True)
    filas, corridas = [], []
    sufijo = "_v1" if args.v1 else ""
    archivo_datos = cfg.dir_trazas / f"a2_trazabilidad{sufijo}.json"
    if archivo_datos.exists() and not args.continuar and not args.demo:
        parser.error("Ya hay evidencia: usa --continuar o una --salida nueva.")
    if args.continuar and archivo_datos.exists():
        anterior = json.loads(archivo_datos.read_text(encoding="utf-8"))
        if (anterior["modelo"], anterior["proveedor"], anterior["demo"]) != (cfg.llm_modelo, cfg.llm_proveedor, args.demo):
            parser.error("La evidencia anterior usa otro modelo o modo; no se pueden mezclar las ejecuciones.")
        if anterior.get("huella") != huella:
            parser.error("Cambió un prompt o los validadores: inicia una medición nueva, sin --continuar.")
        filas, corridas = anterior["filas"], anterior["corridas"]

    def guardar_parcial():
        archivo_datos.write_text(json.dumps({"fecha_utc": datetime.now(timezone.utc).isoformat(),
            "demo": args.demo, "proveedor": cfg.llm_proveedor, "modelo": cfg.llm_modelo,
            "sin_rag": True, "huella": huella, "filas": filas, "corridas": corridas,
            "estado": "parcial; falta terminar la matriz y las repeticiones"},
            ensure_ascii=False, indent=2), encoding="utf-8")
        lineas = ["# Laboratorio 2: matriz parcial", "",
                  "Ejecución parcial: faltan casos o repeticiones. No acredita el checkpoint completo.",
                  f"Proveedor: {cfg.llm_proveedor}; modelo: {cfg.llm_modelo}; demo: {args.demo}.", "",
                  "| Entrada | Repetición | Etapa | Prompt | Artefacto | Válida | Intentos | Errores |",
                  "|---|---|---|---|---|---|---|---|"]
        for f in filas:
            valores = [f[k] for k in ("entrada", "repeticion", "etapa", "prompt", "artefacto", "valida", "intentos", "errores")]
            lineas.append("| " + " | ".join(str(v).replace("|", "/").replace("\n", " ") for v in valores) + " |")
        (cfg.dir_trazas / f"a2_matriz{sufijo}.md").write_text("\n".join(lineas) + "\n", encoding="utf-8")
    demo_respuestas = None
    if args.demo:
        from demo_revisor import respuestas_para
        demo_respuestas = respuestas_para

    def ejecutar(nombre, repeticion):
        anteriores = [c for c in corridas if c["entrada"] == nombre and c["repeticion"] == repeticion]
        if anteriores:
            print(f"{nombre} / {repeticion}: evidencia recuperada ({anteriores[-1]['estado']})")
            return anteriores[-1]["resultado"]
        texto = leer_entrada({"archivo": f"datos/v2-revisor/codigo/{nombre}"})
        if demo_respuestas:
            respuestas = demo_respuestas(nombre, texto)

            def responder(prompt, sistema):
                for marca, respuesta in respuestas.items():
                    if marca in sistema:
                        return json.dumps(respuesta, ensure_ascii=False)
                raise ValueError("La demostración no reconoce el prompt")

            llm.fake.responder = responder
        trazas.registrar("caso_lab2", entrada=nombre, repeticion=repeticion, demo=args.demo)
        res = flujo.ejecutar({"entrada": texto, "contexto": "(sin contexto: Mini-RAG pendiente del Laboratorio 3)"})
        estado = "completo" if res.ok and len(res.etapas) == len(flujo.etapas) else "incompleto"
        for e in res.etapas:
            if not e.ok:
                artefacto = "Salida inválida: " + json.dumps(e.salida, ensure_ascii=False)[:100]
            elif e.nombre in ("detectar", "explicar") and isinstance(e.salida, dict):
                artefacto = f"{len(e.salida['hallazgos'])} hallazgos: " + ", ".join(
                    f"{h['id']} {h['regla']} L{h['linea']}" for h in e.salida["hallazgos"])
            elif e.nombre == "parche" and isinstance(e.salida, dict):
                artefacto = f"{len(e.salida['parches'])} parches; archivo de {len(e.salida['codigo_corregido'].splitlines())} líneas"
            elif e.nombre == "dictamen" and isinstance(e.salida, dict):
                artefacto = f"{e.salida['estado']}: {e.salida['total_hallazgos']} hallazgos"
            else:
                artefacto = json.dumps(e.salida, ensure_ascii=False)[:160]
            filas.append({"entrada": nombre, "repeticion": repeticion, "etapa": e.nombre,
                          "prompt": e.prompt, "artefacto": artefacto, "valida": e.ok,
                          "intentos": e.intentos, "errores": e.errores,
                          "latencia_ms": round(e.latencia_ms, 2), "costo_usd": e.costo_usd})
        resultado = {"ok": estado == "completo", "hallazgos": (res.salidas.get("detectar") or {}).get("hallazgos", []),
                     "parche": res.salidas.get("parche") if estado == "completo" else None}
        corridas.append({"entrada": nombre, "repeticion": repeticion, "estado": estado,
                         "etapas": res.bitacora(), "resultado": resultado})
        guardar_parcial()
        print(f"{nombre} / {repeticion}: {estado}; {len(res.etapas)}/{len(flujo.etapas)} etapas")
        return resultado

    for nombre in entradas:
        ejecutar(nombre, "inicial")
    consistencia = [ejecutar(entradas[0], n) for n in range(1, 4)]
    firmas = [sorted((h["regla"], h["linea"]) for h in r["hallazgos"]) for r in consistencia]
    coinciden = all(r["ok"] for r in consistencia) and firmas[0] == firmas[1] == firmas[2]
    sufijo = "_v1" if args.v1 else ""
    datos = {"fecha_utc": datetime.now(timezone.utc).isoformat(), "demo": args.demo,
             "proveedor": cfg.llm_proveedor, "modelo": cfg.llm_modelo,
             "sin_rag": True, "huella": huella, "filas": filas, "corridas": corridas,
             "consistencia": {"repeticiones": consistencia, "coinciden_reglas_y_lineas": coinciden}}
    (cfg.dir_trazas / f"a2_trazabilidad{sufijo}.json").write_text(
        json.dumps(datos, ensure_ascii=False, indent=2), encoding="utf-8")
    aviso = ("DEMOSTRACIÓN: respuestas preparadas. No mide calidad ni mejora de prompts."
             if args.demo else "Ejecución con proveedor real, sin Mini-RAG.")
    lineas = ["# Laboratorio 2: matriz del revisor", "", aviso,
              f"Proveedor: {cfg.llm_proveedor}. Modelo: {cfg.llm_modelo}.", "",
              "| Entrada | Repetición | Etapa | Prompt | Artefacto | Válida | Intentos | Errores |",
              "|---|---|---|---|---|---|---|---|"]
    for f in filas:
        valores = [f[k] for k in ("entrada", "repeticion", "etapa", "prompt", "artefacto", "valida", "intentos", "errores")]
        lineas.append("| " + " | ".join(str(v).replace("|", "/").replace("\n", " ") for v in valores) + " |")
    lineas += ["", f"Consistencia (transferencias.py x 3), reglas y líneas: {firmas}",
               f"Tres flujos completos y mismos hallazgos: {coinciden}.",
               "La coincidencia no demuestra exactitud; revisar el contenido y los errores en las trazas."]
    ruta = cfg.dir_trazas / f"a2_matriz{sufijo}.md"
    ruta.write_text("\n".join(lineas) + "\n", encoding="utf-8")
    print("Matriz:", ruta)
    return 0 if all(c["estado"] == "completo" for c in corridas) else 1


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as error:
        from finnorte.llm import LLMError
        if isinstance(error, LLMError):
            print(f"No se completó la ejecución: {error}", file=sys.stderr)
            raise SystemExit(1)
        raise
