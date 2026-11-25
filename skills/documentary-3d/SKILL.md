---
name: documentary-3d-by-ashu-dalal-version-3
description: Master Documentary & 3D Production Suite by Ashu Dalal. Uses Ashu Dalal's Evidence-Board + Vintage 2D engine as the primary documentary backbone, combines 3D-Animator (primarily for no-asset gaps or flexible standalone 3D scenes) and Lemo-Opuscar (for overall video polish, 99 styles, GTAO/DOF & CRT), uses WhisperX word-level alignment, real internet archival assets (zero fake assets), and a bundled CC0 documentary SFX library + Openverse audio engine (legacy synth silenced).
---

# Documentary 3D by Ashu Dalal Version 3 (Ashu Dalal + 3D-Animator + Lemo-Opuscar)

Build narrated cinematic documentary videos in code using a clean 3-engine studio:
1. **Main Documentary Backbone**: **Ashu Dalal (`kaz-documentary`) Evidence-Board (`board_engine.py`) + Vintage 2D (`vintage_engine.py`)**.
2. **3D Engine (`3d-animator`)**: Combined seamlessly for **no-asset gaps** (*khali parts*) AND flexible standalone 3D scenes whenever requested.
3. **Polish & Styles Engine (`lemo-opuscar`)**: 99 film styles, `DIRECTOR.md` / `TECHNIQUE.md`, GTAO + Bokeh DOF, and VHS/CRT post-FX to elevate the overall video.

---

## ⚠️ STRICT SYSTEM HIERARCHY

1. **MAIN BACKBONE FIRST (`Ashu Dalal` Evidence Board)**:
   - Wherever real verified archival assets exist for spoken words/sentences, render strictly using the main Ashu Dalal Documentary grammar (`board_engine.py` + `references/style-guide.md`).
2. **`3D-Animator` & `Lemo-Opuscar` (Gaps + Overall Polish + Flexible Use)**:
   - In documentary narration, use `3D-Animator` + `Lemo-Opuscar` (or their 10 glitch-free `--combo` combinations) for **no-asset gaps** after Step 5(1) consultation, and use `Lemo-Opuscar` (`crt.js`, `post.js`, palettes, `DIRECTOR.md` pacing) to enhance the overall video quality.
   - When the user explicitly wants `3d-animator` for a custom scene/intro/reel, allow full flexible usage via `skills/3d-animator/SKILL.md` or `studio.py --render-3d` / `--combo`.
3. **SOUND ENGINE DEFAULT (Bundled Documentary SFX + Openverse Active, Legacy Synth Silenced Not Deleted)**:
   - Use the pre-bundled 23-cue CC0 documentary SFX pack (`assets/sfx/`) + **`openverse_sfx.py`** (Openverse + Wikimedia + Archive + Freesound v2) mixed via `kit/mix.py` / `mix_and_mux.py` at `-14 LUFS`.
   - Legacy synthesized sound (`sound_bed.py`) is **silenced by default** (NOT deleted) via `sound_config.json`.

---

## 🎬 Canonical 5-Step Director Workflow

### Step 1: Full Internet + Social Media Research, Topic, Script & Initial `plan.md`
- Present strong documentary topic ideas on historical events, covert operations, technology, or people.
- **Full Research Rule**: Before writing the script on the chosen topic, search across **all internet sources** (news outlets, official/government archives, Wikipedia, academic/research sites) **AND social media platforms** (Reddit, X/Twitter, YouTube discussions, Instagram/TikTok angles, technical forums) to gather verified facts, human angles, and visual leads. Then write a tightly paced documentary script (150 wpm, one visual per sentence, hook in first 3s).
- **Automatic `plan.md` Generation**: Immediately after writing the script, generate **`plan.md`** via [`director_workflow.py`](scripts/director_workflow.py) (`python studio.py --plan --topic=... --script-file=...`). Map out what is spoken in potential gap sections, research the real-world visuals on the **internet**, decide whether downloadable **3D `.glb`/`.gltf` models** ([`model_fetcher.py`](scripts/model_fetcher.py)) are needed, and pick the best `3D-Animator` / `Lemo-Opuscar` styles.

### Step 2: Voiceover Audio Intake
- Ask the operator for the voiceover audio file (`.wav`/`.mp3`), or offer to generate the voiceover. Receive audio before building scenes.

### Step 3: Multi-Source Real Assets & CC0 3D Models (NO FAKE ASSETS)
- If assets are not provided, **immediately upon receiving audio**, fetch real historical photos, maps, diagrams, documents, and authentic social/news media stills using [`asset_fetcher.py`](scripts/asset_fetcher.py) (Wikimedia Commons, Wikipedia, Openverse Images, Internet Archive, NASA Images, plus `--from-urls` for verified URLs found during Step 1 web/social research).
- Verify every downloaded asset with PIL (min 400×300, non-corrupt, clean RGB). **NO fake assets, NO synthetic cartoon slop, NO fabricated news logos.** Pass `--tags` with bilingual/phonetic aliases if voiceover is Hindi/Hinglish.
- For gap or custom 3D scenes requiring real 3D props/machinery/architecture, download CC0/open **`.glb`/`.gltf` 3D models** via [`model_fetcher.py`](scripts/model_fetcher.py) (`studio.py --fetch-models="<query>"` via Poly Haven 3D API or `--from-urls`).

