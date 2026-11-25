"""Proceso de usuario: acceso, calibración y evaluación; solo requiere la llave local."""
from pathlib import Path
from datetime import datetime,timezone
import argparse,json,os,subprocess,sys
RAIZ=Path(__file__).resolve().parents[1]
def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--rep",type=int,choices=[1,2,3],default=3)
    ap.add_argument("--prueba-local",action="store_true",help="Solo verifica la preparación, sin red")
    a=ap.parse_args()
    os.chdir(RAIZ)
    sys.path.insert(0,str(RAIZ/"src"))
    from finnorte.config import config
    cfg=config()
    if a.prueba_local:
        print(json.dumps(dict(preparado=bool(cfg.gemini_key),llave_mostrada=False,red_utilizada=False,
            directorio=str(RAIZ)),ensure_ascii=True)); return
    if not cfg.gemini_key: raise SystemExit("Falta configurar la llave local.")
    entorno=os.environ.copy()
    entorno.update(PYTHONPATH="src",PYTHONIOENCODING="utf-8",LLM_PROVIDER="gemini",EMB_PROVIDER="gemini",LLM_RETRIES="1")
    base=RAIZ/"bitacora"/"proceso_gemini"
    base.mkdir(parents=True,exist_ok=True)
    puntero=base/"ultimo_proceso.json"
    if puntero.exists():
        carpeta=Path(json.loads(puntero.read_text(encoding="utf8"))["directorio"])
    else:
        carpeta=base/datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
        carpeta.mkdir()
        puntero.write_text(json.dumps(dict(directorio=str(carpeta))),encoding="utf8")
    def guardar(estado,**datos):
        (carpeta/"estado.json").write_text(json.dumps(dict(estado=estado,
            fecha_utc=datetime.now(timezone.utc).isoformat(),**datos),ensure_ascii=False,indent=2),encoding="utf8")
    def correr(nombre,args):
        print("\n"+nombre,flush=True)
        with (carpeta/(nombre+".txt")).open("a",encoding="utf8") as log:
            p=subprocess.Popen([sys.executable,*args],cwd=RAIZ,env=entorno,
                stdout=subprocess.PIPE,stderr=subprocess.STDOUT,text=True,encoding="utf8",errors="replace")
            for linea in p.stdout:
                limpia=linea.replace(cfg.gemini_key,"<CREDENCIAL_OCULTA>")
                print(limpia,end="",flush=True);log.write(limpia);log.flush()
            codigo=p.wait()
        if codigo:
            guardar("interrumpido",etapa=nombre,codigo=codigo)
            raise SystemExit("Se guardó el registro en "+str(carpeta)+". No cambies archivos al reanudar.")
    guardar("verificando_acceso")
    correr("01_acceso",["guia/configurar_y_probar_gemini.py"])
    ultimo=json.loads((RAIZ/"bitacora/gemini_acceso/ultimo_acceso.json").read_text(encoding="utf8"))
    acceso=json.loads(Path(ultimo["registro"]).read_text(encoding="utf8"))
    permitidos=acceso.get("modelos_generacion",[])
    preferencias=["gemini-3.1-flash-lite","gemini-2.5-flash-lite","gemini-2.5-flash","gemini-3.5-flash-lite"]
    modelo=next((x for x in preferencias if x in permitidos),None)
    emb=acceso.get("modelos_embeddings",[])
    embedding="gemini-embedding-001" if "gemini-embedding-001" in emb else next(iter(emb),None)
    if not modelo or not embedding:
        guardar("seleccion_modelo_pendiente",modelos=permitidos,embeddings=emb)
        raise SystemExit("Se guardó la lista de modelos disponibles para revisar antes de seguir.")
    entorno.update(LLM_MODEL=modelo,EMB_MODEL=embedding)
    print("Modelo:",modelo,"Embeddings:",embedding,flush=True)
    seleccion=carpeta/"modelos.json"
    actual=dict(modelo=modelo,embeddings=embedding,repeticiones=a.rep)
    if seleccion.exists() and json.loads(seleccion.read_text(encoding="utf8"))!=actual:
        raise SystemExit("La selección cambió; no se mezclarán ejecuciones.")
    seleccion.write_text(json.dumps(actual),encoding="utf8")
    cal=carpeta/"calibracion.json"
    if not cal.exists():
        correr("02_calibracion",["guia/calibrar_umbral.py","--salida",str(cal)])
    datos=json.loads(cal.read_text(encoding="utf8"))
    if datos.get("validacion",{}).get("exactitud_balanceada",0)<.75:
        guardar("calibracion_requiere_revision",resultado=str(cal))
        raise SystemExit("La calibración no generalizó suficientemente. Se conservó el resultado sin aplicarlo.")
    destino=carpeta/"evaluacion"
    args=["guia/evaluar_guia_gemini.py","--modelo",modelo,"--calibracion",str(cal),"--rep",str(a.rep),
          "--salida",str(destino)]
    if destino.exists(): args.append("--continuar")
    correr("03_evaluacion",args)
    guardar("completo",evaluacion=str(destino/"resumen.json"),calibracion=str(cal))
    print("\nPROCESO TERMINADO. Evidencias:",carpeta,flush=True)
if __name__=="__main__": main()
