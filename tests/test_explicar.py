import pytest

from finnorte.reglas import validar_explicar


@pytest.mark.parametrize("texto,falla", [
    ("La credencial sk_live_CLAVE_FICTICIA queda expuesta.", True),
    ("El log muestra 123456789012345678 completo.", True),
    ("El log muestra una CLABE completa; registra solo los últimos cuatro dígitos.", False),
    ("La credencial sk_live_… debe leerse del entorno.", False),
    ("La referencia enmascarada termina en 5678.", False),
])
def test_explica_sin_reproducir_identificadores_completos(texto, falla):
    h = dict(id="H1", regla="SEC-03", linea=1, descripcion="Dato sensible expuesto")
    salida = {"hallazgos": [dict(h, explicacion="SEC-03, línea 1: " + texto)]}
    assert bool(validar_explicar(salida, {"detectar": {"hallazgos": [h]}})) == falla


def test_explica_con_referencia_autocontenida():
    h = dict(id="H1", regla="SEC-09", linea=6, descripcion="Carga YAML insegura")
    previa = {"detectar": {"hallazgos": [h]}}
    antes = {"hallazgos": [dict(h, explicacion="SEC-09: riesgo de ejecutar objetos al cargar YAML.")]}
    despues = {"hallazgos": [dict(h, explicacion="SEC-09, línea 6: riesgo de ejecutar objetos al cargar YAML.")]}
    assert any("línea 6" in e for e in validar_explicar(antes, previa))
    assert validar_explicar(despues, previa) == []


