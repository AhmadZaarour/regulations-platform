from __future__ import annotations

import logging

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from slowapi.errors import RateLimitExceeded
from slowapi.extension import _rate_limit_exceeded_handler
from starlette.responses import Response

from app.api.health import health
from app.api.v1.router import api_router
from app.core.logging import setup_logging
from app.core.rate_limit import limiter
from app.middleware.request_id import RequestIdMiddleware
from app.middleware.request_logging import RequestLoggingMiddleware

# Import models so Base knows them
from app.models import user  # noqa: F401

app = FastAPI(title="Regulations API")
app.state.limiter = limiter

def rate_limit_exception_handler(request: Request, exc: Exception) -> Response:
    if isinstance(exc, RateLimitExceeded):
        return _rate_limit_exceeded_handler(request, exc)
    raise exc

app.add_exception_handler(RateLimitExceeded, rate_limit_exception_handler)
app.add_middleware(RequestIdMiddleware)
app.add_middleware(RequestLoggingMiddleware)
app.include_router(api_router, prefix="/api/v1")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

log = logging.getLogger(__name__)


def main() -> None:
    setup_logging()
    log.info("app_start")
    log.info("healthcheck", extra={"request_id": "local-dev"})
    print(health())


if __name__ == "__main__":
    main()
