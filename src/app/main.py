from __future__ import annotations

import logging

from app.api.health import health
from app.core.logging import setup_logging

log = logging.getLogger(__name__)


def main() -> None:
    setup_logging()
    log.info("app_start")
    log.info("healthcheck", extra={"request_id": "local-dev"})
    print(health())


if __name__ == "__main__":
    main()
