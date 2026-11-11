import sys
import re

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

INDEX_PATH = r"C:\Users\vajja\Desktop\PolicyNest_AI_Suite\static\index.html"

with open(INDEX_PATH, "r", encoding="utf-8") as f:
    html = f.read()

print(f"Loaded index.html: {len(html)} bytes")

# =============================================================================
# 1. ENHANCE TOP TELEMETRY BAR WITH SOUND PRESETS & COMMAND PALETTE SHORTCUT
# =============================================================================
old_telemetry_top = """<!-- ================= ELON MUSK / SPACEX MISSION CONTROL TELEMETRY BAR ================= -->
  <div class="bg-slate-950 text-slate-300 px-4 py-1.5 border-b border-slate-800 text-[11px] font-mono flex items-center justify-between select-none">
    <div class="flex items-center space-x-3 overflow-x-auto whitespace-nowrap">
      <span class="flex items-center space-x-1.5 text-emerald-400 font-bold">
        <span class="w-2 h-2 rounded-full bg-emerald-500 animate-ping inline-block"></span>
        <span>IRDAI POSP ENGINE: NOMINAL</span>
      </span>
      <span class="text-slate-600">|</span>
      <span>SLA: <strong class="text-white">1.2s</strong></span>
      <span class="text-slate-600">|</span>
      <span>ZERO-TOUCH STP: <strong class="text-emerald-400">60.7%</strong></span>
      <span class="text-slate-600">|</span>
      <span>ENCRYPTION: <strong class="text-white">AES-256 / SHA-256</strong></span>
      <span class="text-slate-600">|</span>
      <span>LATENCY: <strong class="text-brand-400" id="telemetry-latency">24ms</strong></span>
    </div>
    <div class="flex items-center space-x-2 flex-shrink-0 ml-2">
      <button type="button" onclick="toggleAudioSfx()" id="btn-toggle-sfx" class="px-2.5 py-0.5 rounded bg-slate-800 hover:bg-slate-700 text-slate-300 text-[10px] flex items-center space-x-1 transition border border-slate-700" title="Toggle Synthesized Haptic Audio">
        <span id="sfx-icon">🔊</span>
        <span id="sfx-label">SFX ON</span>
      </button>
    </div>
  </div>"""

new_telemetry_top = """<!-- ================= ELON MUSK / SPACEX MISSION CONTROL TELEMETRY BAR ================= -->
  <div class="bg-slate-950 text-slate-300 px-4 py-1.5 border-b border-slate-800 text-[11px] font-mono flex items-center justify-between select-none">
    <div class="flex items-center space-x-3 overflow-x-auto whitespace-nowrap">
      <span class="flex items-center space-x-1.5 text-emerald-400 font-bold">
        <span class="w-2 h-2 rounded-full bg-emerald-500 animate-ping inline-block"></span>
        <span>IRDAI POSP ENGINE: NOMINAL</span>
      </span>
      <span class="text-slate-600">|</span>
      <span>SLA: <strong class="text-white">1.2s</strong></span>
      <span class="text-slate-600">|</span>
      <span>ZERO-TOUCH STP: <strong class="text-emerald-400">60.7%</strong></span>
      <span class="text-slate-600">|</span>
      <span>ENCRYPTION: <strong class="text-white">AES-256 / SHA-256</strong></span>
      <span class="text-slate-600">|</span>
      <span>LATENCY: <strong class="text-brand-400" id="telemetry-latency">24ms</strong></span>
    </div>
    <div class="flex items-center space-x-2 flex-shrink-0 ml-2">
      <!-- Quick SFX Audition Pills -->
      <button type="button" onclick="playSfx('coin')" class="hidden md:inline-flex px-2 py-0.5 rounded bg-amber-950/60 hover:bg-amber-900/80 text-amber-300 text-[10px] border border-amber-800/80 items-center space-x-1 transition" title="Audition Coin Clink SFX">
        <span>🪙 Coin Drop</span>
      </button>
      <button type="button" onclick="playSfx('fanfare'); triggerConfetti();" class="hidden md:inline-flex px-2 py-0.5 rounded bg-purple-950/60 hover:bg-purple-900/80 text-purple-300 text-[10px] border border-purple-800/80 items-center space-x-1 transition" title="Audition Fanfare & Confetti">
        <span>🎉 Fanfare</span>
      </button>
      <button type="button" onclick="openCommandPalette()" class="px-2.5 py-0.5 rounded bg-indigo-950/70 hover:bg-indigo-900 text-indigo-300 text-[10px] border border-indigo-800/80 flex items-center space-x-1 transition" title="Open Quick Command Palette (Ctrl+K)">
        <span>⌘ Palette</span>
        <kbd class="text-[9px] bg-slate-900 px-1 rounded text-slate-400 font-mono">Ctrl+K</kbd>
      </button>
      <button type="button" onclick="toggleAudioSfx()" id="btn-toggle-sfx" class="px-2.5 py-0.5 rounded bg-slate-800 hover:bg-slate-700 text-slate-300 text-[10px] flex items-center space-x-1 transition border border-slate-700" title="Toggle Synthesized Haptic Audio">
        <span id="sfx-icon">🔊</span>
        <span id="sfx-label">SFX ON</span>
      </button>
    </div>
  </div>"""

