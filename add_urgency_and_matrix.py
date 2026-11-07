import re

html_path = r"C:\Users\vajja\Desktop\PolicyNest_AI_Suite\static\index.html"
with open(html_path, "r", encoding="utf-8") as f:
    html = f.read()

# 1. Fast-Track Urgency & Stage-by-Stage SLA Reduction HUD
hud_html = """        <!-- ================= MAIN WORKSPACE ================= -->
        <main class="lg:col-span-8 xl:col-span-8.5 space-y-6">

          <!-- FAST-TRACK URGENCY & STAGE-BY-STAGE SLA REDUCTION HUD -->
          <div class="bg-gradient-to-br from-slate-900 via-indigo-950 to-slate-900 text-white rounded-2xl p-5 shadow-lg border border-indigo-900/60 space-y-4">
            <div class="flex flex-col sm:flex-row sm:items-center justify-between gap-3 border-b border-indigo-900/80 pb-3">
              <div class="flex items-center space-x-3">
                <span class="flex h-3 w-3 relative">
                  <span class="animate-ping absolute inline-flex h-full w-full rounded-full bg-emerald-400 opacity-75"></span>
                  <span class="relative inline-flex rounded-full h-3 w-3 bg-emerald-500"></span>
                </span>
                <div>
                  <div class="flex items-center space-x-2">
                    <span class="text-xs font-black tracking-wider text-emerald-400 uppercase">Accelerated POSP Licensing Slot</span>
                    <span class="text-[10px] bg-emerald-500/20 text-emerald-300 px-2 py-0.5 rounded-full border border-emerald-400/30 font-bold">Fast-Track Active</span>
                  </div>
                  <p class="text-xs text-slate-300 mt-0.5">Complete digital KYC now to bypass the 48-Hour Manual Physical Notary Review.</p>
                </div>
              </div>
              <div class="flex items-center space-x-3 bg-black/40 px-3.5 py-1.5 rounded-xl border border-white/10 self-start sm:self-center">
                <span class="text-[11px] text-slate-400">Slot Expires in:</span>
                <span class="text-sm font-black font-mono text-amber-400" id="slot-countdown-timer">14:58</span>
              </div>
            </div>

            <!-- Stage-by-Stage Time Reduction Pipeline -->
            <div>
              <div class="flex items-center justify-between text-xs mb-2">
                <span class="font-bold text-slate-300">Stage-by-Stage Time Reduction Pipeline (Legacy 8.4 Days ➔ AI 4.7 Days Floor)</span>
                <span class="text-emerald-400 font-bold font-mono">Slashed by 3.7 Days (44% Speedup)</span>
              </div>

              <div class="grid grid-cols-2 sm:grid-cols-3 lg:grid-cols-6 gap-2 text-[10px]">
                <div class="bg-white/5 border border-white/10 rounded-xl p-2.5">
                  <p class="text-slate-400 font-bold uppercase">0. Pre-Screen</p>
                  <p class="text-xs font-black text-emerald-400 font-mono mt-0.5">0.8s <span class="text-slate-500 text-[9px] line-through">1.2d</span></p>
                  <p class="text-slate-400 mt-0.5">Auto-Drops 55%</p>
                </div>

                <div class="bg-white/5 border border-white/10 rounded-xl p-2.5">
                  <p class="text-slate-400 font-bold uppercase">1. DigiLocker KYC</p>
                  <p class="text-xs font-black text-emerald-400 font-mono mt-0.5">35s <span class="text-slate-500 text-[9px] line-through">2.1d</span></p>
                  <p class="text-slate-400 mt-0.5">Crypto Gov Pull</p>
                </div>

                <div class="bg-white/5 border border-white/10 rounded-xl p-2.5">
                  <p class="text-slate-400 font-bold uppercase">2. Bank & Penny</p>
                  <p class="text-xs font-black text-emerald-400 font-mono mt-0.5">1.2s <span class="text-slate-500 text-[9px] line-through">1.8d</span></p>
                  <p class="text-slate-400 mt-0.5">CTS-2010 + IMPS</p>
                </div>

                <div class="bg-white/5 border border-white/10 rounded-xl p-2.5">
                  <p class="text-slate-400 font-bold uppercase">3. Biometrics</p>
                  <p class="text-xs font-black text-emerald-400 font-mono mt-0.5">20s <span class="text-slate-500 text-[9px] line-through">1.4d</span></p>
                  <p class="text-slate-400 mt-0.5">3D Passive Mesh</p>
                </div>

                <div class="bg-white/5 border border-white/10 rounded-xl p-2.5">
                  <p class="text-slate-400 font-bold uppercase">4. STP Decision</p>
                  <p class="text-xs font-black text-emerald-400 font-mono mt-0.5">0.5s <span class="text-slate-500 text-[9px] line-through">17.3h</span></p>
                  <p class="text-slate-400 mt-0.5">Random Forest</p>
                </div>

                <div class="bg-white/5 border border-white/10 rounded-xl p-2.5">
                  <p class="text-slate-400 font-bold uppercase">5. 15h Training</p>
                  <p class="text-xs font-black text-emerald-400 font-mono mt-0.5">0 Drops <span class="text-slate-500 text-[9px] line-through">482</span></p>
                  <p class="text-slate-400 mt-0.5">1-Click SSO Bridge</p>
                </div>
              </div>
            </div>
          </div>"""

