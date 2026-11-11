"""Phase 1 foundation: identity, RBAC, sessions, action tokens, audit log, email deliveries.

Revision ID: 0001_foundation
Revises:
Create Date: 2026-11-11
"""

import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

from alembic import op

revision = "0001_foundation"
down_revision = None
branch_labels = None
depends_on = None

TZ = sa.DateTime(timezone=True)

ROLES = [
    ("APPLICANT", "Applicant", "POSP candidate completing onboarding.", False),
    ("REVIEWER", "Reviewer", "Onboarding Ops verification officer.", True),
    ("SENIOR_REVIEWER", "Senior Reviewer", "Handles escalations, human-only decisions and fraud desk referrals.", True),
    ("ADMIN", "Administrator", "Manages users, roles, configuration and audit.", True),
]

PERMISSIONS = [
    ("profile:read", "profile", "View own profile and sessions."),
    ("profile:update", "profile", "Update own profile, password and sessions."),
    ("application:create", "application", "Create and edit own onboarding application."),
    ("application:read_own", "application", "View own onboarding application."),
    ("application:read_any", "application", "View any onboarding application (subject to ABAC)."),
    ("application:review", "application", "Work the review queue and request corrections."),
    ("application:decide", "application", "Approve or reject standard applications."),
    ("application:escalate", "application", "Escalate applications to senior review or fraud desk."),
    ("application:decide_escalated", "application", "Decide escalated and human-only cases."),
    ("fraud:review", "application", "Work fraud desk referrals."),
    ("analytics:read", "operations", "View operational analytics."),
    ("users:read", "admin", "View user accounts."),
    ("users:manage", "admin", "Invite users, change roles, activate or deactivate accounts."),
    ("roles:read", "admin", "View roles and permissions."),
    ("audit:read", "admin", "View the audit log."),
    ("system:read", "admin", "View system health and integration status."),
    ("config:manage", "admin", "Change platform configuration."),
]

_PROFILE = ["profile:read", "profile:update"]
_REVIEWER = _PROFILE + ["application:read_any", "application:review", "application:decide", "application:escalate"]
ROLE_PERMISSIONS = {
    "APPLICANT": _PROFILE + ["application:create", "application:read_own"],
    "REVIEWER": _REVIEWER,
    "SENIOR_REVIEWER": _REVIEWER + ["application:decide_escalated", "fraud:review", "analytics:read"],
    "ADMIN": _PROFILE
    + [
        "application:read_any",
        "analytics:read",
        "users:read",
        "users:manage",
        "roles:read",
        "audit:read",
        "system:read",
        "config:manage",
    ],
}


