# PolicyNest AI-First POSP Onboarding Suite — External Integration Register
**Document ID:** PN-INT-REG-2026-V1  
**Author:** Government & Bank Verification Integration Engineer  
**Effective Date:** 8 November 2026  
**Status:** OFFICIAL INTEGRATION REGISTER & COMPLIANCE SPECIFICATION

---

## 1. Non-Negotiable Integration Rules

Every external gateway integration must adhere strictly to the following regulatory, technical, and ethical boundaries:

1. **NO UNAUTHORIZED SCRAPING**: Never scrape government portals (UIDAI, Income Tax Department, CBSE) or commercial banking websites.
2. **NO AUTOMATED NET-BANKING LOGIN**: Never simulate or automate personal internet-banking sessions.
3. **ZERO CREDENTIAL COLLECTION**: Never solicit, intercept, or store banking passwords, debit card PINs, UPI PINs, or banking OTPs.
4. **NO BYPASSING PARTNER REQUISITES**: Never bypass government partner registration or API licensing requirements.
5. **EXPLICIT SANDBOX LABELLING**: Every synthetic or simulated response must be explicitly tagged `SANDBOX` in database records and audit trails. Never misrepresent a mock response as a live government or banking result.
6. **STRICT SECRETS ISOLATION**: Keep all API keys, client secrets, and private certificates server-side. Never expose integration credentials in frontend client code or public repositories.
7. **STATUTORY CONSENT & AUDITING**: Capture explicit candidate consent prior to initiating any verification request, recording consent timestamps and IP addresses.

---

## 2. Master Integration Status Matrix

| Integration Category | Target Gateway / Authority | Current Status | Primary Production Provider Options | Production Requisites / Approvals |
| :--- | :--- | :---: | :--- | :--- |
| **1. DigiLocker Document Retrieval** | MeriPehchaan / NeGD / MeitY | **SANDBOX** | NeGD National DigiLocker API / Setu / Karza / Signzy | Broker Org Registration, RSA 2048 Signing Key, IRDAI Broker License copy. |
| **2. PAN Registry Verification** | Income Tax Department / NSDL / Protean | **SANDBOX** | Protean (NSDL) / UTIITSL / Cashfree / Razorpay | NSDL B2B Agreement, Commercial PAN Verification License, Static IP Whitelist. |
| **3. Aadhaar Verification** | UIDAI (Unique Identification Authority of India)| **SANDBOX** | UIDAI Licensed KUA/AUA (Karza, Setu, Bureau) | Sub-KUA Agreement, Aadhaar Act Section 4(3) compliance, Masking Vault. |
| **4. Bank Account & Penny Drop** | NPCI / Commercial Escrow Switch | **SANDBOX** | Cashfree Payouts / RazorpayX / Setu / ICICI Eazypay | Current Account Escrow Agreement, ₹1 IMPS Payout Balance, Webhook Secret Key. |
| **5. IFSC Code Directory** | Reserve Bank of India (RBI) | **ACTIVE** | Local High-Speed In-Memory Master Directory | Zero external credentials required; compiled from official RBI master list. |
| **6. Biometric Face Liveness** | ISO/IEC 30107-3 Biometric Standard | **ACTIVE** | On-Device OpenCV Laplacian + MediaPipe / HyperVerge | Computer vision runs locally on server/browser; zero external API fees. |
| **7. IRDAI Central POSP Registry** | Insurance Regulatory and Development Authority | **SANDBOX** | IRDAI IIB Portal (Insurance Information Bureau) | IRDAI Direct Broker Entity Access, Central POSP Portal Webhooks. |
| **8. Telecom DLT SMS Gateway** | TRAI Distributed Ledger Technology (DLT) | **SANDBOX** | Gupshup / Twilio / Kaleyra / Textlocal | TRAI Principal Entity (PE) Registration, Approved DLT Headers & Templates. |

---

