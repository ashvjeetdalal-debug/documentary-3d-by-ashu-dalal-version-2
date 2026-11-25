---
name: documentary-3d-by-ashu-dalal-version-3
description: Master Documentary & 3D Production Suite by Ashu Dalal. Uses Ashu Dalal's Evidence-Board + Vintage 2D engine as the primary documentary backbone, Lemo-Opuscar at full potential for deep-researched no-asset gaps, and 3D-Animator as a flexible full-potential 3D engine whenever/wherever requested — powered by WhisperX alignment, real internet archival assets, and YouTube + internet documentary SFX strictly clamped at 15%-20% volume.
---

# Documentary 3D by Ashu Dalal Version 3 (3 Clean Independent Engines)

Build narrated cinematic documentary videos and 3D films in code using **3 clean, independent engines** (zero combinations):
1. **Main Documentary Backbone**: **Ashu Dalal (`kaz-documentary`) Evidence-Board (`board_engine.py`) + Vintage 2D (`vintage_engine.py`)**.
2. **Gap Visuals Engine (`lemo-opuscar`)**: 99 film styles, `STYLE.md`, `demo/`, `DIRECTOR.md` / `TECHNIQUE.md`, GTAO + Bokeh DOF, and VHS/CRT post-FX — used at **100% full potential** for **no-asset gaps** (*khali parts*) after deep internet visual research.
3. **Flexible 3D Engine (`3d-animator`)**: Used **whenever and wherever the user wants** (standalone 3D scenes, explainers, product shots, reels) at **100% full potential** (48x Halton HDR motion blur, thin-lens bokeh DOF, cosine sky soft shadows, 12 `styles.js` looks, optional `.glb`/`.gltf`).

---

## ⚠️ STRICT SYSTEM HIERARCHY

1. **MAIN BACKBONE FIRST (`Ashu Dalal` Evidence Board)**:
   - Wherever real verified archival assets exist for spoken words/sentences, render strictly using the main Ashu Dalal Documentary grammar (`board_engine.py` + `references/style-guide.md`).
2. **NO-ASSET GAPS (`Lemo-Opuscar` Full Potential + Deep Internet Research)**:
   - For empty *"khali"* segments lacking archival photos, deeply research on the **internet** how to visually animate what is spoken, document the design in `plan.md`, consult the operator (Step 5(1)), and render strictly with **`lemo-opuscar`** at 100% full potential (`STYLE.md` + `demo/` + `DIRECTOR.md` + `core/` post-FX).
3. **FLEXIBLE 3D ANYTIME/ANYWHERE (`3D-Animator` Full Potential)**:
   - Whenever the user explicitly wants `3d-animator` for any scene, intro, or standalone 3D film/reel, run it independently at **100% full potential** via `skills/3d-animator/SKILL.md` or `studio.py --render-3d`.
4. **SOUND ENGINE DEFAULT (YouTube + Internet SFX Clamped 15%–20%, Legacy Synth Silenced Not Deleted)**:
   - Fetch free documentary SFX on demand from **YouTube (`yt-dlp`)**, **Openverse**, **Wikimedia Audio**, **Internet Archive Audio**, **Freesound v2**, and **`--from-urls`** via `openverse_sfx.py`.
   - `kit/mix.py` strictly clamps EVERY SFX cue between **15% and 20% volume** (`-16.48 dB` to `-13.98 dB`, default `17.5%` = `-15.14 dB`) so main voiceover audio is never compromised, and masters to `-14 LUFS / -1.5 dBTP`.
   - Legacy synthesized sound (`sound_bed.py`) is **silenced by default** (NOT deleted) via `sound_config.json`.

---

## 🎬 Canonical 5-Step Director Workflow

### Step 1: Full Internet + Social Media Research, Topic, Script & Initial `plan.md`
- Present strong documentary topic ideas on historical events, covert operations, technology, or people.
- **Full Research Rule**: Before writing the script on the chosen topic, search across **all internet sources** (news outlets, official/government archives, Wikipedia, academic/research sites) **AND social media platforms** (Reddit, X/Twitter, YouTube discussions, Instagram/TikTok angles, technical forums) to gather verified facts, human angles, and visual leads. Then write a tightly paced documentary script (150 wpm, one visual per sentence, hook in first 3s).
- **Automatic `plan.md` Generation**: Immediately after writing the script, generate **`plan.md`** via [`director_workflow.py`](scripts/director_workflow.py) (`python studio.py --plan --topic=... --script-file=...`). Map out what is spoken in potential gap sections, deeply research the real-world visuals on the **internet**, and pick the best **Lemo-Opuscar** styles from the 99-style library.

### Step 2: Voiceover Audio Intake
- Ask the operator for the voiceover audio file (`.wav`/`.mp3`), or offer to generate the voiceover. Receive audio before building scenes.

### Step 3: Multi-Source Real Assets (NO FAKE ASSETS)
- If assets are not provided, **immediately upon receiving audio**, fetch real historical photos, maps, diagrams, documents, and authentic social/news media stills using [`asset_fetcher.py`](scripts/asset_fetcher.py) (Wikimedia Commons, Wikipedia, Openverse Images, Internet Archive, NASA Images, plus `--from-urls` for verified URLs found during Step 1 web/social research).
- Verify every downloaded asset with PIL (min 400×300, non-corrupt, clean RGB). **NO fake assets, NO synthetic cartoon slop, NO fabricated news logos.** Pass `--tags` with bilingual/phonetic aliases if voiceover is Hindi/Hinglish.
- *(If the user separately requests a `3D-Animator` scene needing real `.glb`/`.gltf` props, download CC0/open 3D models via [`model_fetcher.py`](scripts/model_fetcher.py) / `studio.py --fetch-models="<query>"`.)*