target_workspace = """        <!-- ================= MAIN WORKSPACE ================= -->
        <main class="lg:col-span-8 xl:col-span-8.5 space-y-6">"""

if target_workspace in html:
    html = html.replace(target_workspace, hud_html, 1)
    print("OK: Added Fast-Track Urgency & SLA Reduction HUD")
else:
    print("FAIL: target_workspace match failed")

# 2. Add IRDAI 6-Point Statutory Document Verification Matrix inside Step 1
matrix_html = """            <!-- IRDAI 6-POINT STATUTORY VERIFICATION MATRIX -->
            <div class="bg-white border border-slate-200 rounded-2xl p-5 shadow-sm space-y-4">
              <div class="flex flex-col sm:flex-row sm:items-center justify-between gap-2 border-b border-slate-200 pb-3">
                <div class="flex items-center space-x-2">
                  <i data-lucide="layers" class="w-4 h-4 text-brand-600"></i>
                  <h3 class="text-sm font-extrabold text-slate-900">IRDAI 6-Point Statutory Document Verification Matrix</h3>
                </div>
                <span class="text-xs font-mono font-bold text-emerald-700 bg-emerald-50 border border-emerald-200 px-2.5 py-0.5 rounded-full" id="matrix-status-header">
                  Direct Source Verifications Active
                </span>
              </div>

              <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-3 text-xs">
                
                <!-- 1. PAN Card -->
                <div class="p-3 rounded-xl border border-slate-200 bg-slate-50/70 space-y-2" id="matrix-card-pan">
                  <div class="flex items-center justify-between">
                    <span class="font-bold text-slate-900 flex items-center space-x-1.5">
                      <i data-lucide="credit-card" class="w-3.5 h-3.5 text-brand-600"></i>
                      <span>1. PAN Card</span>
                    </span>
                    <span class="text-[10px] font-bold px-2 py-0.5 rounded bg-emerald-100 text-emerald-800" id="matrix-badge-pan">NSDL Verified ✓</span>
                  </div>
                  <p class="text-[11px] text-slate-600">Source: <strong class="text-slate-800">Income Tax Dept / NSDL Protean</strong></p>
                  <div class="text-[10px] font-mono text-slate-500 bg-white p-2 rounded border border-slate-200 space-y-0.5">
                    <p>Category: <strong class="text-slate-800">Individual ('P')</strong></p>
                    <p>Status: <strong class="text-emerald-600">OPERATIVE & LINKED</strong></p>
                    <p>Latency: <span class="text-slate-700">138ms</span> · SHA-256 Valid</p>
                  </div>
                  <button type="button" onclick="inspectGatewayPayload('pan')" class="w-full py-1 text-[11px] font-bold text-brand-600 hover:bg-brand-50 rounded border border-brand-200 transition">Inspect NSDL Payload</button>
                </div>

                <!-- 2. Aadhaar Identity -->
                <div class="p-3 rounded-xl border border-slate-200 bg-slate-50/70 space-y-2" id="matrix-card-aadhaar">
                  <div class="flex items-center justify-between">
                    <span class="font-bold text-slate-900 flex items-center space-x-1.5">
                      <i data-lucide="fingerprint" class="w-3.5 h-3.5 text-emerald-600"></i>
                      <span>2. Aadhaar XML</span>
                    </span>
                    <span class="text-[10px] font-bold px-2 py-0.5 rounded bg-emerald-100 text-emerald-800" id="matrix-badge-aadhaar">UIDAI CIDR ✓</span>
                  </div>
                  <p class="text-[11px] text-slate-600">Source: <strong class="text-slate-800">UIDAI Paperless e-KYC (CIDR)</strong></p>
                  <div class="text-[10px] font-mono text-slate-500 bg-white p-2 rounded border border-slate-200 space-y-0.5">
                    <p>UID: <strong class="text-slate-800" id="matrix-disp-uid">XXXXXXXX9744</strong></p>
                    <p>Signature: <strong class="text-emerald-600">X.509 Chain Verified</strong></p>
                    <p>Latency: <span class="text-slate-700">210ms</span> · Cryptographic</p>
                  </div>
                  <button type="button" onclick="inspectGatewayPayload('aadhaar')" class="w-full py-1 text-[11px] font-bold text-brand-600 hover:bg-brand-50 rounded border border-brand-200 transition">Inspect UIDAI Payload</button>
                </div>

                <!-- 3. Class 10 Marksheet -->
                <div class="p-3 rounded-xl border border-slate-200 bg-slate-50/70 space-y-2" id="matrix-card-marksheet">
                  <div class="flex items-center justify-between">
                    <span class="font-bold text-slate-900 flex items-center space-x-1.5">
                      <i data-lucide="graduation-cap" class="w-3.5 h-3.5 text-indigo-600"></i>
                      <span>3. 10th Marksheet</span>
                    </span>
                    <span class="text-[10px] font-bold px-2 py-0.5 rounded bg-emerald-100 text-emerald-800" id="matrix-badge-marksheet">CBSE Depository ✓</span>
                  </div>
                  <p class="text-[11px] text-slate-600">Source: <strong class="text-slate-800">DigiLocker / CBSE Academic Depository</strong></p>
                  <div class="text-[10px] font-mono text-slate-500 bg-white p-2 rounded border border-slate-200 space-y-0.5">
                    <p>Result: <strong class="text-emerald-600">PASS (Qualified)</strong></p>
                    <p>IRDAI §1.3: <strong class="text-emerald-600">Meets Min Floor</strong></p>
                    <p>Latency: <span class="text-slate-700">320ms</span> · Verified</p>
                  </div>
                  <button type="button" onclick="inspectGatewayPayload('marksheet')" class="w-full py-1 text-[11px] font-bold text-brand-600 hover:bg-brand-50 rounded border border-brand-200 transition">Inspect CBSE Payload</button>
                </div>

                <!-- 4. Cancelled Cheque / Mandate -->
                <div class="p-3 rounded-xl border border-slate-200 bg-slate-50/70 space-y-2" id="matrix-card-cheque">
                  <div class="flex items-center justify-between">
                    <span class="font-bold text-slate-900 flex items-center space-x-1.5">
                      <i data-lucide="landmark" class="w-3.5 h-3.5 text-teal-600"></i>
                      <span>4. Bank CTS-2010</span>
                    </span>
                    <span class="text-[10px] font-bold px-2 py-0.5 rounded bg-emerald-100 text-emerald-800" id="matrix-badge-cheque">NPCI CTS-2010 ✓</span>
                  </div>
                  <p class="text-[11px] text-slate-600">Source: <strong class="text-slate-800">NPCI NACH & IMPS Switch</strong></p>
                  <div class="text-[10px] font-mono text-slate-500 bg-white p-2 rounded border border-slate-200 space-y-0.5">
                    <p>MICR: <strong class="text-slate-800" id="matrix-disp-micr">400240015 (Valid)</strong></p>
                    <p>Penny Drop: <strong class="text-emerald-600">₹1 Settled (99.4% Match)</strong></p>
                    <p>Latency: <span class="text-slate-700">0.8s</span> · CBS Linked</p>
                  </div>
                  <button type="button" onclick="inspectGatewayPayload('cheque')" class="w-full py-1 text-[11px] font-bold text-brand-600 hover:bg-brand-50 rounded border border-brand-200 transition">Inspect NPCI Payload</button>
                </div>

                <!-- 5. Biometric Liveness -->
                <div class="p-3 rounded-xl border border-slate-200 bg-slate-50/70 space-y-2" id="matrix-card-selfie">
                  <div class="flex items-center justify-between">
                    <span class="font-bold text-slate-900 flex items-center space-x-1.5">
                      <i data-lucide="scan-face" class="w-3.5 h-3.5 text-cyan-600"></i>
                      <span>5. Biometric Selfie</span>
                    </span>
                    <span class="text-[10px] font-bold px-2 py-0.5 rounded bg-emerald-100 text-emerald-800" id="matrix-badge-selfie">ISO 30107-3 Pass ✓</span>
                  </div>
                  <p class="text-[11px] text-slate-600">Source: <strong class="text-slate-800">IRDAI Biometric Mesh & OpenCV</strong></p>
                  <div class="text-[10px] font-mono text-slate-500 bg-white p-2 rounded border border-slate-200 space-y-0.5">
                    <p>Anti-Spoofing: <strong class="text-emerald-600">0.985 (Real 3D Face)</strong></p>
                    <p>Photo Match: <strong class="text-emerald-600">94.2% Similarity</strong></p>
                    <p>OpenCV Var: <span class="text-slate-700">1420.5 (Crisp)</span></p>
                  </div>
                  <button type="button" onclick="inspectGatewayPayload('selfie')" class="w-full py-1 text-[11px] font-bold text-brand-600 hover:bg-brand-50 rounded border border-brand-200 transition">Inspect CV Mesh Data</button>
                </div>

                <!-- 6. Form 1-A POSP Agreement -->
                <div class="p-3 rounded-xl border border-slate-200 bg-slate-50/70 space-y-2" id="matrix-card-form1a">
                  <div class="flex items-center justify-between">
                    <span class="font-bold text-slate-900 flex items-center space-x-1.5">
                      <i data-lucide="file-signature" class="w-3.5 h-3.5 text-purple-600"></i>
                      <span>6. Form 1-A e-Sign</span>
                    </span>
                    <span class="text-[10px] font-bold px-2 py-0.5 rounded bg-emerald-100 text-emerald-800" id="matrix-badge-form1a">CCA e-Sign Valid ✓</span>
                  </div>
                  <p class="text-[11px] text-slate-600">Source: <strong class="text-slate-800">Controller of Certifying Authorities (CCA)</strong></p>
                  <div class="text-[10px] font-mono text-slate-500 bg-white p-2 rounded border border-slate-200 space-y-0.5">
                    <p>Digital Certificate: <strong class="text-purple-700">X.509 Timestamped</strong></p>
                    <p>Covenant: <strong class="text-emerald-600">IRDAI Broker Undertaking</strong></p>
                    <p>Signatory: <span class="text-slate-800">Aadhaar OTP Authorized</span></p>
                  </div>
                  <button type="button" onclick="inspectGatewayPayload('form1a')" class="w-full py-1 text-[11px] font-bold text-brand-600 hover:bg-brand-50 rounded border border-brand-200 transition">Inspect CCA Certificate</button>
                </div>

              </div>
            </div>"""

