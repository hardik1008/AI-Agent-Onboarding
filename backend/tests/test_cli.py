import pytest
from sqlalchemy import select

from app.cli import create_admin
from app.core.db import get_sessionmaker
from app.models import User
from tests.conftest import STRONG_PASSWORD, login


def test_create_admin_rejects_emails_the_login_api_would_reject(monkeypatch):
    monkeypatch.setenv("PN_ADMIN_PASSWORD", STRONG_PASSWORD)
    with pytest.raises(SystemExit, match="Invalid email address"):
        create_admin("admin@policynest.local", "Priya Admin")
    with get_sessionmaker()() as db:
        assert db.scalar(select(User)) is None


def test_created_admin_can_sign_in(client, monkeypatch):
    monkeypatch.setenv("PN_ADMIN_PASSWORD", STRONG_PASSWORD)
    create_admin(" Priya.Admin@PolicyNest.in ", "Priya Admin")
    r = login(client, "priya.admin@policynest.in")
    assert r.status_code == 200, r.text
    assert r.json()["user"]["role"]["code"] == "ADMIN"
