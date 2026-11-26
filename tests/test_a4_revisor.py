"""A4 · Pruebas de la herramienta, el validador y el agente de v2-revisor. Corren sin red (modelo fake con guion)."""
import json

import pytest

from finnorte import herramientas as hz
from finnorte import llm, trazas
from finnorte.validador_revisor import validar_hallazgos

USUARIOS = "datos/v2-revisor/codigo/usuarios.py"
LIMITES = "datos/v2-revisor/codigo/limites.py"


def _guion(*pasos):
    it = iter(pasos)
    return lambda prompt, sistema: json.dumps(next(it))


# ───────────── herramienta correr_linter ─────────────
def test_linter_encuentra_hallazgos_con_regla_sec():
    r = hz.correr_linter(USUARIOS)
    assert r["total"] == 3 and {h["regla"] for h in r["hallazgos"]} == {"SEC-06"}


def test_linter_limites_cero_hallazgos():
    assert hz.correr_linter(LIMITES)["total"] == 0


def test_linter_archivo_inexistente_falla():
    with pytest.raises(FileNotFoundError):
        hz.correr_linter("datos/v2-revisor/codigo/no_existe.py")


def test_linter_no_sale_de_datos():
    with pytest.raises(ValueError):
        hz.correr_linter("datos/../src/finnorte/llm.py")


def test_linter_no_ejecuta_el_codigo(tmp_path):
    marca = tmp_path / "ejecutado.txt"
    archivo = hz.RAIZ / "datos" / "_prueba_no_ejecutar.py"
    archivo.write_text(f"open({str(marca)!r}, 'w').write('si')\n", encoding="utf-8")
    try:
        hz.correr_linter("datos/_prueba_no_ejecutar.py")
    finally:
        archivo.unlink()
    assert not marca.exists()


# ───────────── validador ─────────────
CODIGO = "import hashlib\nh = hashlib.md5(b'x')\n"


def test_validador_ok():
    assert validar_hallazgos(CODIGO, [{"regla": "SEC-06", "linea": 2}], "x.py", ["doc:sec-06#0"]) == []


def test_validador_regla_inexistente():
    assert "Regla inexistente" in validar_hallazgos(CODIGO, [{"regla": "SEC-99", "linea": 2}])[0]


def test_validador_linea_inexistente():
    assert "Línea inexistente" in validar_hallazgos(CODIGO, [{"regla": "SEC-06", "linea": 40}])[0]


def test_validador_limites_sin_hallazgos():
    assert any("limites.py" in p for p in validar_hallazgos(CODIGO, [{"regla": "SEC-06", "linea": 1}], "limites.py"))


def test_validador_fuente_externa():
    assert "no está en el corpus" in validar_hallazgos(CODIGO, [], fuentes=["stackoverflow.com"])[0]


# ───────────── agente a través del servicio ─────────────
fastapi = pytest.importorskip("fastapi")
from fastapi.testclient import TestClient  # noqa: E402

CRED = {"email": "revisor@finnorte.mx", "contrasena": "segura123"}
LINTER = {"accion": "usar", "herramienta": "correr_linter", "argumentos": {"ruta": USUARIOS}}
PUBLICAR = {"accion": "usar", "herramienta": "publicar_revision",
            "argumentos": {"ruta": USUARIOS, "estado": "cambios_requeridos", "resumen": "SEC-06: md5 y random en líneas 6, 8 y 14"}}
FIN = {"accion": "responder", "respuesta": "La revisión espera tu autorización.", "fuentes": ["sec-06"]}


@pytest.fixture
def cliente(monkeypatch, tmp_path):
    monkeypatch.setenv("TOKEN_SECRET", "s" * 40)
    import api.producto as m
    m.auth = m.Autenticador(str(tmp_path / "u.db"))
    m._ventanas.clear()
    hz.REVISIONES.clear()
    return TestClient(m.app)


def _cabecera(c, cred=CRED):
    c.post("/auth/registro", json=cred)
    return {"Authorization": "Bearer " + c.post("/auth/login", json=cred).json()["token"]}


