# Documentary 3D by Ashu Dalal Version 3 — Modular Combinations Guide

Is guide me woh **15 verified, trouble-free combinations** documented hain jo plugin ke engines (`Evidence Board`, `code-3d-video`, `3D-Animator`, `p5.brush`, `Lemo-Opuscar`, `handheld.py`, `WhisperX`, `Openverse`) ko aapas me bina kisi glitch ke combine karte hain.

> [!IMPORTANT]
> **Rule Balance:**
> - **Standalone Mode Safe**: Har engine akela bhi pehle jaise bina kisi disturbance ke chalta hai.
> - **Main Documentary Backbone First**: Real archival assets wale segments par **Main Ashu-Dalal Documentary (`board_engine.py` / `code-3d-video`)** primary rehta hai; gap-only fallbacks (`Step 5`) ya optional combo upgrades operator ki choice se chalte hain.

---

## 🛠️ Stability Guardrails (Koi Combo Kyun Nahi Tootega)

1. **Unified Asset Server (`combo_render.mjs`)**: Local server `/` par `kit/`, `/plugin/` par `PLUGIN_ROOT` (`/skills/p5-brush/`, `/skills/lemo-opuscar/`), `/three/` par `three`, aur `/assets/` par project folder mount karta hai — **zero 404 errors**.
2. **Single Post-FX Pass (`--post=hdr|gtao|crt|none`)**: Ek render me sirf ek clean finish pass chalti hai. Double bloom ya dual WebGL contexts ek hi canvas par stack nahi hote.
3. **Readability Lock (`preserveReadable`)**: Archival photo cards, documents aur painted maps par `o.userData.preserveReadable = true` set hota hai taaki `voxel`, `thermal`, ya heavy shaders text ko unreadable na banayein.
4. **Smart Sub-frame Budget (`--n`)**: Draft inspections ke liye `--n=4..8`, final HDR motion-blur renders ke liye `--n=16..48` (`gtao` aur `crt` modes single high-res pass me fast chalte hain).

---

## 🔥 All 15 Verified Combinations (Kab, Kya, aur Kaise Use Karein)

### Group A — Primary Evidence Board Combinations

| # | Combination | Kab Use Karein | Kaise Use Karein (CLI / Script) | Kya Avoid Karein |
|---|---|---|---|---|
| **1** | **Evidence Board + `p5.brush` Overlay** (`board-brush-overlay`) | Jab real archival maps/photos par hand-drawn charcoal wobble circles, watercolor map tints ya highlighter sweeps chahiye. | Render `board_engine.py`, render `p5.brush` pass, phir `combo_runner.py` ki `overlay_brush_on_video(base, brush, out, 'screen')` chalayein. | Real archival text ke upar heavy opaque charcoal blobs na daalein. |
| **2** | **Evidence Board + Handheld Physics** (`board-handheld`) | Jab rigid digital pan ki jagah subtle real smartphone human camera wander & shake chahiye. | Extract `motion.csv` via `phone_motion.py`, phir `ffmpeg ... \| python present/handheld.py motion.csv W H cx cy \| ffmpeg ...` (ya `--handheld-csv=motion.csv`). | Scale `1.10` se kam mat rakhein warna edges black strip dikhayenge. |
| **3** | **Evidence Board + Lemo VHS/CRT** (`board-crt`) | 1980s–2000s cybercrime, leaked tapes, ya intelligence TV broadcast look ke liye. | `Lemo core/post/crt.js` pass ko rendered frame canvas par chalayein (`scan: 0.16, grille: 0.08`). | High tracking noise (`track > 0.3`) chote captions ko blur kar sakta hai. |
| **4** | **Evidence Board + 3D-Animator / Laptop Reel** (`board-3d-reel`) | Archival photos ko 3D table par soft shadows/DOF me dikhana ho ya 9:16 social reel screen framing banani ho. | `python studio.py --combo --shader=lit --photo=/assets/doc.jpg --post=gtao` ya `present/laptop_reel.py`. | Photo cards par `voxel`/`thermal` shader force na karein (`preserveReadable=true` on rakhein). |

