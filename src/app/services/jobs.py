from __future__ import annotations

import logging
from datetime import UTC, datetime

from sqlalchemy.orm import Session

from app.db.session import SessionLocal
from app.logic.engine import run_egress_stair_engine
from app.models.regulation_run import RegulationRun

log = logging.getLogger("app.worker")


def execute_regulation_run(run_id: int) -> None:
    db: Session = SessionLocal()

    try:
        run = db.get(RegulationRun, run_id)
        if run is None:
            return

        run.status = "running"
        log.info("run_started", extra={"run_id": run_id})
        run.started_at = datetime.now(UTC)
        db.commit()

        result = run_egress_stair_engine(run.input_data)

        run.result = result
        run.status = "succeeded"
        run.finished_at = datetime.now(UTC)
        db.commit()
        log.info("run_succeeded", extra={"run_id": run_id})

    except Exception as exc:
        run = db.get(RegulationRun, run_id)
        if run is not None:
            log.exception("run_failed", extra={"run_id": run_id})
            run.status = "failed"
            run.error_message = str(exc)
            run.finished_at = datetime.now(UTC)
            db.commit()
        raise

    finally:
        db.close()
