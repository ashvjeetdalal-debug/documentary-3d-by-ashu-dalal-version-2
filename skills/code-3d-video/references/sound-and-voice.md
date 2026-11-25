# Sound and voice

## Voice
The pipeline needs one audio file: `audio/voice.wav` (any format ffmpeg reads). Options:
- Record it yourself (best), phone voice memo is fine; export to wav/m4a.
- macOS: `say -v Samantha -o audio/voice.aiff -f script.txt && ffmpeg -y -i audio/voice.aiff audio/voice.wav`
- `pip install edge-tts` then `edge-tts --voice en-US-GuyNeural --file script.txt --write-media audio/voice.mp3`
- A commercial TTS (ElevenLabs etc.): download the file into `audio/`. Check the licence for commercial use.
Set `"voice": "audio/voice.mp3"` in story.json if the extension differs. Clean noise first if needed:
`ffmpeg -i in.wav -af "highpass=f=80,afftdn=nf=-25,loudnorm=I=-16" audio/voice.wav`.

## Word timing
`pip install faster-whisper` gives exact word times. The fallback (speech energy + syllable weights) drifts by up to a
few hundred ms on long, fast narration. If captions look late/early, install faster-whisper and run `--realign`.

## Sfx design
- Every visual event gets a sound within 40 ms: footstep, click, paper, door thud, light flicker (glitch).
- Transitions: `whoosh` on fast camera moves; `riser` 1.5-2 s before a reveal, `boom` or `thud` on the reveal, then 0.3 s of near-silence.
- `ding` for key information appearing (a name, a number). Do not overuse: 5-10 sfx in 40 s is plenty.
- Own sounds: `{ "t": 3.2, "file": "audio/door.wav", "gain": 0.9 }`. Use only sounds you have rights to.

## Music
`pad` is a generated ambient bed (dark/warm/tense) - safe to publish. Gain 0.2-0.35; it ducks automatically under the voice.
Final loudness is normalised to -14 LUFS (YouTube/Instagram/TikTok standard), true peak -1.5 dB.
