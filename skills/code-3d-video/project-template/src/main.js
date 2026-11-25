import { Timeline, makeRng } from './timeline.js';
import { Captions } from './captions.js';

try {
  const params = new URLSearchParams(location.search);
  const story = await (await fetch('./' + (params.get('story') || 'story.json'))).json();
  let words = [];
  try { words = await (await fetch('./' + (story.words || 'words.json') + '?v=' + Date.now())).json(); } catch (e) { /* captions optional */ }

  const canvas = document.getElementById('c');
  const fps = story.fps || 30;
  const camera = new Timeline(story.camera || [], story.cameraTension ?? 1);
  const captions = new Captions(document.getElementById('captions'), words, story.captions || {});
  const labelEl = document.getElementById('label');
  const labels = story.labels || [];

  let scene;
  const engine = story.engine || 'three';
  if (engine === 'canvas') {
    scene = await (await import('./selftest_scene.js')).build({ canvas, story, words });
  } else {
    const THREE = await import('three');
    const mod = await import(engine === 'three-check' ? './three_check.js' : './scene.js');
    scene = await mod.build({ THREE, canvas, story, words, rng: makeRng(story.seed || 1) });
  }

  // Motion blur = temporal supersampling: render `sub` sub-frames across the shutter interval and average them.
  const acc = document.createElement('canvas');
  acc.style.cssText = 'position:absolute;inset:0;width:100%;height:100%;display:none';
  canvas.after(acc);
  const actx = acc.getContext('2d');
  const stateAt = (tt, word) => ({ camera: camera.sample(tt), speaking: !!word, word });

  // The renderer calls this once per output frame with an exact time in seconds.
  window.__renderFrame = (t, sub = 1, shutter = 0.5) => {
    const word = captions.update(t);
    const L = labels.find((l) => t >= l.t0 && t <= l.t1);
    if (L) {
      labelEl.textContent = L.text;
      labelEl.style.opacity = String(Math.max(0, Math.min(1, (t - L.t0) / 0.25, (L.t1 - t) / 0.25)));
    } else labelEl.style.opacity = '0';
    if (sub <= 1) { acc.style.display = 'none'; scene.update(t, stateAt(t, word)); return; }
    for (let i = 0; i < sub; i++) {
      const tt = Math.max(0, t + ((i + 0.5) / sub - 0.5) * (shutter / fps));
      scene.update(tt, stateAt(tt, word));
      if (i === 0) { acc.width = canvas.width; acc.height = canvas.height; }
      actx.globalAlpha = 1 / (i + 1);          // running mean of the sub-frames
      actx.drawImage(canvas, 0, 0);
    }
    actx.globalAlpha = 1;
    acc.style.display = 'block';
  };

  await document.fonts.ready;
  window.__ready = true;
} catch (e) {
  window.__error = String((e && e.stack) || e);
  console.error(window.__error);
}
