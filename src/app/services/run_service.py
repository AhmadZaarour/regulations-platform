from __future__ import annotations

from typing import Any, cast

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
