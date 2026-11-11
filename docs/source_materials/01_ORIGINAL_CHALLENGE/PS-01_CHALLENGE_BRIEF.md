# PS-01 BRIEF — AI-FIRST ONBOARDING

APPLIED AI CHALLENGE · PROBLEM STATEMENT

PS-01 · An onboarding journey where AI reads the documents and does the work

Redesign agent onboarding so that AI reasons through every document, decides what it can, asks for everything missing in one go, and leaves people only the judgement calls.

The problem was set by Vansh Miglani, InsuranceDekho. The data pack describes PolicyNest Insurance Brokers, a fictional company modelled on this problem. All data is synthetic and generated to protect privacy: it does not represent the customers, employees, operations or figures of InsuranceDekho or any other real company.


## 1. At a glance


## 2. The problem

Insurance in India is sold largely through intermediaries, and the Point of Sales Person is the fastest-growing of them: a part-time agent, often a shopkeeper, mechanic or homemaker, who sells simple products after 15 hours of training and an exam. For a broker like PolicyNest, every month an agent spends stuck in onboarding is a month of premium that never gets written. Between January and September 2026, 3,000 people started an application. Only 1,732 (57.7%) were certified; 951 (31.7%) dropped out and 314 (10.5%) were rejected.

The journey is slow. A certified agent takes a median of 8.4 days from starting the application to receiving a certificate, and one in ten takes 13 days or more. The best quartile gets through in 6.6 days, which shows that the steps themselves are not the bottleneck. Applications wait a median of 17.3 hours in a queue before a reviewer opens them. When a document has a problem, the reviewer asks for one fix at a time, and each round trip adds roughly two days.

The work is repetitive but not trivial. A reviewer spends about 21 minutes on the documents of a single application, checking that the name and date of birth agree across PAN, Aadhaar, the Class 10 marksheet and a cancelled cheque. Names are the hardest part: initials, swapped order, a missing middle name and spelling variants such as Mohammad and Mohammed are all common and mostly legitimate. Reviewers disagree on these cases, and about 2.5% of their document-level verdicts in the test set are simply wrong.

The same pattern repeats across financial services. Loan customers, merchants, distributors and agents are all onboarded through a document-heavy journey designed around a human checker. The problem owner's question is whether AI can reason through the documents itself and complete most of the onboarding steps, so that people only handle the cases that genuinely need judgement.

How POSP onboarding works today

Applicant starts on the agent app, the website or through a field partner and types in personal, education and bank details — typing errors are common and never checked against documents.

Applicant uploads photos of PAN, Aadhaar (front and back), Class 10 marksheet, a cancelled cheque and a selfie — 8.6% never upload anything and expire after 7 days.

The application waits in a shared queue — median 17.3 hours, 90th percentile 38 hours.

A reviewer reads each document, compares names and dates by eye, checks PAN format and the face-match score — about 21 minutes per application.

If anything is wrong, the reviewer sends a WhatsApp message asking for one fix — 25.8% of applications are returned at least once, and 27% of those applicants never reply.

Once verified, a penny-drop confirms the bank account and the applicant is sent to the 15-hour training — 22% of verified applicants never start it.

The applicant completes training, passes the POSP exam and is certified — median 8.4 days from start, with 3.3 human touches per application.

The numbers

All figures are computed from the synthetic data pack for this problem.

Why now

Multimodal and long-context models can now read a photographed document, extract fields and reason across several documents in one pass at a cost of a few rupees per application. Government rails such as DigiLocker let applicants share verified documents directly. Together these make a different design possible: instead of a person checking a pile of photos, an agent can do the checking, explain its decision in the rulebook's own terms, and talk to the applicant until the file is complete. The competition for good part-time agents is intense, and the broker that certifies an agent in two days instead of eight keeps that agent.


## 3. The challenge