### Step 4: WhisperX Word-Level Alignment, Asset Mapping, Gap Detection & Final `plan.md`
- Execute [`audio_sync.py`](scripts/audio_sync.py) using **WhisperX** (`whisperx` primary, `faster-whisper` & `openai-whisper` fallbacks) to align every spoken word to exact millisecond timestamps.
- Map each verified archival asset to the exact words/sentences where it belongs.
- Identify empty segments where **no archival asset exists** (`gap_segments` via [`director_workflow.py`](scripts/director_workflow.py)), and update **`plan.md`** (`python studio.py --plan --mapping=project_mapping.json`) with exact timestamps, internet-researched visual designs, 3D model paths, and engine/combo plans.

### Step 5 & Substep 5(1): Researched Gap Visual Consultation (`plan.md` Proposal)
- For the empty *"khali"* segments lacking archival photos, research the real subject/metaphor on the internet first, present the **`plan.md` design proposal** alongside **Lemo-Opuscar** (99 styles), **3D-Animator** (12 shaders), or glitch-free **`studio.py --combo`** combinations, and ask the operator to approve or refine the chosen style/design before rendering. Always offer more styles when requested.

---

## 🏛️ Main Documentary Engine Protocol (`Ashu Dalal` Core)

Read [`references/style-guide.md`](references/style-guide.md) before planning shots and [`references/engine-guide.md`](references/engine-guide.md) before editing `board_engine.py`/`vintage_engine.py`:

1. **Shot list (one beat per sentence)**: Write `time range | beat recipe | assets | trigger word | camera move` before coding. Beat recipes: `REVEAL_PHOTO`, `DOC_FOCUS`, `YEAR_CARD`, `NAME_TAG`, `CONNECT`, `STAMP`, `HIGHLIGHT_LINE`, `THESIS`, `NETWORK_REVEAL`, `COUNTER`, `TITLE_GLITCH`.
2. **One continuous camera**: Over the world surface (`board_engine.py` `WW×WH`). Smooth eased pushes, pulls, pans, slight tilts — no hard cuts except planned world changes (iris wipes for vintage/gap inserts, digital glitch for final title).
3. **Red-only accent (`#d0312d` / BGR `(45, 49, 208)`)**: Reserved strictly for strings/yarn, wobble focus circles, stamps, key labels, and end title.
4. **Build & Contact-Sheet Stills QA**: Edit data blocks in a project copy of `board_engine.py` (keep rendering machinery intact). Render stills (`python board_engine.py stills 2,9,22,...`), inspect a contact sheet, fix layout/BGR color/font glyphs/camera targets before full render.
5. **Parallel Chunked Render & Splice**: Split full render across CPU cores (`python board_engine.py full START END part.mp4`), render approved gap/3D/Lemo clips (`3d-animator` / `lemo-opuscar` / `--combo` / `vintage_engine.py`), and splice cleanly with [`splice.py`](scripts/splice.py) / `splice.sh`.
6. **Documentary Sound Design & Master Audio (`-14 LUFS`)**: Use the bundled CC0 documentary SFX pack (`assets/sfx/`) or fetch additional CC-licensed SFX & music beds via [`openverse_sfx.py`](scripts/openverse_sfx.py), write `sound/cues.json`, and run [`kit/mix.py`](scripts/kit/mix.py) for multi-SFX ducked **-14 LUFS / -1.5 dBTP** mastering (or `mix_and_mux.py` for single bed + voiceover). *(Legacy `sound_bed.py` is silenced by default via `sound_config.json`.)*

---

## 📂 Suite Scripts Reference (`skills/documentary-3d/scripts/`)

| Script | Role |
|---|---|
| `board_engine.py` | **Primary Engine**: Continuous-camera Evidence Board renderer (pinned cards, tags, red strings, circles, stamps, grain, vignette). |
| `vintage_engine.py` | **Primary Vintage Insert Engine**: Silent-film 2D insert engine (sepia, boiling lines on twos, iris wipes). |
| `asset_fetcher.py` | Step 3: Multi-source PIL-verified archival images (Wikimedia, Wikipedia, Openverse, Archive, NASA, LOC, `--from-urls`). |
| `model_fetcher.py` | Step 3B: Downloads & validates real CC0/open 3D `.glb`/`.gltf` models (Poly Haven API + direct `--from-urls`). |
| `audio_sync.py` | Step 4: Runs WhisperX (`faster-whisper` / `openai-whisper` fallbacks) word-level alignment & subtitle sync. |
| `director_workflow.py` | Step 1B–5(1): Generates `plan.md`, maps assets to transcript, detects empty gaps, presents researched visual options. |
| `openverse_sfx.py` | **Active Sound Engine**: Resolves pre-bundled 23-cue CC0 documentary SFX (`assets/sfx/`) + multi-source CC/PD SFX & music (Openverse, Wikimedia Audio, Archive Audio, Freesound v2 API, `--from-urls`). |
| `sound_config.json` | Controls active sound mode (`"openverse"` default vs `"legacy_synth"`). |
| `sound_bed.py` | **Silenced Legacy Fallback (Preserved Intact)**: Original synthesized sound bed. Dormant unless `ASHU_SOUND_ENGINE=legacy_synth` or `--force-legacy`. |
| `kit/mix.py` & `mix_and_mux.py` | Sidechain ducking, cue placement, and EBU R128 `-14 LUFS` mastering. |
| `splice.py` / `splice.sh` | Frame-accurate video segment splicing for gap inserts. |
| `combo_runner.py` + `kit/combo_render.mjs` | **Glitch-Free Combiner**: Runs all 10 verified combinations (`Evidence Board` + `3D-Animator` + `Lemo-Opuscar` + Photos + `.glb` + Handheld). Read `../../guides/COMBINATIONS.md`. |
