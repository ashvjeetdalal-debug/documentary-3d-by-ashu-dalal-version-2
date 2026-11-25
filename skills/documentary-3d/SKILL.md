---
name: documentary-3d-by-ashu-dalal-version-3
description: Master Documentary & 3D Production Suite by Ashu Dalal. Strictly follows the primary Ashu-Dalal Evidence-Board + Code-3D-Video Documentary backbone for all asset-backed narration, uses WhisperX for word-level alignment, downloads real verified internet archival assets (zero fake assets), uses Openverse for real SFX/music (legacy synth silenced but preserved), and invokes p5.brush / lemo-opuscar / 3D-animator ONLY for empty no-asset gaps after operator consultation.
---

# Documentary 3D by Ashu Dalal Version 3 (Restored Main Backbone + Gap Engines + Openverse Audio)

Build narrated cinematic documentary videos in code, preserving the **original Ashu Dalal (`kaz-documentary`) Evidence-Board** and **original 3D (`code-3d-video`)** main files intact as the primary backbone.

---

## ⚠️ STRICT SYSTEM HIERARCHY (DO NOT COMPROMISE)

1. **MAIN BACKBONE ALWAYS FIRST (`kaz-documentary` + `code-3d-video`)**:
   - Wherever real verified archival assets exist for spoken words/sentences, you **MUST** render strictly using the main Ashu Dalal Documentary grammar (`board_engine.py` evidence-board + `skills/code-3d-video/` 3D kit). Never dilute, rewrite, or override the main documentary system with arbitrary custom scenes.
2. **GAP-ONLY FALLBACK ENGINES (`p5.brush`, `lemo-opuscar`, `3D-animator`)**:
   - `p5.brush`, `lemo-opuscar`, and `3D-animator` (`kit/`) exist in this plugin **STRICTLY for words/segments where NO archival asset exists** (*"khali parts"* / empty gaps).
   - Never use them to override asset-backed parts, and never choose a gap style on your own — always run Step 5(1) consultation with the operator first.
3. **SOUND ENGINE DEFAULT (`Openverse` Active, Legacy Synth Silenced Not Deleted)**:
   - Use **`openverse_sfx.py`** (WordPress Openverse Audio API `https://api.openverse.org/v1/audio/`) for real CC-licensed SFX and music beds mixed via `kit/mix.py` / `mix_and_mux.py`.
   - Legacy synthesized sound (`sound_bed.py`, `gen_sfx.py`) is **silenced by default** (NOT deleted) via `sound_config.json`, so it can be re-enabled anytime if needed.

---

## 🎬 Canonical 5-Step Director Workflow

### Step 1: Topic / Idea Selection & Script
- Present strong documentary topic ideas on historical events, covert operations, technology, or people.
- Once the operator selects a topic, write a tightly paced documentary script (150 wpm, one visual per sentence, hook in first 3s).

### Step 2: Voiceover Audio Intake
- Ask the operator for the voiceover audio file (`.wav`/`.mp3`), or offer to generate the voiceover. Receive audio before building scenes.

### Step 3: Real Original Internet Archival Asset Sourcing (NO FAKE ASSETS)
- If assets are not provided, **immediately upon receiving audio**, fetch real historical photos, maps, diagrams, and documents using [`asset_fetcher.py`](scripts/asset_fetcher.py) (Wikimedia Commons / Wikipedia public archives).
- Verify every downloaded asset with PIL (resolution, non-corrupt, RGB). **NO fake assets, NO synthetic cartoon slop, NO fabricated news logos.**

### Step 4: WhisperX Word-Level Alignment, Asset Mapping & Gap Detection
- Execute [`audio_sync.py`](scripts/audio_sync.py) using **WhisperX** (`whisperx` primary, `openai-whisper` fallback) to align every spoken word to exact millisecond timestamps.
- Map each verified archival asset to the exact words/sentences where it belongs.
- Identify empty segments where **no archival asset exists** (`gap_segments` via [`director_workflow.py`](scripts/director_workflow.py)).

### Step 5 & Substep 5(1): Interactive Consultation for No-Asset Gaps
- For the empty *"khali"* segments lacking archival photos, ask the operator which visual engine and style to design with:
  1. **Lemo-Opuscar Studio** (`skills/lemo-opuscar/styles/`, 100 film styles)
  2. **p5.brush** (`skills/p5-brush/`, charcoal, watercolor, pencils, cross-hatching, markers, flow fields)
  3. **3D-Animator / Three.js** (`scripts/kit/` 12 shader looks: `lit`, `clay`, `blueprint`, `paper`, `shadow`, `toon`, `synth`, `chrome`, `voxel`, `thermal`, `neon`, `mix`)
