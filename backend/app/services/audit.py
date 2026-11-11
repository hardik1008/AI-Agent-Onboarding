from typing import Any

from fastapi import Request
from sqlalchemy.orm import Session

from app.core.db import get_sessionmaker
from app.core.request_context import client_ip, request_id, user_agent
from app.models import AuditLog, User

SUCCESS = "SUCCESS"
FAILURE = "FAILURE"
DENIED = "DENIED"


def _build(
    request: Request | None,
    action: str,
    outcome: str,
    actor: User | None,
    resource_type: str | None,
    resource_id: str | None,
    details: dict[str, Any] | None,
    actor_email: str | None,
) -> AuditLog:
    return AuditLog(
        actor_user_id=actor.id if actor else None,
        actor_email=actor.email if actor else actor_email,
        actor_role=actor.role.code if actor else None,
        action=action,
        outcome=outcome,
        resource_type=resource_type,
        resource_id=resource_id,
        ip_address=client_ip(request) if request else None,
        user_agent=user_agent(request) if request else None,
        request_id=request_id(request) if request else None,
        details=details or {},
    )


def add(
    db: Session,
    request: Request | None,
    action: str,
    outcome: str = SUCCESS,
    *,
    actor: User | None = None,
    resource_type: str | None = None,
    resource_id: str | None = None,
    details: dict[str, Any] | None = None,
    actor_email: str | None = None,
) -> None:
    """Record within the caller's transaction so the audit entry commits atomically with the change."""
    db.add(_build(request, action, outcome, actor, resource_type, resource_id, details, actor_email))


def record_independent(
    request: Request | None,
    action: str,
    outcome: str,
    *,
    actor: User | None = None,
    resource_type: str | None = None,
    resource_id: str | None = None,
    details: dict[str, Any] | None = None,
    actor_email: str | None = None,
) -> None:
    """Record in a separate transaction; used for failures/denials whose request transaction rolls back."""
    with get_sessionmaker()() as db:
        db.add(_build(request, action, outcome, actor, resource_type, resource_id, details, actor_email))
        db.commit()
