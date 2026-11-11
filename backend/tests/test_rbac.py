import uuid

from sqlalchemy import select

from app.core.db import get_sessionmaker
from app.models import AuditLog
from app.rbac.catalog import ROLE_PERMISSIONS, RoleCode
from app.rbac.policy import Resource, Subject, evaluate
from tests.conftest import create_staff, csrf, login, register


def _subject(role: RoleCode, region=None, clearance=1, uid=None) -> Subject:
    return Subject(
        id=uid or uuid.uuid4(),
        role=role.value,
        permissions=frozenset(ROLE_PERMISSIONS[role]),
        region=region,
        clearance_level=clearance,
    )


def test_policy_ownership_region_clearance_and_self_admin():
    applicant = _subject(RoleCode.APPLICANT)
    own = Resource(type="application", owner_id=applicant.id)
    other = Resource(type="application", owner_id=uuid.uuid4())
    assert evaluate(applicant, "application:read_own", own).allowed
    assert evaluate(applicant, "application:read_own", other).rule == "OWNERSHIP"
    assert evaluate(applicant, "application:read_any", own).rule == "RBAC"

    north = _subject(RoleCode.REVIEWER, region="NORTH")
    assert evaluate(north, "application:review", Resource(type="application", region="NORTH")).allowed
    assert evaluate(north, "application:review", Resource(type="application", region="SOUTH")).rule == "REGION"
    assert evaluate(
        _subject(RoleCode.REVIEWER, region="ALL"), "application:review", Resource(type="application", region="SOUTH")
    ).allowed
    assert (
        evaluate(north, "application:review", Resource(type="application", region="NORTH", sensitivity=3)).rule
        == "CLEARANCE"
    )
    assert evaluate(_subject(RoleCode.REVIEWER), "application:decide", Resource(type="application")).allowed
    assert not evaluate(
        _subject(RoleCode.REVIEWER), "application:decide_escalated", Resource(type="application")
    ).allowed
    assert not evaluate(
        _subject(RoleCode.ADMIN, clearance=3), "application:decide", Resource(type="application")
    ).allowed

    admin = _subject(RoleCode.ADMIN, clearance=3)
    me = Resource(type="user", id=str(admin.id), attributes={"change": "role"})
    assert evaluate(admin, "users:manage", me).rule == "NO_SELF_ADMINISTRATION"


def _admin_client(make_client):
    create_staff("ADMIN", "admin@policynest.in", "Platform Admin", region="ALL", clearance=3)
    c = make_client()
    assert login(c, "admin@policynest.in").status_code == 200
    return c


def test_applicant_and_reviewer_denied_admin_endpoints(make_client):
    applicant = make_client()
    register(applicant)
    create_staff("REVIEWER", "rev@policynest.in", "Rita Reviewer", region="NORTH")
    reviewer = make_client()
    login(reviewer, "rev@policynest.in")
    for c in (applicant, reviewer):
        for path in [
            "/api/v1/admin/users",
            "/api/v1/admin/audit-logs",
            "/api/v1/admin/roles",
            "/api/v1/admin/system/health",
        ]:
            r = c.get(path)
            assert r.status_code == 403 and r.json()["error"]["code"] == "FORBIDDEN", path
        r = c.post(
            "/api/v1/admin/users", headers=csrf(c), json={"email": "x@y.com", "full_name": "X Y", "role": "ADMIN"}
        )
        assert r.status_code == 403
    with get_sessionmaker()() as db:
        denials = db.scalars(select(AuditLog).where(AuditLog.action == "access.denied")).all()
    assert len(denials) >= 10


def test_unverified_applicant_blocked_from_non_profile_permissions(client, mailbox):
    from fastapi import Depends

    from app.api.deps import require_permission

    register(client)
    app = client.app

    @app.get("/api/v1/_probe")
    def probe(_=Depends(require_permission("application:create"))):
        return {"ok": True}

    r = client.get("/api/v1/_probe")
    assert r.status_code == 403 and r.json()["error"]["code"] == "EMAIL_NOT_VERIFIED"
    client.post("/api/v1/auth/verify-email", json={"token": mailbox.last_token("asha@example.com")})
    assert client.get("/api/v1/_probe").json() == {"ok": True}


