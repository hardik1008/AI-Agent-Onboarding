import sys
sys.stdout.reconfigure(encoding='utf-8')

with open(r"C:\Users\vajja\Desktop\PolicyNest_AI_Suite\static\index.html", "r", encoding="utf-8") as f:
    lines = f.readlines()

for i, l in enumerate(lines):
    if "<script>" in l and i > 500:
        print(f"Body script starts at line {i+1}")
        for j in range(i, min(len(lines), i+35)):
            print(f"  {j+1}: {lines[j]}", end="")
        break
