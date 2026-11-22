// Headless Chrome offline renderer for p5.brush animations.
// Renders frame-by-frame and pipes PNG/raw buffer into ffmpeg.
//
// Usage:
//   node render_brush.mjs --stills=0.5,1.5,3.0
//   node render_brush.mjs --video --fps=30 --out=out/brush_animation.mp4

import http from 'node:http';
import fs from 'node:fs';
import path from 'node:path';
import { spawn } from 'node:child_process';
import puppeteer from 'puppeteer';

const args = Object.fromEntries(
  process.argv.slice(2).map((a) => {
    const [k, v] = a.replace(/^--/, '').split('=');
    return [k, v ?? true];
  })
);

const ROOT = path.resolve('.');
const MIME = {
  '.html': 'text/html',
  '.js': 'text/javascript',
  '.mjs': 'text/javascript',
  '.json': 'application/json',
  '.png': 'image/png',
  '.jpg': 'image/jpeg',
  '.css': 'text/css'
};

const server = http.createServer((req, res) => {
  const p = path.join(ROOT, decodeURIComponent(req.url.split('?')[0]));
  if (!p.startsWith(ROOT) || !fs.existsSync(p) || fs.statSync(p).isDirectory()) {
    res.writeHead(404);
    return res.end();
  }
  res.writeHead(200, { 'Content-Type': MIME[path.extname(p)] || 'application/octet-stream' });
  fs.createReadStream(p).pipe(res);
});

await new Promise((r) => server.listen(0, '127.0.0.1', r));
const port = server.address().port;

const browser = await puppeteer.launch({
  headless: true,
  executablePath: process.env.CHROME_PATH || undefined,
  args: ['--hide-scrollbars', '--force-color-profile=srgb', '--enable-gpu']
});

const page = await browser.newPage();
await page.setViewport({ width: 1920, height: 1080, deviceScaleFactor: 1 });

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
  const out = args.out || 'stills';
  fs.mkdirSync(out, { recursive: true });
  for (const s of String(args.stills).split(',')) {
    const t = parseFloat(s);
    const f = `${out}/brush_t${t.toFixed(2)}.png`;
    fs.writeFileSync(f, await grab(t));
    console.log('p5.brush still ->', f);
  }
} else if (args.video) {
  const fps = +(args.fps || 30);
  const from = +(args.from || 0);
  const to = +(args.to || total);
  const n = Math.round((to - from) * fps);
  const outFile = args.out || 'out/brush_animation.mp4';
  fs.mkdirSync(path.dirname(outFile) || '.', { recursive: true });

  const ff = spawn(
    'ffmpeg',
    [
      '-y', '-v', 'error',
      '-f', 'image2pipe',
      '-framerate', String(fps),
      '-c:v', 'png',
      '-i', '-',
      '-c:v', 'libx264',
      '-preset', 'slow',
      '-crf', String(args.crf || 16),
      '-pix_fmt', 'yuv420p',
      '-movflags', '+faststart',
      outFile
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

await browser.close();
server.close();
