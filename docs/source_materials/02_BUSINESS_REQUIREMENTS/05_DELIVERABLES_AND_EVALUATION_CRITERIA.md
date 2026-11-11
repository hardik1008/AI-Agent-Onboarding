# 05. DELIVERABLES & EVALUATION CRITERIA

---

## 1. Required Engineering Deliverables

### Core Deliverables (Must Have):
1. **Document Understanding Engine**:
   Multimodal OCR & extraction pipeline extracting Name, DOB, ID number, and statutory fields with per-field confidence scores across all 6 documents.
2. **Cross-Document Rulebook Reasoner**:
   Deterministic and probabilistic reasoning engine implementing the 12 sections of Rulebook v3.2 (name matching, DOB agreement, PAN format/holder, 10th pass, bank match, face match).
3. **Application Decision Output**:
   Final application-level verdict matching the three official outcomes (`APPROVE`, `NEEDS_MORE_INFO`, `REJECT`) with every reason code explicitly cited.
4. **Single Consolidated Follow-up Generator**:
   Single aggregated message in English and Hindi addressing all detected defects in a single dispatch.
5. **Human-in-the-Loop Reviewer Routing**:
   Automated routing queue for hard cases and human-only conditions, presenting evidence side by side.
6. **Full 600-Case Evaluation Benchmark Report**:
   Quantitative evaluation report on `PS-01_document_review_test_set.xlsx` reporting overall accuracy, confusion matrix, and precision/recall.
7. **Deployable Web Interfaces**:
   Functional interfaces for both the applicant (mobile-first upload and status) and the ops reviewer (copilot cockpit).

### Extended Deliverables (Should Have & Stretch):
* Re-processing delta engine (re-evaluates only replaced documents).
* Candidate conversational interface (WhatsApp/SMS simulator).
* MeriPehchaan DigiLocker OAuth 2.0 integration with fallback.
* Immutable audit trail logging (actor, rule, timestamp, model version).

---

## 2. Formal Evaluation Rubric & Scoring Weights

| Category | Weight | Evaluation Criteria |
| :--- | :---: | :--- |
| **1. Business Understanding & Opportunity Sizing** | **20%** | Depth of analysis on the 3,000-application dataset; rigorous identification of root causes; realistic before/after operational simulation. |
| **2. Decision Engine Accuracy & Rigour** | **30%** | Accuracy against `application_truth.final_decision` on all 600 cases; REJECT recall ≥ 98%; handling of 8-tier name taxonomy and complex edge cases. |
| **3. Product Design & User Experience** | **25%** | Candidate portal usability; reviewer cockpit ergonomics (side-by-side evidence, diffs); quality of consolidated follow-up messages. |
| **4. Technical Architecture & Compliance** | **15%** | Architectural modularity; DPDP Act 2023 compliance (Aadhaar masking); explainability; deterministic rule engine vs ML boundaries. |
| **5. Executive Presentation & Defence** | **10%** | Quality of executive narrative; clarity on consultant slide decks; defence against tough judge questions. |
