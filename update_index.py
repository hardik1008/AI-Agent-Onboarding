import re

# Read current index.html
with open(r'C:\Users\vajja\Desktop\PolicyNest_AI_Suite\static\index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# 1. Remove "Quick Demo Fill" from navbar and make header strictly enterprise
old_header_actions = """      <!-- Actions: Quick Demo Fill & WhatsApp -->
      <div class="flex items-center space-x-2.5">
        <button onclick="autoFillRealDemoUser()" class="px-3 py-1.5 bg-brand-50 hover:bg-brand-100 text-brand-700 text-xs font-bold rounded-lg border border-brand-200 transition flex items-center space-x-1.5" title="Auto-populate sample applicant details">
          <i data-lucide="sparkles" class="w-3.5 h-3.5"></i>
          <span>Quick Demo Fill</span>
        </button>

        <button onclick="togglePhoneHUD()" class="relative p-2 rounded-xl bg-emerald-50 text-emerald-700 hover:bg-emerald-100 border border-emerald-200 transition" title="Toggle Two-Way WhatsApp Assistant">
          <i data-lucide="message-square" class="w-4 h-4"></i>
          <span class="absolute -top-1 -right-1 flex h-3 w-3">
            <span class="animate-ping absolute inline-flex h-full w-full rounded-full bg-emerald-400 opacity-75"></span>
            <span class="relative inline-flex rounded-full h-3 w-3 bg-emerald-500"></span>
          </span>
        </button>
      </div>"""

new_header_actions = """      <!-- Enterprise Header Actions -->
      <div class="flex items-center space-x-3">
        <div class="hidden sm:flex items-center space-x-1.5 px-3 py-1 rounded-full bg-emerald-50 border border-emerald-200 text-xs font-bold text-emerald-800">
          <span class="w-2 h-2 rounded-full bg-emerald-500 animate-pulse"></span>
          <span>IRDAI Gateway Active</span>
        </div>

        <button onclick="togglePhoneHUD()" class="relative p-2 rounded-xl bg-emerald-50 text-emerald-700 hover:bg-emerald-100 border border-emerald-200 transition flex items-center space-x-1.5" title="Toggle Two-Way WhatsApp Assistant">
          <i data-lucide="message-square" class="w-4 h-4"></i>
          <span class="text-xs font-bold hidden sm:inline">WhatsApp Bot</span>
          <span class="flex h-2.5 w-2.5 relative">
            <span class="animate-ping absolute inline-flex h-full w-full rounded-full bg-emerald-400 opacity-75"></span>
            <span class="relative inline-flex rounded-full h-2.5 w-2.5 bg-emerald-500"></span>
          </span>
        </button>
      </div>"""

if old_header_actions in html:
    html = html.replace(old_header_actions, new_header_actions)
    print("OK: Replaced header actions")
else:
    print("FAIL: Header actions match failed")

# 2. Fix Step 0: Add standard applicant data link discretely in Step 0
step0_sub_old = """                <h2 class="text-2xl font-extrabold text-slate-900 tracking-tight">Basic Regulatory Eligibility</h2>
                <p class="text-xs text-slate-500 mt-1">
                  We check IRDAI age compliance, PAN category, and broker exclusivity instantly before asking for any document uploads.
                </p>"""

step0_sub_new = """                <h2 class="text-2xl font-extrabold text-slate-900 tracking-tight">Basic Regulatory Eligibility</h2>
                <p class="text-xs text-slate-500 mt-1">
                  We check IRDAI age compliance, PAN category, and broker exclusivity instantly before asking for any document uploads.
                  <span class="text-slate-400">·</span>
                  <button type="button" onclick="loadStandardApplicantData('eligible')" class="text-brand-600 hover:underline font-bold text-[11px]">Auto-fill Verified Candidate Profile</button>
                  <span class="text-slate-400">·</span>
                  <button type="button" onclick="loadStandardApplicantData('underage')" class="text-rose-600 hover:underline font-bold text-[11px]">Test Underage Disqualification</button>
                </p>"""

if step0_sub_old in html:
    html = html.replace(step0_sub_old, step0_sub_new)
    print("OK: Replaced Step 0 subtitle")
else:
    print("FAIL: Step 0 subtitle match failed")

# 3. Fix Document Upload buttons (Replace "Use Sample" with "Generate e-KYC Slip")
html = re.sub(
    r'<button type="button" onclick="loadSampleDoc\(\'pan\'\)" class="text-brand-600 font-bold hover:underline">Use Sample</button>',
    r'<button type="button" onclick="generateDigitalEKycProof(\'pan\')" class="text-brand-600 font-bold hover:underline flex items-center space-x-1"><span>⚡ e-PAN Slip</span></button>',
    html
)
html = re.sub(
    r'<button type="button" onclick="loadSampleDoc\(\'aadhaar\'\)" class="text-brand-600 font-bold hover:underline">Use Sample</button>',
    r'<button type="button" onclick="generateDigitalEKycProof(\'aadhaar\')" class="text-brand-600 font-bold hover:underline flex items-center space-x-1"><span>⚡ e-Aadhaar</span></button>',
    html
)
html = re.sub(
    r'<button type="button" onclick="loadSampleDoc\(\'marksheet\'\)" class="text-brand-600 font-bold hover:underline">Use Sample</button>',
    r'<button type="button" onclick="generateDigitalEKycProof(\'marksheet\')" class="text-brand-600 font-bold hover:underline flex items-center space-x-1"><span>⚡ CBSE Marksheet</span></button>',
    html
)
print("OK: Replaced loadSampleDoc button tags")

# 4. Fix Step 2 Cheque Hardcoded field
old_cheque = """              <div>
                <label class="block text-xs font-bold text-slate-700 uppercase tracking-wider mb-1.5">Cancelled Cheque / Passbook</label>
                <div class="bg-slate-50 border border-slate-300 rounded-xl px-4 py-2.5 text-xs text-slate-600 flex items-center justify-between">
                  <span class="font-mono truncate" id="cheque-filename">cheque_verified.pdf</span>
                  <span class="text-emerald-600 font-bold flex-shrink-0">OCR: 96% Match</span>
                </div>
              </div>"""

new_cheque = """              <div>
                <div class="flex items-center justify-between mb-1.5">
                  <label class="block text-xs font-bold text-slate-700 uppercase tracking-wider">Cancelled Cheque / Bank Proof</label>
                  <span id="badge-doc-cheque" class="text-[10px] bg-slate-100 text-slate-600 font-bold px-2 py-0.5 rounded">Optional if Penny-Drop OK</span>
                </div>
                <div class="relative bg-white border border-slate-300 hover:border-brand-500 rounded-xl px-4 py-2.5 text-xs flex items-center justify-between transition group cursor-pointer">
                  <div class="flex items-center space-x-2 truncate">
                    <i data-lucide="file-text" class="w-4 h-4 text-slate-400 group-hover:text-brand-600"></i>
                    <span class="font-medium text-slate-700 truncate" id="cheque-filename">Upload Cheque / Passbook File</span>
                  </div>
                  <input type="file" accept="image/*,.pdf" onchange="handleChequeUpload(this)" class="absolute inset-0 opacity-0 cursor-pointer">
                  <span class="text-[10px] font-bold text-brand-600 group-hover:underline flex-shrink-0">Browse</span>
                </div>
                <p class="text-[11px] text-slate-500 mt-1">Rulebook §4.1: Penny-drop verified accounts do not mandate hardcopy cheque.</p>
              </div>"""

if old_cheque in html:
    html = html.replace(old_cheque, new_cheque)
    print("OK: Replaced hardcoded cheque field")
else:
    print("FAIL: Cheque field match failed")

# 5. Fix Congratulations Sachin in Step 4
html = html.replace(
    '<h2 class="text-3xl font-extrabold text-slate-900 tracking-tight" id="disp-congrats-header">Congratulations, Sachin!</h2>',
    '<h2 class="text-3xl font-extrabold text-slate-900 tracking-tight" id="disp-congrats-header">Congratulations!</h2>'
)
print("OK: Replaced Congratulations, Sachin!")

# 6. Fix "mock exam" in LMS Step 5
html = html.replace(
    'Complete the 5 regulatory modules and pass the 5-question mock exam to receive your official IRDAI License.',
    'Complete the 5 regulatory modules and pass the 5-question IRDAI Mandatory Certification Examination to receive your official IRDAI License.'
)
print("OK: Replaced mock exam text")

# 7. Fix DigiLocker Modal hardcoded PIN & ID
old_dl_inputs = """        <div class="space-y-2">
          <label class="block font-bold text-slate-700">Aadhaar Linked Identity</label>
          <input type="text" id="dl-input-id" value="XXXX-XXXX-9744" disabled class="w-full font-mono bg-slate-100 border border-slate-300 rounded-xl px-4 py-2.5 text-xs font-bold text-slate-700">
        </div>

        <div class="space-y-1.5">
          <label class="block font-bold text-slate-700">6-Digit DigiLocker Security PIN</label>
          <input type="password" id="dl-input-pin" value="123456" maxlength="6" class="w-full text-center tracking-widest font-mono text-sm font-bold bg-white border border-slate-300 rounded-xl px-4 py-2 text-slate-900">
          <p class="text-[10px] text-slate-400">Pre-filled with test PIN 123456.</p>
        </div>"""

new_dl_inputs = """        <div class="space-y-2">
          <label class="block font-bold text-slate-700">Aadhaar / Mobile Linked Identifier</label>
          <input type="text" id="dl-input-id" value="Aadhaar UIDAI Session Linked" disabled class="w-full font-mono bg-slate-100 border border-slate-300 rounded-xl px-4 py-2.5 text-xs font-bold text-slate-700">
        </div>

        <div class="space-y-1.5">
          <label class="block font-bold text-slate-700">6-Digit DigiLocker Security PIN</label>
          <input type="password" id="dl-input-pin" value="123456" maxlength="6" class="w-full text-center tracking-widest font-mono text-sm font-bold bg-white border border-slate-300 rounded-xl px-4 py-2 text-slate-900" placeholder="Enter 6-Digit PIN">
          <p class="text-[10px] text-slate-500">Authorized UIDAI MeriPehchan consent gateway.</p>
        </div>"""

if old_dl_inputs in html:
    html = html.replace(old_dl_inputs, new_dl_inputs)
    print("OK: Replaced DigiLocker inputs")
else:
    print("FAIL: DigiLocker inputs match failed")

with open(r'C:\Users\vajja\Desktop\PolicyNest_AI_Suite\static\index.html', 'w', encoding='utf-8') as f:
    f.write(html)
print("Saved partial update")
