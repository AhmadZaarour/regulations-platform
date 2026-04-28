from __future__ import annotations

from fastapi import APIRouter
from sqlalchemy import text

from app.db.session import SessionLocal
from app.services.queue import redis_conn, runs_queue

router = APIRouter()


@router.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@router.get("/health/deep")
def deep_health() -> dict[str, str | int]:
    db = SessionLocal()
    try:
        db.execute(text("select 1"))
        redis_conn.ping()

        return {
            "status": "ok",
            "db": "ok",
            "redis": "ok",
            "queue_name": runs_queue.name,
            "queued_jobs": runs_queue.count,
        }
    finally:
        db.close()
