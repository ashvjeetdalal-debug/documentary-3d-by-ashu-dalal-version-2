#!/usr/bin/env node
// Deterministic frame-by-frame renderer: headless Chrome -> screenshots -> ffmpeg (silent MP4).
// The page never plays in real time: for frame i we call window.__renderFrame(i / fps) and capture.
// Flags: --story f --scale 0.5 --gpu --chrome --mb N (motion-blur sub-frames) --stills 1,2 --from-frame a --to-frame b --silent path --quiet
import { createRequire } from 'node:module';
import fs from 'node:fs';
import os from 'node:os';
import path from 'node:path';
import http from 'node:http';
import { spawn } from 'node:child_process';
import { arg, getDuration } from './lib.mjs';

const require = createRequire(import.meta.url);
let playwright;
try { playwright = require('playwright'); } catch { console.error('Missing dependency. Run: npm run setup'); process.exit(1); }

const project = path.resolve(arg('project', process.cwd()));
const storyFile = arg('story', 'story.json');
const story = JSON.parse(fs.readFileSync(path.join(project, storyFile), 'utf8'));
const scale = parseFloat(arg('scale', '1'));
const W = Math.round((story.width || 1080) * scale / 2) * 2;
const H = Math.round((story.height || 1920) * scale / 2) * 2;
const fps = story.fps || 30;
const duration = getDuration(project, story);
const outFile = path.resolve(project, arg('silent', 'build/video_silent.mp4'));
const stills = arg('stills', null);
const quiet = arg('quiet', false);
const mb = Math.max(1, parseInt(arg('mb', story.motionBlur ?? (scale < 1 ? 1 : 4)), 10));
const shutter = story.shutter ?? 0.5; // 0.5 = 180-degree shutter (film look)

fs.mkdirSync(path.join(project, 'build'), { recursive: true });
fs.writeFileSync(path.join(project, 'build/meta.json'), JSON.stringify({ duration, fps, width: W, height: H }, null, 2));

const MIME = { '.html': 'text/html', '.js': 'text/javascript', '.mjs': 'text/javascript', '.json': 'application/json',
  '.css': 'text/css', '.png': 'image/png', '.jpg': 'image/jpeg', '.jpeg': 'image/jpeg', '.svg': 'image/svg+xml',
  '.woff2': 'font/woff2', '.wav': 'audio/wav', '.mp3': 'audio/mpeg', '.glb': 'model/gltf-binary', '.gltf': 'model/gltf+json', '.bin': 'application/octet-stream' };
const pluginRootCandidates = [
  process.env.ASHU_PLUGIN_ROOT,
  path.resolve(path.dirname(new URL(import.meta.url).pathname.replace(/^\/([A-Za-z]:)/, '$1')), '../../../..'),
  path.resolve(project, '../..'),
  path.resolve(project, '..'),
  path.join(os.homedir(), '.gemini', 'config', 'plugins', 'documentary-3d-by-ashu-dalal-version-3'),
  path.join(os.homedir(), '.gemini', 'config', 'plugins', 'documentary-3d-by-ashu-dalal-version-2')
].filter(Boolean);
const pluginRoot = pluginRootCandidates.find((d) => fs.existsSync(path.join(d, 'plugin.json')) || fs.existsSync(path.join(d, 'skills', 'documentary-3d')));
const server = http.createServer((req, res) => {
  const urlPath = decodeURIComponent(new URL(req.url, 'http://x').pathname);
  if (urlPath === '/favicon.ico') { res.writeHead(204); return res.end(); }
  let base = project;
  let p = path.normalize(path.join(project, urlPath));
  if (urlPath.startsWith('/plugin/') && pluginRoot) {
    base = pluginRoot;
    p = path.normalize(path.join(pluginRoot, urlPath.slice('/plugin/'.length)));
  }
  if (!p.startsWith(base) || !fs.existsSync(p) || fs.statSync(p).isDirectory()) { res.writeHead(404); return res.end(); }
  res.writeHead(200, { 'Content-Type': MIME[path.extname(p)] || 'application/octet-stream', 'Cache-Control': 'no-store' });
  fs.createReadStream(p).pipe(res);
});
await new Promise((r) => server.listen(0, '127.0.0.1', r));
const port = server.address().port;