if old_telemetry_top in html:
    html = html.replace(old_telemetry_top, new_telemetry_top, 1)
    print("1. Upgraded Top Telemetry Bar with Command Palette & SFX audition buttons.")

# =============================================================================
# 2. ADD INTERACTIVE NPCI IMPS CENTRAL SWITCH VISUALIZER IN STEP 2
# =============================================================================
npci_visualizer_html = """<!-- Real-Time Interactive NPCI IMPS Central Switch Pipeline Visualizer -->
              <div class="bg-gradient-to-br from-slate-950 via-slate-900 to-indigo-950 border border-indigo-900/80 rounded-2xl p-5 text-white font-mono space-y-3.5 shadow-lg">
                <div class="flex items-center justify-between text-xs border-b border-slate-800 pb-2.5">
                  <div class="flex items-center space-x-2">
                    <span class="w-2.5 h-2.5 rounded-full bg-emerald-400 animate-pulse"></span>
                    <span class="font-extrabold tracking-wider text-slate-200">NPCI 24x7 IMPS CENTRAL SWITCH PIPELINE</span>
                  </div>
                  <span class="text-[10px] text-emerald-400 bg-emerald-950/80 border border-emerald-800 px-2 py-0.5 rounded">CBS ROUTE ACTIVE</span>
                </div>

                <!-- 4 Interactive Switch Nodes -->
                <div class="grid grid-cols-2 sm:grid-cols-4 gap-2.5 text-center text-[10px]">
                  <div class="p-3 rounded-xl bg-slate-800/80 border border-slate-700/80 space-y-1 transition-all" id="switch-node-1">
                    <div class="text-base">🏛️</div>
                    <p class="font-bold text-slate-200">1. Escrow CBS</p>
                    <p class="text-[9px] text-slate-400">PolicyNest Node</p>
                    <span class="inline-block text-[9px] px-1.5 py-0.2 rounded bg-slate-700 text-slate-300" id="switch-status-1">READY</span>
                  </div>

                  <div class="p-3 rounded-xl bg-slate-800/80 border border-slate-700/80 space-y-1 transition-all" id="switch-node-2">
                    <div class="text-base">⚡</div>
                    <p class="font-bold text-slate-200">2. NPCI Switch</p>
                    <p class="text-[9px] text-slate-400">ISO 8583 Gateway</p>
                    <span class="inline-block text-[9px] px-1.5 py-0.2 rounded bg-slate-700 text-slate-300" id="switch-status-2">STANDBY</span>
                  </div>

                  <div class="p-3 rounded-xl bg-slate-800/80 border border-slate-700/80 space-y-1 transition-all" id="switch-node-3">
                    <div class="text-base">🏦</div>
                    <p class="font-bold text-slate-200">3. Target CBS</p>
                    <p class="text-[9px] text-slate-400" id="switch-target-bank">HDFC Bank API</p>
                    <span class="inline-block text-[9px] px-1.5 py-0.2 rounded bg-slate-700 text-slate-300" id="switch-status-3">STANDBY</span>
                  </div>

                  <div class="p-3 rounded-xl bg-slate-800/80 border border-slate-700/80 space-y-1 transition-all" id="switch-node-4">
                    <div class="text-base">💰</div>
                    <p class="font-bold text-slate-200">4. Settlement</p>
                    <p class="text-[9px] text-slate-400">₹1 Penny Credit</p>
                    <span class="inline-block text-[9px] px-1.5 py-0.2 rounded bg-slate-700 text-slate-300" id="switch-status-4">PENDING</span>
                  </div>
                </div>

                <div class="flex items-center justify-between text-[11px] text-slate-400 pt-1">
                  <span id="npci-live-log">Status: Awaiting Penny Drop execution trigger.</span>
                  <span class="font-mono text-emerald-400 font-bold" id="npci-rrn-live">RRN: --</span>
                </div>
              </div>\n\n              """

pos_penny = html.find('<!-- Penny Drop Card -->')
if pos_penny != -1 and "NPCI 24x7 IMPS CENTRAL SWITCH PIPELINE" not in html:
    html = html[:pos_penny] + npci_visualizer_html + html[pos_penny:]
    print("2. Added NPCI IMPS Central Switch Visualizer in Step 2.")

