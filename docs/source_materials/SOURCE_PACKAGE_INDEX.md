# PolicyNest Source Materials Package: Master Manifest & Architecture Index

> **Official Repository of Business Requirements, Challenge Artifacts, Raw Datasets, Regulatory Specifications & Reference Guides**  
> **Prepared for:** Commercial-Grade Clean-Slate Platform Build  
> **Case Challenge:** Masters' Union Applied AI Challenge — PS-01 AI-First Onboarding  
> **Problem Owner:** Vansh Miglani, InsuranceDekho  
> **Case Company:** PolicyNest Insurance Brokers (Fictional)  
> **Package Generation Date:** November 9, 2026

---

## 1. Executive Summary & Package Mission

This standalone package consolidates and organizes **100% of the authentic source requirements, raw empirical datasets, regulatory rulebooks, specimen documents, and strategic reference materials** for PolicyNest. 

It is completely decoupled from any legacy codebase, prototype scripts, or temporary database files. It serves as the definitive single source of truth for bootstrapping a commercial-grade, multi-persona AI-First POSP Onboarding Platform.

---

## 2. Directory Hierarchy & File Manifest

```text
POLICYNEST_SOURCE_PACKAGE/
├── 01_ORIGINAL_CHALLENGE/                 # Challenge brief, problem slides & transcripts
├── 02_BUSINESS_REQUIREMENTS/               # Problem statement, process flows, KPIs, and opportunities
├── 03_RULEBOOK_AND_REGULATIONS/            # Rulebook v3.2 (.docx & .md) and Regulatory Matrix
├── 04_DATASETS/                            # 8 raw datasets (.xlsx & .csv) and validation report
├── 05_SPECIMEN_DOCUMENTS/                  # Specimen applications, defect taxonomy & sample files
├── 06_DATA_DICTIONARY/                     # Entity dictionary, column rules & KPI formulations
├── 07_WORKFLOW_AND_BUSINESS_LOGIC/         # Decision engine, name matching, FSM, rework & cockpit specs
├── 08_REFERENCE_MATERIALS/                 # The 47-page PS-01 Bible (.pdf & .md) and IRDAI framework
├── SOURCE_PACKAGE_INDEX.md                 # Master manifest and bootstrapping guide (this file)
└── MISSING_SOURCE_MATERIALS.md             # Transparent accounting of unprovided raw assets
```

---

## 3. Detailed File Catalog by Section

### Section 01: Original Challenge Brief & Presentation
| Filename | Format | Size | Purpose & Core Content |
| :--- | :--- | :--- | :--- |
| `PS-01 Brief — AI-First Onboarding.docx` | Word (.docx) | 25.9 KB | Official problem statement brief provided by Masters' Union & InsuranceDekho. |
| `PS-01_CHALLENGE_BRIEF.md` | Markdown | 22.5 KB | Complete verbatim markdown transcription of the challenge brief, deliverables, and rules. |
| `PS-01_Problem_Breakdown_8slides.pptx` | PowerPoint | 57.3 KB | The original 8-slide executive pitch deck structured using Barbara Minto's Pyramid Principle. |
| `PS-01_PROBLEM_BREAKDOWN_SLIDES_SUMMARY.md` | Markdown | 18.7 KB | Full textual transcript of all 8 slides, speaker notes, data backing, and action titles. |

### Section 02: Business Requirements & Operational Baselines
| Filename | Format | Size | Purpose & Core Content |
| :--- | :--- | :--- | :--- |
| `01_BUSINESS_PROBLEM_STATEMENT.md` | Markdown | 4.2 KB | Business problem, core operational thesis, and strategic objectives. |
| `02_POSP_ONBOARDING_PROCESS_CURRENT_STATE.md` | Markdown | 4.0 KB | Granular current-state process mapping, queue bottlenecks, and leakage points. |
| `03_OPERATIONAL_BASELINE_METRICS.md` | Markdown | 3.6 KB | Empirical baseline numbers: 17h wait, 2.2-day rework, 33.2% drop-off, ₹1,450 unit cost. |
| `04_BUSINESS_OBJECTIVES_AND_SUCCESS_METRICS.md` | Markdown | 2.9 KB | Target benchmarks: >= 60% STP, >= 75% FPY, <= 24h TAT, 98% reject recall. |
| `05_DELIVERABLES_AND_EVALUATION_CRITERIA.md` | Markdown | 2.8 KB | Evaluation rubric, scoring criteria, and required platform deliverables. |
| `06_DATA_INSIGHTS_AND_OPPORTUNITY_ANALYSIS.md` | Markdown | 9.2 KB | Deep-dive quantitative insights synthesized from historical operations. |
| `PolicyNest_Onboarding_Data_Insights.xlsx` | Excel (.xlsx) | 16.1 KB | Source workbook containing executive insights, problem-to-solution mappings, and definitions. |
| `executive_insights.csv` | CSV | 9.8 KB | Exported data insights table from workbook. |
| `problem_to_solution.csv` | CSV | 4.2 KB | Problem-to-solution matrix mapping operational leaks to AI interventions. |
| `definitions_and_caveats.csv` | CSV | 3.7 KB | Operational definitions, edge-case caveats, and assumptions. |

