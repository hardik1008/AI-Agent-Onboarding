from datetime import datetime

from sqlalchemy import DateTime, Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import Base


class RateLimitBucket(Base):
    """Fixed-window request counter shared by all API workers."""

    __tablename__ = "rate_limit_buckets"

    key: Mapped[str] = mapped_column(String(255), primary_key=True)
    window_start: Mapped[datetime] = mapped_column(DateTime(timezone=True), primary_key=True, index=True)
    count: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
