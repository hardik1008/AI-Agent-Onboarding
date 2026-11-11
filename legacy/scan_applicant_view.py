import sys
import re

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding="utf-8")

with open(r"C:\Users\vajja\Desktop\PolicyNest_AI_Suite\static\index.html", "r", encoding="utf-8") as f:
    html = f.read()

# Isolate view-applicant
app_start = html.find('id="view-applicant"')
ops_start = html.find('id="view-ops"')
ai_start = html.find('id="view-ai"')

end_pos = min(pos for pos in [ops_start, ai_start] if pos > app_start)
applicant_view = html[app_start:end_pos]

forbidden_terms = [
    r"\bopencv\b", r"\blaplacian\b", r"\bvariance\b", r"\blatency\b", r"\brulebook\b",
    r"\brandom forest\b", r"\bsqlite\b", r"\bdropped out\b", r"\b482\b",
    r"\bconfusion matrix\b", r"\bstp approved\b"
]

print(f"Scanning applicant view ({len(applicant_view)} chars)...")
total_found = 0
for pattern in forbidden_terms:
    matches = [m.start() for m in re.finditer(pattern, applicant_view, re.IGNORECASE)]
    if matches:
        print(f"Found '{pattern}' {len(matches)} times:")
        for idx in matches:
            snippet = applicant_view[max(0, idx-40):min(len(applicant_view), idx+60)].replace('\n', ' ')
            print(f"   [{idx}]: ...{snippet}...")
        total_found += len(matches)

if total_found == 0:
    print("SUCCESS: 0 forbidden technical terms found in view-applicant!")
else:
    print(f"WARNING: {total_found} terms found.")
