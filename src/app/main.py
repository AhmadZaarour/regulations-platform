from __future__ import annotations

import logging

from fastapi import FastAPI

from app.api.health import health
from app.api.v1.router import api_router
from app.core.logging import setup_logging

# Import models so Base knows them
from app.models import user  # noqa: F401

app = FastAPI(title="Regulations API")

app.include_router(api_router, prefix="/api/v1")


log = logging.getLogger(__name__)


def main() -> None:
    setup_logging()
    log.info("app_start")
    log.info("healthcheck", extra={"request_id": "local-dev"})
    print(health())


if __name__ == "__main__":
    main()
