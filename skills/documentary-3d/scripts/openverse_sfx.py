#!/usr/bin/env python3
"""
Documentary 3D by Ashu Dalal (Version 3) - On-Demand YouTube & Multi-Source Free Documentary SFX Engine
Searches, downloads, normalizes (48 kHz stereo WAV via ffmpeg), and logs attributions across:
  1. YouTube Free / Creative-Commons Documentary SFX (via yt-dlp ytsearch + direct YouTube URLs)
  2. Openverse Audio API (keyless CC0/CC-BY: Freesound previews, Jamendo, Wikimedia)
  3. Wikimedia Commons Audio (keyless authentic .ogg/.wav/.mp3 Foley & sirens)
  4. Internet Archive Audio (keyless public-domain historical/SFX recordings)
  5. Freesound API v2 (auto-enabled when FREESOUND_API_KEY env var is set)
  6. Direct --from-urls found during internet research (YouTube Audio Library, Mixkit, Zapsplat, Sonniss)

Note: Pre-bundled SFX files are removed; all SFX are researched & fetched on demand and mixed at 15%-20% volume (-16.48 to -13.98 dB) so main narration audio is never compromised. Legacy sound_bed.py / gen_sfx.py stay silenced by default.
"""

import os
import sys
import json
import shutil
import subprocess
import urllib.request
import urllib.parse
import argparse

API_BASE = "https://api.openverse.org/v1/audio/"
USER_AGENT = "Documentary3D-AshuDalal/3.0 (YouTube+Multi-Source Audio Client; contact@antigravity.ai)"

# Curated search terms tailored for documentary SFX cues
DEFAULT_SFX_QUERIES = {
    "sub_drop": "sub bass drop impact",
    "braam": "cinematic braam horn boom",
    "thud": "heavy door thud impact",
    "stamp": "heavy rubber stamp thud",
    "riser": "tension riser suspense swell",
    "reverse_cymbal": "reverse cymbal swell",
    "whoosh": "whoosh transition swish",
    "whoosh_deep": "deep whoosh cinematic pass",
    "paper": "paper slide rustle page",
    "page_flip": "book page turn flip",
    "typewriter": "typewriter mechanical keys",
    "typewriter_ding": "typewriter bell ding",
    "marker": "marker pen stroke paper",
    "pin": "thumbtack pin click",
    "shutter": "camera shutter mechanical click",
    "projector": "film projector 16mm reel clatter",
    "glitch": "digital static radio glitch",
    "static_burst": "tv vhs static noise burst",
    "clock_tick": "clock ticking suspense",
    "heartbeat": "heartbeat pulse thump",
    "radar_ping": "sonar radar ping",
    "ui_click": "digital interface click blip",
    "drone_dark": "dark ambient tension drone",
    "typing": "typewriter mechanical keys",
    "click": "camera shutter mechanical click",
    "boom": "sub bass drop impact",
    "ding": "typewriter bell ding",
    "pop": "digital interface click blip",
    "footstep": "footsteps concrete corridor"
}


def _http_get_json(url, timeout=25, headers=None):
    hdrs = {"User-Agent": USER_AGENT, "Accept": "application/json"}
    if headers:
        hdrs.update(headers)
    req = urllib.request.Request(url, headers=hdrs)
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        return json.loads(resp.read().decode("utf-8"))


def search_youtube_audio(query, category=None, limit=4, max_duration_s=25):
    """Search YouTube for copyright-free / no-copyright documentary SFX or ambient music via yt-dlp."""
    ytdlp = shutil.which("yt-dlp")
    if not ytdlp:
        return []
    suffix = "no copyright documentary music" if category == "music" else "copyright free sound effect"
    search_expr = f"ytsearch{max(limit * 2, 6)}:{query} {suffix}"
    cmd = [ytdlp, "--dump-json", "--flat-playlist", "--no-warnings", search_expr]
    try:
        res = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
        if res.returncode != 0:
            return []
        out = []
        max_s = 600 if category == "music" else max_duration_s
        for line in res.stdout.splitlines():
            line = line.strip()
            if not line:
                continue
            try:
                item = json.loads(line)
            except Exception:
                continue
            dur = item.get("duration") or 0
            if dur <= 0 or dur > max_s:
                continue
            vid = item.get("id")
            url = item.get("webpage_url") or item.get("url") or (f"https://www.youtube.com/watch?v={vid}" if vid else None)
            if not url:
                continue
            out.append({
                "id": str(vid or ""),
                "title": item.get("title") or query,
                "creator": item.get("uploader") or item.get("channel") or "YouTube",
                "license": "youtube_verify_cc",
                "license_version": "",
                "source": "youtube_ytdlp",
                "duration_ms": int(dur * 1000),
                "url": url,
                "foreign_landing_url": url
            })
            if len(out) >= limit:
                break
        return out
    except Exception as e:
        print(f"[AUDIO_ENGINE] YouTube search notice for '{query}': {e}", file=sys.stderr)
        return []


