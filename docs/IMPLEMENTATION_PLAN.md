# PolicyNest AI-First POSP Onboarding Suite — Master Implementation Plan
**Document ID:** PN-PLAN-2026-V1  
**Author:** Technical Delivery Manager & Principal Architect  
**Effective Date:** 8 November 2026  
**Status:** PHASED EXECUTION ROADMAP

---

## 1. Roadmap Overview & Phased Sequence

The project executes across **11 sequential, strictly audited phases**. Implementation proceeds iteratively; no downstream phase begins until upstream contracts, models, and acceptance criteria are fully satisfied.

```
[Phase 0: Audit & Architecture Baseline]
                     │
                     ▼
[Phase 1: Database Migration, Normalized Schema & Core Auth]
                     │
                     ▼
[Phase 2: Modular Applicant Portal & Multi-Step Lifecycle]
                     │
                     ▼
[Phase 3: Document Processing Pipeline & Quality Inspection]
                     │
                     ▼
[Phase 4: Cross-Document Entity Reasoning & Rulebook Engine]
                     │
                     ▼
[Phase 5: External Verification Adapters & Sandbox Isolation]
                     │
                     ▼
[Phase 6: Correction Orchestration & Reviewer Operations Cockpit]
                     │
                     ▼
[Phase 7: Regulatory 15-Hour LMS, Exam & Certification Engine]
                     │
                     ▼
[Phase 8: Operations Management Dashboard & Real-Time Telemetry]
                     │
                     ▼
[Phase 9: Comprehensive Security Hardening & End-to-End QA]
                     │
                     ▼
[Phase 10: Production Deployment, Handover & Documentation]
```

---

## 2. Phase-by-Phase Technical Specifications

### Phase 0: Repository Audit & Architecture Baseline
- **Objective**: Conduct comprehensive code, database, and requirement inspection.
- **Deliverables**: Complete 7 architectural documents in `docs/`.
- **Owner**: Principal Architect & CTO.
- **Acceptance Criteria**: 100% agreement between documented requirements and actual codebase assets.

### Phase 1: Database Migration, Normalized Schema & Core Auth
- **Objective**: Establish production-ready relational schema, Alembic migration pipeline, and secure authentication.
- **Scope**:
  - Implement 23 normalized tables in SQLite/PostgreSQL with foreign key constraints and indexes.
  - Implement JWT Bearer token generation with Argon2id password hashing.
  - Integrate FIDO2 WebAuthn relying party and Google GIS token validation.
  - Enforce backend route protection (`get_current_user`, `require_role`).
- **Owner**: Sub-Agent 3 (Backend & Database Engineer).
- **Acceptance Criteria**: All 36 endpoints enforce authentication; automated test `test_auth_rbac.py` passes with 100% assertions.

### Phase 2: Modular Applicant Portal & Multi-Step Lifecycle
- **Objective**: Refactor monolithic frontend into clean, accessible, responsive portal views.
- **Scope**:
  - Multi-step wizard: Step 0 Pre-Screen, Step 1 DigiLocker KYC, Step 2 Bank Mandate, Step 3 Biometric Liveness & e-Sign, Step 4 Status Tracker, Step 5 LMS.
  - Multi-part form validation with instantaneous inline feedback.
  - Save & Resume draft capability with local and remote persistence.
- **Owner**: Sub-Agent 2 (Frontend Engineer).
- **Acceptance Criteria**: Zero static mockups; real form submissions persist to `applications` table.

### Phase 3: Document Processing Pipeline & Quality Inspection
- **Objective**: Build an industrial-strength document ingestion and computer vision quality inspection service.
- **Scope**:
  - File upload validator (MIME checking, 10MB limit, magic byte validation).
  - OpenCV image preprocessing: Laplacian blur variance ($Var \ge 100$), luminance histogram glare ratio ($< 0.15$), orientation auto-correction.
  - OCR extraction service with field-level confidence scores.
  - Document versioning: preserve original and corrected images in private storage.
- **Owner**: Sub-Agent 4 (Document AI & OCR Engineer).
- **Acceptance Criteria**: Blurry, cropped, or glared documents trigger specific `REUPLOAD_REQUESTED` codes.

### Phase 4: Cross-Document Entity Reasoning & Rulebook Engine
- **Objective**: Implement deterministic PolicyNest Rulebook v3.2 and scikit-learn ML inference.
- **Scope**:
  - 8-tier name matching algorithm (§5: Exact, Initials, Swap, Middle Missing, Middle Added, Spelling Variant, Surname Change, Different Person).
  - Cross-check DOB across PAN, Aadhaar, and Class 10 Marksheet.
  - Formulate application-level outcome: `APPROVE`, `NEEDS_MORE_INFO`, `REJECT`.
  - Machine learning inference serving `model_decision_engine.joblib` (100 trees, 97.5% benchmark accuracy).
