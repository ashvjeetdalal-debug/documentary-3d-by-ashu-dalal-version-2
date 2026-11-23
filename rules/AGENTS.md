# Documentary 3D by Ashu Dalal — Master Production Rules & Director Protocol

When authoring, editing, directing, or rendering films with this studio plugin, adhere strictly to the **Canonical 5-Step Director Workflow** and technical laws:

---

## 🎯 The Canonical 5-Step Director Workflow (Mandatory Standard)

Whenever an operator or user initiates a documentary video request, you **MUST follow these exact steps without exception**:

### Step 1: Topic & Script Formulation
- Present high-impact documentary topics and ideas (events, historical operations, mysteries, technology, geopolitical turning points).
- Once the operator selects or confirms a topic/idea, formulate a structured, cinematic documentary script formatted for voiceover narration.

### Step 2: Voiceover Audio Intake
- Prompt the operator for the voiceover audio file (`.wav` / `.mp3`), or offer to generate voiceover audio via TTS.
- Receive the audio file before attempting to write rendering code.

### Step 3: Zero-Fake Original Archival Asset Sourcing
- **The Golden Rule**: The moment the audio file is received, immediately query and download all necessary authentic historical media using `asset_fetcher.py`.
- **Zero AI Slop**: **NO FAKE ASSETS OR CHEAP PLACEHOLDERS ALLOWED**. Every asset must be sourced from authentic public archives (Wikimedia Commons, Wikipedia, NASA, historical repositories) and verified for resolution (400x300 min, preferably 1080p+) and valid RGB image format.

### Step 4: Audio Transcript & Asset Mapping (WhisperX)
- Execute WhisperX / Whisper forced word-level alignment on the audio (`audio_sync.py`).
- Analyze the transcript wording, named entities, and timestamps to map which authentic archival asset appears at each timestamp.
- **Gap Detection**: Identify all segments and empty spaces (*"khali parts"*) where **no archival photo exists**.

### Step 5 & Substep 5(1): Interactive Consultation for Gap Spaces
- For the empty parts that lack archival assets, **do NOT make up arbitrary scenes or improvised slop**.
- **The 3 Creative Engines Consultation**: Proactively ask the user/operator which visual approach they prefer for these specific gaps, presenting the 3 built-in engines:
  1. **Lemo-Opuscar**: Curated film styles (`dark-documentary`, `archive-lighttable`, `briefing-board`, `blueprint`, `circuit-board`, `comic-history`, etc.).
  2. **p5.brush**: Natural generative media (Charcoal sketches, wet-in-wet watercolor wash/bleed, architectural hatching, graphite pencils, vector flow fields).
  3. **3D-Animator / Three.js**: Procedural 3D scene (12 shader looks: `clay`, `paper`, `blueprint`, `lit`, `synth`, `chrome`, `neon`, `voxel`, `thermal`, `shadow`, etc.).
- **Style List Mandate**: Always provide the recommended style list alongside the options. **If the operator asks for more styles, provide additional styles from the library immediately!**

---

## 🏛️ Core Creative & Technical Laws

### 1. Unified Camera Grammar & Continuous Motion
- **Evidence Board**: Maintain **one continuous camera** over the world board. Pushes, pulls, pans, and slight rotations must be smoothly eased (using cubic easing and log-space zoom interpolation).
- **3D Cinematic Scenes**: One camera move = one lens, one Bezier curve, one eased progress value. No decoupled XYZ keyframing.
- **Stylistic Transitions Only**:
  - Circular iris wipes into and out of vintage 2D silent-film inserts.
  - Sliced digital glitch transitions into final end title cards.
  - Seamless match cuts or whip pans when switching between Evidence Board, 3D World, and p5.brush drawings.

### 2. Deterministic Rendering (Pure Functions of Time)
- Across all rendering engines (Three.js WebGL, p5.brush canvases, and OpenCV video generators), `renderAt(t)` must draw the exact same picture for the same `t`, in any order.
- Never use `Date.now()`, `Math.random()`, or forward-stepping physics variables. Always use deterministic seeds (`brush.seed(n)`, `hash(n)`).
- Sub-frame accumulation for 3D: `n=16` for still inspections, `n=48` for master renders.

### 3. Directorial Rhythm & The Music Grid (`DIRECTOR.md`)
- Lock cuts, actions, and beats to a tempo-based music grid (typically 60–120 BPM). Visual marks land on the beat or 1–2 frames early.
- Subtitle rules: Subtitles must hold for a minimum of **1.8 seconds** per line. They should never flash off or jump rapidly.
- Pacing: Vary pacing across three acts: Hook/Establishment (snappy), Deep Dive (measured breathing space), Climax & Resolution (intense).

### 4. The Red Accent Principle
- The red accent color (`#d0312d` / RGB `(208, 49, 45)`) is strictly reserved for narrative meaning:
  - Pinned yarn/strings connecting evidence, 3D nodes, and diagram points
  - Hand-drawn wobble focus circles around key dates or targets
  - Typewriter label accents and underlines
  - Slammed rubber stamps (`FAILED`, `DENIED`, `CLASSIFIED`)
  - Climax thesis cards and signature wireframes
- Never use red for arbitrary decorative backgrounds.

### 5. Natural Media Tactility (`p5.brush`)
- When rendering generative diagrams, character sketches, or historical maps:
  - Use appropriate media: Pencils (`HB`, `2B`), Charcoal (`charcoal`), Markers (`marker`), Watercolor (`watercolor`).
  - Set realistic stroke vibration (`brush.setVibration(0.3)`) and pressure tooth.
  - In standalone builds, always call `brush.render()` to flush the frame buffer.

### 6. Handheld Camera Physics & Presentation
- Apply natural camera drift and subtle hand shake to make digital renders feel tactile and filmed in the real world (`phone_motion.py`, `handheld.py`).
- For vertical social media delivery (9:16 reels), use `laptop_reel.py` to place the master film inside a photorealistic desktop/laptop frame.

### 7. Historical Sensitivity & Non-Graphic Conflict
- Keep conflict and violence stylized and non-graphic: silhouette figures, subtle gunsmoke puffs, white impact frame flashes, and vintage silent-film intertitles. Never generate blood, wounds, or gore.

### 8. Master Audio Standards
- Sync every visual action within 1–2 frames of the voiceover trigger word.
- Duck background music and ambient drones under voiceover using sidechain compression (-14 dB to -18 dB gain reduction during speech).
- Master output audio strictly normalized to **-14 LUFS** with a true peak ceiling of **-1.5 dBTP** per EBU R128 broadcast standards.
