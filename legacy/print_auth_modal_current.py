import sys, re
sys.stdout.reconfigure(encoding='utf-8')

with open(r"C:\Users\vajja\Desktop\PolicyNest_AI_Suite\static\index.html", "r", encoding="utf-8") as f:
    text = f.read()

m = re.search(r'<div id="mobile-auth-modal"[\s\S]*?<!-- ================= GATEWAY PAYLOAD INSPECTION MODAL ================= -->', text)
if m:
    print(m.group(0)[:1500])
