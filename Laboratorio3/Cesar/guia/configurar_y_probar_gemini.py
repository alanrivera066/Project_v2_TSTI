"""Carga una llave local autorizada y verifica acceso sin imprimir credenciales."""
from pathlib import Path
from datetime import datetime,timezone
import json,re,os,sys
import requests
RAIZ=Path(__file__).resolve().parents[1]
ruta=Path(sys.argv[1]) if len(sys.argv)>1 else Path.home()/"Downloads"/"API_GEMINI.txt"
clave=ruta.read_text(encoding="utf-8-sig").strip()
if clave.startswith("GEMINI_API_KEY="): clave=clave.split("=",1)[1].strip()
clave=clave.strip('"').strip("'")
if not clave or any(c.isspace() for c in clave): raise SystemExit("El archivo no contiene una única llave válida; no se mostró su contenido.")
env=RAIZ/".env"
lineas=env.read_text(encoding="utf8").splitlines() if env.exists() else []
valores={"GEMINI_API_KEY":clave,"LLM_PROVIDER":"gemini","EMB_PROVIDER":"gemini"}
nuevas=[]
usadas=set()
for linea in lineas:
    campo=linea.split("=",1)[0].strip()
    if campo in valores:
        nuevas.append(campo+"="+valores[campo]); usadas.add(campo)
    else: nuevas.append(linea)
nuevas += [k+"="+v for k,v in valores.items() if k not in usadas]
env.write_text("\n".join(nuevas)+"\n",encoding="utf8")
out=RAIZ/"bitacora"/"gemini_acceso"
out.mkdir(exist_ok=True,parents=True)
registro={"fecha_utc":datetime.now(timezone.utc).isoformat(),"configuracion_guardada":True,
          "credencial_en_informe":False,"api":"GET /v1beta/models","estado":"pendiente"}
try:
    r=requests.get("https://generativelanguage.googleapis.com/v1beta/models",
        headers={"x-goog-api-key":clave},timeout=20)
    registro["http_status"]=r.status_code
    if r.status_code==200:
        models=r.json().get("models",[])
        registro["estado"]="acceso_confirmado"
        registro["modelos_generacion"]=[m["name"].removeprefix("models/") for m in models if "generateContent" in m.get("supportedGenerationMethods",[])]
        registro["modelos_embeddings"]=[m["name"].removeprefix("models/") for m in models if "embedContent" in m.get("supportedGenerationMethods",[])]
    else:
        d=r.json().get("error",{})
        registro["estado"]="error_http"
        registro["codigo_proveedor"]=d.get("status","desconocido")
except requests.RequestException as e:
    registro["estado"]="error_conexion"
    registro["tipo_error"]=type(e).__name__
    registro["dns"]=bool(re.search(r"(getaddrinfo|NameResolution|resolve)",str(e),re.I))
archivo=out/("acceso_"+datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")+".json")
archivo.write_text(json.dumps(registro,ensure_ascii=False,indent=2),encoding="utf8")
(out/"ultimo_acceso.json").write_text(json.dumps({"registro":str(archivo),"estado":registro["estado"]}),encoding="utf8")
print(json.dumps(registro,ensure_ascii=True,indent=2))
raise SystemExit(0 if registro["estado"]=="acceso_confirmado" else 2)
