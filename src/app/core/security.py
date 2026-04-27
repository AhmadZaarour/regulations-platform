from __future__ import annotations

from datetime import UTC, datetime, timedelta
from typing import Any, cast

from jose import JWTError, jwt
from passlib.context import CryptContext

from app.core.config import settings

ALGORITHM = "HS256"

pwd_context = CryptContext(schemes=["argon2"], deprecated="auto")


def hash_password(password: str) -> str:
    return cast(str, pwd_context.hash(password))


def verify_password(plain: str, hashed: str) -> bool:
    return cast(bool, pwd_context.verify(plain, hashed))


def create_access_token(data: dict[str, Any], expires_minutes: int = 30) -> str:
    to_encode = data.copy()
    expire = datetime.now(UTC) + timedelta(minutes=expires_minutes)
    to_encode.update({"exp": expire})
    return cast(str, jwt.encode(to_encode, settings.secret_key, algorithm=ALGORITHM))


def decode_access_token(token: str) -> dict[str, Any]:
    try:
        payload = jwt.decode(token, settings.secret_key, algorithms=[ALGORITHM])
        return cast(dict[str, Any], payload)
    except JWTError as exc:
        raise ValueError("Invalid token") from exc
