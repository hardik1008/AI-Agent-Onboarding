# PolicyNest AI-First POSP Onboarding Suite — Product Requirements Document (PRD)
**Document ID:** PN-PRD-2026-V1  
**Problem Statement:** Masters' Union Applied AI Challenge · Problem Statement PS-01  
**Problem Owner:** Vansh Miglani, InsuranceDekho / PolicyNest Insurance Brokers  
**Author:** Technical Delivery Manager & Principal Architect  
**Effective Date:** 8 November 2026  
**Status:** APPROVED FOR COMMERCIAL IMPLEMENTATION

---

## 1. Context & Business Objectives

### 1.1 The Operational Bottleneck
PolicyNest Insurance Brokers distributes motor, health, and life insurance through a national network of Point of Sales Persons (POSPs). A 22-person Onboarding Operations team reviews all incoming agent credentials. Historical baseline metrics (January to September 2026 data pack) reveal:
- **3,000 Applications Started**: Only **1,732 (57.7%)** were certified; **951 (31.7%)** dropped out and **314 (10.5%)** were rejected.
- **8.4 Days Median Turnaround Time**: Ranging up to 13.0 days for the 90th percentile.
- **17.3 Hours Queue Wait**: Files languished in queues before a reviewer conducted the initial 21-minute manual inspection.
- **25.8% Return Rate & Piecemeal Friction**: Reviewers requested one document fix at a time; each cycle added 2.0 days, causing 27.0% of returned applicants to abandon the process permanently.
- **482 Dropouts Post-KYC**: 21.7% of applicants passed document verification but never started the statutory 15-hour training course.

### 1.2 Core Business Objectives
1. **Compress Total Turnaround**: Slash median certification time from 8.4 days to under 4.0 days (approaching the regulatory 15-hour training statutory floor).
2. **Autonomous Straight-Through Processing (STP)**: Auto-approve $\ge 60\%$ of clean applications within 3 minutes with zero human intervention.
3. **Consolidated Issue Communication**: Detect all document defects simultaneously and dispatch a single, comprehensive follow-up message in English or Hindi.
4. **Zero Regulatory Leakage**: Achieve **100% Reject Recall** on statutory disqualifications (underage, corporate PANs, failed marksheets, central registry hits).
5. **Human-in-the-Loop Judgement Routing**: Route ambiguous name spellings, marginal face matches (0.60–0.75), and marriage surname changes to specialized regional reviewers.

---

## 2. Target User Personas & Permissions Matrix

| Persona | Primary Role & Responsibility | Core Workflows & Access | Key Performance Indicators |
| :--- | :--- | :--- | :--- |
| **POSP Applicant** | Part-time advisor (shopkeeper, homemaker, gig worker). Needs fast onboarding on mobile. | Step 0-5 wizard, DigiLocker pull, bank mandate, webcam liveness, Form 1-A e-Sign, LMS course. | Time to apply (< 8 mins), Drop-off rate (< 10%). |
| **Ops Reviewer** | Operations officer in the 22-person workforce evaluating complex queues. | Filtered review queue, split-screen document viewer, OCR field correction, approve/reject/needs-info. | Review time per case (< 4 mins), SLA adherence (> 98%). |
| **Operations Manager** | Supervisors managing queue balance, shift scheduling, and team throughput. | Queue reassignment, workload balancing, regional jurisdiction management, bottleneck analytics. | Queue backlog, median first-review SLA (< 4 hours). |
| **Compliance Officer** | Legal & risk chiefs overseeing statutory adherence, IIB conflict, and fraud. | Exclusivity registry overrides, fraud desk referrals, audit log inspection, ML model accuracy checks. | Regulatory compliance (100%), False approval rate (0.0%). |
| **Super Admin** | Platform architects and system administrators managing infra. | User role administration, NIST ABAC policy configuration, provider credentials, telemetry observatory. | System uptime (99.9%), API latency (< 250ms). |

---

## 3. The 10-Section Operational Rulebook Requirements

### §1. Purpose & Scope
The platform must automate PolicyNest Onboarding Operations Standard v3.2. Decisions must be deterministic, auditable, and traceable to specific rulebook citations.

