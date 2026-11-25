# Troubleshooting

| Symptom | Fix |
|---|---|
| `Missing dependency. Run: npm run setup` | run it in the project folder; needs internet once |
| Chromium missing / "Executable doesn't exist" | `npx playwright install chromium`, or add `--chrome` to use installed Chrome |
| `Scene failed to load` + stack trace | the error is from `scene.js`/`story.json`; fix and rerun (stills mode is the quickest loop) |
| Black frames | WebGL unavailable: drop `--gpu`, or add `--chrome`; check the console lines starting `[page]` |
| Import error for `three` | run `npm install`; the importmap in `index.html` points to `node_modules/three` |
| Very slow render | use `--scale 0.5` for drafts, `--gpu` on real hardware, fewer lights/shadow-map size 1024, fewer meshes |
| Captions late/early | install faster-whisper and `--realign`; check voice file is the final cut |
| Flicker between frames | something non-deterministic (`Math.random`, `Date.now`, state that accumulates); make it a function of `t` |
| `libx264` / `amix normalize` ffmpeg error | update ffmpeg (>= 4.4) |
| Odd video size error | width and height must be even |
| Text unreadable on phone | bigger canvas text, higher contrast, hold >= 1.5 s, keep out of bottom 20% |

## Added by the QA tooling
| Symptom | Fix |
|---|---|
| `npm run doctor` says smoke scene failed | the stack trace under it is the real cause (three version, WebGL, import). Try `--chrome`, then `npm install three@0.170` |
| `post-processing disabled` warning | video still renders without bloom/DOF; usually a three version mismatch: `npm install three@0.170` |
| QA says "nearly black" | camera inside geometry, or lights too weak: move camera, raise `lookOverrides.exposure`, add lamps |
| QA says "flat/empty frame" | nothing interesting in shot: add props, point the camera at a character, push in |
| Characters slide | give them a `makePath` path; walk phase comes from distance, so the path speed must be 0.8-2 m/s |
| Parallel render uses too much RAM | `--workers 2` |
