# IRDAI Regulatory Requirements Matrix & PolicyNest Operating Rules

This document provides the authoritative regulatory and compliance mapping for the PolicyNest AI-First POSP Onboarding Platform. It synthesises statutory mandates issued by the Insurance Regulatory and Development Authority of India (IRDAI), the Unique Identification Authority of India (UIDAI), the Income Tax Department (CBDT), and the Digital Personal Data Protection (DPDP) Act 2023 with PolicyNest's internal operational rules (Rulebook v3.2).

---

## 1. Statutory & Regulatory Foundation

The Point of Sales Person (POSP) distribution model in India is governed by the following core regulatory instruments:
1. **IRDAI Guidelines on Point of Sales Person - Life and General Insurance:**
   - Circular Ref: IRDAI/INT/GDL/ECM/044/03/2017 (and subsequent updates).
   - Allows insurance intermediaries (brokers, corporate agents) and insurers to sponsor POSPs to solicit and market pre-underwritten, simplified insurance products.
2. **IRDAI (Insurance Brokers) Regulations, 2018:**
   - Establishes broker responsibility for training, examination, KYC verification, code of conduct, and maintaining the central register of POSPs.
3. **IRDAI Central POSP Registry (IIB / Insurance Information Bureau):**
   - Mandates exclusivity: a POSP can be sponsored by and registered with only **one** life insurer/broker and **one** general insurer/broker at any given time.
4. **UIDAI Aadhaar Regulations & Section 8A of Aadhaar Act 2016:**
   - Prohibits storage of full 12-digit Aadhaar numbers in plaintext. Strict masking (storing only last 4 digits `XXXX-XXXX-1234`) is mandatory for non-banking private entities unless authorised via Aadhaar e-KYC.
5. **Digital Personal Data Protection (DPDP) Act, 2023:**
   - Mandates lawful processing based on explicit consent, purpose limitation, storage limitation, data minimization, and audit trail of data processing.

---

## 2. Regulatory Compliance & Decision Matrix

| Regulatory Dimension | IRDAI Statutory Mandate | PolicyNest Internal Standard (v3.2) | Verification Method | Pass Criteria | Defect Severity & Action | Regulatory Authority |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **Minimum Age** | Applicant must be at least 18 completed years on application date | Age >= 18 calculated against application start timestamp | Cross-checked DOB on PAN, Aadhaar, and Class 10 Marksheet | DOB indicates >= 18.00 years on application date | **REJECT (Hard)**: `UNDERAGE`. Cannot proceed. Reapplication allowed once candidate reaches 18. | IRDAI POSP Guidelines §4(a) |
| **Minimum Education** | 10th standard pass (Secondary School Certificate) from a recognized Board | 10th standard pass or higher from state boards, CBSE, CISCE, or NIOS | OCR analysis of Class 10 marksheet or certificate | Result reads `PASS` or passing grades in all compulsory subjects | **REJECT (Hard)**: `EDU_NOT_ELIGIBLE`. Marksheets from unrecognized boards rejected. | IRDAI POSP Guidelines §4(b) |
| **PAN Verification** | Individual PAN is required for tax deduction and financial integrity | PAN 4th character must be 'P' (Individual). Name & DOB treated as golden reference | Format regex: `^[A-Z]{5}[0-9]{4}[A-Z]$` with char 4 == 'P' | Valid format and individual category | **REJECT (Hard)**: `PAN_FORMAT_INVALID` or `PAN_NOT_INDIVIDUAL` (e.g. company/trust PAN). | Income Tax Act §139A & IRDAI Guidelines |
| **POSP Exclusivity** | Dual registration prohibited across same insurance category | Central register lookup via PAN against IIB / IRDAI database | Automated API query to IRDAI POSP registry | Zero active registrations found (`registry_hit == False`) | **REJECT (Hard)**: `ALREADY_REGISTERED`. Reapplication requires formal No Objection Certificate (NOC) and de-registration from previous sponsor. | IRDAI Circular 044/03/2017 §7 |
| **Identity Verification** | Reliable identity match across KYC documents | 8-tier name matching taxonomy against PAN anchor name | Deterministic string normalization, token sort, initials, and spelling distance | Tiers 1-4: Auto-Match. Tier 5: `NAME_SPELLING_VARIANT` (Rework). Tier 6: Surname change (Gazette/Marriage cert). Tier 7: Different person. | **Tier 5/6**: `NEEDS_INFO`. **Tier 7**: `REJECT` (`NAME_MISMATCH`) + Fraud Desk escalation. | IRDAI KYC Guidelines & PMLA 2002 |
| **DOB Verification** | Date of birth must be consistent across KYC documents | PAN DOB is anchor. Aadhaar and 10th marksheet must agree | Date parser supporting `DD/MM/YYYY`, `YYYY-MM-DD`, and YYYY-only | Full match, or Aadhaar year-only matches PAN birth year | **NEEDS_INFO**: `DOB_MISMATCH`. Applicant asked for affidavit or corrected document. PAN takes precedence. | IRDAI Operational Norms |
| **Address Verification** | Proof of address required for geographic licensing | Aadhaar card front & back. Address state may differ from declared state | OCR extraction of address and state | Valid residential address extracted from Aadhaar back | **INFORMATIONAL ONLY**: `ADDRESS_STATE_MISMATCH` is accepted without blocking (agents frequently migrate for work). | UIDAI / IRDAI |
| **Bank Account & Penny Drop** | Direct commission payouts must go to applicant's verified account | Account must be in applicant's own name; joint accounts accepted only if primary | Penny-drop API verification against NPCI/Bank network | Account active, name returned matches applicant name under Tier 1-4 | **NEEDS_INFO**: `BANK_NAME_MISMATCH`. Spouse/parent accounts strictly prohibited. | RBI & IRDAI Broker Regs 2018 |
| **Liveness & Biometrics** | Person submitting application must match KYC credentials | Real-time selfie compared with photo on PAN card | Computer vision face matching model (Euclidean / Cosine embedding distance) | Match score >= 0.75: Auto-Approve. 0.60 to 0.74: Human Review. < 0.60: Defect. | **Score < 0.60**: `NEEDS_INFO` (`FACE_MATCH_LOW`). Two consecutive failures: Fraud Desk referral. | IRDAI Anti-Fraud Policy |
| **Document Quality & Integrity** | KYC documents must be legible and authentic | All 4 corners visible; no blur, glare, or cropping; OCR confidence >= 0.75 | Laplacian variance (blur), edge detection (crop), luminance analysis (glare) | All quality checks passed, OCR confidence >= 0.75 | **REUPLOAD**: `IMAGE_BLURRY`, `IMAGE_CROPPED`, `IMAGE_GLARE`. One-pass consolidated notification. | IRDAI Inspection Standards |
| **Mandatory Training** | 15 hours of specified POSP training curriculum | Integrated LMS logging 15 completed hours across life, general, and health modules | System tracking of video lectures, reading modules, and time spent | Exactly >= 15.0 hours logged in LMS | **CANNOT SIT EXAM**: Training status locked until completion. | IRDAI Guidelines §5 |
| **Certification Exam** | Successful passage of POSP certification examination | Online proctored / supervised multiple choice examination | Examination engine scoring (Passing threshold e.g. 50%) | Result == `PASS` | **RE-ATTEMPT REQUIRED**: Cooldown period of 24 hours enforced before retake. | IRDAI Guidelines §6 |
| **Data Privacy & Aadhaar Masking** | Storage of raw 12-digit Aadhaar number is illegal | Full Aadhaar number must never be written to DB, logs, or UI. Masked as `XXXX-XXXX-1234` | Regex masking engine on OCR extraction; database field restricted to 4 chars | Zero plaintext Aadhaar stored | **STATUTORY PENALTY**: Non-compliance violates Aadhaar Act §29. System must reject unmasked storage. | UIDAI & DPDP Act 2023 |

