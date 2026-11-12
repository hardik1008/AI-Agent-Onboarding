import math
import secrets
from datetime import datetime, timedelta, timezone

from fastapi import Request
from sqlalchemy import delete
from sqlalchemy.dialects.postgresql import insert

from app.core.config import get_settings
from app.core.db import get_engine
from app.core.errors import AppError
from app.core.request_context import client_ip
from app.models import RateLimitBucket
from app.models.base import utcnow
from app.services import audit

PRUNE_ONE_IN = 100
PRUNE_AFTER = timedelta(days=1)


def _window_start(now: datetime, window_seconds: int) -> datetime:
    epoch = int(now.timestamp())
    return datetime.fromtimestamp(epoch - epoch % window_seconds, tz=timezone.utc)


def hit(key: str, limit: int, window_seconds: int, now: datetime | None = None) -> tuple[int, int]:
    """Count one request against `key`; returns (count in current window, seconds until the window resets).

    Runs in its own transaction so rejected and failed requests still count.
    """
    now = now or utcnow()
    start = _window_start(now, window_seconds)
    stmt = (
        insert(RateLimitBucket)
        .values(key=key, window_start=start, count=1)
        .on_conflict_do_update(
            index_elements=[RateLimitBucket.key, RateLimitBucket.window_start],
            set_={"count": RateLimitBucket.count + 1},
        )
        .returning(RateLimitBucket.count)
    )
    with get_engine().begin() as conn:
        count = conn.execute(stmt).scalar_one()
        if secrets.randbelow(PRUNE_ONE_IN) == 0:
            conn.execute(delete(RateLimitBucket).where(RateLimitBucket.window_start < now - PRUNE_AFTER))
    reset_in = max(1, math.ceil((start + timedelta(seconds=window_seconds) - now).total_seconds()))
    return count, reset_in


def limit_by_ip(scope: str, setting: str):
    """FastAPI dependency limiting `scope` per client IP to `Settings.<setting>` requests per window."""

    def dependency(request: Request) -> None:
        s = get_settings()
        if not s.rate_limit_enabled:
            return
        limit = getattr(s, setting)
        ip = client_ip(request) or "unknown"
        count, reset_in = hit(f"{scope}:ip:{ip}", limit, s.rate_limit_window_seconds)
        if count <= limit:
            return
        if count == limit + 1:
            audit.record_independent(
                request, "security.rate_limited", audit.DENIED, details={"scope": scope, "limit": limit}
            )
        minutes = math.ceil(reset_in / 60)
        raise AppError(
            429,
            "RATE_LIMITED",
            f"Too many requests. Try again in {minutes} minute(s).",
            headers={"Retry-After": str(reset_in)},
        )

    return dependency
