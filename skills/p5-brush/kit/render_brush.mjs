// Headless Chrome offline renderer for p5.brush animations.
// Renders frame-by-frame and pipes PNG/raw buffer into ffmpeg.
//
// Usage:
//   node render_brush.mjs --stills=0.5,1.5,3.0
//   node render_brush.mjs --video --fps=30 --out=out/brush_animation.mp4

import http from 'node:http';
import fs from 'node:fs';
import path from 'node:path';
import { createRequire } from 'node:module';
import { spawn } from 'node:child_process';
import { fileURLToPath } from 'node:url';

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const req = createRequire(import.meta.url);
function findPup() {
  const cands = [
    path.join(__dirname, 'node_modules', 'puppeteer'),
    path.join(__dirname, 'node_modules', 'puppeteer-core'),
    path.resolve(__dirname, '../../../node_modules/puppeteer'),
    path.resolve(__dirname, '../../../node_modules/puppeteer-core'),
    path.resolve(__dirname, '../../../../stuxnet_reel_9x16/node_modules/puppeteer-core')
  ];
  return cands.find((c) => fs.existsSync(c)) || null;
}
const pupDir = findPup();
if (!pupDir) {
  console.error('Error: puppeteer/puppeteer-core not found; run npm install in skills/p5-brush/kit/');
  process.exit(1);
}
const pupMod = req(pupDir);
const puppeteer = pupMod.default || pupMod;

const args = Object.fromEntries(
  process.argv.slice(2).map((a) => {
    const idx = a.indexOf('=');
    if (idx === -1) return [a.replace(/^--/, ''), true];
    return [a.slice(0, idx).replace(/^--/, ''), a.slice(idx + 1)];
  })
);

const ROOT = path.resolve('.');
const DIST_DIR = path.resolve(__dirname, '..', 'dist');
const MIME = {
  '.html': 'text/html', '.js': 'text/javascript', '.mjs': 'text/javascript',
  '.json': 'application/json', '.png': 'image/png', '.jpg': 'image/jpeg', '.css': 'text/css'
};

const server = http.createServer((reqHttp, res) => {
  const urlPath = decodeURIComponent(reqHttp.url.split('?')[0]);
  if (urlPath === '/favicon.ico') { res.writeHead(204); return res.end(); }
  let p = path.join(ROOT, urlPath);
  let base = ROOT;
  if (urlPath.startsWith('/dist/') && fs.existsSync(DIST_DIR)) {
    base = DIST_DIR;
    p = path.join(DIST_DIR, urlPath.slice('/dist/'.length));
  }
  if (!p.startsWith(base) || !fs.existsSync(p) || fs.statSync(p).isDirectory()) {
    res.writeHead(404);
    return res.end();
  }
  res.writeHead(200, { 'Content-Type': MIME[path.extname(p).toLowerCase()] || 'application/octet-stream' });
  fs.createReadStream(p).pipe(res);
});

await new Promise((r) => server.listen(0, '127.0.0.1', r));
const port = server.address().port;

const winChrome = 'C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe';
const execPath = process.env.CHROME_PATH || (fs.existsSync(winChrome) ? winChrome : undefined);
const browser = await puppeteer.launch({
  headless: true,
  executablePath: execPath,
  args: ['--no-sandbox', '--disable-setuid-sandbox', '--hide-scrollbars', '--force-color-profile=srgb', '--disable-dev-shm-usage', '--enable-webgl']
});

const page = await browser.newPage();
await page.setViewport({ width: 1920, height: 1080, deviceScaleFactor: 1 });
let pageErrors = 0;
page.on('pageerror', (e) => { console.log('[pageerror]', e.message); pageErrors++; });
page.on('console', (m) => { if (m.type() === 'error') { console.log('[page error]', m.text()); pageErrors++; } });

await page.goto(`http://127.0.0.1:${port}/index.html`, { waitUntil: 'load' });
await page.waitForFunction('window.__ready === true', { timeout: 60000 });

const total = await page.evaluate('window.total');
const grab = async (t) =>
  Buffer.from(
    await page.evaluate((tt) => {
      window.renderAt(tt);
      return document.getElementById('stage').toDataURL('image/png').split(',')[1];
    }, t),
    'base64'
  );

if (args.stills) {
  const out = path.resolve(String(args.out || 'stills'));
  fs.mkdirSync(out, { recursive: true });
  for (const s of String(args.stills).split(',')) {
    const t = parseFloat(s);
    const f = path.join(out, `brush_t${t.toFixed(2)}.png`);
    fs.writeFileSync(f, await grab(t));
    console.log('p5.brush still ->', f);
  }
} else if (args.video) {
  const fps = +(args.fps || 30);
  const from = +(args.from || 0);
  const to = +(args.to || total);
  const n = Math.round((to - from) * fps);
  const outFile = path.resolve(String(args.out || 'out/brush_animation.mp4'));
  fs.mkdirSync(path.dirname(outFile) || '.', { recursive: true });

  const ff = spawn(
    'ffmpeg',
    [
      '-y', '-v', 'error', '-f', 'image2pipe', '-framerate', String(fps), '-c:v', 'png', '-i', '-',
      '-c:v', 'libx264', '-preset', 'slow', '-crf', String(args.crf || 16), '-pix_fmt', 'yuv420p', '-movflags', '+faststart', outFile
    ],
    { stdio: ['pipe', 'inherit', 'inherit'] }
  );

  console.log(`Rendering ${n} frames of p5.brush animation to ${outFile}...`);
  for (let i = 0; i < n; i++) {
    const buf = await grab(from + i / fps);
    if (!ff.stdin.write(buf)) await new Promise((r) => ff.stdin.once('drain', r));
  }
  ff.stdin.end();
  await new Promise((r) => ff.on('close', r));
  console.log('Video render completed ->', outFile);
} else {
  console.log('Ready. Use --stills=0.5,1.5,3.0 or --video');
}

server.closeAllConnections?.();
server.close();
await Promise.race([browser.close(), new Promise((r) => setTimeout(r, 6000))]);
try { browser.process()?.kill('SIGKILL'); } catch {}
process.exit(pageErrors > 0 ? 2 : 0);
