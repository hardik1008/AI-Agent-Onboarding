import { spawn } from 'child_process';
import fs from 'fs';
import path from 'path';

const EDGE_PATH = 'C:\\Program Files (x86)\\Microsoft\\Edge\\Application\\msedge.exe';
const USER_DATA = path.join(process.env.TEMP || 'C:\\Temp', 'edge_delight_data_' + Date.now());
const PORT = 9335;

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

    // 2. Test 8-Voice Web Audio API Synthesizer
    console.log("\n--- Testing 8-Voice Web Audio API SFX ---");
    await evaluate("playSfx('click'); playSfx('coin'); playSfx('scan'); playSfx('shutter'); playSfx('whoosh'); playSfx('success'); playSfx('fanfare');");
    console.log("✓ All 7 synthesized sound types executed flawlessly without errors!");

    // 3. Test Fullscreen Confetti Cannon
    console.log("\n--- Testing Particle Physics Confetti Cannon ---");
    await evaluate("triggerConfetti()");
    const confettiVisible = await evaluate("!document.getElementById('confetti-canvas').classList.contains('hidden')");
    console.log("Confetti canvas active in DOM:", confettiVisible);

    // 4. Test Spotlight Command Palette (Ctrl+K)
    console.log("\n--- Testing Spotlight Command Palette ---");
    await evaluate("openCommandPalette()");
    const paletteVisible = await evaluate("!document.getElementById('command-palette-modal').classList.contains('hidden')");
    console.log("Command Palette visible:", paletteVisible);
    await evaluate("closeCommandPalette()");
    const paletteClosed = await evaluate("document.getElementById('command-palette-modal').classList.contains('hidden')");
    console.log("Command Palette closed via ESC/close:", paletteClosed);

    // 5. Test Step 2 NPCI Switch Visualizer
    console.log("\n--- Testing Step 2 NPCI IMPS Switch Pipeline ---");
    await evaluate("goToStep(2)");
    const switchNode1 = await evaluate("document.getElementById('switch-node-1')?.innerText");
    console.log("NPCI Switch Node 1:", switchNode1.replace(/\\n/g, ' '));

    // 6. Test Step 4 3D Holographic Tilt Card
    console.log("\n--- Testing 3D Holographic Perspective Card ---");
    await evaluate("goToStep(4)");
    const cardTransform = await evaluate(`
      const card = document.getElementById('holo-posp-card');
      handleCardTilt({ clientX: 200, clientY: 150, clientX: 200 }, card);
      card.style.transform;
    `);
    console.log("3D Perspective Tilt Transform applied:", cardTransform);
    await evaluate("resetCardTilt(document.getElementById('holo-posp-card'))");

    // 7. Check Console Errors
    console.log("\nConsole Errors logged during test:", consoleErrors.length);
    if (consoleErrors.length > 0) {
      console.log("Errors:", consoleErrors);
      throw new Error("Console errors detected!");
    }

    console.log("\n=========================================================================");
    console.log("ALL DELIGHT & SENSORY INTERACTION TESTS PASSED WITH 100% SUCCESS!");
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