step1_header = """            <div class="flex flex-col sm:flex-row sm:items-center justify-between gap-2 border-b border-slate-200/80 pb-4">
              <div>
                <div class="inline-flex items-center space-x-1.5 px-2.5 py-0.5 rounded-full bg-emerald-50 text-emerald-700 text-xs font-bold border border-emerald-200 mb-2">
                  <i data-lucide="zap" class="w-3.5 h-3.5"></i>
                  <span>Stage 1 · Frictionless Identity Verification</span>
                </div>
                <h2 class="text-2xl font-extrabold text-slate-900 tracking-tight">Identity & Educational Proof</h2>
                <p class="text-xs text-slate-500 mt-1">
                  Connect via DigiLocker (recommended by IRDAI) or upload photos with real-time OpenCV image quality verification.
                </p>
              </div>
              <button onclick="goToStep(0)" class="text-xs text-slate-500 hover:text-slate-800 font-bold flex items-center space-x-1 self-start">
                <i data-lucide="arrow-left" class="w-3.5 h-3.5"></i>
                <span>Back</span>
              </button>
            </div>"""

if step1_header in html:
    html = html.replace(step1_header, step1_header + "\n\n" + matrix_html, 1)
    print("OK: Added 6-Point Statutory Verification Matrix to Step 1")
else:
    print("FAIL: step1_header match failed")

with open(html_path, "w", encoding="utf-8") as f:
    f.write(html)
print("Saved matrix update")
