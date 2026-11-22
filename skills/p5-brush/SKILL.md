---
name: p5-brush
description: Create animated generative art, hand-drawn illustrations, watercolor washes, charcoal sketches, hatching textures, and organic vector flow fields in code using the official p5.brush natural media engine. Use when the user wants an animated drawing, a hand-sketched diagram, a watercolor map, charcoal character art, hatched shading, or natural organic strokes rendered frame-by-frame.
---

# p5.brush — Natural Generative Media Engine

Create procedural organic media that animates in code without physical scanners or hand illustration. `p5.brush` brings the tactile physics of pencils, markers, charcoal, watercolor bleeding, and pen hatching to digital canvases.

---

## ⚡ The Two Builds

`p5.brush` provides two distinct builds in `dist/`:

| Feature | **Standalone Build** (Recommended for pure code) | **p5.js Build** |
|---|---|---|
| **File** | `dist/brush.js` or `dist/brush.esm.js` | `dist/p5.brush.js` or `dist/p5.brush.esm.js` |
| **Dependencies** | None (WebGL2 browser context only) | `p5.js 2.x` |
| **Canvas** | `brush.createCanvas(width, height)` | `createCanvas(width, height, WEBGL)` |
| **Transformations** | `brush.push()`, `brush.pop()`, `brush.translate()`, `brush.rotate()` | p5's `push()`, `pop()`, `translate()`, `rotate()` |
| **Clearing** | `brush.clear(color)` | `background(color)` |
| **Frame Flush** | **Must call `brush.render()` at end of frame** | Automatic |
| **Angle Mode** | `brush.angleMode(brush.DEGREES)` | `angleMode(DEGREES)` |

---

## 🖌️ Brushes & Natural Media

Select a brush with `brush.set(brushName, color, weight)`:

- **Pencils**: `"HB"`, `"2B"`, `"cpencil"` (colored pencil with pressure tooth)
- **Charcoal**: `"charcoal"`, `"charcoal2"` (rough powdery drag)
- **Ink & Pens**: `"pen"`, `"rotring"`, `"ballpoint"` (crisp architectural lines)
- **Markers**: `"marker"`, `"marker2"` (semi-translucent felt marker overlay)
- **Watercolor**: `"watercolor"` (pigment pooling, soft bleed, and edge darkening)
- **Spray & Airbrush**: `"spray"` (diffuse stippled noise)

### Customizing Pressure & Vibration:
```javascript
brush.set("charcoal", "#1a1a1a", 2.5);
brush.setVibration(0.4);      // Hand tremor / jitter
brush.setPressure(0.8);       // Brush down-pressure
brush.setBleed(0.25);         // Watercolor bleed expansion
```

---

## 📐 Hatching & Vector Flow Fields

### Cross-Hatching Textures:
```javascript
// brush.hatch(distance, angle, options)
brush.hatch(8, 45, { rand: 0.2, continuous: true, min: 2, max: 12 });
brush.rect(100, 100, 300, 200);
```

### Flow Fields / Vector Fields:
Make strokes curve organically along Perlin noise fields:
```javascript
brush.field("perlin");
brush.flowLine(x, y, length, stepSize);
```

---

## 🎬 Deterministic Time Animation Contract

For frame-by-frame video rendering via headless Chrome:
1. **Rule 1**: Every stroke, path, and hatch must be a pure function of normalized time `t` (seconds).
2. **Deterministic Seed**: Always call `brush.seed(seedValue)` or `brush.noiseSeed(seedValue)` at the start of `renderAt(t)`. Never use non-deterministic `Math.random()`.
3. **Flushing**: In standalone build, finish with `brush.render()`.
4. **Offline Rendering**: Use `kit/render_brush.mjs` to pipe canvas frames into `ffmpeg` at 30 fps.
