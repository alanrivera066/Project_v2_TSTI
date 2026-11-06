"""Etapa dictamen: seis casos y comparación de versiones del prompt, con matriz generada por código.

    python guia/a2_dictamen.py casos --version 1
    python guia/a2_dictamen.py comparar --version 1

casos: dos limpios, tres con un problema y uno con dos.
comparar: tres entradas distintas y una de ellas repetida tres veces.
Solo cambia rev_dictamen; detectar, explicar y parche conservan las versiones del Lab 2.
--demo usa respuestas preparadas: comprueba el mecanismo, no mide calidad.
"""
import argparse
import json
import os
import sys
from dataclasses import replace
from datetime import datetime, timezone
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(RAIZ / "src"))
sys.path.insert(0, str(RAIZ / "guia"))
CASOS = "evals/v2-revisor-dictamen.jsonl"
COMPARACION = ["d6", "d3", "d1"]  # Dos problemas, uno y limpio: los tres reportes posibles sin fallo.


def preparar_demo(llm, respuestas_para, ruta, codigo):
    reglas = {"limites.py": [], "limpio_enmascarado.py": [], "credencial.py": [("SEC-01", 1)],
              "consulta_sql.py": [("SEC-02", 2)], "deserializar.py": [("SEC-09", 5)],
              "dos_problemas.py": [("SEC-01", 1), ("SEC-02", 5)]}[Path(ruta).name]
    respuestas = respuestas_para("limites.py", codigo)
    hallazgos = [dict(id=f"H{i}", regla=r, linea=l, descripcion=f"Ejemplo preparado {r}")
                 for i, (r, l) in enumerate(reglas, 1)]
    explicados = [dict(h, explicacion=f"{h['regla']}, línea {h['linea']}: ejemplo preparado.") for h in hallazgos]
    parches = [dict(id=h["id"], regla=h["regla"], linea=h["linea"], cambio="Corrección preparada") for h in hallazgos]
    respuestas["Eres revisor de seguridad"] = {"hallazgos": hallazgos}
    respuestas["Eres revisor técnico"] = {"hallazgos": explicados}
    respuestas["Eres desarrollador Python"] = {"parches": parches, "codigo_corregido": codigo}
    respuestas["Eres redactor técnico"] = {
        "estado": "con_hallazgos" if reglas else "sin_hallazgos", "total_hallazgos": len(reglas),
        "hallazgos": [dict(h, cambio="Corrección preparada") for h in explicados],
        "resumen": f"Se encontraron {len(reglas)} hallazgos." if reglas else "sin hallazgos"}
    llm.fake.responder = lambda prompt, sistema: next(
        json.dumps(v, ensure_ascii=False) for marca, v in respuestas.items() if marca in sistema)


def tipo_reporte(texto):
    if texto.startswith("REVISIÓN FALLIDA"):
        return "fallida"
    return "sin hallazgos" if texto == "sin hallazgos" else "hallazgos"


def escribir_matriz(ruta, datos):
    filas = datos["filas"]
    lineas = [f"# Dictamen: {datos['modo']} con rev_dictamen.v{datos['version']}", "",
              "DEMOSTRACIÓN: respuestas preparadas. No mide calidad." if datos["demo"] else "Ejecución con proveedor real.",
              f"Proveedor: {datos['proveedor']}. Modelo: {datos['modelo']}. Fecha UTC: {datos['fecha_utc']}.",
              f"Estado: {datos['estado']}.", "",
              "| Caso | Rep. | Archivo | Esperado | Detectado | Reporte | Coincide | Intentos dictamen | Primer intento válido | Errores del validador |",
              "|---|---|---|---|---|---|---|---|---|---|"]
    for f in filas:
        errores = "; ".join(f["errores_dictamen"]).replace("|", "/").replace("\n", " ") or "ninguno"
        lineas.append(f"| {f['caso']} | {f['repeticion']} | {f['archivo']} | {', '.join(f['esperado']) or '-'} | "
                      f"{', '.join(f['detectado']) or '-'} | {f['reporte']} | {f['coincide']} | "
                      f"{f['intentos_dictamen']} | {f['primer_intento']} | {errores} |")
    r = datos["resumen"]
    lineas += ["", f"Flujos: {r['flujos']}. Reporte correcto para lo esperado: {r['coinciden']}/{r['flujos']}. "
               f"Dictamen válido al primer intento: {r['primer_intento']}/{r['con_dictamen']}. "
               f"Revisiones fallidas: {r['fallidas']}."]
    if r["repetidas"]:
        lineas.append(f"Repetición de {r['repetidas']['caso']}: {r['repetidas']['firmas']}; iguales: {r['repetidas']['iguales']}.")
    ruta.write_text("\n".join(lineas) + "\n", encoding="utf-8")


