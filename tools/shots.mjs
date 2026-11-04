// Capturas y mediciones de carga en un navegador real (Edge o Chrome sin interfaz), sin dependencias.
//
//   node tools/shots.mjs --root dist --out build/shots/after
//   node tools/shots.mjs --root dist --out build/shots/after --full --pages /,/es/ --views mobile375
//   node tools/shots.mjs --pages all --views mobile320,mobile375,mobile390   (every page; reports overflow and tight headings)
//   node tools/shots.mjs --menu --pages /es/ --views mobile375               (with the mobile menu open)
//
// Sirve --root con un servidor estático propio (con 404.html como respaldo), abre cada página por CDP con caché
// desactivada y guarda: <out>/<vista>__<página>.png y <out>/metrics.json (bytes transferidos por tipo, pedidos,
// FCP, LCP, CLS, desborde horizontal). "--throttle" simula una red móvil lenta (1,6 Mbps, 150 ms) en esa medición.
import { createServer } from 'node:http';
import { readFile, mkdir, writeFile, stat, rm } from 'node:fs/promises';
import { existsSync } from 'node:fs';
import { spawn } from 'node:child_process';
import { join, extname, resolve } from 'node:path';
import { tmpdir } from 'node:os';

const args = process.argv.slice(2);
const opt = (name, def) => { const i = args.indexOf('--' + name); return i < 0 ? def : args[i + 1]; };
const flag = (name) => args.includes('--' + name);

const ROOT = resolve(opt('root', 'dist'));
const OUT = resolve(opt('out', 'build/shots'));
const PORT = Number(opt('port', '8799'));
const FULL = flag('full');
const THROTTLE = flag('throttle');
const SLUGS = ['', 'features/', 'leveling/', 'dungeons/', 'loot-atlas/', 'customization/', 'download/', 'support/', 'changelog/', 'report/', 'faq/', 'credits/'];
const ALL = SLUGS.flatMap((s) => ['/' + s, '/es/' + s]);
const PAGES = opt('pages', '/,/es/,/customization/,/es/customization/,/download/,/es/download/,/features/,/es/features/') === 'all'
  ? ALL : opt('pages', '/,/es/,/customization/,/es/customization/,/download/,/es/download/,/features/,/es/features/').split(',');
const VIEWS_ALL = {
  desktop: { width: 1440, height: 900, dpr: 1, mobile: false },
  mobile320: { width: 320, height: 640, dpr: 2, mobile: true },
  mobile375: { width: 375, height: 812, dpr: 2, mobile: true },
  mobile390: { width: 390, height: 844, dpr: 3, mobile: true },
  tablet768: { width: 768, height: 1024, dpr: 2, mobile: true },
  wide1920: { width: 1920, height: 1080, dpr: 1, mobile: false },
};
const VIEWS = opt('views', 'desktop,mobile375').split(',').map((v) => [v, VIEWS_ALL[v]]);

const TYPES = { '.html': 'text/html; charset=utf-8', '.css': 'text/css', '.js': 'text/javascript', '.svg': 'image/svg+xml',
  '.webp': 'image/webp', '.jpg': 'image/jpeg', '.png': 'image/png', '.woff2': 'font/woff2', '.xml': 'application/xml',
  '.txt': 'text/plain; charset=utf-8', '.json': 'application/json', '.ico': 'image/x-icon' };

async function serve() {
  const server = createServer(async (req, res) => {
    let p = decodeURIComponent(new URL(req.url, 'http://x').pathname);
    let file = join(ROOT, p);
    try { if ((await stat(file)).isDirectory()) file = join(file, 'index.html'); } catch { /* 404 abajo */ }
    let code = 200;
    if (!existsSync(file)) { code = 404; file = join(ROOT, p.startsWith('/es/') ? 'es/404.html' : '404.html'); }
    res.writeHead(code, { 'content-type': TYPES[extname(file)] || 'application/octet-stream', 'cache-control': 'no-store' });
    res.end(await readFile(file));
  });
  await new Promise((ok) => server.listen(PORT, '127.0.0.1', ok));
  return server;
}

function findBrowser() {
  const c = [process.env.BROWSER, 'C:/Program Files (x86)/Microsoft/Edge/Application/msedge.exe',
    'C:/Program Files/Google/Chrome/Application/chrome.exe', '/usr/bin/google-chrome', '/usr/bin/chromium'];
  return c.find((x) => x && existsSync(x));
}

class CDP {
  constructor(ws) { this.ws = ws; this.id = 0; this.wait = new Map(); this.handlers = [];
    ws.onmessage = (e) => { const m = JSON.parse(e.data);
      if (m.id && this.wait.has(m.id)) { const [ok, ko] = this.wait.get(m.id); this.wait.delete(m.id); m.error ? ko(new Error(m.error.message)) : ok(m.result); }
      else this.handlers.forEach((h) => h(m)); }; }
  send(method, params = {}) { const id = ++this.id; this.ws.send(JSON.stringify({ id, method, params }));
    return new Promise((ok, ko) => this.wait.set(id, [ok, ko])); }
  on(h) { this.handlers.push(h); }
  once(method) { return new Promise((ok) => { const h = (m) => { if (m.method === method) { this.handlers = this.handlers.filter((x) => x !== h); ok(m.params); } }; this.handlers.push(h); }); }
}

