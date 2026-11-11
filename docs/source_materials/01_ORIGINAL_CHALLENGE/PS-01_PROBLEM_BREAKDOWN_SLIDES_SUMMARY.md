# PS-01 PROBLEM BREAKDOWN — 8-SLIDE EXECUTIVE PRESENTATION
**Original Source: `PS-01_Problem_Breakdown_8slides.pptx`**
**Problem Owner: Vansh Miglani, InsuranceDekho**
**Case Company: PolicyNest Insurance Brokers (Fictional)**

---

## Executive Overview
The 8-slide deck represents the foundational strategic and analytical breakdown of the POSP agent onboarding bottleneck at PolicyNest Insurance Brokers. It establishes the quantitative evidence base, the process timeline, root causes, solution scope, North Star metrics, risk boundaries, and executive questions for the problem owner.

---

## Slide-by-Slide Transcription & Analysis

### Slide 1: The Funnel — 42% Leakage
* **Headline**: *42 of every 100 applicants never become agents. They don't fail the exam; they leak out of onboarding before it.*
* **Funnel Breakdown (Jan–Sep 2026)**:
  * **3,000 Applications Started**: Baseline intake (~330/month across 14 states).
  * **−258 Never Uploaded Documents (8.6%)**: Lost before review started.
  * **−314 Rejected on Eligibility (10.5%)**: Failed statutory criteria (Underage, PAN format/entity, Class 10th fail, IRDAI duplicate hit).
  * **−211 No Reply to Fix Request (27.3% of returned)**: Dropped out after receiving sequential rework requests.
  * **−482 Verified, Never Started Training (21.7% of verified)**: Cleared KYC successfully but dropped out before LMS training.
  * **−3 Still in Progress**: Active at snapshot date (30 Sep 2026).
  * **1,732 Certified Agents (57.7%)**: Total yield.
* **Key Takeaway**: 469 applicants (37% of all loss) leak specifically in the document review stage. Nobody drops out at the exam (160 failed once and 100% passed on retry). This proves onboarding friction, not exam difficulty, is the structural bottleneck.

---

### Slide 2: Today's Process — 98% Idle Waiting Time
* **Headline**: *Today's journey takes a median of 8.4 days. In the review zone, 98% of the time is idle waiting: 17.3 h in queue for a ~20-minute check.*
* **Process Step Durations**:
  1. **Apply & Upload**: 17.9 hours (start → docs submitted); 258 drop out (8.6%).
  2. **Wait in Queue**: 17.3 hours median (P90 38.2 hours). Identical backlog at all hours and weekdays.
  3. **Reviewer Checks**: ~21 minutes of actual manual touch time; 314 rejected (10.5%).
  4. **One Fix at a Time**: ~2.2 days per rework cycle; 211 never reply (27.3%).
  5. **KYC to Training Hand-off**: 23.3 hours median wait; 482 never start training (21.7%).
  6. **Training & Exam**: 4.2 days combined median duration.
* **Key Takeaway**: A clean application spends 0.7 days in the review zone; a returned application spends 3.3 days. The queue wait is identical on weekdays and weekends, proving a structural standing backlog rather than staffing shifts.

---

### Slide 3: Sizing Numbers — Volume, Rework & Costs
* **Headline**: *Sizing: ~330 applications a month, 1 in 4 bounces back, and up to ₹15 L of reviewer time goes into touching every file 3.3 times.*
* **Core Metrics**:
  * **3,000 Applications**: Jan–Sep 2026.
  * **57.7% Certified**: 1,732 agents.
  * **25.8% Returned for Fix**: 774 applications, 849 total return events.
  * **211 Lost to Silence**: 27.3% of applicants who received a fix request.
  * **8.4 Days Median TAT**: P90 13.0 days; top quartile 6.6 days.
  * **17.3 Hours Queue**: P90 38.2 hours; P95 47.1 hours.
  * **₹4.1L – ₹14.7L Reviewer Cost**: ₹4.1L for initial review; up to ₹14.7L across all repeat touches.
  * **9,920 Human Touches**: 3.3 average touches per application across the 22-person ops team.
* **Key Takeaway**: Returned applications represent only 26% of volume but consume 37% of reviewer touches and cause 37% of candidate losses.

---

### Slide 4: Four Mutually Exclusive Root Causes
* **Headline**: *Four root causes, no overlaps: three sit inside the document check, and the fourth is a hand-off that AI can trigger.*
* **RC1: Errors Found Late & Asked One-at-a-Time**:
  * 71 applications looped 2–3 times; ~2.2 days added per loop.
  * Returned files drop out at **42.6% vs 18.4%** for clean files (2.3× higher drop-out).
  * *Fix*: Consolidate all defects into a single, multi-lingual follow-up.
