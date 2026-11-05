"""Regresiones del Lab 2: dependencia real, errores de negocio y código nunca ejecutado."""
import json
import sys

import pytest

from finnorte import llm, trazas
from finnorte.config import RAIZ
from finnorte.reglas import validar_parche
from finnorte.variante import FLUJO_V1

sys.path.insert(0, str(RAIZ / "guia"))
from demo_revisor import respuestas_para


def instalar_respuestas(nombre, codigo, modificar=None):
    respuestas = respuestas_para(nombre, codigo)
    if modificar:
        modificar(respuestas)

    def responder(prompt, sistema):
        for marca, salida in respuestas.items():
            if marca in sistema:
                return json.dumps(salida)
        raise AssertionError("Prompt no reconocido")

    llm.fake.responder = responder


@pytest.mark.parametrize("nombre,total", [("transferencias.py", 4), ("tokens.py", 1), ("limites.py", 0)])
def test_tres_archivos_recorran_tres_etapas(nombre, total):
    codigo = (RAIZ / "datos/v2-revisor/codigo" / nombre).read_text(encoding="utf-8")
    instalar_respuestas(nombre, codigo)
    res = FLUJO_V1.ejecutar({"entrada": codigo, "contexto": "(sin contexto)"})
    assert res.ok and len(res.etapas) == 3
    assert len(res.salidas["detectar"]["hallazgos"]) == total
    assert len(res.salidas["parche"]["parches"]) == total


@pytest.mark.parametrize("marca,campo,valor,etapa", [
    ("Eres revisor de seguridad", "linea", 99999, "detectar"),
    ("Eres revisor técnico", "linea", 1, "explicar"),
])
def test_linea_inexistente_o_cambiada_detiene_el_flujo(marca, campo, valor, etapa):
    codigo = (RAIZ / "datos/v2-revisor/codigo/tokens.py").read_text(encoding="utf-8")

    def modificar(respuestas):
        respuestas[marca]["hallazgos"][0][campo] = valor

    instalar_respuestas("tokens.py", codigo, modificar)
    res = FLUJO_V1.ejecutar({"entrada": codigo})
    assert not res.ok
    assert res.etapas[-1].nombre == etapa and res.etapas[-1].intentos == 2
    assert etapa == res.etapas[-1].nombre


def test_parche_no_compilable_se_rechaza():
    codigo = (RAIZ / "datos/v2-revisor/codigo/tokens.py").read_text(encoding="utf-8")
    instalar_respuestas("tokens.py", codigo,
                        lambda r: r["Eres desarrollador Python"].update(codigo_corregido="def roto(:"))
    res = FLUJO_V1.ejecutar({"entrada": codigo})
    assert not res.ok and res.etapas[-1].nombre == "parche"
    assert any("no compila" in e for e in res.etapas[-1].errores)




def test_validar_compila_sin_ejecutar_codigo(tmp_path):
    destino = tmp_path / "no-debe-crearse.txt"
    codigo = f"from pathlib import Path\nPath({str(destino)!r}).write_text('no ejecutar')\n"
    assert validar_parche({"parches": [], "codigo_corregido": codigo},
                          {"explicar": {"hallazgos": []}}, codigo=codigo) == []
    assert not destino.exists()


def test_conserva_error_del_primer_intento_en_trazas():
    codigo = (RAIZ / "datos/v2-revisor/codigo/limites.py").read_text(encoding="utf-8")
    respuestas = respuestas_para("limites.py", codigo)
    llamadas = []

    def responder(prompt, sistema):
        llamadas.append(prompt)
        if len(llamadas) == 1:
            return '{"hallazgos":[{"id":"H1","regla":"SEC-01","linea":999,"descripcion":"error preparado"}]}'
        for marca, salida in respuestas.items():
            if marca in sistema:
                return json.dumps(salida)

    llm.fake.responder = responder
    res = FLUJO_V1.ejecutar({"entrada": codigo})
    assert res.ok and res.etapas[0].intentos == 2
    assert "no cumplió el formato" in llamadas[1] and "999" in llamadas[1]
    intentos = trazas.leer("intento_etapa")
    assert intentos[0]["ok"] is False and intentos[0]["errores"]
    assert intentos[1]["ok"] is True
