# Phase 1 – Platform foundation

## Acceptance criteria

| Criterion | Status | Evidence |
| --- | --- | --- |
| Application starts successfully | Met | `docker compose up --build`; local uvicorn + `next dev`; `/health` |
| Database connects and migrations execute | Met | Alembic `0001_foundation`; `/health/ready` reports `migrations_current: true`; `alembic check` clean |
| Users can register and log in | Met | `/register`, `/login`; `tests/test_auth.py` |
| Protected pages require authentication | Met | Next middleware redirects `/app/*` without a session; protected layout re-checks `/auth/me`; every API route depends on `get_auth` |
| Role permissions enforced by the backend | Met | `require_permission()` on every privileged route; `tests/test_rbac.py` |
| Unauthorized access is rejected | Met | 401 `NOT_AUTHENTICATED` / 403 `FORBIDDEN` / 403 `CSRF_FAILED`; denials audited as `access.denied` |
| Core tests pass | Met | backend 26 pytest tests (PostgreSQL), frontend 11 Vitest tests, lint, typecheck, build |
| No hardcoded credentials or fake auth | Met | First admin created via `python -m app.cli create-admin`; secrets from env only |

## Security model

- **Passwords:** Argon2id; min 12 chars, letter + number, may not contain email local-part or name; transparent rehash on login.
- **Sessions:** opaque random token in an `HttpOnly`, `SameSite=Lax` cookie (`Secure` in production); only its HMAC-SHA256 is stored. 2 h idle / 12 h absolute expiry. Users can list and revoke sessions.
- **CSRF:** per-session token in a readable cookie, required as `X-CSRF-Token` on POST/PUT/PATCH/DELETE; `Origin` must match the allow-list.
- **Lockout:** 5 failed sign-ins lock the account for 15 minutes; admins can unlock.
- **Tokens:** email verification (24 h), password reset (30 min) and staff invitation (72 h) links are single-use, stored hashed; issuing a new one invalidates older ones; password reset revokes all sessions.
- **Account enumeration:** forgot-password always returns the same response; unknown emails spend equivalent hashing time on login.
- **Headers:** `X-Content-Type-Options`, `X-Frame-Options: DENY`, `Referrer-Policy`, `Permissions-Policy`, request IDs.

## Roles and access control

| Role | Purpose |
| --- | --- |
| Applicant | Self-registers; own profile and (Phase 2) own application only |
| Reviewer | Review queue, standard decisions, escalation (Phase 3+) |
| Senior Reviewer | Escalated / human-only decisions, fraud desk, analytics |
| Administrator | Users, roles, audit log, system status, configuration. Cannot decide applications (separation of duties) |

ABAC rules in `backend/app/rbac/policy.py` (unit-tested now, applied to application resources from Phase 2):
ownership isolation for applicants, reviewer region scope (`ALL` = national), clearance level vs. resource
sensitivity, and no self-administration (admins cannot change their own role or status; the last active
admin cannot be removed). Unverified applicants can only use profile permissions.

## Audit log

`audit_logs` is append-only: a PostgreSQL trigger rejects `UPDATE` and `DELETE`. Recorded events include
registration, sign-in success/failure, lockout, logout, verification, password reset/change, session
revocation, profile changes, all admin user changes, permission denials and CSRF rejections. Denials are
written in an independent transaction so they persist even though the request fails. Mobile numbers and
passwords are never logged.

## Integrations status

| Integration | Phase 1 state |
| --- | --- |
| Email (SMTP) | Implemented. Mailpit in local dev; any SMTP provider in production; `NOT_CONFIGURED` when unset |
| OCR, PAN, bank (penny drop), DigiLocker, face match, SMS/WhatsApp, LMS | Reported as `NOT_CONFIGURED` on System status. Adapters are built in their phases; nothing is simulated |

## Known limitations

- No rate limiting at the HTTP layer yet beyond account lockout (planned: reverse-proxy / Redis limiter).
- Email is sent in-process via FastAPI background tasks; there is no retry queue. Failures are recorded in `email_deliveries` and visible on System status.
- No MFA for staff accounts yet.
- Admins cannot change a user's email address.
- Application, document and verification features are not part of Phase 1.
- The legacy prototype in `legacy/` is not wired to the new stack and is not run by Docker Compose.
