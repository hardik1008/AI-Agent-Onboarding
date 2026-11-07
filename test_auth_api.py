import sys
import json
import requests

BASE_URL = "http://127.0.0.1:8000"

def test_endpoints():
    print("Testing /api/health...")
    r = requests.get(f"{BASE_URL}/api/health")
    assert r.status_code == 200, f"Health check failed: {r.status_code}"
    print("Health OK:", r.json())

    print("\nTesting /api/auth/send-otp...")
    r = requests.post(f"{BASE_URL}/api/auth/send-otp", json={
        "mobile": "9820194820",
        "role": "APPLICANT",
        "full_name": "Rohit Ramesh Sharma"
    })
    assert r.status_code == 200, f"Send OTP failed: {r.status_code}"
    res = r.json()
    print("Send OTP OK:", res)
    assert res["success"] is True

    print("\nTesting /api/auth/verify-otp...")
    r = requests.post(f"{BASE_URL}/api/auth/verify-otp", json={
        "mobile": "9820194820",
        "otp": "451660",
        "role": "APPLICANT",
        "full_name": "Rohit Ramesh Sharma"
    })
    assert r.status_code == 200, f"Verify OTP failed: {r.status_code}"
    res = r.json()
    print("Verify OTP OK:", res)
    assert res["success"] is True
    token = res["token"]

    print("\nTesting /api/auth/me...")
    r = requests.get(f"{BASE_URL}/api/auth/me?token={token}")
    assert r.status_code == 200, f"Auth me failed: {r.status_code}"
    res = r.json()
    print("Auth me OK:", res)
    assert res["authenticated"] is True
    assert res["user"]["mobile"] == "9820194820"

    print("\nTesting /api/audit/logs...")
    r = requests.get(f"{BASE_URL}/api/audit/logs?limit=5")
    assert r.status_code == 200, f"Audit logs failed: {r.status_code}"
    res = r.json()
    print("Audit logs OK (count):", len(res))
    assert len(res) > 0

    print("\nTesting /api/auth/logout...")
    r = requests.post(f"{BASE_URL}/api/auth/logout", json={"token": token})
    assert r.status_code == 200
    print("Logout OK:", r.json())

    r = requests.get(f"{BASE_URL}/api/auth/me?token={token}")
    assert r.json()["authenticated"] is False
    print("Session correctly invalidated.")

    print("\nALL AUTH & AUDIT ENDPOINTS PASSED WITH 100% SUCCESS!")

if __name__ == "__main__":
    test_endpoints()
