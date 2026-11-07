import sys
sys.stdout.reconfigure(encoding='utf-8')

with open(r"C:\Users\vajja\Desktop\PolicyNest_AI_Suite\static\index.html", "r", encoding="utf-8") as f:
    lines = f.readlines()

for i, l in enumerate(lines):
    if "function goToStep" in l:
        print(f"goToStep found at line {i+1}")
        for j in range(max(0, i-5), min(len(lines), i+45)):
            print(f"{j+1}: {lines[j]}", end="")
        break