const args = ['--hide-scrollbars', '--force-color-profile=srgb', '--ignore-gpu-blocklist', '--enable-webgl'];
if (!arg('gpu', false)) args.push('--use-gl=angle', '--use-angle=swiftshader', '--enable-unsafe-swiftshader'); // software GL: slow but works everywhere
const launch = { headless: true, args };
if (arg('chrome', false) || !arg('no-chrome', false)) launch.channel = 'chrome'; // default to installed Google Chrome on Windows
const browser = await playwright.chromium.launch(launch);
const page = await browser.newPage({ viewport: { width: W, height: H }, deviceScaleFactor: 1 });
page.on('console', (m) => { if (['error', 'warning'].includes(m.type())) console.error(`[page ${m.type()}]`, m.text()); });
page.on('pageerror', (e) => console.error('[pageerror]', e.message));
await page.goto(`http://127.0.0.1:${port}/index.html?story=${encodeURIComponent(storyFile)}`);
const bail = async (msg) => { console.error(msg); await browser.close(); server.close(); process.exit(1); };
try { await page.waitForFunction(() => window.__ready === true || window.__error, null, { timeout: 180000 }); }
catch { await bail('Page never became ready (timeout).'); }
const err = await page.evaluate(() => window.__error);
if (err) await bail('Scene failed to load:\n' + err);

const frame = (t, sub = 1) => page.evaluate(([tt, s, sh]) => window.__renderFrame(tt, s, sh), [t, sub, shutter]);

if (stills) {
  const dir = path.join(project, arg('stills-dir', 'out/stills')); fs.mkdirSync(dir, { recursive: true });
  const times = stills === true ? [0.2, 0.5, 0.8].map((f) => f * duration) : String(stills).split(',').map(Number);
  for (const t of times) {
    await frame(Math.min(t, duration), 1);
    const f = path.join(dir, `still_${t.toFixed(2)}s.png`);
    await page.screenshot({ path: f, type: 'png' });
    if (!quiet) console.log('wrote', path.relative(project, f));
  }
  await browser.close(); server.close(); process.exit(0);
}

const total = Math.round(duration * fps);
const i0 = parseInt(arg('from-frame', 0), 10), i1 = Math.min(total, parseInt(arg('to-frame', total), 10));
const ff = spawn('ffmpeg', ['-y', '-loglevel', 'error', '-f', 'image2pipe', '-framerate', String(fps), '-c:v', 'mjpeg', '-i', '-',
  '-c:v', 'libx264', '-preset', String(arg('preset', 'medium')), '-crf', String(arg('crf', 16)), '-g', String(fps * 2), '-pix_fmt', 'yuv420p', '-movflags', '+faststart', outFile],
  { stdio: ['pipe', 'inherit', 'inherit'] });
const ffDone = new Promise((r) => ff.on('close', r));
const t0 = Date.now();
for (let i = i0; i < i1; i++) {
  await frame(i / fps, mb);
  const buf = await page.screenshot({ type: 'jpeg', quality: 95 });
  if (!ff.stdin.write(buf)) await new Promise((r) => ff.stdin.once('drain', r));
  const n = i - i0 + 1, N = i1 - i0;
  if (!quiet && (n % 30 === 0 || n === N)) {
    const el = (Date.now() - t0) / 1000;
    process.stderr.write(`\rframe ${n}/${N}  ${(el / n).toFixed(2)}s/frame  eta ${(el / n * (N - n)).toFixed(0)}s   `);
  }
}
if (!quiet) process.stderr.write('\n');
ff.stdin.end();
const code = await ffDone;
await browser.close(); server.close();
if (code !== 0) { console.error('ffmpeg failed'); process.exit(1); }
if (!quiet) console.log('wrote', path.relative(project, outFile), `(${(i1 - i0) / fps}s, ${W}x${H}, ${fps}fps, motion-blur x${mb})`);
