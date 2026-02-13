from __future__ import annotations

from collections.abc import Generator

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from app.core.security import decode_token
from app.db.session import SessionLocal  # Week 3 will make this real
from app.models.user import User  # your model

# from app.services.user_service import get_user_by_id  # if you have it later


# Swagger "Authorize" button will appear with this
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")


def get_db() -> Generator[Session, None, None]:
    """
    DB session dependency.
    Week 3: you’ll implement SessionLocal + proper engine teardown.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def _unauthorized(detail: str = "Not authenticated") -> HTTPException:
    return HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail=detail,
        headers={"WWW-Authenticate": "Bearer"},
    )


def get_current_user(token: str = Depends(oauth2_scheme), db: object = Depends(get_db)) -> User:
    """
    Validates JWT access token and returns the user object.

    Token payload format expected from security.py:
      - sub: user_id (string)
      - type: "access" or "refresh"
    """
    try:
        payload = decode_token(token)
    except ValueError as e:
        raise _unauthorized("Invalid token") from e

    if payload.get("type") != "access":
        raise _unauthorized("Invalid token type")

    user_id = payload.get("sub")
    if not user_id:
        raise _unauthorized("Invalid token subject")

    # --- Week 2 shortcut (until Week 3 DB + user service are ready) ---
    # If you already have a DB model + query, replace this block with real lookup.
    user: User | None = None

    # Example Week 3 style:
    # user = db.query(User).filter(User.id == int(user_id)).first()

    if user is None:
        # Keep 401 (not 404) to avoid leaking which users exist
        raise _unauthorized("User not found")

    return user


def require_active_user(current_user: User = Depends(get_current_user)) -> User:
    """
    Optional: blocks disabled users.
    Assumes your User model has `is_active` (add later if you want).
    """
    is_active = getattr(current_user, "is_active", True)
    if not is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Inactive user",
        )
    return current_user
