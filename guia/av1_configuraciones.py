"""Comparación reproducible A/B/C/D con respuestas guardadas y reanudación."""
import argparse, hashlib, json, os, sys, shutil
from pathlib import Path
from datetime import datetime, timezone
from concurrent.futures import ThreadPoolExecutor, as_completed
RAIZ=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(RAIZ/'src'))
from finnorte import evaluacion, trazas
from finnorte.config import config, _cargar_env, precios_llm
from finnorte.variante import sistema, indice
CONFIGS={
 'A':dict(version_prompt=1,usar_rag=False,controles=False),
 'B':dict(version_prompt=2,usar_rag=False,controles=False),
 'C':dict(version_prompt=2,usar_rag=True,controles=False),
 'D':dict(version_prompt=2,usar_rag=True,controles=True)}

def huella_medicion(casos='evals/v2-revisor.jsonl', contrato='contrato_calidad.yaml'):
 """Incluye código, prompts, corpus, entradas, evaluaciones y contrato; nunca .env."""
 paths={p for carpeta,patron in [('src/finnorte','*.py'),('prompts','*.md'),
  ('prompts/esquemas','*.json'),('corpus/v2-revisor','*.md'),
  ('datos/v2-revisor/codigo','*.py')] for p in (RAIZ/carpeta).glob(patron)}
 paths.update([RAIZ/casos,RAIZ/contrato,Path(__file__)])
 archivos={p.relative_to(RAIZ).as_posix():hashlib.sha256(p.read_bytes()).hexdigest()
           for p in sorted(paths)}
 firma=hashlib.sha256(json.dumps(archivos,sort_keys=True).encode('utf-8')).hexdigest()
 return firma,archivos

def recuperar_respuestas(origen, destino, metadata):
 """Copia evidencia a una carpeta nueva; solo repite fallos del proveedor."""
 origen, destino = Path(origen), Path(destino)
 if origen.resolve()==destino.resolve() or any(destino.iterdir()):
  raise ValueError('La recuperación necesita una carpeta de salida nueva y vacía')
 preparados={}; conservar=set()
 for letra in CONFIGS:
  ruta=origen/f'av1_{letra}.json'
  if not ruta.exists(): continue
  anterior=json.loads(ruta.read_text(encoding='utf-8'))
  for campo in ['firma','modelo','embeddings','repeticiones','demo']:
   if anterior['metadata'][campo]!=metadata[campo]:
    raise ValueError(f'Cambió {campo}; no se pueden reutilizar estas respuestas')
  filas=[]
  for r in anterior['ejecuciones_guardadas']:
   if str(r['salida'].get('error','')).startswith('LLMError:'): continue
   filas.append({**r,'origen':r.get('origen',str(origen))})
   conservar.add((letra,r['id'],r['repeticion']))
  preparados[letra]={'metadata':anterior['metadata'],'config':anterior['config'],'ejecuciones_guardadas':filas}
 if not preparados: raise ValueError('No se encontraron respuestas para recuperar')
 # Validar todo antes de escribir; el intento anterior nunca se modifica.
 for letra,datos in preparados.items():
  (destino/f'av1_{letra}.json').write_text(json.dumps(datos,ensure_ascii=False,indent=2),encoding='utf-8')
 traza=origen/'trazas.jsonl'
 if traza.exists():
  eventos=[json.loads(l) for l in traza.read_text(encoding='utf-8').splitlines() if l.strip()]
  eventos=[{**e,'origen':e.get('origen',str(origen))} for e in eventos
           if (e.get('configuracion'),e.get('caso'),e.get('repeticion')) in conservar]
  (destino/'trazas.jsonl').write_text(''.join(json.dumps(e,ensure_ascii=False)+'\n' for e in eventos),encoding='utf-8')
 for cache in origen.glob('emb_*'):
  if cache.is_file(): shutil.copy2(cache,destino/cache.name)
 return len(conservar)

