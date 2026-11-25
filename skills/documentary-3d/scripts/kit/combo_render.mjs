#!/usr/bin/env node
/**
 * Universal Modular Combo Renderer (Version 3)
 * Serves plugin root cleanly over HTTP (zero 404/CORS path errors) so 3D-Animator,
 * p5.brush, Lemo-Opuscar styles/post-FX, and archival photos work seamlessly together.
 */
import http from 'node:http';
import fs from 'node:fs';
import path from 'node:path';
import { createRequire } from 'node:module';
import { spawn } from 'node:child_process';
import { fileURLToPath } from 'node:url';

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const KIT_DIR = __dirname;
const PLUGIN_ROOT = path.resolve(__dirname, '..', '..', '..', '..');
const WORKSPACE_ROOT = path.resolve(PLUGIN_ROOT, '..');

const args = Object.fromEntries(
  process.argv.slice(2).map((a) => {
    const idx = a.indexOf('=');
    if (idx === -1) return [a.replace(/^--/, ''), true];
    return [a.slice(0, idx).replace(/^--/, ''), a.slice(idx + 1)];
  })
);

// Locate puppeteer / puppeteer-core and three across kit, workspace, or fallback reel node_modules
const req = createRequire(import.meta.url);
function findNodeModule(modName) {
  const candidates = [
    path.join(KIT_DIR, 'node_modules', modName),
    path.join(PLUGIN_ROOT, 'node_modules', modName),
    path.join(WORKSPACE_ROOT, 'stuxnet_reel_9x16', 'node_modules', modName),
    path.join(PLUGIN_ROOT, 'skills', 'lemo-opuscar', 'node_modules', modName),
    path.join(PLUGIN_ROOT, 'skills', 'p5-brush', 'kit', 'node_modules', modName)
  ];
  for (const c of candidates) {
    if (fs.existsSync(c)) return c;
  }
  return null;
}

const threeDir = findNodeModule('three');
if (!threeDir) {
  console.error('Error: Three.js module not found in kit/node_modules or sibling workspace node_modules.');
  process.exit(1);
}

const pupPath = findNodeModule('puppeteer') || findNodeModule('puppeteer-core');
if (!pupPath) {
  console.error('Error: puppeteer or puppeteer-core not found.');
  process.exit(1);
}
const puppeteerMod = req(pupPath);
const puppeteer = puppeteerMod.default || puppeteerMod;

const projectRoot = args.project ? path.resolve(String(args.project)) : process.cwd();
const explicitPhotoPath = args.photo && fs.existsSync(path.resolve(String(args.photo))) ? path.resolve(String(args.photo)) : null;
const explicitModelPath = args.model && fs.existsSync(path.resolve(String(args.model))) ? path.resolve(String(args.model)) : null;
const MIME = {
  '.html': 'text/html', '.js': 'text/javascript', '.mjs': 'text/javascript',
  '.json': 'application/json', '.md': 'text/plain', '.png': 'image/png',
  '.jpg': 'image/jpeg', '.jpeg': 'image/jpeg', '.webp': 'image/webp', '.css': 'text/css',
  '.woff2': 'font/woff2', '.ttf': 'font/ttf', '.glb': 'model/gltf-binary',
  '.gltf': 'model/gltf+json', '.bin': 'application/octet-stream'
};

const server = http.createServer((reqHttp, res) => {
  const urlPath = decodeURIComponent(reqHttp.url.split('?')[0]);
  if (urlPath === '/favicon.ico') {
    res.writeHead(204);
    return res.end();
  }
  let fsPath = null;
  let allowedBase = null;

  if (urlPath === '/local-photo' && explicitPhotoPath) {
    allowedBase = path.dirname(explicitPhotoPath);
    fsPath = explicitPhotoPath;
  } else if (urlPath.startsWith('/local-model/') && explicitModelPath) {
    allowedBase = path.dirname(explicitModelPath);
    fsPath = path.join(allowedBase, urlPath.slice('/local-model/'.length));
  } else if (urlPath.startsWith('/three/')) {
    allowedBase = threeDir;
    fsPath = path.join(threeDir, urlPath.slice('/three/'.length));
  } else if (urlPath.startsWith('/plugin/')) {
    allowedBase = PLUGIN_ROOT;
    fsPath = path.join(PLUGIN_ROOT, urlPath.slice('/plugin/'.length));
  } else if (urlPath.startsWith('/assets/') || urlPath.startsWith('/models/')) {
    allowedBase = projectRoot;
    fsPath = path.join(projectRoot, urlPath.slice(1));
  } else {
    const candProj = path.join(projectRoot, urlPath.replace(/^\/+/, ''));
    if (fs.existsSync(candProj) && !fs.statSync(candProj).isDirectory() && /\.(png|jpe?g|webp|gif)$/i.test(candProj)) {
      allowedBase = projectRoot;
      fsPath = candProj;
    } else {
      allowedBase = KIT_DIR;
      fsPath = path.join(KIT_DIR, urlPath.replace(/^\/+/, ''));
    }
  }

  if (!fsPath.startsWith(allowedBase) || !fs.existsSync(fsPath) || fs.statSync(fsPath).isDirectory()) {
    res.writeHead(404);
    return res.end();
  }
  res.writeHead(200, { 'Content-Type': MIME[path.extname(fsPath).toLowerCase()] || 'application/octet-stream' });
  fs.createReadStream(fsPath).pipe(res);
});

