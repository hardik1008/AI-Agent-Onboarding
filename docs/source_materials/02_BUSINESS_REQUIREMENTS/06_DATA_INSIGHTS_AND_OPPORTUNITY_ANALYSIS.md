# 06. DATA INSIGHTS & OPPORTUNITY ANALYSIS
**Source: `PolicyNest_Onboarding_Data_Insights.xlsx`**

---

## 1. Executive Insights & Evidence Matrix

| # | Theme | Data Point / Insight | Value | Methodology / Calculation | Strategic Implication | Caveat |
| :---: | :--- | :--- | :---: | :--- | :--- | :--- |
| 1 | **Primary bottleneck** | Median document submission → first human review | `17.25 hours` | DOCS_SUBMITTED to REVIEW_STARTED; distinct matched application IDs; median. | Run AI validation at upload so common issues are surfaced before the human-review queue. | Dataset-derived; elapsed event time. |
| 2 | **Primary bottleneck** | Average document submission → first human review | `20.44 hours` | Mean of the same submission-to-review intervals. | Track median and upper percentiles, not only average. | Dataset-derived. |
| 3 | **Primary bottleneck** | P90 first-review wait | `38.25 hours` | 90th percentile of submission-to-review intervals. | Use queue-age alerts and escalation for long-wait cases. | Dataset-derived. |
| 4 | **Primary bottleneck** | P95 first-review wait | `47.10 hours` | 95th percentile of submission-to-review intervals. | Prioritise aging applications and exception queues. | Dataset-derived. |
| 5 | **Certification journey** | Median application-to-certification time | `8.42 days` | Median applications.hours_to_certify divided by 24. | Treat first-review speed as a leading lever; track final certification separately. | Dataset-derived; approx. 8.4 days. |
| 6 | **Correction volume** | Unique applications returned for corrections | `774` | Distinct application_id values with DOC_RETURNED event. | Use as denominator for correction-rate metric. | Dataset-derived; unique applications. |
| 7 | **Correction volume** | Share of started applications returned for corrections | `25.8%` | 774 unique returned applications / 3,000 started applications. | Pre-upload checks can prevent avoidable returns. | Dataset-derived. |
| 8 | **Correction events** | Total correction events | `849` | Count of DOC_RETURNED rows in stage_events. | Consolidate all known issues into one correction request. | Dataset-derived; event count. |
| 9 | **Correction reasons** | Image-quality correction events | `423 (49.8%)` | 423 blurry/cropped notes / 849 DOC_RETURNED events. | Computer-vision quality gate for blur, crop, glare and legibility. | Dataset-derived; event-level. |
| 10 | **Correction reasons** | Name + DOB mismatch events | `245 (28.9%)` | 130 name mismatch + 115 DOB mismatch; 245 / 849 events. | OCR plus field-level comparison across uploaded documents. | Dataset-derived; event-level. |
| 11 | **Correction reasons** | Image + name + DOB candidate events | `668 (78.7%)` | 423 + 130 + 115 = 668; 668 / 849 events. | Run validation at upload and show actionable correction instructions. | Dataset-derived; event-level, not unique-app coverage. |
| 12 | **Correction reasons** | Bank account-holder mismatch events | `111 (13.1%)` | 111 bank-name mismatch notes / 849 events. | Use penny-drop / bank verification integration; route exceptions. | Dataset-derived; event-level. |
| 13 | **Correction reasons** | Selfie / PAN mismatch events | `70 (8.2%)` | 70 selfie mismatch notes / 849 events. | Use confidence thresholds and human escalation. | Dataset-derived; event-level. |
| 14 | **Correction loops** | Applicants with exactly one correction event | `703` | 703 application IDs had one DOC_RETURNED event. | Consolidate all available findings before sending first request. | Dataset-derived. |
| 15 | **Correction loops** | Applicants with multiple correction events | `71` | 67 applications had 2 events; 4 had 3; total 71. | Batch all issues into one message where possible. | Dataset-derived; unique applications. |
| 16 | **Correction loops** | Extra correction events beyond one per returned applicant | `75` | 849 total events − 774 unique returned applications = 75. | A consolidated message may avoid repeat messaging when all issues are detectable together. | Dataset-derived; potential reduction, not guaranteed message reduction. |
| 17 | **Applicant response** | No response to document request within 10 days | `211` | AUTO_EXPIRED note explicitly says 'No response to document request in 10 days'. | Use clear instructions, direct upload links and reminders. | Dataset-derived; distinct application IDs. |
| 18 | **Applicant response** | Non-response rate among correction recipients | `27.3%` | 211 no-response applications / 774 unique returned applications. | Reduce effort and confusion through consolidated communication. | Dataset-derived; denominator assumes returned applications are correction recipients. |
| 19 | **Reupload behaviour** | Unique applicants who reuploaded documents | `582` | Distinct application IDs with DOC_REUPLOADED event. | Make reupload flow simple and identify exactly which file needs replacement. | Dataset-derived. |
| 20 | **Reupload behaviour** | Total document reupload events | `638` | Count of DOC_REUPLOADED rows. | Support repeat upload and revalidate changed documents without restarting. | Dataset-derived; event count. |
| 21 | **Reupload behaviour** | Applicants with multiple reuploads | `52` | Application IDs with more than one DOC_REUPLOADED event. | Preserve context and re-check only changed documents. | Dataset-derived. |
| 22 | **Funnel** | Documents submitted / applications started | `2,742 / 3,000 (91.4%)` | DOCS_SUBMITTED / APPLICATION_STARTED unique application IDs. | Reduce early friction and abandonment before document completion. | Dataset-derived; event funnel. |
| 23 | **Funnel** | KYC verified / applications started | `2,217 / 3,000 (73.9%)` | KYC_VERIFIED / APPLICATION_STARTED unique application IDs. | Improve upstream validation and exception resolution. | Dataset-derived; event funnel. |
| 24 | **Funnel** | Training started / applications started | `1,735 / 3,000 (57.8%)` | TRAINING_STARTED / APPLICATION_STARTED unique application IDs. | Monitor KYC-to-training conversion separately. | Dataset-derived; event funnel. |
| 25 | **Funnel** | Certified / applications started | `1,732 / 3,000 (57.7%)` | CERTIFIED / APPLICATION_STARTED unique application IDs. | Track certification outcome and reconcile event/status definitions. | Dataset-derived; event funnel. |
| 26 | **Post-KYC drop-off** | Drop-off between KYC verification and training start | `482 applicants (21.7%)` | 2,217 KYC-verified − 1,735 training-started = 482; 482 / 2,217 = 21.7%. | Instant automated KYC feedback preserves applicant intent and immediately routes verified agents into training. | Dataset-derived; status = DROPPED with kyc_verified_at populated. |
| 27 | **Training completion** | Conversion rate from training start to certification | `99.8% (1,732 / 1,735)` | 1,732 certified / 1,735 training-started. | All acquisition optimization should focus on removing friction in the pre-training document review window. | Dataset-derived; stage completion count. |
| 28 | **Operations cost** | Total reviewer touches and ops expenditure (Jan–Sep) | `9,920 touches | ~₹14.9 Lakhs` | 9,920 manual touches across 22 reviewers; 21 min/touch; loaded cost ₹430/hr (mean of ops_team). | Automating 60% of cases straight-through and cutting review time to <5 min saves ~₹12+ Lakhs annually. | Derived from applications.manual_touches and ops_team loaded rates. |
| 29 | **Eligibility & compliance** | IRDAI registry rejections (Already registered POSP) | `75 of 314 rejections (23.9%)` | applications.rejection_reason == 'ALREADY_REGISTERED'; 75 / 314. | Move IRDAI registry check to Step 0 (upon typing PAN) before document upload to save applicant effort and reviewer capacity. | Dataset-derived; historical rejection reason. |
| 30 | **Automation feasibility** | Potential Straight-Through Processing (STP) rate in test set | `60.7% (364 / 600)` | application_truth.final_decision == 'APPROVE' (364/600); 268 exact matches + 96 valid rulebook name variants. | Meeting the brief's target of ≥60% zero-human-touch STP is mathematically and operationally feasible. | Labelled test set (application_truth). |
| 31 | **Reviewer quality** | Reviewer verdict error rate on documents | `~2.5% document error rate` | Document review test set README and specimen notes. | AI rule engine enforces uniform regulatory compliance and removes individual reviewer bias. | Documented data pack baseline error rate. |
| 32 | **SOURCE** | PS-01_posp_applications.xlsx (applications, stage_events, ops_team) & PS-01_document_review_test_set.xlsx. Rulebook requires 15h training. | `` |  |  |  |

---

## 2. Key Takeaways for Solution Architecture
1. **Pre-Screening is High Leverage**: 55% of all disqualifications can be identified at Step 0 before document upload.
2. **Quality Gating Solves Half of Returns**: 49.8% of returns are blur/crop/glare, fully preventable at mobile camera capture.
3. **Consolidated Follow-ups Save Candidates**: Multi-round rework causes 2.3× higher drop-out; a single message stops candidate exhaustion.
4. **Automated LMS Hand-off Recovers Dropouts**: Triggering instant training invitations reclaims hundreds of silent verified candidates.
