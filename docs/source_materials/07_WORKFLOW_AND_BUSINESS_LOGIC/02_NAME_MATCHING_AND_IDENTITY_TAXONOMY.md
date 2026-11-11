# Name Matching Algorithm & Identity Taxonomy Specification

> **Engineering Specification for the 8-Tier Identity Resolution Engine**  
> **Source:** Rulebook v3.2 §5 & Specimen Ground Truth Benchmark

---

## 1. The 8-Tier Name Matching Taxonomy

Indian legal names exhibit diverse linguistic variations, patronymics, initializations, and honorific additions. Treating spelling variations as identity mismatches causes over 40% of unnecessary manual touches. PolicyNest implements an 8-tier resolution taxonomy:

| Tier | Pattern Description | Golden Anchor (PAN) | Document Candidate | Verdict | STP Allowed? | Operational Action |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **Tier 1** | **Exact Match** (case & space insensitive) | `RAHUL KUMAR SHARMA` | `Rahul Kumar Sharma` | **MATCH** | Yes | Auto-Approve |
| **Tier 2** | **Initials for Given or Middle Names** | `RAHUL KUMAR SHARMA` | `R K SHARMA` or `RAHUL K SHARMA` | **MATCH** | Yes | Auto-Approve |
| **Tier 3** | **Token Order Swapped** | `RAHUL KUMAR SHARMA` | `SHARMA RAHUL KUMAR` | **MATCH** | Yes | Auto-Approve |
| **Tier 4** | **Middle Name Added or Missing** | `RAHUL KUMAR SHARMA` | `RAHUL SHARMA` or `PRIYA KUMARI SHARMA` | **MATCH** | Yes | Auto-Approve |
| **Tier 5** | **Spelling Variant of Same Name** | `MOHAMMAD ASIF` | `MOHAMMED ASIF` or `LAKSHMI` vs `LAXMI` | **NEEDS_INFO** | No | Emit single-pass rework query (`NAME_SPELLING_VARIANT`) |
| **Tier 6** | **Surname Changed Post-Marriage** | `PRIYA SHARMA` | `PRIYA VERMA` | **NEEDS_INFO** | No | Request Marriage Certificate / Gazette (Human Review) |
| **Tier 7** | **Different Person / Unrelated Identity**| `RAHUL KUMAR SHARMA` | `ANKIT YADAV` | **REJECT** | **NO** | Escalate to Senior Reviewer / Fraud Desk |
| **Tier 8** | **Truncated Core-Banking Return** | `SACHIN CHAND MITTAL` | `S C MITTAL` | **MATCH** | Yes | Bank Penny-Drop auto-approval |

---

## 2. Algorithmic Resolution Pipeline

The Name Matching Engine executes a multi-stage deterministic comparison pipeline:

```text
[Input Strings: Name A (PAN), Name B (Doc/Bank)]
                     │
                     ▼
       Stage 1: Unicode Normalization
   (Strip honorifics: SHRI, SMT, MR, MS, DR;
    Uppercase; strip special characters; collapse whitespace)
                     │
                     ▼
         Stage 2: Exact Equality Check
           (A == B) ───[YES]───> Tier 1: MATCH
                     │ [NO]
                     ▼
         Stage 3: Token Sorted Equality
   (sorted(tokens_A) == sorted(tokens_B)) ───[YES]───> Tier 3: MATCH
                     │ [NO]
                     ▼
        Stage 4: Initial Expansion Match
   (Verify each initial in B corresponds to prefix of token in A) ───[YES]───> Tier 2: MATCH
                     │ [NO]
                     ▼
        Stage 5: Subsequence / Subset Match
   (tokens_B is strict subset of tokens_A or vice-versa) ───[YES]───> Tier 4: MATCH
                     │ [NO]
                     ▼
      Stage 6: Fuzzy & Phonetic Distance
   (Jaro-Winkler >= 0.88 OR Levenshtein distance <= 2 OR Double Metaphone match)
                     │
         ┌───────────┴───────────┐
      [YES]                     [NO]
        │                         │
        ▼                         ▼
Tier 5: SPELLING_VARIANT     Tier 7: DIFFERENT PERSON
(Consolidated Rework)       (Escalate to Human / Fraud Desk)
```

---

## 3. Strict Compliance Guardrail: Zero AI False Accusations

Under PolicyNest Governance Rule §9, the Decision Engine is **strictly forbidden from issuing an autonomous terminal rejection under Tier 7 (`NAME_MISMATCH`)**.
- **Rationale:** OCR artifacts, inverted identity documents (e.g. uploading a parent's document by accident), or transliteration failures could unjustly disqualify a valid applicant.
- **Protocol:** Whenever Tier 7 triggers, the application status transitions to `IN_REVIEW (FRAUD_ESCALATION)` with a high-priority ticket assigned to a Senior Ops Reviewer.
