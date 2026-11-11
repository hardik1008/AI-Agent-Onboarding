"""Operational commands. Usage: python -m app.cli create-admin --email you@example.com --name "Full Name"."""

import argparse
import getpass
import os
import sys
import uuid

from sqlalchemy import select

from app.core.db import get_sessionmaker
from app.core.security import hash_password, password_problems
from app.models import AuditLog, Role, User
from app.models.base import utcnow
from app.rbac.catalog import RoleCode
from app.schemas.auth import normalize_name


def _read_password(email: str, name: str) -> str:
    password = os.environ.get("PN_ADMIN_PASSWORD")
    if password is None:
        password = getpass.getpass("Password: ")
        if password != getpass.getpass("Confirm password: "):
            sys.exit("Passwords do not match.")
    problems = password_problems(password, email, name)
    if problems:
        sys.exit("Weak password: " + " ".join(problems))
    return password


def create_admin(email: str, name: str) -> None:
    email = email.strip().lower()
    name = normalize_name(name)
    with get_sessionmaker()() as db:
        if db.scalar(select(User).where(User.email == email)):
            sys.exit(f"User {email} already exists.")
        role = db.scalar(select(Role).where(Role.code == RoleCode.ADMIN.value))
        if role is None:
            sys.exit("Roles are not seeded. Run `alembic upgrade head` first.")
        password = _read_password(email, name)
        now = utcnow()
        user = User(
            id=uuid.uuid4(),
            email=email,
            full_name=name,
            role=role,
            password_hash=hash_password(password),
            email_verified_at=now,
            password_changed_at=now,
            region="ALL",
            clearance_level=3,
        )
        db.add(user)
        db.add(
            AuditLog(
                action="admin.bootstrap_created",
                outcome="SUCCESS",
                actor_email="cli",
                resource_type="user",
                resource_id=str(user.id),
                details={"email": email},
            )
        )
        db.commit()
        print(f"Administrator {email} created.")


def main() -> None:
    parser = argparse.ArgumentParser(prog="python -m app.cli")
    sub = parser.add_subparsers(dest="command", required=True)
    p = sub.add_parser(
        "create-admin", help="Create an administrator account (password via prompt or PN_ADMIN_PASSWORD)"
    )
    p.add_argument("--email", required=True)
    p.add_argument("--name", required=True)
    args = parser.parse_args()
    if args.command == "create-admin":
        create_admin(args.email, args.name)


if __name__ == "__main__":
    main()
