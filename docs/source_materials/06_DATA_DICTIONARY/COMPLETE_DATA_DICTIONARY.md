# PolicyNest Complete Data Dictionary & KPI Mathematical Formulations

> **Authoritative Specification of All Relational Entities, Attributes, Validation Rules, and Operational Metrics**  
> **Project:** PolicyNest AI-First POSP Onboarding Platform  
> **Source Base:** Masters' Union Applied AI Challenge (PS-01 AI-First Onboarding Data Pack)

---

## 1. Table-by-Table Data Dictionary

### 1.1 `applications` Entity (Historical Cohort — 3,018 records)
Primary operational entity storing applicant demographic data, KYC submissions, pipeline milestones, and completion status.

| Field Name | Type | Nullable | Format / Allowed Values | Validation Rules & Business Semantics | Downstream Impact |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `application_id` | `VARCHAR(32)` | No | PK: `^APP-[0-9]{5}$` | Unique identifier generated upon onboarding registration. Monotonically increasing. | Primary join key across `stage_events` and analytics. |
| `created_at` | `DATETIME` | No | ISO 8601 UTC timestamp | Must equal the first `APPLICATION_STARTED` timestamp in `stage_events`. | Anchor for calculating overall Turnaround Time (TAT). |
| `channel` | `VARCHAR(32)` | No | `Organic`, `Agent Referral`, `Digital Campaign`, `Campus` | Sourcing channel attribution. Determines CAC and cohort conversion rate. | Used in funnel drop-off analysis by channel. |
| `state` | `VARCHAR(64)` | No | 28 Indian States & 8 Union Territories | Declared residence state. Must be a valid Indian administrative state. | Regional compliance and language routing. |
| `city` | `VARCHAR(64)` | No | City name | Declared city of residence. | Geo-demographic reporting. |
| `applicant_name` | `VARCHAR(128)` | No | Normalized uppercase / title case | Declared full legal name. Used as candidate string in Name Matching Engine. | Matched against PAN, Aadhaar, 10th, and Cheque. |
| `gender` | `VARCHAR(16)` | No | `MALE`, `FEMALE`, `OTHER` | Self-declared gender. | Demographic analytics. |
| `dob_declared` | `DATE` | No | `YYYY-MM-DD` | Applicant declared date of birth. Must satisfy `created_at - dob >= 18.00 years`. | Baseline for age verification against KYC documents. |
| `mobile_masked` | `VARCHAR(16)` | No | `XXXXXX[0-9]{4}` | Masked 10-digit mobile number for privacy preservation. | Communication channel for OTP and rework SMS. |
| `pan_declared` | `VARCHAR(10)` | No | `^[A-Z]{5}[0-9]{4}[A-Z]$` | Declared PAN. 4th char must be `'P'`. 5th char typically matches surname. | Anchor identifier for IRDAI registry lookup. |
| `aadhaar_masked`| `VARCHAR(16)` | No | `XXXX-XXXX-[0-9]{4}` | Only last 4 digits stored. Storing 12 digits violates Aadhaar Act §29. | Identity anchor; checked against Aadhaar OCR. |
| `education_declared` | `VARCHAR(32)` | No | `Class 10`, `Class 12`, `Graduate`, `Post-graduate` | Self-declared highest education level. Must be >= `Class 10`. | Cross-checked against Class 10 marksheet result. |
| `bank_name` | `VARCHAR(128)` | No | Scheduled Commercial Bank / Payment Bank | Declared financial institution for commission payouts. | Reconciled against penny-drop API response. |
| `ifsc` | `VARCHAR(11)` | No | `^[A-Z]{4}0[A-Z0-9]{6}$` | 11-character Indian Financial System Code. 5th character must be `'0'`. | Branch routing for penny drop and commission payouts. |
| `account_last4` | `VARCHAR(8)` | No | `[0-9]{4}` | Last 4 digits of bank account. | Validated against cheque OCR. |
| `docs_submitted_at`| `DATETIME` | Yes | ISO 8601 UTC timestamp | Set when all 5 initial documents are uploaded. Null if dropped before docs. | Marks start of Ops Review SLA queue. |
| `kyc_verified_at` | `DATETIME` | Yes | ISO 8601 UTC timestamp | Set when KYC passes (either autonomous STP or human approval). | Triggers LMS training account activation. |
| `training_started_at`| `DATETIME` | Yes | ISO 8601 UTC timestamp | Set when applicant logs into LMS and begins mandatory 15-hr course. | LMS progress tracking. |
| `training_completed_at`| `DATETIME` | Yes | ISO 8601 UTC timestamp | Set when applicant completes 15.0 certified hours. | Unlocks POSP certification examination. |
| `exam_passed_at` | `DATETIME` | Yes | ISO 8601 UTC timestamp | Set when applicant achieves passing score (>= 50%) on proctored exam. | Unlocks digital certificate generation. |
| `certified_at` | `DATETIME` | Yes | ISO 8601 UTC timestamp | Final issuance of POSP license and registration with IRDAI. | Milestone marking successful onboarding completion. |
| `status` | `VARCHAR(32)` | No | `CERTIFIED`, `REJECTED`, `DROPPED_OUT`, `IN_PROGRESS` | Lifecycle state of application. | Primary operational funnel classification. |
| `rejection_reason`| `VARCHAR(64)` | Yes | Defect reason code from `reason_codes.csv` | Non-null if status is `REJECTED` or `DROPPED_OUT`. | Defect root-cause Pareto analysis. |
| `ops_reviewer_id` | `VARCHAR(16)` | Yes | FK: `^REV-[0-9]{2}$` | Reviewer assigned for manual verification. Null if fully STP. | Links to `ops_team.csv` for reviewer attribution. |
| `manual_touches` | `INTEGER` | No | `>= 0` | Count of distinct human reviewer actions. STP cases have `manual_touches == 0`. | Metric for ops efficiency and automation level. |
| `resubmissions` | `INTEGER` | No | `>= 0` | Count of rework cycles (document re-uploads requested). | Inverse indicator of First-Pass Yield (FPY). |
| `hours_to_certify`| `FLOAT` | Yes | `(certified_at - created_at) / 3600.0` | Total lifecycle duration in elapsed hours. Null if not certified. | Core speed KPI (TAT). |

