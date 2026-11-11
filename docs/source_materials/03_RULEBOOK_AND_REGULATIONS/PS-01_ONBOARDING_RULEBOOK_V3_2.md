# PolicyNest POSP Onboarding Rulebook v3.2

> **Operating Standard** — PolicyNest Insurance Brokers (Fictional)  
> **Effective Date:** 1 April 2026  
> **Source:** Masters' Union Applied AI Challenge (PS-01 AI-First Onboarding)

---

## Notice

**SYNTHETIC DATASET NOTICE:** This document is the exact operating standard developed for the Masters' Union Applied AI Challenge. Names, identifiers, numbers, and events described are synthetic. Eligibility rules follow the published IRDAI framework for Point of Sales Persons (POSP). Where PolicyNest applies a stricter internal rule, it is marked **Internal**.

---

PS-01 · DATA PACK

PolicyNest Insurance Brokers (fictional) · Onboarding Ops standard v3.2 · effective 1 April 2026

## 1. Purpose and scope

This rulebook is the operating standard PolicyNest's Onboarding Ops team uses to decide whether a person can be certified as a Point of Sales Person (POSP) for general and life insurance. It covers eligibility, the documents we collect, how each document is checked, how mismatches between documents are resolved, when to ask the applicant for more information and when to reject. It is written for human reviewers today. Your product should apply the same rules, explain each decision in these terms, and leave the decisions marked Human only to a person.

Eligibility rules in section 2 follow the published IRDAI framework for POSPs. Where PolicyNest applies a stricter internal rule, it is marked Internal. Students should check the current IRDAI text themselves before treating any rule as regulatory.

## 2. Eligibility

| Rule | Requirement | Evidence | If not met |
| --- | --- | --- | --- |
| Age | 18 years or older on the date the application is started | DOB on PAN; cross-checked with Aadhaar and Class 10 marksheet | REJECT — UNDERAGE |
| Education | Passed Class 10 (secondary) from a recognised board, including NIOS | Class 10 marksheet or certificate showing PASS | REJECT — EDU_NOT_ELIGIBLE |
| Identity | Valid individual PAN (4th character P) | PAN card | REJECT — PAN_FORMAT_INVALID or PAN_NOT_INDIVIDUAL |
| Exclusivity | Not already registered as a POSP with another insurer or intermediary | IRDAI POSP registry lookup on PAN | REJECT — ALREADY_REGISTERED (applicant may reapply after a no-objection certificate) |
| Training | Complete 15 hours of POSP training | Training platform log | Cannot sit exam |
| Examination | Pass the POSP examination | Exam result | Re-attempt allowed after 24 hours |
| Bank account | Savings or current account in the applicant's own name, for commission | Cancelled cheque or bank statement + penny-drop | NEEDS_INFO — BANK_NAME_MISMATCH |

## 3. Documents we collect

PAN card — the anchor document. Name and date of birth on the PAN are treated as the reference values for every other check.

Aadhaar, front and back — identity and address. Only the last four digits of the Aadhaar number are ever stored; any image showing all twelve digits must be masked before storage.

Class 10 marksheet or certificate — education eligibility and a second source for name and DOB.

Cancelled cheque or the first page of a bank statement — account holder name, IFSC and account number for commission payouts.

Selfie — a live photo compared with the PAN photo by the face-match service. Scores are from 0 to 1.

Optional: GST certificate (for agents above the GST threshold), address proof if the current address differs from Aadhaar.

## 4. Per-document acceptance criteria

### 4.1 Image quality (all documents)

All four corners visible. If a corner or edge field is missing: REUPLOAD — IMAGE_CROPPED.

Every field legible at normal zoom. If any required field cannot be read with confidence: REUPLOAD — IMAGE_BLURRY.

No reflection covering a field. If a reflection hides a field: REUPLOAD — IMAGE_GLARE.

A photocopy or a photo of a screen is accepted only for the bank document; for identity documents ask for a photo of the original (Internal).

OCR confidence below 0.75 should be treated as a likely quality problem and checked, not trusted.

### 4.2 PAN

Format: five letters, four digits, one letter (AAAAA9999A). Anything else: REJECT — PAN_FORMAT_INVALID.

The 4th character shows the holder type. Only P (individual) is eligible. C (company), F (firm), H (HUF), T (trust) and others: REJECT — PAN_NOT_INDIVIDUAL.

The 5th character is normally the first letter of the holder's surname. A mismatch is not by itself a reason to reject, but should raise attention when combined with other inconsistencies.

The PAN typed by the applicant must equal the PAN on the card. A single-character difference is usually a typing error: correct it from the card and log the correction.

### 4.3 Aadhaar

Store only the last four digits. Never write the full number to any system, log or prompt.

Name must match the PAN under the name-matching rules in section 5.

DOB must equal the PAN DOB. Some older Aadhaar cards show only the year of birth; a year-only value that matches the PAN year is acceptable.

The address state may differ from the declared state — agents often work away from home. This is informational and never a reason to reject.

