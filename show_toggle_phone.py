import sys, re
sys.stdout.reconfigure(encoding='utf-8')

with open(r"C:\Users\vajja\Desktop\PolicyNest_AI_Suite\static\index.html", "r", encoding="utf-8") as f:
    text = f.read()

pos = text.find('function togglePhoneHUD')
print(text[pos:pos+500])
