"""Recalcula las 192 salidas con el evaluador docente original, sin llamar al modelo."""
from pathlib import Path
from zipfile import ZipFile
from collections import defaultdict,deque
from datetime import datetime,timezone
import importlib.util,json,sys,hashlib,os
from unittest.mock import patch
RAIZ=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(RAIZ/"src"))
def main():
    carpeta=RAIZ/"bitacora/proceso_gemini/20261125T002950Z/evaluacion"
    original=RAIZ/"referencias/evaluacion_docente_original.py"
    if not original.exists():
        original.parent.mkdir(exist_ok=True)
        with ZipFile(r"C:\Users\cesar\Downloads\finnorte-ia-alumno.zip") as z:
            original.write_bytes(z.read("finnorte-ia-alumno/src/finnorte/evaluacion.py"))
    base=json.loads((carpeta/"resumen.json").read_text(encoding="utf8"))
    os.environ.update(LLM_PROVIDER="gemini",LLM_MODEL=base["modelo"],EMB_PROVIDER="gemini",EMB_MODEL=base["embeddings"])
    spec=importlib.util.spec_from_file_location("finnorte.evaluacion_docente_original",original)
    docente=importlib.util.module_from_spec(spec)
    sys.modules[spec.name]=docente
    spec.loader.exec_module(docente)
    casos=docente.cargar_casos(RAIZ/"evals/comun.jsonl")
    contrato=docente.cargar_contrato(RAIZ/"contrato_guia.yaml")
    destino=carpeta/"analisis_docente"
    destino.mkdir(exist_ok=True)
    tabla=[]
    with patch("finnorte.llm.generar",side_effect=AssertionError("Este análisis no debe llamar al modelo")) as sin_llm:
        for config in "ABCD":
            cola=defaultdict(deque)
            antes={}
            for caso in casos:
                for n in range(1,base["repeticiones"]+1):
                    p=carpeta/config/(caso["id"]+"_"+str(n)+".json")
                    antes[p]=hashlib.sha256(p.read_bytes()).hexdigest()
                    dato=json.loads(p.read_text(encoding="utf8"))
                    assert dato["caso"]==caso["id"] and dato["repeticion"]==n and dato["config"]==config
                    cola[json.dumps(caso["entrada"],sort_keys=True)].append(dato["salida"])
            def reproducir(entrada):
                return cola[json.dumps(entrada,sort_keys=True)].popleft()
            r=docente.evaluar(reproducir,casos,repeticiones=base["repeticiones"],etiqueta="recalculo-docente-sin-llamadas-"+config)
            assert r["metricas"]["errores_sistema"]==0
            previo=next(x for x in base["tabla"] if x["config"]==config)
            for nombre,valor in r["metricas"].items():
                if nombre!="consistencia" and nombre in previo: assert valor==previo[nombre],(config,nombre)
            assert all(hashlib.sha256(p.read_bytes()).hexdigest()==h for p,h in antes.items())
            fila=dict(config=config,**r["metricas"],
                consistencia_literal_previa=previo["consistencia"],
                contrato=docente.revisar_contrato(r["metricas"],contrato))
            tabla.append(fila)
            docente.guardar_reporte(r,destino/("docente_"+config+".json"))
        assert sin_llm.call_count==0
    resultado=dict(fecha_utc=datetime.now(timezone.utc).isoformat(),
        metodo="Evaluador original del ZIP docente, cargado sin modificar; agregado offline de las mismas 192 salidas.",
        sha256_evaluador_original=hashlib.sha256(original.read_bytes()).hexdigest(),
        llamadas_nuevas_modelo=0,respuestas_modificadas=0,
        definicion_docente="Estabilidad del acierto booleano por caso entre repeticiones",
        definicion_literal_previa="Igualdad literal de respuesta, fuentes y abstención",
        tabla=tabla,intervalos=base["intervalos"],modelo=base["modelo"],embeddings=base["embeddings"],
        casos=base["casos"],repeticiones=base["repeticiones"],ejecuciones=base["ejecuciones"],umbral=base["umbral"])
    docente.guardar_reporte(resultado,destino/"resumen_docente.json")
    print(json.dumps(dict(evaluador_original_sha=resultado["sha256_evaluador_original"],
        nuevas_llamadas=0,tabla=[{k:x[k] for k in ("config","exactitud","consistencia","consistencia_literal_previa")}|
            {"metas_cumplidas":sum(r["cumple"] for r in x["contrato"])} for x in tabla]),ensure_ascii=True,indent=2))
if __name__=="__main__": main()