### Step 4: WhisperX Word-Level Alignment, Asset Mapping, Gap Detection & Final `plan.md`
- Execute [`audio_sync.py`](scripts/audio_sync.py) using **WhisperX** (`whisperx` primary, `faster-whisper` & `openai-whisper` fallbacks) to align every spoken word to exact millisecond timestamps.
- Map each verified archival asset to the exact words/sentences where it belongs.
- Identify empty segments where **no archival asset exists** (`gap_segments` via [`director_workflow.py`](scripts/director_workflow.py)), and update **`plan.md`** (`python studio.py --plan --mapping=project_mapping.json`) with exact timestamps, deep internet-researched visual designs, and full-potential **Lemo-Opuscar** style plans.

### Step 5 & Substep 5(1): Deep-Researched Lemo-Opuscar Gap Consultation (`plan.md` Proposal)
- For the empty *"khali"* segments lacking archival photos, present the deep internet-researched **`plan.md` visual design proposal** alongside matching **Lemo-Opuscar** styles (from all 99 styles), and ask the operator to approve or refine the chosen style/design before rendering at full Lemo-Opuscar potential. Always offer more styles when requested (`python studio.py --list-gap-styles`).

---

## 🏛️ Main Documentary Engine Protocol (`Ashu Dalal` Core)

Read [`references/style-guide.md`](references/style-guide.md) before planning shots and [`references/engine-guide.md`](references/engine-guide.md) before editing `board_engine.py`/`vintage_engine.py`:

1. **Shot list (one beat per sentence)**: Write `time range | beat recipe | assets | trigger word | camera move` before coding. Beat recipes: `REVEAL_PHOTO`, `DOC_FOCUS`, `YEAR_CARD`, `NAME_TAG`, `CONNECT`, `STAMP`, `HIGHLIGHT_LINE`, `THESIS`, `NETWORK_REVEAL`, `COUNTER`, `TITLE_GLITCH`.
2. **One continuous camera**: Over the world surface (`board_engine.py` `WW×WH`). Smooth eased pushes, pulls, pans, slight tilts — no hard cuts except planned world changes (iris wipes for vintage/gap inserts, digital glitch for final title).
3. **Red-only accent (`#d0312d` / BGR `(45, 49, 208)`)**: Reserved strictly for strings/yarn, wobble focus circles, stamps, key labels, and end title.
4. **Build & Contact-Sheet Stills QA**: Edit data blocks in a project copy of `board_engine.py` (keep rendering machinery intact). Render stills (`python board_engine.py stills 2,9,22,...`), inspect a contact sheet, fix layout/BGR color/font glyphs/camera targets before full render.
5. **Parallel Chunked Render & Splice**: Split full render across CPU cores (`python board_engine.py full START END part.mp4`), render approved Lemo-Opuscar gap clips (or any user-requested `3D-Animator` / `vintage_engine.py` clips), and splice cleanly with [`splice.py`](scripts/splice.py) / `splice.sh`.
6. **Documentary Sound Design & Master Audio (`-14 LUFS`, SFX 15%–20%)**: Fetch free documentary SFX & music beds from YouTube (`yt-dlp`) and internet sources via [`openverse_sfx.py`](scripts/openverse_sfx.py), write `sound/cues.json`, and run [`kit/mix.py`](scripts/kit/mix.py) for **15%–20% clamped SFX** + sidechain ducked **-14 LUFS / -1.5 dBTP** mastering (or `mix_and_mux.py` for single bed + voiceover). *(Legacy `sound_bed.py` is silenced by default via `sound_config.json`.)*

---

## 📂 Suite Scripts Reference (`skills/documentary-3d/scripts/`)

| Script | Role |
|---|---|
| `board_engine.py` | **Primary Engine**: Continuous-camera Evidence Board renderer (pinned cards, tags, red strings, circles, stamps, grain, vignette). |
| `vintage_engine.py` | **Primary Vintage Insert Engine**: Silent-film 2D insert engine (sepia, boiling lines on twos, iris wipes). |
| `director_workflow.py` | Step 1B–5(1): Generates `plan.md`, maps assets to transcript, detects empty gaps, presents deep-researched Lemo-Opuscar gap options. |
| `asset_fetcher.py` | Step 3: Multi-source PIL-verified archival images (Wikimedia, Wikipedia, Openverse, Archive, NASA, LOC, `--from-urls`). |
| `model_fetcher.py` | Optional 3D-Animator helper: Downloads & validates real CC0/open 3D `.glb`/`.gltf` models (Poly Haven API + `--from-urls`). |
| `audio_sync.py` | Step 4: Runs WhisperX (`faster-whisper` / `openai-whisper` fallbacks) word-level alignment & subtitle sync. |
| `openverse_sfx.py` | **Active Sound Engine**: Fetches free documentary SFX & music from YouTube (`yt-dlp`), Openverse, Wikimedia Audio, Archive Audio, Freesound v2 API, and `--from-urls`. |
| `sound_config.json` | Controls active sound mode (`"openverse"` default vs `"legacy_synth"`). |
| `sound_bed.py` | **Silenced Legacy Fallback (Preserved Intact)**: Original synthesized sound bed. Dormant unless `ASHU_SOUND_ENGINE=legacy_synth` or `--force-legacy`. |
| `kit/mix.py` & `mix_and_mux.py` | Enforces **15%–20% SFX volume clamp**, sidechain ducking, cue placement, and EBU R128 `-14 LUFS` mastering. |
| `splice.py` / `splice.sh` | Frame-accurate video segment splicing for gap inserts. |
| `kit/present/` | Presentation & post-production helpers (`handheld.py`, `phone_motion.py`, `laptop_reel.py`). |
