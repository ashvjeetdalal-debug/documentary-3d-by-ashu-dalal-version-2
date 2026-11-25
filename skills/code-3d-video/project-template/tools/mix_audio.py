#!/usr/bin/env python3
"""Mix voice + sfx + music into build/audio.wav: music ducks under voice, loudness normalised to -14 LUFS."""
import argparse, json, os, subprocess, sys

ap = argparse.ArgumentParser(); ap.add_argument('--story', default='story.json'); ap.add_argument('--duration', type=float, required=True)
a = ap.parse_args(); story = json.load(open(a.story)); D = a.duration

inputs = [['-f', 'lavfi', '-t', f'{D:.3f}', '-i', 'anullsrc=r=48000:cl=stereo']]
chains, mix = [], ['[base]']
chains.append('[0:a]anull[base]')


def add(extra, path):
    inputs.append(['-ac', '2'] + extra + ['-i', path]); return len(inputs) - 1


voice = story.get('voice'); vi = None
has_music = False
music = story.get('music') or {}
mpath = music.get('file') or ('build/music_pad.wav' if music.get('kind') == 'pad' else None)
if mpath and os.path.exists(mpath): has_music = True

if voice and os.path.exists(voice):
    vi = add([], voice)
    g = story.get('voiceGain', 1.0)
    if has_music: chains.append(f'[{vi}:a]aresample=48000,volume={g},asplit=2[voice][vsc]')
    else: chains.append(f'[{vi}:a]aresample=48000,volume={g}[voice]')
    mix.append('[voice]')

for k, s in enumerate(story.get('sfx', [])):
    p = s.get('file') or f"build/sfx/{s['kind']}.wav"
    if not os.path.exists(p): print('skip missing sfx', p, file=sys.stderr); continue
    i = add([], p); ms = int(s['t'] * 1000)
    chains.append(f"[{i}:a]aresample=48000,volume={s.get('gain', 0.8)},adelay={ms}|{ms}[s{k}]"); mix.append(f'[s{k}]')

if has_music:
    mi = add(['-stream_loop', '-1'], mpath)
    chains.append(f"[{mi}:a]aresample=48000,atrim=0:{D:.3f},volume={music.get('gain', 0.2)}[mus]")
    if vi is not None:
        chains.append('[mus][vsc]sidechaincompress=threshold=0.03:ratio=10:attack=15:release=350[musd]'); mix.append('[musd]')
    else: mix.append('[mus]')

chains.append(f"{''.join(mix)}amix=inputs={len(mix)}:normalize=0:duration=first,loudnorm=I=-14:TP=-1.5:LRA=11,alimiter=limit=0.94,apad=whole_dur={D:.3f},atrim=0:{D:.3f}[out]")
cmd = ['ffmpeg', '-y', '-loglevel', 'error'] + [x for grp in inputs for x in grp] + ['-filter_complex', ';'.join(chains), '-map', '[out]', '-ar', '48000', '-ac', '2', 'build/audio.wav']
r = subprocess.run(cmd)
if r.returncode: print(' '.join(cmd), file=sys.stderr); sys.exit(1)
print('audio mixed -> build/audio.wav')