### §2. Regulatory Eligibility
- **Rule 2.1 (Age)**: Applicant must be $\ge 18.0$ years old on application start date. If DOB indicates $< 18$: Disqualify with `REJECT — UNDERAGE`.
- **Rule 2.2 (Education)**: Must have passed Class 10 (secondary) from a recognized central or state board. If result is FAIL or absent: `REJECT — EDU_NOT_ELIGIBLE`.
- **Rule 2.3 (Individual Identity)**: Valid individual PAN required. 4th character must be `'P'`. If `'C'`, `'F'`, `'H'`, `'T'`, etc.: `REJECT — PAN_NOT_INDIVIDUAL`.
- **Rule 2.4 (Exclusivity)**: Cannot hold an active POSP license with another insurer or intermediary. If IRDAI central registry hit: `REJECT — ALREADY_REGISTERED`.

### §3. Mandatory Document Collection
1. **PAN Card**: Anchor document. Name and DOB serve as ground truth.
2. **Aadhaar Card (Front & Back)**: Identity and address. **Regulatory Rule**: Only store last 4 digits; first 8 digits must be masked immediately.
3. **Class 10 Marksheet / Certificate**: Educational eligibility and secondary identity validation.
4. **Cancelled Cheque / Bank Statement**: Account holder name, Account number, and IFSC for commission payouts.
5. **Biometric Photograph / Live Selfie**: Captured via webcam, matched against PAN photo with anti-spoofing liveness verification.

### §4. Per-Document Acceptance Criteria
- **4.1 Image Quality**: Laplacian blur variance $\ge 100.0$, glare luminance ratio $< 0.15$, all four corners visible. OCR confidence must be $\ge 0.75$. If failed: `REUPLOAD — IMAGE_BLURRY` or `IMAGE_GLARE` or `IMAGE_CROPPED`.
- **4.2 PAN Quality**: Format must strictly match `^[A-Z]{5}[0-9]{4}[A-Z]$`. 5th character should correspond to surname initial.
- **4.3 Aadhaar**: Name and DOB must agree with PAN. Address state difference is informational and never grounds for rejection.
- **4.4 Class 10 Marksheet**: Must indicate PASS. Unrecognized boards routed to `HUMAN_REVIEW`.
- **4.5 Bank Verification**: Account must belong to applicant (joint accounts permitted only if applicant is primary holder). NPCI penny-drop beneficiary name must match PAN name. Third-party accounts (spouse, parent) strictly forbidden: `NEEDS_INFO — BANK_NAME_MISMATCH`.
- **4.6 Facial Biometrics**:
  - Score $\ge 0.75$: Automatic Pass.
  - Score $0.60 - 0.75$: Route to `HUMAN_REVIEW` (Human only).
  - Score $< 0.60$: `NEEDS_INFO — FACE_MATCH_LOW`. Two consecutive failures trigger fraud desk escalation.

### §5. Name Matching Taxonomy
Cross-document name reconciliation must apply the approved 8-tier hierarchy:
1. **Exact Match**: Character-for-character match ignoring case and whitespace $\rightarrow$ `MATCH`.
2. **Initials Match**: Initials for first/middle names (e.g. `RAHUL KUMAR SHARMA` $\leftrightarrow$ `R K SHARMA`) $\rightarrow$ `MATCH`.
3. **Order Swapped**: Reordered tokens (e.g. `RAHUL KUMAR SHARMA` $\leftrightarrow$ `SHARMA RAHUL KUMAR`) $\rightarrow$ `MATCH`.
4. **Middle Name Missing**: Dropped middle token (e.g. `RAHUL KUMAR SHARMA` $\leftrightarrow$ `RAHUL SHARMA`) $\rightarrow$ `MATCH`.
5. **Middle Name Added**: Additional middle token (e.g. `PRIYA SHARMA` $\leftrightarrow$ `PRIYA KUMARI SHARMA`) $\rightarrow$ `MATCH`.
6. **Spelling Variants**: Common phonetic/regional variants (`MOHAMMAD` $\leftrightarrow$ `MOHAMMED`, `LAXMI` $\leftrightarrow$ `LAKSHMI`) $\rightarrow$ `NEEDS_INFO — NAME_SPELLING_VARIANT` (Requires applicant confirmation).
7. **Surname Change (Marriage)**: Surname changed post-marriage (`PRIYA SHARMA` $\rightarrow$ `PRIYA VERMA`) $\rightarrow$ `NEEDS_INFO` (Route to human review with marriage certificate request).
8. **Different Person**: Complete token divergence (`RAHUL SHARMA` $\leftrightarrow$ `ANKIT YADAV`) $\rightarrow$ `REJECT — NAME_MISMATCH` (Escalate to fraud desk).

