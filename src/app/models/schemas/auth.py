from __future__ import annotations

from pydantic import BaseModel, EmailStr, Field

# ---------------------------
# Register
# ---------------------------


class RegisterRequest(BaseModel):
    email: EmailStr
    password: str = Field(min_length=8, max_length=128)


class RegisterResponse(BaseModel):
    id: int
    email: EmailStr
    is_active: bool
    is_superuser: bool


# ---------------------------
# Login
# ---------------------------


class LoginRequest(BaseModel):
    email: EmailStr
    password: str


# ---------------------------
# Token Responses
# ---------------------------


class TokenResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"


class AccessTokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"


# ---------------------------
# Refresh
# ---------------------------


class RefreshRequest(BaseModel):
    refresh_token: str


# ---------------------------
# Generic Message
# ---------------------------


class MessageResponse(BaseModel):
    message: str
