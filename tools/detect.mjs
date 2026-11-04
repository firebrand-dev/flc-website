// Runs Impeccable's design detector over rendered pages of the local preview, one private headless Edge per page.
//
//   node tools/detect.mjs --out build/detect/after --pages /,/es/download/ --sizes 1440x900,390x844
//
// Needs the preview running (python tools/build.py --serve) and the Impeccable skill installed in .claude/skills
// (npx impeccable install). Each page opens in a throwaway Edge profile with its own DevTools port; the detector reads
// it through --cdp, and that Edge process tree is closed afterwards. Writes <out>/<page>__<size>.json and summary.txt.
import { spawn, spawnSync } from 'node:child_process';
import { mkdirSync, writeFileSync, rmSync, existsSync } from 'node:fs';
import { join, resolve } from 'node:path';
import { tmpdir } from 'node:os';

const args = process.argv.slice(2);
const opt = (n, d) => { const i = args.indexOf('--' + n); return i < 0 ? d : args[i + 1]; };
const BASE = opt('base', 'http://localhost:8791');
const OUT = resolve(opt('out', 'build/detect'));
const PAGES = opt('pages', '/').split(',');
const SIZES = opt('sizes', '1440x900').split(',');
const EDGE = ['C:/Program Files (x86)/Microsoft/Edge/Application/msedge.exe', 'C:/Program Files/Google/Chrome/Application/chrome.exe'].find(existsSync);
const LAUNCHER = resolve('.claude/skills/impeccable/scripts/impeccable');
const sleep = (ms) => new Promise((r) => setTimeout(r, ms));

mkdirSync(OUT, { recursive: true });
const summary = [];
let port = 9400 + Math.floor(Math.random() * 400);
for (const page of PAGES) {
  for (const size of SIZES) {
    port += 1;
    const profile = join(tmpdir(), `flc-detect-${process.pid}-${port}`);
    const lang = page.startsWith('/es/') ? 'es' : 'en-US';
    const edge = spawn(EDGE, ['--headless=new', `--remote-debugging-port=${port}`, '--no-first-run', '--disable-extensions',
      '--disable-sync', '--hide-scrollbars', `--lang=${lang}`, `--user-data-dir=${profile}`,
      `--window-size=${size.replace('x', ',')}`, BASE + page], { stdio: 'ignore' });
    for (let i = 0; i < 60; i++) { try { await fetch(`http://127.0.0.1:${port}/json/version`); break; } catch { await sleep(250); } }
    await sleep(3500);
    const r = spawnSync('sh', [LAUNCHER, 'detect', '--json', '--cdp', String(port), '--target', 'localhost'],
      { encoding: 'utf8', env: { ...process.env, DO_NOT_TRACK: '1' } });
    const name = `${(page.replace(/\//g, '_').replace(/^_|_$/g, '') || 'home')}__${size}`;
    let findings = [];
    try { findings = JSON.parse(r.stdout || '[]'); } catch { findings = [{ antipattern: 'detector-output-unreadable', selector: (r.stderr || '').slice(0, 120) }]; }
    writeFileSync(join(OUT, name + '.json'), JSON.stringify(findings, null, 1));
    const line = `${name.padEnd(30)} ${String(findings.length).padStart(2)} | ` +
      findings.map((f) => `${f.antipattern}@${(f.selector || '').slice(0, 50)}`).join('; ');
    console.log(line);
    summary.push(line);
    // Edge re-launches itself, so the spawned pid is not the browser: close every process using this page's profile.
    spawnSync('powershell', ['-NoProfile', '-Command', `Get-CimInstance Win32_Process -Filter "Name='${EDGE.split('/').pop()}'" | ` +
      `Where-Object { $_.CommandLine -like '*${profile.split(/[\\/]/).pop()}*' } | ` +
      'ForEach-Object { Stop-Process -Id $_.ProcessId -Force -ErrorAction SilentlyContinue }'], { stdio: 'ignore' });
    edge.kill();
    await sleep(800);
    try { rmSync(profile, { recursive: true, force: true }); } catch { /* Edge may still hold a lock for a moment */ }
  }
}
writeFileSync(join(OUT, 'summary.txt'), summary.join('\n') + '\n');