# =============================================================================
# 3. ADD CYBERPUNK BIOMETRIC FACE MESH HUD IN STEP 3
# =============================================================================
old_webcam_finder = """<div class="relative w-44 h-44 mx-auto rounded-full border-4 border-dashed border-emerald-400 flex items-center justify-center overflow-hidden bg-slate-950">
                  <video id="webcam-stream" autoplay playsinline muted class="hidden w-full h-full object-cover"></video>
                  <img id="selfie-frozen-img" class="hidden absolute inset-0 w-full h-full object-cover">
                  <div id="liveness-radar" class="laser-scan-anim"></div>
                  <i id="webcam-placeholder-icon" data-lucide="user" class="w-24 h-24 text-slate-600"></i>
                  <div class="absolute bottom-2 text-[10px] font-mono bg-black/60 px-2 py-0.5 rounded text-emerald-400">
                    LIVE FEED ACTIVE
                  </div>
                </div>"""

new_webcam_finder = """<div class="relative w-52 h-52 mx-auto rounded-3xl border-2 border-emerald-400/80 flex items-center justify-center overflow-hidden bg-slate-950 shadow-2xl shadow-emerald-500/10">
                  <!-- Cyberpunk Targeting Corners -->
                  <div class="absolute top-2 left-2 w-4 h-4 border-t-2 border-l-2 border-emerald-400 z-20"></div>
                  <div class="absolute top-2 right-2 w-4 h-4 border-t-2 border-r-2 border-emerald-400 z-20"></div>
                  <div class="absolute bottom-2 left-2 w-4 h-4 border-b-2 border-l-2 border-emerald-400 z-20"></div>
                  <div class="absolute bottom-2 right-2 w-4 h-4 border-b-2 border-r-2 border-emerald-400 z-20"></div>

                  <!-- Face Oval Target Reticle -->
                  <div class="absolute inset-4 rounded-full border border-dashed border-emerald-500/40 pointer-events-none z-10 animate-pulse"></div>

                  <video id="webcam-stream" autoplay playsinline muted class="hidden w-full h-full object-cover"></video>
                  <img id="selfie-frozen-img" class="hidden absolute inset-0 w-full h-full object-cover">
                  
                  <!-- Sweeping High-Tech Laser Scan Line -->
                  <div id="liveness-radar" class="laser-scan-anim z-10"></div>
                  
                  <i id="webcam-placeholder-icon" data-lucide="user" class="w-24 h-24 text-slate-600"></i>
                  
                  <!-- Flash Screen Effect for Selfie Snapshot -->
                  <div id="camera-flash-overlay" class="hidden absolute inset-0 bg-white z-30 transition-opacity duration-300 opacity-0"></div>

                  <!-- Real-Time Telemetry Badge -->
                  <div class="absolute bottom-2.5 z-20 text-[9px] font-mono bg-slate-900/90 border border-emerald-500/50 px-2 py-0.5 rounded text-emerald-400 tracking-wider">
                    <span id="face-mesh-telemetry">MESH: 468 PTS · ISO 30107-3 PASS</span>
                  </div>
                </div>"""

if old_webcam_finder in html:
    html = html.replace(old_webcam_finder, new_webcam_finder, 1)
    print("3. Upgraded Step 3 Biometric Finder to Cyberpunk Face Mesh HUD.")

# =============================================================================
# 4. UPGRADE STEP 4 PROVISIONAL CARD TO 3D HOLOGRAPHIC PERSPECTIVE TILT
# =============================================================================
old_posp_card_start = '<div class="max-w-md mx-auto bg-gradient-to-br from-slate-900 via-indigo-950 to-slate-900 text-white p-6 rounded-2xl shadow-2xl border border-indigo-500/30 text-left relative overflow-hidden">'
new_posp_card_start = """<div id="holo-posp-card" onmousemove="handleCardTilt(event, this)" onmouseleave="resetCardTilt(this)" class="max-w-md mx-auto bg-gradient-to-br from-slate-900 via-indigo-950 to-slate-900 text-white p-6 rounded-2xl shadow-2xl border border-indigo-500/30 text-left relative overflow-hidden select-none cursor-pointer" style="transition: transform 0.15s ease-out, box-shadow 0.15s ease-out; transform-style: preserve-3d; will-change: transform;">
              <!-- Dynamic Specular Glare Layer -->
              <div id="card-specular-glare" class="absolute inset-0 pointer-events-none opacity-0 transition-opacity duration-200 z-10" style="background: radial-gradient(circle at 50% 50%, rgba(255,255,255,0.25) 0%, transparent 60%);"></div>"""

if old_posp_card_start in html:
    html = html.replace(old_posp_card_start, new_posp_card_start, 1)
    print("4. Upgraded Step 4 POSP Card to 3D Holographic Perspective Tilt.")