### Section 03: Rulebook & Statutory Regulations
| Filename | Format | Size | Purpose & Core Content |
| :--- | :--- | :--- | :--- |
| `PS-01_onboarding_rulebook.docx` | Word (.docx) | 18.3 KB | Original operating standard document (PolicyNest Ops Standard v3.2). |
| `PS-01_ONBOARDING_RULEBOOK_V3_2.md` | Markdown | 10.6 KB | Clean, verbatim markdown conversion with all 3 regulatory and operational tables. |
| `REGULATORY_REQUIREMENTS_MATRIX.md` | Markdown | 9.5 KB | Comprehensive statutory matrix: IRDAI Guidelines, UIDAI masking, PMLA, DPDP Act 2023. |

### Section 04: Raw Datasets & Benchmarks
| Filename | Format | Records | Purpose & Schema Overview |
| :--- | :--- | :--- | :--- |
| `PS-01_posp_applications.xlsx` | Excel (.xlsx) | 4 sheets | Master historical operational workbook (3,018 applications, 21,188 events). |
| `PS-01_document_review_test_set.xlsx` | Excel (.xlsx) | 3 sheets | Master evaluation workbook (600 applications, 3,600 documents, 14 reason codes). |
| `applications.csv` | CSV | 3,018 rows | 27 columns: full historical applicant demographic, KYC, and milestone log. |
| `stage_events.csv` | CSV | 21,188 rows | 5 columns: complete event-sourcing audit trail of all lifecycle events. |
| `ops_team.csv` | CSV | 22 rows | 7 columns: operations reviewer roster, tenure, shifts, speed, and loaded hourly cost. |
| `monthly_funnel.csv` | CSV | 9 rows | 8 columns: monthly operational metrics from Jan 2026 to Sep 2026. |
| `documents.csv` | CSV | 3,600 rows | 13 columns: test set documents with OCR text, confidence, and reviewer verdicts. |
| `application_truth.csv` | CSV | 600 rows | 12 columns: ground truth benchmark decisions, reason codes, and name patterns. |
| `reason_codes.csv` | CSV | 14 rows | 3 columns: official IRDAI defect taxonomy and verdict classifications. |
| `DATASET_SCHEMA_AND_VALIDATION_REPORT.md` | Markdown | 15.1 KB | In-depth technical report on schemas, nullability, referential integrity, and distributions. |

### Section 05: Specimen Documents & Defect Taxonomy
| Filename | Format | Size | Purpose & Core Content |
| :--- | :--- | :--- | :--- |
| `PS-01_specimen_documents.docx` | Word (.docx) | 20.7 KB | Official challenge document containing the 12 worked specimen applications. |
| `SPECIMEN_APPLICATIONS_VERBATIM.md` | Markdown | 17.7 KB | Complete markdown transcription of all 12 specimens, tables, OCR texts, and verdicts. |
| `SPECIMEN_DEFECT_TAXONOMY_GUIDE.md` | Markdown | 5.1 KB | Engineering guide detailing failure modes, computer vision indicators, and rework rules. |
| `sample_specimens/Aadhar.jpg` | Image (JPG) | 101.6 KB | Concrete visual specimen of Aadhaar card for UI rendering and OCR calibration. |
| `sample_specimens/PAN.pdf` | PDF Document | 174.5 KB | Concrete visual specimen of PAN card. |
| `sample_specimens/10TH.pdf` | PDF Document | 91.3 KB | Concrete visual specimen of Class 10 Secondary Education Marksheet. |
| `sample_specimens/12TH.pdf` | PDF Document | 124.9 KB | Concrete visual specimen of Class 12 Higher Secondary Certificate. |
| `sample_specimens/Profile.jpg` | Image (JPG) | 30.9 KB | Concrete visual specimen of applicant photo / selfie. |
| `sample_specimens/Signature.jpg` | Image (JPG) | 25.2 KB | Concrete visual specimen of applicant specimen signature. |
| `sample_specimens/ananya_pan.jpg` | Image (JPG) | 71.3 KB | Additional sample PAN card specimen. |
| `sample_specimens/pan_card.jpg` | Image (JPG) | 10.5 KB | Additional sample PAN card specimen. |

