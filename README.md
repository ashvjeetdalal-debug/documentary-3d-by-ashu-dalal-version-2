# Documentary 3D by Ashu Dalal Version 3

A clean **3-Independent-Engine Cinematic Documentary & 3D Studio** (zero combinations) built around:

1. **Main Documentary Engine — Ashu Dalal (`board_engine.py`, `vintage_engine.py`)**: 2.5D investigative evidence board (one continuous camera, pinned photos, red yarn/strings, typewriter labels, stamps) + vintage 2D silent-film inserts (boiling lines on twos, iris wipes, intertitle cards).
2. **Gap Visuals Engine — Lemo-Opuscar (`skills/lemo-opuscar/`)**: 99 film styles (`dark-documentary`, `archive-lighttable`, `briefing-board`, `circuit-board`, `halftone-dossier`, etc.), GTAO + 96-tap Bokeh DOF (`core/three/post.js`), VHS/CRT post-FX (`core/post/crt.js`), `DIRECTOR.md` pacing, and `TECHNIQUE.md` mastering — used at **100% full potential** for **no-asset documentary gaps** (*khali parts*) after deep internet visual research.
3. **Flexible 3D Engine — 3D-Animator (`skills/3d-animator/` + `kit/`)**: Code-driven Three.js 3D studio (headless Chrome offline renderer, 48x Halton HDR motion blur, thin-lens bokeh DOF, cosine sky soft shadows, 12 shader looks, handheld camera shake `handheld.py`, and 9:16 mockup reels `laptop_reel.py`). Completely independent — use **whenever and wherever you want** at **100% full potential**.
4. **Automated Intake & YouTube/Internet Documentary Audio (15%–20% SFX Volume Clamp)**:
   - **WhisperX Sync & Deep-Researched Gap Planner (`audio_sync.py`, `director_workflow.py`)**: Word-level forced alignment (English, Hindi, Hinglish) and internet-researched `plan.md`.
   - **Real Internet Media & Optional CC0 3D Models (`asset_fetcher.py`, `model_fetcher.py`)**: Verified archival images (zero fake assets) and optional CC0 `.glb`/`.gltf` 3D models.
   - **YouTube + Multi-Source Internet SFX (`openverse_sfx.py`)**: Free documentary SFX & music fetched on demand from YouTube (`yt-dlp`), Openverse, Wikimedia Audio, Internet Archive Audio, Freesound v2, and `--from-urls`. Every SFX cue is strictly clamped between **15% and 20% volume** (`-16.48 dB` to `-13.98 dB`) in `kit/mix.py` so main voiceover audio is never compromised (`sound_bed.py` legacy synth preserved intact & silenced by default).

---

## 📂 Clean Directory Structure

```text
documentary-3d-by-ashu-dalal-version-3/
├── plugin.json                 # Studio Edition plugin manifest
├── README.md                   # Master documentation
├── INSTALL.txt                 # Setup & dependencies guide
├── studio.py                   # Master studio CLI
├── assets/
│   └── logo.svg                # Master plugin badge
├── rules/
│   └── AGENTS.md               # Unified production & system hierarchy laws
└── skills/
    ├── documentary-3d/         # Primary Ashu Dalal documentary workflow & tools
    │   ├── SKILL.md
    │   ├── references/         # style-guide.md, engine-guide.md, sound.md, film-styles-catalog.md, etc.
    │   └── scripts/
    │       ├── board_engine.py      # Primary 2.5D Evidence Board renderer
    │       ├── vintage_engine.py    # Primary Vintage 2D silent-film insert engine
    │       ├── director_workflow.py # Step 1B-5(1) plan.md & Lemo-Opuscar gap consultation
    │       ├── asset_fetcher.py     # Multi-source archival image fetcher
    │       ├── model_fetcher.py     # CC0/open 3D .glb/.gltf model fetcher
    │       ├── audio_sync.py        # WhisperX / Whisper word alignment
    │       ├── openverse_sfx.py     # YouTube + Multi-source CC SFX & music engine
    │       ├── sound_bed.py         # Legacy synth (silenced by default)
    │       ├── sound_config.json    # Active audio mode config
    │       ├── mix_and_mux.py/.sh   # Sidechain ducking & -14 LUFS multiplexer
    │       ├── splice.py/.sh        # Frame-accurate video splicing
    │       └── kit/                 # mix.py (15%-20% SFX clamp) & present/ reel tools
    ├── 3d-animator/            # Independent, flexible full-potential 3D-Animator engine
    │   ├── SKILL.md
    │   ├── 3D-Animator-Skill.pdf
    │   ├── references/
    │   └── kit/
    └── lemo-opuscar/           # Full Lemo-Opuscar Studio (99 film styles, core post-FX, guides)
```

---

## 🛠️ Quick Commands

```bash
# Inspect 3-engine hierarchy & 99 Lemo-Opuscar gap styles:
python studio.py --list-engines
python studio.py --list-gap-styles

# Generate plan.md, fetch real archival assets, YouTube/internet SFX & optional 3D models:
python studio.py --plan --topic="Stuxnet" --script-file=script.txt --out=plan.md
python studio.py --fetch-assets="Stuxnet,Natanz" --out=assets
python studio.py --fetch-sfx="whoosh,sub_drop,typewriter,shutter,riser" --sources=youtube,openverse --out=sound
python studio.py --fetch-models="camera,desk" --out=models --res=1k

# Render Primary Evidence Board & Independent Full-Potential 3D-Animator:
python studio.py --render-board --script=my_project/board_engine.py --stills=2,5
python studio.py --render-3d --style=blueprint --stills=2.5
```