---

## 3. Human vs Autonomous AI Decision Boundaries

Under IRDAI governance guidelines and PolicyNest Risk Controls, autonomous AI straight-through processing (STP) is strictly constrained:

### 3.1 Decisions Permitted for Autonomous AI (STP)
- **STP Approval:** Granted **ONLY** when:
  1. All 5 required documents present.
  2. Image quality is OK on all documents (OCR confidence >= 0.75, no blur, no glare, no crop).
  3. Age >= 18 verified across PAN, Aadhaar, 10th.
  4. Class 10 education passed from recognized board.
  5. Individual PAN format validated (`P` as 4th char).
  6. IRDAI POSP registry check returns clean (no hit).
  7. Name matching conforms strictly to Tier 1 (Exact), Tier 2 (Initials), Tier 3 (Swap), or Tier 4 (Middle Added/Missing).
  8. Bank penny-drop name matches under Tier 1-4.
  9. Face-match score >= 0.75.
- **Autonomous Rework Request (Needs Info / Reupload):** Triggered when minor defects occur (e.g. blurry image, middle initial spelling variant, penny-drop name mismatch). All defects across all 5 documents must be bundled into a **single consolidated rework notification**.

### 3.2 Decisions Reserved for Human Ops Reviewers (Human-in-the-Loop)
1. **Hard Rejection on Identity (`NAME_MISMATCH`):** AI must **NEVER** issue an autonomous hard rejection for `NAME_MISMATCH`. Any document presenting a completely different name must be routed to a Senior Ops Reviewer or Fraud Desk to prevent false accusation.
2. **Borderline Face Match (0.60 to 0.74):** Reviewed side-by-side by a human reviewer comparing lighting, angle, and age progression.
3. **Name Change After Marriage:** Requires human inspection of gazette notification or marriage certificate.
4. **Unrecognized Education Board:** Requires human verification against the Council of Boards of School Education (COBSE) directory.
5. **Two Consecutive Face-Match Failures:** Immediate escalation to Compliance / Fraud Desk.
