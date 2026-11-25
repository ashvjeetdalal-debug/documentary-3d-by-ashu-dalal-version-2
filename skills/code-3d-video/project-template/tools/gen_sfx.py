#!/usr/bin/env python3
"""Procedural, copyright-free sound effects + ambient pad (numpy only). Writes build/sfx/<kind>.wav.
NOTE: SILENCED BY DEFAULT in Version 3 in favor of Openverse real SFX & music (openverse_sfx.py).
To re-enable anytime: set "active_engine": "legacy_synth" in sound_config.json,
export ASHU_SOUND_ENGINE=legacy_synth, or pass --force-legacy."""
import argparse, json, os, sys, wave
import numpy as np


def _is_legacy_enabled():
    if "--force-legacy" in sys.argv:
        return True
    env = os.environ.get("ASHU_SOUND_ENGINE", "").strip().lower()
    if env:
        return env == "legacy_synth"
    here = os.path.dirname(os.path.abspath(__file__))
    for cand in [
        os.path.join(here, "sound_config.json"),
        os.path.abspath(os.path.join(here, "..", "..", "..", "documentary-3d", "scripts", "sound_config.json")),
    ]:
        if os.path.exists(cand):
            try:
                return json.load(open(cand, encoding="utf-8")).get("active_engine") == "legacy_synth"
            except Exception:
                pass
    return False

SR = 48000
rng = np.random.default_rng(7)


def t_(d): return np.arange(int(SR * d)) / SR
def noise(d): return rng.standard_normal(int(SR * d))


def lp(x, a):  # one-pole low-pass; `a` may be scalar or per-sample array
    a = np.broadcast_to(np.asarray(a, dtype=np.float64), x.shape)
    y = np.empty_like(x); s = 0.0
    for i in range(len(x)):
        s += a[i] * (x[i] - s); y[i] = s
    return y


def hp(x, a): return x - lp(x, a)
def decay(d, k): return np.exp(-k * t_(d))


def whoosh():
    d = 0.9; t = t_(d); a = 0.02 + 0.5 * np.sin(np.pi * t / d) ** 1.5
    return lp(noise(d), a) * np.sin(np.pi * t / d) ** 1.2
def click():
    d = 0.07; return hp(noise(d), 0.3) * decay(d, 90) * 0.8 + np.sin(2 * np.pi * 2200 * t_(d)) * decay(d, 120) * 0.3
def thud():
    d = 0.45; t = t_(d); return np.sin(2 * np.pi * (45 + 40 * np.exp(-14 * t)) * t) * decay(d, 9) + lp(noise(d), 0.05) * decay(d, 25) * 0.6
def footstep():
    d = 0.2; return lp(noise(d), 0.12) * decay(d, 30) + np.sin(2 * np.pi * 85 * t_(d)) * decay(d, 28) * 0.6
def ding():
    d = 1.6; t = t_(d); return (np.sin(2 * np.pi * 1318 * t) + 0.4 * np.sin(2 * np.pi * 2650 * t) + 0.2 * np.sin(2 * np.pi * 3960 * t)) * decay(d, 3.2)
def pop():
    d = 0.14; t = t_(d); return np.sin(2 * np.pi * (180 + 600 * np.exp(-40 * t)) * t) * decay(d, 28)
def riser():
    d = 2.2; t = t_(d); a = 0.01 + 0.4 * (t / d) ** 2
    return lp(noise(d), a) * (t / d) ** 1.5 + 0.25 * np.sin(2 * np.pi * np.cumsum(180 + 1100 * (t / d) ** 2) / SR) * (t / d)
def paper():
    d = 0.4; t = t_(d); crackle = (rng.random(len(t)) > 0.985) * 1.0
    return hp(noise(d), 0.4) * (0.25 + 0.75 * lp(crackle, 0.02) * 30).clip(0, 1) * decay(d, 8)
def boom():
    d = 1.4; t = t_(d); return np.sin(2 * np.pi * (38 + 30 * np.exp(-5 * t)) * t) * decay(d, 3) + lp(noise(d), 0.03) * decay(d, 6) * 0.7
def glitch():
    d = 0.25; x = np.sign(np.sin(2 * np.pi * rng.choice([300, 900, 1700, 450], 10).repeat(int(SR * d / 10) + 1)[: int(SR * d)] * t_(d)))
    return x * (rng.random(len(x)) > 0.3) * decay(d, 6) * 0.5

KINDS = {k: f for k, f in dict(whoosh=whoosh, click=click, thud=thud, footstep=footstep, ding=ding, pop=pop, riser=riser, paper=paper, boom=boom, glitch=glitch).items()}


def pad(duration, mood='dark'):
    chords = {'dark': [55, 82.4, 110, 130.8, 164.8], 'warm': [65.4, 98, 130.8, 164.8, 196], 'tense': [55, 58.3, 110, 116.5, 164.8]}[mood]
    t = t_(duration); y = np.zeros_like(t)
    for i, f in enumerate(chords):
        y += np.sin(2 * np.pi * f * t + i) * (0.6 + 0.4 * np.sin(2 * np.pi * (0.05 + 0.017 * i) * t + i))
    y += 0.15 * lp(noise(duration), 0.01) * 10
    fade = np.minimum(1, np.minimum(t / 2.0, (duration - t) / 2.5))
    return y * fade


def write(path, x):
    x = x / (np.abs(x).max() + 1e-9) * 0.9
    with wave.open(path, 'wb') as w:
        w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR); w.writeframes((x * 32767).astype('<i2').tobytes())


if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('--story', default='story.json')
    ap.add_argument('--duration', type=float, default=30)
    ap.add_argument('--force-legacy', action='store_true')
    a = ap.parse_args()
    story = json.load(open(a.story))
    os.makedirs('build/sfx', exist_ok=True)
    if not _is_legacy_enabled():
        print('[gen_sfx.py] Legacy synthetic SFX silenced by default (Openverse is active). Writing silent tracks; pass --force-legacy or switch sound_config.json to "legacy_synth" to re-enable.')
        silent = np.zeros(int(SR * 0.25), dtype=np.float64)
        for kind in {s['kind'] for s in story.get('sfx', []) if 'kind' in s}:
            write(f'build/sfx/{kind}.wav', silent)
        m = story.get('music')
        if m and m.get('kind') == 'pad':
            write('build/music_pad.wav', np.zeros(int(SR * min(a.duration, 2.0)), dtype=np.float64))
        sys.exit(0)
    for kind in {s['kind'] for s in story.get('sfx', []) if 'kind' in s}:
        if kind not in KINDS: raise SystemExit(f'Unknown sfx kind "{kind}". Available: {", ".join(KINDS)}')
        write(f'build/sfx/{kind}.wav', KINDS[kind]())
    m = story.get('music')
    if m and m.get('kind') == 'pad':
        write('build/music_pad.wav', pad(a.duration, m.get('mood', 'dark')))
    print('sfx/music ready')
