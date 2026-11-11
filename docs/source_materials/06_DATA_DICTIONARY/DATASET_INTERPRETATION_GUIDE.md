# PolicyNest Dataset Interpretation, Hygiene & Anomaly Handling Guide

> **Engineering Guide for Joining, Filtering, and Processing Historical & Benchmark Datasets**  
> **Source:** Masters' Union Applied AI Challenge Data Pack

---

## 1. Relational Entity Architecture & Join Patterns

The PolicyNest source pack includes two distinct analytical contexts:
1. **Historical Operations Cohort (`PS-01_posp_applications.xlsx`):** Covers 3,018 real-world simulated applications spanning 9 months of operations.
2. **Calibration & Benchmark Test Set (`PS-01_document_review_test_set.xlsx`):** Covers 600 applications with 3,600 individual documents evaluated against ground truth labels.

### 1.1 Historical Cohort Join Topology
```text
applications (3,018 rows) [PK: application_id]
     │
     ├── 1:N ──> stage_events (21,188 rows) [FK: application_id]
     │
     └── N:1 ──> ops_team (22 rows) [FK: ops_reviewer_id == reviewer_id]
```

- **Joining `applications` and `stage_events`:**  
  Always join on `applications.application_id = stage_events.application_id`. Order events chronologically by `event_time ASC`.
- **Joining `applications` and `ops_team`:**  
  Left outer join on `applications.ops_reviewer_id = ops_team.reviewer_id`. Note that fully automated (STP) cases have `ops_reviewer_id IS NULL`.

### 1.2 Benchmark Test Set Join Topology
```text
application_truth (600 rows) [PK: application_id]
     │
     ├── 1:N ──> documents (3,600 rows) [FK: application_id]
     │
     └── N:1 ──> reason_codes (14 rows) [FK: decision_reasons contains reason_code]
```

- **Joining `application_truth` and `documents`:**  
  Join on `application_truth.application_id = documents.application_id`. Each application has exactly 6 documents: `PAN`, `AADHAAR_FRONT`, `AADHAAR_BACK`, `CLASS10_MARKSHEET`, `BANK_DOCUMENT`, and `SELFIE`.

---

## 2. Partitioning Real Production Data vs Synthetic Benchmarks

When building the production platform, it is non-negotiable that synthetic test data must never be mixed with live user applications:
1. **ID Namespace Isolation:**
   - Synthetic benchmark applications use ID range: `APP-26000` to `APP-26599` (600 cases).
   - Historical training applications use ID range: `APP-00001` to `APP-03018` (3,018 cases).
   - Live production user applications MUST use the namespace: `APP-LIVE-XXXXX` or UUIDv7.
2. **Database Partitioning / Filtering:**
   - Add an `is_synthetic` or `environment` boolean column (`is_synthetic = TRUE` for benchmark datasets).
   - All production dashboard queries, agent lists, and executive KPIs MUST include `WHERE is_synthetic = FALSE`.
   - Benchmark evaluation suites must filter `WHERE is_synthetic = TRUE`.

---

## 3. Data Hygiene & Anomaly Handling Rules

### 3.1 Aadhaar Masking & PII Redaction
- **The 4-Digit Mandate:** Under UIDAI regulations and DPDP Act 2023, full 12-digit Aadhaar numbers must never enter persistent storage.
- **OCR Redaction:** When processing Aadhaar front/back OCR, apply an immediate regex scrubber to replace any 12-digit sequence with `XXXX-XXXX-` followed by the last 4 digits.
- **Log Sanitation:** Ensure application loggers intercept and mask any pattern matching `\d{4}\s?\d{4}\s?\d{4}`.

### 3.2 Date of Birth Inconsistencies
- **Aadhaar Year-Only Format:** Many older Indian Aadhaar cards display only the birth year (e.g., `YYYY` instead of `DD/MM/YYYY`).
  - *Rule:* If Aadhaar displays only `YYYY`, check whether `YYYY` equals the birth year on the PAN card. If yes, treat as a **PASS**. Do not reject or request rework.
- **PAN as Golden Anchor:** When DOB conflicts arise between PAN and Class 10 marksheet, the PAN card DOB is statutory anchor for tax and age verification. Marksheet DOB differences require a single-pass clarification query (`DOB_MISMATCH`), not immediate rejection.

### 3.3 Name Variations & Indian Transliteration Patterns
- Indian names frequently exhibit regional patterns that must not be treated as identity mismatches:
  1. **Initials:** Expanding `R K SHARMA` to `RAHUL KUMAR SHARMA` is valid (Tier 2).
  2. **Token Inversion:** Swapping `SHARMA RAHUL` to `RAHUL SHARMA` is valid (Tier 3).
  3. **Middle Honorifics:** Adding/omitting `KUMAR`, `KUMARI`, `DEVI`, `PRASAD` is valid (Tier 4).
  4. **Phonetic Transliteration:** `LAKSHMI` vs `LAXMI`, `MOHAMMAD` vs `MOHAMMED` represent Tier 5 (`NAME_SPELLING_VARIANT`), which requires confirmation, not hard rejection.
  5. **Surname Change Post-Marriage:** Female applicants presenting different surnames between 10th marksheet and PAN (e.g. `PRIYA SHARMA` vs `PRIYA VERMA`) must be routed to human review for marriage certificate / gazette upload.

### 3.4 Penny-Drop Name Truncation
- Bank core banking systems frequently truncate account holder names to 20 or 24 characters or return names in abbreviated format (e.g. `S C MITTAL` for `Sachin Chand Mittal`).
  - *Rule:* Apply token-subset matching and initial expansion between the penny-drop name and PAN name. If the penny drop initials match the candidate tokens, accept as valid match.