* **RC2: Most Issues are Detectable at Upload**:
  * Out of 849 return events: Blur = 423, Name = 130, DOB = 115.
  * **79% of all defects** could be caught instantly on the applicant's phone before submission.
  * *Fix*: Real-time edge quality gate and pre-screening at upload.
* **RC3: Reviewer Effort is Flat, Not Aimed at Judgement**:
  * Reviewers spend 20.6 minutes on clean files vs 20.9 minutes on hard files.
  * 61% of files are clean approvals requiring zero human judgement.
  * *Fix*: Straight-Through Processing (STP) for clean files; route only hard cases to humans.
* **RC4: Hand-off Leaks After KYC**:
  * 482 verified applicants never start training (51% of all drop-outs). Only 52% start within 24 hours.
  * *Fix*: Trigger instantaneous training activation SMS/WhatsApp deep link the second KYC completes.

---

### Slide 5: Solution Scope — AI Automation vs Human Responsibility
* **Headline**: *Scope: AI decides ~90% of files and starts before the first photo is taken. People keep the calls the rulebook reserves for them.*
* **AI Automated Scope (~90% of Volume)**:
  * **Step 0 Pre-Screening**: Catches 174 of 314 rejections (55%: Registry = 75, PAN format/entity = 50, Age = 49) before document upload.
  * **Quality Gating at Upload**: Blur, glare, and cropping detection.
  * **Cross-Document Field Extraction**: Name, DOB, PAN, Class 10th pass, bank account match.
  * **Consolidated Multi-lingual Message**: Single follow-up in English or Hindi.
  * **Automated Hand-off**: Instant training activation.
* **Human-in-the-Loop Scope (~10% of Volume)**:
  * **Rejections for Different Person Name**: Mandatory human confirmation; never auto-reject.
  * **Borderline Face-match Scores (0.60 – 0.75)**: Human reviewer comparison.
  * **Unrecognised Education Boards**: Discretionary evaluation.
  * **Surname Changes after Marriage**: Marriage certificate/gazette review.
  * **Disputed Outcomes & Low AI Confidence**: Escalations desk.
* **Out of Scope**:
  * Authoring the 15-hour training course or exam content.
  * Direct UIDAI Aadhaar biometrics or real core banking integrations (simulated with partner specs).
  * Fraud prosecution beyond internal escalation.
  * Storing or displaying full 12-digit Aadhaar numbers.

---

### Slide 6: North Star Metric & Economic Value
* **Headline**: *Success: 6 in 10 files decided in minutes with no human touch, without letting a single ineligible agent through.*
* **North Star Metric**:
  * **Straight-Through Processing (STP) Rate**: 0% → **≥ 60%**.
  * **Compliance Guardrail**: Recall on REJECT **≥ 98%**. Missing an ineligible candidate is an unacceptable regulatory breach.
* **Economic & Operational Impact**:
  * **Median Time to Certificate**: 8.4 days → **6.9 days** with AI review alone; → **5.7 days** with instant training activation.
  * **Reviewer Time**: 21 minutes → **< 5 minutes** averaged across all applications.
  * **Agent Retention**: Eliminating sequential rework silence recovers **~105 additional certified agents (+6% yield)**.

---

### Slide 7: Critical Operational Risks & Guardrails
* **Headline**: *The biggest risk is a confident wrong approval, and the data shows exactly where it would hide.*
* **Key Risks & Mitigations**:
  * **False Approval Compliance Breach**: Governed by strict rulebook gating, dual-threshold confidence filters, and 98% reject recall guardrail.
  * **Reviewer Ground-Truth Noise**: 2.5% of human document verdicts in the test set are incorrect. Algorithms must be validated against `application_truth.final_decision`, not human verdicts.
  * **Fairness Across Demographics**: Verify zero performance disparity across genders, states, and name structures.
  * **Data Privacy (DPDP Act 2023)**: Mandatory 8-digit masking of Aadhaar numbers.

---

### Slide 8: Six Hypotheses & Questions for Vansh Miglani
* **Headline**: *Six questions for Vansh Miglani. Each one tests a hypothesis the data raised but cannot settle.*
  1. *What error rate on auto-approvals would compliance sign off, and who signs?* (Sets the STP ceiling; reviewers run at 97.5% today).
  2. *Why does a 20-minute check wait 17 hours: staffing, batching or SLA design?* (Queue wait is invariant across all hours and weekdays).
  3. *Are registry and penny-drop checks run before or after review, and what does each call cost?* (22 of 60 rejections depend on them).
  4. *Can we send a training link the moment KYC clears?* (482 verified agents drop out; only 52% start within 24 hours).
  5. *Can the pilot pull documents from DigiLocker instead of photos?* (49.8% of returns are image-quality defects).
  6. *Which region would you pilot in, and should applicants be told an AI decided?* (State certification rates vary from 53% to 65%).