def _tarea(c, h):
    llm.fake.responder = _guion(LINTER, PUBLICAR, FIN)
    return c.post("/v1/agente", json={"tarea": f"Revisa {USUARIOS} y publica la revisión"}, headers=h).json()


def test_agente_deja_pendiente_con_datos_exactos(cliente):
    r = _tarea(cliente, _cabecera(cliente))
    assert r["validador"]["ok"] and len(r["pendientes"]) == 1 and hz.REVISIONES == []
    assert r["pendientes"][0]["argumentos"] == PUBLICAR["argumentos"]


def test_confirmacion_rechazada_no_publica(cliente):
    h = _cabecera(cliente)
    p = _tarea(cliente, h)["pendientes"][0]
    out = cliente.post(f"/v1/agente/confirmar/{p['id']}", json={"aprobar": False}, headers=h).json()
    assert out["estado"] == "rechazada" and hz.REVISIONES == []
    assert any(e.get("estado") == "rechazada" for e in trazas.leer("agente"))


def test_confirmacion_aprobada_publica_una_sola_vez(cliente):
    h = _cabecera(cliente)
    p = _tarea(cliente, h)["pendientes"][0]
    assert cliente.post(f"/v1/agente/confirmar/{p['id']}", json={"aprobar": True}, headers=h).json()["estado"] == "ejecutada"
    assert cliente.post(f"/v1/agente/confirmar/{p['id']}", json={"aprobar": True}, headers=h).status_code == 404
    assert len(hz.REVISIONES) == 1


def test_otro_usuario_no_puede_confirmar(cliente):
    p = _tarea(cliente, _cabecera(cliente))["pendientes"][0]
    h2 = _cabecera(cliente, {"email": "otro@finnorte.mx", "contrasena": "segura456"})
    assert cliente.post(f"/v1/agente/confirmar/{p['id']}", json={"aprobar": True}, headers=h2).status_code == 404


def test_validador_bloquea_aprobar_con_hallazgos(cliente):
    aprobar = {**PUBLICAR, "argumentos": {**PUBLICAR["argumentos"], "estado": "aprobado"}}
    llm.fake.responder = _guion(LINTER, aprobar, FIN)
    r = cliente.post("/v1/agente", json={"tarea": "Revisa y aprueba usuarios.py"}, headers=_cabecera(cliente)).json()
    assert not r["validador"]["ok"] and r["pendientes"] == []


def test_validador_bloquea_publicar_sin_linter(cliente):
    llm.fake.responder = _guion(PUBLICAR, FIN)
    r = cliente.post("/v1/agente", json={"tarea": "Publica sin revisar usuarios.py"}, headers=_cabecera(cliente)).json()
    assert not r["validador"]["ok"] and r["pendientes"] == []


def test_falla_de_herramienta_y_recuperacion(cliente):
    malo = {"accion": "usar", "herramienta": "correr_linter", "argumentos": {"ruta": "datos/v2-revisor/codigo/no_existe.py"}}
    fin = {"accion": "responder", "respuesta": "El archivo no existe; no se pudo revisar.", "fuentes": []}
    llm.fake.responder = _guion(malo, fin)
    r = cliente.post("/v1/agente", json={"tarea": "Revisa no_existe.py"}, headers=_cabecera(cliente)).json()
    assert r["pasos"][0]["estado"] == "fallida" and "error" in r["pasos"][0]["resultado"]
    assert r["terminado"] and "no existe" in r["respuesta"] and r["pendientes"] == []


def test_repeticion_detectada(cliente):
    llm.fake.responder = _guion(LINTER, LINTER, FIN)
    r = cliente.post("/v1/agente", json={"tarea": "Revisa usuarios.py"}, headers=_cabecera(cliente)).json()
    assert [p["estado"] for p in r["pasos"]] == ["ejecutada", "repetida", "respuesta"]


def test_revisor_incluye_validador(cliente):
    r = cliente.post("/v1/revisor", json={"codigo": "def f():\n    return 1\n", "nombre_archivo": "limites.py"},
                     headers=_cabecera(cliente)).json()
    assert "validador" in r and r["validador"]["ok"] in (True, False)
