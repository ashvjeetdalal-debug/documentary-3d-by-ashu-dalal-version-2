#!/usr/bin/env python3
"""Make words.json = [{"w","t0","t1"}...] (seconds) for captions, mouth movement and camera sync.

Priority: faster-whisper -> openai-whisper -> energy-based alignment of story.script to the voice file
-> pure estimate (no voice, ~150 wpm). Install real alignment with: pip install faster-whisper
"""
import argparse, json, os, re, subprocess, sys
import numpy as np

ap = argparse.ArgumentParser()
ap.add_argument('--story', default='story.json')
ap.add_argument('--out', default='words.json')
ap.add_argument('--estimate', action='store_true', help='no voice: spread script at --wpm')
ap.add_argument('--wpm', type=float, default=150)
ap.add_argument('--model', default='small')
a = ap.parse_args()

story = json.load(open(a.story))
script = story.get('script', '')
tokens = re.findall(r"\S+", script)
voice = story.get('voice')
has_voice = bool(voice) and os.path.exists(voice) and not a.estimate


def syll(w):
    return max(1, len(re.findall(r"[aeiouy]+", w.lower()))) + 0.3


def write(words, method):
    json.dump([{'w': w['w'], 't0': round(w['t0'], 3), 't1': round(w['t1'], 3)} for w in words], open(a.out, 'w'), indent=1)
    print(f'words.json: {len(words)} words via {method}', file=sys.stderr)


def whisper_words():
    try:
        import whisperx, torch
        device = 'cuda' if torch.cuda.is_available() else 'cpu'
        m = whisperx.load_model(a.model, device, compute_type='float32')
        audio = whisperx.load_audio(voice)
        res = m.transcribe(audio, batch_size=4)
        am, meta = whisperx.load_align_model(language_code=res['language'], device=device)
        aligned = whisperx.align(res['segments'], am, meta, audio, device, return_char_alignments=False)
        out = [{'w': w['word'].strip(), 't0': w['start'], 't1': w['end']} for s in aligned.get('segments', []) for w in s.get('words', []) if 'start' in w and 'end' in w]
        if out:
            return out, 'whisperx'
    except Exception:
        pass
    try:
        from faster_whisper import WhisperModel
        m = WhisperModel(a.model, device='cpu', compute_type='int8')
        segs, _ = m.transcribe(voice, word_timestamps=True)
        return [{'w': w.word.strip(), 't0': w.start, 't1': w.end} for s in segs for w in s.words], 'faster-whisper'
    except ImportError:
        pass
    try:
        import whisper
        r = whisper.load_model(a.model).transcribe(voice, word_timestamps=True)
        return [{'w': w['word'].strip(), 't0': w['start'], 't1': w['end']} for s in r['segments'] for w in s['words']], 'openai-whisper'
    except ImportError:
        return None, None


if has_voice:
    words, method = whisper_words()
    if words:
        write(words, method); sys.exit(0)
    if not tokens:
        sys.exit('No whisper installed and story.script is empty: install faster-whisper or add "script" to story.json')
    # Energy-based fallback: find voiced regions, map script words (weighted by syllables) onto voiced time only.
    pcm = subprocess.run(['ffmpeg', '-v', 'error', '-i', voice, '-ac', '1', '-ar', '16000', '-f', 's16le', '-'], capture_output=True).stdout
    x = np.frombuffer(pcm, dtype=np.int16).astype(np.float32) / 32768
    hop = 320  # 20 ms
    n = len(x) // hop
    rms = np.sqrt((x[:n * hop].reshape(n, hop) ** 2).mean(axis=1))
    thr = max(0.012, 0.08 * np.percentile(rms, 95))
    on = rms > thr
    regions, s = [], None
    for i, v in enumerate(on):
        if v and s is None: s = i
        if not v and s is not None: regions.append([s, i]); s = None
    if s is not None: regions.append([s, n])
    merged = []
    for r in regions:  # bridge gaps < 180 ms (inside words/phrases)
        if merged and r[0] - merged[-1][1] < 9: merged[-1][1] = r[1]
        else: merged.append(r)
    merged = [[r[0] * 0.02, r[1] * 0.02] for r in merged if (r[1] - r[0]) >= 4]
    if not merged: sys.exit('No speech detected in voice file')
    total = sum(e - s for s, e in merged)

    def to_real(v):
        for s, e in merged:
            if v <= e - s: return s + v
            v -= e - s
        return merged[-1][1]
    wts = [syll(t) for t in tokens]; tw = sum(wts); c = 0; words = []
    for t, w in zip(tokens, wts):
        words.append({'w': t, 't0': to_real(c / tw * total), 't1': to_real((c + w * 0.92) / tw * total)}); c += w
    write(words, 'energy alignment (install faster-whisper for exact timing)')
else:
    if not tokens: sys.exit('story.script is empty')
    t = 0.4; words = []
    for tok in tokens:
        d = 60 / a.wpm * (0.7 + 0.18 * syll(tok))
        words.append({'w': tok, 't0': t, 't1': t + d * 0.9})
        t += d + (0.28 if re.search(r"[.!?]$", tok) else 0.1 if tok.endswith(',') else 0)
    write(words, 'estimate (no voice)')
