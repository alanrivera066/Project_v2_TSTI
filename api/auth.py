"""Autenticación del servicio (Laboratorio A3+A4 · caso guía).

Registro, login y token, sin librerías externas. Requisitos mínimos de la A3:
  1. Contraseñas con hash y sal (PBKDF2-HMAC-SHA256), nunca texto plano ni MD5.
  2. Token con expiración de 15 minutos o menos.
  3. El MISMO mensaje para usuario inexistente y contraseña incorrecta.
  4. Comparación en tiempo constante (hmac.compare_digest).
  5. Bloqueo temporal tras intentos fallidos.
  6. La bitácora de intentos NO guarda la contraseña.

Las piezas marcadas TODO(LAB) las completamos juntos en el laboratorio con ayuda del asistente de IA.
El secreto para firmar tokens se lee de TOKEN_SECRET en .env (nunca en el código).
"""
from __future__ import annotations

import base64
import hashlib
import hmac
import json
import os
import re
import sqlite3
import time
from dataclasses import dataclass

ITERACIONES = 200_000
VIGENCIA_S = int(os.getenv("TOKEN_VIGENCIA_S", str(15 * 60)))
MAX_FALLOS, VENTANA_FALLOS_S = 5, 15 * 60
EMAIL = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")
MENSAJE_CREDENCIALES = "Correo o contraseña incorrectos"


def _secreto() -> bytes:
    s = os.getenv("TOKEN_SECRET", "")
    if len(s) < 32:
        raise RuntimeError("Define TOKEN_SECRET en .env con al menos 32 caracteres (python -c \"import secrets;print(secrets.token_hex(32))\")")
    return s.encode()


class ErrorAuth(Exception):
    def __init__(self, status: int, mensaje: str):
        super().__init__(mensaje)
        self.status = status


def _b64(b: bytes) -> str:
    return base64.urlsafe_b64encode(b).rstrip(b"=").decode()


def _unb64(s: str) -> bytes:
    return base64.urlsafe_b64decode(s + "=" * (-len(s) % 4))


def hash_contrasena(contrasena: str, sal: bytes | None = None) -> str:
    """Devuelve 'pbkdf2$<iteraciones>$<sal>$<hash>' (todo en base64url)."""
    sal = sal or os.urandom(16)                       # sal nueva y aleatoria para cada usuario
    huella = hashlib.pbkdf2_hmac("sha256", contrasena.encode(), sal, ITERACIONES)
    return f"pbkdf2${ITERACIONES}${_b64(sal)}${_b64(huella)}"


def verificar_contrasena(contrasena: str, guardado: str) -> bool:
    """Recalcula el hash con la misma sal y compara en TIEMPO CONSTANTE."""
    try:
        algoritmo, iteraciones, sal, huella = guardado.split("$")
        if algoritmo != "pbkdf2":
            return False
        calculada = hashlib.pbkdf2_hmac("sha256", contrasena.encode(), _unb64(sal), int(iteraciones))
    except (ValueError, TypeError):
        return False                                  # texto guardado con formato raro: no pasa
    return hmac.compare_digest(calculada, _unb64(huella))


def emitir_token(usuario: str, ahora: float | None = None) -> str:
    """Token 'payload.firma': payload = {sub, iat, exp} en base64url; firma = HMAC-SHA256 con TOKEN_SECRET."""
    ahora = int(ahora if ahora is not None else time.time())
    datos = {"sub": usuario, "iat": ahora, "exp": ahora + VIGENCIA_S}
    payload = _b64(json.dumps(datos, separators=(",", ":")).encode())
    firma = _b64(hmac.new(_secreto(), payload.encode(), hashlib.sha256).digest())
    return f"{payload}.{firma}"


def validar_token(token: str, ahora: float | None = None) -> str:
    """Devuelve el usuario si el token es válido; si no, ErrorAuth(401). Revisa formato, firma y expiración."""
    ahora = ahora if ahora is not None else time.time()
    try:
        payload, firma = token.split(".")
        esperada = _b64(hmac.new(_secreto(), payload.encode(), hashlib.sha256).digest())
        if not hmac.compare_digest(firma, esperada):
            raise ErrorAuth(401, "Token inválido")
        datos = json.loads(_unb64(payload))
    except ErrorAuth:
        raise
    except Exception:                                 # formato roto, base64 o JSON inválido
        raise ErrorAuth(401, "Token inválido")
    if not isinstance(datos, dict) or "sub" not in datos or "exp" not in datos:
        raise ErrorAuth(401, "Token inválido")
    if ahora >= datos["exp"]:
        raise ErrorAuth(401, "Token expirado; vuelve a iniciar sesión")
    return datos["sub"]


_HASH_FALSO = hash_contrasena("usuario-que-no-existe", b"0" * 16)


@dataclass
class Autenticador:
    ruta_db: str = ":memory:"

    def __post_init__(self):
        self.db = sqlite3.connect(self.ruta_db, check_same_thread=False)
        self.db.execute("CREATE TABLE IF NOT EXISTS usuarios (email TEXT PRIMARY KEY, hash TEXT NOT NULL)")
        # Bitácora de intentos: correo, hora y resultado. NUNCA la contraseña.
        self.db.execute("CREATE TABLE IF NOT EXISTS intentos (email TEXT, ts REAL, ok INTEGER)")

    def registrar(self, email: str, contrasena: str) -> None:
        email = email.strip().lower()
        if not EMAIL.match(email):
            raise ErrorAuth(422, "Correo inválido")
        if len(contrasena) < 8:
            raise ErrorAuth(422, "La contraseña debe tener al menos 8 caracteres")
        try:
            with self.db:
                self.db.execute("INSERT INTO usuarios VALUES (?, ?)", (email, hash_contrasena(contrasena)))
        except sqlite3.IntegrityError:
            raise ErrorAuth(409, "El correo ya está registrado")

    def login(self, email: str, contrasena: str, ahora: float | None = None) -> str:
        email, ahora = email.strip().lower(), ahora or time.time()
        # 1) Bloqueo: fallos de este correo en los últimos 15 minutos
        fallos = self.db.execute("SELECT COUNT(*) FROM intentos WHERE email = ? AND ok = 0 AND ts > ?",
                                 (email, ahora - VENTANA_FALLOS_S)).fetchone()[0]
        if fallos >= MAX_FALLOS:
            raise ErrorAuth(429, "Demasiados intentos fallidos; espera 15 minutos")
        # 2) Verificar. Si el usuario no existe se compara contra un hash falso para tardar lo mismo.
        fila = self.db.execute("SELECT hash FROM usuarios WHERE email = ?", (email,)).fetchone()
        ok = verificar_contrasena(contrasena, fila[0] if fila else _HASH_FALSO)
        ok = ok and fila is not None
        # 3) Bitácora: correo, hora y resultado. NUNCA la contraseña.
        with self.db:
            self.db.execute("INSERT INTO intentos VALUES (?, ?, ?)", (email, ahora, int(ok)))
        if not ok:
            raise ErrorAuth(401, MENSAJE_CREDENCIALES)  # mismo mensaje exista o no el usuario
        return emitir_token(email, ahora)
