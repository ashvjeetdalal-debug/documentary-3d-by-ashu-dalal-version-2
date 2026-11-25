---
name: lemo-opuscar
description: Direct and produce short cinematic films, explainers, and motion graphics entirely in code using the 99 curated film styles of the Lemo-Opuscar studio library. Use when the user wants an explainer, documentary, anime, architectural visualization, technical teardown, or animated story in a specific aesthetic style, or when applying code-driven cinematic direction.
---

# Lemo-Opuscar — Code-Driven Film Studio (99 Styles)

> [!NOTE]
> **Version 3 Role Rule**: When producing a documentary under `documentary-3d-by-ashu-dalal-version-3`, follow `rules/AGENTS.md` first: **Main Ashu-Dalal Documentary (`board_engine.py`)** handles all asset-backed narration, while **`lemo-opuscar` is the dedicated engine for no-asset gaps (*khali parts*)** — used at **100% full potential** (`STYLE.md`, `demo/`, `DIRECTOR.md`, `TECHNIQUE.md`, GTAO/DOF `post.js`, VHS/CRT `crt.js`) after deep internet visual research in `plan.md`. Never bridge or mix `lemo-opuscar` into combo pipelines with `3d-animator`.

Direct and produce complete animated films, motion explainers, and visual essays entirely through code. No generative video hallucination or cloud rendering costs—every frame, camera move, subtitle, and audio cue is driven by deterministic code.

The studio library contains **99 curated styles** located in `${PLUGIN_ROOT}/skills/lemo-opuscar/styles/` and core tools in `${PLUGIN_ROOT}/skills/lemo-opuscar/core/`.

---

## 📖 Master Production Manuals

Before generating any film, consult the core production guides inside this folder:

1. **[`DIRECTOR.md`](DIRECTOR.md)**:
   - Creative direction, emotional pacing, storyboards, and treatments (`TREATMENT.md`).
   - The **Music Grid**: Locking cuts and actions to rhythmic tempos (60–120 BPM).
   - Camera blocking: Pushes, pans, framing rules, and preventing visual fatigue.
   - Subtitle timing: Minimum 1.8s hold per line, never flashing.

2. **[`TECHNIQUE.md`](TECHNIQUE.md)**:
   - Frame-by-frame offline rendering pipeline via headless Chrome.
   - Text-to-speech voice generation and word-level timestamp alignment.
   - Background score assembly and procedural Foley sound design.
   - Broadcast audio mixing (-14 LUFS) and FFmpeg packaging.

3. **[`MY-STYLES.md`](MY-STYLES.md)**:
   - Designing and saving custom visual styles from scratch.

---

## 🎨 Featured Styles from the 99 Library

| Category | Representative Styles |
|---|---|
| **Documentary & Archival** | `dark-documentary`, `archive-lighttable`, `briefing-board`, `halftone-dossier`, `vintage-collage`, `visual-investigation` |
| **Technical & Diagrams** | `blueprint`, `circuit-board`, `assembly-line-diagram`, `hardcore-info`, `lidar-survey`, `teardown` |
| **Illustration & Painting** | `watercolor`, `impasto`, `colored-pencil`, `crayon-world`, `ink-wash`, `woodcut`, `engraving` |
| **Motion Graphics & 2D** | `bauhaus-shapes`, `art-deco`, `text-flash-cuts`, `paper-popup`, `comic-history`, `papercut-red` |
| **Retro & Tech** | `ascii-crt`, `neon-tubes`, `pixel-rpg`, `thermal-camera`, `silent-film`, `chalkboard` |

Each style folder in `styles/<style_name>/` contains:
- `STYLE.md`: Design specifications, color palettes, camera motion, typography, and shader rules.
- `style.json`: Metadata, tags, supported aspect ratios.
- `demo/`: Working reference implementation (`index.html`, plus style-specific JS/Python render & audio scripts such as `film.js` / `main.js` and `mix.py`).

---

## 🎬 5-Step Production Workflow

> *Note:* When working inside a documentary workflow, follow `rules/AGENTS.md` (`plan.md`, `board_engine.py`, `openverse_sfx.py` with YouTube + internet SFX clamped at 15%–20% volume); use the standalone steps below when authoring standalone Lemo films.

1. **Intake & Style Selection**: Select a style from `styles/` that matches the topic's mood and audience.
2. **Treatment & Script**: Write a `TREATMENT.md` defining the 3-act emotional arc, beats, voiceover lines, and sound cues.
3. **Storyboard / Shot Table**: Map each sentence to visual actions, camera moves, and prop entrances.
4. **Scene Programming**: Customize the scene logic in the project folder. Ensure all visuals are a pure function of time `renderAt(t)`.
5. **Score & Master**: Align timestamps with `dur.json` and `words.json`, run `mix.py` to duck the score under speech, and render final H.264 video.
