with open(r"C:\Users\vajja\Desktop\PolicyNest_AI_Suite\static\index.html", "r", encoding="utf-8") as f:
    lines = f.readlines()

for i, l in enumerate(lines):
    if "initAuthSession" in l:
        print(f"Line {i+1}: {l.strip()}")
        for j in range(max(0, i-5), min(len(lines), i+30)):
            print(f"  {j+1}: {lines[j]}", end="")
        break
