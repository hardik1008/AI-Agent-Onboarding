import requests
r = requests.post("http://127.0.0.1:8000/api/auth/passkey", json={"user_name": "Rohit Ramesh Sharma"})
print("Status:", r.status_code)
print("Text:", r.text)
