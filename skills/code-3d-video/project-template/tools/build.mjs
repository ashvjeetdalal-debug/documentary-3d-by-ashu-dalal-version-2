#!/usr/bin/env node
// One command: lint -> words -> render (parallel) -> sfx/music -> mix -> mux.
//   node tools/build.mjs [--story f] [--scale 0.5] [--workers 4] [--mb 4] [--gpu] [--chrome] [--stills 1,4] [--out out/final.mp4] [--realign] [--force]
import fs from 'node:fs';
import os from 'node:os';
import path from 'node:path';
import { spawn, spawnSync } from 'node:child_process';
import { arg, python, getDuration } from './lib.mjs';
import { lint, printIssues } from './lint.mjs';

const project = path.resolve(arg('project', process.cwd()));
const storyFile = arg('story', 'story.json');
const story = JSON.parse(fs.readFileSync(path.join(project, storyFile), 'utf8'));
const py = python();
const run = (cmd, args) => {
  console.log('\n$', cmd, args.join(' '));
  const r = spawnSync(cmd, args, { cwd: project, stdio: 'inherit' });
  if (r.status !== 0) { console.error(`\nStep failed: ${cmd} ${args[0]}`); process.exit(r.status || 1); }
};
const passthru = ['--story', storyFile];
for (const f of ['scale', 'crf', 'preset', 'mb']) if (arg(f)) passthru.push('--' + f, String(arg(f)));
for (const f of ['gpu', 'chrome']) if (arg(f, false)) passthru.push('--' + f);

// 1. words (captions + mouth movement + camera sync)
const wordsPath = path.join(project, story.words || 'words.json');
const hasVoice = story.voice && fs.existsSync(path.join(project, story.voice));
if (!fs.existsSync(wordsPath) || arg('realign', false)) {
  const a = ['tools/align_words.py', '--story', storyFile, '--out', story.words || 'words.json'];
  if (!hasVoice) a.push('--estimate');
  run(py, a);
} else console.log('Using existing', story.words || 'words.json', '(pass --realign to redo)');
if (!hasVoice) console.log('NOTE: no voice file -> silent dry run with estimated word timing. Add story.voice for the real thing.');

// 2. lint: stop on real problems before spending minutes rendering
const issues = lint(project, story);
printIssues(issues);
if (issues.some((i) => i.level === 'FAIL') && !arg('force', false)) { console.error('\nFix the FAIL items above (or pass --force).'); process.exit(2); }

if (arg('stills', false)) { run('node', ['tools/render.mjs', ...passthru, '--stills', String(arg('stills'))]); process.exit(0); }

// 3. render, in parallel chunks (frames are independent because every frame is a pure function of t)
const dur = getDuration(project, story), fps = story.fps || 30, total = Math.round(dur * fps);
const workers = Math.max(1, Math.min(parseInt(arg('workers', Math.min(4, Math.floor(os.cpus().length / 2))), 10), Math.floor(total / 30) || 1));
if (workers <= 1) run('node', ['tools/render.mjs', ...passthru]);
else {
  console.log(`\nRendering ${total} frames with ${workers} parallel workers...`);
  const t0 = Date.now(), chunk = Math.ceil(total / workers), segs = [];
  await Promise.all(Array.from({ length: workers }, (_, k) => new Promise((resolve) => {
    const a = k * chunk, b = Math.min(total, a + chunk), seg = `build/seg_${k}.mp4`; segs.push(seg);
    const p = spawn('node', ['tools/render.mjs', ...passthru, '--from-frame', String(a), '--to-frame', String(b), '--silent', seg, '--quiet'], { cwd: project, stdio: 'inherit' });
    p.on('close', (c) => { if (c !== 0) { console.error(`worker ${k} failed`); process.exit(1); } console.log(`  worker ${k + 1}/${workers} done (${((Date.now() - t0) / 1000).toFixed(0)}s)`); resolve(); });
  })));
  segs.sort();
  fs.writeFileSync(path.join(project, 'build/segs.txt'), segs.map((s) => `file '${path.basename(s)}'`).join('\n'));
  run('ffmpeg', ['-y', '-loglevel', 'error', '-f', 'concat', '-safe', '0', '-i', 'build/segs.txt', '-c', 'copy', 'build/video_silent.mp4']);
}

// 4. audio (Openverse real SFX/music active by default; legacy gen_sfx.py silenced unless --legacy-sfx, ASHU_SOUND_ENGINE=legacy_synth, or sound_config.json)
let cfgLegacy = false;
for (const cfgPath of [path.join(project, 'tools/sound_config.json'), path.resolve(project, '../../documentary-3d/scripts/sound_config.json')]) {
  if (fs.existsSync(cfgPath)) {
    try { cfgLegacy = JSON.parse(fs.readFileSync(cfgPath, 'utf8')).active_engine === 'legacy_synth'; break; } catch {}
  }
}
const useLegacySfx = arg('legacy-sfx', false) || process.env.ASHU_SOUND_ENGINE === 'legacy_synth' || cfgLegacy;
if (useLegacySfx) {
  run(py, ['tools/gen_sfx.py', '--story', storyFile, '--duration', String(dur)]);
} else {
  const localOv = path.join(project, 'tools/openverse_sfx.py');
  const pluginOv = path.resolve(project, '../../documentary-3d/scripts/openverse_sfx.py');
  const openverseScript = fs.existsSync(localOv) ? localOv : pluginOv;
  const kinds = [...new Set((story.sfx || []).map((s) => s.kind).filter(Boolean))];
  const mood = story.music && story.music.kind === 'pad' ? `${story.music.mood || 'dark'} ambient documentary underscore` : '';
  if (fs.existsSync(openverseScript) && (kinds.length || mood)) {
    const ovArgs = [openverseScript, '--out', 'build/sfx'];
    if (kinds.length) ovArgs.push('--sfx', kinds.join(','));
    if (mood) ovArgs.push('--music', mood);
    run(py, ovArgs);
    if (mood && fs.existsSync(path.join(project, 'build/sfx/music_bed.wav'))) {
      fs.copyFileSync(path.join(project, 'build/sfx/music_bed.wav'), path.join(project, 'build/music_pad.wav'));
    }
  }
}
run(py, ['tools/mix_audio.py', '--story', storyFile, '--duration', String(dur)]);

// 5. mux
const out = arg('out', 'out/final.mp4');
fs.mkdirSync(path.dirname(path.join(project, out)), { recursive: true });
run('ffmpeg', ['-y', '-loglevel', 'error', '-i', 'build/video_silent.mp4', '-i', 'build/audio.wav', '-c:v', 'copy', '-af', 'apad', '-c:a', 'aac', '-b:a', '192k', '-t', String(dur), '-movflags', '+faststart', out]);
console.log('\nDONE ->', out);