### §6. Application-Level Decision Logic
- If ANY document finding is `REJECT` $\rightarrow$ Final Decision: **`REJECT`** (List every failure reason).
- Else if ANY finding is `NEEDS_INFO` or `REUPLOAD` $\rightarrow$ Final Decision: **`NEEDS_MORE_INFO`** (Generate single consolidated checklist).
- Else $\rightarrow$ Final Decision: **`APPROVE`** (Trigger instant provisional agent code and unlock 15-Hour LMS).

### §7. Service Level Agreements (SLAs) & Escalation
- Initial Document Review: **4 working hours** (Escalate to Team Lead at 8 hours).
- Re-upload Review: **2 working hours** (Escalate at 4 hours).
- Fraud Desk Referral: **Same-day review** by Compliance Officer.
- Applicant Query Response: **1 working hour** via WhatsApp/SMS copilot.

### §8. Consolidated Communication Standards
Follow-up messages must group all outstanding requirements into a single communication dispatched in the applicant's preferred language (English or Hindi). Individual, piecemeal requests are prohibited.

---

## 4. Primary System Portals & Functional Specifications

### Portal A: Candidate Onboarding Portal (`join.policynest.com`)
1. **Step 0 — Statutory Pre-Screen**: Real-time validation of DOB, individual PAN format, and exclusivity prior to uploading any files.
2. **Step 1 — Identity & DigiLocker e-KYC**: MeriPehchaan OAuth modal integration pulling cryptographically verified XML records.
3. **Step 2 — Bank Payout Mandate**: Live RBI IFSC directory lookup + NPCI IMPS ₹1 penny drop with banking switch visualization.
4. **Step 3 — Biometric Liveness & Form 1-A e-Sign**: Real HTML5 webcam capture, passive anti-spoofing liveness verification, canvas signature capture, and downloadable legal PDF generation.
5. **Step 4 — Application Decision Status**: Real-time status tracker displaying STP auto-approval or consolidated correction items.
6. **Step 5 — 15-Hour Statutory LMS Classroom**: Modular insurance curriculum, randomized 50-question regulatory exam, and instant cryptographic certificate generation (`IRDAI-POSP-2026-XXXXX`).

### Portal B: Reviewer Operations Cockpit (`ops.policynest.com`)
1. **Queue Management**: Multi-filter application grid (STP Approved, Manual Review Queue, Rejected, Incomplete).
2. **Side-by-Side Document Comparator**: Visual comparison of PAN, Aadhaar, Cheque, and Marksheet with extracted OCR bounding boxes and field confidence scores.
3. **Field-Level Correction Override**: Allows reviewers to correct noisy OCR text with an audited modification reason.
4. **Adjudication Actions**: 1-click Approve, Reject, or Return Consolidated with automated WhatsApp/SMS dispatch.
5. **NIST ABAC Jurisdiction Guard**: Blocks out-of-region reviews and restricts hard cases to senior reviewers.

### Portal C: Executive Management & Analytics Dashboard (`admin.policynest.com`)
1. **Google Analytics 4 / PostHog Telemetry Pulse**: Live active visitors counter, today's session volume, bounce rate, and average candidate dwell time.
2. **Conversion Funnel Breakdown**: Granular drop-off analysis between Step 0, Step 1, Step 2, Step 3, Step 4, and Step 5.
3. **Interactive ABAC Policy Inspector**: Real-time Policy Decision Point (PDP) sandbox allowing compliance officers to test multi-attribute policies.
4. **AI Observatory & Retraining Lab**: Live confusion matrix, 14 Gini feature importances, and 1-click model retraining with 5-fold cross-validation.
5. **Integration Provider Health Register**: Real-time operational monitoring of DigiLocker, NSDL, UIDAI, NPCI, and Telecom DLT gateways.