Build an AI-first onboarding product for POSP agents. It should take an application and its uploaded documents, extract and cross-check every field, apply the onboarding rulebook, and reach a decision — approve, needs more information, or reject — with every reason stated. When something is missing or wrong, it should ask the applicant for everything in one clear message and re-check what comes back. Decisions the rulebook reserves for a person must be routed to a reviewer with the evidence laid out. Measure your product against the labelled test set and show what it would do to time-to-certificate and drop-off.


### Must have

Document reading: extract name, date of birth, ID number and other required fields from each document's OCR text (or from images you capture yourself), with a confidence for each field.

Cross-document checks: name matching under the rulebook's rules, DOB agreement, PAN format and holder type, education result, bank-account ownership and face-match thresholds.

An application-level decision with every reason listed, matching the rulebook's three outcomes.

One consolidated follow-up message to the applicant listing everything needed, in English or Hindi.

Human routing for the decisions the rulebook marks Human only, with the evidence shown side by side.

An evaluation report on the 600-application test set: overall accuracy, and precision and recall for REJECT and NEEDS_MORE_INFO.

A working interface a reviewer and an applicant can each use, deployed at a public URL.

Should have

Re-processing of a re-uploaded document without re-checking everything else.

A reviewer dashboard showing the queue, what the AI decided, and where it was unsure.

An audit trail recording every decision, the rule behind it and the model version.

A simulation using the applications workbook of what your product would do to time-to-certificate and drop-off.

Stretch

A conversational onboarding flow on WhatsApp that collects documents and answers applicant questions.

Pulling verified documents through DigiLocker instead of photos, with a fallback when the applicant cannot.

Generalising the engine to a second journey, such as onboarding a loan customer, by swapping the rulebook.

Out of scope

Building the 15-hour training course or the exam.

Real Aadhaar e-KYC, real penny-drop or real IRDAI registry calls — use the values in the data pack.

Fraud investigation beyond flagging a case to a human.

Storing or displaying full Aadhaar numbers in any form.


## 4. Who you are building for


## 5. Your data pack

Four files. Start with the rulebook, because it defines what a correct decision is. Then read the specimen documents to see real cases end to end. Use the applications workbook to understand today's process and size the opportunity, and the test set to build and measure your engine. Every workbook opens with a README sheet listing the sheets, a data dictionary and the deliberate data-quality issues.

Before you start

Images are not included. OCR text stands in for each image and is corrupted where the image was poor, as it would be in production. To work with real images, use a public identity-document dataset (see Readings) or capture specimen documents your team creates yourselves — never real people's documents.

Judge your engine against application_truth.final_decision, not against the document-level human_verdict: about 2.5% of reviewer verdicts are deliberately wrong.

The applications sheet contains 18 duplicate rows, upper-case city names and blank channels. Clean before you analyse.

Penny-drop names, IRDAI registry hits and face-match scores are provided as fields. Treat them as the outputs of external services your product would call.


## 6. How your product will be tested

Your product should pass these scenarios by the final demo. Use them as acceptance tests from Stage 2 onwards; reviewers will run some of them live.


## 7. How success is measured


## 8. Guardrails and constraints

Follow the Digital Personal Data Protection Act, 2023: collect only what onboarding needs, state the purpose, and never send full Aadhaar numbers to any model, log or prompt.

No real people's documents. Use the synthetic data, a public dataset, or specimen documents your team creates.

The AI recommends; a human confirms every rejection for NAME_MISMATCH and every decision the rulebook marks Human only.

Every decision must cite the rule it applied. A decision you cannot explain is not a decision.

Prefer NEEDS_MORE_INFO over REJECT when unsure. A wrongful approval is a breach; a wrongful rejection loses a good agent. Both count.

Check that your engine performs equally well across states, genders and name patterns, and report any gap.

Messages to applicants must never mention fraud or show another person's data.


## 9. Suggested build path

Three stages. Treat each as the minimum you should be able to show at that point in the challenge.

