import re

# 1. Update database.py
with open(r"C:\Users\vajja\Desktop\PolicyNest_AI_Suite\database.py", "r", encoding="utf-8") as f:
    db_code = f.read()

old_conn = """def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn"""

new_conn = """def get_connection():
    conn = sqlite3.connect(DB_PATH, timeout=30.0, check_same_thread=False)
    conn.execute("PRAGMA journal_mode=WAL")
    conn.row_factory = sqlite3.Row
    return conn"""

if old_conn in db_code:
    db_code = db_code.replace(old_conn, new_conn)
    with open(r"C:\Users\vajja\Desktop\PolicyNest_AI_Suite\database.py", "w", encoding="utf-8") as f:
        f.write(db_code)
    print("Updated database.py with WAL mode and 30s timeout.")

# 2. Update main.py passkey endpoint
with open(r"C:\Users\vajja\Desktop\PolicyNest_AI_Suite\main.py", "r", encoding="utf-8") as f:
    main_code = f.read()

bad_audit = '''c.execute(
        "INSERT INTO audit_trail (application_id, stage, event_type, details) VALUES (?, ?, ?, ?)",
        ("APP-2026-PASSKEY", "PASSKEY_AUTH", "FIDO2_WEBAUTHN_SUCCESS", f"Biometric passkey certified for {req.user_name}")
    )'''

good_audit = '''c.execute(
        "INSERT INTO audit_trail (application_id, actor, event, details, timestamp) VALUES (?, ?, ?, ?, ?)",
        ("APP-2026-PASSKEY", "SYSTEM_WEBAUTHN", "FIDO2_PASSKEY_SUCCESS", f"Biometric passkey authentication certified for {req.user_name}", datetime.now().isoformat())
    )'''

if bad_audit in main_code:
    main_code = main_code.replace(bad_audit, good_audit)
    with open(r"C:\Users\vajja\Desktop\PolicyNest_AI_Suite\main.py", "w", encoding="utf-8") as f:
        f.write(main_code)
    print("Updated main.py audit_trail columns in auth_passkey.")
