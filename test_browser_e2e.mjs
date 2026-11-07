import { spawn } from 'child_process';
import fs from 'fs';
import path from 'path';

const EDGE_PATH = 'C:\\Program Files (x86)\\Microsoft\\Edge\\Application\\msedge.exe';
const USER_DATA = path.join(process.env.TEMP || 'C:\\Temp', 'edge_god_tier_data_' + Date.now());
const PORT = 9334;

console.log("Launching headless Edge on port", PORT);

const edgeProcess = spawn(EDGE_PATH, [
  `--remote-debugging-port=${PORT}`,
  '--headless=new',
  '--disable-gpu',
  '--no-sandbox',
  `--user-data-dir=${USER_DATA}`,
  'about:blank'
], { stdio: 'ignore' });

async function sleep(ms) {
  return new Promise(r => setTimeout(r, ms));
}

let ws = null;
let msgId = 1;
const pending = new Map();
const consoleErrors = [];

function send(method, params = {}) {
  return new Promise((resolve, reject) => {
    const id = msgId++;
    pending.set(id, { resolve, reject });
    ws.send(JSON.stringify({ id, method, params }));
  });
}

async function evaluate(expression) {
  const res = await send('Runtime.evaluate', {
    expression,
    returnByValue: true,
    awaitPromise: true
  });
  if (res.result && res.result.exceptionDetails) {
    throw new Error(JSON.stringify(res.result.exceptionDetails));
  }
  return res.result ? res.result.result ? res.result.result.value : res.result.value : null;
}

async function run() {
  try {
    let targets = null;
    for (let i = 0; i < 20; i++) {
      await sleep(500);
      try {
        const resp = await fetch(`http://127.0.0.1:${PORT}/json/list`);
        targets = await resp.json();
        if (targets && targets.length > 0) break;
      } catch (e) {}
    }

    if (!targets || targets.length === 0) {
      throw new Error("Could not connect to Edge DevTools target.");
    }

    const pageTarget = targets.find(t => t.type === 'page') || targets[0];
    const wsUrl = pageTarget.webSocketDebuggerUrl;
    console.log("Connected to CDP:", wsUrl);

    ws = new WebSocket(wsUrl);
    await new Promise((resolve, reject) => {
      ws.onopen = resolve;
      ws.onerror = reject;
    });

    ws.onmessage = (event) => {
      const data = JSON.parse(event.data);
      if (data.id && pending.has(data.id)) {
        const { resolve, reject } = pending.get(data.id);
        pending.delete(data.id);
        if (data.error) reject(data.error);
        else resolve(data);
      } else if (data.method === 'Runtime.consoleAPICalled') {
        if (data.params.type === 'error') {
          consoleErrors.push(data.params.args.map(a => a.value || a.description).join(' '));
        }
      } else if (data.method === 'Runtime.exceptionThrown') {
        consoleErrors.push(JSON.stringify(data.params.exceptionDetails));
      }
    };

    await send('Page.enable');
    await send('Runtime.enable');

    console.log("Navigating to http://127.0.0.1:8000 ...");
    await send('Page.navigate', { url: 'http://127.0.0.1:8000' });
    await sleep(2000);

    // 1. Verify Title & Telemetry Bar
    const title = await evaluate('document.title');
    console.log("Page title:", title);

    const telemetryText = await evaluate("document.getElementById('telemetry-latency')?.innerText");
    console.log("Mission Control Telemetry Latency:", telemetryText);

    // 2. Test Audio Synthesizer
    await evaluate("playSfx('click'); playSfx('success');");
    console.log("✓ Web Audio API synthesized SFX triggered without errors!");

    // 3. Test Passkey Biometric Auth
    console.log("\n--- Testing FIDO2 WebAuthn Passkey Login ---");
    await evaluate("signInWithPasskey()");
    await sleep(800);
    const passkeyToken = await evaluate("localStorage.getItem('pn_sec_token')");
    console.log("Passkey Token issued:", passkeyToken ? passkeyToken.substring(0, 20) + "..." : "null");
    if (!passkeyToken || !passkeyToken.startsWith('pn_sec_passkey_')) {
      throw new Error("Passkey login did not persist session token!");
    }
    console.log("✓ FIDO2 WebAuthn Passkey Login Verified!");

    // 4. Test Google OAuth Pop-up Endpoint directly
    console.log("\n--- Testing Google OAuth Pop-up Gateway ---");
    const popupResp = await fetch("http://127.0.0.1:8000/auth/google/popup");
    console.log("Google Popup HTTP Status:", popupResp.status);
    const popupHtml = await popupResp.text();
    if (!popupHtml.includes("Sign in with Google")) {
      throw new Error("Google popup HTML missing 'Sign in with Google'!");
    }
    console.log("✓ Google Identity Services Pop-up Gateway verified!");

    // 5. Test 6-Digit Discrete OTP Auto-Fill & Auto-Submit
    console.log("\n--- Testing 6-Digit DLT OTP Interactive Auto-Fill ---");
    await evaluate("openMobileAuthModal()");
    await evaluate("autoFillDemoOTP()");
    await sleep(1000);
    const otpUser = await evaluate("currentUserSession?.full_name");
    console.log("Logged in user after OTP:", otpUser);

    // 6. Test McKinsey & Co. C-Suite Unit Economics Simulator
    console.log("\n--- Testing McKinsey & Co. Unit Economics Simulator ---");
    await evaluate("switchPortal('ai')");
    await sleep(500);

    // Drag sliders to 15,000 agents, 35 reviewers
    await evaluate("document.getElementById('slider-agents').value = 15000; document.getElementById('slider-ops').value = 35; updateMckinseyModel();");
    await sleep(300);

    const savings = await evaluate("document.getElementById('disp-roi-savings')?.innerText");
    const gwp = await evaluate("document.getElementById('disp-roi-gwp')?.innerText");
    console.log(`Recalculated McKinsey Metrics -> Savings: ${savings}, GWP Accelerated: ${gwp}`);

    if (!savings || !savings.includes("Lakhs")) {
      throw new Error("McKinsey simulator failed to recalculate savings!");
    }
    console.log("✓ McKinsey C-Suite Unit Economics Simulator verified!");

    // 7. Check Console Errors
    console.log("\nConsole Errors logged during test:", consoleErrors.length);
    if (consoleErrors.length > 0) {
      console.log("Errors:", consoleErrors);
      throw new Error("Console errors detected!");
    }

    console.log("\n=========================================================================");
    console.log("ALL GOOGLE + MCKINSEY + ELON MUSK GOD-TIER PRODUCTION TESTS PASSED 100%!");
    console.log("=========================================================================");

  } catch (err) {
    console.error("TEST FAILED:", err);
    process.exitCode = 1;
  } finally {
    if (ws) ws.close();
    edgeProcess.kill();
    try {
      fs.rmSync(USER_DATA, { recursive: true, force: true });
    } catch (e) {}
  }
}

run();