---

### 1.2 `documents` Entity (Evaluation Benchmark — 3,600 records)
Stores document-level OCR extractions, quality indicators, and reviewer labels for exactly 600 applications (6 documents per application).

| Field Name | Type | Nullable | Format / Allowed Values | Validation Rules & Business Semantics |
| :--- | :--- | :--- | :--- | :--- |
| `doc_id` | `VARCHAR(32)` | No | PK: `^DOC-[0-9]{5}$` | Unique identifier for each uploaded document record. |
| `application_id` | `VARCHAR(32)` | No | FK: References `application_truth.application_id` | Foreign key binding document to candidate application. |
| `doc_type` | `VARCHAR(32)` | No | `PAN`, `AADHAAR_FRONT`, `AADHAAR_BACK`, `CLASS10_MARKSHEET`, `BANK_DOCUMENT`, `SELFIE` | Canonical document category. Exactly one of each per application. |
| `image_quality` | `VARCHAR(16)` | No | `OK`, `BLURRY`, `CROPPED`, `GLARE` | CV quality assessment. Any value other than `OK` triggers `REUPLOAD`. |
| `ocr_confidence` | `FLOAT` | Yes | `0.000` to `1.000` | Average confidence of OCR text recognition. Values `< 0.75` trigger quality warning. |
| `ocr_text` | `TEXT` | Yes | Full UTF-8 text string | Verbatim output from OCR extraction engine. |
| `name_extracted` | `VARCHAR(128)` | Yes | Extracted name string | Entity-extracted applicant name from document OCR. |
| `dob_extracted` | `VARCHAR(32)` | Yes | `DD/MM/YYYY`, `YYYY-MM-DD`, `YYYY` | Date of birth extracted from document. May be year-only on Aadhaar. |
| `id_number_extracted`| `VARCHAR(32)` | Yes | ID string | PAN number, Aadhaar last 4, Roll number, Account/IFSC extracted from text. |
| `face_match_score`| `FLOAT` | Yes | `0.00` to `1.00` | Biometric match score against PAN card photo. Populated ONLY for `SELFIE`. |
| `human_verdict` | `VARCHAR(16)` | No | `PASS`, `REUPLOAD`, `REJECT` | Ground truth human reviewer evaluation. |
| `human_reason_code`| `VARCHAR(32)` | Yes | Foreign key to `reason_codes.reason_code` | Specific defect code assigned by reviewer when verdict != `PASS`. |
| `reviewer_minutes`| `FLOAT` | No | `>= 0.0` | Elapsed human reviewer time in minutes spent verifying this document. |

---

### 1.3 `application_truth` Entity (Ground Truth Decisions — 600 records)
Golden benchmark dataset used for validating automated decision logic against ground truth.

