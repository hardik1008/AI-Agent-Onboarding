# 03. OPERATIONAL BASELINE METRICS & SIZING
**Dataset Source: `PS-01_posp_applications.xlsx` (Jan–Sep 2026, 3,018 records deduplicated)**

---

## 1. Funnel Conversion & Attrition Baseline

| Metric Dimension | Absolute Count | Percentage of Intake | Operational Commentary |
| :--- | :---: | :---: | :--- |
| **Total Inbound Starts** | **3,000** | 100.0% | Normalised intake (18 exact duplicate rows excluded from 3,018). |
| **Documents Never Uploaded** | 258 | 8.6% | Candidate drop-off between registration and initial document upload. |
| **Documents Submitted** | 2,742 | 91.4% | Applications entering ops queue. |
| **Returned for Document Rework** | 774 | 25.8% | Applications sent back to candidate for 1 or more document fixes. |
| **Lost to Rework Silence** | 211 | 7.0% | **27.3% of returned candidates** abandon and never respond. |
| **Statutorily Disqualified (Reject)** | 314 | 10.5% | Ineligible under IRDAI statutory rules (Underage, PAN entity, etc.). |
| **KYC Verified (Approved)** | 2,217 | 73.9% | Candidates successfully passing KYC and bank penny-drop. |
| **Dropped After KYC Approval** | 482 | 16.1% | **21.7% of verified candidates** never begin the 15-hour LMS training. |
| **Training Started** | 1,735 | 57.8% | Candidates entering LMS training platform. |
| **Training Completed & Exam Passed** | 1,732 | 57.7% | Candidates passing exam (160 failed attempt 1, 100% passed attempt 2). |
| **Total Certified Agents** | **1,732** | **57.7%** | Final commercial yield. Total leakage = 1,268 candidates (42.3%). |

---

## 2. Turnaround Time (TAT) & Velocity Breakdown

| Journey Milestone Segment | Median Duration | 90th Percentile (P90) | Best Quartile (Q1) | Operational Significance |
| :--- | :---: | :---: | :---: | :--- |
| **Registration → Upload** | 17.9 hours | 42.1 hours | 4.2 hours | Candidate gathering and uploading documents. |
| **Queue Wait (Upload → First Review)** | **17.3 hours** | **38.2 hours** | 8.1 hours | Pure idle backlog waiting for human reviewer availability. |
| **Active Document Review Time** | **20.7 minutes** | 31.5 minutes | 14.2 minutes | Active reviewer manual inspection across all 6 documents. |
| **Rework Round-trip Delay** | **2.2 days** | 4.8 days | 1.1 days | Time lost per sequential correction request and resubmission. |
| **KYC Verified → Training Start** | 23.3 hours | 72.0 hours | 6.5 hours | Friction in post-verification notification and LMS activation. |
| **LMS Training Duration** | 3.1 days | 6.4 days | 1.8 days | Time spent consuming 15-hour training curriculum. |
| **Exam Pass → Certificate Issuance** | 1.1 days | 2.5 days | 0.4 days | Final compliance stamping and agent code assignment. |
| **End-to-End Journey (Start → Certified)** | **8.4 days** (201.6 h) | **13.0 days** (312 h) | **6.6 days** (158 h) | Total calendar turnaround time from click to active agent. |

---

## 3. Reviewer Ops Touches & Financial Cost Sizing

* **Reviewer Headcount**: 22 dedicated full-time reviewers across 2 daily shifts.
* **Total Human Review Actions**: 9,920 recorded touches (average **3.3 touches per application**).
* **Loaded Reviewer Hourly Wage**: ₹430/hour average (Base: ₹380/h; Senior: ₹520/h).
* **Cost per Clean Application**: ~₹148 (20.6 min at ₹430/h).
* **Cost per Reworked Application**: ~₹495 (3.3 touches × 21 min at ₹430/h).
* **9-Month Operational Reviewer Spend**:
  * *First-touch only baseline*: ₹4.1 Lakhs (20.7 min × 3,000 apps at ₹430/h).
  * *Full repeat-touch actual*: **₹14.7 Lakhs** (9,920 touches × ₹148/touch).
