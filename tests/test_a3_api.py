"""A3 · Pruebas propias del servicio: token expirado, token alterado, bloqueo, 422 y el endpoint /v1/revisor.
Corren sin red (LLM_PROVIDER=fake)."""
import time

import pytest

pytest.importorskip("fastapi")
from fastapi.testclient import TestClient  # noqa: E402

CRED = {"email": "alan.rivera@finnorte.mx", "contrasena": "Mauricio2026"}
CODIGO = "def suma(a, b):\n    return a + b\n"


@pytest.fixture
def cliente(monkeypatch, tmp_path):
    monkeypatch.setenv("TOKEN_SECRET", "s" * 40)
    import api.producto as m
    m.auth = m.Autenticador(str(tmp_path / "u.db"))
    m._ventanas.clear()
    return TestClient(m.app)


def _cabecera(c):
    c.post("/auth/registro", json=CRED)
    return {"Authorization": "Bearer " + c.post("/auth/login", json=CRED).json()["token"]}


def test_revisor_sin_token_401_problem_json(cliente):
    r = cliente.post("/v1/revisor", json={"codigo": CODIGO})
    assert r.status_code == 401 and r.headers["content-type"].startswith("application/problem+json")


def test_revisor_con_token_responde(cliente):
    r = cliente.post("/v1/revisor", json={"codigo": CODIGO}, headers=_cabecera(cliente))
    assert r.status_code == 200 and {"respuesta", "fuentes", "abstuvo"} <= set(r.json())


def test_revisor_entrada_invalida_422(cliente):
    r = cliente.post("/v1/revisor", json={"codigo": "x"}, headers=_cabecera(cliente))
    assert r.status_code == 422 and r.json()["title"] == "Entrada inválida"


def test_token_expirado(cliente):
    from api import auth
    _cabecera(cliente)
    viejo = auth.emitir_token(CRED["email"], ahora=time.time() - 16 * 60)
    r = cliente.post("/v1/revisor", json={"codigo": CODIGO}, headers={"Authorization": f"Bearer {viejo}"})
    assert r.status_code == 401 and "expirado" in r.json()["detail"]


def test_token_alterado(cliente):
    h = _cabecera(cliente)
    payload, firma = h["Authorization"].removeprefix("Bearer ").split(".")
    falso = {"Authorization": f"Bearer {payload}.{firma[::-1]}"}
    assert cliente.post("/v1/revisor", json={"codigo": CODIGO}, headers=falso).status_code == 401


def test_bloqueo_tras_5_fallos(cliente):
    cliente.post("/auth/registro", json=CRED)
    for _ in range(5):
        assert cliente.post("/auth/login", json={**CRED, "contrasena": "incorrecta"}).status_code == 401
    r = cliente.post("/auth/login", json=CRED)
    assert r.status_code == 429 and r.headers["Retry-After"] == "60"


def test_limite_de_solicitudes(cliente, monkeypatch):
    import api.producto as m
    monkeypatch.setattr(m, "LIMITE_POR_MINUTO", 2)
    h = _cabecera(cliente)
    codigos = [cliente.post("/v1/revisor", json={"codigo": "z"}, headers=h).status_code for _ in range(3)]
    assert codigos[-1] == 429


def test_bitacora_no_guarda_contrasena(cliente):
    import api.producto as m
    cliente.post("/auth/registro", json=CRED)
    cliente.post("/auth/login", json={**CRED, "contrasena": "incorrecta"})
    filas = m.auth.db.execute("SELECT * FROM intentos").fetchall()
    assert filas and all("incorrecta" not in str(f) for f in filas)
