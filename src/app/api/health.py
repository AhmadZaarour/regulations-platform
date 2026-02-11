from __future__ import annotations

from app.core.config import settings


def health() -> dict[str, str]:
    return {"status": "ok", "app": settings.app_name, "env": settings.env}
