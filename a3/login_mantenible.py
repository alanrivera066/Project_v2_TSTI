"""Versión 3 · MANTENIBILIDAD del login() oficial.

Qué cambió
  1. Una clase Autenticador con el almacén de usuarios inyectable: en pruebas se usa un dict y
     en producción podría ser una base de datos, sin cambiar login().
  2. Resultados como Enum (Resultado.OK, Resultado.ERROR, Resultado.BLOQUEADO) en vez de textos
     sueltos: un error de dedo como "user not found " ya no es posible.
  3. Constantes con nombre, tipos y docstrings: se entiende qué hace cada parte sin adivinar.
  4. Las reglas de seguridad de la versión 1 se mantienen, pero cada una en su propio método.

Por qué
  El original mezcla datos, reglas y mensajes en 6 líneas; cambiar cualquier cosa obliga a
  reescribirlo y no se puede probar por partes.

Matriz problema → versión → evidencia
  | Problema del original            | Qué lo resuelve aquí           | Evidencia (prueba)                          |
  |----------------------------------|--------------------------------|---------------------------------------------|
  | Datos dentro del código          | almacén inyectable (__init__)  | test_a3_login::test_mantenible_almacen      |
  | Textos mágicos y con errores     | Enum Resultado                 | test_a3_login::test_mantenible_enum         |
  | Todo en una función              | _verificar() y _bloqueado()    | métodos de la clase                         |
  | Sin pruebas                      | tests/test_a3_login.py         | las 3 pruebas oficiales en verde            |
"""
from __future__ import annotations

import hashlib
import hmac
import os
from enum import Enum


class Resultado(str, Enum):
    OK = "access granted"
    ERROR = "invalid credentials"
    BLOQUEADO = "account locked"


class Autenticador:
    ITERACIONES = 200_000
    MAX_FALLOS = 5

    def __init__(self, almacen: dict[str, tuple[bytes, bytes]] | None = None):
        self.almacen = almacen if almacen is not None else {}
        self.fallos: dict[str, int] = {}

    def registrar(self, usuario: str, contrasena: str) -> None:
        sal = os.urandom(16)
        self.almacen[usuario] = (sal, self._huella(contrasena, sal))

    def login(self, usuario: str, contrasena: str) -> Resultado:
        if self._bloqueado(usuario):
            return Resultado.BLOQUEADO
        if self._verificar(usuario, contrasena):
            self.fallos.pop(usuario, None)
            return Resultado.OK
        self.fallos[usuario] = self.fallos.get(usuario, 0) + 1
        return Resultado.ERROR

    def _huella(self, contrasena: str, sal: bytes) -> bytes:
        return hashlib.pbkdf2_hmac("sha256", contrasena.encode(), sal, self.ITERACIONES)

    def _verificar(self, usuario: str, contrasena: str) -> bool:
        """Compara en tiempo constante; si el usuario no existe, compara contra un valor falso."""
        sal, guardada = self.almacen.get(usuario, (b"\x00" * 16, b""))
        return hmac.compare_digest(self._huella(contrasena, sal), guardada) and usuario in self.almacen

    def _bloqueado(self, usuario: str) -> bool:
        return self.fallos.get(usuario, 0) >= self.MAX_FALLOS


_por_defecto = Autenticador()


def registrar(user: str, password: str) -> None:
    _por_defecto.registrar(user, password)


def login(user: str, password: str) -> str:
    """Misma firma que el login() oficial, para poder compararlos."""
    return _por_defecto.login(user, password).value
