"""Calibración de recuperación del caso guía con desarrollo y validación separados."""
from pathlib import Path
from datetime import datetime,timezone
import argparse,json,os,sys,hashlib
RAIZ=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(RAIZ/"src"))
ap=argparse.ArgumentParser()
ap.add_argument("--proveedor",choices=["gemini","hash"],default="gemini")
ap.add_argument("--salida",type=Path)
a=ap.parse_args()
os.environ["EMB_PROVIDER"]=a.proveedor
from finnorte.config import config
from finnorte.retrieval import Indice
from finnorte.controles import filtrar_clasificacion
cfg=config()
salida=a.salida or RAIZ/"bitacora"/("calibracion_"+a.proveedor+".json")
if salida.exists(): raise SystemExit("El archivo ya existe; usa otra ruta de salida.")
salida.parent.mkdir(parents=True,exist_ok=True)
if a.proveedor=="gemini" and not cfg.gemini_key:
    salida.write_text(json.dumps(dict(estado="pendiente",motivo="No hay GEMINI_API_KEY autorizada configurada",
        proveedor="gemini",llamadas_al_proveedor=0),ensure_ascii=False,indent=2),encoding="utf8")
    raise SystemExit("Gemini pendiente: falta una llave configurada. No se hicieron llamadas.")
pares=[
("desarrollo",True,"¿Qué revisiones y pruebas pide FinNorte antes de aprobar un pull request?"),
("desarrollo",True,"¿Dónde se guardan y cada cuánto se renuevan las credenciales de los servicios?"),
("desarrollo",True,"¿Qué restricciones de calendario aplican al despliegue productivo?"),
("desarrollo",True,"¿Cómo clasificamos y comunicamos un incidente técnico?"),
("desarrollo",False,"¿Cuánto cuesta el plan comercial para una tienda nueva?"),
("desarrollo",False,"¿Qué documentos debo presentar para un crédito hipotecario?"),
("desarrollo",False,"¿Cómo inscribo un empleado en nómina y calculo su salario neto?"),
("desarrollo",False,"¿Cuáles son las tasas de rendimiento de una cuenta de inversión?"),
("validacion",True,"¿Qué datos se deben eliminar de los registros de aplicación?"),
("validacion",True,"¿Qué controles exige FinNorte para dependencias de terceros?"),
("validacion",True,"¿Cómo se concede acceso a un repositorio y cómo se revoca al salir alguien?"),
("validacion",True,"¿Qué identificadores y campos incluye una respuesta de error de API?"),
("validacion",False,"¿Qué sucursales abren el domingo y en qué horario atienden?"),
("validacion",False,"¿Qué convenio de seguro médico tienen los familiares de empleados?"),
("validacion",False,"¿Cuál es el pronóstico de ventas de mi comercio el próximo mes?"),
("validacion",False,"¿Qué plazo de liquidación exige mi contrato particular con el banco?")
]
ind=Indice.desde_carpeta(RAIZ/"corpus"/"comun")
parcial=salida.with_suffix(".parcial.json")
firma={str(p.relative_to(RAIZ)):hashlib.sha256(p.read_bytes()).hexdigest()
       for p in (RAIZ/"corpus/comun").glob("*.md")}
metadata=dict(proveedor=a.proveedor,modelo=cfg.emb_modelo,corpus=firma)
guardado=json.loads(parcial.read_text(encoding="utf8")) if parcial.exists() else {}
if guardado and guardado.get("metadata")!=metadata:
    raise SystemExit("Cambió el corpus o el modelo; usa otra ruta de calibración.")
filas=guardado.get("filas",[])
for grupo,dentro,pregunta in pares:
    if any(f["grupo"]==grupo and f["pregunta"]==pregunta for f in filas):
        continue
    rs=filtrar_clasificacion(ind.buscar(pregunta,k=4))
    filas.append(dict(grupo=grupo,dentro=dentro,pregunta=pregunta,
        puntaje=rs[0].puntaje if rs else 0.0,fuentes=[r.fragmento.id for r in rs]))
    parcial.write_text(json.dumps(dict(metadata=metadata,filas=filas),ensure_ascii=False,indent=2),encoding="utf8")
def medir(filas,t):
    tp=sum(f["dentro"] and f["puntaje"]>=t for f in filas)
    tn=sum(not f["dentro"] and f["puntaje"]<t for f in filas)
    positivos=sum(f["dentro"] for f in filas)
    negativos=len(filas)-positivos
    return dict(verdaderos_positivos=tp,verdaderos_negativos=tn,
        falsos_negativos=positivos-tp,falsos_positivos=negativos-tn,
        sensibilidad=tp/positivos,especificidad=tn/negativos,
        exactitud_balanceada=(tp/positivos+tn/negativos)/2)
dev=[f for f in filas if f["grupo"]=="desarrollo"]
scores=sorted(set(f["puntaje"] for f in dev))
candidatos=[scores[0]-1e-9]+[(x+y)/2 for x,y in zip(scores,scores[1:])]+[scores[-1]+1e-9]
mejor=max(candidatos,key=lambda t:(medir(dev,t)["exactitud_balanceada"],medir(dev,t)["especificidad"],t))
r=dict(estado="calibrado" if a.proveedor=="gemini" else "demostracion_no_aplicar_a_gemini",
    fecha_utc=datetime.now(timezone.utc).isoformat(),proveedor=a.proveedor,modelo=cfg.emb_modelo,
    corpus="corpus/comun",k=4,umbral_propuesto=mejor,
    criterio="Mayor exactitud balanceada en desarrollo; empate prioriza abstención fuera de dominio.",
    alcance="Recuperación de la guía común; no calibra el clasificador AST ni certifica calidad generativa.",
    desarrollo=medir(dev,mejor),validacion=medir([f for f in filas if f["grupo"]=="validacion"],mejor),filas=filas)
salida.write_text(json.dumps(r,ensure_ascii=False,indent=2),encoding="utf8")
print(json.dumps({k:r[k] for k in ("estado","umbral_propuesto","desarrollo","validacion")},ensure_ascii=True,indent=2))