def test_admin_invites_staff_who_sets_password(make_client, mailbox):
    admin = _admin_client(make_client)
    r = admin.post(
        "/api/v1/admin/users",
        headers=csrf(admin),
        json={
            "email": "Senior@PolicyNest.in",
            "full_name": "Sunil Senior",
            "role": "SENIOR_REVIEWER",
            "region": "WEST",
            "clearance_level": 2,
        },
    )
    assert r.status_code == 201, r.text
    assert r.json()["invitation_pending"] is True
    invited = make_client()
    assert login(invited, "senior@policynest.in").status_code == 401
    token = mailbox.last_token("senior@policynest.in")
    assert invited.post("/api/v1/auth/check-token", json={"token": token}).json()["purpose"] == "INVITE"
    assert f"/reset-password?token={token}" in mailbox.sent[-1].text
    assert (
        invited.post(
            "/api/v1/auth/reset-password", json={"token": token, "password": "Escalation#Desk2026"}
        ).status_code
        == 200
    )
    me = login(invited, "senior@policynest.in", "Escalation#Desk2026").json()
    assert me["user"]["role"]["code"] == "SENIOR_REVIEWER" and me["user"]["email_verified"]
    assert "fraud:review" in me["permissions"] and "users:manage" not in me["permissions"]


def test_admin_role_change_deactivation_and_guards(make_client):
    admin = _admin_client(make_client)
    applicant = make_client()
    uid = register(applicant).json()["user"]["id"]
    r = admin.patch(f"/api/v1/admin/users/{uid}", headers=csrf(admin), json={"role": "REVIEWER", "region": "SOUTH"})
    assert r.status_code == 200 and r.json()["role"]["code"] == "REVIEWER"
    assert applicant.get("/api/v1/auth/me").status_code == 401  # role change revokes sessions
    login(applicant, "asha@example.com")
    assert admin.patch(f"/api/v1/admin/users/{uid}", headers=csrf(admin), json={"is_active": False}).status_code == 200
    assert applicant.get("/api/v1/auth/me").status_code == 401
    assert login(applicant, "asha@example.com").json()["error"]["code"] == "ACCOUNT_DISABLED"

    admin_id = admin.get("/api/v1/auth/me").json()["user"]["id"]
    self_change = admin.patch(f"/api/v1/admin/users/{admin_id}", headers=csrf(admin), json={"role": "REVIEWER"})
    assert self_change.status_code == 403
    other_admin = create_staff("ADMIN", "admin2@policynest.in", "Second Admin", clearance=3)
    assert (
        admin.patch(f"/api/v1/admin/users/{other_admin}", headers=csrf(admin), json={"is_active": False}).status_code
        == 200
    )


def test_last_admin_cannot_be_removed(make_client):
    admin = _admin_client(make_client)
    second = create_staff("ADMIN", "admin2@policynest.in", "Second Admin", clearance=3)
    c2 = make_client()
    login(c2, "admin2@policynest.in")
    first_id = admin.get("/api/v1/auth/me").json()["user"]["id"]
    assert c2.patch(f"/api/v1/admin/users/{first_id}", headers=csrf(c2), json={"is_active": False}).status_code == 200
    r = c2.patch(f"/api/v1/admin/users/{second}", headers=csrf(c2), json={"is_active": False})
    assert r.status_code == 403  # self-administration blocked first


def test_admin_lists_filters_users_audit_roles_and_health(make_client):
    admin = _admin_client(make_client)
    applicant = make_client()
    register(applicant)
    users = admin.get("/api/v1/admin/users", params={"role": "APPLICANT"}).json()
    assert users["total"] == 1 and users["items"][0]["email"] == "asha@example.com"
    assert admin.get("/api/v1/admin/users", params={"status": "unverified"}).json()["total"] == 1
    assert admin.get("/api/v1/admin/users", params={"q": "nomatch"}).json()["total"] == 0
    logs = admin.get("/api/v1/admin/audit-logs", params={"action": "auth."}).json()
    assert logs["total"] >= 2 and all(i["action"].startswith("auth.") for i in logs["items"])
    roles = admin.get("/api/v1/admin/roles").json()
    assert {r["code"] for r in roles["roles"]} == {"APPLICANT", "REVIEWER", "SENIOR_REVIEWER", "ADMIN"}
    health = admin.get("/api/v1/admin/system/health").json()
    assert health["status"] == "healthy"
    statuses = {i["key"]: i["status"] for i in health["integrations"]}
    assert statuses["pan_verification"] == "NOT_CONFIGURED"
    stats = admin.get("/api/v1/admin/stats").json()
    assert stats["users_by_role"]["APPLICANT"] == 1 and stats["unverified_users"] == 1
