"""Ejecuta pytest real y registra comandos, directorios, entorno y JUnit XML."""
from pathlib import Path
from datetime import datetime,timezone
import argparse,json,os,platform,subprocess,sys,hashlib
RAIZ=Path(__file__).resolve().parents[1]
ap=argparse.ArgumentParser()
ap.add_argument("--equipo-root",type=Path,help="Copia local del repositorio del equipo; no se modifica")
a=ap.parse_args()
marca=datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
salida=RAIZ/"bitacora"/"validacion_oficial"/marca
salida.mkdir(parents=True,exist_ok=False)
entorno=os.environ.copy()
entorno.update(PYTHONPATH=str(RAIZ/"herramientas_pruebas")+os.pathsep+"src",
    PYTEST_DISABLE_PLUGIN_AUTOLOAD="1",PYTHONIOENCODING="utf-8",LLM_PROVIDER="fake",EMB_PROVIDER="hash")
registros=[]
tareas=[("controles_lab3",RAIZ,["tests/test_av1_controles.py"]),
        ("suite_local",RAIZ,[])]
if a.equipo_root: tareas.append(("equipo_a1_a2_av1",a.equipo_root.resolve(),
    ["tests/test_a1_vectores.py","tests/test_a2_pipeline.py","tests/test_av1_controles.py"]))
for nombre,cwd,seleccion in tareas:
    cmd=[sys.executable,"-m","pytest",*seleccion,"-q","-rA","--junitxml",str(salida/(nombre+".xml"))]
    inicio=datetime.now(timezone.utc).isoformat()
    r=subprocess.run(cmd,cwd=cwd,env=entorno,capture_output=True,text=True,encoding="utf-8")
    (salida/(nombre+".txt")).write_text(r.stdout+r.stderr,encoding="utf8")
    archivos=list((cwd/"src"/"finnorte").glob("*.py"))+list((cwd/"tests").glob("*.py"))
    registros.append(dict(grupo=nombre,comando=cmd,cwd=str(cwd),inicio_utc=inicio,
        fin_utc=datetime.now(timezone.utc).isoformat(),exit_code=r.returncode,
        stdout=nombre+".txt",junit=nombre+".xml",
        sha256_archivos={str(p.relative_to(cwd)):hashlib.sha256(p.read_bytes()).hexdigest() for p in archivos}))
m=dict(python=sys.executable,version_python=sys.version,plataforma=platform.platform(),
       pytest="8.4.2 desde fuentes oficiales; ver herramientas_pruebas/procedencia.json",
       variables={k:entorno[k] for k in ("PYTHONPATH","PYTEST_DISABLE_PLUGIN_AUTOLOAD","LLM_PROVIDER","EMB_PROVIDER","PYTHONIOENCODING")},
       alcance="Copia de laboratorio y, si se indicó, subconjunto A1/A2/AV1 del equipo. No es CI de GitHub ni evaluación Gemini.",
       pruebas=registros)
(salida/"ejecucion.json").write_text(json.dumps(m,ensure_ascii=False,indent=2),encoding="utf8")
(RAIZ/"bitacora"/"validacion_oficial"/"ultima_ejecucion.json").write_text(json.dumps(
    {"directorio":str(salida),"manifest":str(salida/"ejecucion.json")},ensure_ascii=False,indent=2),encoding="utf8")
print(json.dumps({"evidencias":str(salida),"grupos":[{"grupo":r["grupo"],"exit_code":r["exit_code"]} for r in registros]},ensure_ascii=True))
raise SystemExit(0 if all(r["exit_code"]==0 for r in registros) else 1)