---
## Raw Slide Dump Reference
```text
=== SLIDE 1 ===
  The problem
  Today's process
  Sizing numbers
  Root causes
  Scope
  Success metric
  Risks
  Owner questions
  42 of every 100 applicants never become agents. They don't fail the exam; they leak out of onboarding before it
  3,000
  Applications started
  −258
  Never uploaded documents
  −314
  Rejected on eligibility
  −211
  No reply to fix request
  −482
  Verified, never started training
  −3
  Still in progress
  1,732
  Certified agents
  Red = leak in the document stage (469, 37% of all loss)
  Reading the funnel
  1,268 lost = 469 in the document stage + 482 after KYC + 314 rejected on eligibility (+3 still in progress).
  Nobody is lost at the exam: 160 failed once and all of them passed on a retry.
  27.3% of applicants asked to fix a document never reply (211 of 774).
  83% of rejections apply a fixed rule, yet still wait 17.7 h for a reviewer.
  So what  Certification sits at 53–63% in every month, Jan–Sep. This is a structural process problem, not a seasonal dip. Every lost applicant is premium that never gets written.
  Source: applications sheet (status, rejection_reason), stage_events (AUTO_EXPIRED notes), monthly_funnel; 18 duplicate rows removed
  1

=== SLIDE 2 ===
  The problem
  Today's process
  Sizing numbers
  Root causes
  Scope
  Success metric
  Risks
  Owner questions
  Today's journey takes a median of 8.4 days. In the review zone, 98% of the time is idle waiting: 17.3 h in queue for a ~20-minute check
  DOCUMENT-REVIEW ZONE · what AI can own
  Apply and upload
  17.9 h
  start → docs
  258 never upload (8.6%)
  Wait in queue
  17.3 h
  P90 38.2 h
  Same wait at any hour or weekday
  Reviewer checks
  ~21 min
  of actual work
  314 rejected (10.5%)
  One fix at a time
  ~2.2 days
  per loop
  211 never reply (27.3%)
  KYC, then training
  23.3 h
  to start training
  482 never start (21.7%)
  Training and exam
  4.2 days
  median, combined
  Out of scope
  So what  A clean file spends 0.7 days in the review zone; a returned file spends 3.3. The wait is the same at every hour and on every weekday, so this is a standing backlog, not an off-hours gap.
  Source: stage_events: medians between first occurrences of each event per application; certified cohort for 'review zone' (DOCS_SUBMITTED → KYC_VERIFIED)
  2

=== SLIDE 3 ===
  The problem
  Today's process
  Sizing numbers
  Root causes
  Scope
  Success metric
  Risks
  Owner questions
  Sizing: ~330 applications a month, 1 in 4 bounces back, and up to ₹15 L of reviewer time goes into touching every file 3.3 times
  3,000
  applications, Jan–Sep 2026
  ≈ 330 a month across 14 states
  57.7%
  certified
  1,732 agents; 31.7% dropped, 10.5% rejected
  25.8%
  returned for a fix
  774 applications, 849 return events
  211
  agents lost to silence
  27.3% of applicants who got a fix request
  8.4 days
  median to certificate
  P90 13.0 days; best quartile 6.6 days
  17.3 h
  queue before first look
  P90 38.2 h; P95 47.1 h
  ₹4–15 L
  reviewer cost, 9 months
  ₹4.1 L first review; ≤ ₹14.7 L if every touch were a full review
  9,920
  human touches (3.3 per file)
  Returned files: 26% of volume, 37% of touches
  So what  Cost is real, but the bigger prize is people: 469 lost in the document stage and 482 after KYC. Each one is premium that never gets written.
  Source: applications (manual_touches, hours_to_certify), stage_events, ops_team (weighted loaded cost ₹430/h), test set reviewer_minutes (mean 20.7 per application)
  3

=== SLIDE 4 ===
  The problem
  Today's process
  Sizing numbers
  Root causes
  Scope
  Success metric
  Risks
  Owner questions
  Four root causes, no overlaps: three sit inside the document check, and the fourth is a hand-off that AI can trigger
  Why do 42% of applicants fail to certify, and why does it take 8.4 days?
  RC1
  Errors found late, asked one at a time
  71 files looped 2–3×; ~2.2 days per loop; returned files drop out 42.6% vs 18.4%
  2.3×
  drop-out
  AI can fix
  RC2
  Most issues are detectable at upload
  Of 849 return events: blur 423, name 130, DOB 115. Caught only after a 17-hour queue
  79%
  detectable
  AI can fix
  RC3
  Effort is flat, not aimed at judgement
  20.6 min clean vs 20.9 min hard; 61% clean approvals; 79 good approvals have legit name variants
  21 min
  every file
  AI can fix
  RC4
  Hand-off leaks after KYC
  482 verified never start training (half of all drop-outs); only 52% start within 24 h
  482
  lost
  AI can nudge
  So what  RC1–RC3 are fixed by checking at upload, asking once, and routing only judgement calls to people. RC4 is fixed by sending a training link the moment KYC clears.
  Source: stage_events (DOC_RETURNED notes, KYC_VERIFIED → TRAINING_STARTED), test set reviewer_minutes by is_hard_case and final_decision
  4

=== SLIDE 5 ===
  The problem
  Today's process
  Sizing numbers
  Root causes
  Scope
  Success metric
  Risks
  Owner questions
  Scope: AI decides ~90% of files and starts before the first photo is taken. People keep the calls the rulebook reserves for them
  AI decides
  end to end, with every rule cited
  60.7% + 29.3%
  of test-set files are APPROVE or NEEDS MORE INFO
  Step 0: registry, PAN and age on typed details
  Quality gate at upload (blur, glare)
  Read and cross-check names and DOB
  Class 10 pass; penny-drop name match
  One fix message, English or Hindi
  Training link the moment KYC clears
  AI recommends, human confirms
  evidence laid out side by side
  ≈ 2%
  of test files (12 different-person names) + Human-only rules
  REJECT for a different person's name (never auto-reject)
  Borderline face-match scores (e.g. 0.68)
  Any decision the rulebook marks Human only
  Cases where AI confidence is low
  Reviewer copilot: evidence side by side; target 21 → < 5 min per file
  Out of scope
  for this challenge
  Building the 15-hour training or the exam
  Real Aadhaar e-KYC, penny-drop or IRDAI calls (we use data-pack values)
  Fraud investigation beyond flagging
  Storing or showing full Aadhaar numbers
  So what  Step 0 catches 174 of 314 rejections (55%: registry 75, PAN 50, age 49) from typed details, before anyone photographs a document. Age is re-confirmed against the documents.
  Source: test set application_truth.final_decision (364 / 176 / 60), name_match_category = DIFFERENT (12); applications.rejection_reason; PS-01 brief §3, §8
  5

=== SLIDE 6 ===
  The problem
  Today's process
  Sizing numbers
  Root causes
  Scope
  Success metric
  Risks
  Owner questions
  Success: 6 in 10 files decided in minutes with no human touch, without letting a single ineligible agent through
  NORTH STAR
  Straight-through rate
  Share of applications decided correctly with no human touch
  0%  →  ≥60%
  Why 60% is realistic: 60.7% of test-set files are true approvals.
  Guardrail: REJECT recall ≥98%. Missing one is a compliance breach.
  What this is worth (our simulation on today's data)
  Median to certificate: 8.4 → 6.9 days with AI review alone; → 5.7 days if training also starts within an hour of KYC. Training to certificate takes 4.7 days, which is the floor. Silence at 10% keeps ~105 more agents (+6%).
  Source: PS-01 brief §7 targets; baselines from applications, stage_events and test set. Simulation: certified journeys with DOCS_SUBMITTED → KYC_VERIFIED set to 10 min; 134 fewer non-responders × 78.9% downstream certification
  6

=== SLIDE 7 ===
  The problem
  Today's process
  Sizing numbers
  Root causes
  Scope
  Success metric
  Risks
  Owner questions
  The biggest risk is a confident wrong approval, and the data shows exactly where it would hide
  So what  Also, 2.5% of reviewer document verdicts are wrong. We will score the engine against ground truth, not against reviewers, or we will copy their mistakes.
  Source: Test set: application_truth vs roll-up of document human_verdict; documents.ocr_confidence by image_quality; applications by state; PS-01 brief §8
  7

=== SLIDE 8 ===
  The problem
  Today's process
  Sizing numbers
  Root causes
  Scope
  Success metric
  Risks
  Owner questions
  Six questions for Vansh Miglani. Each one tests a hypothesis the data raised but cannot settle
  QUESTION
  WHY WE ASK (EVIDENCE)
  1
  What error rate on auto-approvals would compliance sign off, and who signs?
  Sets the straight-through ceiling. Reviewers run at 97.5% on documents today.
  2
  Why does a 20-minute check wait 17 hours: staffing, batching or SLA design?
  The wait is identical at every hour and on every weekday.
  3
  Are registry and penny-drop checks run before or after review, and what does each call cost?
  22 of 60 rejections depend on them; rejections take 17.7 h.
  4
  Can we send a training link the moment KYC clears?
  482 verified agents never start: half of all drop-outs. Only 52% start within 24 h.
  5
  Can the pilot pull documents from DigiLocker instead of photos?
  Half of all returns (49.8%) are image-quality problems.
  6
  Which region would you pilot in, and should applicants be told an AI decided?
  Certification varies 53–65% by state; 27% go silent after a request.
  Red = must answer before we fix targets. They decide how much the engine may do on its own.
  Source: Team analysis of PS-01 data pack; question list builds on PS-01 brief §10
  8


```
