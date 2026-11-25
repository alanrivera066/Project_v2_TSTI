"""Evaluación Gemini A-D, con checkpoint por respuesta y reanudación verificada."""
from pathlib import Path
from datetime import datetime,timezone
import argparse,json,os,sys,hashlib
from collections import defaultdict,deque
RAIZ=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(RAIZ/"src"))
def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--modelo",required=True)
    ap.add_argument("--calibracion",type=Path,required=True)
    ap.add_argument("--rep",type=int,choices=[1,2,3],default=1)
    ap.add_argument("--salida",type=Path)
    ap.add_argument("--continuar",action="store_true")
    ap.add_argument("--intervalo",type=float,default=6.0)
    a=ap.parse_args()
    os.environ.update(LLM_PROVIDER="gemini",LLM_MODEL=a.modelo,EMB_PROVIDER="gemini")
    from finnorte.config import config
    cfg=config()
    if not cfg.gemini_key: raise SystemExit("Falta GEMINI_API_KEY. No se hicieron llamadas.")
    cal=json.loads(a.calibracion.read_text(encoding="utf8"))
    if cal.get("estado")!="calibrado" or cal.get("proveedor")!="gemini":
        raise SystemExit("Se requiere calibración real Gemini; hash no se acepta.")
    if cal.get("modelo")!=cfg.emb_modelo:
        raise SystemExit("Cambió el modelo de embeddings. Vuelve a calibrar.")
    from finnorte.asistente import Asistente
    from finnorte import evaluacion
    salida=a.salida or RAIZ/"bitacora"/"gemini_nuevo"/datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    if salida.exists() and not a.continuar: raise SystemExit("El directorio existe; usa --continuar.")
    salida.mkdir(parents=True,exist_ok=True)
    entradas=list((RAIZ/"src/finnorte").glob("*.py"))+list((RAIZ/"prompts").rglob("*"))
    entradas += list((RAIZ/"corpus/comun").glob("*.md"))+[RAIZ/"evals/comun.jsonl",a.calibracion]
    firmas={str(p.resolve()):hashlib.sha256(p.read_bytes()).hexdigest() for p in entradas if p.is_file()}
    manifiesto=dict(modelo=cfg.llm_modelo,embeddings=cfg.emb_modelo,repeticiones=a.rep,umbral=cal["umbral_propuesto"],sha256=firmas)
    ruta=salida/"firma.json"
    if ruta.exists() and json.loads(ruta.read_text(encoding="utf8"))!=manifiesto:
        raise SystemExit("Cambió código, modelo o datos. No se mezclarán respuestas; usa otra carpeta.")
    ruta.write_text(json.dumps(manifiesto,ensure_ascii=False,indent=2),encoding="utf8")
    from control_cuota import instalar_control
    control=instalar_control(salida/"cuotas",cfg.gemini_key,max(0,a.intervalo))
    existentes={str(p.relative_to(salida)):hashlib.sha256(p.read_bytes()).hexdigest()
                for c in "ABCD" for p in (salida/c).glob("*.json")}
    evento=dict(fecha_utc=datetime.now(timezone.utc).isoformat(),intervalo_s=max(0,a.intervalo),
        respuestas_previas=existentes,esperas_fuera_de_latencia_respuesta=True,
        nota="Cambio de ritmo registrado; no se cambian modelo, prompts ni respuestas anteriores")
    (salida/("reanudacion_"+datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%S%fZ")+".json")).write_text(
        json.dumps(evento,ensure_ascii=False,indent=2),encoding="utf8")
    casos=evaluacion.cargar_casos(RAIZ/"evals/comun.jsonl")
    configs={"A":dict(version_prompt=1,usar_rag=False,controles=False),
             "B":dict(version_prompt=2,usar_rag=False,controles=False),
             "C":dict(version_prompt=2,usar_rag=True,controles=False),
             "D":dict(version_prompt=2,usar_rag=True,controles=True)}
    aciertos,tablas={},[]
    for nombre,op in configs.items():
        carpeta=salida/nombre
        carpeta.mkdir(exist_ok=True)
        asis=Asistente.crear(umbral=cal["umbral_propuesto"],**op)
        respuestas=defaultdict(deque)
        for caso in casos:
            for repeticion in range(a.rep):
                archivo=carpeta/(str(caso["id"])+"_"+str(repeticion+1)+".json")
                if archivo.exists():
                    dato=json.loads(archivo.read_text(encoding="utf8"))
                else:
                    for intento_externo in range(3):
                        control.ultimo_error=None
                        control.antes()  # Pausa fuera del tiempo medido de responder().
                        try:
                            respuesta=asis.responder(caso["entrada"])
                            break
                        except Exception as exc:
                            error=str(exc).replace(cfg.gemini_key,"<CREDENCIAL_OCULTA>")
                            registro=dict(fecha_utc=datetime.now(timezone.utc).isoformat(),config=nombre,caso=caso["id"],
                                repeticion=repeticion+1,tipo=type(exc).__name__,error=error)
                            (salida/"interrupcion.json").write_text(json.dumps(registro,ensure_ascii=False,indent=2),encoding="utf8")
                            if "429" in error and control.puede_reintentar() and intento_externo<2:
                                control.esperar()
                                continue
                            motivo="Cuota diaria agotada." if control.ultimo_error and control.ultimo_error["tipo_limite"]=="diario" else "Evaluación interrumpida."
                            raise SystemExit(motivo+" El avance está guardado; revisa el registro antes de reanudar.")
                    dato=dict(caso=caso["id"],repeticion=repeticion+1,config=nombre,
                        fecha_utc=datetime.now(timezone.utc).isoformat(),modelo=cfg.llm_modelo,salida=respuesta)
                    archivo.write_text(json.dumps(dato,ensure_ascii=False,indent=2),encoding="utf8")
                respuestas[json.dumps(caso["entrada"],sort_keys=True)].append(dato["salida"])
                print(f"{nombre} caso {caso['id']} repetición {repeticion+1}/{a.rep} guardada",flush=True)
        def reproducir(entrada):
            return respuestas[json.dumps(entrada,sort_keys=True)].popleft()
        r=evaluacion.evaluar(reproducir,casos,repeticiones=a.rep,etiqueta="guia-gemini-"+nombre)
        r["origen"]="Agregado de respuestas reales guardadas; sin llamadas nuevas para agregar métricas"
        r["umbral"]=cal["umbral_propuesto"]
        r["firma"]="firma.json"
        evaluacion.guardar_reporte(r,salida/("guia_"+nombre+".json"))
        aciertos[nombre]=[sum(d["acierto"] for d in r["detalle"] if d["id"]==c["id"])/a.rep for c in casos]
        tablas.append(dict(config=nombre,**r["metricas"],
            contrato=evaluacion.revisar_contrato(r["metricas"],evaluacion.cargar_contrato(RAIZ/"contrato_guia.yaml"))))
    resumen=dict(estado="completo",modelo=cfg.llm_modelo,embeddings=cfg.emb_modelo,
        repeticiones=a.rep,casos=len(casos),ejecuciones=len(casos)*a.rep*4,umbral=cal["umbral_propuesto"],
        tabla=tablas,intervalos={y+"-"+x:evaluacion.bootstrap_diferencia(aciertos[x],aciertos[y])
            for x,y in [("A","B"),("B","C"),("C","D"),("A","D")]})
    evaluacion.guardar_reporte(resumen,salida/"resumen.json")
    print("EVALUACION TERMINADA:",salida,flush=True)
if __name__=="__main__": main()
