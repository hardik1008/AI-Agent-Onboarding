# Script to verify we have all assets and dependencies ready
import os

static_dir = r"C:\Users\vajja\Desktop\PolicyNest_AI_Suite\static"
index_path = os.path.join(static_dir, "index.html")

with open(index_path, "r", encoding="utf-8") as f:
    content = f.read()

print("Current index.html size:", len(content))
print("Has sms-toast:", "sms-toast" in content)
print("Has digilocker-modal:", "digilocker-modal" in content)
