import pytest

from finnorte.llm import Respuesta


@pytest.mark.parametrize('modelo,esperado', [
    ('gemini-3.1-flash-lite', 1.75),
    ('gemini-3.5-flash-lite', 2.80),
])
def test_costo_usa_la_tarifa_del_modelo(modelo, esperado):
    respuesta = Respuesta('', 'gemini', modelo, tokens_entrada=1_000_000,
                          tokens_salida=1_000_000)
    assert respuesta.costo_usd == pytest.approx(esperado)
