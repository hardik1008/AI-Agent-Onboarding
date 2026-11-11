import sys
sys.stdout.reconfigure(encoding='utf-8')

with open(r"C:\Users\vajja\Desktop\PolicyNest_AI_Suite\static\index.html", "r", encoding="utf-8") as f:
    lines = f.readlines()

for i in range(2700, min(2760, len(lines))):
    print(f"{i+1}: {lines[i]}", end="")