def upgrade() -> None:
    roles = op.create_table(
        "roles",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("code", sa.String(32), nullable=False),
        sa.Column("name", sa.String(64), nullable=False),
        sa.Column("description", sa.Text, nullable=False),
        sa.Column("is_staff", sa.Boolean, nullable=False),
        sa.PrimaryKeyConstraint("id", name="pk_roles"),
        sa.UniqueConstraint("code", name="uq_roles_code"),
    )
    permissions = op.create_table(
        "permissions",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("code", sa.String(64), nullable=False),
        sa.Column("category", sa.String(32), nullable=False),
        sa.Column("description", sa.Text, nullable=False),
        sa.PrimaryKeyConstraint("id", name="pk_permissions"),
        sa.UniqueConstraint("code", name="uq_permissions_code"),
    )
    op.create_table(
        "role_permissions",
        sa.Column("role_id", sa.Integer, nullable=False),
        sa.Column("permission_id", sa.Integer, nullable=False),
        sa.ForeignKeyConstraint(
            ["role_id"], ["roles.id"], ondelete="CASCADE", name="fk_role_permissions_role_id_roles"
        ),
        sa.ForeignKeyConstraint(
            ["permission_id"],
            ["permissions.id"],
            ondelete="CASCADE",
            name="fk_role_permissions_permission_id_permissions",
        ),
        sa.PrimaryKeyConstraint("role_id", "permission_id", name="pk_role_permissions"),
    )
    op.create_table(
        "users",
        sa.Column("id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("email", sa.String(320), nullable=False),
        sa.Column("full_name", sa.String(200), nullable=False),
        sa.Column("mobile", sa.String(16)),
        sa.Column("password_hash", sa.String(255)),
        sa.Column("role_id", sa.Integer, nullable=False),
        sa.Column("is_active", sa.Boolean, nullable=False, server_default=sa.true()),
        sa.Column("email_verified_at", TZ),
        sa.Column("failed_login_count", sa.Integer, nullable=False, server_default="0"),
        sa.Column("locked_until", TZ),
        sa.Column("last_login_at", TZ),
        sa.Column("password_changed_at", TZ),
        sa.Column("region", sa.String(32)),
        sa.Column("clearance_level", sa.SmallInteger, nullable=False, server_default="1"),
        sa.Column("created_at", TZ, server_default=sa.func.now(), nullable=False),
        sa.Column("updated_at", TZ, server_default=sa.func.now(), nullable=False),
        sa.PrimaryKeyConstraint("id", name="pk_users"),
        sa.UniqueConstraint("email", name="uq_users_email"),
        sa.ForeignKeyConstraint(["role_id"], ["roles.id"], name="fk_users_role_id_roles"),
        sa.CheckConstraint("email = lower(email)", name="email_lowercase"),
        sa.CheckConstraint("clearance_level BETWEEN 1 AND 3", name="clearance_range"),
    )
    op.create_index("ix_users_role_id", "users", ["role_id"])

    op.create_table(
        "user_sessions",
        sa.Column("id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("user_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("token_hash", sa.String(64), nullable=False),
        sa.Column("csrf_token", sa.String(64), nullable=False),
        sa.Column("created_at", TZ, server_default=sa.func.now(), nullable=False),
        sa.Column("last_seen_at", TZ, nullable=False),
        sa.Column("expires_at", TZ, nullable=False),
        sa.Column("revoked_at", TZ),
        sa.Column("ip_address", sa.String(64)),
        sa.Column("user_agent", sa.String(512)),
        sa.PrimaryKeyConstraint("id", name="pk_user_sessions"),
        sa.UniqueConstraint("token_hash", name="uq_user_sessions_token_hash"),
        sa.ForeignKeyConstraint(["user_id"], ["users.id"], ondelete="CASCADE", name="fk_user_sessions_user_id_users"),
    )
    op.create_index("ix_user_sessions_user_id", "user_sessions", ["user_id"])

    op.create_table(
        "user_action_tokens",
        sa.Column("id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("user_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("purpose", sa.String(32), nullable=False),
        sa.Column("token_hash", sa.String(64), nullable=False),
        sa.Column("created_at", TZ, server_default=sa.func.now(), nullable=False),
        sa.Column("expires_at", TZ, nullable=False),
        sa.Column("used_at", TZ),
        sa.PrimaryKeyConstraint("id", name="pk_user_action_tokens"),
        sa.UniqueConstraint("token_hash", name="uq_user_action_tokens_token_hash"),
        sa.ForeignKeyConstraint(
            ["user_id"], ["users.id"], ondelete="CASCADE", name="fk_user_action_tokens_user_id_users"
        ),
    )
    op.create_index("ix_user_action_tokens_user_id", "user_action_tokens", ["user_id"])

    op.create_table(
        "audit_logs",
        sa.Column("id", sa.BigInteger, sa.Identity(), nullable=False),
        sa.Column("occurred_at", TZ, server_default=sa.func.now(), nullable=False),
        sa.Column("actor_user_id", postgresql.UUID(as_uuid=True)),
        sa.Column("actor_email", sa.String(320)),
        sa.Column("actor_role", sa.String(32)),
        sa.Column("action", sa.String(100), nullable=False),
        sa.Column("outcome", sa.String(16), nullable=False),
        sa.Column("resource_type", sa.String(50)),
        sa.Column("resource_id", sa.String(100)),
        sa.Column("ip_address", sa.String(64)),
        sa.Column("user_agent", sa.String(512)),
        sa.Column("request_id", sa.String(64)),
        sa.Column("details", postgresql.JSONB, nullable=False, server_default=sa.text("'{}'::jsonb")),
        sa.PrimaryKeyConstraint("id", name="pk_audit_logs"),
    )
    op.create_index("ix_audit_logs_occurred_at", "audit_logs", ["occurred_at"])
    op.create_index("ix_audit_logs_action", "audit_logs", ["action"])
    op.create_index("ix_audit_logs_actor_user_id", "audit_logs", ["actor_user_id"])
    op.execute(
        """
        CREATE FUNCTION audit_logs_block_mutation() RETURNS trigger AS $$
        BEGIN
            RAISE EXCEPTION 'audit_logs is append-only';
        END;
        $$ LANGUAGE plpgsql;
        CREATE TRIGGER audit_logs_append_only BEFORE UPDATE OR DELETE ON audit_logs
            FOR EACH ROW EXECUTE FUNCTION audit_logs_block_mutation();
        """
    )

    op.create_table(
        "email_deliveries",
        sa.Column("id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("user_id", postgresql.UUID(as_uuid=True)),
        sa.Column("recipient", sa.String(320), nullable=False),
        sa.Column("template", sa.String(64), nullable=False),
        sa.Column("subject", sa.String(255), nullable=False),
        sa.Column("status", sa.String(20), nullable=False),
        sa.Column("provider", sa.String(32), nullable=False),
        sa.Column("error", sa.Text),
        sa.Column("created_at", TZ, server_default=sa.func.now(), nullable=False),
        sa.Column("sent_at", TZ),
        sa.PrimaryKeyConstraint("id", name="pk_email_deliveries"),
        sa.ForeignKeyConstraint(
            ["user_id"], ["users.id"], ondelete="SET NULL", name="fk_email_deliveries_user_id_users"
        ),
    )
    op.create_index("ix_email_deliveries_user_id", "email_deliveries", ["user_id"])

    op.bulk_insert(
        roles,
        [{"id": i + 1, "code": c, "name": n, "description": d, "is_staff": s} for i, (c, n, d, s) in enumerate(ROLES)],
    )
    op.bulk_insert(
        permissions,
        [{"id": i + 1, "code": c, "category": cat, "description": d} for i, (c, cat, d) in enumerate(PERMISSIONS)],
    )
    role_ids = {c: i + 1 for i, (c, *_rest) in enumerate(ROLES)}
    perm_ids = {c: i + 1 for i, (c, *_rest) in enumerate(PERMISSIONS)}
    rp = sa.table("role_permissions", sa.column("role_id", sa.Integer), sa.column("permission_id", sa.Integer))
    op.bulk_insert(
        rp,
        [
            {"role_id": role_ids[r], "permission_id": perm_ids[p]}
            for r, perms in ROLE_PERMISSIONS.items()
            for p in perms
        ],
    )
    op.execute("SELECT setval(pg_get_serial_sequence('roles', 'id'), (SELECT max(id) FROM roles))")
    op.execute("SELECT setval(pg_get_serial_sequence('permissions', 'id'), (SELECT max(id) FROM permissions))")


def downgrade() -> None:
    op.drop_table("email_deliveries")
    op.execute("DROP TRIGGER IF EXISTS audit_logs_append_only ON audit_logs")
    op.execute("DROP FUNCTION IF EXISTS audit_logs_block_mutation()")
    op.drop_table("audit_logs")
    op.drop_table("user_action_tokens")
    op.drop_table("user_sessions")
    op.drop_table("users")
    op.drop_table("role_permissions")
    op.drop_table("permissions")
    op.drop_table("roles")
