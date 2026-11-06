"""Etapa 4: el reporte no omite, inventa ni cambia lo recibido, y siempre dice qué pasó."""
import copy
import json
import sys

import pytest

from finnorte import llm, variante
from finnorte.config import RAIZ
from finnorte.dictamen import reporte_final, validar_dictamen
from finnorte.evaluacion import cargar_casos
from finnorte.pipeline import ResultadoEtapa, ResultadoFlujo
from finnorte.variante import FLUJO, leer_entrada

sys.path.insert(0, str(RAIZ / "guia"))
from demo_revisor import respuestas_para

H1 = {"id": "H1", "regla": "SEC-01", "linea": 3, "descripcion": "Credencial en el código",
      "explicacion": "SEC-01, línea 3: la credencial queda en el repositorio."}
H2 = {"id": "H2", "regla": "SEC-02", "linea": 8, "descripcion": "SQL con f-string",
      "explicacion": "SEC-02, línea 8: la consulta admite inyección."}


RESUMEN = "Se encontraron 2 hallazgos: SEC-01 en línea 3; SEC-02 en línea 8. Los parches son propuestas y requieren revisión humana."


def previas():
    return {"explicar": {"hallazgos": [copy.deepcopy(H1), copy.deepcopy(H2)]},
            "parche": {"parches": [{"id": "H1", "regla": "SEC-01", "linea": 3, "cambio": "Usar variable de entorno"},
                                   {"id": "H2", "regla": "SEC-02", "linea": 8, "cambio": "Parametrizar la consulta"}],
                       "codigo_corregido": "x = 1\n"}}


def fiel():
    return {"estado": "con_hallazgos", "total_hallazgos": 2,
            "hallazgos": [dict(H1, cambio="Usar variable de entorno"), dict(H2, cambio="Parametrizar la consulta")],
            "resumen": RESUMEN}


def test_reporte_fiel_pasa():
    assert validar_dictamen(fiel(), previas()) == []


@pytest.mark.parametrize("alterar,esperado", [
    (lambda d: d["hallazgos"].pop(), "omite H2"),
    (lambda d: d["hallazgos"].append(dict(H2, id="H9", cambio="x")), "inventa H9"),
    (lambda d: d["hallazgos"].append(copy.deepcopy(d["hallazgos"][0])), "más de una vez"),
    (lambda d: d["hallazgos"][0].update(regla="SEC-09"), "cambió regla"),
    (lambda d: d["hallazgos"][0].update(linea=4), "cambió linea"),
    (lambda d: d["hallazgos"][0].update(descripcion="otra"), "cambió descripcion"),
    (lambda d: d["hallazgos"][1].update(explicacion="SEC-02, línea 8: parafraseada."), "cambió explicacion"),
    (lambda d: d["hallazgos"][1].update(cambio="otro parche"), "cambió cambio"),
    (lambda d: d["hallazgos"][0].update(fuente="doc:sec-01#0"), "cambió fuente"),
    (lambda d: d.update(total_hallazgos=3), "total_hallazgos"),
    (lambda d: d.update(estado="sin_hallazgos"), "estado"),
    (lambda d: d.update(resumen="También incumple SEC-07."), "SEC-07"),
    (lambda d: d.update(resumen="Revisar H7."), "H7"),
    (lambda d: d.update(resumen="El problema está en la línea 40."), "línea 40"),
    (lambda d: d.update(resumen="La llave sk_live_abcd1234 queda expuesta."), "credencial"),
    (lambda d: d.update(resumen="La CLABE 123456789012345678 queda expuesta."), "18 dígitos"),
    (lambda d: d.update(resumen="Los problemas ya se corrigieron."), "propuesta"),
    (lambda d: d.update(resumen="El archivo es seguro."), "propuesta"),
    (lambda d: d.update(resumen=RESUMEN.replace("SEC-02 en línea 8", "línea 8")), "omite SEC-02"),
    (lambda d: d.update(resumen=RESUMEN.replace("2 hallazgos", "varios hallazgos")), "total de 2"),
    (lambda d: d.update(resumen=RESUMEN + " Busca mitigar la vulnerabilidad."), "mitigar"),
])
def test_cada_alteracion_se_rechaza(alterar, esperado):
    dictamen = fiel()
    alterar(dictamen)
    assert any(esperado in e for e in validar_dictamen(dictamen, previas()))


def test_resumen_puede_usar_palabras_de_los_datos_recibidos():
    dictamen = fiel()
    dictamen["resumen"] = RESUMEN + " Revisar credencial y consulta."
    assert any("revisar" in e for e in validar_dictamen(dictamen, previas()))
    dictamen["resumen"] = RESUMEN + " Incluye credencial y consulta."
    assert any("incluye" in e and "credencial" not in e for e in validar_dictamen(dictamen, previas()))


def test_hallazgo_sin_parche_se_rechaza():
    datos = previas()
    datos["parche"]["parches"].pop()
    assert any("no tiene parche" in e for e in validar_dictamen(fiel(), datos))


def test_sin_hallazgos_exige_el_texto_exacto():
    datos = {"explicar": {"hallazgos": []}, "parche": {"parches": [], "codigo_corregido": "x = 1\n"}}
    limpio = {"estado": "sin_hallazgos", "total_hallazgos": 0, "hallazgos": [], "resumen": "sin hallazgos"}
    assert validar_dictamen(limpio, datos) == []
    assert validar_dictamen(dict(limpio, resumen="Todo bien"), datos)


