from __future__ import annotations

from redis import Redis
from rq import Worker

from app.core.config import settings

redis_conn = Redis.from_url(settings.redis_url)


def main() -> None:
    worker = Worker(["regulation_runs"], connection=redis_conn)
    worker.work()


if __name__ == "__main__":
    main()