Stage 1 — Understand and scope

Know the process, the rules and the data well enough to say exactly what you will automate.

A process map of today's journey built from stage_events, with time and drop-off at each step.

20 test applications decided by hand by your team, including at least 8 hard cases.

The decisions your product will make and the ones it will route to a human.

A first business case: hours and drop-offs saved if your product hits its targets.

Answers from your problem-owner meeting.

Stage 2 — Working product

An end-to-end engine that decides real test cases and can be used by a reviewer and an applicant.

Extraction and cross-checks running on all 600 test applications.

A first evaluation report: accuracy and per-class precision and recall.

The consolidated follow-up message working for multi-issue cases.

A reviewer view for routed cases, deployed at a public URL.

A list of the ten cases your engine gets most wrong and why.

Stage 3 — Tested and adopted

Proof that people can use it and that it would change the numbers.

Accuracy at or near target, with a fairness check across states, genders and name patterns.

Usability tests with at least five people playing applicants and two playing reviewers.

A before/after simulation of time-to-certificate and drop-off on the applications data.

An audit trail a compliance officer could read.

A clear statement of what still needs a human, and why.

10. Questions to take to your problem owner

You will meet the problem owner. Go in with these, and add your own once you have explored the data.

Which onboarding journey costs InsuranceDekho the most today — agents, customers or partners — and why?

Where do your reviewers disagree with each other most often, and how is that resolved?

What error rate would compliance accept for an automated approval, and who would sign it off?

Which external checks (DigiLocker, penny-drop, registry lookups) do you already use, and what do they cost per call?

At which step do you lose the most applicants, and what do you believe causes it?

Would applicants trust a decision made by an AI, and should they be told?

What does a reviewer's day look like, and what would they want an AI to take off them first?

How would you measure success for a pilot in one region?

What would stop you from putting a product like this into production?

11. Readings and resources

What is POSP certificate and how to become a certified POSP  —  InsuranceDekho

https://www.insurancedekho.com/news/what-is-posp-certificate-how-to-become-a-certified-posp-112

The problem owner's own explainer of the POSP role and certification steps.

Point of Sales Persons: an alternate distribution channel for insurers  —  Cyril Amarchand Mangaldas (corporate law blog)

https://corporate.cyrilamarchandblogs.com/2022/09/point-of-sales-persons-an-alternate-distribution-channel-for-insurers/

A clear legal overview of the IRDAI framework for POSPs: eligibility, training and what they may sell.

The Digital Personal Data Protection Act, 2023 (full text)  —  India Code, Government of India

https://www.indiacode.nic.in/bitstream/123456789/22037/2/a2023-22.pdf

The law your product must respect when it collects and processes identity documents.

Amendment to Master Direction on KYC (video-based customer identification)  —  Reserve Bank of India

https://website.rbi.org.in/web/rbi/-/notifications/amendment-to-master-direction-md-on-kyc-11783

How the financial regulator allows digital and video-based KYC — useful if you generalise to loan customers.

DigiLocker Authorized Partner API Specification  —  DigiLocker, Government of India

https://img1.digitallocker.gov.in/assets/img/Digital%20Locker%20Authorized%20Partner%20API%20Specification%20v1.11.pdf

How a company can pull verified documents with the user's consent instead of reading photos.

Document Intelligence model overview (including the ID document model)  —  Microsoft Learn

https://learn.microsoft.com/en-us/azure/ai-services/document-intelligence/model-overview

What off-the-shelf document AI already extracts, so you can decide what to build and what to buy.

MIDV-500: a dataset for identity document analysis on mobile devices  —  arXiv

https://arxiv.org/abs/1807.05786v4

A public dataset of synthetic identity documents captured on phones — use it to test real image handling.

12. Glossary



# BRIEF TABLES

### Table 1

