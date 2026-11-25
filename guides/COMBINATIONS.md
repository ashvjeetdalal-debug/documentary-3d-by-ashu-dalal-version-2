# Documentary 3D by Ashu Dalal Version 3 — Glitch-Free Modular Combinations Guide

Is guide me woh **10 verified, glitch-free combinations** documented hain jo plugin ke teen core engines (**Ashu Dalal Evidence Board**, **3D-Animator**, aur **Lemo-Opuscar** + `handheld.py`, `WhisperX`, aur Bundled CC0 Documentary SFX) ko aapas me bina kisi visual glitch ya error ke combine karte hain.

> [!IMPORTANT]
> **Rule Balance:**
> - **Main System (`Ashu Dalal` Evidence Board + Vintage 2D):** Real archival assets wale documentary segments par primary backbone rehta hai.
> - **3D-Animator (Gaps + Flexible Mode):** Missing-asset *khali* gaps me use hota hai, aur jab operator chahe tab standalone ya custom scenes me bhi freely use ho sakta hai.
> - **Lemo-Opuscar (Overall Video Upgrade):** 99 film styles, color palettes, GTAO + Bokeh DOF (`post.js`), VHS/CRT (`crt.js`), aur directorial pacing (`DIRECTOR.md`) poori video ko cinematic banane ke liye use hota hai.

---

## 🛠️ Stability Guardrails (Zero-Glitch Guarantees)

1. **Unified Asset Server (`combo_render.mjs`)**: Local server `/` par `kit/`, `/plugin/` par `PLUGIN_ROOT` (`/skills/lemo-opuscar/`, `/assets/`), `/three/` par `three`, aur `/assets/` + `/models/` par project folder mount karta hai — **zero 404 / CORS errors**.
2. **Single Post-FX Pass (`--post=hdr|gtao|crt|none`)**: Ek render me sirf ek clean finish pass chalti hai. Double bloom ya dual WebGL contexts ek hi canvas par kabhi collide nahi hote (`crt` aur `hdr` offscreen canvas par render hokar `stageCanvas` par blit hote hain).
3. **Readability Lock (`preserveReadable`)**: Archival photo cards aur documents par `o.userData.preserveReadable = true` set hota hai taaki `voxel`, `thermal`, ya heavy shaders text ko unreadable na banayein.
4. **Clean Stills vs Video Output Handling**: `--stills` mode me output hamesha directory me `.png` stills likhta hai (kabhi `.mp4` path ko directory nahi banata), aur `--n=4..8` fast preview / `--n=16..48` final HDR motion blur ke liye tuned hai.
5. **Tone-Mapping Safety**: `gtao` mode (`Lemo core/three/post.js`) apna `OutputPass` tone-mapping khud handle karta hai, isliye `combo_film.js` automatically `THREE.NoToneMapping` set karke double-gamma washout rokta hai.

---

## 🔥 All 10 Verified Glitch-Free Combinations

### Group A — Primary Evidence Board Combinations

| # | Combination | Kab Use Karein | Kaise Use Karein (CLI / Script) | Kya Avoid Karein |
|---|---|---|---|---|
| **1** | **Evidence Board + Handheld Physics** (`board-handheld`) | Jab rigid digital pan ki jagah real smartphone human camera wander & shake chahiye. | Extract `motion.csv` via `phone_motion.py`, phir `combo_runner.py` ki `apply_handheld_filter()` ya `--handheld-csv=motion.csv` use karein. | Scale `1.10` se kam mat rakhein warna edges black strip dikhayenge. |
| **2** | **Evidence Board + Lemo VHS/CRT** (`board-crt`) | 1980s–2000s cybercrime, leaked tapes, ya intelligence TV broadcast look ke liye. | `Lemo core/post/crt.js` pass ko rendered frame canvas par chalayein (`scan: 0.16, grille: 0.08`). | High tracking noise (`track > 0.3`) chote captions ko blur kar sakta hai. |
| **3** | **Evidence Board + 3D-Animator / Laptop Reel** (`board-3d-reel`) | Archival photos ko 3D table par soft shadows/DOF me dikhana ho ya 9:16 social reel screen framing banani ho. | `python studio.py --combo --shader=lit --photo=assets/doc.jpg --post=gtao --stills=1.5` ya `present/laptop_reel.py`. | Photo cards par `voxel`/`thermal` shader force na karein (`preserveReadable=true` on rakhein). |

---

### Group B — `3D-Animator` + `Lemo-Opuscar`

