"""Kaz Documentary sound bed: dark drone + pulse + SFX, synthesized (no downloads).
NOTE: SILENCED BY DEFAULT in Version 3 in favor of Openverse real SFX & music (openverse_sfx.py).
All original synthesis code is preserved intact below. To re-enable anytime:
  - Set "active_engine": "legacy_synth" in sound_config.json, OR
  - Set environment variable ASHU_SOUND_ENGINE=legacy_synth, OR
  - Pass --force-legacy flag: python sound_bed.py cues.json out.wav --force-legacy
Usage: python3 sound_bed.py cues.json out.wav [--force-legacy]"""
import numpy as np, wave, json, sys, os

def _is_legacy_enabled():
    if "--force-legacy" in sys.argv:
        return True
    env = os.environ.get("ASHU_SOUND_ENGINE", "").strip().lower()
    if env:
        return env == "legacy_synth"
    cfg_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "sound_config.json")
    if os.path.exists(cfg_path):
        try:
            with open(cfg_path, encoding="utf-8-sig") as f:
                return json.load(f).get("active_engine") == "legacy_synth"
        except Exception:
            pass
    return False

if len(sys.argv) < 3:
    print("Usage: python sound_bed.py cues.json out.wav [--force-legacy]")
    sys.exit(1)

with open(sys.argv[1], encoding="utf-8-sig") as f:
    c = json.load(f)
sr = 48000; D = c["duration"]; n = int(sr*D)
os.makedirs(os.path.dirname(os.path.abspath(sys.argv[2])), exist_ok=True)

if not _is_legacy_enabled():
    print("[sound_bed.py] Legacy synthetic sound is SILENCED by default (Openverse is active). Writing silent track; pass --force-legacy or switch sound_config.json to 'legacy_synth' to re-enable.")
    w = wave.open(sys.argv[2], "wb"); w.setnchannels(1); w.setsampwidth(2); w.setframerate(sr)
    w.writeframes(np.zeros(n, dtype=np.int16).tobytes()); w.close()
    sys.exit(0)

t = np.arange(n)/sr
rng = np.random.default_rng(3)
pad = sum(a*np.sin(2*np.pi*f*t+np.sin(2*np.pi*.07*t)*2) for f, a in [(55,1),(65.4,.6),(82.4,.5),(110,.35),(130.8,.2)])
pad *= (.5+.5*np.sin(2*np.pi*t/23)**2)*np.clip(t/3,0,1)*np.clip((D-t)/2.5,0,1)
for p in c.get("tension", []): pad *= 1+.6*np.exp(-((t-p)/5)**2)
x = pad/np.abs(pad).max()*.16
for b in np.arange(15, D-2, 1.25):
    i = int(b*sr); L = int(.25*sr); x[i:i+L] += .08*np.sin(2*np.pi*48*np.arange(L)/sr)*np.exp(-np.arange(L)/sr*18)
def add(s, at, g):
    i = int(at*sr); e = min(n, i+len(s)); x[i:e] += g*s[:e-i]
def whoosh(d=.6):
    L = int(d*sr); r = rng.normal(0,1,L); env = np.sin(np.linspace(0,np.pi,L))**2; y = np.zeros(L); a = 0
    for k in range(L): a += (.02+.25*env[k])*(r[k]-a); y[k] = a
    return y*env/(np.abs(y).max()+1e-9)
tt = np.arange(int(1.2*sr))/sr
thud = (np.sin(2*np.pi*(70*np.exp(-tt*6)+40)*tt)*np.exp(-tt*7)+.3*rng.normal(0,1,len(tt))*np.exp(-tt*40))
shot = rng.normal(0,1,len(tt))*np.exp(-tt*9)+.8*np.sin(2*np.pi*55*tt)*np.exp(-tt*4)
click = lambda: rng.normal(0,1,int(.03*sr))*np.exp(-np.arange(int(.03*sr))/sr*250)
W = whoosh()
for a in c.get("whoosh", []): add(W, a, .25)
for s, k in c.get("type", []):
    for j in range(k): add(click(), s+j/22, .12)
for a in c.get("thud", []): add(thud, a, .55)
for a in c.get("shot", []): add(shot, a, .55)
for a, d in c.get("scratch", []):
    L = int(d*sr); add(rng.normal(0,1,L)*.5*(1+np.sin(np.arange(L)/sr*90)), a, .05)
for a, b in c.get("film", []):   # projector clatter + hiss, board SFX softened
    i, j = int(a*sr), int(b*sr); x[i:j] *= .5; L = j-i; seg = np.zeros(L)
    for k in range(int(L/sr*24)):
        p = int(k*sr/24); m = int(.012*sr)
        if p+m < L: seg[p:p+m] += rng.normal(0,1,m)*np.exp(-np.arange(m)/sr*400)
    x[i:j] += seg*.06 + rng.normal(0,1,L)*.02
for a, b in c.get("engine", []):
    i, j = int(a*sr), int(b*sr); u = np.arange(j-i)/sr; x[i:j] += np.sin(2*np.pi*38*u)*(np.sin(2*np.pi*9*u) > 0)*.12
w = wave.open(sys.argv[2], "wb"); w.setnchannels(1); w.setsampwidth(2); w.setframerate(sr)
w.writeframes((np.clip(x,-1,1)*32767).astype(np.int16).tobytes()); w.close()
