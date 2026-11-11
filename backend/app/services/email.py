import logging
import smtplib
import ssl
import uuid
from dataclasses import dataclass
from email.message import EmailMessage as MimeMessage
from html import escape
from typing import Protocol

from fastapi import BackgroundTasks
from sqlalchemy.orm import Session

from app.core.config import get_settings
from app.core.db import get_sessionmaker
from app.models import EmailDelivery, User
from app.models.base import utcnow

log = logging.getLogger("policynest.email")

STATUS_QUEUED = "QUEUED"
STATUS_SENT = "SENT"
STATUS_FAILED = "FAILED"
STATUS_NOT_CONFIGURED = "NOT_CONFIGURED"


@dataclass(frozen=True)
class OutgoingEmail:
    to: str
    subject: str
    text: str
    html: str


class EmailProvider(Protocol):
    name: str
    configured: bool

    def send(self, message: OutgoingEmail) -> None: ...


class SmtpEmailProvider:
    name = "smtp"
    configured = True

    def send(self, message: OutgoingEmail) -> None:
        s = get_settings()
        mime = MimeMessage()
        mime["From"] = s.email_from
        mime["To"] = message.to
        mime["Subject"] = message.subject
        mime.set_content(message.text)
        mime.add_alternative(message.html, subtype="html")
        assert s.smtp_host
        if s.smtp_ssl:
            server: smtplib.SMTP = smtplib.SMTP_SSL(
                s.smtp_host, s.smtp_port, timeout=s.smtp_timeout_seconds, context=ssl.create_default_context()
            )
        else:
            server = smtplib.SMTP(s.smtp_host, s.smtp_port, timeout=s.smtp_timeout_seconds)
        with server:
            if s.smtp_starttls and not s.smtp_ssl:
                server.starttls(context=ssl.create_default_context())
            if s.smtp_username and s.smtp_password:
                server.login(s.smtp_username, s.smtp_password)
            server.send_message(mime)


class UnconfiguredEmailProvider:
    name = "none"
    configured = False

    def send(self, message: OutgoingEmail) -> None:
        raise RuntimeError("Email provider is not configured")


_provider_override: EmailProvider | None = None


def set_provider_override(provider: EmailProvider | None) -> None:
    global _provider_override
    _provider_override = provider


def get_provider() -> EmailProvider:
    if _provider_override is not None:
        return _provider_override
    return SmtpEmailProvider() if get_settings().email_configured else UnconfiguredEmailProvider()


def _layout(title: str, intro: str, cta_label: str, url: str, footer: str) -> tuple[str, str]:
    text = f"{title}\n\n{intro}\n\n{cta_label}: {url}\n\n{footer}\n\n— PolicyNest Onboarding"
    html = f"""<!doctype html><html><body style="font-family:Inter,Arial,sans-serif;background:#f6f7fb;padding:24px">
<table role="presentation" style="max-width:520px;margin:auto;background:#fff;border-radius:12px;padding:32px;border:1px solid #e5e7eb">
<tr><td><p style="font-weight:700;color:#1e3a8a;font-size:18px;margin:0 0 16px">PolicyNest</p>
<h1 style="font-size:20px;color:#0f172a;margin:0 0 12px">{escape(title)}</h1>
<p style="color:#334155;line-height:1.6">{escape(intro)}</p>
<p style="margin:24px 0"><a href="{escape(url)}" style="background:#1d4ed8;color:#fff;padding:12px 20px;border-radius:8px;text-decoration:none;font-weight:600">{escape(cta_label)}</a></p>
<p style="color:#64748b;font-size:13px;line-height:1.5">{escape(footer)}</p>
<p style="color:#94a3b8;font-size:12px;word-break:break-all">{escape(url)}</p></td></tr></table></body></html>"""
    return text, html


def build_email(template: str, user: User, token: str) -> OutgoingEmail:
    s = get_settings()
    base = s.public_app_url.rstrip("/")
    if template == "verify_email":
        subject = "Verify your PolicyNest email address"
        url = f"{base}/verify-email?token={token}"
        text, html = _layout(
            "Confirm your email",
            f"Hi {user.full_name}, confirm this email address to continue your POSP onboarding.",
            "Verify email",
            url,
            f"This link expires in {s.email_verify_ttl_hours} hours. If you did not create an account, ignore this email.",
        )
    elif template == "password_reset":
        subject = "Reset your PolicyNest password"
        url = f"{base}/reset-password?token={token}"
        text, html = _layout(
            "Reset your password",
            f"Hi {user.full_name}, we received a request to reset your password.",
            "Choose a new password",
            url,
            f"This link expires in {s.password_reset_ttl_minutes} minutes and can be used once. "
            "If you did not request it, you can ignore this email.",
        )
    elif template == "invite":
        subject = "You have been invited to PolicyNest"
        url = f"{base}/accept-invite?token={token}"
        text, html = _layout(
            "Set up your PolicyNest account",
            f"Hi {user.full_name}, an administrator created a {user.role.name} account for you.",
            "Set your password",
            url,
            f"This invitation expires in {s.invite_ttl_hours} hours.",
        )
    else:
        raise ValueError(f"Unknown email template {template}")
    return OutgoingEmail(to=user.email, subject=subject, text=text, html=html)


def queue_email(db: Session, background: BackgroundTasks, user: User, template: str, token: str) -> str:
    """Create a delivery record and dispatch after the response. Returns the initial delivery status."""
    provider = get_provider()
    message = build_email(template, user, token)
    delivery = EmailDelivery(
        id=uuid.uuid4(),
        user_id=user.id,
        recipient=user.email,
        template=template,
        subject=message.subject,
        provider=provider.name,
        status=STATUS_QUEUED if provider.configured else STATUS_NOT_CONFIGURED,
        error=None if provider.configured else "No email provider configured (set SMTP_HOST and EMAIL_FROM).",
    )
    db.add(delivery)
    if provider.configured:
        background.add_task(_deliver, delivery.id, message)
    else:
        log.warning("Email '%s' to user %s not sent: provider not configured", template, user.id)
    return delivery.status


def _deliver(delivery_id: uuid.UUID, message: OutgoingEmail) -> None:
    provider = get_provider()
    status, error = STATUS_SENT, None
    try:
        provider.send(message)
    except Exception as exc:  # noqa: BLE001 - any provider failure is recorded, not raised
        status, error = STATUS_FAILED, f"{type(exc).__name__}: {exc}"[:1000]
        log.error("Email delivery %s failed: %s", delivery_id, error)
    with get_sessionmaker()() as db:
        delivery = db.get(EmailDelivery, delivery_id)
        if delivery:
            delivery.status = status
            delivery.error = error
            delivery.sent_at = utcnow() if status == STATUS_SENT else None
            db.commit()
