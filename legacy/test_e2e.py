import requests

BASE = "http://127.0.0.1:8000"

def test_all():
    print("Testing Complete Enterprise Endpoints against http://127.0.0.1:8000 ...")

    # 1. Root & Health
    r = requests.get(f"{BASE}/")
    assert r.status_code == 200
    print("OK: GET / (HTML loaded, length: {})".format(len(r.text)))

    r = requests.get(f"{BASE}/api/health")
    assert r.status_code == 200 and r.json().get("status") == "ok"
    print("OK: GET /api/health")

    # 2. Real NSDL PAN Gateway
    r = requests.post(f"{BASE}/api/gov/nsdl-pan-verify", json={
        "pan": "ABCPR4891K",
        "declared_name": "Rohit Ramesh Sharma"
    })
    assert r.status_code == 200 and r.json().get("pan_status") == "OPERATIVE_AND_VALID"
    print("OK: POST /api/gov/nsdl-pan-verify (NSDL TIN Gateway: OPERATIVE & LINKED)")

    # 3. UIDAI CIDR OTP Request & Verify
    r_otp_req = requests.post(f"{BASE}/api/gov/uidai-otp-request", json={"mobile_or_aadhaar": "9820194820"})
    assert r_otp_req.status_code == 200 and r_otp_req.json().get("success") is True
    txn_id = r_otp_req.json().get("txn_id")
    print(f"OK: POST /api/gov/uidai-otp-request (Txn: {txn_id[:25]}...)")

    r_otp_ver = requests.post(f"{BASE}/api/gov/uidai-otp-verify", json={
        "txn_id": txn_id,
        "otp": "451660",
        "declared_name": "Rohit Ramesh Sharma"
    })
    assert r_otp_ver.status_code == 200 and r_otp_ver.json().get("status") == "UIDAI_XML_AUTHENTICATED"
    print("OK: POST /api/gov/uidai-otp-verify (UIDAI Offline XML e-KYC Certified)")

    # 4. Bank Lookup
    r = requests.get(f"{BASE}/api/bank/lookup?ifsc=HDFC0000060")
    assert r.status_code == 200 and r.json().get("valid") is True
    print(f"OK: GET /api/bank/lookup ({r.json().get('bank')} · {r.json().get('branch')})")

    # 5. CTS-2010 Cheque OCR & MICR Analyzer
    r_cheque = requests.post(f"{BASE}/api/bank/cheque-ocr-verify", json={
        "account_number": "50100492817492",
        "ifsc_code": "HDFC0000060",
        "declared_name": "Rohit Ramesh Sharma"
    })
    assert r_cheque.status_code == 200 and r_cheque.json().get("is_cts2010_compliant") is True
    print(f"OK: POST /api/bank/cheque-ocr-verify (CTS-2010 MICR: {r_cheque.json().get('extracted_micr_code')} · Blur: {r_cheque.json().get('blur_variance')})")

    # 6. NPCI IMPS Penny Drop
    r = requests.post(f"{BASE}/api/bank/penny-drop", json={
        "account_number": "50100492817492",
        "ifsc_code": "HDFC0000060",
        "declared_name": "Rohit Ramesh Sharma"
    })
    assert r.status_code == 200 and r.json().get("success") is True
    print(f"OK: POST /api/bank/penny-drop (Beneficiary: {r.json().get('beneficiary_name')} · Match: {r.json().get('match_score')}%)")

    # 7. Form 1-A POSP Agreement e-Sign
    r_esign = requests.post(f"{BASE}/api/agreement/form1a-esign", json={
        "application_id": "APP-2026-LIVE-ROHIT",
        "declared_name": "Rohit Ramesh Sharma",
        "pan": "ABCPR4891K"
    })
    assert r_esign.status_code == 200 and r_esign.json().get("status") == "ESIGN_SUCCESS"
    print(f"OK: POST /api/agreement/form1a-esign (Fingerprint: {r_esign.json().get('digital_certificate_fingerprint')[:18]}...)")

    # 8. Step 0 Eligibility Check
    r = requests.post(f"{BASE}/api/verify/step0", json={
        "pan": "ABCPR4891K",
        "dob": "1994-04-30",
        "irdai_registry_hit": False
    })
    assert r.status_code == 200 and r.json().get("passed") is True
    print("OK: POST /api/verify/step0 (Rulebook §1.1 & §1.2 Gatekeeper Cleared)")

    # 9. Full Application Verify & SQLite DB Write
    r = requests.post(f"{BASE}/api/verify/full", json={
        "application_id": "APP-2026-LIVE-ROHIT",
        "declared_name": "Rohit Ramesh Sharma",
        "declared_dob": "1994-04-30",
        "declared_pan": "ABCPR4891K",
        "mobile": "9820194820",
        "declared_education": "Graduate",
        "declared_state": "Maharashtra",
        "penny_drop_name_returned": "ROHIT RAMESH SHARMA"
    })
    assert r.status_code == 200 and r.json().get("final_decision") in ["APPROVE", "REVIEW_QUEUE"]
    print(f"OK: POST /api/verify/full -> Decision: {r.json().get('final_decision')} (Recorded to SQLite policynest.db)")

    # 10. Recent Applications Query from SQLite
    r = requests.get(f"{BASE}/api/applications/recent?limit=5")
    assert r.status_code == 200 and len(r.json()) > 0
    print(f"OK: GET /api/applications/recent (Retrieved {len(r.json())} apps from database)")

    # 11. Ops Reviewer Action (1-Click Database Write)
    r = requests.post(f"{BASE}/api/ops/action", json={
        "application_id": "APP-2026-LIVE-ROHIT",
        "reviewer_id": "OPS-07",
        "action": "APPROVE",
        "notes": "Verified via NSDL & NPCI"
    })
    assert r.status_code == 200 and r.json().get("status") == "SUCCESS"
    print("OK: POST /api/ops/action (Reviewer OPS-07 Action Committed to SQLite)")

    # 12. LMS Completion & Certification
    r = requests.post(f"{BASE}/api/lms/complete", json={
        "application_id": "APP-2026-LIVE-ROHIT",
        "exam_score": 100
    })
    assert r.status_code == 200 and r.json().get("status") == "CERTIFIED"
    print(f"OK: POST /api/lms/complete (Issued Official License: {r.json().get('certificate_id')})")

    # 13. AI Metrics & Observatory
    r = requests.get(f"{BASE}/api/ai/metrics")
    assert r.status_code == 200 and "training_accuracy" in r.json()
    print(f"OK: GET /api/ai/metrics (Accuracy: {r.json().get('training_accuracy')}% · Reject Recall: {r.json().get('reject_recall')}%)")

    print("\nALL 13 ENTERPRISE END-TO-END TESTS PASSED WITH 100% SUCCESS (HTTP 200 OK)!")

if __name__ == "__main__":
    test_all()
