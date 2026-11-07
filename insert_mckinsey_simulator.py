with open(r"C:\Users\vajja\Desktop\PolicyNest_AI_Suite\static\index.html", "r", encoding="utf-8") as f:
    html = f.read()

target = "<!-- KEY BUSINESS & SLA IMPACT CARDS -->"
mckinsey_card = """<!-- ================= MCKINSEY & CO. C-SUITE UNIT ECONOMICS & ROI SIMULATOR ================= -->
      <div class="glass-surface rounded-2xl p-6 sm:p-8 space-y-6 shadow-sm border border-slate-200 bg-white">
        <div class="flex flex-col sm:flex-row sm:items-center justify-between gap-3 border-b border-slate-200 pb-4">
          <div>
            <div class="inline-flex items-center space-x-2 px-3 py-0.5 rounded-full bg-blue-50 text-blue-700 text-xs font-bold border border-blue-200 mb-2">
              <i data-lucide="calculator" class="w-3.5 h-3.5"></i>
              <span>McKinsey & Co. Board Advisory Framework</span>
            </div>
            <h3 class="text-xl font-extrabold text-slate-900 tracking-tight">Interactive POSP Broker Unit Economics & ROI Simulator</h3>
            <p class="text-xs text-slate-500 mt-0.5">
              Simulate operational savings, cycle time compression, and early gross written premium (GWP) acceleration based on custom agency scale.
            </p>
          </div>
          <button type="button" onclick="downloadBoardSummary()" class="px-4 py-2 bg-slate-900 hover:bg-slate-800 text-white text-xs font-bold rounded-xl flex items-center space-x-2 transition self-start shadow-sm">
            <i data-lucide="download" class="w-3.5 h-3.5"></i>
            <span>Download Board Summary</span>
          </button>
        </div>

        <!-- Simulator Sliders Grid -->
        <div class="grid grid-cols-1 md:grid-cols-3 gap-6 bg-slate-50/70 p-5 rounded-2xl border border-slate-200">
          <!-- Slider 1: Annual Target -->
          <div class="space-y-2">
            <div class="flex justify-between items-center text-xs">
              <span class="font-bold text-slate-700">Annual New POSP Target:</span>
              <strong class="font-mono text-brand-600 font-black text-sm" id="disp-slider-agents">5,000 Agents</strong>
            </div>
            <input type="range" id="slider-agents" min="500" max="25000" step="500" value="5000" oninput="updateMckinseyModel()" class="w-full h-2 bg-slate-200 rounded-lg appearance-none cursor-pointer accent-brand-600">
            <div class="flex justify-between text-[10px] text-slate-400 font-mono">
              <span>500</span>
              <span>12,500</span>
              <span>25,000</span>
            </div>
          </div>

          <!-- Slider 2: Manual Reviewers -->
          <div class="space-y-2">
            <div class="flex justify-between items-center text-xs">
              <span class="font-bold text-slate-700">Manual Reviewers:</span>
              <strong class="font-mono text-brand-600 font-black text-sm" id="disp-slider-ops">22 Reviewers</strong>
            </div>
            <input type="range" id="slider-ops" min="5" max="50" step="1" value="22" oninput="updateMckinseyModel()" class="w-full h-2 bg-slate-200 rounded-lg appearance-none cursor-pointer accent-brand-600">
            <div class="flex justify-between text-[10px] text-slate-400 font-mono">
              <span>5</span>
              <span>25</span>
              <span>50 (@ ₹430/hr)</span>
            </div>
          </div>

          <!-- Slider 3: Baseline Turnaround -->
          <div class="space-y-2">
            <div class="flex justify-between items-center text-xs">
              <span class="font-bold text-slate-700">Baseline Turnaround:</span>
              <strong class="font-mono text-brand-600 font-black text-sm" id="disp-slider-days">8.4 Days</strong>
            </div>
            <input type="range" id="slider-days" min="5.0" max="15.0" step="0.2" value="8.4" oninput="updateMckinseyModel()" class="w-full h-2 bg-slate-200 rounded-lg appearance-none cursor-pointer accent-brand-600">
            <div class="flex justify-between text-[10px] text-slate-400 font-mono">
              <span>5.0d</span>
              <span>10.0d</span>
              <span>15.0d</span>
            </div>
          </div>
        </div>

        <!-- Live Recalculated Metric Cards -->
        <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
          <div class="p-4 rounded-xl border border-emerald-200 bg-emerald-50/50 space-y-1">
            <span class="text-[10px] font-bold uppercase tracking-wider text-emerald-800">Direct Ops Labor Saved</span>
            <p class="text-2xl font-black text-emerald-700 font-mono" id="disp-roi-savings">₹11.95 Lakhs/yr</p>
            <p class="text-[11px] text-emerald-600">Eliminates 55.9% of routine document review time.</p>
          </div>

          <div class="p-4 rounded-xl border border-blue-200 bg-blue-50/50 space-y-1">
            <span class="text-[10px] font-bold uppercase tracking-wider text-blue-800">Cycle Time Compression</span>
            <p class="text-2xl font-black text-blue-700 font-mono" id="disp-roi-cycletime">8.4d → 4.7d</p>
            <p class="text-[11px] text-blue-600">44.1% reduction in time-to-first-policy issuance.</p>
          </div>

          <div class="p-4 rounded-xl border border-purple-200 bg-purple-50/50 space-y-1">
            <span class="text-[10px] font-bold uppercase tracking-wider text-purple-800">Early GWP Accelerated</span>
            <p class="text-2xl font-black text-purple-700 font-mono" id="disp-roi-gwp">₹4.85 Crores</p>
            <p class="text-[11px] text-purple-600">Additional 3.7 productive selling days per agent.</p>
          </div>

          <div class="p-4 rounded-xl border border-amber-200 bg-amber-50/50 space-y-1">
            <span class="text-[10px] font-bold uppercase tracking-wider text-amber-800">Zero-Touch STP Rate</span>
            <p class="text-2xl font-black text-amber-700 font-mono" id="disp-roi-stp">60.7%</p>
            <p class="text-[11px] text-amber-600">100% statutory adherence to IRDAI §42D rules.</p>
          </div>
        </div>
      </div>\n\n      """

if target in html and "McKinsey & Co. Board Advisory Framework" not in html:
    html = html.replace(target, mckinsey_card + target)
    with open(r"C:\Users\vajja\Desktop\PolicyNest_AI_Suite\static\index.html", "w", encoding="utf-8") as f:
        f.write(html)
    print("Inserted McKinsey Simulator successfully!")
else:
    print("Already inserted or target not found.")