| # | Combination | Kab Use Karein | Kaise Use Karein (CLI / Script) | Kya Avoid Karein |
|---|---|---|---|---|
| **4** | **`3D-Animator` + Lemo `post.js` (GTAO + Bokeh)** (`3d-gtao-dof`) | Jab corners me soft contact shadows aur camera rack-focus bokeh blur chahiye (no flat CGI). | `python studio.py --combo --shader=lit --post=gtao --stills=1.5,3.5` | `gtao` ke saath duplicate `UnrealBloomPass` loop na lagayein (`lemo_bridge.js` auto-prevents this). |
| **5** | **`3D-Animator` + Lemo 99 Style Palettes** (`3d-lemo-palette`) | Lemo library ke `dark-documentary`, `archive-lighttable`, `blueprint`, `briefing-board`, `comic-history` jaise curated palettes 3D stage me lagane ke liye. | `python studio.py --combo --shader=paper --lemo=dark-documentary --post=gtao --stills=2.0` | Light Lemo styles (`briefing-board`) par `--shader=neon` mat force karein. |
| **6** | **Mid-Shot Live Look Morph + Lemo + WhisperX** (`3d-whisperx-morph`) | Bina cut kiye ek hi shot ke beech spoken trigger word (e.g. "hack", "heat") par scene `lit` $\to$ `blueprint`/`thermal` morph karne ke liye. | `python studio.py --combo --shader=0:lit,2.2:blueprint,4.2:thermal --lemo=dark-documentary --video --out=out/morph.mp4` | Har 0.5s me style flip mat karein (eye fatigue hota hai); beat par change karein. |
| **7** | **3D `mix` Mode + Archival Photo + `.glb` Model + Lemo** (`3d-mix-archival`) | Ek hi frame me room `lit`, real archival photo card 100% readable, aur `.glb` hero prop `blueprint`/`clay` + Lemo palette rakhne ke liye. | `python studio.py --combo --shader=mix --model=models/prop.gltf --photo=assets/target.jpg --lemo=archive-lighttable --post=gtao --stills=2.5` | Hero object ko explicitly `mesh.name` dekar `MIX_DEFAULT` / map target clear rakhein. |

---

### Group C — Lemo Overall Polish & Master `3D-Animator + Lemo` Fusions

| # | Combination | Kab Use Karein | Kaise Use Karein (CLI / Script) | Kya Avoid Karein |
|---|---|---|---|---|
| **8** | **Any Lemo Style + WhisperX + Documentary SFX + Handheld** (`lemo-whisperx-audio`) | Lemo library ki kisi bhi 99 styles ko exact word-synced captions, bundled CC0 documentary SFX (`-14 LUFS`), aur subtle human shake dene ke liye. | `audio_sync.py` + `openverse_sfx.py` + `kit/mix.py` + optional `handheld.py`. | Legacy synthetic `sound_bed.py` off rakhein (bundled CC0 + Openverse default). |
| **9** | **`3D-Animator` + Lemo Palette + Lemo VHS/CRT** (`3d-lemo-crt`) | Cyber/intelligence/1990s surveillance 3D scenes jahan Three.js geometry par CRT phosphor glow aur scanlines chahiye. | `python studio.py --combo --shader=blueprint --lemo=ascii-crt --post=crt --stills=2.0` | Heavy scanlines (`track > 0.3`) chote 3D text ko blur kar sakti hain (`0.0` default clean hai). |
| **10** | **Master `3D-Animator` + `Lemo-Opuscar` + `.glb` + Handheld + Audio** (`master-3d-lemo-fusion`) | Flagship gap ya custom 3D scene jahan studio 3D geometry, real CC0 `.glb` model, Lemo color grade + GTAO bokeh, aur human shake ek saath chahiye. | `python studio.py --combo --shader=paper --lemo=dark-documentary --post=gtao --width=1080 --height=1920 --video --out=out/hybrid_9x16.mp4 --handheld-csv=motion.csv` | Ek shot me ek clear dominant look rakhein (`paper` ya `blueprint` + ek Lemo palette). |

---

## 💻 Quick CLI Cheat Sheet (`studio.py`)

```bash
# Sabhi 10 glitch-free combinations aur unke IDs terminal me dekhne ke liye:
python studio.py --list-combos

# Combo test stills (fast check --n=4):
python studio.py --combo --shader=paper --lemo=dark-documentary --post=gtao --stills=1.5,3.5 --out=stills_test

# Downloaded real CC0 3D Model (.glb/.gltf) + 3D-Animator + Lemo combo:
python studio.py --fetch-models="camera,desk" --out=models --max=2
python studio.py --combo --shader=blueprint --model=models/Camera_01/Camera_01_1k.gltf --lemo=blueprint --post=gtao --stills=2.0

# Script-aware research & gap plan.md generation:
python studio.py --plan --topic="Stuxnet" --script-file=script.txt --out=plan.md

# Live mid-shot WhisperX-synced look morphing (9:16 vertical):
python studio.py --combo --shader=0:lit,2.5:blueprint,4.5:synth --lemo=dark-documentary --width=1080 --height=1920 --video --out=out/morph_reel.mp4

# VHS/CRT archival 3D + Lemo hybrid look:
python studio.py --combo --shader=lit --lemo=briefing-board --post=crt --stills=2.0
```
