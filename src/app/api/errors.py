from __future__ import annotations

from typing import Any

from app.core.errors import AppError


def error_response(err: AppError) -> dict[str, Any]:
    # Matches your standard schema
    return {"error": err.to_dict()}
