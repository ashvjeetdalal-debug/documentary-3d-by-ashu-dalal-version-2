---
name: code-3d-video
description: Build short 3D explainer / story videos (9:16 reels, shorts, 16:9) entirely from code with Claude Code - real 3D scenes (three.js) with articulated characters, cinematic lighting, bloom, depth of field and motion blur, rendered frame-by-frame in headless Chrome, word-synced captions, procedural sound effects, ducked music, final MP4 via ffmpeg. No Blender, no AI image or video generators. Includes automatic doctor / lint / visual-QA tooling so the first build lands close to the brief. Use this skill whenever the user wants a 3D video, animated explainer, faceless-channel story, reel/short made with code, a "Claude makes the video" workflow, or asks to turn a script or voiceover into a visual video, even if they never say "three.js" or "skill".
compatibility: Node 18+, Python 3.9+ with numpy, ffmpeg + ffprobe on PATH, Chrome/Chromium via Playwright, three.js (npm). Optional - faster-whisper for exact word timing; a GPU for fast renders.
---

# code-3d-video

> [!NOTE]
> **Version 3 Role Rule**: Inside `documentary-3d-by-ashu-dalal-version-3`, `code-3d-video` is part of the **Primary 3D Documentary Backbone** alongside `board_engine.py`. Follow `rules/AGENTS.md` 5-Step Intake (Topic $\to$ Audio $\to$ Zero-Fake Internet Assets $\to$ WhisperX $\to$ Gap Choice) when making documentaries; `tools/build.mjs` defaults to **Openverse SFX/Music** (legacy `gen_sfx.py` silenced unless `--legacy-sfx`).

Pipeline: **brief -> script -> voice -> word timings -> 3D scene (kit) -> QA stills -> parallel deterministic render
(motion blur) -> sfx/music mix -> MP4.** Everything visual is code. The only thing this skill cannot create is the
voice recording (see `references/sound-and-voice.md`).

## What to tell the user up front (be honest, once, briefly)
- Look = stylized 3D (articulated mannequin characters, real lights/shadows/fog/bloom/DOF/motion blur). It is NOT
  photoreal. For richer characters use a glTF model the user has rights to (`src/kit/gltf.js`, section below).
- The first render of a brand-new story is a draft. The QA loop below exists to make draft #1 already close and draft #2 final.

## Setup (once per machine) - run in this order, stop at the first failure
1. Copy `project-template/` to a new folder (one folder per video).
2. `npm run setup` (installs three + playwright + Chromium; needs internet once).
3. `npm run doctor` - proves ffmpeg, Python, browser, WebGL **and a real three.js smoke scene** work. If it fails, fix what it
   says (each line has a fix). Never start building on a failing doctor.
4. `npm run selftest` -> `out/selftest.mp4` plays with captions and sound.

## Intake (Obeys Version 3 `rules/AGENTS.md` First)
- **In Documentary Mode (default)**: Follow Version 3's 5-Step Workflow (`Topic + Full Internet/Social Research -> Script -> Audio Intake -> Multi-Source Real Assets -> WhisperX Alignment -> Gap Consultation`). Do NOT skip Step 2 audio or synthesize pad audio when Openverse is active.
- **In Standalone Quick-Draft Mode** (only if user explicitly asks for a fast silent 3D test): Defaults are `9:16`, `1080x1920`, `30 fps`, `30-45 s`, look `noir` / `day` / `warm` / `clean`.

## Protocol (follow exactly; this is what makes it work first time)
1. **Script** (`references/directing.md`): 150 wpm, one visual per sentence, hook in the first 3 s. Write it into `story.json -> script`.
2. **Shot list** in a short table: time | location | what is in frame | camera move | on-screen text | sfx. Keep locations physically
   adjacent along the camera path (one continuous take).
3. **Build the world** in `src/scene.js` using the kit (`src/kit/*`, API below). Copy the structure of the demo scene. Set `look`,
   `camera` keys, `labels`, `sfx`, `music` in `story.json`. Do NOT write raw three.js when a kit builder exists.
4. **`npm run qa`** - lint + renders stills at every camera key / label / reveal + exposure checks + `out/qa/contact.png`.
   **Open `out/qa/contact.png` and look at it.** Judge against this rubric; fix and re-run until all pass (usually 1-2 rounds):
   - Subject (character/prop) visible and not cropped in every shot where the narration mentions it.
   - Not too dark/flat; lit subject clearly lighter or warmer than background; no camera inside geometry (black or striped frames).
   - Text (labels, documents, signs) legible at phone size; nothing important in the bottom 20% (captions live there).
   - Each location reads in one glance; the world is not empty (add props, lamps, signs, fog depth).
   - Camera framing changes between consecutive stills (no static 3 s stretches).
