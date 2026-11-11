# Operations Reviewer Cockpit Specification

> **UX/UI & High-Throughput Verification Workspace Specification**  
> **Source:** Rulebook v3.2 §7 & Reviewer Productivity Baseline

---

## 1. Cockpit Overview & Layout Philosophy

The Reviewer Cockpit is designed for maximum review throughput, error reduction, and cognitive ergonomics, targeting an average review time of $\le 90	ext{ seconds}$ per case (down from historical baseline of $3.5	ext{ minutes}$).

### Split-Screen Workspace Grid
```text
┌───────────────────────────────────────┬───────────────────────────────────────┐
│ LEFT PANEL: DOCUMENT VIEWER (50%)     │ RIGHT PANEL: VERIFICATION MATRIX (50%)│
│                                       │                                       │
│ [Doc Tabs: PAN | Aadhaar | 10th | ...]│ Applicant: Sachin Chand Mittal        │
│                                       │ App ID: APP-26001 | SLA: 03:42:10     │
│ ┌───────────────────────────────────┐ │                                       │
│ │                                   │ │ 1. Identity & PAN Check               │
│ │   High-Res Document Canvas        │ │    Declared PAN: NREPM4880W           │
│ │   (Pan, Zoom, Rotate, Invert)     │ │    OCR PAN:      NREPM4880W [MATCH]   │
│ │                                   │ │    Holder Type:  Individual (P) [OK] │
│ │   [Bounding Box Overlays]         │ │                                       │
│ │                                   │ │ 2. Name Matching Engine               │
│ └───────────────────────────────────┘ │    Declared: Sachin Chand Mittal      │
│                                       │    PAN Card: SACHIN CHAND MITTAL      │
│ CV Quality Signals:                   │    Aadhaar:  Sachin Chand Mittal      │
│ • Sharpness: 142.4 [OK]               │    Result:   Tier 1 (Exact Match)     │
│ • Glare: None Detected                │                                       │
│ • Crop: All 4 Corners Verified        │ 3. Penny-Drop & Bank Verification     │
│                                       │    Returned: S C MITTAL [MATCH]       │
│                                       │                                       │
│                                       │ 4. Face Match Score: 0.91 [PASSED]    │
├───────────────────────────────────────┴───────────────────────────────────────┤
│ ACTION BAR:                                                                   │
│ [F1: One-Click Approve]  [F2: Single-Pass Rework]  [F3: Escalate to Fraud]   │
└───────────────────────────────────────────────────────────────────────────────┘
```

---

## 2. Reviewer Productivity Features

1. **Synchronized Field Highlighting:** Clicking on an extracted field in the right panel immediately pans and zooms the document canvas on the left to highlight the exact OCR bounding box.
2. **Side-by-Side Diffing:** Mismatches between declared values and OCR values are rendered with character-level color diffing (red strikethrough for missing, green for additions).
3. **Keyboard Accelerators:**
   - `1` through `5`: Switch active document tab.
   - `Space`: Toggle full-screen image zoom.
   - `F1`: Approve Application (advances automatically to next in queue).
   - `F2`: Open Consolidated Rework Drawer (pre-populated with AI defect findings).
   - `F3`: Escalate to Senior Reviewer / Fraud Desk.
4. **SLA Countdown & Warning Banners:** Live countdown timer tracking the 4-hour SLA target for first review, turning amber at 2 hours and red at 3.5 hours.
