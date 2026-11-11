"""Attribute-based access control layered on top of role permissions.

RBAC answers "may this role perform this action at all"; these rules answer
"may this subject perform it on this specific resource".
"""

import uuid
from dataclasses import dataclass, field

from app.rbac.catalog import RoleCode


@dataclass(frozen=True)
class Subject:
    id: uuid.UUID
    role: str
    permissions: frozenset[str]
    region: str | None = None
    clearance_level: int = 1


@dataclass(frozen=True)
class Resource:
    type: str
    id: str | None = None
    owner_id: uuid.UUID | None = None
    region: str | None = None
    sensitivity: int = 1
    attributes: dict[str, object] = field(default_factory=dict)


@dataclass(frozen=True)
class Decision:
    allowed: bool
    rule: str
    reason: str


def _deny(rule: str, reason: str) -> Decision:
    return Decision(False, rule, reason)


def evaluate(subject: Subject, permission: str, resource: Resource) -> Decision:
    if permission not in subject.permissions:
        return _deny("RBAC", f"Role {subject.role} lacks permission {permission}.")

    owner_scoped = permission.endswith("_own") or subject.role == RoleCode.APPLICANT
    if owner_scoped:
        if resource.owner_id is None and permission.endswith("_own"):
            return _deny("OWNERSHIP", "Owner-scoped permission requires an owned resource.")
        if resource.owner_id is not None and resource.owner_id != subject.id:
            return _deny("OWNERSHIP", "Subject does not own this resource.")

    if subject.role in (RoleCode.REVIEWER, RoleCode.SENIOR_REVIEWER) and resource.region:
        if subject.region not in (None, "ALL") and subject.region != resource.region:
            return _deny("REGION", f"Resource region {resource.region} is outside subject jurisdiction.")

    if resource.sensitivity > subject.clearance_level:
        return _deny("CLEARANCE", "Resource sensitivity exceeds subject clearance level.")

    if resource.type == "user" and resource.id == str(subject.id):
        if resource.attributes.get("change") in {"role", "is_active"}:
            return _deny("NO_SELF_ADMINISTRATION", "Administrators cannot change their own role or status.")

    return Decision(True, "ALLOW", "All applicable rules passed.")