def etapa(nombre, ok=True):
    return ResultadoEtapa(nombre, f"rev_{nombre}.v1", ok, {}, [], 1, 0.0, 0.0)


def test_reporte_muestra_los_hallazgos():
    texto = reporte_final(ResultadoFlujo({}, {"dictamen": fiel()}, [etapa("dictamen")]))
    assert "H1 · SEC-01 · línea 3" in texto and "Parametrizar la consulta" in texto


def test_reporte_sin_hallazgos():
    dictamen = {"estado": "sin_hallazgos", "total_hallazgos": 0, "hallazgos": [], "resumen": "sin hallazgos"}
    assert reporte_final(ResultadoFlujo({}, {"dictamen": dictamen}, [etapa("dictamen")])) == "sin hallazgos"


@pytest.mark.parametrize("etapas,salidas,esperado", [
    ([etapa("detectar", ok=False)], {}, "detectar"),
    ([etapa("dictamen", ok=False)], {"dictamen": fiel()}, "dictamen"),
    ([etapa("parche")], {}, "sin dictamen"),
])
def test_revision_fallida_avisa_y_no_muestra_datos(etapas, salidas, esperado):
    texto = reporte_final(ResultadoFlujo({}, salidas, etapas))
    assert texto.startswith("REVISIÓN FALLIDA") and esperado in texto and "SEC-01" not in texto


def instalar(nombre, codigo, modificar=None):
    candidatos = {"tokens.py": "tokens.py", "limites.py": "limites.py"}
    respuestas = respuestas_para(candidatos[nombre], codigo)
    if modificar:
        modificar(respuestas)
    llamadas = []

    def responder(prompt, sistema):
        llamadas.append(sistema)
        return next(json.dumps(v) for marca, v in respuestas.items() if marca in sistema)

    llm.fake.responder = responder
    return llamadas


def leer(nombre):
    return (RAIZ / "datos/v2-revisor/codigo" / nombre).read_text(encoding="utf-8")


def test_dictamen_recibe_la_salida_real_de_explicar_y_parche():
    assert next(e for e in FLUJO.etapas if e.nombre == "dictamen").usa == ["explicar", "parche"]
    codigo = leer("tokens.py")
    instalar("tokens.py", codigo)
    vistos = []
    responder = llm.fake.responder
    llm.fake.responder = lambda p, s: (vistos.append(p) if "redactor técnico" in s else None) or responder(p, s)
    res = FLUJO.ejecutar({"entrada": codigo})
    assert res.ok and "H1" in res.salidas["dictamen"]["hallazgos"][0]["id"]
    assert "Deserialización YAML insegura" in vistos[0] and "Corrección preparada" in vistos[0]


def test_dictamen_alterado_reintenta_y_termina_en_aviso():
    codigo = leer("tokens.py")

    def modificar(respuestas):
        respuestas["Eres redactor técnico"]["hallazgos"][0]["cambio"] = "otro"

    instalar("tokens.py", codigo, modificar)
    res = FLUJO.ejecutar({"entrada": codigo})
    assert not res.ok and res.etapas[-1].nombre == "dictamen" and res.etapas[-1].intentos == 2
    assert reporte_final(res).startswith("REVISIÓN FALLIDA")


def test_etapa_anterior_fallida_no_llama_al_dictamen():
    codigo = leer("tokens.py")

    def modificar(respuestas):
        respuestas["Eres revisor técnico"]["hallazgos"][0]["linea"] = 1

    llamadas = instalar("tokens.py", codigo, modificar)
    res = FLUJO.ejecutar({"entrada": codigo})
    assert [e.nombre for e in res.etapas] == ["detectar", "explicar"]
    assert not any("redactor técnico" in s for s in llamadas)
    assert "explicar" in reporte_final(res)


def test_a_b_c_d_siguen_siendo_tres_etapas():
    import runpy
    configs = runpy.run_path(str(RAIZ / "guia/av1_configuraciones.py"))["CONFIGS"]
    assert all(c["incluir_dictamen"] is False for c in configs.values())


def test_sistema_entrega_reporte_con_dictamen(monkeypatch):
    class Sin:
        def buscar(self, *a, **k):
            return []
    monkeypatch.setattr(variante, "indice", lambda: Sin())
    codigo = leer("limites.py")
    instalar("limites.py", codigo)
    r = variante.sistema({"codigo": codigo}, {"usar_rag": False})
    assert r["respuesta"] == "sin hallazgos" and r["artefacto"]["dictamen"]["estado"] == "sin_hallazgos"


def test_seis_casos_con_la_mezcla_pedida():
    casos = cargar_casos(RAIZ / "evals/v2-revisor-dictamen.jsonl")
    assert [c["tipo"] for c in casos] == ["limpio"] * 2 + ["un_problema"] * 3 + ["dos_problemas"]
    assert [len(c["esperado"]["reglas"]) for c in casos] == [0, 0, 1, 1, 1, 2]
    for caso in casos:
        compile(leer_entrada(caso["entrada"]), caso["id"], "exec")
