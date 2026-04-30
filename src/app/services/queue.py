from __future__ import annotations

from redis import Redis
from rq import Queue
from rq.job import Job

from app.core.config import settings

from .jobs import execute_regulation_run

redis_conn = Redis.from_url(settings.redis_url)
runs_queue = Queue("regulation_runs", connection=redis_conn, default_timeout=300)


def enqueue_run(run_id: int) -> Job:
    redis_conn = Redis.from_url(settings.redis_url)
    queue = Queue("default", connection=redis_conn)

    job = queue.enqueue(
        execute_regulation_run,
        run_id,
        job_timeout=300,
        result_ttl=86400,
        failure_ttl=86400,
    )

    return job
