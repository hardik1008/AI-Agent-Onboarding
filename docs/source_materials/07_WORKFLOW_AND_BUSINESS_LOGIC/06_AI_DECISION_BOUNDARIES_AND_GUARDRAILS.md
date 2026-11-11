# AI Decision Boundaries, Safety Guardrails & Compliance Governance

> **Engineering Specification for Safe Autonomous AI Deployment in Financial Onboarding**  
> **Statutory Alignment:** IRDAI Governance, PMLA 2002, DPDP Act 2023

---

## 1. Autonomous STP Thresholds & Safety Bounds

To ensure regulatory compliance and eliminate wrongful disqualifications, autonomous AI Straight-Through Processing (STP) is governed by strict mathematical confidence bounds:

| Evaluation Dimension | Autonomous STP Approval Threshold | Human Escalation Trigger | Autonomous Hard Rejection Permitted? |
| :--- | :--- | :--- | :--- |
| **OCR Document Legibility** | Confidence $\ge 0.75$ across all required fields | Confidence $< 0.75$ on any required field | **NO** (Triggers `REUPLOAD`, never rejection) |
| **Identity Name Match** | Tiers 1 to 4 (Exact, Initial, Swap, Middle Add) | Tier 5 (Spelling) or Tier 6 (Marriage) | **STRICTLY FORBIDDEN** (Tier 7 must be verified by human) |
| **Date of Birth** | Exact match or Aadhaar year matching PAN birth year | Full conflict between PAN and 10th marksheet | **NO** (Triggers `NEEDS_MORE_INFO`) |
| **Bank Account Holder** | Penny-drop name matches candidate under Tiers 1–4 | Penny-drop name differs | **NO** (Triggers `NEEDS_MORE_INFO` for personal cheque) |
| **Biometric Face Match** | Cosine similarity score $\ge 0.75$ | Score between $0.60$ and $0.74$ | **NO** (Score $< 0.60$ triggers retry; 2nd failure to Fraud Desk) |
| **Age Requirement** | Calculated age $\ge 18.00$ years | Age between $17.95$ and $18.00$ | **YES** (Only if unambiguous proof of age $< 18$) |
| **Class 10 Education** | Recognized Board with explicit `PASS` | Unlisted Board / Missing Pass status | **NO** (Unlisted board routed to Human Reviewer) |
| **IRDAI Exclusivity** | Central Registry returns clean (`hit == False`) | Central Registry returns match (`hit == True`) | **YES** (Statutory exclusivity rule) |

---

## 2. Digital Personal Data Protection (DPDP) Act 2023 Safeguards

1. **Purpose Limitation:** Applicant KYC documents and facial embeddings are processed solely for POSP certification and regulatory reporting to IRDAI. Secondary use is strictly prohibited.
2. **Storage Limitation & Encryption:**
   - Document images stored with AES-256 server-side encryption.
   - Presigned S3/storage URLs expire after 15 minutes.
   - Aadhaar numbers strictly masked to last 4 digits (`XXXX-XXXX-1234`) across all relational storage and cache layers.
3. **Audit Trail & Non-Repudiation:**
   - Every autonomous decision logs the exact model version, feature vector, OCR bounding boxes, and timestamp in immutable event logs.
   - Human reviewer overrides are captured with mandatory reviewer justification notes.
