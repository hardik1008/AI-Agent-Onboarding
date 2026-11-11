import sys
sys.stdout.reconfigure(encoding='utf-8')

with open(r"C:\Users\vajja\Desktop\PolicyNest_AI_Suite\static\index.html", "r", encoding="utf-8") as f:
    text = f.read()

import re
m = re.search(r'function loadAIMetrics[\s\S]*?\}', text)
if m:
    print(m.group(0))