# =============================================================================
# 5. ADD SPOTLIGHT COMMAND PALETTE & FULLSCREEN CONFETTI CANVAS MODALS
# =============================================================================
palette_and_confetti_html = """
  <!-- ================= FULLSCREEN HIGH-PERFORMANCE CONFETTI CANVAS ================= -->
  <canvas id="confetti-canvas" class="pointer-events-none fixed inset-0 z-[9999] w-full h-full hidden"></canvas>

  <!-- ================= SPOTLIGHT COMMAND PALETTE (CTRL+K / CMD+K) ================= -->
  <div id="command-palette-modal" class="hidden fixed inset-0 z-50 flex items-start justify-center pt-24 p-4 modal-backdrop" onclick="if(event.target===this) closeCommandPalette()">
    <div class="bg-slate-900/95 backdrop-blur-xl border border-slate-700/80 rounded-2xl max-w-xl w-full overflow-hidden shadow-2xl shadow-black/80 animate-scale-up text-white font-sans">
      <div class="p-4 border-b border-slate-800 flex items-center space-x-3">
        <i data-lucide="search" class="w-5 h-5 text-brand-400"></i>
        <input type="text" id="palette-search-input" oninput="filterPaletteCommands(this.value)" placeholder="Search commands, stages, test scenarios, or shortcuts..." class="w-full bg-transparent text-sm font-semibold text-white placeholder-slate-500 focus:outline-none">
        <kbd class="text-[10px] bg-slate-800 text-slate-400 px-2 py-0.5 rounded border border-slate-700 font-mono">ESC</kbd>
      </div>

      <div class="p-2 max-h-80 overflow-y-auto space-y-1 text-xs" id="palette-results-list">
        <!-- Quick Jumps -->
        <div onclick="selectPaletteAction('step-0')" class="p-2.5 rounded-xl hover:bg-slate-800/80 cursor-pointer flex items-center justify-between transition">
          <div class="flex items-center space-x-2.5">
            <span class="text-base">🚀</span>
            <div>
              <p class="font-bold text-slate-200">Stage 0: Eligibility Pre-Screen</p>
              <p class="text-[10px] text-slate-400">Age floor & PAN format check</p>
            </div>
          </div>
          <span class="text-[10px] font-mono text-slate-500">Jump → 0</span>
        </div>

        <div onclick="selectPaletteAction('step-1')" class="p-2.5 rounded-xl hover:bg-slate-800/80 cursor-pointer flex items-center justify-between transition">
          <div class="flex items-center space-x-2.5">
            <span class="text-base">⚡</span>
            <div>
              <p class="font-bold text-slate-200">Stage 1: DigiLocker & Identity KYC</p>
              <p class="text-[10px] text-slate-400">MeriPehchaan Govt Gateway pull</p>
            </div>
          </div>
          <span class="text-[10px] font-mono text-slate-500">Jump → 1</span>
        </div>

        <div onclick="selectPaletteAction('step-2')" class="p-2.5 rounded-xl hover:bg-slate-800/80 cursor-pointer flex items-center justify-between transition">
          <div class="flex items-center space-x-2.5">
            <span class="text-base">🏦</span>
            <div>
              <p class="font-bold text-slate-200">Stage 2: Bank Payout & NPCI Penny Drop</p>
              <p class="text-[10px] text-slate-400">IMPS switch & CTS-2010 cheque OCR</p>
            </div>
          </div>
          <span class="text-[10px] font-mono text-slate-500">Jump → 2</span>
        </div>

        <div onclick="selectPaletteAction('step-3')" class="p-2.5 rounded-xl hover:bg-slate-800/80 cursor-pointer flex items-center justify-between transition">
          <div class="flex items-center space-x-2.5">
            <span class="text-base">👤</span>
            <div>
              <p class="font-bold text-slate-200">Stage 3: Biometric Liveness & e-Sign</p>
              <p class="text-[10px] text-slate-400">ISO 30107-3 liveness & Form 1-A</p>
            </div>
          </div>
          <span class="text-[10px] font-mono text-slate-500">Jump → 3</span>
        </div>

        <div onclick="selectPaletteAction('step-4')" class="p-2.5 rounded-xl hover:bg-slate-800/80 cursor-pointer flex items-center justify-between transition">
          <div class="flex items-center space-x-2.5">
            <span class="text-base">🎖️</span>
            <div>
              <p class="font-bold text-slate-200">Stage 4: Provisional Credential (3D Card)</p>
              <p class="text-[10px] text-slate-400">Interactive 3D holographic accreditation</p>
            </div>
          </div>
          <span class="text-[10px] font-mono text-slate-500">Jump → 4</span>
        </div>

        <div onclick="selectPaletteAction('portal-ai')" class="p-2.5 rounded-xl hover:bg-slate-800/80 cursor-pointer flex items-center justify-between transition">
          <div class="flex items-center space-x-2.5">
            <span class="text-base">📊</span>
            <div>
              <p class="font-bold text-slate-200">McKinsey AI Intelligence Deck</p>
              <p class="text-[10px] text-slate-400">Unit economics simulator & Board pitch</p>
            </div>
          </div>
          <span class="text-[10px] font-mono text-slate-500">View AI</span>
        </div>

        <div onclick="selectPaletteAction('portal-ops')" class="p-2.5 rounded-xl hover:bg-slate-800/80 cursor-pointer flex items-center justify-between transition">
          <div class="flex items-center space-x-2.5">
            <span class="text-base">🛡️</span>
            <div>
              <p class="font-bold text-slate-200">Ops Reviewer Cockpit</p>
              <p class="text-[10px] text-slate-400">Manual review queue & live actions</p>
            </div>
          </div>
          <span class="text-[10px] font-mono text-slate-500">View Ops</span>
        </div>

        <div onclick="selectPaletteAction('confetti')" class="p-2.5 rounded-xl hover:bg-slate-800/80 cursor-pointer flex items-center justify-between transition">
          <div class="flex items-center space-x-2.5">
            <span class="text-base">🎉</span>
            <div>
              <p class="font-bold text-amber-400">Launch Confetti Celebration Cannon</p>
              <p class="text-[10px] text-slate-400">Particle physics fanfare burst</p>
            </div>
          </div>
          <span class="text-[10px] font-mono text-slate-500">Trigger</span>
        </div>
      </div>

      <div class="bg-slate-950 px-4 py-2 border-t border-slate-800 flex items-center justify-between text-[10px] text-slate-500 font-mono">
        <span>Tip: Press ESC anytime to exit</span>
        <span>PolicyNest Enterprise Command Engine</span>
      </div>
    </div>
  </div>\n\n"""

