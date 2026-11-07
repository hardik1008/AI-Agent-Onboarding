import requests

BASE_URL = "http://127.0.0.1:8000"

def test_google_auth():
    print("Testing /api/auth/google...")
    r = requests.post(f"{BASE_URL}/api/auth/google", json={
        "email": "rohit.sharma@gmail.com",
        "name": "Rohit Ramesh Sharma",
        "picture": "https://lh3.googleusercontent.com/a/sample-avatar"
    })
    assert r.status_code == 200, f"Google auth failed: {r.status_code}"
    res = r.json()
    print("Google Auth OK:", res)
    assert res["success"] is True
    assert res["user"]["email"] == "rohit.sharma@gmail.com"
    assert res["user"]["auth_provider"] == "GOOGLE"
    
    token = res["token"]
    r_me = requests.get(f"{BASE_URL}/api/auth/me?token={token}")
    assert r_me.status_code == 200
    assert r_me.json()["authenticated"] is True
    print("Google session verified via /api/auth/me successfully!")

if __name__ == "__main__":
    test_google_auth()
