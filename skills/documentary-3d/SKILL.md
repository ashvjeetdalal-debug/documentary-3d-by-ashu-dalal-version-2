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
5. **WhisperX / Word-Level Speech Sync Engine (`audio_sync.py`)**: Automatic forced word-level alignment across English, Hindi, and Hinglish speech. Calculates exact word timings, kinetic typography, subtitle blocks (holding min 1.8s), and 1–2 frame visual cue marks.
6. **Automated Archival Asset Fetcher (`asset_fetcher.py`)**: Automatic discovery, download, and PIL verification of authentic historical assets from Wikimedia Commons/Wikipedia without synthetic slop.

---

## 🎬 Canonical 5-Step Director Workflow

When producing a documentary, follow this step-by-step protocol:

### Step 1: Topic & Script Formulation
- Present high-impact topics/ideas on events, persons, or historical turning points.
- Once the operator confirms the topic, generate the cinematic documentary script.

### Step 2: Voiceover Audio Intake
- Ask the operator for the voiceover audio file (`.wav`/`.mp3`), or offer automated speech generation.

### Step 3: Zero-Fake Original Archival Asset Sourcing
- Execute `asset_fetcher.py` to source authentic historical assets from Wikimedia Commons / Wikipedia.
- **Rule**: NO FAKE ASSETS or cheap synthetic placeholders. Every asset must be verified for resolution and clean RGB format.

### Step 4: WhisperX Audio Mapping & Gap Analysis
- Execute `audio_sync.py` to compute word-level timestamps.
- Match assets to the transcript and identify **gap spaces** (*khali parts* where no archival media exists).

### Step 5 & Substep 5(1): Interactive Consultation for Gap Spaces
- Ask the operator which visual style they want for the gap spaces, presenting the 3 creative engines:
  1. **Lemo-Opuscar Studio**: Film styles (`dark-documentary`, `archive-lighttable`, `briefing-board`, `blueprint`, etc.).
  2. **p5.brush**: Natural media (Charcoal sketches, watercolor washes, architectural hatching, graphite pencils).
  3. **3D-Animator (Three.js)**: 12 procedural shader looks (`clay`, `paper`, `blueprint`, `lit`, `synth`, `chrome`, `neon`, etc.).
- Present the recommended style list. If the operator asks for more styles, provide additional options from the library.

### Step 6: Deterministic Rendering & Audio Mastering
- Render scenes using deterministic pure functions of time `renderAt(t)`.
- Sidechain duck score under voiceover (-14 dB to -18 dB) and master to **-14 LUFS** (true peak **-1.5 dBTP**).