| Field Name | Type | Nullable | Description / Business Semantics |
| :--- | :--- | :--- | :--- |
| `application_id` | `VARCHAR(32)` | No | PK: `^APP-26[0-9]{3}$` (APP-26000 to APP-26599). |
| `declared_name` | `VARCHAR(128)` | No | Form-declared full name. |
| `declared_dob` | `VARCHAR(16)` | No | Form-declared DOB (`DD/MM/YYYY`). |
| `declared_pan` | `VARCHAR(10)` | No | Form-declared PAN. |
| `declared_education`| `VARCHAR(32)` | No | Form-declared education qualification. |
| `declared_state` | `VARCHAR(64)` | No | Form-declared residential state. |
| `penny_drop_name_returned`| `VARCHAR(128)`| Yes | Account holder name returned by banking API. Null if penny-drop fails. |
| `irdai_posp_registry_hit`| `VARCHAR(8)` | No | `Yes` if PAN is registered with another insurer/broker; `No` otherwise. |
| `final_decision` | `VARCHAR(16)` | No | Ground truth application verdict: `APPROVE`, `NEEDS_MORE_INFO`, `REJECT`. |
| `decision_reasons` | `VARCHAR(128)`| Yes | Semicolon-delimited list of applicable reason codes (e.g. `DOB_MISMATCH`). |
| `name_match_category`| `VARCHAR(32)` | No | Name pattern classification: `exact`, `initial`, `swap`, `middle added`, `spelling`, `different`. |
| `is_hard_case` | `INTEGER` | No | Binary flag (`0` or `1`) identifying edge cases that stress-test policy logic. |

---

### 1.4 `stage_events` Entity (Audit Trail — 21,188 records)
Event sourcing log capturing every granular lifecycle event.

| Field Name | Type | Description |
| :--- | :--- | :--- |
| `application_id` | `VARCHAR(32)` | FK: References `applications.application_id`. |
| `event_time` | `DATETIME` | Exact timestamp of state event. |
| `actor` | `VARCHAR(32)` | Initiating entity: `APPLICANT`, `OPS_REVIEWER`, `SYSTEM`, `TRAINING_ENGINE`. |
| `event` | `VARCHAR(32)` | Event type: `APPLICATION_STARTED`, `DOCS_UPLOADED`, `KYC_APPROVED`, `REWORK_REQUESTED`, `REWORK_SUBMITTED`, `TRAINING_STARTED`, `TRAINING_COMPLETED`, `EXAM_PASSED`, `CERTIFICATE_ISSUED`, `REJECTED`, `DROPPED_OUT`. |
| `note` | `TEXT` | Diagnostic comment, rework request details, or failure explanation. |

---

### 1.5 `ops_team` Entity (Reviewer Roster — 22 records)
Operations reviewer team metadata for capacity planning and cost modeling.

| Field Name | Type | Description |
| :--- | :--- | :--- |
| `reviewer_id` | `VARCHAR(16)` | PK: `REV-01` to `REV-22`. |
| `team` | `VARCHAR(32)` | `Tier 1 Ops`, `Tier 2 Senior Ops`, `Fraud Desk`. |
| `tenure_months` | `INTEGER` | Reviewer experience in months. |
| `shift` | `VARCHAR(16)` | `Morning`, `Evening`, `General`. |
| `speed_index` | `FLOAT` | Review speed factor (relative to 1.0 standard). Higher is faster. |
| `loaded_cost_inr_per_hour` | `FLOAT` | Fully burdened labor rate in INR (₹280 to ₹520/hr). |
| `applications_handled_jan_sep`| `INTEGER` | Total applications reviewed in 9-month period. |

---

### 1.6 `monthly_funnel` Entity (Historical KPIs — 9 records)
Monthly operational rollups from January 2026 to September 2026.

| Field Name | Type | Description |
| :--- | :--- | :--- |
| `month` | `VARCHAR(16)` | Reporting period (`2026-01` to `2026-09`). |
| `applications` | `INTEGER` | Total applications initiated in month. |
| `certified` | `INTEGER` | Total POSPs successfully certified. |
| `dropped` | `INTEGER` | Applicants who abandoned the onboarding funnel. |
| `rejected` | `INTEGER` | Applicants rejected due to statutory ineligibility. |
| `median_hours_to_certify` | `FLOAT` | Median elapsed TAT in hours for certified POSPs. |
| `avg_manual_touches` | `FLOAT` | Average number of human reviewer interactions per application. |
| `certification_rate` | `FLOAT` | `certified / applications` ratio. |

---

### 1.7 `reason_codes` Entity (Taxonomy — 14 records)
Official standard defect codes, verdicts, and definitions.

