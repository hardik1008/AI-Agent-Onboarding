from datetime import datetime, timezone

import pytest
from sqlalchemy import select

from app.core.config import get_settings
from app.core.db import get_sessionmaker
from app.models import AuditLog
from app.services.rate_limit import hit
from tests.conftest import login, register


@pytest.fixture
def tight_limits(monkeypatch):
    s = get_settings()
    monkeypatch.setattr(s, "rate_limit_login", 3)
    monkeypatch.setattr(s, "rate_limit_password_reset", 2)
    monkeypatch.setattr(s, "rate_limit_register", 1)
    return s


def _rate_limited_audits() -> list[AuditLog]:
    with get_sessionmaker()() as db:
        return list(db.scalars(select(AuditLog).where(AuditLog.action == "security.rate_limited")).all())


def test_login_rate_limited_per_ip_even_for_valid_credentials(make_client, tight_limits):
    c = make_client()
    assert register(c, email="ravi@example.com", name="Ravi Kumar").status_code == 201
    for _ in range(2):
        assert login(c, "ravi@example.com", "wrong-password-1").status_code == 401
    assert login(c, "ravi@example.com").status_code == 200
    blocked = login(c, "ravi@example.com")
    assert blocked.status_code == 429
    assert blocked.json()["error"]["code"] == "RATE_LIMITED"
    assert 0 < int(blocked.headers["Retry-After"]) <= tight_limits.rate_limit_window_seconds
    assert login(c, "ravi@example.com").status_code == 429
    audits = _rate_limited_audits()
    assert len(audits) == 1
    assert audits[0].outcome == "DENIED" and audits[0].details == {"scope": "login", "limit": 3}


def test_scopes_are_counted_independently(make_client, tight_limits):
    c = make_client()
    for _ in range(2):
        assert c.post("/api/v1/auth/forgot-password", json={"email": "nobody@example.com"}).status_code == 202
    assert c.post("/api/v1/auth/forgot-password", json={"email": "nobody@example.com"}).status_code == 429
    assert register(c, email="meera@example.com", name="Meera Shah").status_code == 201
    assert register(c, email="arjun@example.com", name="Arjun Rao").status_code == 429
    assert login(c, "meera@example.com").status_code == 200


def test_rate_limit_can_be_disabled(make_client, tight_limits, monkeypatch):
    monkeypatch.setattr(tight_limits, "rate_limit_enabled", False)
    c = make_client()
    for _ in range(5):
        assert c.post("/api/v1/auth/forgot-password", json={"email": "nobody@example.com"}).status_code == 202


def test_fixed_window_resets():
    t0 = datetime(2026, 11, 11, 10, 0, 5, tzinfo=timezone.utc)
    assert hit("unit", 2, 60, now=t0) == (1, 55)
    assert hit("unit", 2, 60, now=t0.replace(second=59)) == (2, 1)
    assert hit("unit", 2, 60, now=t0.replace(minute=1, second=0)) == (1, 60)


@pytest.mark.parametrize("field", ["RATE_LIMIT_WINDOW_SECONDS", "RATE_LIMIT_LOGIN", "RATE_LIMIT_TOKEN"])
def test_non_positive_rate_limit_settings_are_rejected(monkeypatch, field):
    from pydantic import ValidationError

    from app.core.config import Settings

    monkeypatch.setenv(field, "0")
    with pytest.raises(ValidationError):
        Settings()
