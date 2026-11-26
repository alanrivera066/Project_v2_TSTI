"""A3 · Pruebas del login() oficial y de sus 3 versiones.

Las 3 pruebas oficiales (login exitoso, contraseña incorrecta, usuario inexistente) corren
sobre las 4 versiones. Después, pruebas propias que demuestran lo que cada versión dice resolver.
"""
import importlib
from pathlib import Path

import pytest

from a3 import login_original

MEJORADAS = ["a3.login_seguridad", "a3.login_eficiencia", "a3.login_mantenible"]


@pytest.fixture(params=MEJORADAS)
def version(request):
    m = importlib.reload(importlib.import_module(request.param))   # estado limpio en cada prueba
    m.registrar("admin", "Rivera-Garza-26")
    return m


# ───────────── las 3 pruebas oficiales ─────────────
def test_oficial_original():
    assert login_original.login("admin", "1234") == "access granted"
    assert login_original.login("admin", "otra") == "wrong password"
    assert login_original.login("nadie", "1234") == "user not found "   # el espacio extra es un defecto


def test_login_exitoso(version):
    assert version.login("admin", "Rivera-Garza-26") == "access granted"


def test_contrasena_incorrecta(version):
    assert version.login("admin", "equivocada") == "invalid credentials"


def test_usuario_inexistente(version):
    assert version.login("nadie", "Rivera-Garza-26") == "invalid credentials"


# ───────────── pruebas propias ─────────────
def test_mismo_mensaje(version):
    """No se puede saber si un usuario existe por el mensaje (SEC)."""
    assert version.login("admin", "equivocada") == version.login("nadie", "equivocada")


def test_sin_credenciales_en_codigo():
    for nombre in MEJORADAS:
        texto = Path(importlib.import_module(nombre).__file__).read_text(encoding="utf-8")
        assert '"1234"' not in texto and '== "admin"' not in texto


def test_seguridad_guarda_hash():
    from a3 import login_seguridad as s
    s.registrar("ana", "Rivera-Garza-26")
    sal, huella = s._USUARIOS["ana"]
    assert len(sal) == 16 and b"Rivera-Garza-26" not in huella


def test_seguridad_bloquea():
    s = importlib.reload(importlib.import_module("a3.login_seguridad"))
    s.registrar("admin", "Rivera-Garza-26")
    for _ in range(5):
        s.login("admin", "mala")
    assert s.login("admin", "Rivera-Garza-26") == "account locked"


def test_eficiencia_muchos():
    e = importlib.reload(importlib.import_module("a3.login_eficiencia"))
    for i in range(50):
        e.registrar(f"u{i}", f"clave-{i}", iteraciones=1_000)
    assert e.login("u42", "clave-42", iteraciones=1_000) == "access granted"
    assert e.login("u42", "clave-41", iteraciones=1_000) == "invalid credentials"


def test_mantenible_almacen():
    from a3.login_mantenible import Autenticador, Resultado
    almacen = {}
    a = Autenticador(almacen)
    a.registrar("ana", "Rivera-Garza-26")
    assert "ana" in almacen and a.login("ana", "Rivera-Garza-26") is Resultado.OK


def test_mantenible_enum():
    from a3.login_mantenible import Autenticador, Resultado
    a = Autenticador()
    assert a.login("nadie", "x") is Resultado.ERROR and Resultado.ERROR.value == "invalid credentials"
