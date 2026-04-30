from __future__ import annotations

from typing import Any, cast

from sqlalchemy import desc
from sqlalchemy.orm import Session

from app.models.regulation_run import RegulationRun


def create_regulation_run(
    db: Session,
    *,
    user_id: int,
    project_type: str,
    input_data: dict[str, Any],
) -> RegulationRun:
    run = RegulationRun(
        user_id=user_id,
        project_type=project_type,
        input_data=input_data,
        status="queued",
    )
    db.add(run)
    db.commit()
    db.refresh(run)
    return run


def attach_job_id(db: Session, *, run: RegulationRun, job_id: str) -> RegulationRun:
    run.rq_job_id = job_id
    db.commit()
    db.refresh(run)
    return run


def get_regulation_run(db: Session, run_id: int) -> RegulationRun | None:
    return cast(RegulationRun | None, db.get(RegulationRun, run_id))


def list_user_runs(db: Session, *, user_id: int, limit: int = 20) -> list[RegulationRun]:
    return list(
        db.query(RegulationRun)
        .filter(RegulationRun.user_id == user_id)
        .order_by(desc(RegulationRun.created_at))
        .limit(limit)
        .all()
    )


def get_run_for_user(db: Session, run_id: int, user_id: int) -> RegulationRun | None:  # type: ignore[reduntant-cast]
    return cast(
        RegulationRun | None,
        db.query(RegulationRun)
        .filter(RegulationRun.id == run_id, RegulationRun.user_id == user_id)
        .first(),
    )
