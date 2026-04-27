from __future__ import annotations

from typing import cast

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.deps import get_current_user, get_db
from app.models.schemas.runs import EgressStairsInput, RunCreateResponse, RunResultResponse
from app.models.user import User
from app.services.jobs import execute_regulation_run
from app.services.queue import runs_queue
from app.services.run_service import attach_job_id, create_regulation_run, get_regulation_run

router = APIRouter()


@router.post("", response_model=RunCreateResponse)  # type: ignore[misc]
def create_run(
    payload: EgressStairsInput,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> RunCreateResponse:
    run = create_regulation_run(
        db,
        user_id=current_user.id,
        project_type="egress_stairs_residential",
        input_data=payload.model_dump(),
    )

    job = runs_queue.enqueue(execute_regulation_run, run.id)
    run = attach_job_id(db, run=run, job_id=job.id)

    return RunCreateResponse(
        run_id=run.id,
        job_id=cast(str, run.rq_job_id),
        status=run.status,
    )


@router.get("/{run_id}", response_model=RunResultResponse)  # type: ignore[misc]
def read_run(
    run_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> RunResultResponse:
    run = get_regulation_run(db, run_id)

    if run is None or run.user_id != current_user.id:
        raise HTTPException(status_code=404, detail="Run not found")

    return RunResultResponse(
        id=run.id,
        status=run.status,
        project_type=run.project_type,
        input_data=dict(run.input_data),
        result=dict(run.result) if run.result is not None else None,
        error_message=run.error_message,
        rq_job_id=run.rq_job_id,
        created_at=run.created_at.isoformat() if run.created_at else None,
        started_at=run.started_at.isoformat() if run.started_at else None,
        finished_at=run.finished_at.isoformat() if run.finished_at else None,
    )
