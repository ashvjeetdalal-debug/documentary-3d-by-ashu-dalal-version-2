# Documentary 3D by Ashu Dalal — Master Production Rules & System Hierarchy

When authoring, editing, directing, or rendering films with this studio plugin, follow these **non-negotiable laws**:

---

## ⚠️ Rule 0: Clean 3 Independent Engines Architecture (Zero Combinations)

1. **Main Documentary Engine = Ashu Dalal (`kaz-documentary`: `board_engine.py` + `vintage_engine.py` + `style-guide.md`)**:
   - This is the **PRIMARY** system for documentary productions.
   - Wherever real archival assets exist for spoken narration, render strictly using the Evidence-Board grammar (one continuous camera, shallow 3D cards, beat recipes, red accents `#d0312d`, contact-sheet QA). Never abandon it to improvise arbitrary scenes.
2. **No-Asset Gaps (*Khali Parts*) = `Lemo-Opuscar` (`skills/lemo-opuscar/`) at 100% Full Potential**:
   - Whenever WhisperX + asset mapping shows a gap (*khali part*) with no archival photo, use **Lemo-Opuscar** exclusively (99 curated styles, `STYLE.md`, `demo/`, `DIRECTOR.md` pacing & 60–120 BPM grid, `TECHNIQUE.md`, `core/three/post.js` GTAO/DOF, `core/post/crt.js` VHS/CRT).
   - **MANDATORY DEEP INTERNET VISUAL RESEARCH**: Before writing or rendering any Lemo-Opuscar gap scene, deeply research on the **internet** how to visually animate and design what is being spoken in that gap, document the visual design in `plan.md`, consult the operator (Step 5(1)), and then render at full Lemo-Opuscar potential.
3. **`3D-Animator` (`skills/3d-animator/` + `kit/`): 100% Independent & Flexible Anytime/Anywhere**:
   - `3D-Animator` is completely independent (zero combos). Use it **whenever and wherever the user requests** a 3D animation, explainer, product shot, reel, or custom 3D scene.
   - Whenever `3D-Animator` is used, run it at **100% full potential** (`PLAN.md`, 48x Halton HDR motion blur, thin-lens bokeh DOF, cosine sky soft shadows, 12 `styles.js` looks, optional `.glb`/`.gltf` via `model_fetcher.py`).
4. **No Combinations**: Do NOT combine or bridge `3D-Animator` and `Lemo-Opuscar` into combo pipelines. Keep all 3 engines clean and independent.

---

## 🎯 Canonical 5-Step Director Workflow (Mandatory)

1. **Step 1 — Full Internet & Social Media Research $\to$ Topic & Script $\to$ Initial `plan.md`**:
   - Suggest documentary ideas/topics $\to$ operator chooses.
   - **MANDATORY DEEP RESEARCH BEFORE SCRIPT**: Search the **full internet** (news outlets, official/government archives, historical/academic papers, Wikipedia) **AND social media platforms** (Reddit threads, X/Twitter public discussions, YouTube documentary/comment angles, Instagram/TikTok trends, HackerNews/forums) before drafting the script. Cite verified facts/dates/angles in a brief research summary alongside the tightly paced narrated script.
   - **MANDATORY SCRIPT-AWARE `plan.md`**: Immediately after writing the script, generate **`plan.md`** (`python studio.py --plan --topic=... --script-file=...`) analyzing each spoken line: mark archival vs potential gap (*khali*) sections, deeply research on the **internet** how to visually animate what is spoken in each gap, and map **Lemo-Opuscar** styles from the 99-style library.
