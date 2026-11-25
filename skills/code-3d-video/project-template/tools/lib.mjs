import fs from 'node:fs';
import path from 'node:path';
import { spawnSync } from 'node:child_process';

export const argv = process.argv.slice(2);
export function arg(name, def) {
  const i = argv.indexOf('--' + name);
  if (i === -1) return def;
  const v = argv[i + 1];
  return v === undefined || v.startsWith('--') ? true : v;
}

export function probeDuration(file) {
  const r = spawnSync('ffprobe', ['-v', 'error', '-show_entries', 'format=duration', '-of', 'default=nw=1:nk=1', file], { encoding: 'utf8' });
  const d = parseFloat(r.stdout);
  return Number.isFinite(d) ? d : null;
}

// Total video length = max(voice length, last caption word) + tail. story.duration overrides everything.
export function getDuration(project, story) {
  if (story.duration) return story.duration;
  let d = 0;
  if (story.voice && fs.existsSync(path.join(project, story.voice))) d = Math.max(d, probeDuration(path.join(project, story.voice)) || 0);
  const wp = path.join(project, story.words || 'words.json');
  if (fs.existsSync(wp)) {
    const w = JSON.parse(fs.readFileSync(wp, 'utf8'));
    if (w.length) d = Math.max(d, w[w.length - 1].t1);
  }
  if (!d) d = 10;
  return d + (story.tail ?? 0.8);
}

export function python() {
  const candidates = process.platform === 'win32' ? ['python', 'py -3', 'python3'] : ['python3', 'python'];
  for (const c of candidates) {
    const parts = c.split(' ');
    if (spawnSync(parts[0], [...parts.slice(1), '--version']).status === 0) return c;
  }
  throw new Error('Python 3 not found');
}

// Decode an image to a small gray buffer and return simple exposure/contrast stats.
export function grayBuffer(file, w = 96) {
  const r = spawnSync('ffmpeg', ['-v', 'error', '-i', file, '-vf', `scale=${w}:-2`, '-f', 'rawvideo', '-pix_fmt', 'gray', '-'], { maxBuffer: 1 << 26 });
  return r.status === 0 ? r.stdout : null;
}
export function frameStats(buf) {
  const n = buf.length; let s = 0, s2 = 0, hi = 0, lo = 0;
  for (let i = 0; i < n; i++) { const v = buf[i]; s += v; s2 += v * v; if (v > 250) hi++; if (v < 5) lo++; }
  const mean = s / n;
  return { mean, std: Math.sqrt(Math.max(0, s2 / n - mean * mean)), blown: hi / n, crushed: lo / n };
}
export function meanAbsDiff(a, b) {
  const n = Math.min(a.length, b.length); let d = 0;
  for (let i = 0; i < n; i++) d += Math.abs(a[i] - b[i]);
  return d / n;
}
