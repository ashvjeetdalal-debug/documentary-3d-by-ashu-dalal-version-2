#!/usr/bin/env python3
"""
Documentary 3D by Ashu Dalal - Openverse Audio / SFX Engine
Integrates the WordPress Openverse Audio API (https://api.openverse.org/v1/audio/)
to search, download, normalize (48 kHz WAV via ffmpeg), and log attributions for
real Creative-Commons SFX and ambient music beds (Freesound, Jamendo, Wikimedia Commons).

Replaces synthetic numpy sound generation by default while keeping sound_bed.py preserved.
"""

import os
import sys
import json
import re
import subprocess
import urllib.request
import urllib.parse
import argparse

API_BASE = "https://api.openverse.org/v1/audio/"
USER_AGENT = "Documentary3D-AshuDalal/2.1 (Openverse Audio Client; contact@antigravity.ai)"

# Curated Openverse search terms tailored for documentary SFX cues
DEFAULT_SFX_QUERIES = {
    "whoosh": "whoosh transition swish",
    "paper": "paper slide rustle page",
    "stamp": "heavy rubber stamp thud",
    "typing": "typewriter mechanical keys",
    "click": "camera shutter mechanical click",
    "thud": "deep cinematic impact boom",
    "riser": "tension riser suspense swell",
    "glitch": "digital static radio glitch",
    "footstep": "footsteps concrete corridor",
    "ding": "subtle bell notification chime"
}


def search_openverse_audio(query, category="sound_effect", license_filter="cc0,pdm,by", page_size=8, max_duration_ms=None):
    """Query Openverse Audio API for real openly-licensed sound effects or music."""
    params = {
        "q": query,
        "page_size": str(page_size)
    }
    if category:
        params["category"] = category
    if license_filter:
        params["license"] = license_filter

    url = API_BASE + "?" + urllib.parse.urlencode(params)
    req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT, "Accept": "application/json"})

    try:
        with urllib.request.urlopen(req, timeout=20) as resp:
            data = json.loads(resp.read().decode("utf-8"))
    except Exception as e:
        print(f"[OPENVERSE_SFX] API query error for '{query}': {e}", file=sys.stderr)
        return []

    results = []
    for item in data.get("results", []):
        audio_url = item.get("url")
        if not audio_url:
            continue
        dur = item.get("duration") or 0
        if max_duration_ms and dur > max_duration_ms:
            continue
        results.append({
            "id": item.get("id"),
            "title": item.get("title") or query,
            "creator": item.get("creator") or "Unknown",
            "license": item.get("license"),
            "license_version": item.get("license_version"),
            "source": item.get("source"),
            "duration_ms": dur,
            "url": audio_url,
            "foreign_landing_url": item.get("foreign_landing_url")
        })
    return results


def download_and_normalize_wav(url, out_wav, max_seconds=None):
    """Download remote Openverse audio file and normalize to 48 kHz stereo PCM WAV using ffmpeg."""
    os.makedirs(os.path.dirname(os.path.abspath(out_wav)), exist_ok=True)
    tmp_raw = out_wav + ".download"

    req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    try:
        with urllib.request.urlopen(req, timeout=30) as resp, open(tmp_raw, "wb") as f:
            f.write(resp.read())
    except Exception as e:
        print(f"[OPENVERSE_SFX] Download failed ({url}): {e}", file=sys.stderr)
        return False

    cmd = ["ffmpeg", "-y", "-v", "error", "-i", tmp_raw]
    if max_seconds:
        cmd.extend(["-t", str(max_seconds)])
    cmd.extend(["-ar", "48000", "-ac", "2", "-c:a", "pcm_s16le", out_wav])

    res = subprocess.run(cmd, capture_output=True, text=True)
    try:
        os.remove(tmp_raw)
    except OSError:
        pass

    if res.returncode != 0 or not os.path.exists(out_wav) or os.path.getsize(out_wav) < 1024:
        print(f"[OPENVERSE_SFX] ffmpeg conversion failed for {url}: {res.stderr}", file=sys.stderr)
        return False

    return True


def fetch_sfx_pack(kinds, out_dir, music_query=None):
    """
    Download a real Openverse SFX pack for named documentary action kinds + optional music bed.
    Writes normalized 48 kHz WAVs into `out_dir` and records legal attribution in `openverse_attribution.json`.
    """
    os.makedirs(out_dir, exist_ok=True)
    attributions = []
    fetched = {}

    for kind in kinds:
        query = DEFAULT_SFX_QUERIES.get(kind, kind)
        max_ms = 12000 if kind not in ("riser", "typing") else 20000
        print(f"[OPENVERSE_SFX] Searching Openverse SFX for '{kind}' ('{query}')...")
        candidates = search_openverse_audio(query, category="sound_effect", max_duration_ms=max_ms)
        if not candidates:
            # Retry without strict category filter
            candidates = search_openverse_audio(query, category=None, max_duration_ms=max_ms)

        out_wav = os.path.join(out_dir, f"{kind}.wav")
        ok = False
        for c in candidates[:4]:
            if download_and_normalize_wav(c["url"], out_wav, max_seconds=10):
                fetched[kind] = out_wav
                attributions.append({"role": f"sfx:{kind}", **c})
                print(f"  -> Ready: {kind}.wav ({c['source']} / CC-{c['license']} by {c['creator']})")
                ok = True
                break
        if not ok:
            print(f"  -> Warning: Could not download playable SFX for '{kind}'")

    if music_query:
        print(f"[OPENVERSE_SFX] Searching Openverse ambient/music bed: '{music_query}'...")
        candidates = search_openverse_audio(music_query, category="music")
        if not candidates:
            candidates = search_openverse_audio(music_query, category=None)
        music_wav = os.path.join(out_dir, "music_bed.wav")
        for c in candidates[:4]:
            if download_and_normalize_wav(c["url"], music_wav):
                fetched["music_bed"] = music_wav
                attributions.append({"role": "music_bed", **c})
                print(f"  -> Ready: music_bed.wav ({c['source']} / CC-{c['license']} by {c['creator']})")
                break

    attr_path = os.path.join(out_dir, "openverse_attribution.json")
    with open(attr_path, "w", encoding="utf-8") as f:
        json.dump(attributions, f, indent=2, ensure_ascii=False)

    print(f"[OPENVERSE_SFX] Attribution log saved -> {attr_path}")
    return fetched, attributions


def main():
    parser = argparse.ArgumentParser(description="Openverse Real SFX & Music Fetcher for Documentary 3D")
    parser.add_argument("--search", type=str, help="Search Openverse audio and print matches without downloading")
    parser.add_argument("--sfx", type=str, help="Comma-separated SFX cues/queries to fetch (e.g. whoosh,paper,stamp,typing)")
    parser.add_argument("--music", type=str, help="Ambient music / tension bed search query")
    parser.add_argument("--category", type=str, default="sound_effect", help="Openverse category (sound_effect, music, all)")
    parser.add_argument("--out", type=str, default="sound", help="Output directory for normalized 48kHz WAV files")
    args = parser.parse_args()

    if args.search:
        cat = None if args.category == "all" else args.category
        res = search_openverse_audio(args.search, category=cat, page_size=10)
        print(json.dumps(res, indent=2, ensure_ascii=False))
        return

    kinds = [k.strip() for k in (args.sfx or "").split(",") if k.strip()]
    if not kinds and not args.music:
        parser.print_help()
        return

    fetch_sfx_pack(kinds, args.out, music_query=args.music)


if __name__ == "__main__":
    main()