### 4.4 Class 10 marksheet

Result must read PASS (or show passing marks in every compulsory subject where no result line exists).

Accept any state board, CBSE, CISCE or NIOS. Marksheets from boards not on the recognised list are Human only.

Name must match the PAN under section 5. A spelling difference here is common because marksheets are older than PAN cards.

DOB on the marksheet should match the PAN. If they differ, the PAN is treated as correct only if the Aadhaar agrees with the PAN; otherwise NEEDS_INFO — DOB_MISMATCH.

### 4.5 Bank document

The account must be in the applicant's own name. Joint accounts are accepted if the applicant is the first holder.

IFSC format: four letters, a zero, six alphanumeric characters.

The penny-drop check returns the account holder name from the bank. It must match the PAN name under section 5. If it does not: NEEDS_INFO — BANK_NAME_MISMATCH.

A spouse's or parent's account is never accepted, whatever the explanation.

### 4.6 Selfie

Face-match score ≥ 0.75: accept.

0.60–0.75: Human only — a reviewer compares the photos.

Below 0.60: NEEDS_INFO — FACE_MATCH_LOW. Ask for a fresh selfie in good light. Two failures in a row go to the fraud desk.

## 5. Name matching — the rules that cause most rework

Indian names appear in many legitimate forms across documents issued years apart. Reviewers spend more time on names than on anything else, and they disagree with each other more often on names than on anything else. The rules below are how a decision should be made.

| Pattern | Example (PAN → other document) | Decision |
| --- | --- | --- |
| Exact (ignoring case and spacing) | RAHUL KUMAR SHARMA → Rahul Kumar Sharma | Match |
| Initials for given or middle names | RAHUL KUMAR SHARMA → R K SHARMA | Match |
| Order swapped | RAHUL KUMAR SHARMA → SHARMA RAHUL KUMAR | Match |
| Middle name missing | RAHUL KUMAR SHARMA → RAHUL SHARMA | Match |
| Middle name added | PRIYA SHARMA → PRIYA KUMARI SHARMA | Match |
| Spelling variant of the same name | MOHAMMAD ASIF → MOHAMMED ASIF; LAKSHMI → LAXMI | NEEDS_INFO — NAME_SPELLING_VARIANT |
| Surname changed after marriage | PRIYA SHARMA → PRIYA VERMA | NEEDS_INFO — ask for marriage certificate or gazette notification (Human only) |
| Different person | RAHUL KUMAR SHARMA → ANKIT YADAV | REJECT — NAME_MISMATCH; flag to fraud desk |

When in doubt between a spelling variant and a different person, prefer NEEDS_INFO and route to a human. A wrongful rejection costs us a good agent; a wrongful approval of a different person is a compliance breach.

## 6. Making the application-level decision

Collect every document-level finding.

If any finding is a REJECT reason, the application is REJECT. Give every reason, not only the first.

Otherwise, if any finding is a NEEDS_INFO or REUPLOAD reason, the application is NEEDS_MORE_INFO. Ask for everything that is needed in a single message — today's process asks one thing at a time, and each round trip adds about two days.

Otherwise the application is APPROVE and moves to training.

Informational findings (address state differs, PAN 5th character unusual) are recorded but never change the decision on their own.

## 7. Service levels and escalation

| Step | Target | Escalate to |
| --- | --- | --- |
| First review after documents submitted | 4 working hours | Team lead after 8 hours |
| Review after re-upload | 2 working hours | Team lead after 4 hours |
| Fraud desk referral (different person, two face-match failures) | Same day | Compliance officer |
| Applicant query by phone or WhatsApp | 1 working hour | Team lead |

## 8. Messages to applicants

Messages go out by WhatsApp and SMS in English or Hindi. They must say exactly what is wrong, what to send, and how. They must never mention fraud, never show another person's data and never include a full PAN or Aadhaar number.

Re-upload: "Your Class 10 marksheet photo is blurry, so we could not read your date of birth. Please take a new photo in daylight with all four corners visible and upload it here: <link>."

Bank name mismatch: "The bank account you shared is not in your name. Commission can only be paid into your own account. Please upload a cancelled cheque or statement for an account in your name."

Spelling variant: "Your name is spelt differently on your PAN (MOHAMMAD) and marksheet (MOHAMMED). Please upload either a corrected document or a signed declaration in the attached format."

Rejection (underage): "You must be 18 or older to register. You can apply again from <date>."

## 9. Decisions that stay with a human

Any REJECT for NAME_MISMATCH (a different person) — the system may recommend, a person confirms.

Face-match scores between 0.60 and 0.75.

Marksheets from boards not on the recognised list.

Surname changes after marriage.

Any case the applicant disputes.

## 10. What good looks like

A reviewer who follows this rulebook well decides a clean application in under five minutes and asks for everything missing in one message. The best reviewers on the team certify agents in under three days end to end. The team average is far slower, mainly because of one-at-a-time document requests and queue waiting, not because any single check is hard.
