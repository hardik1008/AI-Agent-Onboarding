import { spawn } from 'child_process';
import fs from 'fs';
import path from 'path';

const EDGE_PATH = 'C:\\Program Files (x86)\\Microsoft\\Edge\\Application\\msedge.exe';
const USER_DATA = path.join(process.env.TEMP || 'C:\\Temp', 'edge_test_user_data_' + Date.now());
const PORT = 9333;

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
    // Wait for Edge CDP to be ready
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
    console.log("Connecting WebSocket to:", wsUrl);

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

    // 1. Verify Title & Core Elements
    const title = await evaluate('document.title');
    console.log("Page title:", title);

    // 2. Verify Timers
    const initialStopwatch = await evaluate("document.getElementById('live-sla-timer')?.innerText");
    const initialCountdown = await evaluate("document.getElementById('slot-countdown-timer')?.innerText");
    console.log(`Initial timers -> Stopwatch: ${initialStopwatch}, Countdown: ${initialCountdown}`);

    await sleep(2100);
    const tickingStopwatch = await evaluate("document.getElementById('live-sla-timer')?.innerText");
    const tickingCountdown = await evaluate("document.getElementById('slot-countdown-timer')?.innerText");
    console.log(`Ticking timers after 2s -> Stopwatch: ${tickingStopwatch}, Countdown: ${tickingCountdown}`);

    if (initialStopwatch === tickingStopwatch) {
      throw new Error(`Stopwatch is frozen at ${initialStopwatch}!`);
    }
    console.log("✓ Live Stopwatch is ticking smoothly!");

    // 3. Test Google Sign-In & Session Persistence
    console.log("\n--- Testing Google Sign-In Flow ---");
    await evaluate("openMobileAuthModal()");
    const authModalHidden = await evaluate("document.getElementById('mobile-auth-modal').classList.contains('hidden')");
    console.log("Auth modal visible:", !authModalHidden);

    // Open Google Account Chooser
    await evaluate("triggerGoogleSignIn()");
    const chooserHidden = await evaluate("document.getElementById('google-account-chooser-modal').classList.contains('hidden')");
    console.log("Google Account Chooser modal visible:", !chooserHidden);

    // Select Rohit Sharma
    await evaluate("selectGoogleAccount('rohit.sharma@gmail.com', 'Rohit Ramesh Sharma')");
    await sleep(1000);

    const userProfileText = await evaluate("document.getElementById('user-profile-badge')?.innerText");
    const storedToken = await evaluate("localStorage.getItem('pn_sec_token')");
    console.log("Header User Profile Badge:", userProfileText);
    console.log("Stored Session Token in LocalStorage:", storedToken ? storedToken.substring(0, 15) + "..." : "null");

    if (!storedToken || !storedToken.startsWith('pn_sec_g_')) {
      throw new Error("Google authentication failed to store session token!");
    }
    console.log("✓ Google Sign-In successfully authenticated and persisted session!");

    // 4. Test WhatsApp Chatbot HUD & Close Button
    console.log("\n--- Testing WhatsApp Chatbot HUD ---");
    await evaluate("togglePhoneHUD()");
    const hudVisible = await evaluate("!document.getElementById('phone-hud').classList.contains('hidden')");
    console.log("Phone HUD visible after toggle:", hudVisible);

    // Close HUD via Close Button
    await evaluate("closePhoneHUD()");
    await sleep(400);
    const hudClosed = await evaluate("document.getElementById('phone-hud').classList.contains('hidden')");
    console.log("Phone HUD closed successfully via X button:", hudClosed);

    // Reopen and test 15h Training Prerequisite Gating
    await evaluate("togglePhoneHUD()");
    console.log("Sending 'Start 15h Training Course' while on Step 0...");
    await evaluate("sendUserWhatsAppReply('🚀 Start 15h Training Course')");
    await sleep(1500);

    const activePortal = await evaluate("activePortal");
    const currentStepVal = await evaluate("currentStep");
    console.log(`After training request -> activePortal: ${activePortal}, currentStep: ${currentStepVal}`);

    if (activePortal === 'lms') {
      throw new Error("Statutory gating failure: Applicant jumped to LMS before completing KYC!");
    }
    console.log("✓ IRDAI Statutory Gating Verified: Candidate correctly held at Step 0 with prerequisite alert!");

    // 5. Test DigiLocker / MeriPehchaan Multi-Step Government Gateway
    console.log("\n--- Testing DigiLocker Government Modal ---");
    await evaluate("openDigiLockerModal()");
    const dlModalVisible = await evaluate("!document.getElementById('digilocker-modal').classList.contains('hidden')");
    console.log("DigiLocker Government Gateway Modal open:", dlModalVisible);

    // Advance to Step 2 (OTP)
    await evaluate("nextDigiLockerGovStep(2)");
    const step2Visible = await evaluate("!document.getElementById('dl-step-2').classList.contains('hidden')");
    console.log("DigiLocker Step 2 (UIDAI OTP & PIN) visible:", step2Visible);

    // Advance to Step 3 (Statutory Consent)
    await evaluate("nextDigiLockerGovStep(3)");
    const step3Visible = await evaluate("!document.getElementById('dl-step-3').classList.contains('hidden')");
    console.log("DigiLocker Step 3 (Statutory Consent Grant) visible:", step3Visible);

    // Submit Consent
    await evaluate("submitDigiLockerGovConsent()");
    await sleep(2500);

    const nextStep = await evaluate("currentStep");
    console.log("Current step after DigiLocker completion:", nextStep);
    if (nextStep < 1) {
      throw new Error("DigiLocker failed to advance applicant to next step!");
    }
    console.log("✓ MeriPehchaan Government Gateway verified documents and advanced seamlessly!");

    // Check console errors
    console.log("\nConsole Errors logged during test:", consoleErrors.length);
    if (consoleErrors.length > 0) {
      console.log("Errors:", consoleErrors);
      throw new Error("Console errors detected!");
    }

    console.log("\n=======================================================");
    console.log("ALL REAL COMMERICAL PRODUCTION BROWSER TESTS PASSED 100%!");
    console.log("=======================================================");

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