def search_openverse_audio(query, category=None, license_filter="cc0,pdm,by", page_size=8, max_duration_ms=None):
    """Query Openverse Audio API for real openly-licensed sound effects or music."""
    params = {"q": query, "page_size": str(page_size)}
    if category and category != "all":
        params["category"] = category
    if license_filter:
        params["license"] = license_filter

    try:
        data = _http_get_json(API_BASE + "?" + urllib.parse.urlencode(params))
        if not data.get("results") and "category" in params:
            params.pop("category", None)
            data = _http_get_json(API_BASE + "?" + urllib.parse.urlencode(params))
    except Exception as e:
        print(f"[AUDIO_ENGINE] Openverse query error for '{query}': {e}", file=sys.stderr)
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
            "license": item.get("license") or "cc",
            "license_version": item.get("license_version") or "",
            "source": f"openverse:{item.get('source', 'web')}",
            "duration_ms": dur,
            "url": audio_url,
            "foreign_landing_url": item.get("foreign_landing_url") or audio_url
        })
    return results


def search_wikimedia_audio(query, limit=4):
    """Search Wikimedia Commons File namespace for real .ogg/.wav/.mp3/.flac audio recordings."""
    try:
        sdata = _http_get_json("https://commons.wikimedia.org/w/api.php?" + urllib.parse.urlencode({
            "action": "query", "list": "search", "srsearch": f"{query} filetype:audio",
            "srnamespace": "6", "srlimit": str(limit), "format": "json"
        }))
        titles = [
            it.get("title", "")
            for it in sdata.get("query", {}).get("search", [])
            if it.get("title", "").lower().endswith((".ogg", ".wav", ".mp3", ".flac", ".oga"))
        ]
        if not titles:
            return []
        idata = _http_get_json("https://commons.wikimedia.org/w/api.php?" + urllib.parse.urlencode({
            "action": "query", "titles": "|".join(titles),
            "prop": "imageinfo", "iiprop": "url|size|mime", "format": "json"
        }))
        out = []
        for _, page in idata.get("query", {}).get("pages", {}).items():
            info = (page.get("imageinfo") or [{}])[0]
            u = info.get("url")
            if u:
                out.append({
                    "id": str(page.get("pageid", "")),
                    "title": page.get("title", query).replace("File:", ""),
                    "creator": "Wikimedia Commons",
                    "license": "cc_or_pd",
                    "license_version": "",
                    "source": "wikimedia_commons",
                    "duration_ms": 0,
                    "url": u,
                    "foreign_landing_url": f"https://commons.wikimedia.org/wiki/{urllib.parse.quote(page.get('title', ''))}"
                })
        return out
    except Exception as e:
        print(f"[AUDIO_ENGINE] Wikimedia audio notice for '{query}': {e}", file=sys.stderr)
        return []


def search_archive_audio(query, limit=3):
    """Search Internet Archive title-filtered public audio items."""
    try:
        q_tok = query.strip().split()[0]
        sdata = _http_get_json("https://archive.org/advancedsearch.php?" + urllib.parse.urlencode({
            "q": f'title:("{q_tok}") AND mediatype:audio',
            "fl[]": "identifier,title,creator", "rows": str(limit), "page": "1", "output": "json"
        }))
        out = []
        for doc in sdata.get("response", {}).get("docs", []):
            ident = doc.get("identifier")
            if not ident:
                continue
            meta = _http_get_json(f"https://archive.org/metadata/{ident}")
            aud = next(
                (f.get("name") for f in meta.get("files", [])
                 if str(f.get("name", "")).lower().endswith((".mp3", ".wav", ".ogg"))),
                None
            )
            if aud:
                u = f"https://archive.org/download/{ident}/{urllib.parse.quote(aud)}"
                out.append({
                    "id": ident,
                    "title": doc.get("title") or ident,
                    "creator": doc.get("creator") or "Internet Archive",
                    "license": "public_archive",
                    "license_version": "",
                    "source": "internet_archive",
                    "duration_ms": 0,
                    "url": u,
                    "foreign_landing_url": f"https://archive.org/details/{ident}"
                })
        return out
    except Exception as e:
        print(f"[AUDIO_ENGINE] Archive.org audio notice for '{query}': {e}", file=sys.stderr)
        return []