def resumir(filas):
    dictamenes = [f for f in filas if f["intentos_dictamen"]]
    repetidas = [f for f in filas if isinstance(f["repeticion"], int)]
    firmas = [[f["reporte"], f["detectado_lineas"]] for f in repetidas]
    return {"flujos": len(filas), "coinciden": sum(f["coincide"] for f in filas),
            "con_dictamen": len(dictamenes), "primer_intento": sum(f["primer_intento"] for f in dictamenes),
            "fallidas": sum(f["reporte"] == "fallida" for f in filas),
            "repetidas": {"caso": repetidas[0]["caso"], "firmas": firmas,
                          "iguales": all(x == firmas[0] for x in firmas)} if repetidas else None}


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("modo", choices=["casos", "comparar"])
    ap.add_argument("--version", type=int, required=True, help="Versión de rev_dictamen")
    ap.add_argument("--demo", action="store_true")
    ap.add_argument("--continuar", action="store_true", help="Recupera lo guardado tras un fallo del proveedor")
    ap.add_argument("--intervalo", type=float, default=4.2, help="Segundos entre llamadas; cuota gratuita 15/min")
    a = ap.parse_args()
    carpeta = RAIZ / "bitacora" / ("demo_dictamen" if a.demo else "dictamen") / f"{a.modo}_v{a.version}"
    if a.demo:
        os.environ.update(LLM_PROVIDER="fake", LLM_MODEL="fake-1")
    os.environ["FINNORTE_DIR_TRAZAS"] = str(carpeta)
    os.environ["LLM_INTERVALO_SEG"] = str(a.intervalo)

    from finnorte import llm, prompts, trazas
    from finnorte.config import config
    from finnorte.dictamen import reporte_final
    from finnorte.evaluacion import cargar_casos
    from finnorte.reglas import FlujoRevisor
    from finnorte.variante import FLUJO, VARIANTE, leer_entrada
    from demo_revisor import respuestas_para

    cfg = config()
    if cfg.llm_proveedor == "fake" and not a.demo:
        ap.error("Configura Gemini en .env o usa --demo para probar sin conexión.")
    if cfg.llm_proveedor == "gemini" and not cfg.gemini_key:
        ap.error("Falta GEMINI_API_KEY en .env. No pegues la llave en el chat ni en GitHub.")
    prompts.cargar("rev_dictamen", a.version)
    archivo = carpeta / "resultados.json"
    filas = []
    if archivo.exists():
        if not a.continuar:
            ap.error(f"{archivo} ya existe; usa --continuar. Las evidencias no se sobrescriben.")
        anterior = json.loads(archivo.read_text(encoding="utf-8"))
        if (anterior["modelo"], anterior["demo"]) != (cfg.llm_modelo, a.demo):
            ap.error("La evidencia guardada usa otro modelo o modo; no se pueden mezclar.")
        filas = anterior["filas"]
    carpeta.mkdir(parents=True, exist_ok=True)

    flujo = FlujoRevisor([replace(e, version=a.version) if e.nombre == "dictamen" else e for e in FLUJO.etapas],
                         nombre=VARIANTE)
    casos = {c["id"]: c for c in cargar_casos(RAIZ / CASOS)}
    if a.modo == "casos":
        plan = [(i, "unica") for i in casos]
    else:
        plan = [(i, "inicial") for i in COMPARACION] + [(COMPARACION[0], n) for n in (1, 2, 3)]

    def guardar(estado):
        datos = {"modo": a.modo, "version": a.version, "demo": a.demo, "proveedor": cfg.llm_proveedor,
                 "modelo": cfg.llm_modelo, "prompt": f"rev_dictamen.v{a.version}", "estado": estado,
                 "fecha_utc": datetime.now(timezone.utc).isoformat(), "filas": filas, "resumen": resumir(filas)}
        archivo.write_text(json.dumps(datos, ensure_ascii=False, indent=2), encoding="utf-8")
        escribir_matriz(carpeta / "matriz.md", datos)
        return datos

    hechos = {(f["caso"], f["repeticion"]) for f in filas}
    for caso_id, repeticion in plan:
        if (caso_id, repeticion) in hechos:
            continue
        caso = casos[caso_id]
        codigo = leer_entrada(caso["entrada"])
        if a.demo:
            preparar_demo(llm, respuestas_para, caso["entrada"]["archivo"], codigo)
        token = trazas.EJECUCION.set({"caso": caso_id, "repeticion": repeticion})
        try:
            res = flujo.ejecutar({"entrada": codigo, "contexto": "(sin contexto: flujo del Laboratorio 2)"})
        finally:
            trazas.EJECUCION.reset(token)
        intentos = [t for t in trazas.leer("intento_etapa")
                    if t["etapa"] == "dictamen" and t.get("caso") == caso_id and t.get("repeticion") == repeticion]
        reporte = reporte_final(res)
        hallazgos = (res.salidas.get("explicar") or {}).get("hallazgos", [])
        detectado = sorted(h["regla"] for h in hallazgos)
        esperado = caso["esperado"]["reglas"]
        tipo = tipo_reporte(reporte)
        filas.append({"caso": caso_id, "repeticion": repeticion, "archivo": Path(caso["entrada"]["archivo"]).name,
                      "tipo": caso["tipo"], "esperado": esperado, "detectado": detectado,
                      "detectado_lineas": sorted([h["regla"], h["linea"]] for h in hallazgos),
                      "reporte": tipo, "coincide": tipo != "fallida" and detectado == sorted(esperado),
                      "intentos_dictamen": len(intentos), "primer_intento": bool(intentos and intentos[0]["ok"]),
                      "errores_dictamen": [e for t in intentos for e in t["errores"]],
                      "etapas": [{"nombre": e.nombre, "prompt": e.prompt, "ok": e.ok, "intentos": e.intentos,
                                  "errores": e.errores} for e in res.etapas],
                      "reporte_texto": reporte})
        guardar("parcial")
        print(f"{caso_id} / {repeticion}: {tipo}; detectado {detectado}; dictamen {len(intentos)} intento(s)", flush=True)
    guardar("completo")
    print("Matriz:", carpeta / "matriz.md")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as error:
        from finnorte.llm import LLMError
        if isinstance(error, LLMError):
            print(f"No se completó: {error}. Repite con --continuar.", file=sys.stderr)
            raise SystemExit(1)
        raise
