#!/usr/bin/env python3
"""Build the soundtrack from sound/cues.json: voice + music (ducked under the voice) + SFX,
then level it to streaming loudness (default -14 LUFS) with a peak limiter at -1.5 dB.

SFX VOLUME LAW (NON-NEGOTIABLE):
  Every SFX cue is strictly clamped between 15% and 20% linear amplitude (-16.48 dB to -13.98 dB,
  default 17.5% = -15.14 dB) so sound effects NEVER overpower or compromise the main narration audio.

usage: python3 mix.py [sound/cues.json] [sound/mix.wav]
"""
import json, math, os, subprocess, sys

MIN_SFX_DB = 20.0 * math.log10(0.15)  # -16.478 dB (15%)
MAX_SFX_DB = 20.0 * math.log10(0.20)  # -13.979 dB (20%)
DEF_SFX_DB = 20.0 * math.log10(0.175) # -15.139 dB (17.5%)


def _clamp_sfx_db(cue):
    if "volume_pct" in cue and cue["volume_pct"] is not None:
        pct = max(1.0, float(cue["volume_pct"]))
        raw_db = 20.0 * math.log10(pct / 100.0)
    elif "gain_db" in cue and cue["gain_db"] is not None:
        raw_db = float(cue["gain_db"])
    else:
        raw_db = DEF_SFX_DB
    clamped = max(MIN_SFX_DB, min(MAX_SFX_DB, raw_db))
    return clamped


cues_path = sys.argv[1] if len(sys.argv) > 1 else 'sound/cues.json'
out_path = sys.argv[2] if len(sys.argv) > 2 else 'sound/mix.wav'
os.makedirs(os.path.dirname(os.path.abspath(out_path)), exist_ok=True)
cfg = json.load(open(cues_path, encoding='utf-8-sig'))
L = float(cfg['length'])
inputs, chains, mix = [], [], []

def add_input(path, ss=None):
    if ss: inputs.extend(['-ss', str(ss)])
    inputs.extend(['-i', path]); return len([a for a in inputs if a == '-i']) - 1

def ms(t): return int(round(float(t) * 1000))

voice = cfg.get('voice')
if voice:
    i = add_input(voice['file'])
    d = ms(voice.get('at', 0))
    chains.append(f"[{i}:a]aresample=48000,aformat=channel_layouts=stereo,volume={voice.get('gain_db', 0)}dB,asetpts=PTS+{d}/1000/TB,aresample=async=1:first_pts=0,apad,atrim=0:{L}[vo]")
    if cfg.get('music', {}).get('duck', True) and cfg.get('music'):
        chains.append('[vo]asplit=2[vo_mix][vo_key]'); mix.append('[vo_mix]')
    else: mix.append('[vo]')

music = cfg.get('music')
if music:
    i = add_input(music['file'], music.get('start'))
    fo = float(music.get('fade_out', 0.8))
    chains.append(f"[{i}:a]aresample=48000,aformat=channel_layouts=stereo,atrim=0:{L},asetpts=N/SR/TB,volume={music.get('gain_db', -16)}dB,"
                  f"afade=t=in:d=0.05,afade=t=out:st={max(0, L - fo)}:d={fo},apad,atrim=0:{L}[mu]")
    if voice and music.get('duck', True):
        chains.append('[mu][vo_key]sidechaincompress=threshold=0.02:ratio=5:attack=20:release=350:makeup=1[mud]'); mix.append('[mud]')
    else: mix.append('[mu]')

sfx_log = []
for k, s in enumerate(cfg.get('sfx', [])):
    i = add_input(s['file'])
    d = ms(s['at']); trim = f",atrim=0:{s['trim']}" if s.get('trim') else ''
    sfx_db = _clamp_sfx_db(s)
    sfx_pct = 100.0 * (10.0 ** (sfx_db / 20.0))
    sfx_log.append((os.path.basename(s['file']), s['at'], sfx_db, sfx_pct))
    chains.append(f"[{i}:a]aresample=48000,aformat=channel_layouts=stereo{trim},volume={sfx_db:.2f}dB,asetpts=PTS+{d}/1000/TB,aresample=async=1:first_pts=0,apad,atrim=0:{L}[s{k}]")
    mix.append(f'[s{k}]')

if not mix: sys.exit('cues.json has no voice, music or sfx')
graph = ';'.join(chains) + f";{''.join(mix)}amix=inputs={len(mix)}:normalize=0:duration=longest,atrim=0:{L}[bus]"
T = cfg.get('target_lufs', -14)
tmp = out_path + '.raw.wav'
subprocess.run(['ffmpeg', '-y', '-v', 'error', *inputs, '-filter_complex', graph, '-map', '[bus]', '-c:a', 'pcm_f32le', tmp], check=True)

def loudness(path, extra=''):
    r = subprocess.run(['ffmpeg', '-hide_banner', '-nostats', '-i', path, '-af', (extra + ',' if extra else '') + 'ebur128=peak=true', '-f', 'null', '-'],
                       capture_output=True, text=True).stderr
    if 'Summary:' not in r:
        raise RuntimeError(f"ffmpeg ebur128 failed:\n{r}")
    summary = r[r.rindex('Summary:'):]
    I = float(summary.split('I:')[1].split('LUFS')[0]); P = float(summary.split('Peak:')[1].split('dBFS')[0])
    return I, P

I0, P0 = loudness(tmp)
gain = T - I0
for _ in range(3):
    chain = f'volume={gain:.2f}dB,alimiter=limit=0.84:attack=5:release=60:level=false'
    I1, P1 = loudness(tmp, chain)
    if abs(I1 - T) < 0.3: break
    gain += T - I1
subprocess.run(['ffmpeg', '-y', '-v', 'error', '-i', tmp, '-af', chain + ',aresample=48000', '-c:a', 'pcm_s24le', out_path], check=True)
os.replace(tmp, out_path + '.unlevelled.wav')
print(f"mix -> {out_path}  ({len(mix)} layers, {L:.2f} s)  {I0:.1f} LUFS -> {I1:.1f} LUFS (target {T}), true peak {P1:.1f} dBTP")
if voice and voice.get('at') is not None:
    print(f"  {float(voice.get('at')):6.2f} s  voice (100%)")
for name, at, db, pct in sfx_log:
    print(f"  {float(at):6.2f} s  {name} [clamped SFX: {pct:.1f}% / {db:.2f} dB]")
