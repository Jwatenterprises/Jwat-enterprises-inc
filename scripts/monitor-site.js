// JWAT Site Monitor — runs via Windows Task Scheduler every 30 minutes
// Checks: HTTP 200, page size, JS integrity, Cassidy widget validity

const https = require('https');
const fs = require('fs');
const path = require('path');

const SITE_URL = 'https://www.jwatenterprisesinc.com';
const LOG_FILE = path.join(__dirname, 'monitor.log');
const MIN_PAGE_SIZE = 50000;

function log(msg) {
  const line = `[${new Date().toISOString()}] ${msg}`;
  console.log(line);
  fs.appendFileSync(LOG_FILE, line + '\n', 'utf8');
}

function fetchPage(url) {
  return new Promise((resolve, reject) => {
    https.get(url, { headers: { 'User-Agent': 'JWAT-Monitor/1.0' } }, (res) => {
      if (res.statusCode >= 300 && res.statusCode < 400 && res.headers.location) {
        return fetchPage(res.headers.location).then(resolve).catch(reject);
      }
      let body = '';
      res.on('data', chunk => body += chunk);
      res.on('end', () => resolve({ status: res.statusCode, body }));
    }).on('error', reject);
  });
}

async function runChecks() {
  const issues = [];

  let result;
  try {
    result = await fetchPage(SITE_URL);
  } catch (err) {
    issues.push(`SITE DOWN — could not reach ${SITE_URL}: ${err.message}`);
    report(issues);
    return;
  }

  // Check 1: HTTP 200
  if (result.status !== 200) {
    issues.push(`HTTP ${result.status} — expected 200`);
  }

  // Check 2: Page size
  if (result.body.length < MIN_PAGE_SIZE) {
    issues.push(`Page too small — ${result.body.length} chars (expected >${MIN_PAGE_SIZE}). Content may be missing.`);
  }

  // Check 3: Cassidy widget present
  if (!result.body.includes('cassidy-bubble')) {
    issues.push(`Cassidy chat widget missing from page`);
  }

  // Check 4: JS syntax — scan each inline script block for unterminated strings
  const scriptRegex = /<script(?![^>]*\bsrc\s*=)[^>]*>([\s\S]*?)<\/script>/gi;
  let scriptMatch, scriptIndex = 0;
  const { spawnSync } = require('child_process');
  const os = require('os');
  const tmpDir = fs.mkdtempSync(path.join(os.tmpdir(), 'jwat-monitor-'));

  try {
    while ((scriptMatch = scriptRegex.exec(result.body)) !== null) {
      const code = scriptMatch[1].trim();
      if (!code) continue;
      scriptIndex++;
      const tmpFile = path.join(tmpDir, `block_${scriptIndex}.js`);
      fs.writeFileSync(tmpFile, code, 'utf8');
      const check = spawnSync(process.execPath, ['--check', tmpFile], { encoding: 'utf8' });
      if (check.status !== 0) {
        const errLine = (check.stderr || '').split('\n')[0];
        issues.push(`JS syntax error in script block ${scriptIndex}: ${errLine}`);
      }
    }
  } finally {
    try { fs.rmSync(tmpDir, { recursive: true, force: true }); } catch (_) {}
  }

  // Check 5: Key CTAs present
  if (!result.body.includes('Get Started') && !result.body.includes('Start Free Consultation')) {
    issues.push(`CTA buttons appear to be missing from page`);
  }

  report(issues);
}

function report(issues) {
  if (issues.length === 0) {
    log(`OK — all checks passed`);
    return;
  }

  log(`ALERT — ${issues.length} issue(s) detected:`);
  issues.forEach(i => log(`  ✗ ${i}`));

  // Write alert file so Task Scheduler can trigger a notification
  const alertFile = path.join(__dirname, 'SITE_ALERT.txt');
  const content = [
    `JWAT Site Monitor Alert — ${new Date().toLocaleString()}`,
    `Site: ${SITE_URL}`,
    '',
    'Issues detected:',
    ...issues.map(i => `  • ${i}`),
    '',
    'Action: Visit https://github.com/Jwatenterprises/Jwat-enterprises-inc to check the repo.',
  ].join('\n');

  fs.writeFileSync(alertFile, content, 'utf8');
  log(`Alert written to ${alertFile}`);

  // Windows toast notification via PowerShell
  const { spawnSync } = require('child_process');
  const ps = `
Add-Type -AssemblyName System.Windows.Forms
$notify = New-Object System.Windows.Forms.NotifyIcon
$notify.Icon = [System.Drawing.SystemIcons]::Warning
$notify.Visible = $true
$notify.BalloonTipIcon = 'Warning'
$notify.BalloonTipTitle = 'JWAT Site Alert'
$notify.BalloonTipText = '${issues.length} issue(s) detected on jwatenterprisesinc.com — check monitor.log'
$notify.ShowBalloonTip(10000)
Start-Sleep -Seconds 12
$notify.Dispose()
`.trim();

  spawnSync('powershell', ['-NonInteractive', '-Command', ps], { encoding: 'utf8' });
}

runChecks().catch(err => log(`Monitor error: ${err.message}`));
