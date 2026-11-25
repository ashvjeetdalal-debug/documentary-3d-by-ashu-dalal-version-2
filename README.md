# Documentary 3D by Ashu Dalal Version 3

A clean, glitch-free **3-Engine Cinematic Documentary & 3D Studio** built around:

1. **Main Documentary Engine — Ashu Dalal (`board_engine.py`, `vintage_engine.py`)**: 2.5D investigative evidence board (one continuous camera, pinned photos, red yarn/strings, typewriter labels, stamps) + vintage 2D silent-film inserts (boiling lines on twos, iris wipes, intertitle cards).
2. **3D-Animator Engine (`skills/3d-animator/` + `kit/`)**: Code-driven Three.js 3D studio (headless Chrome offline renderer, 12 shader looks, sub-frame motion blur, depth of field, handheld camera shake `handheld.py`, and 9:16 mockup reels `laptop_reel.py`). Used primarily for **no-asset documentary gaps** (*khali parts*), and freely available anytime for custom/standalone 3D scenes.
3. **Lemo-Opuscar Studio (`skills/lemo-opuscar/`)**: 99 film styles (`dark-documentary`, `archive-lighttable`, `briefing-board`, `circuit-board`, `halftone-dossier`, etc.), GTAO + 96-tap Bokeh DOF (`core/three/post.js`), VHS/CRT post-FX (`core/post/crt.js`), `DIRECTOR.md` pacing, and `TECHNIQUE.md` mastering — elevating overall video quality and pairing cleanly with `3D-Animator`.
4. **Automated Intake & Bundled Documentary Audio**:
   - **WhisperX Sync & Gap Planner (`audio_sync.py`, `director_workflow.py`)**: Word-level forced alignment (English, Hindi, Hinglish) and research-driven `plan.md`.
   - **Real Internet Media & CC0 3D Models (`asset_fetcher.py`, `model_fetcher.py`)**: Verified archival images (zero fake assets) and real CC0 `.glb`/`.gltf` 3D models.
   - **Bundled 23-Cue CC0 Documentary SFX + Multi-Source Audio (`assets/sfx/`, `openverse_sfx.py`)**: Instant 48 kHz WAV documentary cues (`sub_drop`, `braam`, `riser`, `whoosh`, `paper`, `typewriter`, `shutter`, `projector`, `glitch`, `drone_dark`, etc.) + Openverse/Wikimedia/Archive/Freesound fetch mixed at `-14 LUFS` (`sound_bed.py` legacy synth preserved intact & silenced by default).

---

## 📂 Clean Directory Structure

```text
documentary-3d-by-ashu-dalal-version-3/
├── plugin.json                 # Studio Edition plugin manifest
├── README.md                   # Master documentation
├── INSTALL.txt                 # Setup & dependencies guide
├── studio.py                   # Master studio CLI
├── assets/
│   ├── logo.svg                # Master plugin badge
│   └── sfx/                    # Bundled 23-cue CC0/CC-BY documentary SFX pack (48 kHz WAV)
├── guides/
│   └── COMBINATIONS.md         # 10 verified glitch-free combinations guide
├── rules/
│   └── AGENTS.md               # Unified production & system hierarchy laws
└── skills/
    ├── documentary-3d/         # Primary Ashu Dalal documentary workflow & combo scripts
    │   ├── SKILL.md
    │   ├── references/         # style-guide.md, engine-guide.md, sound.md, film-styles-catalog.md, etc.
    │   └── scripts/
    │       ├── board_engine.py      # Primary 2.5D Evidence Board renderer
    │       ├── vintage_engine.py    # Primary Vintage 2D silent-film insert engine
    │       ├── director_workflow.py # Step 1B-5(1) plan.md & gap consultation
    │       ├── asset_fetcher.py     # Multi-source archival image fetcher
    │       ├── model_fetcher.py     # CC0/open 3D .glb/.gltf model fetcher
    │       ├── audio_sync.py        # WhisperX / Whisper word alignment
    │       ├── openverse_sfx.py     # Bundled SFX + Multi-source CC audio engine
    │       ├── combo_runner.py      # Glitch-free 10-combo runner
    │       ├── sound_bed.py         # Legacy synth (silenced by default)
    │       ├── sound_config.json    # Active audio mode config
    │       ├── mix_and_mux.py/.sh   # Sidechain ducking & -14 LUFS multiplexer
    │       ├── splice.py/.sh        # Frame-accurate video splicing
    │       └── kit/                 # 3D-Animator + Lemo Combo & Presentation Tools
    ├── 3d-animator/            # Standalone & gap-ready 3D-Animator skill (from 3d-animator.zip)
    │   ├── SKILL.md
    │   ├── 3D-Animator-Skill.pdf
    │   ├── references/
    │   └── kit/
    └── lemo-opuscar/           # Full Lemo-Opuscar Studio (99 film styles, core post-FX, guides)
```

---

## 🛠️ Quick Commands

```bash
# Inspect 3-engine hierarchy, 10 glitch-free combos & 23 bundled documentary SFX:
python studio.py --list-engines
python studio.py --list-combos
python studio.py --list-sfx

# Generate plan.md, fetch real archival assets, 3D models & documentary SFX:
python studio.py --plan --topic="Stuxnet" --script-file=script.txt --out=plan.md
python studio.py --fetch-assets="Stuxnet,Natanz" --out=assets
python studio.py --fetch-models="camera,desk" --out=models --res=1k
python studio.py --fetch-sfx="sub_drop,riser,whoosh,paper,typewriter,shutter,stamp" --out=sound

# Render glitch-free 3D-Animator + Lemo-Opuscar combinations:
python studio.py --combo --shader=paper --lemo=dark-documentary --post=gtao --stills=1.5,3.5 --out=stills_test
python studio.py --combo --shader=blueprint --lemo=briefing-board --post=crt --stills=1.5 --out=stills_crt

# Render Primary Evidence Board & Standalone 3D-Animator:
python studio.py --render-board --script=my_project/board_engine.py --stills=2,5
python studio.py --render-3d --style=blueprint --stills=2.5
```