| Problem owner | Vansh Miglani, InsuranceDekho |
| --- | --- |
| Domain | Insurance · Distribution operations · Document AI |
| Case company | PolicyNest Insurance Brokers (fictional). A Gurugram-based insurance broker that sells motor, health and life insurance through a network of about 14,000 Point of Sales Persons (POSPs) across 14 states. A 22-person Onboarding Ops team reviews every new agent's documents before they can be trained, examined and certified. |

### Table 2

| Who it's for | New POSP agents signing up from their phones, and the Onboarding Ops reviewers who check their documents today. |
| --- | --- |
| What you'll build | An AI onboarding agent that reads uploaded documents, checks them against each other and the rulebook, decides approve / needs more info / reject with reasons, asks the applicant for everything missing in one message, and routes judgement calls to a human. |
| Core AI capabilities | Document understanding (OCR + LLM extraction), cross-document reasoning, rule application with explanations, conversational follow-up in English and Hindi, human-in-the-loop routing. |
| Data you get | 3,000 applications with full stage timestamps, a 21,000-row event log, a labelled test set of 600 applications and 3,600 documents with OCR text, the 10-section onboarding rulebook, and 12 worked specimen cases. |
| What makes it hard | Indian names appear in many legitimate forms; OCR is noisy; some reviewer labels are wrong; and a wrongful approval is a compliance breach while a wrongful rejection loses a good agent. |
| What a win looks like | Most clean applications decided in minutes with no human touch, every follow-up asked in a single message, and accuracy on the test set that a compliance head would sign off. |

### Table 3

| Metric | Value | What it means |
| --- | --- | --- |
| Applications started (Jan–Sep 2026) | 3,000 | About 330 a month across 14 states. |
| Certified | 57.7% | 1,732 agents. The rest dropped out (31.7%) or were rejected (10.5%). |
| Median time to certificate | 8.4 days | 90th percentile 13.0 days; best quartile 6.6 days. |
| Queue wait before first review | 17.3 hours | Median. The 90th percentile is 38.2 hours. |
| Applications returned for a fix | 25.8% | 774 applications; 27% of those applicants then dropped out. |
| Verified but never started training | 21.7% | 482 people cleared KYC and then went quiet. |
| Reviewer time on documents | 21 minutes | Per application, before any follow-up. |
| Human touches per application | 3.3 | Across a 22-person Onboarding Ops team. |

### Table 4

| User | What they need | How they would use your product |
| --- | --- | --- |
| Applicant (new POSP) | To get certified quickly, know exactly what is wrong, and fix it once. | Uploads documents, receives one clear message if anything is missing, re-uploads, sees status. |
| Onboarding reviewer | To stop re-reading clean files and spend time only on real judgement calls. | Works a queue of cases the AI could not decide, with extracted fields and conflicts highlighted. |
| Ops team lead | To meet service levels and see where applications are stuck. | Watches queue age, AI decision mix, overrides and drop-off by stage. |
| Compliance officer | Assurance that no ineligible person is certified and every decision can be explained. | Samples decisions and reads the audit trail and the rule behind each outcome. |

### Table 5

| File | What's inside | Size | Use it to |
| --- | --- | --- | --- |
| PS-01_onboarding_rulebook.docx | Onboarding Ops standard: eligibility, per-document checks, name-matching rules, decision logic, service levels, message templates and Human-only decisions. | 10 sections · ~1,500 words | Define your rules, prompts and evaluation criteria. |
| PS-01_specimen_documents.docx | 12 applications from the test set, each with OCR output for every document and the correct decision explained. | 12 worked cases | Design and debug your reasoning on hard cases first. |
| PS-01_posp_applications.xlsx | applications, stage_events (event log), ops_team, monthly_funnel. | 3,018 + 21,188 + 22 + 9 rows · 4 sheets | Map today's process, find bottlenecks and build your before/after business case. |
| PS-01_document_review_test_set.xlsx | documents (OCR text, extracted fields, reviewer verdicts), application_truth (correct decision), reason_codes. | 3,600 + 600 + 14 rows · 3 sheets | Build and measure your engine; report accuracy against application_truth. |

