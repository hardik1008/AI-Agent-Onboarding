import re

with open(r'C:\Users\vajja\Desktop\PolicyNest_AI_Suite\static\index.html', 'r', encoding='utf-8') as f:
    text = f.read()

inputs_with_val = re.findall(r'<input[^>]*\bvalue=["\'][^"\']+["\'][^>]*>', text)
print(f"Inputs with hardcoded value attribute ({len(inputs_with_val)}):")
for inp in inputs_with_val:
    print("  ", inp)

# Check for hardcoded badges or dummy names
names = re.findall(r'(Sachin|Mittal|Sharma|Rahul|Priya|Amit|Sunita|Vansh|Vikram|Rohan)', text, re.IGNORECASE)
print("\nNames found in text:", set(names))

# Check for 'mock', 'dummy', 'fake', 'testable', 'sample'
keywords = ['mock', 'dummy', 'fake', 'testable', 'sample', 'demo fill']
for kw in keywords:
    matches = re.findall(rf'.{{0,40}}{kw}.{{0,40}}', text, re.IGNORECASE)
    print(f"\nKeyword '{kw}' ({len(matches)} occurrences):")
    for m in matches[:5]:
        print("   ...", m.strip().replace('\n', ' '), "...")