- Always share the recommended style list alongside the options. **If the operator asks for more styles, provide additional styles from `skills/documentary-3d/references/film-styles-catalog.md` / `skills/lemo-opuscar/styles/`.**

---

## 🏛️ Restored Main Documentary Engine Protocol (`kaz-documentary` Core)

Read [`references/style-guide.md`](references/style-guide.md) before planning shots, [`references/engine-guide.md`](references/engine-guide.md) before editing `board_engine.py`/`vintage_engine.py`, and [`../code-3d-video/SKILL.md`](../code-3d-video/SKILL.md) when building full `code-3d-video` 3D worlds:

1. **Shot list (one beat per sentence)**: Write `time range | beat recipe | assets | trigger word | camera move` before coding. Beat recipes: `REVEAL_PHOTO`, `DOC_FOCUS`, `YEAR_CARD`, `NAME_TAG`, `CONNECT`, `STAMP`, `HIGHLIGHT_LINE`, `THESIS`, `NETWORK_REVEAL`, `COUNTER`, `TITLE_GLITCH`.
2. **One continuous camera**: Over the world surface (`board_engine.py` `WW×WH` or continuous 3D path). Smooth eased pushes, pulls, pans, slight tilts — no hard cuts except planned world changes (iris wipes for vintage/gap inserts, digital glitch for final title).
3. **Red-only accent (`#d0312d` / BGR `(45, 49, 208)`)**: Reserved strictly for strings/yarn, wobble focus circles, stamps, key labels, and end title.
4. **Build & Contact-Sheet Stills QA**: Edit data blocks in a project copy of `board_engine.py` (keep rendering machinery intact). Render stills (`python board_engine.py stills 2,9,22,...`), inspect a contact sheet, fix layout/BGR color/font glyphs/camera targets before full render.
5. **Parallel Chunked Render & Splice**: Split full render across CPU cores (`python board_engine.py full START END part.mp4`), render approved gap-engine clips (`p5.brush` / `lemo-opuscar` / `3D-animator` / `vintage_engine.py`), and splice cleanly with [`splice.py`](scripts/splice.py) / `splice.sh`.
6. **Openverse Sound Design & Master Audio (`-14 LUFS`)**: Fetch real CC-licensed SFX & music beds via [`openverse_sfx.py`](scripts/openverse_sfx.py), mix frame-accurately with ducking (`kit/mix.py` or `mix_and_mux.py`) to **-14 LUFS / -1.5 dBTP**, and deliver CRF 24 shareable MP4 (`ffmpeg` verified).

---

## 📂 Suite Scripts Reference (`skills/documentary-3d/scripts/`)

| Script | Role |
|---|---|
| `board_engine.py` | **Primary Engine**: Continuous-camera Evidence Board renderer (pinned cards, tags, red strings, circles, stamps, grain, vignette). |
| `code-3d-video` (`../code-3d-video/`) | **Primary 3D Engine**: Restored original 3D video kit (`builders.js`, `character.js`, `looks.js`, `stage.js`, `qa.mjs`, `lint.mjs`, `doctor.mjs`). |
| `asset_fetcher.py` | Step 3: Downloads & PIL-verifies real historical assets from Wikimedia Commons / Wikipedia (zero fake assets). |
| `audio_sync.py` | Step 4: Runs WhisperX (fallback: OpenAI Whisper) word-level alignment & subtitle sync. |
| `director_workflow.py` | Step 4–5(1): Maps verified assets to transcript, detects empty gaps, presents 3 gap engines + style catalogs. |
| `openverse_sfx.py` | **Active Sound Engine**: Queries, downloads & normalizes real CC-licensed SFX & ambient music from Openverse API (`https://api.openverse.org/v1/audio/`). |
| `sound_config.json` | Controls active sound mode (`"openverse"` default vs `"legacy_synth"`). |
| `sound_bed.py` | **Silenced Legacy Fallback (Preserved Intact)**: Original synthesized sound bed. Dormant unless `SOUND_ENGINE=legacy_synth` or `--force-legacy`. |
| `vintage_engine.py` | Legacy silent-film 2D insert engine (optional gap insert). |
| `kit/mix.py` & `mix_and_mux.py` | Sidechain ducking, cue placement, and EBU R128 `-14 LUFS` mastering. |
| `splice.py` / `splice.sh` | Frame-accurate video segment splicing for gap inserts. |
