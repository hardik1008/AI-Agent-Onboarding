INDEX_PATH = r"C:\Users\vajja\Desktop\PolicyNest_AI_Suite\static\index.html"

with open(INDEX_PATH, "r", encoding="utf-8") as f:
    html = f.read()

# 1. Add id="slot-countdown-timer" to the Consumer Enrollment Banner
old_banner_fast_track = '<p class="text-xs font-bold text-emerald-400">Paperless e-KYC Enabled</p>'
new_banner_fast_track = '<p class="text-xs font-bold text-emerald-400">Paperless e-KYC Enabled · <span id="slot-countdown-timer" class="font-mono text-amber-300">14:58</span></p>'

if old_banner_fast_track in html:
    html = html.replace(old_banner_fast_track, new_banner_fast_track, 1)
    print("Added slot-countdown-timer")

# 2. Add id="ai-stat-acc" and id="ai-stat-cv" and id="ticker-accuracy" in view-ai
old_kpi_block = """<!-- KEY BUSINESS & SLA IMPACT CARDS -->
      <div class="grid grid-cols-2 md:grid-cols-4 gap-4">
        <div class="bg-white border border-slate-200 rounded-2xl p-5 shadow-sm space-y-1">
          <div class="flex items-center justify-between">
            <p class="text-xs font-bold text-slate-400 uppercase">Overall SLA Impact</p>
            <span class="text-[10px] bg-emerald-100 text-emerald-800 font-bold px-1.5 py-0.5 rounded">-44% Floor</span>
          </div>
          <p class="text-2xl font-black text-slate-900 font-mono">8.4d ➔ 4.7d</p>
          <p class="text-[11px] text-emerald-600 font-bold">3.7 Days Shaved per Advisor</p>
        </div>

        <div class="bg-white border border-slate-200 rounded-2xl p-5 shadow-sm space-y-1">
          <div class="flex items-center justify-between">
            <p class="text-xs font-bold text-slate-400 uppercase">Annual Ops Savings</p>
            <span class="text-[10px] bg-emerald-100 text-emerald-800 font-bold px-1.5 py-0.5 rounded">&gt;80% Cut</span>
          </div>
          <p class="text-2xl font-black text-emerald-600 font-mono">₹11.9 Lakhs</p>
          <p class="text-[11px] text-slate-500">22 Reviewers @ ₹430/hr Saved</p>
        </div>

        <div class="bg-white border border-slate-200 rounded-2xl p-5 shadow-sm space-y-1">
          <div class="flex items-center justify-between">
            <p class="text-xs font-bold text-slate-400 uppercase">Straight-Through STP</p>
            <span class="text-[10px] bg-indigo-100 text-brand-700 font-bold px-1.5 py-0.5 rounded">Zero Touch</span>
          </div>
          <p class="text-2xl font-black text-brand-600 font-mono">60.7%</p>
          <p class="text-[11px] text-slate-500">364 of 600 Verified Apps STP</p>
        </div>

        <div class="bg-white border border-slate-200 rounded-2xl p-5 shadow-sm space-y-1">
          <div class="flex items-center justify-between">
            <p class="text-xs font-bold text-slate-400 uppercase">Disqualification Recall</p>
            <span class="text-[10px] bg-rose-100 text-rose-800 font-bold px-1.5 py-0.5 rounded">Zero Slip</span>
          </div>
          <p class="text-2xl font-black text-rose-600 font-mono" id="ai-stat-recall">100.0%</p>
          <p class="text-[11px] text-slate-500">All Underage & Corporate Blocked</p>
        </div>
      </div>"""

