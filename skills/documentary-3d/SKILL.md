---
name: documentary-3d-by-ashu-dalal-version-2
description: Master skill for Documentary 3D by Ashu Dalal Version 2. Use when the user asks to "make an Ashu Dalal documentary", "make a 3D documentary video", "create an evidence-board video", "animate a history script with 3D scenes", "turn voiceover into a cinematic documentary", "add a vintage 2D silent-film section", "draw an animated sketch with p5.brush", or wants a procedural short film using any of the 100+ Lemo-Opuscar styles.
---

# Documentary 3D by Ashu Dalal Version 2

Build narrated cinematic documentary videos entirely in code. This suite fuses **6 world-class video production engines**:

1. **Ashu Dalal Evidence-Board & Vintage 2D Engine**: Pinned archival photos, red yarn/strings, wobble focus circles, typewriter labels, slammed rubber stamps, continuous camera motion, and vintage silent-film inserts.
2. **Three.js 3D Procedural Engine (`kit/`)**: Headless Chrome frame-by-frame renderer (no Blender), 12 procedural shader looks, sub-frame motion blur, depth-of-field, and soft shadows.
3. **p5.brush Natural Generative Media Engine (`skills/p5-brush/`)**: Procedural charcoal, watercolor bleeding, colored pencils, felt markers, architectural hatching, and vector flow fields rendered frame-by-frame.
4. **Lemo-Opuscar Studio (100+ Styles) (`skills/lemo-opuscar/`)**: 100 curated film styles (`styles/`), core directorial guides (`guides/DIRECTOR.md`), technical execution manuals (`guides/TECHNIQUE.md`), and automated audio scoring pipelines.
5. **WhisperX / Word-Level Speech Sync Engine (`audio_sync.py`)**: Automatic forced word-level alignment across any language (English, Hindi, Hinglish), broadcast subtitle timing (min 1.8s hold), and 1-2 frame camera trigger marks.
6. **Automated Archival Asset Fetcher (`asset_fetcher.py`)**: Automatic discovery, download, and PIL verification of authentic historical assets from Wikimedia Commons/Wikipedia without synthetic slop.

---

## 🗂️ Unified Suite Directory Structure

```text
documentary-3d-by-ashu-dalal/
├── plugin.json                 # Studio Edition plugin manifest
├── README.md                   # Full master guide & documentation
├── INSTALL.txt                 # Setup & dependencies guide
├── studio.py                   # Master Unified Studio CLI
├── 3D-Animator-Skill.pdf       # Complete 3D animation reference manual
├── assets/
│   └── logo.svg                # Master logo badge
├── rules/
│   └── AGENTS.md               # Unified production & creative laws
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
    │       ├── audio_sync.py        # WhisperX / Whisper forced word-level alignment
    │       ├── asset_fetcher.py     # Automated authentic archival asset sourcing
    │       ├── board_engine.py      # 2.5D Evidence Board renderer
    │       ├── vintage_engine.py    # Vintage silent-film 2D engine
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
    └── lemo-opuscar/           # 100+ Film Styles & Studio Skill
```

---

## 🎬 Master 6-Stage Production Workflow

### Stage 1: Audio Intake & Forced Word-Level Alignment (WhisperX)
- Input voiceover audio (`.wav` or `.mp3`).
- Run `python studio.py --sync-audio=<path>` to generate `sync_timeline.json`.
- Outputs exact sentence intervals, word timestamps for kinetic subtitles (min 1.8s hold), and visual cue marks.

### Stage 2: Automatic Archival Asset Acquisition
- If authentic assets are not provided, run `python studio.py --fetch-assets="<topic, entities>"` to query Wikimedia Commons / Wikipedia.
- Never generate synthetic placeholder slop. Every asset is verified for resolution, aspect ratio, and clean RGB mode.

### Stage 3: Treatment & Unified Camera Choreography (`DIRECTOR.md`)
- Lock visual actions, pushpin slams, and 3D camera transitions within **1–2 frames** of the spoken trigger words from `sync_timeline.json`.
- Adhere to the Single Continuous Camera Grammar: One camera move = one lens, one Bezier curve, one progress parameter.

### Stage 4: Scene Programming
- Every frame must be a pure function of time `renderAt(t)`.
- Use deterministic seeds (`brush.seed(42)`, `hash(n)`).

### Stage 5: Offline Frame-by-Frame Rendering
- Use `render.mjs` for Three.js 3D (sub-frame jitter `n=16` for inspections, `n=48` for master finals).
- Use `render_brush.mjs` for natural media p5.brush animations.
- Use `board_engine.py` for Evidence Board video.

### Stage 6: Sound Design & Master QC
- Synthesize tension sound beds with `sound_bed.py`.
- Sidechain duck score under voiceover (-14 dB to -18 dB gain reduction during speech).
- Master output normalized strictly to **-14 LUFS** with a true peak ceiling of **-1.5 dBTP** via `mix_and_mux.py`.
