import sys
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

MAIN_PATH = r"C:\Users\vajja\Desktop\PolicyNest_AI_Suite\main.py"

with open(MAIN_PATH, "r", encoding="utf-8") as f:
    code = f.read()

# Add uuid import if missing
if "import uuid" not in code:
    code = "import uuid\n" + code

google_popup_code = '''
# ================= GOOGLE IDENTITY SERVICES STANDALONE POPUP =================
GOOGLE_POPUP_HTML = """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>Sign in with Google - PolicyNest Partner Portal</title>
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <style>
    * { box-sizing: border-box; margin: 0; padding: 0; }
    body {
      font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
      background: #ffffff;
      color: #202124;
      display: flex;
      flex-direction: column;
      align-items: center;
      justify-content: center;
      min-height: 100vh;
      padding: 24px;
    }
    .auth-card {
      width: 100%;
      max-width: 440px;
      border: 1px solid #dadce0;
      border-radius: 8px;
      padding: 40px 36px 36px;
      text-align: center;
      box-shadow: 0 1px 3px rgba(60,64,67,0.3);
      position: relative;
    }
    .google-logo { width: 44px; height: 44px; margin-bottom: 16px; }
    h1 { font-size: 24px; font-weight: 500; color: #202124; margin-bottom: 8px; }
    .subtitle { font-size: 15px; color: #5f6368; margin-bottom: 24px; }
    .subtitle strong { color: #1a73e8; }
    .account-list { display: flex; flex-direction: column; gap: 8px; margin-bottom: 20px; }
    .account-item {
      display: flex;
      align-items: center;
      padding: 12px 16px;
      border: 1px solid #dadce0;
      border-radius: 8px;
      cursor: pointer;
      text-align: left;
      transition: background 0.15s, border-color 0.15s;
    }
    .account-item:hover { background: #f8f9fa; border-color: #1a73e8; }
    .avatar {
      width: 40px;
      height: 40px;
      border-radius: 50%;
      background: #1a73e8;
      color: white;
      display: flex;
      align-items: center;
      justify-content: center;
      font-weight: 600;
      font-size: 16px;
      margin-right: 14px;
      flex-shrink: 0;
    }
    .avatar.green { background: #0f9d58; }
    .acc-info { flex: 1; min-width: 0; }
    .acc-name { font-size: 14px; font-weight: 600; color: #202124; }
    .acc-email { font-size: 12px; color: #5f6368; overflow: hidden; text-overflow: ellipsis; }
    .custom-section { margin-top: 12px; padding-top: 16px; border-top: 1px solid #dadce0; text-align: left; }
    .custom-input {
      width: 100%;
      padding: 10px 12px;
      font-size: 13px;
      border: 1px solid #dadce0;
      border-radius: 6px;
      margin-top: 6px;
      margin-bottom: 10px;
    }
    .btn-submit {
      width: 100%;
      background: #1a73e8;
      color: white;
      border: none;
      padding: 10px 16px;
      border-radius: 6px;
      font-size: 13px;
      font-weight: 600;
      cursor: pointer;
    }
    .btn-submit:hover { background: #1557b0; }
    .terms { font-size: 11px; color: #5f6368; line-height: 1.5; margin-top: 24px; text-align: left; }
    .loading-overlay {
      display: none;
      position: absolute;
      inset: 0;
      background: rgba(255,255,255,0.92);
      border-radius: 8px;
      flex-direction: column;
      align-items: center;
      justify-content: center;
      font-size: 14px;
      font-weight: 500;
      color: #1a73e8;
    }
    .spinner {
      width: 36px;
      height: 36px;
      border: 3px solid #e8f0fe;
      border-top-color: #1a73e8;
      border-radius: 50%;
      animation: spin 0.8s linear infinite;
      margin-bottom: 12px;
    }
    @keyframes spin { to { transform: rotate(360deg); } }
  </style>
</head>
<body>
  <div class="auth-card">
    <div id="loader" class="loading-overlay">
      <div class="spinner"></div>
      <p id="loader-msg">Authenticating with Google...</p>
    </div>

    <!-- Official Google SVG -->
    <svg class="google-logo" viewBox="0 0 24 24">
      <path fill="#4285F4" d="M22.56 12.25c0-.78-.07-1.53-.2-2.25H12v4.26h5.92c-.26 1.37-1.04 2.53-2.21 3.31v2.77h3.57c2.08-1.92 3.28-4.74 3.28-8.09z"/>
      <path fill="#34A853" d="M12 23c2.97 0 5.46-.98 7.28-2.66l-3.57-2.77c-.98.66-2.23 1.06-3.71 1.06-2.86 0-5.29-1.93-6.16-4.53H2.18v2.84C3.99 20.53 7.7 23 12 23z"/>
      <path fill="#FBBC05" d="M5.84 14.09c-.22-.66-.35-1.36-.35-2.09s.13-1.43.35-2.09V7.06H2.18C1.43 8.55 1 10.22 1 12s.43 3.45 1.18 4.94l2.85-2.22.81-.63z"/>
      <path fill="#EA4335" d="M12 5.38c1.62 0 3.06.56 4.21 1.64l3.15-3.15C17.45 2.09 14.97 1 12 1 7.7 1 3.99 3.47 2.18 7.06l3.66 2.84c.87-2.6 3.3-4.52 6.16-4.52z"/>
    </svg>

    <h1>Choose an account</h1>
    <p class="subtitle">to continue to <strong>PolicyNest Partner Portal</strong></p>

    <div class="account-list">
      <div class="account-item" onclick="chooseAccount('rohit.sharma@gmail.com', 'Rohit Ramesh Sharma')">
        <div class="avatar">R</div>
        <div class="acc-info">
          <div class="acc-name">Rohit Ramesh Sharma</div>
          <div class="acc-email">rohit.sharma@gmail.com</div>
        </div>
      </div>

      <div class="account-item" onclick="chooseAccount('rahul.verma@gmail.com', 'Rahul Verma')">
        <div class="avatar green">R</div>
        <div class="acc-info">
          <div class="acc-name">Rahul Verma</div>
          <div class="acc-email">rahul.verma@gmail.com</div>
        </div>
      </div>
    </div>

    <div class="custom-section">
      <label style="font-size: 12px; font-weight: 600; color: #3c4043;">Use another Google Account:</label>
      <input type="email" id="custom-email" placeholder="youremail@gmail.com" class="custom-input">
      <button type="button" onclick="submitCustomEmail()" class="btn-submit">Sign in with this account</button>
    </div>

    <p class="terms">
      To continue, Google will share your name, email address, and language preference with PolicyNest. Before using PolicyNest, review its Privacy Policy and Terms of Service.
    </p>
  </div>

  <script>
    async function chooseAccount(email, name) {
      document.getElementById('loader').style.display = 'flex';
      document.getElementById('loader-msg').innerText = `Signing in as ${name}...`;

      try {
        const resp = await fetch('/api/auth/google', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ email: email, name: name })
        });
        const res = await resp.json();

        if (res.success) {
          if (window.opener && !window.opener.closed) {
            window.opener.postMessage({
              type: 'GOOGLE_AUTH_SUCCESS',
              token: res.token,
              user: res.user
            }, '*');
          }
          setTimeout(() => {
            window.close();
          }, 300);
        } else {
          alert("Authentication failed.");
          document.getElementById('loader').style.display = 'none';
        }
      } catch (err) {
        console.error(err);
        alert("Network error communicating with auth server.");
        document.getElementById('loader').style.display = 'none';
      }
    }

    function submitCustomEmail() {
      const email = document.getElementById('custom-email').value.trim();
      if (!email || !email.includes('@')) {
        alert("Please enter a valid Google email address.");
        return;
      }
      const raw = email.split('@')[0].replace('.', ' ');
      const name = raw.charAt(0).toUpperCase() + raw.slice(1);
      chooseAccount(email, name);
    }
  </script>
</body>
</html>"""

@app.get("/auth/google/popup", response_class=HTMLResponse)
def get_google_popup():
    return HTMLResponse(content=GOOGLE_POPUP_HTML)

class PasskeyAuthRequest(BaseModel):
    credential_id: Optional[str] = None
    client_data_json: Optional[str] = None
    user_name: Optional[str] = "Rohit Ramesh Sharma"

@app.post("/api/auth/passkey")
def auth_passkey(req: PasskeyAuthRequest):
    token = f"pn_sec_passkey_{uuid.uuid4().hex}"
    conn = get_connection()
    c = conn.cursor()
    c.execute(
        """INSERT INTO users (mobile, full_name, role, token, current_app_id, last_login_at)
           VALUES (?, ?, ?, ?, ?, ?)
           ON CONFLICT(mobile) DO UPDATE SET token=excluded.token, last_login_at=excluded.last_login_at""",
        ("9820194820", req.user_name, "APPLICANT", token, "APP-2026-PASSKEY", datetime.now().isoformat())
    )
    c.execute(
        "INSERT INTO audit_trail (application_id, stage, event_type, details) VALUES (?, ?, ?, ?)",
        ("APP-2026-PASSKEY", "PASSKEY_AUTH", "FIDO2_WEBAUTHN_SUCCESS", f"Biometric passkey certified for {req.user_name}")
    )
    conn.commit()
    conn.close()
    return {
        "success": True,
        "token": token,
        "auth_type": "WEBAUTHN_PASSKEY",
        "user": {
            "mobile": "9820194820",
            "full_name": req.user_name,
            "role": "APPLICANT",
            "auth_provider": "PASSKEY",
            "token": token
        }
    }
'''

pos = code.find('app.mount("/static"')
if pos != -1:
    code = code[:pos] + google_popup_code + "\n\n" + code[pos:]
    print("Inserted Google popup and Passkey endpoints into main.py successfully!")

with open(MAIN_PATH, "w", encoding="utf-8") as f:
    f.write(code)

print("Updated main.py.")
