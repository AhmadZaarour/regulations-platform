from __future__ import annotations

from datetime import UTC, datetime, timedelta
from typing import Any

from jose import JWTError, jwt
from passlib.context import CryptContext

from app.core.config import settings

_pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password: str) -> Any:
    return _pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> Any:
    return _pwd_context.verify(plain_password, hashed_password)


def _create_token(*, subject: str, token_type: str, expires_delta: timedelta) -> Any:
    now = datetime.now(UTC)
    payload: dict[str, Any] = {
        "sub": subject,
        "type": token_type,  # "access" or "refresh"
        "iat": int(now.timestamp()),
        "exp": int((now + expires_delta).timestamp()),
    }
    return jwt.encode(payload, settings.secret_key, algorithm=settings.jwt_algorithm)


def create_access_token(subject: str) -> Any:
    return _create_token(
        subject=subject,
        token_type="access",
        expires_delta=timedelta(minutes=settings.access_token_exp_minutes),
    )


def create_refresh_token(subject: str) -> Any:
    return _create_token(
        subject=subject,
        token_type="refresh",
        expires_delta=timedelta(days=settings.refresh_token_exp_days),
    )


def decode_token(token: str) -> Any:
    """
    Returns the decoded payload or raises ValueError for invalid tokens.
    """
    try:
        payload = jwt.decode(token, settings.secret_key, algorithms=[settings.jwt_algorithm])
        # minimal validation
        if "sub" not in payload or "type" not in payload:
            raise ValueError("Invalid token payload")
        return payload
    except JWTError as e:
        raise ValueError("Invalid token") from e
