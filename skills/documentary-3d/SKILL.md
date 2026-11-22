---
name: documentary-3d-by-ashu-dalal-version-2
description: Master skill for Documentary 3D by Ashu Dalal Version 2. Use when the user asks to "make an Ashu Dalal documentary", "make a 3D documentary video", "create an evidence-board video", "animate a history script with 3D scenes", "turn voiceover into a cinematic documentary", "add a vintage 2D silent-film section", "draw an animated sketch with p5.brush", or wants a procedural short film using any of the 100+ Lemo-Opuscar styles.
---

# Documentary 3D by Ashu Dalal Version 2

Build narrated cinematic documentary videos entirely in code. This suite fuses **4 world-class video production engines**:

1. **Ashu Dalal Evidence-Board & Vintage 2D Engine**: Pinned archival photos, red yarn/strings, wobble focus circles, typewriter labels, slammed rubber stamps, continuous camera motion, and vintage silent-film inserts.
2. **Three.js 3D Procedural Engine (`kit/`)**: Headless Chrome frame-by-frame renderer (no Blender), 12 procedural shader looks, sub-frame motion blur, depth-of-field, and soft shadows.
3. **p5.brush Natural Generative Media Engine (`skills/p5-brush/`)**: Procedural charcoal, watercolor bleeding, colored pencils, felt markers, architectural hatching, and vector flow fields rendered frame-by-frame.
4. **Lemo-Opuscar Studio (100+ Styles) (`skills/lemo-opuscar/`)**: 100 curated film styles (`styles/`), core directorial guides (`guides/DIRECTOR.md`), technical execution manuals (`guides/TECHNIQUE.md`), and automated audio scoring pipelines.

---

## 🗂️ Unified Suite Directory Structure

```text
documentary-3d-by-ashu-dalal/
├── plugin.json                 # Studio Edition plugin manifest
├── README.md                   # Full master guide & documentation
├── INSTALL.txt                 # Setup & dependencies guide
├── 3D-Animator-Skill.pdf       # Complete 3D animation reference manual
├── assets/
│   └── logo.svg                # Master logo badge
├── rules/
│   └── AGENTS.md               # Unified production & creative rules
├── guides/                     # Core directorial & production manuals
│   ├── DIRECTOR.md             # Narrative rhythm, music grid, camera blocking, treatment
│   ├── TECHNIQUE.md            # Technical rendering, audio pipelines, QA loops
│   ├── MY-STYLES.md            # Authoring and saving new custom styles
│   └── MAINTAINING.md          # System maintenance & toolchain notes
└── skills/
    ├── documentary-3d/         # Primary documentary workflow skill
    │   ├── SKILL.md
    │   ├── references/         # In-depth reference manuals
    │   │   ├── 3d-styles.md
    │   │   ├── camera.md
    │   │   ├── engine-guide.md
    │   │   ├── film-styles-catalog.md # 100 styles index
    │   │   ├── light.md
    │   │   ├── motion.md
    │   │   ├── p5-brush-guide.md
    │   │   ├── present.md
    │   │   ├── sound.md
    │   │   └── style-guide.md
    │   └── scripts/
    │       ├── board_engine.py      # 2.5D Evidence Board renderer
    │       ├── vintage_engine.py    # Vintage silent-film 2D engine
    │       ├── align_timing.py      # Silence detection & timing aligner
    │       ├── sound_bed.py         # Algorithmic drone & pulse synthesizer
    │       ├── mix_and_mux.py/.sh   # Sidechain ducking & -14 LUFS multiplexer
    │       ├── splice.py/.sh        # Frame-accurate video splicing
    │       └── kit/                 # 3D Procedural Engine & Presentation Tools
    │           ├── index.html       # WebGL stage canvas
    │           ├── film.js          # 3D scene definition (pure function of time)
    │           ├── styles.js        # 12 artistic shader looks
    │           ├── render.mjs       # Headless Chrome offline renderer
    │           ├── lib.js           # Easing curves, Halton jitter, hash math
    │           ├── mix.py           # Multitrack audio mixer (-14 LUFS)
    │           ├── package.json     # Three.js + Puppeteer configuration
    │           └── present/
    │               ├── phone_motion.py # Camera shake extractor (2D FFT)
    │               ├── handheld.py     # Camera shake injector
    │               └── laptop_reel.py/.sh # Laptop/phone mockup reel generator
    ├── p5-brush/               # Natural Media Generative Drawing Skill
    │   ├── SKILL.md            # Brush usage & animation guide
    │   ├── llms.txt            # Complete API spec for code generation
    │   ├── dist/               # Standalone and p5 production builds
    │   ├── src/                # Full library source code
    │   ├── examples/           # Official demo sketches
    │   └── kit/                # Ready-to-render template (render_brush.mjs)
    └── lemo-opuscar/           # 100+ Film Styles & Studio Skill
        ├── SKILL.md            # Production guide for styles
        ├── core/               # Shared rendering, audio, post-processing tools
        └── styles/             # 100 complete film style folders
```

---

## 🎬 Master 5-Stage Production Workflow

1. **Intake & Aesthetic Selection**:
   - Collect voiceover / text script and archival materials.
   - Choose visual engines: Evidence Board for paper trails; Three.js 3D for physical spaces & objects; p5.brush for natural hand-sketched maps; Lemo-Opuscar style (`dark-documentary`, `blueprint`, `archive-lighttable`) for complete aesthetic thematic coherence.
2. **Treatment & Music Grid (`guides/DIRECTOR.md`)**:
   - Write a `TREATMENT.md` defining the 3-act narrative arc.
   - Lock visual events and sentence starts to a defined BPM tempo grid.
3. **Scene Programming**:
   - Adhere to the core law: Every frame is a pure function of time `renderAt(t)`.
   - Use deterministic seeds (`brush.seed(42)`, `hash(n)`).
4. **Offline Frame-by-Frame Rendering**:
   - Use `kit/render.mjs` for Three.js 3D (sub-frame jitter `n=16` for stills, `n=48` for finals).
   - Use `skills/p5-brush/kit/render_brush.mjs` for natural brush animations.
   - Use `board_engine.py` for Evidence Board video.
   - Splice scenes together seamlessly with `splice.py`.
5. **Sound Design & Master QC**:
   - Synthesize or mix audio cues with `sound_bed.py` and `mix.py`.
   - Sidechain duck score under speech and master strictly to **-14 LUFS** (ceiling **-1.5 dBTP**) via `mix_and_mux.py`.
