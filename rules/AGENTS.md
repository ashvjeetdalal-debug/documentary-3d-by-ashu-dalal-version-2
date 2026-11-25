# Documentary 3D by Ashu Dalal — Master Production Rules & System Hierarchy

When authoring, editing, directing, or rendering films with this studio plugin, follow these **non-negotiable laws**:

---

## ⚠️ Rule 0: System Hierarchy (Main Backbone First, Other Engines Gap-Only)

1. **Never Compromise the Main Documentary System**:
   - The restored **Ashu Dalal Documentary (`kaz-documentary` `board_engine.py` + `style-guide.md`)** and **Original 3D Documentary Kit (`skills/code-3d-video/`)** form the **PRIMARY engine**.
   - Wherever real archival assets exist for spoken narration, render strictly using the main documentary grammar (one continuous camera, shallow 3D cards, beat recipes, red accents, contact-sheet QA). Never abandon it to improvise arbitrary scenes.
   - **Auto-Bootstrap New 3D Folders**: Whenever creating a new `code-3d-video` project folder, the AI agent **MUST automatically** run `python studio.py --init-3d <project_dir>` (or copy `skills/code-3d-video/project-template/` and run `npm run setup` followed by `npm run doctor`) **before** authoring `src/scene.js` or rendering. Never ask the user to run setup manually or write scenes on an unverified folder.
2. **`p5.brush`, `lemo-opuscar`, and `3D-Animator` Are Strictly for No-Asset Gaps**:
   - Do **NOT** use `p5.brush`, `lemo-opuscar`, or `3D-animator` (`kit/`) on segments that already have verified archival assets.
   - Use them **ONLY** when WhisperX + asset mapping shows a spoken word/sentence has **no archival asset** (*khali part*), and **ONLY** after consulting the operator via Step 5(1).

---

## 🎯 Canonical 5-Step Director Workflow (Mandatory)

1. **Step 1 — Full Internet & Social Media Research $\to$ Topic & Script $\to$ Initial `plan.md`**:
   - Suggest documentary ideas/topics $\to$ operator chooses.
   - **MANDATORY DEEP RESEARCH BEFORE SCRIPT**: Search the **full internet** (news outlets, official/government archives, historical/academic papers, Wikipedia) **AND social media platforms** (Reddit threads, X/Twitter public discussions, YouTube documentary/comment angles, Instagram/TikTok trends, HackerNews/forums) before drafting the script. Cite verified facts/dates/angles in a brief research summary alongside the tightly paced narrated script.
   - **MANDATORY SCRIPT-AWARE `plan.md`**: Immediately after writing the script, generate **`plan.md`** (`python studio.py --plan --topic=... --script-file=...`) analyzing each spoken line: mark archival vs potential gap (*khali*) sections, research on the **internet** how to visually animate what is spoken in each gap, decide whether real CC0/open **3D `.glb`/`.gltf` models** should be downloaded (`model_fetcher.py`), and map the best plugin engines & styles.
2. **Step 2 — Voiceover Audio Intake**: Ask operator for voiceover audio (or generate if requested) before writing visual scenes.
3. **Step 3 — Multi-Source Original Internet & Social Assets + Real 3D Models (NO FAKE ASSETS)**: As soon as audio arrives, if assets are not provided, fetch real verified historical/event media across **all public internet & social sources** via `asset_fetcher.py` (`wikimedia`, `wikipedia`, `openverse` images, `archive.org`, `loc.gov`, `nasa` + `--from-urls` extracted from AI web/social research). Zero AI slop, zero placeholder boxes, zero fabricated outlet logos. Include bilingual/phonetic alias `tags` in `assets_manifest.json`. If `plan.md` specifies 3D props/objects for gaps, download real CC0/open `.glb`/`.gltf` models via `model_fetcher.py` (`--fetch-models` via Poly Haven / `--from-urls`).
4. **Step 4 — WhisperX Forced Alignment, Gap Detection & Updated `plan.md`**: Run WhisperX (`audio_sync.py`, `whisperx` $\to$ `faster-whisper` $\to$ `openai-whisper`) for exact word-level timestamps. Match verified assets to spoken words/sentences using both `filename` AND semantic/phonetic `tags` aliases, isolate empty gap segments (*khali parts*), and update **`plan.md`** with exact `[start - end]` timestamps, internet-researched visual designs, 3D model paths, and engine/combo recipes.
5. **Step 5 & 5(1) — Internet-Researched Gap Consultation & Rendering**: Present the researched **`plan.md`** gap proposals (with exact spoken text, internet-researched visual idea, downloaded 3D `.glb` options if helpful, and style/engine choices across **Lemo-Opuscar** 99 styles, **p5.brush**, **3D-Animator**, or `--combo` fusion) to the operator for approval before rendering gaps (`studio.py --combo --model=...`). Always include style choices and offer additional styles whenever requested.

---

## 🔊 Sound System Law: Multi-Source Openverse Default, Legacy Synth Silenced (Not Deleted)

1. **Multi-Source Real CC Audio Active by Default (`openverse_sfx.py`)**:
   - All SFX (`whoosh`, `thud`, `paper`, `click`, `typing`, `boom`, `riser`, etc.) and music beds MUST come from **real CC0/PD/CC-BY audio** via **`openverse_sfx.py`** (combining **Openverse Audio API**, **Wikimedia Commons Audio**, **Internet Archive Audio**, optional **Freesound API v2** when `FREESOUND_API_KEY` is set, and `--from-urls`), normalized to `48 kHz` WAV and mixed via `FFmpeg` (`kit/mix.py` / `mix_and_mux.py`) at **-14 LUFS** (ceiling **-1.5 dBTP**) with attribution logged in `openverse_attribution.json`.
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
