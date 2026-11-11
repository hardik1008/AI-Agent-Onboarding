# PolicyNest Missing Source Materials & Asset Inventory Accounting

> **Comprehensive Accounting of Provided vs Synthesized Materials**  
> **Source Pack:** Masters' Union Applied AI Challenge — PS-01 AI-First Onboarding

---

## 1. Context & Purpose of this Report

In strict compliance with non-negotiable instruction #7 ("Do not invent missing regulatory requirements or fabricate missing materials. If a requirement or material is missing, document it as missing"), this report provides a transparent accounting of all materials mentioned in the case context that were **not** provided as raw production assets in the official challenge data pack.

---

## 2. Itemized Inventory of Missing or Synthesized Assets

### 2.1 Raw Photograph Images for the 3,600 Evaluation Documents
- **Expected Asset:** 3,600 individual JPEG/PNG camera images corresponding to the rows in `documents.csv` (Sheet 1 of `PS-01_document_review_test_set.xlsx`).
- **Actual Status in Source Pack:** The challenge brief author (Vansh Miglani, InsuranceDekho) explicitly states in **Section 5 of `PS-01 Brief — AI-First Onboarding.docx`** that raw photograph files for all 3,600 documents were **deliberately not distributed**:
  > *"Because real KYC documents contain sensitive personally identifiable information, we have provided the OCR text extractions, bounding quality indicators (BLURRY, CROPPED, GLARE, OK), and confidence scores directly in the dataset, along with 12 worked synthetic cases in PS-01_specimen_documents.docx."*
- **Resolution & Mitigation:**
  1. The 12 worked specimen applications with complete OCR transcripts in `05_SPECIMEN_DOCUMENTS/PS-01_specimen_documents.docx` provide the authoritative ground truth for testing.
  2. Concrete visual specimens (`Aadhar.jpg`, `PAN.pdf`, `10TH.pdf`, `12TH.pdf`, `Profile.jpg`, `Signature.jpg`) located in the project desktop workspace have been packaged into `05_SPECIMEN_DOCUMENTS/sample_specimens/` to support UI mockup and OCR testing.

---

### 2.2 Live External API Gateways
- **Expected Asset:** Live endpoints and production credentials for:
  1. NSDL / UTIITSL PAN verification API.
  2. NPCI / Banking IMPS Penny-Drop verification API.
  3. IIB / IRDAI Central POSP Registry exclusivity lookup.
  4. UIDAI Aadhaar OTP / e-KYC service.
- **Actual Status in Source Pack:** No live government or banking API keys were provided in the academic challenge pack. Instead:
  1. The dataset provides simulated API outputs: `penny_drop_name_returned` and `irdai_posp_registry_hit` in `application_truth.csv`.
- **Resolution & Mitigation:**
  - For local development and demonstration, the new architecture must implement clean adapter interfaces (e.g. `IPennyDropAdapter`, `IIRDAIRegistryAdapter`) that read from these fields in benchmark mode and connect to real vendor endpoints (e.g. Cashfree, Karza, Bureau, or Sandbox.co.in) when live API keys are provisioned in `.env`.

---

### 2.3 Training Course Videos & LMS SCORM Packages
- **Expected Asset:** Full 15-hour video lecture files and SCORM-compliant e-learning courseware for life and general insurance modules.
- **Actual Status in Source Pack:** The challenge pack defines the mandatory 15-hour regulatory requirement and syllabus outline in Rulebook v3.2 §2, but did not distribute ~15 hours of video files.
- **Resolution & Mitigation:**
  - The LMS module should provide structured mock syllabus content, reading summaries, module completion tracking, and verifiable time logging satisfying IRDAI §5.

---

### 2.4 Proprietary InsuranceDekho Internal Databases
- **Expected Asset:** Direct access to InsuranceDekho's private production servers or real applicant records.
- **Actual Status in Source Pack:** To protect customer privacy and comply with the DPDP Act 2023, the challenge uses the synthetic company **PolicyNest Insurance Brokers** and 3,018 synthetic records.
- **Resolution & Mitigation:**
  - We strictly treat the dataset as high-fidelity synthetic benchmark data, exactly as instructed by the challenge designers.
