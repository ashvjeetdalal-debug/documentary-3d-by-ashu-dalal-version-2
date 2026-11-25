#!/usr/bin/env node
// Environment doctor: proves every dependency works BEFORE you build anything. Run: npm run doctor
import { createRequire } from 'node:module';
import fs from 'node:fs';
import path from 'node:path';
import { spawnSync } from 'node:child_process';
import { arg, python, grayBuffer, frameStats } from './lib.mjs';

const project = path.resolve(arg('project', process.cwd()));
const require = createRequire(import.meta.url);
let bad = 0;
const ok = (m) => console.log('  [ ok ]', m);
const no = (m, fix) => { bad++; console.log('  [FAIL]', m); if (fix) console.log('         fix:', fix); };
const run = (c, a) => spawnSync(c, a, { encoding: 'utf8', cwd: project });

console.log('Doctor');
const major = parseInt(process.versions.node, 10);
major >= 18 ? ok(`node ${process.versions.node}`) : no(`node ${process.versions.node} is too old`, 'install Node 18+ (nodejs.org)');

const ffv = run('ffmpeg', ['-version']);
if (ffv.status) no('ffmpeg not found', 'macOS: brew install ffmpeg | Windows: winget install ffmpeg | Linux: apt install ffmpeg');
else {
  ok(ffv.stdout.split('\n')[0]);
  const enc = run('ffmpeg', ['-hide_banner', '-encoders']).stdout, fil = run('ffmpeg', ['-hide_banner', '-filters']).stdout;
  /libx264/.test(enc) ? ok('libx264 encoder') : no('ffmpeg lacks libx264', 'install a full ffmpeg build');
  /\saac\s/.test(enc) ? ok('aac encoder') : no('ffmpeg lacks aac');
  for (const f of ['sidechaincompress', 'loudnorm', 'amix', 'adelay', 'alimiter']) new RegExp(`\\s${f}\\s`).test(fil) ? ok(`filter ${f}`) : no(`ffmpeg lacks filter ${f}`, 'update ffmpeg (>= 4.4)');
}
run('ffprobe', ['-version']).status ? no('ffprobe not found (ships with ffmpeg)') : ok('ffprobe');

let py = null; try { py = python(); ok(`${py} found`); } catch { no('python 3 not found', 'install Python 3.9+'); }
if (py) run(py, ['-c', 'import numpy']).status ? no('numpy missing', `${py} -m pip install numpy`) : ok('numpy');
if (py) run(py, ['-c', 'import faster_whisper']).status ? console.log('  [info] faster-whisper not installed: word timing will use the energy fallback (pip install faster-whisper for exact captions)') : ok('faster-whisper (exact word timing)');

let playwright = null;
try { playwright = require('playwright'); ok('playwright module'); } catch { no('playwright missing', 'npm run setup'); }
if (playwright) {
  const args = ['--ignore-gpu-blocklist', '--enable-webgl'];
  if (!arg('gpu', false)) args.push('--use-gl=angle', '--use-angle=swiftshader', '--enable-unsafe-swiftshader');
  try {
    const b = await playwright.chromium.launch({ headless: true, args, ...(arg('no-chrome', false) ? {} : { channel: 'chrome' }) });
    const pg = await b.newPage();
    const info = await pg.evaluate(() => {
      const c = document.createElement('canvas'), gl = c.getContext('webgl2');
      if (!gl) return null;
      const e = gl.getExtension('WEBGL_debug_renderer_info');
      return e ? gl.getParameter(e.UNMASKED_RENDERER_WEBGL) : 'webgl2';
    });
    await b.close();
    info ? ok(`browser launches, WebGL2 available (${info})`) : no('browser launched but WebGL2 is unavailable', 'try --chrome (installed Google Chrome) or drop --gpu');
  } catch (e) { no('cannot launch browser: ' + String(e.message).split('\n')[0], 'npx playwright install chromium   (or use --chrome)'); }
}

const threePkg = path.join(project, 'node_modules/three/package.json');
if (!fs.existsSync(threePkg)) no('three is not installed', 'npm install   (in the project folder)');
else {
  ok('three ' + JSON.parse(fs.readFileSync(threePkg, 'utf8')).version);
  if (!bad) {
    console.log('  ...rendering a three.js smoke scene (stage + lights + character + post-processing)');
    const passthru = ['--story', 'story.check.json', '--stills', '1.0', '--stills-dir', 'build/check', '--quiet', '--scale', '0.5'];
    for (const f of ['gpu', 'chrome']) if (arg(f, false)) passthru.push('--' + f);
    const r = run('node', ['tools/render.mjs', ...passthru]);
    const out = path.join(project, 'build/check/still_1.00s.png');
    if (r.status || !fs.existsSync(out)) no('three.js smoke scene failed to render', 'read the error below, fix the cause, rerun doctor:\n' + (r.stderr || r.stdout).split('\n').slice(0, 12).join('\n'));
    else {
      const st = frameStats(grayBuffer(out));
      st.mean < 10 || st.std < 6 ? no(`smoke scene rendered but looks empty (brightness ${st.mean.toFixed(0)}, contrast ${st.std.toFixed(0)})`, 'WebGL context may be broken: try --chrome') : ok(`three.js smoke scene renders (brightness ${st.mean.toFixed(0)}, contrast ${st.std.toFixed(0)})`);
      const warn = (r.stderr || '').split('\n').filter((l) => l.includes('[page warning]') && /post|bloom|bokeh|composer/i.test(l));
      if (warn.length) console.log('  [info] post-processing fell back (still renders, just without bloom/DOF):', warn[0]);
    }
  }
}
console.log(bad ? `\n${bad} problem(s). Fix them, then run: npm run doctor` : '\nAll good. Next: npm run selftest, then build your story.');
process.exit(bad ? 1 : 0);
