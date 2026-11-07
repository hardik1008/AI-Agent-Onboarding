import re
import os
import sys

INDEX_PATH = r"C:\Users\vajja\Desktop\PolicyNest_AI_Suite\static\index.html"
BACKUP_PATH = r"C:\Users\vajja\Desktop\PolicyNest_AI_Suite\static\index.html.bak"

with open(INDEX_PATH, "r", encoding="utf-8") as f:
    content = f.read()

# Make backup if not exists
if not os.path.exists(BACKUP_PATH):
    with open(BACKUP_PATH, "w", encoding="utf-8") as f_bak:
        f_bak.write(content)
    print("Created backup at index.html.bak")

# ================= 1. CLEAN HEAD SCRIPT =================
# Find the first <script> in <head> containing tailwind.config and strip lines 45-437
pattern_head = r'(<script>\s*tailwind\.config\s*=\s*\{[\s\S]*?\}\s*\}\s*\}\s*\n)([\s\S]*?)(</script>\s*<style>)'

match_head = re.search(pattern_head, content)
if match_head:
    print("Found duplicate script in head, cleaning it...")
    cleaned_head = match_head.group(1) + match_head.group(3)
    content = content[:match_head.start()] + cleaned_head + content[match_head.end():]
    print("Head script cleaned successfully.")
else:
    print("WARNING: Could not find exact head script pattern, checking alternate...")

# ================= 2. ENHANCE HEADER WITH USER AUTHENTICATION PILL =================
target_header_actions = r'<div class="flex items-center space-x-3">\s*<div class="hidden sm:flex items-center space-x-1.5 px-3 py-1 rounded-full bg-emerald-50 border border-emerald-200 text-xs font-bold text-emerald-800">'

replacement_header_actions = """<div class="flex items-center space-x-3">
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

        <!-- User Authentication & Profile Pill -->
        <div id="header-user-container" class="flex items-center pl-1">
          <button id="btn-header-signin" onclick="openMobileAuthModal()" class="px-3.5 py-1.5 bg-brand-600 hover:bg-brand-700 text-white rounded-xl text-xs font-bold flex items-center space-x-1.5 shadow-sm transition">
            <i data-lucide="user" class="w-3.5 h-3.5"></i>
            <span>Sign In / Register</span>
          </button>
          
          <div id="header-user-profile" class="hidden flex items-center space-x-2 bg-slate-50 hover:bg-slate-100 border border-slate-300 px-3 py-1.5 rounded-xl transition">
            <div class="w-7 h-7 rounded-lg bg-brand-600 text-white font-black text-xs flex items-center justify-center shadow-sm" id="header-user-avatar">
              R
            </div>
            <div class="text-left hidden sm:block">
              <p class="text-xs font-bold text-slate-900 leading-tight" id="header-user-name">Rohit Sharma</p>
              <p class="text-[10px] text-brand-700 font-bold uppercase tracking-wider leading-tight" id="header-user-role">POSP Applicant</p>
            </div>
            <button onclick="logoutUser()" class="ml-1 text-slate-400 hover:text-rose-600 p-1 transition" title="Sign Out">
              <i data-lucide="log-out" class="w-3.5 h-3.5"></i>
            </button>
          </div>
        </div>
      </div>"""

if "id=\"header-user-container\"" not in content:
    # replace the header actions block
    pattern_actions = r'<div class="flex items-center space-x-3">\s*<div class="hidden sm:flex items-center space-x-1.5 px-3 py-1 rounded-full bg-emerald-50 border border-emerald-200 text-xs font-bold text-emerald-800">[\s\S]*?</button>\s*</div>'
    match_actions = re.search(pattern_actions, content)
    if match_actions:
        content = content[:match_actions.start()] + replacement_header_actions + content[match_actions.end():]
        print("Header actions replaced with user profile pill.")
    else:
        print("WARNING: Could not match header actions block.")

# ================= 3. DYNAMIC SUB-TICKER =================
old_sub_ticker = r'<!-- ================= SUB-TICKER ================= -->[\s\S]*?<!-- ================= MAIN CONTAINER ================= -->'

new_sub_ticker = """<!-- ================= SUB-TICKER ================= -->
  <div class="bg-gradient-to-r from-slate-900 via-indigo-950 to-slate-900 text-white py-2 px-4 border-b border-indigo-900/50">
    <div id="sub-ticker-content" class="max-w-[1440px] mx-auto flex flex-wrap items-center justify-between text-xs gap-2">
      <div class="flex items-center space-x-3">
        <span class="flex items-center space-x-1.5 text-emerald-400 font-bold">
          <i data-lucide="shield-check" class="w-3.5 h-3.5"></i>
          <span>IRDAI Registered Digital Insurance Broker (Licence #842)</span>
        </span>
        <span class="text-slate-500 hidden sm:inline">|</span>
        <span class="text-slate-300 hidden sm:inline">Trusted by 45,000+ Certified POSP Advisors across India</span>
      </div>
      <div class="flex items-center space-x-4 text-slate-300">
        <span class="flex items-center space-x-1"><i data-lucide="zap" class="w-3.5 h-3.5 text-amber-400"></i><span>100% Paperless DigiLocker e-KYC</span></span>
        <span class="flex items-center space-x-1"><i data-lucide="landmark" class="w-3.5 h-3.5 text-emerald-400"></i><span>Instant Weekly Bank Payouts</span></span>
        <span class="flex items-center space-x-1"><i data-lucide="building" class="w-3.5 h-3.5 text-indigo-400"></i><span>40+ General & Life Insurers</span></span>
      </div>
    </div>
  </div>

  <!-- ================= MAIN CONTAINER ================= -->"""

content = re.sub(old_sub_ticker, new_sub_ticker, content)
print("Sub-ticker replaced with dynamic container.")

# Save intermediate
with open(INDEX_PATH, "w", encoding="utf-8") as f:
    f.write(content)

print("Pass 1 written successfully.")