await new Promise((r) => server.listen(0, '127.0.0.1', r));
const port = server.address().port;

const chromeFallback = 'C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe';
const execPath = process.env.CHROME_PATH || (fs.existsSync(chromeFallback) ? chromeFallback : undefined);

const browser = await puppeteer.launch({
  headless: true,
  executablePath: execPath,
  args: [
    '--no-sandbox', '--disable-setuid-sandbox', '--hide-scrollbars',
    '--force-color-profile=srgb', '--disable-dev-shm-usage',
    '--enable-webgl', '--ignore-gpu-blocklist'
  ]
});

const W = parseInt(args.width || '1920', 10);
const H = parseInt(args.height || '1080', 10);
const page = await browser.newPage();
await page.setViewport({ width: W, height: H, deviceScaleFactor: 1 });

let fatalErrors = 0;
page.on('console', (m) => {
  if (m.type() === 'error') {
    console.log('[page error]', m.text());
    fatalErrors++;
  }
});
page.on('pageerror', (e) => {
  console.log('[pageerror]', e.message);
  fatalErrors++;
});
page.on('response', (r) => {
  if (r.status() >= 400) {
    console.log('[http missing]', r.status(), r.url());
  }
});

const qs = new URLSearchParams({
  render: '1',
  width: String(W),
  height: String(H),
  style: String(args.shader || args.style || 'lit'),
  brush: String(args.brush || 'none'),
  lemo: String(args.lemo || 'none'),
  post: String(args.post || 'hdr'),
  total: String(args.total || '6')
});
if (args.photo) qs.set('photo', explicitPhotoPath ? '/local-photo' : String(args.photo));
if (args.model) qs.set('model', explicitModelPath ? '/local-model/' + encodeURIComponent(path.basename(explicitModelPath)) : String(args.model));

await page.goto(`http://127.0.0.1:${port}/combo_stage.html?${qs.toString()}`, { waitUntil: 'load' });
await page.waitForFunction('window.__ready === true', { timeout: 120000 });

const total = await page.evaluate('window.total');
const N = parseInt(args.n || '4', 10);
const grab = async (t) =>
  Buffer.from(
    await page.evaluate((tt, n) => {
      window.renderAt(tt, n);
      return document.getElementById('stage').toDataURL('image/png').split(',')[1];
    }, t, N),
    'base64'
  );

if (args.stills) {
  const outDir = path.resolve(String(args.out || 'stills'));
  fs.mkdirSync(outDir, { recursive: true });
  for (const s of String(args.stills).split(',')) {
    const t = parseFloat(s.trim());
    const f = path.join(outDir, `combo_t${t.toFixed(2)}.png`);
    fs.writeFileSync(f, await grab(t));
    console.log('still ->', f);
  }
} else if (args.video) {
  const fps = parseInt(args.fps || '30', 10);
  const from = parseFloat(args.from || '0');
  const to = parseFloat(args.to || String(total));
  const frames = Math.round((to - from) * fps);
  const outFile = path.resolve(String(args.out || 'out/combo_final.mp4'));
  fs.mkdirSync(path.dirname(outFile), { recursive: true });

  const audio = args.audio ? ['-ss', String(from), '-i', path.resolve(String(args.audio))] : [];
  const ff = spawn('ffmpeg', [
    '-y', '-v', 'error', '-f', 'image2pipe', '-framerate', String(fps), '-c:v', 'png', '-i', '-',
    ...audio, '-map', '0:v', ...(args.audio ? ['-map', '1:a', '-c:a', 'aac', '-b:a', '256k', '-shortest'] : []),
    '-c:v', 'libx264', '-preset', 'veryfast', '-crf', String(args.crf || '18'), '-pix_fmt', 'yuv420p',
    outFile
  ], { stdio: ['pipe', 'inherit', 'inherit'] });

  for (let i = 0; i < frames; i++) {
    const buf = await grab(from + i / fps);
    if (!ff.stdin.write(buf)) await new Promise((r) => ff.stdin.once('drain', r));
    if (i > 0 && i % 30 === 0) console.log(`combo frame ${i}/${frames}`);
  }
  ff.stdin.end();
  await new Promise((r) => ff.on('close', r));
  console.log('combo video ->', outFile);
} else {
  console.log('Nothing to do. Pass --stills=1,3 or --video');
}

server.closeAllConnections?.();
server.close();
await Promise.race([browser.close(), new Promise((r) => setTimeout(r, 6000))]);
try { browser.process()?.kill('SIGKILL'); } catch {}
if (fatalErrors > 0) process.exit(2);
process.exit(0);