## 3. Detailed Gateway Specifications & Sandbox Simulators

### 3.1 DigiLocker MeriPehchaan Gateway
- **Endpoint**: `POST /api/digilocker/fetch-dynamic`
- **Current Mode**: `SANDBOX`
- **Behavior**: Emulates the official MeriPehchaan OAuth 2.0 PKCE consent screen. Upon candidate authorization, retrieves standardized XML payloads for e-Aadhaar, NSDL PAN, and CBSE Class X marksheet.
- **Production Implementation Path**:
  1. Register PolicyNest as a certified "Requester" on the MeriPehchaan Portal (`meripehchaan.gov.in`).
  2. Implement OAuth 2.0 PKCE redirection flow with `client_id`, `client_secret`, and `redirect_uri`.
  3. Decrypt received signed XML files using PolicyNest's private PKI key.

### 3.2 PAN Verification Gateway
- **Endpoint**: `POST /api/gov/nsdl-pan-verify`
- **Current Mode**: `SANDBOX`
- **Behavior**: Validates PAN structure (`AAAAA9999A`), verifies the 4th character is `'P'` (Individual), and confirms active taxpayer status with masked full name.
- **Production Implementation Path**:
  1. Contract an authorized Protean/NSDL verification provider (e.g. Setu, Cashfree).
  2. Configure `PAN_PROVIDER_URL` and `PAN_PROVIDER_API_KEY` in server environment variables.
  3. Validate returned `fullName` against candidate's declared PAN name using the §5 Name Matching Taxonomy.

### 3.3 NPCI IMPS Bank Account & Penny Drop Gateway
- **Endpoint**: `POST /api/bank/penny-drop`
- **Current Mode**: `SANDBOX`
- **Behavior**: Simulates an automated ₹1 IMPS payout from PolicyNest's commission escrow account to the applicant's verified IFSC and account number. Simulates banking switch states: Escrow CBS $\rightarrow$ NPCI IMPS Switch $\rightarrow$ Destination Bank.
- **Production Implementation Path**:
  1. Provision a funded commercial payout account with a partner bank (e.g. ICICI Bank, HDFC Bank) or fintech aggregator (Cashfree/Razorpay).
  2. Configure webhook callback handler with HMAC SHA-256 signature verification for asynchronous credit status updates.
  3. Enforce Rulebook §4.5: Name returned by beneficiary bank must match candidate PAN. Third-party accounts are strictly rejected.

### 3.4 Biometric Face Liveness Gateway
- **Endpoint**: `POST /api/biometrics/liveness-mesh` & `POST /api/liveness/verify`
- **Current Mode**: `ACTIVE (PRODUCTION READY)`
- **Behavior**: Processes real camera frames captured from the client webcam. OpenCV extracts the facial bounding box, computes Laplacian variance to verify texture sharpness, verifies human presence, and calculates facial feature similarity against the anchor PAN photo.
- **Assurance Level**: Local real-time inference (0.12s latency, ₹0.00 cloud API cost).

---

## 4. Integration Evidence & Audit Schema

Every verification execution must write a normalized record to the database with the following minimum schema:

```json
{
  "transaction_id": "PN-TXN-20261108-84920",
  "application_id": "APP-2026-00482",
  "provider": "NPCI_IMPS_GATEWAY",
  "mode": "SANDBOX",
  "endpoint": "/api/bank/penny-drop",
  "status": "SUCCESS",
  "assurance_level": "LEVEL_3_HIGH",
  "request_timestamp": "2026-11-08T10:45:12.194Z",
  "response_timestamp": "2026-11-08T10:45:13.208Z",
  "latency_ms": 1014,
  "evidence": {
    "bank_rrn": "IMPS2026110899120",
    "beneficiary_name_bank": "ROHIT RAMESH SHARMA",
    "name_match_score": 0.994,
    "ifsc_resolved": "HDFC0000060"
  },
  "sha256_audit_signature": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855"
}
```
