# 02. POSP ONBOARDING PROCESS — CURRENT STATE SPECIFICATION

---

## 1. End-to-End Journey Map (7 Operational Stages)

```
[Stage 0: Registration] ──> [Stage 1: Document Upload] ──> [Stage 2: Queue Wait] ──> [Stage 3: Reviewer Check]
        │                                                                                     │
        ▼ (8.6% drop)                                                                         ▼
   (258 dropouts)                                                                     [Fix Loop ~2.2d]
                                                                                              │ (27.3% drop)
                                                                                              ▼
[Stage 6: Certification] <── [Stage 5: Exam & License] <── [Stage 4: 15h LMS] <── [KYC Verified]
```

### Detailed Stage Breakdown:

| Stage # | Stage Name | Actor | Description | Median Duration | Drop-off / Attrition |
| :---: | :--- | :--- | :--- | :---: | :--- |
| **0** | **Applicant Registration** | Candidate | Applicant initiates application via Agent App, Website, or Field Referral. Enters declared name, DOB, PAN, mobile, state, and bank IFSC. | 0 h | Typing errors common; zero real-time pre-flight validation. |
| **1** | **Document Upload** | Candidate | Applicant photographs and uploads 6 statutory files: PAN, Aadhaar Front, Aadhaar Back, Class 10th Marksheet, Cancelled Cheque, and Live Selfie. | 17.9 h (start → upload) | **258 candidates (8.6%)** never upload and auto-expire after 7 days. |
| **2** | **Ops Review Queue** | System | Application enters shared unassigned queue for the 22-person Gurugram Onboarding Ops team. | **17.3 h** (P90: 38.2 h) | Pure idle waiting time; 98% of total review stage duration. |
| **3** | **Manual Reviewer Check** | Reviewer | Ops reviewer manually inspects all 6 documents side by side: compares names, checks DOBs, verifies PASS status on marksheet, checks PAN holder type 'P', and reviews face-match score. | **~21 minutes** of active work | **314 rejected (10.5%)** on statutory eligibility; 2.5% reviewer error rate. |
| **4** | **Rework & Correction Loop** | Reviewer & Candidate | If defects are identified (blur, name mismatch, bank name), reviewer dispatches a manual WhatsApp/SMS requesting a fix. | **~2.2 days** per cycle | **211 candidates (27.3%)** go silent after receiving request and abandon application. |
| **5** | **Penny-Drop & KYC Complete** | System & Reviewer | System triggers ₹1 penny-drop to bank account. Account holder name is confirmed against PAN. Ops marks KYC Verified. | 0.5 h | Hand-off delay: Candidate must wait for batch LMS sync. |
| **6** | **LMS Training (15 Hours)** | Candidate | Candidate completes mandatory 15-hour regulatory training modules covering general and life insurance fundamentals. | 23.3 h to start; 3.1 days duration | **482 candidates (21.7%)** clear KYC but never start training course. |
| **7** | **Regulatory Exam & Certification** | Candidate & System | Candidate completes 20-question statutory online exam. Passing threshold is 50% (10/20). Upon passing, official POSP certificate and unique agent code are issued. | 1.1 days (exam → cert) | **160 failed once; 100% passed on retry.** Zero terminal leakage at exam stage. |

---

## 2. Reviewer Operations & Staffing Model
* **Team Structure**: 22 full-time Onboarding Ops reviewers operating in 2 shifts (09:00–18:00 and 13:00–22:00) divided into regional sub-teams (North, South, West, East).
* **Work Allocation**: Shared FIFO queue with manual pulling. No automated routing based on case complexity or reviewer seniority.
* **Touch Intensity**: Average of **3.3 human actions per application** (9,920 total reviewer touches across 3,000 applications).
* **Cost Structure**: Reviewer loaded hourly wage averages **₹430/hour** (range: ₹380 to ₹520/hour including overheads). Total loaded reviewer expenditure: **₹14.7 Lakhs** over 9 months.
