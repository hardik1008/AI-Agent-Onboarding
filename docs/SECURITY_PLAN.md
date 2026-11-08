# PolicyNest AI-First POSP Onboarding Suite — Security & Compliance Plan
**Document ID:** PN-SEC-2026-V1  
**Regulatory Baseline:** IRDAI Information Security Guidelines 2026 & DPDP Act 2023  
**Security Standard:** NIST SP 800-162 (ABAC) & OWASP Top 10:2021  
**Author:** Chief Information Security Officer (CISO) & Lead Security Engineer  
**Effective Date:** 8 November 2026  
**Status:** MANDATORY SECURITY SPECIFICATION

---

## 1. Regulatory Compliance Frameworks

PolicyNest processes sensitive Personally Identifiable Information (PII), financial account numbers, educational certificates, and biometric photographs. All platform components must comply with:

1. **IRDAI Guidelines on Information and Cyber Security for Insurers and Intermediaries (2026)**:
   - Mandatory two-factor authentication (2FA) for administrative and reviewer access.
   - Immutable audit trails tracking every inspection, override, and status modification.
   - Segregation of duties: Reviewers cannot review applications originating outside their designated operational territory without Senior Supervisor escalation.
2. **Digital Personal Data Protection (DPDP) Act 2023**:
   - Explicit candidate consent captured and timestamped prior to document processing.
   - Purpose limitation: Candidate PII cannot be utilized for third-party commercial marketing.
   - Right to erasure and data retention policies: Application records retained for 5 years per statutory brokerage mandate, after which files are cryptographically shredded.
3. **Aadhaar Act 2016 (Section 4(3)) & UIDAI Circulars**:
   - **STRICT PROHIBITION**: Never store or display the full 12-digit Aadhaar number in any database column, log file, HTTP header, or client UI.
   - **MASKING ENGINE**: All incoming Aadhaar images must have the first 8 digits redacted immediately upon upload. Systems store and display only the last 4 digits (e.g. `XXXX-XXXX-9744`).

---

## 2. OWASP Top 10 InsurTech Threat Modeling & Countermeasures

| OWASP Risk | Threat Vector in POSP Onboarding | Architectural Countermeasure | Verification Mechanism |
| :--- | :--- | :--- | :--- |
| **A01: Broken Access Control** | An applicant views or modifies another applicant's documents via IDOR (`/api/applications/APP-XXXX`). | Strict tenant isolation in DB queries: `WHERE application_id = ? AND user_id = ?`. NIST ABAC Rule 1 blocks applicants from operational endpoints. | Automated IDOR penetration tests in `test_security_pentest.py`. |
| **A02: Cryptographic Failures** | Document images or database files leaked from server storage. | AES-256 encryption at rest for document vault. TLS 1.3 enforced for all transport. Sensitive PII hashed with SHA-256 with salts. | Regular cipher-suite audit and TLS protocol validation. |
| **A03: Injection** | SQL injection in application filters or shell injection in image processing. | Parameterized queries on all SQLite/PostgreSQL statements. Zero raw string concatenation. File names sanitized via `secure_filename`. | Bandit static analysis and SQLMap automated scans. |
| **A04: Insecure Design** | LLM makes autonomous, unmonitored regulatory decisions. | Deterministic Rulebook Engine v3.2 enforces statutory checks. ML provides probabilistic scoring; regulatory decisions require deterministic rule passes. | Model observatory sanity checks and confusion matrix audits. |
| **A05: Security Misconfiguration** | Debug routes, default passwords, or public directory listing exposed. | FastAPI `docs_url` disabled in production. CORS strictly restricted to authorized PolicyNest origins. Hardened Docker container. | Production configuration validator executed on startup. |
| **A06: Vulnerable Components** | Outdated pip dependencies containing known CVEs. | Pinned dependencies in `requirements.txt`. Automated Dependabot / safety scans. | `pip audit` and Snyk container vulnerability scans. |
| **A07: Identification & Auth Failures** | Brute-force OTP attacks or stolen session tokens. | Rate-limiting on `/api/auth/*` (max 5 attempts per 10 mins). Session tokens signed using HS256 with 2-hour expiry and secure cookie flags. | Automated auth brute-force simulation tests. |
| **A08: Software & Data Integrity Failures** | Tampered certificate downloads or spoofed webhook callbacks. | Cryptographic certificate hashing (SHA-256) verifiable via IRDAI public portal. Webhook HMAC signature validation. | Webhook replay attack tests and hash verification checks. |
| **A09: Security Logging & Monitoring Failures** | Reviewer overrides case without justification or audit trace. | Immutable `audit_trail` and `abac_access_logs` recording actor ID, IP address, timestamp, previous state, and justification notes. | Daily automated integrity checksum audit. |
| **A10: Server-Side Request Forgery (SSRF)** | Malicious document URL supplied in upload analysis. | File uploads accept multipart byte streams or Base64 payloads directly; system refuses to fetch arbitrary remote URLs. | SSRF payload test suite in QA pipeline. |

