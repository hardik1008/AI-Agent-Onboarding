"""Rate limit buckets for unauthenticated auth endpoints.

Revision ID: 0002_rate_limits
Revises: 0001_foundation
Create Date: 2026-11-11
"""

import sqlalchemy as sa

from alembic import op

revision = "0002_rate_limits"
down_revision = "0001_foundation"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "rate_limit_buckets",
        sa.Column("key", sa.String(255), nullable=False),
        sa.Column("window_start", sa.DateTime(timezone=True), nullable=False),
        sa.Column("count", sa.Integer(), nullable=False),
        sa.PrimaryKeyConstraint("key", "window_start", name=op.f("pk_rate_limit_buckets")),
    )
    op.create_index(op.f("ix_rate_limit_buckets_window_start"), "rate_limit_buckets", ["window_start"])


def downgrade() -> None:
    op.drop_index(op.f("ix_rate_limit_buckets_window_start"), table_name="rate_limit_buckets")
    op.drop_table("rate_limit_buckets")
