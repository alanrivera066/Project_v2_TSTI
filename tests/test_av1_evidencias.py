import copy
import json
import runpy

from finnorte.config import RAIZ
from finnorte.evaluacion import calificar_caso


def caso_limpio():
    return {'id': 'limpio', 'tipo': 'limite', 'entrada': {'codigo': 'x = 1\n'},
            'esperado': {'contiene': ['sin hallazgos'], 'hallazgos_vacios': True,
                         'codigo_sin_cambios': True, 'debe_abstenerse': False}}


def salida_limpia():
    return {'respuesta': 'sin hallazgos', 'fuentes': [], 'abstuvo': False,
            'artefacto': {'hallazgos': [], 'parches': [], 'codigo_corregido': 'x = 1\n'}}


def test_texto_sin_hallazgos_no_oculta_un_falso_positivo():
    buena = salida_limpia()
    assert calificar_caso(caso_limpio(), buena).acierto
    mala = copy.deepcopy(buena)
    mala['artefacto']['hallazgos'] = [{'regla': 'SEC-01'}]
    assert not calificar_caso(caso_limpio(), mala).acierto


def test_archivo_limpio_modificado_no_aprueba_por_su_respuesta():
    mala = salida_limpia()
    mala['artefacto']['codigo_corregido'] = 'x = 2\n'
    assert not calificar_caso(caso_limpio(), mala).acierto


def test_casos_legibles_y_limpio_con_validacion_estructural():
    casos = {c['id']: c for c in map(json.loads, (RAIZ/'evals/v2-revisor.jsonl').read_text(encoding='utf-8').splitlines())}
    assert '¿está bien' in casos['r09']['entrada']['codigo']
    assert casos['r06']['esperado']['hallazgos_vacios']
    assert casos['r06']['esperado']['codigo_sin_cambios']
    assert 'no_contiene' not in casos['r06']['esperado']


def test_huella_cubre_corpus_entradas_contrato_y_medidor(tmp_path):
    modulo = runpy.run_path(str(RAIZ/'guia/av1_configuraciones.py'))
    huella = modulo['huella_medicion']
    globals_reales = huella.__globals__
    anterior = globals_reales['RAIZ']
    globals_reales['RAIZ'] = tmp_path
    archivos = ['src/finnorte/variante.py', 'prompts/p.v1.md', 'prompts/esquemas/p.json',
                'corpus/v2-revisor/sec-01.md', 'datos/v2-revisor/codigo/a.py',
                'evals/v2-revisor.jsonl', 'contrato_calidad.yaml', 'guia/av1_configuraciones.py']
    archivo_anterior = globals_reales['__file__']
    globals_reales['__file__'] = str(tmp_path/'guia/av1_configuraciones.py')
    try:
        for nombre in archivos:
            p = tmp_path/nombre
            p.parent.mkdir(parents=True, exist_ok=True)
            p.write_text('original', encoding='utf-8')
        firma, manifiesto = huella()
        assert set(manifiesto) == set(archivos)
        for nombre in archivos:
            p = tmp_path/nombre
            p.write_text('cambio', encoding='utf-8')
            assert huella()[0] != firma
            p.write_text('original', encoding='utf-8')
        (tmp_path/'.env').write_text('NO ES UNA LLAVE REAL', encoding='utf-8')
        assert huella()[0] == firma
    finally:
        globals_reales['RAIZ'] = anterior
        globals_reales['__file__'] = archivo_anterior
