"""
Authentication — JWT-based user auth with SQLite user store.

When AUTH_ENABLED=false (default): all endpoints work without login (dev-user).
When AUTH_ENABLED=true: endpoints require Bearer token.

Env vars:
  AUTH_ENABLED=false
  JWT_SECRET=change-this-to-a-random-32-char-secret
  JWT_EXPIRE_HOURS=24
  AUTH_DB_PATH=users.db
"""
from __future__ import annotations

import base64
import hashlib
import hmac
import json
import os
import sqlite3
import time
import uuid
from pathlib import Path
from typing import Optional


# ── Config ────────────────────────────────────────────────────────────────────

_AUTH_ENABLED = os.getenv("AUTH_ENABLED", "false").lower() == "true"
_JWT_SECRET = os.getenv("JWT_SECRET", "change-this-to-a-random-32-char-secret")
_JWT_EXPIRE_HOURS = int(os.getenv("JWT_EXPIRE_HOURS", "24"))
_AUTH_DB_PATH = os.getenv("AUTH_DB_PATH", "users.db")


# ── Password hashing ──────────────────────────────────────────────────────────

def _hash_password(password: str, salt: str) -> str:
    """Hash password using PBKDF2-SHA256 with 260,000 iterations."""
    return hashlib.pbkdf2_hmac("sha256", password.encode(), salt.encode(), 260000).hex()


def _make_password(password: str) -> str:
    """Return 'salt:hash' string for storage."""
    salt = uuid.uuid4().hex
    hashed = _hash_password(password, salt)
    return f"{salt}:{hashed}"


def _check_password(password: str, stored: str) -> bool:
    """Verify a password against a stored 'salt:hash' string."""
    try:
        salt, stored_hash = stored.split(":", 1)
    except ValueError:
        return False
    candidate = _hash_password(password, salt)
    return hmac.compare_digest(candidate, stored_hash)


# ── JWT (manual HS256 — no external libraries) ────────────────────────────────

def _b64url_encode(data: bytes) -> str:
    """Base64url-encode bytes without padding."""
    return base64.urlsafe_b64encode(data).rstrip(b"=").decode()


def _b64url_decode(s: str) -> bytes:
    """Base64url-decode a string (adds padding as needed)."""
    padding = 4 - len(s) % 4
    if padding != 4:
        s += "=" * padding
    return base64.urlsafe_b64decode(s)


def create_access_token(user_id: str, email: str) -> str:
    """Create a signed HS256 JWT token."""
    header = {"alg": "HS256", "typ": "JWT"}
    now = int(time.time())
    payload = {
        "sub": user_id,
        "email": email,
        "iat": now,
        "exp": now + _JWT_EXPIRE_HOURS * 3600,
    }

    header_b64 = _b64url_encode(json.dumps(header, separators=(",", ":")).encode())
    payload_b64 = _b64url_encode(json.dumps(payload, separators=(",", ":")).encode())
    signing_input = f"{header_b64}.{payload_b64}"

    signature = hmac.new(
        _JWT_SECRET.encode(),
        signing_input.encode(),
        hashlib.sha256,
    ).digest()
    sig_b64 = _b64url_encode(signature)

    return f"{signing_input}.{sig_b64}"


def decode_token(token: str) -> Optional[dict]:
    """
    Verify and decode a JWT token.
    Returns the payload dict, or None if the token is invalid or expired.
    """
    try:
        parts = token.split(".")
        if len(parts) != 3:
            return None

        header_b64, payload_b64, sig_b64 = parts
        signing_input = f"{header_b64}.{payload_b64}"

        # Verify signature
        expected_sig = hmac.new(
            _JWT_SECRET.encode(),
            signing_input.encode(),
            hashlib.sha256,
        ).digest()
        actual_sig = _b64url_decode(sig_b64)

        if not hmac.compare_digest(expected_sig, actual_sig):
            return None

        # Decode payload
        payload = json.loads(_b64url_decode(payload_b64))

        # Check expiry
        if payload.get("exp", 0) < int(time.time()):
            return None

        return payload

    except Exception:
        return None


def get_current_user_id(authorization: Optional[str]) -> str:
    """
    Extract user_id from a Bearer token in the Authorization header.
    Returns 'dev-user' if AUTH_ENABLED=false or no/invalid token is provided.
    """
    if not _AUTH_ENABLED:
        return "dev-user"

    if not authorization or not authorization.startswith("Bearer "):
        return "dev-user"

    token = authorization[len("Bearer "):]
    payload = decode_token(token)
    if payload is None:
        return "dev-user"

    return payload.get("sub", "dev-user")


# ── UserDB ────────────────────────────────────────────────────────────────────

class UserDB:
    """SQLite-backed user store."""

    def __init__(self, db_path: str = _AUTH_DB_PATH):
        self.db_path = db_path
        self._lock = sqlite3.Connection
        self.conn = sqlite3.connect(self.db_path, check_same_thread=False, isolation_level=None)
        self.conn.row_factory = sqlite3.Row
        self.init_db()

    def close(self) -> None:
        """Close database connection."""
        try:
            self.conn.close()
        except Exception:
            pass

    def init_db(self) -> None:
        """Create the users table if it doesn't exist."""
        self.conn.execute(
            """
            CREATE TABLE IF NOT EXISTS users (
                user_id   TEXT PRIMARY KEY,
                email     TEXT UNIQUE NOT NULL,
                password  TEXT NOT NULL,
                created_at INTEGER NOT NULL
            )
            """
        )

    def create_user(self, email: str, password: str) -> dict:
        """Create a new user and return the user record."""
        user_id = str(uuid.uuid4())
        password_stored = _make_password(password)
        created_at = int(time.time())

        self.conn.execute(
            "INSERT INTO users (user_id, email, password, created_at) VALUES (?, ?, ?, ?)",
            (user_id, email, password_stored, created_at),
        )

        return {"user_id": user_id, "email": email, "created_at": created_at}

    def get_user(self, email: str) -> Optional[dict]:
        """Return user record by email, or None if not found."""
        row = self.conn.execute(
            "SELECT user_id, email, password, created_at FROM users WHERE email = ?",
            (email,),
        ).fetchone()
        if row is None:
            return None
        return dict(row)

    def verify_password(self, email: str, password: str) -> bool:
        """Return True if the password matches the stored hash for this email."""
        user = self.get_user(email)
        if user is None:
            return False
        return _check_password(password, user["password"])