const sleep = (ms) => new Promise((r) => setTimeout(r, ms));

const VITALS = `(() => { window.__v = { lcp: 0, cls: 0, lcpEl: '' };
  new PerformanceObserver((l) => { for (const e of l.getEntries()) { window.__v.lcp = e.startTime; window.__v.lcpEl = (e.element && (e.element.currentSrc || e.element.tagName)) || ''; } }).observe({ type: 'largest-contentful-paint', buffered: true });
  new PerformanceObserver((l) => { for (const e of l.getEntries()) if (!e.hadRecentInput) { window.__v.cls += e.value; (window.__v.shifts = window.__v.shifts || []).push(e.value.toFixed(4) + ' ' + (e.sources || []).map((x) => x.node ? (x.node.className || x.node.nodeName) : '?').join(',')); } }).observe({ type: 'layout-shift', buffered: true });
})();`;

async function main() {
  const browser = findBrowser();
  if (!browser) throw new Error('No se encontró Edge ni Chrome (variable BROWSER).');
  await mkdir(OUT, { recursive: true });
  const server = await serve();
  const profile = join(tmpdir(), 'flc-shots-' + process.pid);
  const proc = spawn(browser, ['--headless=new', '--remote-debugging-port=9339', '--no-first-run', '--no-default-browser-check',
    '--disable-extensions', '--hide-scrollbars', '--user-data-dir=' + profile, 'about:blank'], { stdio: 'ignore' });
  let target;
  for (let i = 0; i < 50 && !target; i++) {
    try { target = await (await fetch('http://127.0.0.1:9339/json/new?about:blank', { method: 'PUT' })).json(); } catch { await sleep(200); }
  }
  const ws = new WebSocket(target.webSocketDebuggerUrl);
  await new Promise((ok) => (ws.onopen = ok));
  const cdp = new CDP(ws);
  await cdp.send('Page.enable'); await cdp.send('Network.enable'); await cdp.send('Runtime.enable');
  await cdp.send('Network.setCacheDisabled', { cacheDisabled: true });
  await cdp.send('Page.addScriptToEvaluateOnNewDocument', { source: VITALS });
  if (FULL) await cdp.send('Emulation.setEmulatedMedia', { features: [{ name: 'prefers-reduced-motion', value: 'reduce' }] });
  if (THROTTLE) await cdp.send('Network.emulateNetworkConditions', { offline: false, latency: 150, downloadThroughput: 1.6e6 / 8, uploadThroughput: 0.75e6 / 8 });

  const reqs = new Map();
  cdp.on((m) => {
    if (m.method === 'Network.responseReceived') { const r = reqs.get(m.params.requestId) || {}; r.url = m.params.response.url; r.type = m.params.type; reqs.set(m.params.requestId, r); }
    if (m.method === 'Network.loadingFinished') { const r = reqs.get(m.params.requestId) || {}; r.bytes = m.params.encodedDataLength; reqs.set(m.params.requestId, r); }
  });

  const metrics = [];
  for (const [vname, v] of VIEWS) {
    await cdp.send('Emulation.setDeviceMetricsOverride', { width: v.width, height: v.height, deviceScaleFactor: v.dpr, mobile: v.mobile });
    await cdp.send('Emulation.setTouchEmulationEnabled', { enabled: v.mobile });
    for (const page of PAGES) {
      reqs.clear();
      const lang = page.startsWith('/es/') ? 'es-419,es' : 'en-US,en';
      await cdp.send('Emulation.setLocaleOverride', { locale: lang.split(',')[0] }).catch(() => {});
      await cdp.send('Network.setExtraHTTPHeaders', { headers: { 'Accept-Language': lang } });
      // La preferencia de idioma guardada evita que el script de detección redirija la página medida.
      await cdp.send('Page.navigate', { url: `http://127.0.0.1:${PORT}/` });
      await cdp.once('Page.loadEventFired');
      await cdp.send('Runtime.evaluate', { expression: `localStorage.setItem('flc-lang', '${page.startsWith('/es/') ? 'es' : 'en'}')` });
      await cdp.send('Page.navigate', { url: 'about:blank' });
      await sleep(150);
      reqs.clear();
      const t0 = Date.now();
      await cdp.send('Page.navigate', { url: `http://127.0.0.1:${PORT}${page}` });
      await cdp.once('Page.loadEventFired');
      const loadMs = Date.now() - t0;
      await sleep(THROTTLE ? 1500 : 700);
      const firstView = [...reqs.values()].filter((r) => r.url && !r.url.startsWith('data:'));
      const res = (await cdp.send('Runtime.evaluate', { returnByValue: true, expression: `(() => {
        const nav = performance.getEntriesByType('navigation')[0];
        const fcp = performance.getEntriesByName('first-contentful-paint')[0];
        return { fcp: fcp ? Math.round(fcp.startTime) : null, lcp: Math.round(window.__v.lcp), lcpEl: window.__v.lcpEl.replace(location.origin, ''),
          cls: Number(window.__v.cls.toFixed(4)), shifts: window.__v.shifts || [], dcl: Math.round(nav.domContentLoadedEventEnd), load: Math.round(nav.loadEventEnd),
          overflow: document.documentElement.scrollWidth - innerWidth, height: document.documentElement.scrollHeight, url: location.pathname,
          // headings whose longest word does not fit their box (they would overflow, since words are never split)
          tightHeadings: [...document.querySelectorAll('h1, h2, h3')].filter((h) => h.offsetParent && h.clientWidth > 4 && h.scrollWidth > h.clientWidth + 1).map((h) => h.textContent.trim().slice(0, 48)) };
      })()` })).result.value;
      const sum = (list) => list.reduce((a, r) => a + (r.bytes || 0), 0);
      const byType = {};
      for (const r of firstView) { byType[r.type] = (byType[r.type] || 0) + (r.bytes || 0); }
      const name = `${vname}__${(page.replace(/\//g, '_').replace(/^_|_$/g, '') || 'home')}`;
      let shot;
      if (flag('menu')) { await cdp.send('Runtime.evaluate', { expression: "document.querySelector('[data-menu-btn]').click()" }); await sleep(700); }
      if (FULL) {
        // load every lazy image first, then measure: the page grows as they arrive
        await cdp.send('Runtime.evaluate', { awaitPromise: true, expression: `(async () => { for (let y = 0; y < document.documentElement.scrollHeight; y += innerHeight / 2) { scrollTo(0, y); await new Promise(r => setTimeout(r, 120)); } scrollTo(0, 0); await new Promise(r => setTimeout(r, 400)); })()` });
        res.height = (await cdp.send('Runtime.evaluate', { returnByValue: true, expression: 'document.documentElement.scrollHeight' })).result.value;
        // a single capture taller than 16384 device pixels repeats from the top: long pages are captured in
        // slices (name.partN.png) that tools/stitch.py joins; full pages use DPR 2 at most
        const fullDpr = Math.min(v.dpr, 2);
        await cdp.send('Emulation.setDeviceMetricsOverride', { width: v.width, height: res.height, deviceScaleFactor: fullDpr, mobile: v.mobile });
        await sleep(1200);
        const slice = Math.floor(16000 / fullDpr);
        if (res.height <= slice) {
          shot = await cdp.send('Page.captureScreenshot', { format: 'png', captureBeyondViewport: true });
        } else {
          for (let y = 0, n = 0; y < res.height; y += slice, n++) {
            const part = await cdp.send('Page.captureScreenshot', { format: 'png', captureBeyondViewport: true,
              clip: { x: 0, y, width: v.width, height: Math.min(slice, res.height - y), scale: 1 } });
            await writeFile(join(OUT, `${name}.part${n}.png`), Buffer.from(part.data, 'base64'));
          }
          shot = null;
        }
        await cdp.send('Emulation.setDeviceMetricsOverride', { width: v.width, height: v.height, deviceScaleFactor: v.dpr, mobile: v.mobile });
      } else {
        shot = await cdp.send('Page.captureScreenshot', { format: 'png' });
      }
      if (shot) await writeFile(join(OUT, name + '.png'), Buffer.from(shot.data, 'base64'));
      // Todo lo que pide la página si la visita se recorre entera (imágenes diferidas incluidas).
      await cdp.send('Runtime.evaluate', { awaitPromise: true, expression: `(async () => { for (let y = 0; y < document.documentElement.scrollHeight; y += innerHeight / 2) { scrollTo(0, y); await new Promise(r => setTimeout(r, 120)); } })()` });
      await sleep(THROTTLE ? 4000 : 800);
      const whole = [...reqs.values()].filter((r) => r.url && !r.url.startsWith('data:'));
      metrics.push({ view: vname, page, ...res, loadMsWall: loadMs, firstView: { requests: firstView.length, bytes: sum(firstView), byType },
        wholePage: { requests: whole.length, bytes: sum(whole), images: whole.filter((r) => r.type === 'Image').length } });
      console.log(`${name.padEnd(36)} 1ª vista ${String(firstView.length).padStart(2)} pedidos ${(sum(firstView) / 1024).toFixed(0).padStart(4)} KB · página completa ${(sum(whole) / 1024).toFixed(0).padStart(5)} KB · FCP ${res.fcp} ms · LCP ${res.lcp} ms · CLS ${res.cls} · desborde ${res.overflow}px${res.tightHeadings.length ? ' · TÍTULOS APRETADOS: ' + res.tightHeadings.join(' | ') : ''}`);
    }
  }
  await writeFile(join(OUT, 'metrics.json'), JSON.stringify({ throttle: THROTTLE, root: ROOT, date: new Date().toISOString(), metrics }, null, 2));
  ws.close(); proc.kill(); server.close();
  await sleep(500); await rm(profile, { recursive: true, force: true }).catch(() => {});
}

main().catch((e) => { console.error(e); process.exit(1); });
