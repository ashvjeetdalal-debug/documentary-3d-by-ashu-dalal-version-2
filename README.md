# Documentary 3D by Ashu Dalal Version 2

An industrial-grade, code-driven cinematic video production suite.

This unified studio fuses **four powerful film-making technologies** into a single cohesive development environment:

1. **Ashu Dalal / Kaz Documentary Engine**: 2.5D investigative evidence board (pinned photos, red yarn/strings, typewriter labels, stamps, smooth camera moves) + vintage 2D silent-film inserts (boiling lines, iris wipes, intertitle cards).
2. **Three.js 3D Procedural Studio (`kit/`)**: Headless Chrome offline renderer (no Blender), 12 shader looks (`lit`, `clay`, `paper`, `blueprint`, `toon`, `synth`, etc.), sub-frame motion blur, depth of field, real phone shake physics (`phone_motion.py`, `handheld.py`), and vertical social reels (`laptop_reel.py`).
3. **p5.brush Generative Natural Media Engine (`skills/p5-brush/`)**: Official `p5.brush` engine for procedural charcoal, watercolor wash & bleed, colored pencils, felt markers, architectural cross-hatching, and vector flow fields rendered frame-by-frame.
4. **Lemo-Opuscar Directorial Studio (`skills/lemo-opuscar/`)**: 100 complete code-driven film styles (`dark-documentary`, `archive-lighttable`, `briefing-board`, `circuit-board`, `comic-history`, etc.), the legendary `DIRECTOR.md` (narrative rhythm, music grid, camera blocking), and `TECHNIQUE.md` (frame synthesis, automated TTS, EBU R128 audio mastering).

---

## 📂 Suite Directory Structure

```text
documentary-3d-by-ashu-dalal/
├── plugin.json                 # Studio Edition plugin manifest
├── README.md                   # Full master documentation
├── INSTALL.txt                 # Setup & dependencies guide
├── 3D-Animator-Skill.pdf       # 3D animation manual
├── assets/
│   └── logo.svg                # Master plugin badge
├── rules/
│   └── AGENTS.md               # Unified production & creative laws
├── guides/                     # Core directorial & production manuals
│   ├── DIRECTOR.md             # Narrative rhythm, music grid, camera blocking
│   ├── TECHNIQUE.md            # Technical rendering, audio pipelines, QA
│   ├── MY-STYLES.md            # Creating and customizing new styles
│   └── MAINTAINING.md          # Toolchain maintenance
└── skills/
    ├── documentary-3d/         # Master documentary workflow skill
    │   ├── SKILL.md
    │   ├── references/         # Deep reference manuals (lighting, camera, styles, sound)
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

## 🎨 Creative Highlights

### 1. The 12 3D Shader Styles (`kit/styles.js`)
Switch styles on the fly via query parameter or flag (`--style=<name>`):
- **`lit`**: Photorealistic cinematic room lighting with motivated keys and sky fill.
- **`clay`**: Matte ivory sculpt maquette.
- **`paper`**: Textured construction paper cutout with dark edges.
- **`shadow`**: Backlit shadow puppet silhouettes.
- **`blueprint`**: Deep architectural navy with crisp white construction wireframes.
- **`toon`**: Cel-shaded 3-band comic book look with hand-inked outlines.
- **`voxel`**: Tiny cubic discretization under dynamic lighting.
- **`thermal`**: Infrared heat vision gradient (cold blue to white-hot).
- **`synth`**: 80s synthwave neon magenta grid with cyan outlines.
- **`chrome`**: Liquid mercury polished metal reflections.
- **`neon`**: Night-time room washed in vivid neon tubes.
- **`mix`**: Multi-style composite per scene object.

### 2. Natural Media Simulation (`skills/p5-brush/`)
- Pressure-sensitive pencils (`HB`, `2B`, `cpencil`), rough charcoal, semi-translucent markers, and watercolor pigment washes with authentic bleed physics.
- Cross-hatching algorithms and Perlin flow fields.

### 3. Directing with the Music Grid (`guides/DIRECTOR.md`)
- Tempo-based pacing (BPM grids).
- Camera blocking without static monotony.
- Minimum 1.8-second subtitle duration rules.

### 4. Broadcast Audio Engineering
- Procedural tension drones and pulses (`sound_bed.py`).
- Automatic sidechain ducking of background music under speech.
- Master normalization strictly calibrated to **-14 LUFS** and **-1.5 dBTP** (EBU R128).

---

## 🛠️ Quick Commands

### 1. Render 3D Scenes:
```bash
cd skills/documentary-3d/scripts/kit
npm run stills
npm run preview
npm run final
```

### 2. Render p5.brush Generative Drawings:
```bash
cd skills/p5-brush/kit
npm run stills
npm run preview
```

### 3. Render 2.5D Evidence Board:
```bash
cd skills/documentary-3d/scripts
python board_engine.py stills 2,5
python board_engine.py full 0 300 board.mp4
```

### 4. Create Vertical Mockup Reel (9:16):
```bash
python skills/documentary-3d/scripts/kit/present/laptop_reel.py laptop.png out/final.mp4 200 450 680 380 out/reel.mp4 motion.csv
```

---

## 📜 Credits & Attributions
- **Ashu Dalal**: Suite creator & documentary director.
- **p5.brush**: Alejandro Campos Uribe (`acamposuribe/p5.brush`).
- **Lemo-Opuscar**: Lemomo AI (`lemomo-ai/lemo-opuscar`).
- **Three.js**: Mr.doob and Three.js contributors.
