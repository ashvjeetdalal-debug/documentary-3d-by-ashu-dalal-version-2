# Documentary 3D by Ashu Dalal — Master Production Rules & System Hierarchy

When authoring, editing, directing, or rendering films with this studio plugin, follow these **non-negotiable laws**:

---

## ⚠️ Rule 0: System Hierarchy (Main Backbone First, Other Engines Gap-Only)

1. **Never Compromise the Main Documentary System**:
   - The restored **Ashu Dalal Documentary (`kaz-documentary` `board_engine.py` + `style-guide.md`)** and **Original 3D Documentary Kit (`skills/code-3d-video/`)** form the **PRIMARY engine**.
   - Wherever real archival assets exist for spoken narration, render strictly using the main documentary grammar (one continuous camera, shallow 3D cards, beat recipes, red accents, contact-sheet QA). Never abandon it to improvise arbitrary scenes.
2. **`p5.brush`, `lemo-opuscar`, and `3D-Animator` Are Strictly for No-Asset Gaps**:
   - Do **NOT** use `p5.brush`, `lemo-opuscar`, or `3D-animator` (`kit/`) on segments that already have verified archival assets.
   - Use them **ONLY** when WhisperX + asset mapping shows a spoken word/sentence has **no archival asset** (*khali part*), and **ONLY** after consulting the operator via Step 5(1).

---

## 🎯 Canonical 5-Step Director Workflow (Mandatory)

1. **Step 1 — Topic & Script**: Suggest documentary ideas/topics $\to$ operator chooses $\to$ write tight narrated script.
2. **Step 2 — Voiceover Audio Intake**: Ask operator for voiceover audio (or generate if requested) before writing visual scenes.
3. **Step 3 — Real Original Internet Assets First (NO FAKE ASSETS)**: As soon as audio arrives, if assets are not provided, run `asset_fetcher.py` to download real verified historical assets from Wikimedia Commons / Wikipedia. Zero AI slop, zero placeholder boxes, zero fabricated outlet logos.
4. **Step 4 — WhisperX Forced Alignment & Gap Detection**: Run WhisperX (`audio_sync.py`, preferring `whisperx` repo) for exact word-level timestamps. Map verified assets to spoken words/sentences and isolate empty gap segments (*khali parts*).
5. **Step 5 & 5(1) — Interactive Gap Visual Selection**: Present the empty gap timestamps to the operator and ask which visual engine to use from the 3 fallback tools:
   - **Lemo-Opuscar** (100 film styles)
   - **p5.brush** (charcoal, watercolor, pencil, hatching, marker, flow field)
   - **3D-Animator** (12 procedural shader looks)
   Always include a style list, and provide additional styles immediately whenever requested.

---

## 🔊 Sound System Law: Openverse Default, Legacy Synth Silenced (Not Deleted)

1. **Openverse Repo / API Active by Default (`openverse_sfx.py`)**:
   - All SFX (`whoosh`, `thud`, `paper`, `click`, `typing`, `boom`, `riser`) and music beds MUST come from **Openverse (`https://api.openverse.org/v1/audio/`)** CC0/CC-BY real audio recordings, normalized to `48 kHz` and mixed via `kit/mix.py` / `mix_and_mux.py` at **-14 LUFS** (ceiling **-1.5 dBTP**) with attribution metadata logged in `openverse_attribution.json`.
2. **Legacy Sound System Preserved & Silenced (`sound_bed.py`, `gen_sfx.py`)**:
   - **NEVER delete** `sound_bed.py` or `gen_sfx.py`. Keep their code completely intact inside the plugin.
   - Keep them **silenced/inactive by default** (`sound_config.json` -> `"active_engine": "openverse"`). Only execute legacy synthetic sound if the user explicitly flips `"active_engine": "legacy_synth"` or passes `--force-legacy`.

---

## 🏛️ Core Documentary Technical Laws

- **Continuous Camera**: One continuous camera over the world surface / 3D path; smooth eased moves; hard cuts only for planned gap/vintage iris wipes or end-title glitch.
- **Pure Functions of Time**: `renderAt(t)` / frame indices must be 100% deterministic. Never use `Date.now()` or unseeded `Math.random()`.
- **Marks Synced to Speech**: Circles, underlines, and camera marks land within **1–2 frames (≤40 ms)** of the WhisperX trigger word. Captions/tags hold at least **1.8 s**.
- **The Red Accent Rule**: `#d0312d` / RGB `(208, 49, 45)` strictly reserved for pins, strings/yarn, wobble circles, stamps, underlines, and climax thesis.
- **Visual QA Gate**: Always generate contact sheets (`stills` / `npm run qa`) and inspect before final master renders.
- **Modular Combinations (`guides/COMBINATIONS.md`)**: When combining engines (`3D-Animator`, `p5.brush`, `Lemo-Opuscar`, `code-3d-video`, `Evidence Board`), follow the 15 verified recipes in `guides/COMBINATIONS.md` (`studio.py --combo`), keep `preserveReadable = true` on archival documents/photos, and run only one post pass (`hdr` | `gtao` | `crt` | `none`) per shot.
- **Non-Graphic Conflict**: Never depict gore, blood, or graphic wounds; use silhouettes, smoke, flash frames, and intertitles.
