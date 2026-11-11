from datetime import timedelta

from sqlalchemy import select, update

from app.core.db import get_sessionmaker
from app.models import AuditLog, EmailDelivery, User, UserActionToken, UserSession
from app.models.base import utcnow
from tests.conftest import STRONG_PASSWORD, csrf, login, register


def _actions() -> list[str]:
    with get_sessionmaker()() as db:
        return [a.action for a in db.scalars(select(AuditLog).order_by(AuditLog.id)).all()]


def test_register_creates_applicant_session_and_sends_verification(client, mailbox):
    r = register(client)
    assert r.status_code == 201, r.text
    body = r.json()
    assert body["user"]["role"]["code"] == "APPLICANT"
    assert body["user"]["email_verified"] is False
    assert body["user"]["mobile"] == "9876543210"
    assert body["email_delivery"] == "QUEUED"
    assert client.cookies.get("pn_session") and client.cookies.get("pn_csrf")
    assert mailbox.sent[-1].to == "asha@example.com"
    with get_sessionmaker()() as db:
        user = db.scalar(select(User))
        assert user.password_hash.startswith("$argon2id$")
        assert db.scalar(select(EmailDelivery)).status == "SENT"
        token_row = db.scalar(select(UserActionToken))
        assert token_row.token_hash != mailbox.last_token("asha@example.com")
    me = client.get("/api/v1/auth/me")
    assert me.status_code == 200 and me.json()["user"]["email"] == "asha@example.com"
    assert "auth.register" in _actions()


def test_register_rejects_duplicates_weak_passwords_and_bad_input(client):
    assert register(client).status_code == 201
    dup = register(client, email="ASHA@example.com")
    assert dup.status_code == 409 and dup.json()["error"]["code"] == "EMAIL_ALREADY_REGISTERED"
    weak = register(client, email="b@example.com", password="short1")
    assert weak.status_code == 422 and weak.json()["error"]["code"] == "WEAK_PASSWORD"
    bad = client.post(
        "/api/v1/auth/register",
        json={
            "email": "nope",
            "password": STRONG_PASSWORD,
            "full_name": "X1",
            "mobile": "12345",
            "accept_terms": False,
        },
    )
    assert bad.status_code == 422
    fields = {d["field"] for d in bad.json()["error"]["details"]}
    assert {"email", "full_name", "mobile", "accept_terms"} <= fields


def test_email_verification_flow(client, mailbox):
    register(client)
    token = mailbox.last_token("asha@example.com")
    r = client.post("/api/v1/auth/verify-email", json={"token": token})
    assert r.status_code == 200
    assert client.get("/api/v1/auth/me").json()["user"]["email_verified"] is True
    again = client.post("/api/v1/auth/verify-email", json={"token": token})
    assert again.status_code == 400 and again.json()["error"]["code"] == "TOKEN_USED"
    bogus = client.post("/api/v1/auth/verify-email", json={"token": "x" * 40})
    assert bogus.json()["error"]["code"] == "TOKEN_INVALID"


def test_resend_verification_invalidates_previous_link(client, mailbox):
    register(client)
    first = mailbox.last_token("asha@example.com")
    r = client.post("/api/v1/auth/resend-verification", headers=csrf(client))
    assert r.status_code == 200, r.text
    second = mailbox.last_token("asha@example.com")
    assert first != second
    assert client.post("/api/v1/auth/verify-email", json={"token": first}).json()["error"]["code"] == "TOKEN_USED"
    assert client.post("/api/v1/auth/verify-email", json={"token": second}).status_code == 200


def test_login_logout_and_generic_errors(make_client):
    a = make_client()
    register(a)
    b = make_client()
    assert login(b, "asha@example.com", "wrong-password1").json()["error"]["code"] == "INVALID_CREDENTIALS"
    assert login(b, "nobody@example.com").json()["error"]["code"] == "INVALID_CREDENTIALS"
    ok = login(b, "Asha@Example.com")
    assert ok.status_code == 200 and ok.json()["permissions"]
    assert b.post("/api/v1/auth/logout", headers=csrf(b)).status_code == 200
    assert b.get("/api/v1/auth/me").status_code == 401


def test_account_lockout_after_repeated_failures(make_client):
    c = make_client()
    register(c)
    for _ in range(5):
        assert login(c, "asha@example.com", "wrong-password1").status_code == 401
    locked = login(c, "asha@example.com")
    assert locked.status_code == 423 and locked.json()["error"]["code"] == "ACCOUNT_LOCKED"
    assert "auth.account_locked" in _actions()
    with get_sessionmaker()() as db:
        db.execute(update(User).values(locked_until=utcnow() - timedelta(seconds=1)))
        db.commit()
    assert login(c, "asha@example.com").status_code == 200