new_kpi_block = """<!-- KEY BUSINESS & SLA IMPACT CARDS -->
      <div class="grid grid-cols-2 md:grid-cols-4 gap-4">
        <div class="bg-white border border-slate-200 rounded-2xl p-5 shadow-sm space-y-1">
          <div class="flex items-center justify-between">
            <p class="text-xs font-bold text-slate-400 uppercase">Model Accuracy</p>
            <span class="text-[10px] bg-emerald-100 text-emerald-800 font-bold px-1.5 py-0.5 rounded">Random Forest</span>
          </div>
          <p class="text-2xl font-black text-emerald-600 font-mono" id="ai-stat-acc">97.5%</p>
          <p class="text-[11px] text-slate-500">5-Fold CV Mean: <strong class="text-brand-700" id="ai-stat-cv">95.17%</strong></p>
        </div>

        <div class="bg-white border border-slate-200 rounded-2xl p-5 shadow-sm space-y-1">
          <div class="flex items-center justify-between">
            <p class="text-xs font-bold text-slate-400 uppercase">Annual Ops Savings</p>
            <span class="text-[10px] bg-emerald-100 text-emerald-800 font-bold px-1.5 py-0.5 rounded">&gt;80% Cut</span>
          </div>
          <p class="text-2xl font-black text-emerald-600 font-mono">₹11.9 Lakhs</p>
          <p class="text-[11px] text-slate-500">22 Reviewers @ ₹430/hr Saved</p>
        </div>

        <div class="bg-white border border-slate-200 rounded-2xl p-5 shadow-sm space-y-1">
          <div class="flex items-center justify-between">
            <p class="text-xs font-bold text-slate-400 uppercase">Overall SLA Impact</p>
            <span class="text-[10px] bg-indigo-100 text-brand-700 font-bold px-1.5 py-0.5 rounded">-44% Floor</span>
          </div>
          <p class="text-2xl font-black text-slate-900 font-mono">8.4d ➔ 4.7d</p>
          <p class="text-[11px] text-emerald-600 font-bold">3.7 Days Shaved per Advisor</p>
        </div>

        <div class="bg-white border border-slate-200 rounded-2xl p-5 shadow-sm space-y-1">
          <div class="flex items-center justify-between">
            <p class="text-xs font-bold text-slate-400 uppercase">Disqualification Recall</p>
            <span class="text-[10px] bg-rose-100 text-rose-800 font-bold px-1.5 py-0.5 rounded">Zero Slip</span>
          </div>
          <p class="text-2xl font-black text-rose-600 font-mono" id="ai-stat-recall">100.0%</p>
          <p class="text-[11px] text-slate-500">All Underage & Corporate Blocked</p>
        </div>
      </div>

      <!-- Hidden ticker-accuracy anchor for background update compatibility -->
      <span id="ticker-accuracy" class="hidden">97.5%</span>"""

if old_kpi_block in html:
    html = html.replace(old_kpi_block, new_kpi_block, 1)
    print("Updated KPI cards with ai-stat-acc, ai-stat-cv, ticker-accuracy")

# 3. Add DOMContentLoaded for initAuthSession
target_script_top = "lucide.createIcons();\n\n    let activePortal = 'applicant';"
new_script_top = """lucide.createIcons();

    document.addEventListener('DOMContentLoaded', () => {
      initAuthSession();
      const otpBoxes = document.querySelectorAll('.otp-box');
      otpBoxes.forEach((box, idx) => {
        box.addEventListener('input', (e) => {
          const val = e.target.value;
          if (val.length === 1 && idx < otpBoxes.length - 1) {
            otpBoxes[idx + 1].focus();
          }
        });

        box.addEventListener('keydown', (e) => {
          if (e.key === 'Backspace' && !box.value && idx > 0) {
            otpBoxes[idx - 1].focus();
          }
        });

        box.addEventListener('paste', (e) => {
          e.preventDefault();
          const pasteData = (e.clipboardData || window.clipboardData).getData('text').trim();
          const digits = pasteData.replace(/\\D/g, '').slice(0, 6);
          digits.split('').forEach((d, i) => {
            if (otpBoxes[i]) otpBoxes[i].value = d;
          });
          if (otpBoxes[Math.min(digits.length, 5)]) {
            otpBoxes[Math.min(digits.length, 5)].focus();
          }
        });
      });
    });

    let activePortal = 'applicant';"""

if target_script_top in html:
    html = html.replace(target_script_top, new_script_top, 1)
    print("Added DOMContentLoaded and OTP box listeners")

with open(INDEX_PATH, "w", encoding="utf-8") as f:
    f.write(html)

print("Saved successfully.")
