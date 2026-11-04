import pytest

from finnorte.reglas import validar_detectar


@pytest.mark.parametrize("codigo,omision", [
    ("print(destino_clabe)\n", True),
    ('log.info("cliente %s", cliente["clabe"])\n', True),
    ('print("123456789012345678")\n', True),
    ('print("error al validar clabe")\n', False),
    ("print(str(clabe)[-4:])\n", False),
    ("print(clabe[-4::-1])\n", True),
    ("print(enmascarar(clabe))\n", False),
    ("# print(clabe)\nvalor = 1\n", False),
])
def test_cobertura_estatica_distingue_datos_y_mascaras(codigo, omision):
    errores = validar_detectar({"hallazgos": []}, {}, codigo=codigo)
    assert any("Falta SEC-03" in e for e in errores) == omision


def test_sec03_no_puede_apuntar_a_una_linea_ajena_al_registro():
    h = dict(id="H1", regla="SEC-03", linea=1, descripcion="Dato expuesto")
    errores = validar_detectar({"hallazgos": [h]}, {}, codigo='import logging\nprint(clabe)\n')
    assert any("no corresponde" in e for e in errores)
    assert any("Falta SEC-03" in e for e in errores)


def test_registro_multilinea_acepta_linea_del_argumento():
    h = dict(id="H1", regla="SEC-03", linea=2, descripcion="CLABE expuesta")
    assert validar_detectar({"hallazgos": [h]}, {}, codigo='print(\n    clabe\n)\n') == []




