/**
 * p5.brush <-> Three.js Universal Bridge Module (Version 3)
 * Renders deterministic standalone p5.brush generative canvases (watercolor, charcoal,
 * cross-hatching, marker, flow_field) with proper WebGL2 center-to-topleft framing
 * and binds them live onto Three.js 3D meshes via CanvasTexture.
 */

import * as THREE from 'three';
import * as brush from '/plugin/skills/p5-brush/dist/brush.esm.js';

export const BRUSH_PRESETS = ['watercolor', 'charcoal', 'hatching', 'marker', 'flow_field', 'pencil_hb'];

export class BrushTextureTarget {
  constructor(width = 1024, height = 1024) {
    this.width = width;
    this.height = height;

    this.canvas = document.createElement('canvas');
    this.canvas.width = width;
    this.canvas.height = height;

    brush.load(this.canvas);
    brush.scaleBrushes(Math.max(1.5, width / 450));
    brush.angleMode(brush.DEGREES);

    this.texture = new THREE.CanvasTexture(this.canvas);
    this.texture.colorSpace = THREE.SRGBColorSpace;
    this.texture.anisotropy = 8;
  }

  /**
   * Render a deterministic standalone p5.brush frame into this target texture.
   * Wraps transforms cleanly in (-W/2, -H/2) and flushes via brush.render().
   */
  update(t, drawCallbackOrPreset = 'watercolor', palette = ['#f4efe4', '#242936', '#d0312d']) {
    const W = this.width, H = this.height;
    const [bg, ink, accent] = palette;

    brush.load(this.canvas);
    brush.seed(1337 + (Math.floor(t * 12) % 3)); // subtle deterministic media tooth
    brush.noiseSeed(42);
    brush.clear(bg);
    brush.push();
    brush.translate(-W / 2, -H / 2);

    if (typeof drawCallbackOrPreset === 'function') {
      drawCallbackOrPreset(brush, t, { W, H, bg, ink, accent });
    } else {
      drawPreset(brush, drawCallbackOrPreset, t, { W, H, bg, ink, accent });
    }

    brush.pop();
    brush.render();
    this.texture.needsUpdate = true;
  }

  createMaterial(options = {}) {
    return new THREE.MeshStandardMaterial({
      map: this.texture,
      roughness: options.roughness ?? 0.85,
      metalness: options.metalness ?? 0.0,
      ...options
    });
  }
}

function drawPreset(b, preset, t, { W, H, ink, accent }) {
  const prog = Math.min(1, Math.max(0.15, t / 3.5));
  b.noFill();
  b.noHatch();

  if (preset === 'watercolor') {
    b.noStroke();
    b.fill(ink, 75);
    b.fillBleed(0.25);
    b.fillTexture(0.45, 0.3);
    b.circle(W * 0.42, H * 0.45, 220 * prog + 60);
    b.fill(accent, 110);
    b.fillBleed(0.22);
    b.circle(W * 0.62, H * 0.52, 150 * prog + 40);
    b.noFill();
    b.set('HB', ink, 1.4);
    b.line(80, H * 0.78, 80 + (W - 160) * prog, H * 0.78);
  } else if (preset === 'charcoal') {
    b.set('charcoal', ink, 3.2);
    for (let i = 0; i < 6; i++) {
      const y = 140 + i * 130;
      b.line(100, y, 100 + (W - 200) * Math.min(1, prog * 1.2 - i * 0.08), y + Math.sin(i * 2) * 18);
    }
    b.set('marker', accent, 4.0);
    b.circle(W * 0.5, H * 0.5, 190 * prog);
  } else if (preset === 'hatching') {
    b.hatch(18, 45, { rand: 0.15, continuous: true });
    b.set('rotring', ink, 1.6);
    b.rect(110, 140, (W - 220) * prog, H - 280);
    b.noHatch();
    b.set('pen', accent, 2.8);
    b.rect(110, 140, (W - 220) * prog, H - 280);
  } else if (preset === 'flow_field') {
    b.field('waves');
    b.refreshField(t * 0.4);
    b.set('cpencil', ink, 1.8);
    for (let i = 0; i < 18; i++) {
      const y = 120 + i * 44;
      b.flowLine(100, y, (W - 200) * prog, 0);
    }
    b.noField();
    b.set('pen', accent, 3.0);
    b.circle(W * 0.5, H * 0.5, 130);
  } else if (preset === 'marker') {
    b.set('marker', accent, 6.0);
    b.line(120, H * 0.45, 120 + (W - 240) * prog, H * 0.45);
    b.set('HB', ink, 2.0);
    b.rect(120, H * 0.25, W - 240, H * 0.5);
  } else {
    // pencil_hb
    b.set('HB', ink, 1.8);
    b.rect(90, 90, W - 180, H - 180);
    b.line(90, 90, 90 + (W - 180) * prog, 90 + (H - 180) * prog);
    b.set('pen', accent, 2.2);
    b.circle(W / 2, H / 2, 160 * prog);
  }
}
