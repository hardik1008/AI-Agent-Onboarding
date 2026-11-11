# Frontend Requirements Specification: Applicant Portal, Cockpit & Executive Suite

> **Technical Specification for Multi-Persona User Interfaces**  
> **Source:** Baseline UX Failure Audit & Commercial Product Requirements

---

## 1. System Personas & Role-Based Access Control (RBAC)

The PolicyNest platform serves three primary user personas:
1. **Applicant (Candidate POSP):** Mobile-first onboarding portal; self-registration, client-side camera capture, LMS training, and online examination.
2. **Ops Reviewer (Verification Officer):** High-throughput desktop cockpit; queue management, side-by-side inspection, single-pass rework tool.
3. **Admin / Ops Lead (Compliance & Leadership):** Real-time monitoring dashboard, STP analytics, reviewer performance, regulatory export.

---

## 2. Applicant Portal Requirements

### 2.1 Mobile-First Onboarding Flow
- **Responsive Layout:** Optimized for mobile viewports (360px to 420px width) running modern mobile browsers.
- **Client-Side Real-Time Quality Check (WebAssembly / OpenCV.js):**
  - **Blur Detection:** Calculates Laplacian variance prior to upload. If variance < 100, displays instant warning: *"Image is blurry. Please hold camera steady."*
  - **Glare Detection:** Checks for specular overexposure. Displays warning: *"Turn off flash to eliminate glare."*
  - **Edge / Corner Detection:** Verifies all 4 card corners are inside bounding guide.
- **Single Document Upload Progress:** Visual checklist showing status of each required document (Uploaded, Processing, Verified, Action Needed).
- **Consolidated Rework View:** Deep-link view isolating only defective documents with tailored guidance in English and Hindi.

---

## 3. Operations Reviewer Cockpit Requirements

- **Zero-Latency Split View:** 50% high-res canvas (WebGL/Canvas) with smooth pan, pinch-to-zoom, rotate, and contrast inversion; 50% structured decision matrix.
- **Synchronized Visual Grounding:** Clicking on an extracted field highlights its bounding box on the original document.
- **One-Click Decision Bar:** Single hotkey actions for Approve (`F1`), Consolidate Rework (`F2`), and Escalate (`F3`).
- **Live SLA Countdown:** Visual SLA timer showing remaining minutes before SLA breach.

---

## 4. Executive Analytics & Monitoring Dashboard

- **Real-Time KPIs:** Live ticker showing Straight-Through Processing (STP) rate, First-Pass Yield (FPY), Median TAT (hours), and Cost per Onboarded POSP.
- **Funnel Stage Drop-Off Waterfall:** Step-by-step conversion tracking from Registration -> Docs Submitted -> KYC Verified -> Training Completed -> Exam Passed -> Certified.
- **Defect Pareto Analysis:** Ranked bar chart of top failure causes across all 14 standard reason codes.
- **Reviewer Productivity Roster:** Reviewer speed index, throughput, and error rate tracking.