### Table 6

| # | Scenario | Expected behaviour |
| --- | --- | --- |
| T1 | A clean application where every document agrees exactly (pick any APPROVE with name_match_category EXACT). | Approves in one pass with no human touch and records each check performed. |
| T2 | The marksheet shows the name with initials (e.g. R K SHARMA against RAHUL KUMAR SHARMA on the PAN). | Treats it as a match under the rulebook and approves; does not ask the applicant for anything. |
| T3 | The marksheet spells the name differently (MOHAMMED vs MOHAMMAD on the PAN). | Returns NEEDS_MORE_INFO with NAME_SPELLING_VARIANT and a message asking for a corrected document or declaration. |
| T4 | The Aadhaar and marksheet carry a different person's name. | Recommends REJECT for NAME_MISMATCH and routes it to a human to confirm; never auto-rejects. |
| T5 | The Class 10 marksheet photo is blurry and the DOB is unreadable, and the cheque is in a parent's name. | Asks for both fixes in a single message, not one at a time. |
| T6 | The PAN's fourth character is C. | Rejects for PAN_NOT_INDIVIDUAL and explains why in plain words. |
| T7 | Aadhaar DOB differs from PAN DOB by one year. | Returns NEEDS_MORE_INFO with DOB_MISMATCH; does not silently pick one date. |
| T8 | Face-match score is 0.68. | Routes to a human reviewer as the rulebook requires; does not decide on its own. |
| T9 | Address state on the Aadhaar differs from the declared state, everything else is clean. | Records it as informational and approves. |
| T10 | An applicant re-uploads a corrected marksheet after a NEEDS_MORE_INFO. | Re-checks only what changed, updates the decision and keeps the audit trail of both rounds. |

### Table 7

| Metric | Baseline today | Target | How to measure |
| --- | --- | --- | --- |
| Decision accuracy | Reviewers: 97.5% at document level | ≥ 95% vs application_truth | Run on all 600 test applications; confusion matrix by decision. |
| Recall on REJECT | Not measured today | ≥ 98% | Share of true REJECTs your engine rejects or routes to a human. Missing one is a compliance breach. |
| Straight-through rate | 0% (every file is read by a person) | ≥ 60% of applications | Share decided with no human touch and no error. |
| Follow-up rounds per returned application | 1–3 one-at-a-time requests | 1 | Count messages sent per application in the test set simulation. |
| Time to decision | Median 17.3 h queue + review | < 10 minutes for straight-through cases | Timestamp from upload to decision in your product. |
| Reviewer minutes per application | 21 minutes | < 5 minutes averaged across all applications | Time on routed cases only, spread over all applications. |
| Applicant-facing clarity | Not measured | ≥ 4 / 5 | Five real users rate your follow-up messages for clarity. |

### Table 8

| Term | Meaning |
| --- | --- |
| POSP | Point of Sales Person: an IRDAI-recognised part-time insurance seller who may sell simple products after training and an exam. |
| IRDAI | Insurance Regulatory and Development Authority of India, the insurance regulator. |
| KYC | Know Your Customer: verifying a person's identity and address with documents. |
| PAN | Permanent Account Number: a 10-character tax ID. The 4th character shows the holder type; P means an individual. |
| Penny-drop | Depositing ₹1 into a bank account to confirm it exists and to get the account holder's name from the bank. |
| OCR | Optical character recognition: turning an image of text into machine-readable text. |
| Straight-through processing | A case handled from start to finish with no human touch. |
| Face-match score | A 0–1 similarity score between two photos of a face, returned by a face-match service. |
| DigiLocker | The Government of India's platform for issuing and sharing verified digital documents. |
| Human-in-the-loop | A design where people review or approve some of the system's decisions. |

