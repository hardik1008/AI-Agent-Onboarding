import sys
sys.stdout.reconfigure(encoding='utf-8')

with open(r"C:\Users\vajja\Desktop\PolicyNest_AI_Suite\static\index.html", "r", encoding="utf-8") as f:
    lines = f.readlines()

for i in range(2135, min(2200, len(lines))):
    print(f"{i+1}: {lines[i]}", end="")