5. **`npm run preview`** (half size, 1 motion-blur sample, parallel workers). Watch with sound; check timing against the words.
6. **`npm run build`** -> `out/final.mp4`. On a machine with a GPU add `-- --gpu`; if WebGL is flaky add `-- --chrome`.
7. Deliver: path of the MP4, the script, and what to tweak (`story.json` is the control panel). Offer 2 concrete variations.

`build` runs lint first and refuses to render on FAIL items (override: `--force`).

## story.json reference
| key | meaning |
|---|---|
| `look` | `noir` `warm` `day` `clean` (`lookOverrides` tweaks any key in `src/kit/looks.js`) |
| `post`, `dof` | `false` disables post-processing / depth of field |
| `width,height,fps` | default 1080x1920 @30. Must be even numbers |
| `script` | exact narration text |
| `voice`, `words` | voice file path; words.json path (generated) |
| `camera[]` | `{t, pos:[x,y,z], look:[x,y,z], fov}`; smooth path, soft start/stop. `cameraTension` 0..1 reduces overshoot |
| `labels[]` | `{t0,t1,text}` location/date pills |
| `speaker`, `speakers[]` | who talks (`{t0,t1,who}`); scenes use it to move the right mouth |
| `sfx[]` | `{t, kind, gain}` kinds: whoosh click thud footstep ding pop riser paper boom glitch; or `{t, file}` |
| `music` | `{kind:"pad", mood:"dark|warm|tense", gain}` or `{file, gain}`; ducks under voice |
| `motionBlur`, `shutter` | sub-frames per frame (final default 4, preview 1) and shutter (0.5 = film) |
| `captions.chunk` | words per caption chunk (default 3) |
| `duration`, `tail` | override length / seconds after last word (default 0.8) |

## Kit API (`src/kit/`)
```js
const stage = await createStage({THREE, canvas, story});   // renderer, scene, camera, lights, post-FX (auto-falls back if post fails)
stage.render(t, s.camera, focusPoint /*[x,y,z] DOF target*/);

street({THREE, scene, rng, length, lamps, look})   -> {update(t)}      // road, lit buildings, flickering lamps
room({THREE, scene, w,d,h, origin})                 -> {group, update(t)}  // open toward +z; window + lamp
desk / box / sign / documentMesh({title,text|numbers}) / picture({draw(ctx,w,h)})   // props with readable canvas text

const path = makePath([{t, pos:[x,y,z]}, ...], {ease:'linear'|'inOut'});   // deterministic walking route
createCharacter({THREE, scene, name, height, skin, shirt, pants, hair, hairStyle:'short|long|bald',
                 mood:'neutral|smile|worried|angry', path | pos+yaw, lookAt: [x,y,z] | t=>[x,y,z]})
   .update(t, {speaking, word})      // walk cycle from distance walked, gestures per spoken word, blinking, mouth flap, head look
loadGLTFCharacter({THREE, scene, url:'./assets/x.glb', height, path, clips:{idle:'idle', walk:'walk'}})   // optional upgrade
```
`update(t, s)` in a scene receives `s.camera`, `s.speaking`, `s.word`. Gate `speaking` per character with `speakers[]`.

## Hard rules for scene code (cause 90% of broken renders)
- **Deterministic**: frame = pure function of `t`. No `Date.now`, `Math.random` (use the `rng` passed in), `requestAnimationFrame`,
  accumulating physics. Build once; only *set* values in `update`.
- No network at render time: no CDN, no remote textures. Draw textures with canvas or load files from `assets/`.
- Everything relative to canvas size; never hard-code pixels.
- Keep point lights <= 8, one shadow-casting light (the stage key). More lights = much slower renders.
- A noun is visible within 0.3 s of being spoken. Labels stay on screen >= 1.5 s.
- Characters: heights 1.2 (kid) to 1.9 m; camera eye height 1.2-1.7 m for human POV; camera never inside walls (check the stills).

## Commands
```
npm run doctor | selftest | qa | stills -- 2,8,14 | preview | build
node tools/build.mjs --workers 4 --mb 4 --gpu --chrome --realign --story other.json --out out/x.mp4 --force
```
Speed: parallel workers split frames across browsers (default min(4, cores/2)); `--gpu` is the biggest win on real hardware.
Software GL (default) is reliable but slow: budget minutes for a 40 s 1080x1920 video; preview at half size first.

## glTF upgrade (richer characters)
Free CC0 character packs exist (e.g. Quaternius, Kenney) - check each licence; some sites (Mixamo) require login and have their own terms.
Put the `.glb` in `assets/`, then in `scene.js` swap `createCharacter` for `loadGLTFCharacter` (`await` it in `build`). Animation is driven by
distance walked and time, never by wall clock. Face/mouth morphs are not driven automatically (model-specific): add head nods or rely on captions.

## Troubleshooting
See `references/troubleshooting.md`. When a render fails, read the first `[page error]` line - it is the scene's real error.
