import sys, re
sys.stdout.reconfigure(encoding='utf-8')

with open(r"C:\Users\vajja\Desktop\PolicyNest_AI_Suite\static\index.html", "r", encoding="utf-8") as f:
    text = f.read()

pos_matrix = text.find('IRDAI 6-Point Statutory Document Verification Matrix')
print(text[pos_matrix:pos_matrix+3500])