- **Owner**: Sub-Agent 6 (Workflow & Decision Engine Engineer).
- **Acceptance Criteria**: Evaluated on the 600-application benchmark dataset; 100% Reject Recall achieved.

### Phase 5: External Verification Adapters & Sandbox Isolation
- **Objective**: Build a provider-independent verification gateway with explicit sandbox labelling.
- **Scope**:
  - MeriPehchaan DigiLocker OAuth partner adapter.
  - NSDL / Income Tax PAN validation adapter.
  - NPCI IMPS ₹1 penny-drop banking switch adapter.
  - ISO/IEC 30107-3 compliant biometric face liveness adapter.
  - Strict separation: All mock/synthetic responses tagged `SANDBOX` in database.
- **Owner**: Sub-Agent 5 (Government & Bank Verification Engineer).
- **Acceptance Criteria**: Zero hardcoded mock responses masquerading as live verifications; clear integration readiness register.

### Phase 6: Correction Orchestration & Reviewer Operations Cockpit
- **Objective**: Eliminate piecemeal document requests and deliver a high-throughput reviewer cockpit.
- **Scope**:
  - Group all detectable issues into a single consolidated follow-up message in English and Hindi (§8).
  - Reviewer workspace: split-screen document viewer, OCR field correction override, queue filters (STP, Review, Reject).
  - NIST SP 800-162 ABAC enforcement: prevent out-of-jurisdiction reviews and enforce clearance levels.
- **Owner**: Sub-Agent 2 (Frontend) & Sub-Agent 6 (Workflow Engine).
- **Acceptance Criteria**: Reviewer decisions write immutable audit logs with justification.

### Phase 7: Regulatory 15-Hour LMS, Exam & Certification Engine
- **Objective**: Deliver statutory POSP training curriculum, exam engine, and verifiable certificate generator.
- **Scope**:
  - Gated access: locked until candidate clears KYC and bank mandate.
  - 4 statutory insurance modules (Motor, Health, Life, Governance).
  - Randomized 50-question regulatory exam with 70% passing threshold.
  - Verifiable digital certificate generation (`IRDAI-POSP-2026-XXXXX`) with SHA-256 tamper-proof seal.
- **Owner**: Sub-Agent 3 (Backend) & Sub-Agent 2 (Frontend).
- **Acceptance Criteria**: Exam scoring verified; certificate download renders official SVG/PDF vector.

### Phase 8: Operations Management Dashboard & Real-Time Telemetry
- **Objective**: Deliver database-backed operational command center with real visitor analytics.
- **Scope**:
  - Real-time visitor pulse monitoring (active sessions in last 5 minutes).
  - Stage-by-stage onboarding conversion funnel (Step 0 $\rightarrow$ Step 5 drop-offs).
  - Operations workforce queue analytics (reviewer utilization, queue age, SLA breaches).
  - AI Model Observatory: live confusion matrix, feature importances, 1-click model retraining.
- **Owner**: Sub-Agent 8 (DevOps & Observability) & Sub-Agent 3 (Backend).
- **Acceptance Criteria**: Dashboard aggregates 100% from SQLite `policynest.db`; zero hardcoded KPI values.

### Phase 9: Comprehensive Security Hardening & End-to-End QA
- **Objective**: Conduct rigorous security penetration testing and browser automation verification.
- **Scope**:
  - Penetration tests: IDOR, SQL injection, XSS, broken role access, rate limiting.
  - Automated headless Microsoft Edge CDP test suites (`test_browser_e2e.mjs`, `test_analytics_abac_e2e.mjs`).
  - Strict PII masking: verify zero full Aadhaar numbers in database or logs.
- **Owner**: Sub-Agent 7 (QA, Security & Compliance Engineer).
- **Acceptance Criteria**: 0 console errors, 0 security vulnerabilities with High/Critical severity.

### Phase 10: Production Deployment, Handover & Documentation
- **Objective**: Deploy live platform to production infrastructure and package deployment assets.
- **Scope**:
  - Docker containerization with multi-stage build.
  - Production blueprints for Render, Railway, and Lovable static CDN.
  - Public tunnel ingress maintenance.
  - Synchronize GitHub repository `saisidhardy/policy-nest-onboarding`.
- **Owner**: Sub-Agent 8 (DevOps Engineer) & Principal Architect.
- **Acceptance Criteria**: Fully functional public deployment accessible over HTTPS.