def search_freesound_v2(query, limit=4):
    """Optional Freesound.org API v2 search (active automatically if FREESOUND_API_KEY env var is set)."""
    api_key = os.environ.get("FREESOUND_API_KEY", "").strip()
    if not api_key:
        return []
    try:
        url = "https://freesound.org/apiv2/search/text/?" + urllib.parse.urlencode({
            "query": query,
            "fields": "id,name,username,license,duration,previews,url",
            "page_size": str(limit),
            "token": api_key
        })
        data = _http_get_json(url)
        out = []
        for item in data.get("results", []):
            prev = item.get("previews") or {}
            u = prev.get("preview-hq-mp3") or prev.get("preview-lq-mp3")
            if u:
                out.append({
                    "id": str(item.get("id", "")),
                    "title": item.get("name") or query,
                    "creator": item.get("username") or "Freesound",
                    "license": item.get("license") or "cc",
                    "license_version": "",
                    "source": "freesound_v2",
                    "duration_ms": int((item.get("duration") or 0) * 1000),
                    "url": u,
                    "foreign_landing_url": item.get("url") or u
                })
        return out
    except Exception as e:
        print(f"[AUDIO_ENGINE] Freesound v2 notice for '{query}': {e}", file=sys.stderr)
        return []


def search_multi_source_audio(query, category=None, sources="all", page_size=8, max_duration_ms=None):
    """Round-robin multi-source audio search across Openverse, YouTube (yt-dlp), Freesound v2, Wikimedia Commons, and Internet Archive."""
    enabled = (
        {"openverse", "youtube", "wikimedia", "archive", "freesound"}
        if sources == "all"
        else {s.strip().lower() for s in sources.split(",")}
    )
    buckets = []
    if "freesound" in enabled and os.environ.get("FREESOUND_API_KEY"):
        buckets.append(search_freesound_v2(query, limit=min(4, page_size)))
    if "openverse" in enabled:
        buckets.append(search_openverse_audio(query, category=category, page_size=page_size, max_duration_ms=max_duration_ms))
    if "youtube" in enabled:
        max_s = int(max_duration_ms / 1000) if max_duration_ms else 25
        buckets.append(search_youtube_audio(query, category=category, limit=min(4, page_size), max_duration_s=max_s))
    if "wikimedia" in enabled:
        buckets.append(search_wikimedia_audio(query, limit=min(4, page_size)))
    if "archive" in enabled:
        buckets.append(search_archive_audio(query, limit=min(3, page_size)))

    merged = []
    max_len = max((len(b) for b in buckets), default=0)
    for i in range(max_len):
        for b in buckets:
            if i < len(b):
                merged.append(b[i])
    return merged


def download_and_normalize_wav(url, out_wav, max_seconds=None):
    """Download remote audio or YouTube clip and normalize to 48 kHz stereo PCM WAV using ffmpeg."""
    os.makedirs(os.path.dirname(os.path.abspath(out_wav)), exist_ok=True)
    tmp_raw = out_wav + ".download"

    is_yt = ("youtube.com" in url.lower()) or ("youtu.be" in url.lower())
    if is_yt:
        ytdlp = shutil.which("yt-dlp")
        if not ytdlp:
            print("[AUDIO_ENGINE] yt-dlp not installed; cannot download YouTube URL.", file=sys.stderr)
            return False
        tmp_tpl = out_wav + ".yt.%(ext)s"
        yt_cmd = [
            ytdlp, "--no-playlist", "--no-warnings", "--max-filesize", "25M",
            "-x", "--audio-format", "wav", "-o", tmp_tpl, url
        ]
        yt_res = subprocess.run(yt_cmd, capture_output=True, text=True, timeout=60)
        cand = out_wav + ".yt.wav"
        if yt_res.returncode != 0 or not os.path.exists(cand):
            print(f"[AUDIO_ENGINE] yt-dlp download failed ({url}): {yt_res.stderr}", file=sys.stderr)
            return False
        tmp_raw = cand
    else:
        req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
        try:
            with urllib.request.urlopen(req, timeout=30) as resp, open(tmp_raw, "wb") as f:
                f.write(resp.read())
        except Exception as e:
            print(f"[AUDIO_ENGINE] Download failed ({url}): {e}", file=sys.stderr)
            return False

    cmd = ["ffmpeg", "-y", "-v", "error", "-i", tmp_raw]
    if max_seconds:
        cmd.extend(["-t", str(max_seconds)])
    cmd.extend(["-ar", "48000", "-ac", "2", "-c:a", "pcm_s16le", out_wav])

    res = subprocess.run(cmd, capture_output=True, text=True)
    if os.path.exists(tmp_raw):
        try:
            os.remove(tmp_raw)
        except OSError:
            pass

    if res.returncode != 0 or not os.path.exists(out_wav) or os.path.getsize(out_wav) < 1024:
        print(f"[AUDIO_ENGINE] ffmpeg conversion failed for {url}: {res.stderr}", file=sys.stderr)
        return False

    return True


