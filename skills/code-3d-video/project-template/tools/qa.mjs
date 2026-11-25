#!/usr/bin/env node
// Visual QA: lint + render stills at the moments that matter + exposure checks + ONE contact sheet to look at.
//   node tools/qa.mjs [--story f] [--scale 0.5] [--gpu] [--chrome]
import fs from 'node:fs';
import path from 'node:path';
import { spawnSync } from 'node:child_process';
import { arg, python, getDuration, grayBuffer, frameStats, meanAbsDiff } from './lib.mjs';
import { lint, printIssues } from './lint.mjs';

const project = path.resolve(arg('project', process.cwd()));
const storyFile = arg('story', 'story.json');
const story = JSON.parse(fs.readFileSync(path.join(project, storyFile), 'utf8'));
const sh = (cmd, args, opts = {}) => spawnSync(cmd, args, { cwd: project, encoding: 'utf8', ...opts });

// words must exist so captions are part of what we judge
const wordsFile = story.words || 'words.json';
if (!fs.existsSync(path.join(project, wordsFile))) {
  const hasVoice = story.voice && fs.existsSync(path.join(project, story.voice));
  const r = sh(python(), ['tools/align_words.py', '--story', storyFile, '--out', wordsFile, ...(hasVoice ? [] : ['--estimate'])]);
  if (r.status) { console.error(r.stderr); process.exit(1); }
}

const issues = lint(project, story);
const dur = getDuration(project, story);

// pick moments: start, every camera key, label starts (+0.7s so text is fully visible), reveals (boom/ding), even spread
let times = [0.3, ...(story.camera || []).map((k) => k.t), ...(story.labels || []).map((l) => l.t0 + 0.7),
  ...(story.sfx || []).filter((s) => ['boom', 'ding', 'riser'].includes(s.kind)).map((s) => s.t + 0.15),
  dur * 0.25, dur * 0.5, dur * 0.75, dur - 0.4];
times = [...new Set(times.map((t) => Math.round(Math.min(Math.max(t, 0.1), dur - 0.1) * 10) / 10))].sort((a, b) => a - b);
const keep = [];
for (const t of times) if (!keep.length || t - keep[keep.length - 1] >= 0.6) keep.push(t);
while (keep.length > 12) keep.splice(Math.floor(keep.length / 2), 1);

const qaDir = path.join(project, 'out/qa');
fs.rmSync(qaDir, { recursive: true, force: true }); fs.mkdirSync(qaDir, { recursive: true });
const passthru = [];
for (const f of ['gpu', 'chrome']) if (arg(f, false)) passthru.push('--' + f);
console.log(`Rendering ${keep.length} QA stills at: ${keep.join('s, ')}s ...`);
const r = sh('node', ['tools/render.mjs', '--story', storyFile, '--scale', String(arg('scale', 0.5)), '--stills', keep.join(','), '--stills-dir', 'out/qa', '--quiet', ...passthru], { stdio: ['ignore', 'inherit', 'inherit'] });
if (r.status) { console.error('\nQA render failed: the scene did not load. Fix the error above first.'); process.exit(1); }

const files = fs.readdirSync(qaDir).filter((f) => f.startsWith('still_')).sort((a, b) => parseFloat(a.slice(6)) - parseFloat(b.slice(6)));
const rows = []; let prev = null; const bufs = [];
for (const f of files) {
  const t = parseFloat(f.slice(6)), buf = grayBuffer(path.join(qaDir, f)), st = frameStats(buf);
  const probs = [];
  if (st.mean < 12) probs.push('FAIL nearly black (lighting/camera inside geometry/scene not drawn)');
  else if (st.mean < 28) probs.push('warn very dark: raise exposure or add practical lights');
  if (st.mean > 235) probs.push('FAIL nearly white');
  if (st.std < 10) probs.push('warn flat/empty frame: nothing interesting in shot');
  if (st.blown > 0.25) probs.push('warn >25% blown highlights');
  if (st.crushed > 0.75) probs.push('warn >75% pure black');
  const diff = prev ? meanAbsDiff(prev, buf) : null; prev = buf; bufs.push(buf);
  rows.push({ f, t, st, probs, diff });
  for (const p of probs) issues.push({ level: p.startsWith('FAIL') ? 'FAIL' : 'WARN', msg: `frame @${t.toFixed(1)}s: ${p.replace(/^(FAIL|warn) /, '')}` });
}
if (rows.length > 2 && rows.slice(1).every((r) => r.diff < 2)) issues.push({ level: 'WARN', msg: 'All stills look almost identical: camera/scene are not changing.' });

// contact sheet
const tmp = path.join(project, 'build/qa'); fs.rmSync(tmp, { recursive: true, force: true }); fs.mkdirSync(tmp, { recursive: true });
files.forEach((f, i) => fs.copyFileSync(path.join(qaDir, f), path.join(tmp, `s_${String(i + 1).padStart(2, '0')}.png`)));
const cols = Math.min(4, files.length), rws = Math.ceil(files.length / cols);
const cs = sh('ffmpeg', ['-y', '-loglevel', 'error', '-framerate', '1', '-i', 'build/qa/s_%02d.png', '-vf', `scale=360:-2,tile=${cols}x${rws}:padding=8:color=black`, '-frames:v', '1', 'out/qa/contact.png']);
if (cs.status) console.error('contact sheet failed:', cs.stderr);

const md = ['# QA report', '', `Story: ${storyFile}  |  duration ${dur.toFixed(1)}s  |  stills: ${files.length}`, '',
  'Contact sheet (left-to-right, top-to-bottom = times below): `out/qa/contact.png`', '',
  '| # | time | brightness | contrast | notes |', '|---|---|---|---|---|',
  ...rows.map((r, i) => `| ${i + 1} | ${r.t.toFixed(1)}s | ${r.st.mean.toFixed(0)} | ${r.st.std.toFixed(0)} | ${r.probs.join('; ') || 'ok'} |`), '',
  '## Lint', ...issues.map((i) => `- **${i.level}** ${i.msg}`), ''].join('\n');
fs.writeFileSync(path.join(qaDir, 'report.md'), md);
printIssues(issues);
console.log('\nRead:  out/qa/contact.png  (LOOK at it)  and  out/qa/report.md');
console.log('Times: ' + files.map((f, i) => `#${i + 1}=${parseFloat(f.slice(6)).toFixed(1)}s`).join('  '));
process.exit(issues.some((i) => i.level === 'FAIL') ? 2 : 0);
