"""Versión 1 · SEGURIDAD del login() oficial.

Qué cambió
  1. Ya no hay usuario ni contraseña escritos en el código: se registran con registrar().
  2. Se guarda una huella (hash PBKDF2-HMAC-SHA256 con sal), nunca la contraseña.
  3. Se compara con hmac.compare_digest (tiempo constante), no con ==.
  4. El mismo mensaje para "usuario no existe" y "contraseña incorrecta".
  5. Bloqueo tras 5 intentos fallidos seguidos.

Por qué
  El original permite adivinar usuarios (mensajes distintos), expone la contraseña en el código
  (SEC-01, ing-02) y deja probar contraseñas sin límite.

Matriz problema → versión → evidencia
  | Problema del original           | Qué lo resuelve aquí            | Evidencia (prueba)                             |
  |---------------------------------|---------------------------------|------------------------------------------------|
  | Credenciales en el código       | registrar() + _USUARIOS          | test_a3_login::test_sin_credenciales_en_codigo  |
  | Contraseña en texto plano       | _huella() con PBKDF2 y sal       | test_a3_login::test_seguridad_guarda_hash       |
  | Comparación con ==              | hmac.compare_digest en login()   | línea con compare_digest                        |
  | Mensajes que revelan usuarios   | MENSAJE_ERROR único              | test_a3_login::test_mismo_mensaje               |
  | Intentos ilimitados             | MAX_FALLOS y _fallos             | test_a3_login::test_seguridad_bloquea           |
"""
import hashlib
import hmac
import os

ITERACIONES = 200_000
MAX_FALLOS = 5
MENSAJE_OK = "access granted"
MENSAJE_ERROR = "invalid credentials"
MENSAJE_BLOQUEO = "account locked"

_USUARIOS: dict[str, tuple[bytes, bytes]] = {}   # usuario -> (sal, huella)
_fallos: dict[str, int] = {}
_SAL_FALSA = b"\x00" * 16                        # para tardar lo mismo si el usuario no existe


def _huella(password: str, sal: bytes) -> bytes:
    return hashlib.pbkdf2_hmac("sha256", password.encode(), sal, ITERACIONES)


def registrar(user: str, password: str) -> None:
    sal = os.urandom(16)
    _USUARIOS[user] = (sal, _huella(password, sal))


def login(user: str, password: str) -> str:
    if _fallos.get(user, 0) >= MAX_FALLOS:
        return MENSAJE_BLOQUEO
    sal, guardada = _USUARIOS.get(user, (_SAL_FALSA, b""))
    correcta = hmac.compare_digest(_huella(password, sal), guardada) and user in _USUARIOS
    if not correcta:
        _fallos[user] = _fallos.get(user, 0) + 1
        return MENSAJE_ERROR
    _fallos.pop(user, None)
    return MENSAJE_OK