---

### Group B — 3D Worlds (`3D-Animator` + `code-3d-video` + `p5.brush` + `Lemo`)

> *Note (`code-3d-video` Auto-Setup)*: Naya project folder banate hi AI automatically `python studio.py --init-3d <project_dir>` (ya `npm run setup` + `npm run doctor`) pehle chalaye before editing `src/scene.js`.

| # | Combination | Kab Use Karein | Kaise Use Karein (CLI / Script) | Kya Avoid Karein |
|---|---|---|---|---|
| **5** | **`code-3d-video` + `3D-Animator` Shaders** (`3d-code-shaders`) | Walking 3D characters (`character.js`) aur rooms ko `clay`, `paper`, `blueprint`, `toon`, `voxel`, ya `synth` look + HDR motion blur dene ke liye. | Project `scene.js` me `./kit/combo.js` ki `attachStyleToStage(stage, 'paper')` call karein (`render.mjs` auto `/plugin/` mount karta hai). | Text props (`documentMesh`) par `preserveReadable = true` zaroor set karein. |
| **6** | **`3D-Animator` + `p5.brush` Surface Art** (`3d-brush-surface`) | Jab 3D props/walls par digital color ke bajay animated watercolor, charcoal ya pencil cross-hatching chahiye. | `python studio.py --combo --shader=paper --brush=watercolor --stills=1.5,3.5` (presets: `watercolor`, `charcoal`, `hatching`, `marker`, `flow_field`, `pencil_hb`). | Brush textures ko bahut dark shader (`shadow`) ke andar chhupa mat dein. |
| **7** | **`3D-Animator` + Lemo `post.js` (GTAO + Bokeh)** (`3d-gtao-dof`) | Jab corners me soft contact shadows aur camera rack-focus bokeh blur chahiye (no flat CGI). | `python studio.py --combo --shader=lit --post=gtao --stills=1.5,3.5` | `gtao` ke saath duplicate `UnrealBloomPass` loop na lagayein (`lemo_bridge.js` auto-prevents this). |
| **8** | **`3D-Animator` + Lemo 99 Style Palettes** (`3d-lemo-palette`) | Lemo library ke `dark-documentary`, `archive-lighttable`, `blueprint`, `comic-history` jaise curated palettes 3D stage me lagane ke liye. | `python studio.py --combo --shader=lit --lemo=dark-documentary --stills=2.0` | `comic-history` (light bg) par white ink brush mat use karein (`combo_film.js` auto palette handle karta hai). |
| **9** | **`code-3d-video` + Lemo `post.js` / `crt.js`** (`code3d-post-crt`) | Original `code-3d-video` characters/streets par GTAO depth-of-field ya retro VHS scanline finish lagane ke liye. | Project `scene.js` me `./kit/combo.js` ki `loadLemoBridge()` -> `createPostController('gtao' \| 'crt', ...)` connect karein. | Point lights > 8 mat rakhein warna GTAO render slow ho jayega. |
| **10** | **Mid-Shot Live Look Morph + WhisperX** (`3d-whisperx-morph`) | Bina cut kiye ek hi shot ke beech spoken trigger word (e.g. "hack", "heat") par scene `lit` $\to$ `blueprint`/`thermal` morph karne ke liye. | `python studio.py --combo --shader=0:lit,2.2:blueprint,4.2:thermal --video --out=out/morph.mp4` | Har 0.5s me style flip mat karein (eye fatigue hota hai); beat par change karein. |
| **11** | **3D `mix` Mode + Archival Photo + `p5.brush`** (`3d-mix-archival`) | Ek hi frame me room `lit`, real archival photo card 100% readable, aur 3D machine/prop `blueprint` + wall `p5.brush` rakhne ke liye. | `python studio.py --combo --shader=mix --brush=hatching --photo=/assets/target.jpg --stills=2.5` | Hero object ko explicitly `mesh.name` dekar `MIX_DEFAULT` / map target clear rakhein. |