def firma_salida(out):
 a=out.get('artefacto',{})
 return json.dumps({'abstuvo':out.get('abstuvo'),'error':out.get('error'),
  'hallazgos':sorted((h['regla'],h['linea']) for h in a.get('hallazgos',[])),
  'parches':sorted((h['regla'],h['linea']) for h in a.get('parches',[]))},sort_keys=True)

def main():
 ap=argparse.ArgumentParser(description=__doc__)
 ap.add_argument('--casos',required=True); ap.add_argument('--rep',type=int,default=3)
 ap.add_argument('--env',help='Lee una configuración .env existente en memoria, sin copiar la llave')
 ap.add_argument('--continuar',action='store_true'); ap.add_argument('--trabajadores',type=int,default=1)
 ap.add_argument('--recuperar-de',help='Reutiliza respuestas previas en una carpeta nueva y repite solo fallos del proveedor')
 ap.add_argument('--salida',default='bitacora/av1_medicion'); ap.add_argument('--contrato',default='contrato_calidad.yaml')
 ap.add_argument('--intervalo',type=float,default=4.2,help='Separación mínima entre llamadas al modelo; cuota gratuita 15/min')
 a=ap.parse_args()
 if a.env: _cargar_env(Path(a.env))
 if a.rep<3: ap.error('Avance 1 requiere --rep >= 3')
 if a.trabajadores<1: ap.error('trabajadores debe ser positivo')
 destino=RAIZ/a.salida; destino.mkdir(parents=True,exist_ok=True)
 os.environ['FINNORTE_DIR_TRAZAS']=str(destino)
 os.environ['LLM_INTERVALO_SEG']=str(a.intervalo)
 cfg=config(); demo=cfg.llm_proveedor=='fake' or cfg.emb_proveedor=='hash'
 pin,pout=precios_llm(cfg.llm_proveedor,cfg.llm_modelo)
 casos=evaluacion.cargar_casos(RAIZ/a.casos); contrato=evaluacion.cargar_contrato(RAIZ/a.contrato)
 firma,archivos=huella_medicion(a.casos,a.contrato)
 meta={'fecha_utc':datetime.now(timezone.utc).isoformat(),'proveedor':cfg.llm_proveedor,'modelo':cfg.llm_modelo,
  'embeddings':cfg.emb_modelo,'demo':demo,'etiqueta':'demostración sin modelo real, NO es medición' if demo else 'medición con API real',
  'firma':firma,'metodo_firma':'sha256_manifest_v1','archivos':archivos,
  'repeticiones':a.rep,'trabajadores':a.trabajadores,'intervalo_seg':a.intervalo,'versiones':{'A':[1,1,1],'BCD':[4,5,5]},
  'dictamen':'PENDIENTE · Kevin',
  'costo':f'Estimación LLM a tarifa de pago Standard; tokens reales, tarifa {pin:.2f}/{pout:.2f} USD por millón; excluye embeddings; no es factura',
  'tarifa_usd_millon':{'entrada':pin,'salida':pout},
  'precios_fuente':'https://aistudio.google.com/docs/pricing#'+cfg.llm_modelo}
 if a.recuperar_de:
  try: reutilizadas=recuperar_respuestas(RAIZ/a.recuperar_de,destino,meta)
  except ValueError as e: ap.error(str(e))
  a.continuar=True
  print(f'Respuestas reutilizadas: {reutilizadas}; originales conservados',flush=True)
 promedios={}; tablas=[]
 for letra,op in CONFIGS.items():
  ruta=destino/f'av1_{letra}.json'; registros=[]
  if ruta.exists():
   anterior=json.loads(ruta.read_text(encoding='utf-8'))
   if not a.continuar: ap.error(f'{ruta} existe; usa --continuar o una carpeta nueva')
   for k in ['firma','modelo','embeddings','repeticiones','demo']:
    if anterior['metadata'][k]!=meta[k]: ap.error(f'Cambió {k}; usa otra carpeta de salida')
   registros=anterior['ejecuciones_guardadas']
  hechos={(r['id'],r['repeticion']) for r in registros}
  if op['usar_rag']: indice()  # Evita construcción simultánea de la caché.
  def ejecutar(caso,rep):
   token=trazas.EJECUCION.set({'caso':caso['id'],'repeticion':rep,'configuracion':letra})
   try:
    try: out=sistema(caso['entrada'],op)
    except Exception as e: out={'respuesta':'','fuentes':[],'abstuvo':False,'error':f'{type(e).__name__}: {e}'}
   finally: trazas.EJECUCION.reset(token)
   return {'id':caso['id'],'repeticion':rep,'salida':out}
  with ThreadPoolExecutor(max_workers=a.trabajadores) as pool:
   pendientes=[pool.submit(ejecutar,c,rep) for c in casos for rep in range(1,a.rep+1) if (c['id'],rep) not in hechos]
   for fut in as_completed(pendientes):
    registro=fut.result()
    if str(registro['salida'].get('error','')).startswith('LLMError:'):
     for pendiente in pendientes: pendiente.cancel()
     interrupcion={'metadata':meta,'configuracion':letra,'caso':registro['id'],
      'repeticion':registro['repeticion'],'error':registro['salida']['error'],
      'estado':'PENDIENTE DE MEDIR: interrupción del proveedor; conservar respuestas válidas y reanudar con --continuar'}
     (destino/'av1_interrupcion.json').write_text(json.dumps(interrupcion,ensure_ascii=False,indent=2),encoding='utf-8')
     print(interrupcion['estado'],flush=True)
     raise SystemExit(2)
    registros.append(registro)
    ruta.write_text(json.dumps({'metadata':meta,'config':op,'ejecuciones_guardadas':registros},ensure_ascii=False,indent=2),encoding='utf-8')
    print(f'{letra}: {len(registros)}/{len(casos)*a.rep}',flush=True)
  mapa={(r['id'],r['repeticion']):r['salida'] for r in registros}
  salidas=iter(mapa[c['id'],rep] for c in casos for rep in range(1,a.rep+1))
  res=evaluacion.evaluar(lambda _:next(salidas),casos,repeticiones=a.rep,etiqueta='av1-'+letra)
  fallos=[r for r in registros if 'error' in r['salida']]
  res['metricas']['errores_sistema']=len(fallos); res['errores_sistema']=[r['salida']['error'] for r in fallos]
  estables={c['id']:len({firma_salida(mapa[c['id'],rep]) for rep in range(1,a.rep+1)})==1 for c in casos}
  res['metricas']['consistencia_acierto_legacy']=res['metricas']['consistencia']
  res['metricas']['consistencia']=sum(estables.values())/len(casos)
  res['consistencia_por_tipo']={t:sum(estables[c['id']] for c in casos if c['tipo']==t)/sum(c['tipo']==t for c in casos) for t in {c['tipo'] for c in casos}}
  res.update(metadata=meta,config=op,ejecuciones_guardadas=registros,contrato=evaluacion.revisar_contrato(res['metricas'],contrato))
  ruta.write_text(json.dumps(res,ensure_ascii=False,indent=2),encoding='utf-8')
  promedios[letra]=[sum(d['acierto'] for d in res['detalle'] if d['id']==c['id'])/a.rep for c in casos]
  tablas.append({'config':letra,**res['metricas'],'cumple':all(f['cumple'] for f in res['contrato'])})
 intervalos={y+'-'+x:evaluacion.bootstrap_diferencia(promedios[x],promedios[y]) for x,y in [('A','B'),('B','C'),('C','D'),('A','D')]}
 resumen={'metadata':meta,'tabla':tablas,'intervalos_pareados_por_caso':intervalos}
 (destino/'av1_resumen.json').write_text(json.dumps(resumen,ensure_ascii=False,indent=2),encoding='utf-8')
 print(json.dumps(resumen,ensure_ascii=False,indent=2))
if __name__=='__main__': main()