| Reason Code | Verdict Type | Meaning / Statutory Justification |
| :--- | :--- | :--- |
| `IMAGE_BLURRY` | `REUPLOAD` | Text not legible at normal zoom due to motion blur or poor focus. |
| `IMAGE_CROPPED` | `REUPLOAD` | Part of the document is outside the camera frame; missing corners. |
| `IMAGE_GLARE` | `REUPLOAD` | Direct light reflection washes out critical required fields. |
| `PAN_FORMAT_INVALID` | `REJECT` | PAN does not match regex `AAAAA9999A` or fails checksum. |
| `PAN_NOT_INDIVIDUAL` | `REJECT` | 4th character is not 'P' (corporate, firm, trust, or HUF PAN). |
| `EDU_NOT_ELIGIBLE` | `REJECT` | Class 10 examination not passed or board not recognized. |
| `NAME_MISMATCH` | `REJECT` | Document belongs to a completely different individual (fraud risk). |
| `NAME_SPELLING_VARIANT`| `NEEDS_INFO`| Same person; slight phonetic or transliteration spelling variation. |
| `DOB_MISMATCH` | `NEEDS_INFO`| Date of birth conflicts across KYC documents (PAN is anchor). |
| `BANK_NAME_MISMATCH` | `NEEDS_INFO`| Account holder name from penny drop does not match applicant. |
| `FACE_MATCH_LOW` | `NEEDS_INFO`| Biometric selfie vs PAN photo cosine similarity < 0.60. |
| `UNDERAGE` | `REJECT` | Applicant is under 18 years on the application date. |
| `ALREADY_REGISTERED` | `REJECT` | PAN already registered as POSP with another insurer/intermediary. |
| `REVIEWER_DISCRETION` | `NEEDS_INFO`| Unclassified edge case requiring subjective reviewer clarification. |

---

## 2. Operational KPI Mathematical Formulations

To ensure rigorous benchmarking and commercial-grade analytics, all performance metrics in PolicyNest must be calculated using the exact formulas below:

### 2.1 Straight-Through Processing (STP) Rate
Measures the percentage of completed applications that pass from registration through KYC verification to LMS training without any human reviewer intervention.

$$	ext{STP Rate} = rac{\sum_{i=1}^{N} \mathbb{I}(	ext{status}_i = 	ext{'CERTIFIED'} \land 	ext{manual\_touches}_i = 0)}{\sum_{i=1}^{N} \mathbb{I}(	ext{status}_i = 	ext{'CERTIFIED'})} 	imes 100\%$$

- **Historical Baseline (Jan–Sep 2026):** $0.0\%$ (every application required at least 1 manual touch).
- **Target AI Platform Benchmark:** $\ge 65.0\%$.

---

### 2.2 First-Pass Yield (FPY)
Measures the percentage of applicants whose initial document submissions are accepted without requiring a rework cycle (re-upload).

$$	ext{FPY} = rac{\sum_{i=1}^{N} \mathbb{I}(	ext{docs\_submitted}_i \land 	ext{resubmissions}_i = 0)}{\sum_{i=1}^{N} \mathbb{I}(	ext{docs\_submitted}_i)} 	imes 100\%$$

- **Historical Baseline:** $38.4\%$.
- **Target with Instant AI Client-Side Guidance:** $\ge 75.0\%$.

---

### 2.3 Turnaround Time (TAT) / Hours to Certify
Measures the total elapsed duration from application initiation to final POSP certificate generation.

$$	ext{TAT}_i = rac{	ext{Timestamp}(	ext{certified\_at}_i) - 	ext{Timestamp}(	ext{created\_at}_i)}{3600.0} \quad 	ext{[hours]}$$

$$	ext{Median TAT} = 	ext{Median}\left(\{ 	ext{TAT}_i : 	ext{status}_i = 	ext{'CERTIFIED'} \}ight)$$

- **Historical Baseline:** $114.2	ext{ hours}$ ($pprox 4.8	ext{ days}$).
- **Target AI Platform Benchmark:** $\le 24.0	ext{ hours}$ (LMS training completed within 15–20 active hours).

---

### 2.4 Operations Cost per Onboarded Agent
Calculates the fully loaded human reviewer labor cost incurred per successfully certified POSP.

$$	ext{Ops Cost per Agent} = rac{\sum_{r \in 	ext{Reviewers}} (	ext{Hours Worked}_r 	imes 	ext{Loaded Cost Rate}_r)}{	ext{Total Certified POSPs}}$$

$$	ext{Alternative Granular Formulation} = rac{\sum_{i \in 	ext{Certified}} \sum_{d \in 	ext{Docs}_i} \left( rac{	ext{Reviewer Minutes}_{i,d}}{60.0} 	imes 	ext{Loaded Rate}_{	ext{Reviewer}} ight)}{	ext{Total Certified POSPs}}$$

- **Historical Baseline:** $pprox 	ext{₹}1,450	ext{ per onboarded POSP}$.
- **Target AI Platform Benchmark:** $\le 	ext{₹}350	ext{ per onboarded POSP}$ ($> 75\%	ext{ reduction}$).

---

### 2.5 Touch Count & Rework Metrics
- **Average Touches:** $ar{T} = rac{1}{N} \sum_{i=1}^{N} 	ext{manual\_touches}_i$ (Baseline: $3.0	ext{ touches}$).
- **Drop-off Rate:** $	ext{Drop Rate} = rac{	ext{Dropped Applications}}{	ext{Total Applications}} 	imes 100\%$ (Baseline: $33.2\%$).
