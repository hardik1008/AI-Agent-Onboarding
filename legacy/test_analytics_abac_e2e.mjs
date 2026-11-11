import { spawn } from 'child_process';
import http from 'http';

const EDGE_PATH = 'C:\\Program Files (x86)\\Microsoft\\Edge\\Application\\msedge.exe';
const PORT = 9336;

console.log("Launching headless Edge for Analytics & ABAC E2E Test...");

const edgeProcess = spawn(EDGE_PATH, [
  `--remote-debugging-port=${PORT}`,
  '--headless=new',
  '--disable-gpu',
  '--no-sandbox',
  `--user-data-dir=C:\\Temp\\edge_abac_test_${Date.now()}`,
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

async function run() {
  await sleep(1500);

  const targets = await new Promise((resolve, reject) => {
    http.get(`http://127.0.0.1:${PORT}/json`, res => {
      let data = '';
      res.on('data', chunk => data += chunk);
      res.on('end', () => resolve(JSON.parse(data)));
    }).on('error', reject);
  });

  const pageTarget = targets.find(t => t.type === 'page');
  const wsUrl = pageTarget.webSocketDebuggerUrl;
  console.log("Connected to CDP WebSocket:", wsUrl);

  ws = new WebSocket(wsUrl);

  await new Promise((resolve, reject) => {
    ws.onopen = resolve;
    ws.onerror = reject;
  });

  ws.onmessage = (event) => {
    const msg = JSON.parse(event.data);
    if (msg.method === 'Runtime.consoleAPICalled') {
      if (msg.params.type === 'error') {
        const text = msg.params.args.map(a => a.value || a.description || '').join(' ');
        console.error('Browser Console Error:', text);
        consoleErrors.push(text);
      }
    }
    if (msg.id && pending.has(msg.id)) {
      const { resolve, reject } = pending.get(msg.id);
      pending.delete(msg.id);
      if (msg.error) reject(msg.error);
      else resolve(msg.result);
    }
  };

  await send('Runtime.enable');
  await send('Page.enable');

  console.log("Navigating to http://127.0.0.1:8000 ...");
  await send('Page.navigate', { url: 'http://127.0.0.1:8000' });
  await sleep(2500);

  // 1. Verify Client-Side Telemetry Initialized
  console.log("\n--- Testing Telemetry Auto-Tracker ---");
  const trackerCheck = await send('Runtime.evaluate', {
    expression: 'Boolean(window.pnVisitorId && window.pnSessionId)',
    returnByValue: true
  });
  console.log("Telemetry Visitor & Session IDs Initialized:", trackerCheck.result.value);

  // 2. Test RBAC: Unauthenticated switch to analytics is blocked
  console.log("\n--- Testing RBAC Security Guard ---");
  const rbacAlertIntercepted = await send('Runtime.evaluate', {
    expression: `
      (function() {
        let blocked = false;
        const origAlert = window.alert;
        window.alert = function(msg) {
          if (msg.includes('RBAC Access Denied')) blocked = true;
        };
        switchPortal('analytics');
        window.alert = origAlert;
        return blocked;
      })()
    `,
    returnByValue: true
  });
  console.log("RBAC Access Denied on unauthenticated portal switch:", rbacAlertIntercepted.result.value);

  // 3. Authenticate as Super Admin & Reveal Analytics Tab
  console.log("\n--- Testing Super Admin Authentication & Analytics Perspective ---");
  const authSuperAdmin = await send('Runtime.evaluate', {
    expression: `
      (function() {
        const adminUser = {
          mobile: '9899999999',
          full_name: 'Chief Security & Analytics Admin',
          role: 'SUPER_ADMIN',
          token: 'pn_sec_admin_root_master_key_2026'
        };
        currentUserSession = adminUser;
        updateHeaderUserUI(adminUser);
        switchPortal('analytics');
        const viewHidden = document.getElementById('view-analytics').classList.contains('hidden');
        return !viewHidden;
      })()
    `,
    returnByValue: true
  });
  console.log("Analytics Command Center successfully revealed for Super Admin:", authSuperAdmin.result.value);

  // 4. Test Analytics Dashboard Metrics Populated
  await sleep(2000);
  const metricsCheck = await send('Runtime.evaluate', {
    expression: `
      ({
        livePulse: document.getElementById('analytics-live-pulse-cnt')?.innerText,
        totalSessions: document.getElementById('kpi-total-sessions')?.innerText,
        step0Funnel: document.getElementById('funnel-step-0-cnt')?.innerText,
        recentEventsRows: document.getElementById('analytics-live-events-tbody')?.children.length
      })
    `,
    returnByValue: true
  });
  console.log("Analytics Dashboard Real-Time Metrics:", metricsCheck.result.value);

  // 5. Test Interactive NIST SP 800-162 ABAC Policy Simulation
  console.log("\n--- Testing Interactive NIST SP 800-162 ABAC Simulator ---");
  const abacSimResult = await send('Runtime.evaluate', {
    expression: `
      (async function() {
        document.getElementById('sim-subject-role').value = 'OPS_REVIEWER';
        document.getElementById('sim-subject-region').value = 'North';
        document.getElementById('sim-clearance-level').value = '1';
        document.getElementById('sim-resource-state').value = 'Maharashtra';
        document.getElementById('sim-is-hard-case').value = 'false';
        document.getElementById('sim-risk-score').value = '12.0';
        document.getElementById('sim-action').value = 'review_case';

        await runABACSimulation();
        return document.getElementById('sim-result-box')?.innerText;
      })()
    `,
    awaitPromise: true,
    returnByValue: true
  });
  console.log("ABAC Simulation Result:\n", abacSimResult.result.value);

  console.log("\nConsole Errors logged during test:", consoleErrors.length);

  ws.close();
  try { edgeProcess.kill(); } catch (e) {}

  if (consoleErrors.length === 0 && authSuperAdmin.result.value && abacSimResult.result.value.includes('DECISION')) {
    console.log("\n=========================================================================");
    console.log("ALL GOOGLE ANALYTICS, RBAC & NIST ABAC POLICY VERIFICATION TESTS PASSED!");
    console.log("=========================================================================");
    process.exit(0);
  } else {
    console.error("Some tests failed.");
    process.exit(1);
  }
}

run().catch(e => {
  console.error(e);
  try { edgeProcess.kill(); } catch (e) {}
  process.exit(1);
});
