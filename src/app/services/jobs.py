from __future__ import annotations

from datetime import UTC, datetime

from sqlalchemy.orm import Session

from app.db.session import SessionLocal
from app.logic.engine import run_egress_stair_engine
from app.models.regulation_run import RegulationRun


def execute_regulation_run(run_id: int) -> None:
    db: Session = SessionLocal()

    try:
        run = db.get(RegulationRun, run_id)
        if run is None:
            return

        run.status = "running"
        run.started_at = datetime.now(UTC)
        db.commit()

        result = run_egress_stair_engine(run.input_data)

        run.result = result
        run.status = "succeeded"
        run.finished_at = datetime.now(UTC)
        db.commit()

    except Exception as exc:
        run = db.get(RegulationRun, run_id)
        if run is not None:
            run.status = "failed"
            run.error_message = str(exc)
            run.finished_at = datetime.now(UTC)
            db.commit()
        raise

    finally:
        db.close()
