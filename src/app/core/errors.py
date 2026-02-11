from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True)
class AppError(Exception):
    error_code: str
    message: str
    details: dict[str, Any] | None = None

    def to_dict(self) -> dict[str, Any]:
        return {
            "error_code": self.error_code,
            "message": self.message,
            "details": self.details or {},
        }


class ValidationError(AppError):
    pass


class NotFoundError(AppError):
    pass


class UnauthorizedError(AppError):
    pass