def test_protected_endpoints_require_authentication(client):
    for method, path in [
        ("get", "/api/v1/auth/me"),
        ("get", "/api/v1/auth/sessions"),
        ("get", "/api/v1/admin/users"),
        ("patch", "/api/v1/account/profile"),
    ]:
        r = getattr(client, method)(path)
        assert r.status_code == 401, path
        assert r.json()["error"]["code"] == "NOT_AUTHENTICATED"


def test_csrf_required_for_state_changes(client):
    register(client)
    r = client.post("/api/v1/auth/logout")
    assert r.status_code == 403 and r.json()["error"]["code"] == "CSRF_FAILED"
    r = client.post("/api/v1/auth/logout", headers={"X-CSRF-Token": "forged"})
    assert r.status_code == 403
    r = client.post("/api/v1/auth/logout", headers={**csrf(client), "Origin": "https://evil.example"})
    assert r.status_code == 403 and r.json()["error"]["code"] == "ORIGIN_REJECTED"
    assert "security.csrf_rejected" in _actions()


def test_expired_and_idle_sessions_rejected(client):
    register(client)
    with get_sessionmaker()() as db:
        db.execute(update(UserSession).values(last_seen_at=utcnow() - timedelta(hours=5)))
        db.commit()
    r = client.get("/api/v1/auth/me")
    assert r.status_code == 401 and r.json()["error"]["code"] == "SESSION_EXPIRED"


def test_password_reset_flow_revokes_sessions(make_client, mailbox):
    a = make_client()
    register(a)
    b = make_client()
    r = b.post("/api/v1/auth/forgot-password", json={"email": "asha@example.com"})
    assert r.status_code == 202
    unknown = b.post("/api/v1/auth/forgot-password", json={"email": "ghost@example.com"})
    assert unknown.status_code == 202 and unknown.json() == r.json()
    token = mailbox.last_token("asha@example.com")
    assert b.post("/api/v1/auth/check-token", json={"token": token}).json()["purpose"] == "PASSWORD_RESET"
    weak = b.post("/api/v1/auth/reset-password", json={"token": token, "password": "weak"})
    assert weak.json()["error"]["code"] == "WEAK_PASSWORD"
    new_pw = "BrandNewPass2027"
    assert b.post("/api/v1/auth/reset-password", json={"token": token, "password": new_pw}).status_code == 200
    assert a.get("/api/v1/auth/me").status_code == 401
    assert login(b, "asha@example.com").status_code == 401
    assert login(b, "asha@example.com", new_pw).status_code == 200
    assert (
        b.post("/api/v1/auth/reset-password", json={"token": token, "password": new_pw}).json()["error"]["code"]
        == "TOKEN_USED"
    )


def test_expired_reset_token(client, mailbox):
    register(client)
    client.post("/api/v1/auth/forgot-password", json={"email": "asha@example.com"})
    token = mailbox.last_token("asha@example.com")
    with get_sessionmaker()() as db:
        db.execute(update(UserActionToken).values(expires_at=utcnow() - timedelta(minutes=1)))
        db.commit()
    r = client.post("/api/v1/auth/reset-password", json={"token": token, "password": "BrandNewPass2027"})
    assert r.json()["error"]["code"] == "TOKEN_EXPIRED"


def test_change_password_and_session_management(make_client, mailbox):
    a = make_client()
    register(a)
    b = make_client()
    login(b, "asha@example.com")
    sessions = a.get("/api/v1/auth/sessions").json()
    assert len(sessions) == 2 and sum(s["current"] for s in sessions) == 1
    wrong = a.post(
        "/api/v1/auth/change-password",
        headers=csrf(a),
        json={"current_password": "nope-nope1", "new_password": "AnotherPass2028"},
    )
    assert wrong.json()["error"]["code"] == "INVALID_CURRENT_PASSWORD"
    ok = a.post(
        "/api/v1/auth/change-password",
        headers=csrf(a),
        json={"current_password": STRONG_PASSWORD, "new_password": "AnotherPass2028"},
    )
    assert ok.status_code == 200
    assert a.get("/api/v1/auth/me").status_code == 200
    assert b.get("/api/v1/auth/me").status_code == 401


def test_cannot_revoke_another_users_session(make_client):
    a = make_client()
    register(a)
    b = make_client()
    register(b, email="ravi@example.com", name="Ravi Kumar")
    b_session = b.get("/api/v1/auth/sessions").json()[0]["id"]
    r = a.delete(f"/api/v1/auth/sessions/{b_session}", headers=csrf(a))
    assert r.status_code == 403
    assert b.get("/api/v1/auth/me").status_code == 200


def test_profile_update(client):
    register(client)
    r = client.patch("/api/v1/account/profile", headers=csrf(client), json={"full_name": "Asha  K Verma", "mobile": ""})
    assert r.status_code == 200
    assert r.json()["full_name"] == "Asha K Verma" and r.json()["mobile"] is None
