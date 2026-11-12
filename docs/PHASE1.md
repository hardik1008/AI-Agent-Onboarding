# Phase 1 – Platform foundation

## Acceptance criteria

| Criterion | Status | Evidence |
| --- | --- | --- |
| Application starts successfully | Met | `docker compose up --build`; local uvicorn + `next dev`; `/health` |
| Database connects and migrations execute | Met | Alembic `0001_foundation`, `0002_rate_limits`; `/health/ready` reports `migrations_current: true`; `alembic check` clean |
| Users can register and log in | Met | `/register`, `/login`; `tests/test_auth.py` |
| Protected pages require authentication | Met | Next middleware redirects `/app/*` without a session; protected layout re-checks `/auth/me`; every API route depends on `get_auth` |
| Role permissions enforced by the backend | Met | `require_permission()` on every privileged route; `tests/test_rbac.py` |
| Unauthorized access is rejected | Met | 401 `NOT_AUTHENTICATED` / 403 `FORBIDDEN` / 403 `CSRF_FAILED`; denials audited as `access.denied` |
| Core tests pass | Met | backend 34 pytest tests (PostgreSQL), frontend 11 Vitest tests, lint, typecheck, build; all run in GitHub Actions (`.github/workflows/ci.yml`) |
| No hardcoded credentials or fake auth | Met | First admin created via `python -m app.cli create-admin`; secrets from env only |

## Security model

- **Passwords:** Argon2id; min 12 chars, letter + number, may not contain email local-part or name; transparent rehash on login.
- **Sessions:** opaque random token in an `HttpOnly`, `SameSite=Lax` cookie (`Secure` in production); only its HMAC-SHA256 is stored. 2 h idle / 12 h absolute expiry. Users can list and revoke sessions.
- **CSRF:** per-session token in a readable cookie, required as `X-CSRF-Token` on POST/PUT/PATCH/DELETE; `Origin` must match the allow-list.
- **Lockout:** 5 failed sign-ins lock the account for 15 minutes; admins can unlock.
- **Rate limiting:** login, registration, forgot-password and token endpoints (verify, check, reset/invite) are limited per client IP in fixed 15-minute windows (defaults 30 / 10 / 10 / 30, `RATE_LIMIT_*`). Counters live in PostgreSQL (`rate_limit_buckets`) so every worker shares them; excess requests get `429 RATE_LIMITED` with `Retry-After`, and the first rejection per window is audited as `security.rate_limited`. Client IP comes from `X-Forwarded-For` only when `TRUST_PROXY_HEADERS=true`; in Docker Compose the nginx `proxy` service overwrites that header with the real peer address, so clients cannot spoof it and audit/session IPs are the real client rather than the frontend container.
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
revocation, profile changes, all admin user changes, permission denials, CSRF rejections and rate-limit rejections. Denials are
written in an independent transaction so they persist even though the request fails. Mobile numbers and
passwords are never logged.

## Integrations status

| Integration | Phase 1 state |
| --- | --- |
| Email (SMTP) | Implemented. Mailpit in local dev; any SMTP provider in production; `NOT_CONFIGURED` when unset |
| OCR, PAN, bank (penny drop), DigiLocker, face match, SMS/WhatsApp, LMS | Reported as `NOT_CONFIGURED` on System status. Adapters are built in their phases; nothing is simulated |

## Known limitations

- Rate limits are per IP only; users behind one shared NAT share a budget. With `TRUST_PROXY_HEADERS=true` the backend port must only be reachable through the trusted proxy, otherwise `X-Forwarded-For` can be spoofed.
- Email is sent in-process via FastAPI background tasks; there is no retry queue. Failures are recorded in `email_deliveries` and visible on System status.
- No MFA for staff accounts yet.
- Admins cannot change a user's email address.
- Application, document and verification features are not part of Phase 1.
- The legacy prototype in `legacy/` is not wired to the new stack and is not run by Docker Compose.
