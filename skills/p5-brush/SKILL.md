---
name: p5-brush
description: Natural generative media engine (charcoal, watercolor washes, pencils, hatching, vector flow fields) using official p5.brush. In Documentary 3D Version 3 workflows, follow rules/AGENTS.md first: use p5-brush strictly for no-asset gap segments (Step 5) or --combo 3D surface textures unless the user explicitly asks for standalone brush art.
---

# p5.brush — Natural Generative Media Engine

> [!NOTE]
> **Version 3 Role Rule**: For full documentaries, **Main Ashu-Dalal (`board_engine.py` / `code-3d-video`)** handles all asset-backed narration. Use `p5.brush` only for missing-asset *"khali"* gaps (after operator Step 5 consultation) or `--combo` 3D `CanvasTexture` layers, unless asked standalone.

Create procedural organic media that animates in code without physical scanners or hand illustration. See `../documentary-3d/references/p5-brush-guide.md` for full API details.

---

## ⚡ The Two Builds

| Feature | **Standalone Build** (Default in headless kit) | **p5.js Build** |
|---|---|---|
| **File** | `dist/brush.js` or `dist/brush.esm.js` | `dist/p5.brush.js` or `dist/p5.brush.esm.js` |
| **Origin / Transforms** | `brush.push(); brush.translate(-W/2, -H/2); ... brush.pop();` | p5's `push()`, `translate(-width/2, -height/2)`, `pop()` |
| **Clearing** | `brush.clear(color)` | `background(color)` |
| **Frame Flush** | **Must call `brush.render()` at end of frame** | Automatic |
| **Seeding / Angles** | `brush.seed(n)`, `brush.noiseSeed(n)`, `brush.angleMode(brush.DEGREES)` | `randomSeed(n)`, `noiseSeed(n)`, `angleMode(DEGREES)` |

---

## 🖌️ Real Built-in Brushes & Watercolor Fills

Select a stroke brush with `brush.set(brushName, color, weight)`:

- **Pencils**: `"HB"`, `"2B"`, `"2H"`, `"cpencil"`
- **Charcoal & Crayon**: `"charcoal"`, `"pastel"`, `"crayon"`
- **Ink & Pens**: `"pen"`, `"rotring"`
- **Markers & Spray**: `"marker"`, `"spray"`

*(Important: `"watercolor"` is **NOT** a `brush.set()` stroke brush — use `brush.fill()` + `brush.fillBleed()` + `brush.fillTexture()` for watercolor washes!)*

```javascript
brush.clear("#f5f0e0");
brush.push();
brush.translate(-W / 2, -H / 2);

// Charcoal / Pencil / Pen strokes + hand wobble:
brush.wiggle(0.35);
brush.set("charcoal", "#1a1a1a", 2.5);
brush.line(80, 120, 520, 120);

// Authentic Watercolor Fill:
brush.noStroke();
brush.fill("#d0312d", 110);
brush.fillBleed(0.22);
brush.fillTexture(0.45, 0.30);
brush.circle(300, 300, 140);

brush.pop();
brush.render(); // REQUIRED in standalone build
```

---

## 📐 Hatching & Vector Flow Fields

- **Cross-Hatching**: `brush.hatch(dist, angle, { rand: 0.2, continuous: true }); brush.rect(100, 100, 300, 200); brush.noHatch();`
- **Built-in Vector Fields** (`"hand"`, `"curved"`, `"zigzag"`, `"waves"`, `"seabed"`, `"spiral"`, `"columns"`):
```javascript
brush.field("waves");
brush.refreshField(t);
brush.flowLine(x, y, length, 0);
brush.noField();
```

---

## 🎬 Deterministic Time & Combo Integration

1. Every frame must be a pure function of `t` (`renderAt(t)`), using fixed seeds (`brush.seed(42)`).
2. Always place `brush.esm.js` inside the served HTTP root or use `studio.py --combo --brush=<preset>`.
3. Standalone render: `kit/render_brush.mjs` -> `ffmpeg` @ 30 fps. Combined 3D projection: `BrushTextureTarget` (`../documentary-3d/scripts/kit/p5_brush_texture.js`).
