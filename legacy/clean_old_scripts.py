import re

html_path = r"C:\Users\vajja\Desktop\PolicyNest_AI_Suite\static\index.html"
with open(html_path, "r", encoding="utf-8") as f:
    text = f.read()

# Replace sendRealOTP and autoFillOTPFromSMS
pattern_otp = r'    // Real SMS OTP Flow\s*async function sendRealOTP\(\) \{.*?function autoFillOTPFromSMS\(\) \{.*?\n    \}'
replacement_otp = """    // Real 2FA Telecom DLT Flow
    async function sendRealOTP() {
      const mob = document.getElementById('input-mobile').value.trim();
      if (mob.length !== 10) {
        alert("Please enter a valid 10-digit mobile number first.");
        return;
      }
      openMobileAuthModal();
    }"""

text_new = re.sub(pattern_otp, replacement_otp, text, flags=re.DOTALL)
if text_new != text:
    print("OK: Replaced sendRealOTP and autoFillOTPFromSMS")
    text = text_new
else:
    print("FAIL: OTP pattern match failed")

# Replace handleChequeUpload
pattern_cheque = r'    async function handleChequeUpload\(input\) \{.*?    \}'
text_new = re.sub(pattern_cheque, '', text, flags=re.DOTALL)
if text_new != text:
    print("OK: Removed old handleChequeUpload")
    text = text_new
else:
    print("FAIL: Cheque pattern match failed")

with open(html_path, "w", encoding="utf-8") as f:
    f.write(text)
print("Saved clean script replacements")
