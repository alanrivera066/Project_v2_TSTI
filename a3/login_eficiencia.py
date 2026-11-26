"""Versión 2 · EFICIENCIA del login() oficial.

Qué cambió
  1. Los usuarios se buscan en un diccionario (una sola búsqueda, sin importar si hay 1 o 1 millón).
     El original solo funciona para "admin"; agregar usuarios exigiría más if anidados.
  2. Un solo camino de salida: una búsqueda y una comparación, sin ramas repetidas.
  3. El costo del hash (ITERACIONES) es un parámetro: se ajusta sin tocar la lógica.
  4. Se conservan hash con sal y compare_digest: ser rápido no debe abrir un hueco de seguridad.

Por qué
  El original no escala: cada usuario nuevo es otro if. En un servicio real lo caro es el hash
  de la contraseña, así que se hace una sola vez por intento y nada más.

Matriz problema → versión → evidencia
  | Problema del original              | Qué lo resuelve aquí          | Evidencia (prueba)                          |
  |------------------------------------|-------------------------------|---------------------------------------------|
  | Solo sirve para un usuario         | dict USUARIOS                 | test_a3_login::test_eficiencia_muchos       |
  | Ifs anidados, varias salidas       | un solo return por resultado  | función login() (2 returns)                 |
  | Costo fijo imposible de ajustar    | parámetro iteraciones         | test_a3_login::test_eficiencia_muchos       |
  | Espacio extra en "user not found " | MENSAJE_ERROR sin espacios    | test_a3_login::test_mismo_mensaje           |
"""
import hashlib
import hmac
import os

ITERACIONES = 200_000
MENSAJE_OK = "access granted"
MENSAJE_ERROR = "invalid credentials"
USUARIOS: dict[str, tuple[bytes, bytes]] = {}


def registrar(user: str, password: str, iteraciones: int = ITERACIONES) -> None:
    sal = os.urandom(16)
    USUARIOS[user] = (sal, hashlib.pbkdf2_hmac("sha256", password.encode(), sal, iteraciones))


def login(user: str, password: str, iteraciones: int = ITERACIONES) -> str:
    sal, guardada = USUARIOS.get(user, (b"\x00" * 16, b""))
    calculada = hashlib.pbkdf2_hmac("sha256", password.encode(), sal, iteraciones)
    if user in USUARIOS and hmac.compare_digest(calculada, guardada):
        return MENSAJE_OK
    return MENSAJE_ERROR
