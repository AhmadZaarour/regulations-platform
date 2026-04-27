from __future__ import annotations

from typing import Any

from sqlalchemy.orm import Session

from app.models.audit_log import AuditLog


def create_audit_log(
    db: Session,
    *,
    action: str,
    entity_type: str,
    actor_user_id: int | None = None,
    entity_id: str | None = None,
    request_id: str | None = None,
    metadata_json: dict[str, Any] | None = None,
) -> AuditLog:
    audit_log = AuditLog(
        actor_user_id=actor_user_id,
        action=action,
        entity_type=entity_type,
        entity_id=entity_id,
        request_id=request_id,
        metadata_json=metadata_json,
    )
    db.add(audit_log)
    db.commit()
    db.refresh(audit_log)
    return audit_log