---

## 3. Strict PII Masking & Data Sanitization Standards

The platform enforces field-level sanitization across all layers:

```
[Candidate Declares Data] ──> [Sanitization Pipeline] ──> [Safe Display & Logging]
- Full Aadhaar Number (12 digits) ──> Extract Last 4 ──> "XXXX-XXXX-9744"
- Bank Account Number ────────────> Mask Middle ──────> "XXXXXX4820"
- Mobile Number ──────────────────> Mask Center ──────> "+91 98*** **820"
- Secret Keys / Passwords ────────> Purge Entirely ────> "[REDACTED]"
```

---

## 4. NIST SP 800-162 Attribute-Based Access Control Specification

Access decisions evaluate four distinct attribute categories:
1. **Subject Attributes ($S$)**: Role (`APPLICANT`, `OPS_REVIEWER`, `OPERATIONS_MANAGER`, `COMPLIANCE_OFFICER`, `SUPER_ADMIN`), Clearance Level ($1-3$), Assigned Region (`North`, `West`, `South`, `East`, `ALL`), Active Shift ($09:00 - 18:00$).
2. **Resource Attributes ($R$)**: Application ID, Applicant ID, Declared State, Is Hard Case (Boolean), Risk Score ($0.0 - 100.0$), Current Stage.
3. **Action Attributes ($A$)**: `submit_application`, `read_application`, `review_case`, `override_decision`, `approve_payout`, `view_analytics`, `retrain_model`.
4. **Environment Attributes ($E$)**: Current UTC Timestamp, Client IP Address, Device Fingerprint.

### The 5 Core Policy Rules

```python
# Rule ABAC-0: Super Admin Global Executive Override
if S.role == "SUPER_ADMIN" and S.clearance_level >= 3:
    return PERMIT("Global administrative authority granted.")

# Rule ABAC-1: Applicant Tenant Isolation
if S.role == "APPLICANT":
    if A in ["view_ops", "review_case", "view_analytics", "retrain_model"]:
        return DENY("Applicants cannot access internal operational perspectives.")
    if R.owner_id != S.id:
        return DENY("Cross-tenant access violation: Cannot inspect unowned application.")
    return PERMIT("Self-service applicant access granted.")

# Rule ABAC-2: Regional Ops Jurisdiction
if S.role == "OPS_REVIEWER":
    if S.assigned_region != "ALL" and S.assigned_region != R.region:
        return DENY(f"Reviewer region ({S.assigned_region}) does not match case region ({R.region}).")

# Rule ABAC-3: Senior Clearance for Hard/High-Risk Cases
if S.role in ["OPS_REVIEWER", "OPERATIONS_MANAGER"]:
    if (R.is_hard_case or R.risk_score > 70.0) and S.clearance_level < 2:
        return DENY("Escalated case requires Senior Reviewer (Clearance Level 2+) authorization.")

# Rule ABAC-4: Active Shift Schedule Enforcement
if S.role == "OPS_REVIEWER":
    if not (S.shift_start <= E.current_time <= S.shift_end):
        return DENY("Reviewer is currently outside authorized operational shift hours.")
```
