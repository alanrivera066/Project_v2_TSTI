"""Guarda evidencia reproducible del laboratorio sin ejecutar código no confiable."""
from __future__ import annotations
import contextlib
import io
import json
import os
from pathlib import Path
import subprocess
import sys
import unittest

RAIZ=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(RAIZ/"src"))
os.chdir(RAIZ)
os.environ["LLM_PROVIDER"]="fake"
os.environ["EMB_PROVIDER"]="hash"
os.environ["PYTHONIOENCODING"]="utf-8"
from finnorte import evaluacion,revisor
from finnorte.config import config
from finnorte.asistente import Asistente

destino=RAIZ/"bitacora"/"laboratorio3"
destino.mkdir(parents=True,exist_ok=True)
# Pruebas de comportamiento; no se presentan como una ejecución de pytest.
stream=io.StringIO()
suite=unittest.defaultTestLoader.discover(str(RAIZ/"tests"),pattern="test_revisor_unittest.py")
resultado=unittest.TextTestRunner(stream=stream,verbosity=2).run(suite)
(destino/"pruebas_unittest.txt").write_text(stream.getvalue(),encoding="utf8")
resumen=dict(ejecutor="unittest",pruebas=resultado.testsRun,fallos=len(resultado.failures),
             errores=len(resultado.errors),omitidas=len(resultado.skipped),pytest="Ver bitacora/validacion_oficial/ultima_ejecucion.json")
# No contaminar las evidencias con la fixture de la última prueba.
from finnorte import llm
llm.fake.responder=None
pregunta="¿Puedo desplegar el 30?"
comparacion={}
for nombre,op in {"normal":{},"sin_rag":{"usar_rag":False},"sin_controles":{"controles":False}}.items():
    comparacion[nombre]=Asistente.crear(**op).responder(pregunta)
(destino/"comparacion_guia.json").write_text(json.dumps(dict(pregunta=pregunta,proveedor="fake",embeddings="hash",
    calidad_representativa=False,resultados=comparacion),ensure_ascii=False,indent=2),encoding="utf8")
# Las cuatro configuraciones de la guía común, dos repeticiones.
cmd=[sys.executable,"guia/av1_configuraciones.py","--guia","--casos","evals/comun.jsonl",
     "--rep","2","--contrato","contrato_guia.yaml","--salida-dir","bitacora/laboratorio3/guia_ABCD"]
r=subprocess.run(cmd,capture_output=True,text=True,encoding="utf8",env=os.environ.copy())
(destino/"guia_ABCD.txt").write_text(r.stdout+r.stderr,encoding="utf8")
resumen["guia_ABCD_exit_code"]=r.returncode
oficial=subprocess.run([sys.executable,"guia/s3_rag_eval.py","--rep","2"],capture_output=True,text=True,encoding="utf8",env=os.environ.copy())
(destino/"s3_rag_eval.txt").write_text(oficial.stdout+oficial.stderr,encoding="utf8")
resumen["s3_rag_eval_exit_code"]=oficial.returncode
# Evaluación final de desarrollo de la variante, separada de la guía común.
cmd=[sys.executable,"guia/av1_configuraciones.py","--casos","evals/v2-revisor.jsonl","--rep","3"]
r=subprocess.run(cmd,capture_output=True,text=True,encoding="utf8",env=os.environ.copy())
(RAIZ/"bitacora"/"simulacion"/"tabla_ABCD.txt").write_text(r.stdout+r.stderr,encoding="utf8")
resumen["variante_ABCD_exit_code"]=r.returncode
# Demostración de referencia.
from finnorte.variante import sistema
demo=sistema({"archivo":"datos/v2-revisor/codigo/transferencias.py"})
(destino/"ejemplo_revisor.json").write_text(json.dumps(demo,ensure_ascii=False,indent=2),encoding="utf8")
# Diagnóstico A1 puro sin atribuirle semántica a hash.
from finnorte.variante import indice
filas=[]
for regla,(consulta,_) in revisor.DETALLES.items():
    esperada=f"sec-{regla:02d}"
    rs=indice().buscar(consulta,k=3)
    filas.append(dict(regla=esperada,consulta=consulta,recuperados=[r.fragmento.doc_id for r in rs],
        acierto1=bool(rs) and rs[0].fragmento.doc_id==esperada,acierto3=any(r.fragmento.doc_id==esperada for r in rs)))
resumen["a1_hash"]={"acierto1":sum(f["acierto1"] for f in filas)/len(filas),
                    "acierto3":sum(f["acierto3"] for f in filas)/len(filas)}
(destino/"recuperacion_hash.json").write_text(json.dumps(dict(calidad_semantica_real=False,filas=filas,
    metricas=resumen["a1_hash"]),ensure_ascii=False,indent=2),encoding="utf8")
(destino/"resumen_validacion.json").write_text(json.dumps(resumen,ensure_ascii=False,indent=2),encoding="utf8")
print(json.dumps(resumen,ensure_ascii=True,indent=2))
raise SystemExit(0 if resultado.wasSuccessful() and r.returncode==0 else 1)
