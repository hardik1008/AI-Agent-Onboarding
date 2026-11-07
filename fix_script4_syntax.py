with open(r"C:\Users\vajja\Desktop\PolicyNest_AI_Suite\extracted_script_4.js", "r", encoding="utf-8") as f:
    text = f.read()

target = """    // Real 2FA Telecom DLT Flow
    async function sendRealOTP() {
      const mob = document.getElementById('input-mobile').value.trim();
      if (mob.length !== 10) {
        alert("Please enter a valid 10-digit mobile number first.");
        return;
      }"""

replacement = """    // Real 2FA Telecom DLT Flow
    function sendRealOTP() {
      const mob = document.getElementById('input-mobile').value.trim();
      openMobileAuthModal('APPLICANT');
      if (mob && mob.length === 10) {
        document.getElementById('auth-modal-mobile-input').value = mob;
        requestAuthOTP();
      }
    }"""

if target in text:
    text = text.replace(target, replacement, 1)
    print("Replaced sendRealOTP successfully.")
else:
    print("Target not found in extracted_script_4.js")

with open(r"C:\Users\vajja\Desktop\PolicyNest_AI_Suite\extracted_script_4.js", "w", encoding="utf-8") as f:
    f.write(text)