2. **Step 2 — Voiceover Audio Intake**: Ask operator for voiceover audio (or generate if requested) before writing visual scenes.
3. **Step 3 — Multi-Source Original Internet & Social Assets (NO FAKE ASSETS)**: As soon as audio arrives, if assets are not provided, fetch real verified historical/event media across **all public internet & social sources** via `asset_fetcher.py` (`wikimedia`, `wikipedia`, `openverse` images, `archive.org`, `loc.gov`, `nasa` + `--from-urls` extracted from AI web/social research). Zero AI slop, zero placeholder boxes, zero fabricated outlet logos. Include bilingual/phonetic alias `tags` in `assets_manifest.json`. (If the user also requests a standalone `3D-Animator` scene with real `.glb`/`.gltf` props, download CC0 models via `model_fetcher.py`.)
4. **Step 4 — WhisperX Forced Alignment, Gap Detection & Updated `plan.md`**: Run WhisperX (`audio_sync.py`, `whisperx` $\to$ `faster-whisper` $\to$ `openai-whisper`) for exact word-level timestamps. Match verified assets to spoken words/sentences using both `filename` AND semantic/phonetic `tags` aliases, isolate empty gap segments (*khali parts*), and update **`plan.md`** with exact `[start - end]` timestamps, deep internet-researched visual designs, and full-potential **Lemo-Opuscar** style recipes.
5. **Step 5 & 5(1) — Deep-Researched Lemo-Opuscar Gap Consultation & Rendering**: Present the researched **`plan.md`** gap proposals (with exact spoken text, deep internet-researched visual design, and **Lemo-Opuscar** style choices from all 99 styles) to the operator for approval before rendering gaps at full Lemo-Opuscar potential. Always offer additional styles whenever requested.

---

## 🔊 Sound System Law: YouTube + Internet Free Documentary SFX (15%–20% Volume Clamp), Legacy Synth Silenced (Not Deleted)

1. **No Bundled SFX — Fetch Real Free SFX from YouTube & Internet (`openverse_sfx.py`)**:
   - Bundled local SFX pack is removed. Fetch all documentary SFX (`sub_drop`, `braam`, `thud`, `stamp`, `riser`, `reverse_cymbal`, `whoosh`, `whoosh_deep`, `paper`, `page_flip`, `typewriter`, `typewriter_ding`, `marker`, `pin`, `shutter`, `projector`, `glitch`, `static_burst`, `clock_tick`, `heartbeat`, `radar_ping`, `ui_click`, `drone_dark`) and music beds on demand from **YouTube (`yt-dlp`)**, **Openverse Audio API**, **Wikimedia Commons Audio**, **Internet Archive Audio**, optional **Freesound API v2**, and **`--from-urls`**, normalized to `48 kHz` WAV with attribution logged in `openverse_attribution.json`.
2. **Mandatory 15%–20% SFX Volume Rule (Never Compromise Main Audio)**:
   - Every SFX cue mixed via `kit/mix.py` (in both `documentary-3d` and `3d-animator`) MUST stay strictly between **15% and 20% linear amplitude** (`-16.48 dB` to `-13.98 dB`, default `17.5%` = `-15.14 dB`). `mix.py` enforces this hard clamp automatically so main voiceover audio is never drowned out. Master output target: **-14 LUFS** (ceiling **-1.5 dBTP**).
3. **Legacy Sound System Preserved & Silenced (`sound_bed.py`)**:
   - **NEVER delete** `sound_bed.py`. Keep its code completely intact inside the plugin.
   - Keep it **silenced/inactive by default** (`sound_config.json` -> `"active_engine": "openverse"`). Only execute legacy synthetic sound if the user explicitly flips `"active_engine": "legacy_synth"` or passes `--force-legacy`.

---

## 🏛️ Core Documentary Technical Laws

- **Continuous Camera**: One continuous camera over the world surface / 3D path; smooth eased moves; hard cuts only for planned gap/vintage iris wipes or end-title glitch.
- **Pure Functions of Time**: `renderAt(t)` / frame indices must be 100% deterministic. Never use `Date.now()` or unseeded `Math.random()`.
- **Marks Synced to Speech**: Circles, underlines, and camera marks land within **1–2 frames (≤40 ms)** of the WhisperX trigger word. Captions/tags hold at least **1.8 s**.
- **The Red Accent Rule**: `#d0312d` / RGB `(208, 49, 45)` strictly reserved for pins, strings/yarn, wobble circles, stamps, underlines, and climax thesis.
- **Visual QA Gate**: Always generate contact sheets (`stills`) and inspect before final master renders.
- **Non-Graphic Conflict**: Never depict gore, blood, or graphic wounds; use silhouettes, smoke, flash frames, and intertitles.
