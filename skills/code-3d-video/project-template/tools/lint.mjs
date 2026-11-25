// Fast static checks (no browser). Catches the mistakes that waste a 10-minute render.
import fs from 'node:fs';
import path from 'node:path';
import { Timeline } from '../src/timeline.js';
import { getDuration } from './lib.mjs';

const KINDS = ['whoosh', 'click', 'thud', 'footstep', 'ding', 'pop', 'riser', 'paper', 'boom', 'glitch'];
const dist = (a, b) => Math.hypot(a[0] - b[0], a[1] - b[1], a[2] - b[2]);

export function lint(project, story) {
  const out = [];
  const add = (level, msg) => out.push({ level, msg });
  const W = story.width || 1080, H = story.height || 1920, fps = story.fps || 30;
  if (W % 2 || H % 2) add('FAIL', `width/height must be even (got ${W}x${H}).`);
  if (fps < 24 || fps > 60) add('WARN', `fps ${fps} is unusual; use 30 (or 24/60).`);
  const dur = getDuration(project, story);
  if (dur > 90) add('WARN', `Video is ${dur.toFixed(0)}s: render time grows linearly; reels/shorts work best at 20-60s.`);

  // script / voice / words
  const script = (story.script || '').trim();
  if (!script) add('WARN', 'story.script is empty: captions and timing will rely on Whisper only.');
  const vp = story.voice && path.join(project, story.voice);
  const wp = path.join(project, story.words || 'words.json');
  let words = [];
  if (fs.existsSync(wp)) { try { words = JSON.parse(fs.readFileSync(wp, 'utf8')); } catch { add('FAIL', 'words.json is not valid JSON.'); } }
  if (!words.length) add('WARN', 'No words.json yet (build creates it).');
  for (let i = 1; i < words.length; i++) if (words[i].t0 < words[i - 1].t0 - 1e-3) { add('FAIL', `words.json not in time order at word ${i} ("${words[i].w}").`); break; }
  const long = words.filter((w) => w.t1 - w.t0 > 1.6);
  if (long.length) add('WARN', `${long.length} word(s) last >1.6s (e.g. "${long[0].w}" at ${long[0].t0.toFixed(1)}s): alignment drifted; install faster-whisper and run --realign.`);
  if (vp && fs.existsSync(vp) && script) {
    const n = script.split(/\s+/).length, voiceDur = words.length ? words[words.length - 1].t1 : dur;
    const wpm = n / (voiceDur / 60);
    if (wpm > 190) add('WARN', `Narration is ~${wpm.toFixed(0)} wpm: too fast to follow with visuals; trim the script.`);
    if (wpm < 100) add('WARN', `Narration is ~${wpm.toFixed(0)} wpm: slow; consider tightening for retention.`);
  } else if (!vp || !fs.existsSync(vp)) add('INFO', 'No voice file: silent dry run (timing is estimated).');

  // camera
  const keys = story.camera || [];
  const engine = story.engine || 'three';
  if (engine !== 'canvas') {
    if (keys.length < 2) add('FAIL', 'story.camera needs at least 2 keyframes.');
    for (const [i, k] of keys.entries()) {
      for (const f of ['pos', 'look']) if (!Array.isArray(k[f]) || k[f].length !== 3 || k[f].some((x) => !Number.isFinite(x))) add('FAIL', `camera[${i}].${f} must be [x,y,z] numbers.`);
      if (!Number.isFinite(k.t)) add('FAIL', `camera[${i}].t missing.`);
      if (k.fov && (k.fov < 18 || k.fov > 85)) add('WARN', `camera[${i}].fov ${k.fov} is extreme (use 30-60).`);
    }
  }
  if (keys.length >= 2 && !out.some((o) => o.level === 'FAIL')) {
    const tl = new Timeline(keys, story.cameraTension ?? 1);
    const ks = [...keys].sort((a, b) => a.t - b.t);
    if (ks[0].t > 0.6) add('INFO', `Camera starts moving only at ${ks[0].t}s (holds first pose before that).`);
    if (ks[ks.length - 1].t < dur - 1.2) add('WARN', `Camera stops at ${ks[ks.length - 1].t}s but video lasts ${dur.toFixed(1)}s: last ${(dur - ks[ks.length - 1].t).toFixed(1)}s is frozen. Add a final key near ${dur.toFixed(0)}s.`);
    for (let i = 1; i < ks.length; i++) if (ks[i].t - ks[i - 1].t < 0.8) add('WARN', `Camera keys at ${ks[i - 1].t}s and ${ks[i].t}s are <0.8s apart: will look jerky.`);
    let maxV = 0, at = 0, prev = tl.sample(0);
    for (let t = 0.1; t <= dur; t += 0.1) { const c = tl.sample(t), v = dist(c.pos, prev.pos) / 0.1; if (v > maxV) { maxV = v; at = t; } prev = c; }
    if (maxV > 9) add('WARN', `Camera reaches ${maxV.toFixed(1)} units/s near ${at.toFixed(1)}s: very fast, will smear. Space the keys further apart in time.`);
    // static stretches: no camera movement, label or sfx for >3s
    const events = [...(story.labels || []).map((l) => l.t0), ...(story.sfx || []).map((s) => s.t)];
    let run0 = null;
    for (let t = 0; t + 3 <= dur + 0.01; t += 0.5) {
      const a = tl.sample(t), b = tl.sample(t + 3);
      const move = dist(a.pos, b.pos) + dist(a.look, b.look) * 0.5 + Math.abs(a.fov - b.fov) * 0.05;
      const ev = events.some((e) => e >= t && e <= t + 3);
      const still = move < 0.4 && !ev;
      if (still && run0 === null) run0 = t;
      if ((!still || t + 3.5 > dur) && run0 !== null) { add('WARN', `Static stretch ${run0.toFixed(1)}s-${(t + 3).toFixed(1)}s: no camera move, label or sfx for 3s+. Add a push-in, prop reveal or sfx accent.`); run0 = null; }
    }
  }

  // labels
  const labs = [...(story.labels || [])].sort((a, b) => a.t0 - b.t0);
  labs.forEach((l, i) => {
    if (l.t1 - l.t0 < 1.5) add('WARN', `Label "${l.text}" is on screen ${(l.t1 - l.t0).toFixed(1)}s: too short to read (>=1.5s).`);
    if (l.t1 > dur + 0.01) add('WARN', `Label "${l.text}" ends after the video.`);
    if (i && l.t0 < labs[i - 1].t1) add('WARN', `Labels "${labs[i - 1].text}" and "${l.text}" overlap.`);
  });

  // audio
  const sfx = story.sfx || [];
  for (const s of sfx) {
    if (s.file) { if (!fs.existsSync(path.join(project, s.file))) add('FAIL', `sfx file missing: ${s.file}`); }
    else if (!KINDS.includes(s.kind)) add('FAIL', `Unknown sfx kind "${s.kind}". Available: ${KINDS.join(', ')}.`);
    if (!(s.t >= 0 && s.t <= dur)) add('WARN', `sfx at ${s.t}s is outside the video (0-${dur.toFixed(1)}s).`);
  }
  if (sfx.length > dur / 2.5) add('WARN', `${sfx.length} sfx in ${dur.toFixed(0)}s is busy; aim for 1 per ~4s so accents land.`);
  const m = story.music;
  if (m) {
    if (m.file && !fs.existsSync(path.join(project, m.file))) add('FAIL', `music file missing: ${m.file}`);
    if ((m.gain ?? 0.2) > 0.45) add('WARN', `music gain ${m.gain} will fight the voice (use 0.15-0.35).`);
  } else add('INFO', 'No music configured; add {"music":{"kind":"pad","mood":"dark","gain":0.25}} for atmosphere.');
  return out;
}

export function printIssues(issues) {
  const icon = { FAIL: 'FAIL ', WARN: 'warn ', INFO: 'info ' };
  console.log('\nLint:');
  if (!issues.length) console.log('  all clear');
  for (const i of issues) console.log(`  [${icon[i.level]}] ${i.msg}`);
}

if (import.meta.url === `file://${process.argv[1]}`) {
  const { arg } = await import('./lib.mjs');
  const project = path.resolve(arg('project', process.cwd()));
  const story = JSON.parse(fs.readFileSync(path.join(project, arg('story', 'story.json')), 'utf8'));
  const issues = lint(project, story); printIssues(issues);
  process.exit(issues.some((i) => i.level === 'FAIL') ? 2 : 0);
}