---

### Group C — Vintage 2D, Brush & Lemo Finishes

| # | Combination | Kab Use Karein | Kaise Use Karein (CLI / Script) | Kya Avoid Karein |
|---|---|---|---|---|
| **12** | **Vintage Silent-Film + `p5.brush`** (`vintage-brush`) | Historical flashback inserts me flat polygons ki jagah 12 fps hand-drawn charcoal boiling animation ke liye. | `brush.seed(1337 + Math.floor(t * 12))` ("on twos" jitter) + sepia grade + iris wipe splice (`splice.py`). | Flashback pe 30 fps jitter mat daalein — authentic silent-film look ke liye 12 fps (`twos`) best hai. |
| **13** | **`p5.brush` + Lemo `crt.js`** (`brush-crt`) | Cyber/retro explainer sketches jahan ink/watercolor drawings CRT monitor par chalti dikhani hon. | `python studio.py --combo --shader=lit --brush=flow_field --lemo=ascii-crt --post=crt --stills=2.0` | Heavy scanlines (`scan > 0.35`) thin pencil strokes ko kaat sakti hain (`0.15` sweet spot hai). |
| **14** | **Any Lemo Style + WhisperX + Openverse + Handheld** (`lemo-whisperx-openverse`) | Lemo library ki kisi bhi 99 styles ko exact word-synced captions, real CC SFX (`-14 LUFS`), aur subtle human shake dene ke liye. | `audio_sync.py` + `openverse_sfx.py` + `kit/mix.py` + optional `handheld.py`. | Legacy synthetic `sound_bed.py` off rakhein (Openverse default). |

---

### Group D — Master 4-in-1 Hybrid Fusion

| # | Combination | Kab Use Karein | Kaise Use Karein (CLI / Script) | Kya Avoid Karein |
|---|---|---|---|---|
| **15** | **Master 4-in-1 Hybrid** (`3D-Animator` + `p5.brush` + `Lemo` + `Handheld` + `WhisperX` + `Openverse`) | Flagship explainer / missing-asset climax gap jahan studio 3D depth, hand-painted organic art, cinema color grade aur real SFX ek saath chahiye. | `python studio.py --combo --shader=paper --brush=watercolor --lemo=dark-documentary --post=gtao --width=1080 --height=1920 --video --out=out/hybrid_9x16.mp4 --handheld-csv=motion.csv` | Ek shot me ek clear dominant look rakhein (e.g. `paper + watercolor` ya `blueprint + hatching`) — saare filters ek saath force na karein. |

---

## 💻 Quick CLI Cheat Sheet (`studio.py`)

```bash
# Sabhi 15 combinations aur unke IDs terminal me dekhne ke liye:
python studio.py --list-combos

# Combo test stills (fast check --n=4):
python studio.py --combo --shader=paper --brush=watercolor --lemo=dark-documentary --post=gtao --stills=1.5,3.5

# Downloaded real CC0 3D Model (.glb/.gltf) + Shader + Lemo + Brush combo:
python studio.py --fetch-models="camera,desk" --out=models --max=2
python studio.py --combo --shader=blueprint --model=models/Camera_01/Camera_01_1k.gltf --brush=flow_field --post=gtao --stills=2.0

# Script-aware research & gap plan.md generation:
python studio.py --plan --topic="Stuxnet" --script-file=script.txt --out=plan.md

# Live mid-shot WhisperX-synced look morphing (9:16 vertical):
python studio.py --combo --shader=0:lit,2.5:blueprint,4.5:synth --brush=hatching --width=1080 --height=1920 --video --out=out/morph_reel.mp4

# VHS/CRT archival hybrid look:
python studio.py --combo --shader=lit --brush=charcoal --lemo=briefing-board --post=crt --stills=2.0
```