def fetch_sfx_pack(kinds, out_dir, music_query=None, sources="all", extra_urls=None):
    """
    Fetch real free documentary SFX + music beds on demand from YouTube & public CC sources.
    Writes normalized 48 kHz WAVs into `out_dir` and records attribution in `openverse_attribution.json`.
    """
    os.makedirs(out_dir, exist_ok=True)
    attributions = []
    fetched = {}

    if extra_urls:
        for idx, u in enumerate(extra_urls, 1):
            out_wav = os.path.join(out_dir, f"custom_audio_{idx}.wav")
            if download_and_normalize_wav(u, out_wav):
                fetched[f"custom_audio_{idx}"] = out_wav
                attributions.append({"role": f"custom:{idx}", "title": f"custom_audio_{idx}", "url": u, "source": "direct_url"})
                print(f"  -> Ready: custom_audio_{idx}.wav (from direct URL)")

    for kind in kinds:
        query = DEFAULT_SFX_QUERIES.get(kind, kind)
        max_ms = 12000 if kind not in ("riser", "typing", "drone_dark", "clock_tick") else 22000
        print(f"[AUDIO_ENGINE] Searching YouTube + free internet SFX ({sources}) for '{kind}' ('{query}')...")
        candidates = search_multi_source_audio(query, category=None, sources=sources, max_duration_ms=max_ms)

        out_wav = os.path.join(out_dir, f"{kind}.wav")
        ok = False
        for c in candidates[:6]:
            if download_and_normalize_wav(c["url"], out_wav, max_seconds=10):
                fetched[kind] = out_wav
                attributions.append({"role": f"sfx:{kind}", **c})
                print(f"  -> Ready: {kind}.wav ({c['source']} / {c['license']} by {c['creator']})")
                ok = True
                break
        if not ok:
            print(f"  -> Warning: Could not download playable SFX for '{kind}'")

    if music_query:
        print(f"[AUDIO_ENGINE] Searching music/underscore ({sources}): '{music_query}'...")
        candidates = search_multi_source_audio(music_query, category="music", sources=sources)
        music_wav = os.path.join(out_dir, "music_bed.wav")
        for c in candidates[:6]:
            if download_and_normalize_wav(c["url"], music_wav):
                fetched["music_bed"] = music_wav
                attributions.append({"role": "music_bed", **c})
                print(f"  -> Ready: music_bed.wav ({c['source']} / {c['license']} by {c['creator']})")
                break

    attr_path = os.path.join(out_dir, "openverse_attribution.json")
    with open(attr_path, "w", encoding="utf-8") as f:
        json.dump(attributions, f, indent=2, ensure_ascii=False)

    print(f"[AUDIO_ENGINE] Attribution log saved -> {attr_path}")
    return fetched, attributions


def main():
    parser = argparse.ArgumentParser(description="YouTube & Multi-Source Free Documentary SFX & Music Engine")
    parser.add_argument("--search", type=str, help="Search audio across YouTube + Openverse + Wikimedia + Archive")
    parser.add_argument("--sfx", type=str, help="Comma-separated SFX cues/queries to fetch (e.g. whoosh,paper,stamp,typing)")
    parser.add_argument("--music", type=str, help="Ambient music / tension bed search query")
    parser.add_argument("--sources", type=str, default="all", help="all or comma list: youtube,openverse,wikimedia,archive,freesound")
    parser.add_argument("--from-urls", type=str, default="", help="Comma-separated direct YouTube/Mixkit/Zapsplat/audio URLs from research")
    parser.add_argument("--category", type=str, default="all", help="Category (all, sound_effects, music)")
    parser.add_argument("--out", type=str, default="sound", help="Output directory for normalized 48kHz WAV files")
    args = parser.parse_args()

    if args.search:
        cat = None if args.category == "all" else args.category
        res = search_multi_source_audio(args.search, category=cat, sources=args.sources, page_size=10)
        print(json.dumps(res, indent=2, ensure_ascii=False))
        return

    kinds = [k.strip() for k in (args.sfx or "").split(",") if k.strip()]
    urls = [u.strip() for u in (args.from_urls or "").split(",") if u.strip()]
    if not kinds and not args.music and not urls:
        parser.print_help()
        return

    fetch_sfx_pack(kinds, args.out, music_query=args.music, sources=args.sources, extra_urls=urls)


if __name__ == "__main__":
    main()
