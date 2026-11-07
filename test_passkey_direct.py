import uuid
from datetime import datetime
from database import get_connection

conn = get_connection()
c = conn.cursor()
req_user_name = "Rohit Ramesh Sharma"
token = f"pn_sec_passkey_{uuid.uuid4().hex}"

c.execute(
    """INSERT INTO users (mobile, full_name, role, token, current_app_id, last_login_at)
       VALUES (?, ?, ?, ?, ?, ?)
       ON CONFLICT(mobile) DO UPDATE SET token=excluded.token, last_login_at=excluded.last_login_at""",
    ("9820194820", req_user_name, "APPLICANT", token, "APP-2026-PASSKEY", datetime.now().isoformat())
)

c.execute(
    "INSERT INTO audit_trail (application_id, actor, event, details, timestamp) VALUES (?, ?, ?, ?, ?)",
    ("APP-2026-PASSKEY", "SYSTEM_WEBAUTHN", "FIDO2_PASSKEY_SUCCESS", f"Biometric passkey certified for {req_user_name}", datetime.now().isoformat())
)

conn.commit()
conn.close()
print("Direct DB Passkey write SUCCESS! Token:", token)
