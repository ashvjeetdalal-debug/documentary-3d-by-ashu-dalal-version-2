---
name: lemo-opuscar
description: Direct and produce short cinematic films, explainers, and motion graphics entirely in code using the 99 curated film styles of the Lemo-Opuscar studio library. Use when the user wants an explainer, documentary, anime, architectural visualization, technical teardown, or animated story in a specific aesthetic style, or when applying code-driven cinematic direction.
---

# Lemo-Opuscar — Code-Driven Film Studio (99 Styles)

> [!NOTE]
> **Version 3 Role Rule**: When producing a documentary under `documentary-3d-by-ashu-dalal-version-3`, follow `rules/AGENTS.md` first: **Main Ashu-Dalal Documentary (`board_engine.py` / `code-3d-video`)** handles all asset-backed narration. Use `lemo-opuscar` for **no-asset gap segments** (Step 5 operator choice) or `--combo` bridges (`lemo_bridge.js`, `post.js`, `crt.js`), unless explicitly asked standalone.

Direct and produce complete animated films, motion explainers, and visual essays entirely through code. No generative video hallucination or cloud rendering costs—every frame, camera move, subtitle, and audio cue is driven by deterministic code.

The studio library contains **99 curated styles** located in `${PLUGIN_ROOT}/skills/lemo-opuscar/styles/` and core tools in `${PLUGIN_ROOT}/skills/lemo-opuscar/core/`.

---

## 📖 Master Production Manuals

Before generating any film, consult the core production guides in `guides/`:

1. **[`guides/DIRECTOR.md`](file:///C:/editing%20automation/documentary-3d-by-ashu-dalal/guides/DIRECTOR.md)**:
   - Creative direction, emotional pacing, storyboards, and treatments (`TREATMENT.md`).
   - The **Music Grid**: Locking cuts and actions to rhythmic tempos (60–120 BPM).
   - Camera blocking: Pushes, pans, framing rules, and preventing visual fatigue.
   - Subtitle timing: Minimum 1.8s hold per line, never flashing.

2. **[`guides/TECHNIQUE.md`](file:///C:/editing%20automation/documentary-3d-by-ashu-dalal/guides/TECHNIQUE.md)**:
   - Frame-by-frame offline rendering pipeline via headless Chrome.
   - Text-to-speech voice generation and word-level timestamp alignment.
   - Background score assembly and procedural Foley sound design.
   - Broadcast audio mixing (-14 LUFS) and FFmpeg packaging.

3. **[`guides/MY-STYLES.md`](file:///C:/editing%20automation/documentary-3d-by-ashu-dalal/guides/MY-STYLES.md)**:
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
- `demo/`: Complete working reference code (`index.html`, `main.js` / `film.js`, `mix.py`).

---

## 🎬 5-Step Production Workflow

1. **Intake & Style Selection**: Select a style from `styles/` that matches the topic's mood and audience.
2. **Treatment & Script**: Write a `TREATMENT.md` defining the 3-act emotional arc, beats, voiceover lines, and sound cues.
3. **Storyboard / Shot Table**: Map each sentence to visual actions, camera moves, and prop entrances.
4. **Scene Programming**: Customize the scene logic in the project folder. Ensure all visuals are a pure function of time `renderAt(t)`.
5. **Score & Master**: Align timestamps with `dur.json` and `words.json`, run `mix.py` to duck the score under speech, and render final H.264 video.