pos_body_end = html.find('<!-- Hidden Canvas for Webcam Snapshots -->')
if pos_body_end != -1 and "id=\"command-palette-modal\"" not in html:
    html = html[:pos_body_end] + palette_and_confetti_html + html[pos_body_end:]
    print("5. Added Spotlight Command Palette & Confetti Canvas HTML.")

# =============================================================================
# 6. EXPANDED WEB AUDIO API SYNTHESIZER & MINDBLOWING INTERACTION SCRIPTS
# =============================================================================
expanded_interactions_js = """
    // ================= EXPANDED 8-VOICE WEB AUDIO API SYNTHESIZER =================
    function playSfx(type) {
      if (!isSfxEnabled) return;
      try {
        if (!audioCtx) audioCtx = new (window.AudioContext || window.webkitAudioContext)();
        if (audioCtx.state === 'suspended') audioCtx.resume();
        const now = audioCtx.currentTime;

        if (type === 'click') {
          // Tactile mechanical switch click
          const osc = audioCtx.createOscillator();
          const gain = audioCtx.createGain();
          osc.type = 'triangle';
          osc.frequency.setValueAtTime(1400, now);
          osc.frequency.exponentialRampToValueAtTime(500, now + 0.035);
          gain.gain.setValueAtTime(0.09, now);
          gain.gain.exponentialRampToValueAtTime(0.001, now + 0.035);
          osc.connect(gain);
          gain.connect(audioCtx.destination);
          osc.start(now);
          osc.stop(now + 0.035);
        }
        else if (type === 'coin') {
          // Double metallic coin clink + ringing cash register chime
          [2200, 3300].forEach((freq, i) => {
            const osc = audioCtx.createOscillator();
            const gain = audioCtx.createGain();
            osc.type = 'sine';
            osc.frequency.setValueAtTime(freq, now + i * 0.08);
            gain.gain.setValueAtTime(0.12, now + i * 0.08);
            gain.gain.exponentialRampToValueAtTime(0.001, now + i * 0.08 + 0.4);
            osc.connect(gain);
            gain.connect(audioCtx.destination);
            osc.start(now + i * 0.08);
            osc.stop(now + i * 0.08 + 0.4);
          });
        }
        else if (type === 'scan') {
          // Sci-fi high-tech frequency sweep
          const osc = audioCtx.createOscillator();
          const gain = audioCtx.createGain();
          osc.type = 'sawtooth';
          osc.frequency.setValueAtTime(320, now);
          osc.frequency.exponentialRampToValueAtTime(1280, now + 0.2);
          gain.gain.setValueAtTime(0.05, now);
          gain.gain.exponentialRampToValueAtTime(0.001, now + 0.2);
          osc.connect(gain);
          gain.connect(audioCtx.destination);
          osc.start(now);
          osc.stop(now + 0.2);
        }
        else if (type === 'shutter') {
          // Camera mechanical shutter click
          const osc1 = audioCtx.createOscillator();
          const gain1 = audioCtx.createGain();
          osc1.frequency.setValueAtTime(800, now);
          gain1.gain.setValueAtTime(0.15, now);
          gain1.gain.exponentialRampToValueAtTime(0.001, now + 0.06);
          osc1.connect(gain1);
          gain1.connect(audioCtx.destination);
          osc1.start(now);
          osc1.stop(now + 0.06);

          const osc2 = audioCtx.createOscillator();
          const gain2 = audioCtx.createGain();
          osc2.frequency.setValueAtTime(450, now + 0.08);
          gain2.gain.setValueAtTime(0.12, now + 0.08);
          gain2.gain.exponentialRampToValueAtTime(0.001, now + 0.16);
          osc2.connect(gain2);
          gain2.connect(audioCtx.destination);
          osc2.start(now + 0.08);
          osc2.stop(now + 0.16);
        }
        else if (type === 'whoosh') {
          // Air rush step transition
          const osc = audioCtx.createOscillator();
          const gain = audioCtx.createGain();
          osc.type = 'sine';
          osc.frequency.setValueAtTime(180, now);
          osc.frequency.exponentialRampToValueAtTime(420, now + 0.1);
          osc.frequency.exponentialRampToValueAtTime(120, now + 0.25);
          gain.gain.setValueAtTime(0.08, now);
          gain.gain.exponentialRampToValueAtTime(0.001, now + 0.25);
          osc.connect(gain);
          gain.connect(audioCtx.destination);
          osc.start(now);
          osc.stop(now + 0.25);
        }
        else if (type === 'success') {
          // Golden major triad chord (C5, E5, G5, C6)
          [523.25, 659.25, 783.99, 1046.5].forEach((freq, idx) => {
            const o = audioCtx.createOscillator();
            const g = audioCtx.createGain();
            o.type = 'sine';
            o.connect(g);
            g.connect(audioCtx.destination);
            o.frequency.setValueAtTime(freq, now + idx * 0.05);
            g.gain.setValueAtTime(0.08, now + idx * 0.05);
            g.gain.exponentialRampToValueAtTime(0.001, now + idx * 0.05 + 0.4);
            o.start(now + idx * 0.05);
            o.stop(now + idx * 0.05 + 0.4);
          });
        }
        else if (type === 'fanfare') {
          // Celebratory brass fanfare (C4 -> F4 -> G4 -> C5)
          const notes = [
            { f: 261.63, t: 0, d: 0.15 },
            { f: 349.23, t: 0.15, d: 0.15 },
            { f: 392.00, t: 0.30, d: 0.20 },
            { f: 523.25, t: 0.50, d: 0.60 }
          ];
          notes.forEach(n => {
            const o = audioCtx.createOscillator();
            const g = audioCtx.createGain();
            o.type = 'triangle';
            o.connect(g);
            g.connect(audioCtx.destination);
            o.frequency.setValueAtTime(n.f, now + n.t);
            g.gain.setValueAtTime(0.12, now + n.t);
            g.gain.exponentialRampToValueAtTime(0.001, now + n.t + n.d);
            o.start(now + n.t);
            o.stop(now + n.t + n.d);
          });
        }
      } catch (e) {}
    }

    // ================= 3D HOLOGRAPHIC PERSPECTIVE TILT CARD =================
    function handleCardTilt(e, card) {
      const rect = card.getBoundingClientRect();
      const x = e.clientX - rect.left;
      const y = e.clientY - rect.top;
      const centerX = rect.width / 2;
      const centerY = rect.height / 2;

      // Max tilt 12 degrees
      const rotX = ((centerY - y) / centerY) * 12;
      const rotY = ((x - centerX) / centerX) * 12;

      card.style.transform = `perspective(1000px) rotateX(${rotX.toFixed(2)}deg) rotateY(${rotY.toFixed(2)}deg) scale3d(1.02, 1.02, 1.02)`;

      const glare = document.getElementById('card-specular-glare');
      if (glare) {
        glare.style.opacity = '0.6';
        const pctX = ((x / rect.width) * 100).toFixed(1);
        const pctY = ((y / rect.height) * 100).toFixed(1);
        glare.style.background = `radial-gradient(circle at ${pctX}% ${pctY}%, rgba(255,255,255,0.35) 0%, transparent 60%)`;
      }
    }

    function resetCardTilt(card) {
      card.style.transform = 'perspective(1000px) rotateX(0deg) rotateY(0deg) scale3d(1, 1, 1)';
      const glare = document.getElementById('card-specular-glare');
      if (glare) glare.style.opacity = '0';
    }

    // ================= ZERO-DEPENDENCY VANILLA CONFETTI ENGINE =================
    let confettiActive = false;
    let confettiParticles = [];

    function triggerConfetti() {
      const canvas = document.getElementById('confetti-canvas');
      if (!canvas) return;
      canvas.classList.remove('hidden');
      canvas.width = window.innerWidth;
      canvas.height = window.innerHeight;
      const ctx = canvas.getContext('2d');

      const colors = ['#10b981', '#6366f1', '#f59e0b', '#ec4899', '#3b82f6', '#14b8a6', '#f43f5e'];
      confettiParticles = [];
      for (let i = 0; i < 110; i++) {
        confettiParticles.push({
          x: canvas.width * 0.5 + (Math.random() - 0.5) * 200,
          y: canvas.height * 0.4,
          w: Math.random() * 9 + 5,
          h: Math.random() * 5 + 3,
          color: colors[Math.floor(Math.random() * colors.length)],
          vx: (Math.random() - 0.5) * 18,
          vy: Math.random() * -16 - 6,
          rot: Math.random() * 360,
          rotSpeed: (Math.random() - 0.5) * 14,
          gravity: 0.42,
          drag: 0.96
        });
      }

      if (!confettiActive) {
        confettiActive = true;
        let frames = 0;
        function animateConfetti() {
          ctx.clearRect(0, 0, canvas.width, canvas.height);
          let alive = false;
          confettiParticles.forEach(p => {
            p.vx *= p.drag;
            p.vy *= p.drag;
            p.vy += p.gravity;
            p.x += p.vx;
            p.y += p.vy;
            p.rot += p.rotSpeed;

            if (p.y < canvas.height + 20) {
              alive = true;
              ctx.save();
              ctx.translate(p.x, p.y);
              ctx.rotate((p.rot * Math.PI) / 180);
              ctx.fillStyle = p.color;
              ctx.fillRect(-p.w / 2, -p.h / 2, p.w, p.h);
              ctx.restore();
            }
          });

          frames++;
          if (alive && frames < 240) {
            requestAnimationFrame(animateConfetti);
          } else {
            confettiActive = false;
            canvas.classList.add('hidden');
          }
        }
        requestAnimationFrame(animateConfetti);
      }
    }

    // ================= SPOTLIGHT COMMAND PALETTE ENGINE =================
    function openCommandPalette() {
      playSfx('click');
      const m = document.getElementById('command-palette-modal');
      if (m) {
        m.classList.remove('hidden');
        lucide.createIcons();
        const input = document.getElementById('palette-search-input');
        if (input) {
          input.value = '';
          input.focus();
          filterPaletteCommands('');
        }
      }
    }

    function closeCommandPalette() {
      const m = document.getElementById('command-palette-modal');
      if (m) m.classList.add('hidden');
    }

    function filterPaletteCommands(q) {
      const term = q.toLowerCase();
      const list = document.getElementById('palette-results-list');
      if (!list) return;
      const items = list.querySelectorAll('div[onclick^="selectPaletteAction"]');
      items.forEach(it => {
        const txt = it.innerText.toLowerCase();
        it.style.display = txt.includes(term) ? 'flex' : 'none';
      });
    }

    function selectPaletteAction(action) {
      closeCommandPalette();
      playSfx('click');

      if (action.startsWith('step-')) {
        const stepNum = parseInt(action.replace('step-', ''), 10);
        switchPortal('applicant');
        goToStep(stepNum);
      } else if (action === 'portal-ai') {
        switchPortal('ai');
      } else if (action === 'portal-ops') {
        switchPortal('ops');
      } else if (action === 'confetti') {
        playSfx('fanfare');
        triggerConfetti();
      }
    }

    // Global Key Listener for Ctrl+K, ESC, and Number Jumps
    window.addEventListener('keydown', (e) => {
      if ((e.ctrlKey || e.metaKey) && e.key.toLowerCase() === 'k') {
        e.preventDefault();
        const m = document.getElementById('command-palette-modal');
        if (m && !m.classList.contains('hidden')) {
          closeCommandPalette();
        } else {
          openCommandPalette();
        }
      } else if (e.key === 'Escape') {
        closeCommandPalette();
        closeMobileAuthModal();
        closeGoogleAccountChooser();
        closeDigiLockerModal();
        closePhoneHUD();
      }
    });

    // Animate NPCI Pipeline Nodes during Penny Drop
    const originalExecutePennyDrop = window.executePennyDrop;
    async function executePennyDrop() {
      playSfx('click');
      const acc = document.getElementById('input-acc').value.trim();
      const ifsc = document.getElementById('input-ifsc').value.trim();
      const name = candidateName || "ROHIT RAMESH SHARMA";

      // 1. Animate Node 1
      const n1 = document.getElementById('switch-node-1');
      const s1 = document.getElementById('switch-status-1');
      if (n1 && s1) {
        n1.className = "p-3 rounded-xl bg-emerald-950/80 border-2 border-emerald-400 space-y-1 transition-all shadow-lg shadow-emerald-500/20";
        s1.className = "inline-block text-[9px] px-1.5 py-0.2 rounded bg-emerald-700 text-white font-bold animate-pulse";
        s1.innerText = "DISPATCHING";
      }
      document.getElementById('npci-live-log').innerText = "12:31:02.104 - Remitter Escrow transaction initiated...";
      playSfx('scan');

      // 2. Animate Node 2
      setTimeout(() => {
        const n2 = document.getElementById('switch-node-2');
        const s2 = document.getElementById('switch-status-2');
        if (n2 && s2) {
          n2.className = "p-3 rounded-xl bg-blue-950/80 border-2 border-blue-400 space-y-1 transition-all shadow-lg shadow-blue-500/20";
          s2.className = "inline-block text-[9px] px-1.5 py-0.2 rounded bg-blue-700 text-white font-bold animate-pulse";
          s2.innerText = "ROUTING";
        }
        document.getElementById('npci-live-log').innerText = "12:31:02.248 - NPCI Central Switch validating ISO 8583 message...";
        playSfx('scan');
      }, 350);

      // 3. Animate Node 3
      setTimeout(() => {
        const n3 = document.getElementById('switch-node-3');
        const s3 = document.getElementById('switch-status-3');
        if (n3 && s3) {
          n3.className = "p-3 rounded-xl bg-indigo-950/80 border-2 border-indigo-400 space-y-1 transition-all shadow-lg shadow-indigo-500/20";
          s3.className = "inline-block text-[9px] px-1.5 py-0.2 rounded bg-indigo-700 text-white font-bold animate-pulse";
          s3.innerText = "CBS MATCH";
        }
        document.getElementById('npci-live-log').innerText = "12:31:02.390 - Target Bank CBS verifying account number...";
      }, 700);

      try {
        const resp = await fetch('/api/bank/penny-drop', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ account_number: acc, ifsc_code: ifsc, declared_name: name })
        });
        const res = await resp.json();

        setTimeout(() => {
          // 4. Animate Node 4 & Play Coin Sound!
          const n4 = document.getElementById('switch-node-4');
          const s4 = document.getElementById('switch-status-4');
          if (n4 && s4) {
            n4.className = "p-3 rounded-xl bg-emerald-950/80 border-2 border-emerald-400 space-y-1 transition-all shadow-lg shadow-emerald-500/20";
            s4.className = "inline-block text-[9px] px-1.5 py-0.2 rounded bg-emerald-600 text-white font-bold";
            s4.innerText = "₹1 SETTLED";
          }
          document.getElementById('npci-live-log').innerText = `12:31:02.482 - ₹1 Deposited successfully. Beneficiary: ${res.beneficiary_name}`;
          document.getElementById('npci-rrn-live').innerText = `RRN: ${res.reference_id}`;

          playSfx('coin');

          const btn = document.getElementById('btn-penny');
          if (btn) {
            btn.innerHTML = `✓ ₹1 Verified`;
            btn.className = "px-5 py-2.5 bg-emerald-700 text-white font-bold rounded-xl text-xs flex items-center justify-center space-x-2 transition shadow-md shadow-emerald-500/25 flex-shrink-0 cursor-default";
          }
          document.getElementById('penny-returned-name').innerText = res.beneficiary_name;
          document.getElementById('penny-ref-badge').innerText = `Ref: ${res.reference_id}`;
          document.getElementById('penny-result-box').classList.remove('hidden');

          pushWhatsAppMessage(`🏦 *Bank Mandate Verified:* ₹1 credited via NPCI IMPS. Beneficiary '${res.beneficiary_name}' verified.`);
        }, 1000);

      } catch (err) {
        console.error(err);
      }
    }

    // Enhance captureWebcamSnapshot with Shutter Flash & Camera Sound
    const origCapture = window.captureWebcamSnapshot;
    function captureWebcamSnapshot() {
      playSfx('shutter');
      const flash = document.getElementById('camera-flash-overlay');
      if (flash) {
        flash.classList.remove('hidden');
        flash.style.opacity = '0.9';
        setTimeout(() => {
          flash.style.opacity = '0';
          setTimeout(() => flash.classList.add('hidden'), 300);
        }, 80);
      }
      if (origCapture) origCapture();
      else if (window.takeSelfie) window.takeSelfie();
    }
"""

pos_end_script = html.rfind('</script>')
if pos_end_script != -1:
    html = html[:pos_end_script] + expanded_interactions_js + "\n" + html[pos_end_script:]
    print("6. Added Expanded 8-Voice Synthesizer, 3D Hologram, Confetti, and NPCI Pipeline scripts.")

with open(INDEX_PATH, "w", encoding="utf-8") as f:
    f.write(html)

print("Saved updated index.html successfully.")
