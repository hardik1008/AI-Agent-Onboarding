# 01. BUSINESS PROBLEM STATEMENT
**Challenge ID: PS-01**
**Problem Owner: Vansh Miglani, InsuranceDekho**
**Case Company: PolicyNest Insurance Brokers Private Limited (Fictional)**

---

## 1. Industry & Business Context
In the Indian insurance ecosystem, distribution is heavily reliant on agency channels. The **Point of Sales Person (POSP)** framework, established by the Insurance Regulatory and Development Authority of India (IRDAI), represents the fastest-growing distribution vector. POSPs are typically non-traditional, part-time micro-entrepreneurs—local shopkeepers, kirana owners, tax consultants, and homemakers—who market pre-underwritten retail insurance policies (motor, health, life) within their communities.

For an insurance broker like PolicyNest, scaling its POSP network is directly correlated with top-line Gross Written Premium (GWP). Every week an aspiring agent spends trapped in onboarding bureaucracy is a week of lost commission, lost policy distribution, and immediate competitive leakage to rival brokers.

---

## 2. The Operational Crisis at PolicyNest
PolicyNest operates across 14 states with a current network of approximately 14,000 active POSPs. Inbound agent applications are processed by a dedicated **22-person Onboarding Operations team** located in Gurugram.

Between **January and September 2026**, PolicyNest recorded:
* **3,000 Application Starts**: Average inbound velocity of ~330 applicants per month.
* **1,732 Certified Agents (57.7%)**: Total funnel conversion yield.
* **951 Dropped Out (31.7%)**: Candidates who abandoned the process prematurely.
* **314 Rejected (10.5%)**: Ineligible candidates disqualified under statutory regulations.
* **3 In Progress (0.1%)**: Active at quarterly snapshot.

### The Problem in One Sentence:
> **"42 out of every 100 applicants who want to sell insurance for PolicyNest never get certified—not because they fail the regulatory exam, but because they are exhausted by a slow, repetitive, human-dependent document review process."**

---

## 3. Four Quantified Failure Points
Analysis of 21,188 operational stage events revealed that operational leakage is concentrated in the document review zone:

1. **Massive Idle Queue Latency**:
   Applications sit in an unassigned queue for a **median of 17.3 hours** (90th percentile: 38.2 hours; 95th percentile: 47.1 hours) before a human reviewer opens them. This latency is invariant across time of day, day of week, or seasonal volume.
2. **Repetitive, Disproportionate Touch Time**:
   Reviewers spend an average of **20.7 minutes of manual eye-checking** per application. They perform the same exhaustive checks on perfectly clean files (20.6 min) as on complex edge cases (20.9 min), despite 61% of files being straightforward approvals.
3. **Sequential 'One-at-a-Time' Rework Loops**:
   When documents contain flaws, reviewers send sequential messages requesting one document fix at a time. Each cycle adds **~2.2 days** of turnaround time. While clean files certify in 0.7 days of review, returned files take **3.3 days**. Over **27.3% of applicants asked for a fix never reply** (211 agents lost).
4. **Post-KYC Drop-off Hand-off Friction**:
   Once KYC is marked complete, **482 candidates (21.7% of verified applicants)** go completely silent and never start their mandatory 15-hour training course, largely due to sluggish manual hand-offs and lack of instant engagement.

---

## 4. The Mandate for an AI-First Re-architecture
PolicyNest requires a complete re-engineering of the POSP onboarding workflow from a human-push model to an **autonomous, AI-first decision engine**:
* **Real-time Gating**: Instant quality checking and statutory eligibility pre-flight at upload.
* **Autonomous Reasoning**: Multimodal extraction and rulebook adjudication across all 6 documents.
* **Single Consolidated Follow-up**: An aggregated, multi-lingual message explaining all defects in one pass.
* **Human-in-the-Loop Safeguards**: Precise routing of ambiguous name matches and edge cases to senior reviewers, with evidence displayed side by side.
* **Instant Activation**: Immediate automated triggering of LMS training upon KYC approval.