### Section 06: Data Dictionary & Interpretation Guide
| Filename | Format | Size | Purpose & Core Content |
| :--- | :--- | :--- | :--- |
| `COMPLETE_DATA_DICTIONARY.md` | Markdown | 16.1 KB | Detailed dictionary for all 7 entities, 88 attributes, allowed values, and 6 KPI formulas. |
| `DATASET_INTERPRETATION_GUIDE.md` | Markdown | 5.2 KB | Anomaly handling, Aadhaar masking, date formatting, and relational join patterns. |

### Section 07: Workflows & Business Logic Specifications
| Filename | Format | Size | Purpose & Core Content |
| :--- | :--- | :--- | :--- |
| `01_POLICY_ENGINE_SPECIFICATION.md` | Markdown | 5.3 KB | Deterministic decision hierarchy, multi-issue aggregation, and conflict resolution. |
| `02_NAME_MATCHING_AND_IDENTITY_TAXONOMY.md` | Markdown | 4.2 KB | The 8-tier name matching algorithm, token sorting, phonetic distance, and guardrails. |
| `03_APPLICATION_LIFECYCLE_STATE_MACHINE.md` | Markdown | 3.7 KB | FSM specification, valid transitions, Mermaid state diagram, and timeout rules. |
| `04_CONSOLIDATED_REWORK_ENGINE.md` | Markdown | 5.5 KB | Single-pass rework logic, bi-lingual templates (English/Hindi), and deep-link design. |
| `05_OPS_REVIEWER_COCKPIT_SPECIFICATION.md` | Markdown | 4.3 KB | Reviewer cockpit UX, split-screen grid, visual diffing, and keyboard accelerators. |
| `06_AI_DECISION_BOUNDARIES_AND_GUARDRAILS.md` | Markdown | 2.8 KB | Safety bounds: zero autonomous identity rejections, 98% reject recall, DPDP Act 2023. |
| `07_FRONTEND_REQUIREMENTS_SPECIFICATION.md` | Markdown | 2.9 KB | Multi-persona UI specifications for Applicant Portal, Cockpit, and Executive Dashboard. |

### Section 08: Reference Materials & Regulatory Framework
| Filename | Format | Size | Purpose & Core Content |
| :--- | :--- | :--- | :--- |
| `PS-01_Bible.pdf` | PDF (47 pages) | 2.27 MB | The original 47-page master guide covering every number, slide, and calculation. |
| `PS-01_BIBLE_COMPREHENSIVE_GUIDE.md` | Markdown | 11.7 KB | Complete textual synthesis of the Bible, including all Tough Questions & Answers. |
| `IRDAI_REGULATORY_FRAMEWORK_REFERENCE.md` | Markdown | 5.8 KB | Statutory guide on POSP circulars, permitted products, 15h training, and exclusivity. |

---

## 4. Bootstrapping Instructions for the New Platform

When initiating development in the new repository:
1. **Unpack Source Archive:** Extract `POLICYNEST_SOURCE_PACKAGE.zip` into the project root under `/docs/source_materials/`.
2. **Database Initialization:** Populate SQLite/PostgreSQL tables using the clean CSV files in `04_DATASETS/`. Ensure `is_synthetic = TRUE` is assigned to benchmark records (`APP-26000` to `APP-26599`).
3. **Calibrate Policy Engine:** Implement the deterministic decision hierarchy from `07_WORKFLOW_AND_BUSINESS_LOGIC/01_POLICY_ENGINE_SPECIFICATION.md` and test against the 600 ground-truth cases in `application_truth.csv`. Verify that benchmark accuracy exceeds 98% on true rejections.
4. **Implement Name Matching:** Encode the 8-tier algorithm specified in `07_WORKFLOW_AND_BUSINESS_LOGIC/02_NAME_MATCHING_AND_IDENTITY_TAXONOMY.md` to ensure Tiers 1–4 are automatically matched without human intervention.
5. **Enforce Single-Pass Rework:** Integrate the bi-lingual notification templates from `07_WORKFLOW_AND_BUSINESS_LOGIC/04_CONSOLIDATED_REWORK_ENGINE.md` so that multiple defects across documents are never fragmented into separate messages.
