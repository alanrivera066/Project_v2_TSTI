import json
from types import SimpleNamespace
from finnorte import llm, pipeline

def test_esquema_rechaza_formato_incorrecto():
    esquema = {'type':'object','required':['hallazgos'],'additionalProperties':False,
               'properties':{'hallazgos':{'type':'array'}}}
    assert pipeline.validar_esquema({'otro':1}, esquema)
    assert not pipeline.validar_esquema({'hallazgos':[]}, esquema)

def test_reintento_conserva_error_y_valida_dependencia(monkeypatch):
    llamadas = []
    def cargar(id, version):
        return SimpleNamespace(variables={'entrada'}, salida_json=True, nombre=id+'.v1',
            esquema={'type':'object','required':['ok']}, render=lambda **kw: ('sistema',kw['entrada']))
    monkeypatch.setattr(pipeline.prompts,'cargar',cargar)
    def responder(p,s):
        llamadas.append(p)
        return 'no es JSON' if len(llamadas)==1 else json.dumps({'ok':True})
    llm.fake.responder = responder
    r = pipeline.Pipeline([pipeline.Etapa('uno','prueba')]).ejecutar({'entrada':'dato'})
    assert r.ok and r.etapas[0].intentos==2
    assert 'no cumplió el formato' in llamadas[1]

def test_dependencia_no_ejecutada_se_rechaza(monkeypatch):
    monkeypatch.setattr(pipeline.prompts,'cargar',lambda *a: SimpleNamespace(variables=set()))
    import pytest
    with pytest.raises(ValueError,match='no se ejecutó'):
        pipeline.Pipeline([pipeline.Etapa('dos','prueba',usa=['uno'])]).ejecutar({})
