import sys, re
sys.stdout.reconfigure(encoding='utf-8')

with open(r"C:\Users\vajja\Desktop\PolicyNest_AI_Suite\static\index.html", "r", encoding="utf-8") as f:
    text = f.read()

m = re.search(r'<div id="digilocker-modal"[\s\S]*?</div>\s*</div>\s*</div>', text)
if m:
    print(m.group(0)[:1500])
else:
    print("digilocker-modal not matched")
