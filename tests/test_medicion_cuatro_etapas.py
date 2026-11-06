"""La comparación nueva incluye dictamen y no mezcla evidencia de tres etapas."""
import copy
import json
import runpy

import pytest
from finnorte.config import RAIZ
from finnorte import variante

medidor = runpy.run_path(str(RAIZ / 'guia/av1_configuraciones.py'))


@pytest.mark.parametrize('letra,versiones', [('A', [1,1,1,1]), ('B', [4,5,5,2]),
                                          ('C', [4,5,5,2]), ('D', [4,5,5,2])])
def test_perfil_ejecuta_las_cuatro_versiones(monkeypatch, letra, versiones):
    class IndiceVacio:
        def buscar(self, *a, **kw): return []
    monkeypatch.setattr(variante, 'indice', lambda: IndiceVacio())
    vistas = []
    class FinInspeccion(Exception): pass
    class Captura:
        def __init__(self, etapas, **kw): vistas.extend(etapas)
        def ejecutar(self, valores): raise FinInspeccion
    monkeypatch.setattr(variante, 'Pipeline', Captura)
    with pytest.raises(FinInspeccion):
        variante.sistema({'codigo': 'x = 1'}, medidor['configuraciones'](True)[letra])
    assert [e.nombre for e in vistas] == ['detectar','explicar','parche','dictamen']
    assert [e.version for e in vistas] == versiones
    assert vistas[-1].usa == ['explicar','parche']
    assert bool(vistas[-1].validar) == (letra == 'D')


def test_consistencia_detecta_un_dictamen_distinto():
    original = {'artefacto': {'dictamen': {'estado':'sin_hallazgos','total_hallazgos':0,'hallazgos':[]}}}
    cambiado = copy.deepcopy(original)
    cambiado['artefacto']['dictamen']['total_hallazgos'] = 1
    assert medidor['firma_salida'](original) != medidor['firma_salida'](cambiado)


def test_recuperacion_rechaza_otro_alcance(tmp_path):
    origen, destino = tmp_path/'antes', tmp_path/'nuevo'
    origen.mkdir(); destino.mkdir()
    meta = dict(firma='igual',modelo='modelo',embeddings='emb',repeticiones=3,demo=False,
                dictamen='no incluido en A/B/C/D')
    (origen/'av1_A.json').write_text(json.dumps({'metadata':meta}),encoding='utf-8')
    with pytest.raises(ValueError, match='dictamen'):
        medidor['recuperar_respuestas'](origen,destino,{**meta,'dictamen':'incluido en A/B/C/D'})
    assert not list(destino.iterdir())
