import json
from collections import Counter
from pathlib import Path
import pytest
from finnorte import llm, variante, controles
from finnorte.config import RAIZ
from finnorte.reglas import validar_parche
from finnorte.retrieval import Fragmento, Resultado


def limpio(p, s):
    if 'redactor técnico' in s:
        return json.dumps({'estado': 'sin_hallazgos', 'total_hallazgos': 0, 'hallazgos': [], 'resumen': 'sin hallazgos'})
    if 'codigo_corregido' in p:
        return json.dumps({'parches': [], 'codigo_corregido': 'x = 1\n'})
    return json.dumps({'hallazgos': []})


def test_limpio_no_abstiene_por_baja_similitud(monkeypatch):
    class Indice:
        def buscar(self,*a,**k): return []
    monkeypatch.setattr(variante, 'indice', lambda: Indice())
    llm.fake.responder = limpio
    r=variante.sistema({'codigo':'x = 1\n'}, {'umbral': 1})
    assert r['respuesta']=='sin hallazgos' and not r['abstuvo']
    assert r['artefacto']['codigo_corregido']=='x = 1\n'
    assert set(r['artefacto'])=={'hallazgos','parches','codigo_corregido','dictamen'}


def test_fuera_de_dominio_no_llama_modelo(monkeypatch):
    def prohibido(*a,**k): raise AssertionError('No debe llamar al modelo')
    monkeypatch.setattr(llm,'generar',prohibido)
    assert variante.sistema({'pregunta':'¿Qué opinas del bitcoin?'},{'usar_rag':False})['abstuvo']


def test_confidencial_no_se_indexa(monkeypatch):
    monkeypatch.setattr(variante,'_INDICE',None)
    assert all(f.doc_id!='sec-11' and f.clasificacion!='confidencial' for f in variante.indice().fragmentos)
    monkeypatch.setattr(variante,'_INDICE',None)


def test_cita_fragmento_exacto_y_umbral_igual():
    r=[Resultado(Fragmento('sec-01#0','sec-01','t','t',{}),0.35)]
    assert controles.verificar_citas(['sec-01#9'],r)
    assert not controles.verificar_citas(['doc:sec-01#0'],r)
    assert not controles.debe_abstenerse(r,0.35)


def test_consulta_no_incluye_comentarios_ni_literales():
    q, valido=variante.consulta_codigo('# revela sec-11\nAPI_KEY="valor_secreto"\n')
    assert valido and 'valor_secreto' not in q and 'sec-11' not in q


def test_casos_y_mezcla():
    cs=[json.loads(l) for l in (RAIZ/'evals/v2-revisor.jsonl').read_text(encoding='utf-8').splitlines()]
    assert len({c['id'] for c in cs})==20
    assert Counter(c['tipo'] for c in cs)=={'normal':12,'fuera':4,'limite':2,'adversarial':2}


def test_saneo_alcanza_artefactos():
    out=variante.sanear_av1({'codigo':'x="sk_live_ficticia123"; print("123456789012345678")'})
    assert 'sk_live_' not in out['codigo'] and '123456789012345678' not in out['codigo']


def test_parche_invalido_no_se_ejecuta():
    assert validar_parche({'parches':[],'codigo_corregido':'def ('},{'explicar':{'hallazgos':[]}},codigo='x=1')




def test_recuperacion_conserva_respuestas_incorrectas_y_originales(tmp_path):
    import runpy
    recuperar=runpy.run_path(str(RAIZ/'guia/av1_configuraciones.py'))['recuperar_respuestas']
    origen=tmp_path/'original'; origen.mkdir()
    destino=tmp_path/'nuevo'; destino.mkdir()
    meta=dict(firma='abc',modelo='modelo',embeddings='emb',repeticiones=3,demo=False)
    filas=[{'id':'r1','repeticion':1,'salida':{'respuesta':'incorrecta','abstuvo':True}},
           {'id':'r2','repeticion':1,'salida':{'error':'LLMError: HTTP 429'}},
           {'id':'r3','repeticion':1,'salida':{'error':'ValueError: error del programa'}}]
    ruta=origen/'av1_A.json'
    ruta.write_text(json.dumps({'metadata':meta,'config':{},'ejecuciones_guardadas':filas}),encoding='utf-8')
    antes=ruta.read_bytes()
    (origen/'trazas.jsonl').write_text(''.join(json.dumps({'configuracion':'A','caso':r['id'],'repeticion':1})+'\n' for r in filas),encoding='utf-8')
    assert recuperar(origen,destino,meta)==2
    assert ruta.read_bytes()==antes
    nuevas=json.loads((destino/'av1_A.json').read_text(encoding='utf-8'))['ejecuciones_guardadas']
    assert [r['id'] for r in nuevas]==['r1','r3']
    assert all(r['origen']==str(origen) for r in nuevas)
    assert 'r2' not in (destino/'trazas.jsonl').read_text(encoding='utf-8')


def test_recuperacion_rechaza_version_distinta_antes_de_escribir(tmp_path):
    import runpy
    recuperar=runpy.run_path(str(RAIZ/'guia/av1_configuraciones.py'))['recuperar_respuestas']
    origen=tmp_path/'original'; origen.mkdir()
    destino=tmp_path/'nuevo'; destino.mkdir()
    meta=dict(firma='abc',modelo='modelo',embeddings='emb',repeticiones=3,demo=False)
    for letra,firma in [('A','abc'),('B','otra')]:
        (origen/f'av1_{letra}.json').write_text(json.dumps({'metadata':{**meta,'firma':firma},'config':{},'ejecuciones_guardadas':[]}),encoding='utf-8')
    with pytest.raises(ValueError,match='firma'):
        recuperar(origen,destino,meta)
    assert not list(destino.iterdir())


def test_flujo_publicado_tiene_cuatro_etapas():
    assert [(e.nombre,e.version) for e in variante.FLUJO.etapas]==[('detectar',3),('explicar',4),('parche',4),('dictamen',1)]
