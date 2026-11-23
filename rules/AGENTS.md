# Documentary 3D by Ashu Dalal — Master Production Rules

When authoring, editing, directing, or rendering films with this studio plugin, adhere strictly to these core creative and technical laws:

---

## 0. Zero Synthetic Slop & Automatic Archival Asset Intake (The Golden Rule)
- **Zero AI Slop / Synthetic Placeholders**: Never generate cheap procedural drawings, flat synthetic placeholder boxes, or unverified cartoon imagery.
- **Automatic Archival Sourcing**: The moment a voiceover or topic is provided without pre-existing assets, the system **MUST automatically search, download, and verify authentic historical assets** from Wikimedia Commons, Wikipedia, and public historical repositories (`asset_fetcher.py`).
- **Asset Verification Mandate**: Every downloaded asset must be programmatically verified for resolution (minimum 400x300, preferably 1080p+), valid image integrity via PIL, and clean RGB format before being mapped onto 3D evidence slabs or PBR materials.

---

## 1. WhisperX Forced Word-Level Alignment & Precise Audio Sync
- **No Manual Timing Guesswork**: Never estimate sentence or cut timings using crude syllable counting or manual guessing.
- **Automatic Word Alignment**: Immediately upon receiving voiceover audio, run WhisperX / Whisper forced word-level alignment (`audio_sync.py` with `word_timestamps=True`).
- **Exact Visual-to-Speech Locking**:
  - Visual marks, camera focus shifts, pushpin slams, and 3D transitions MUST land within **1–2 frames** of the exact spoken trigger word.
  - Subtitles must be generated from the word alignment and hold for a minimum of **1.8 seconds** per line.

---

## 2. Unified Camera Grammar & Continuous Motion
- **Evidence Board**: Maintain **one continuous camera** over the world board. Pushes, pulls, pans, and slight rotations must be smoothly eased (using cubic easing and log-space zoom interpolation).
- **3D Cinematic Scenes**: One camera move = one lens, one Bezier curve, one eased progress value. No decoupled XYZ keyframing.
- **Stylistic Transitions Only**:
  - Circular iris wipes into and out of vintage 2D silent-film inserts.
  - Sliced digital glitch transitions into final end title cards.
  - Seamless match cuts or whip pans when switching between Evidence Board, 3D World, and p5.brush drawings.

---

## 3. Deterministic Rendering (Pure Functions of Time)
- **The Core Law**: Across all rendering engines (Three.js WebGL, p5.brush canvases, and OpenCV video generators), `renderAt(t)` must draw the exact same picture for the same `t`, in any order.
- **No Non-Deterministic State**: Never use `Date.now()`, `Math.random()`, or forward-stepping physics variables. Always use deterministic seeds (`brush.seed(n)`, `hash(n)`).
- **Sub-frame Accumulation for 3D**:
  - `n = 4–8`: Previews
  - `n = 16`: Still inspections
  - `n = 48`: Master renders (motion blur, soft shadows, depth-of-field, anti-aliasing)

---

## 4. Directorial Rhythm & The Music Grid (`DIRECTOR.md`)
- **Sound & Music Grid**: Lock cuts, actions, and beats to a tempo-based music grid (typically 60–120 BPM). Visual marks land on the beat or 1–2 frames early.
- **Subtitle Rules**: Subtitles must hold for a minimum of **1.8 seconds** per line. They should never flash off or jump rapidly.
- **Pacing**: Vary the pacing across three acts: Hook/Establishment (snappy, energetic), Exploration/Deep Dive (measured, breathing space), Climax & Resolution (intense, definitive).

---

## 5. The Red Accent Principle
- The red accent color (`#d0312d` / RGB `(208, 49, 45)`) is strictly reserved for narrative meaning:
  - Pinned yarn/strings connecting evidence, 3D nodes, and diagram points
  - Hand-drawn wobble focus circles around key dates or targets
  - Typewriter label accents and underlines
  - Slammed rubber stamps (`FAILED`, `DENIED`, `CLASSIFIED`)
  - Climax thesis cards and signature wireframes
- Never use red for arbitrary decorative backgrounds.

---

## 6. Natural Media Tactility (`p5.brush`)
- When rendering generative diagrams, character sketches, or historical maps:
  - Use appropriate media: Pencils (`HB`, `2B`) for technical drawings, Charcoal (`charcoal`) for expressive silhouettes, Markers (`marker`) for overlays, and Watercolor (`watercolor`) for atmospheric washes.
  - Set realistic stroke vibration (`brush.setVibration(0.3)`) and pressure tooth.
  - When using the standalone build, always call `brush.render()` to flush the frame buffer.

---

## 7. Handheld Camera Physics & Presentation
- Apply natural camera drift and subtle hand shake to make digital renders feel tactile and filmed in the real world.
- Use `phone_motion.py` to sample real human camera motion via 2D FFT phase correlation, and `handheld.py` to inject natural micro-shake and wander into rendered frames.
- For vertical social media delivery (9:16 reels), use `laptop_reel.py` to place the master film inside a photorealistic desktop/laptop frame.

---

## 8. Historical Sensitivity & Non-Graphic Conflict
- Keep conflict and violence stylized and non-graphic:
  - Depict clashes using silhouette figures, subtle gunsmoke puffs, white impact frame flashes, and vintage silent-film intertitles.
  - Never generate blood, wounds, or graphic gore.

---

## 9. Master Audio Standards
- Sync every visual action within 1–2 frames of the voiceover trigger word.
- Duck background music and ambient drones under voiceover using sidechain compression (-14 dB to -18 dB gain reduction during speech).
- Master output audio strictly normalized to **-14 LUFS** with a true peak ceiling of **-1.5 dBTP** per EBU R128 broadcast standards.
