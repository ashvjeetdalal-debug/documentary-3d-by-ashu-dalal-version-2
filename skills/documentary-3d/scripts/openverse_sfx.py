#!/usr/bin/env python3
"""
Documentary 3D by Ashu Dalal (Version 3) - Bundled Documentary SFX + Multi-Source Audio Engine
1. Checks the pre-bundled verified CC0/CC-BY Documentary SFX Pack (`assets/sfx/*.wav`, 23 researched cues) FIRST
   for instant, glitch-free, zero-latency documentary sound design.
2. For custom SFX or music beds (or when --online-only is passed), searches, downloads, normalizes
   (48 kHz stereo WAV via ffmpeg), and logs attributions across:
     - Openverse Audio API (keyless CC0/CC-BY: Freesound previews, Jamendo, Wikimedia)
     - Wikimedia Commons Audio (keyless authentic .ogg/.wav/.mp3 Foley & sirens)
     - Internet Archive Audio (keyless public-domain historical/SFX recordings)
     - Freesound API v2 (auto-enabled when FREESOUND_API_KEY env var is set)
     - Direct --from-urls found during internet research

Replaces synthetic numpy sound generation by default while keeping sound_bed.py / gen_sfx.py preserved & silenced.
"""

import os
import sys
import json
import shutil
import subprocess
import urllib.request
import urllib.parse
import argparse

SCRIPTS_DIR = os.path.dirname(os.path.abspath(__file__))
PLUGIN_ROOT = os.path.abspath(os.path.join(SCRIPTS_DIR, "..", "..", ".."))
BUNDLED_SFX_DIR = os.path.join(PLUGIN_ROOT, "assets", "sfx")
BUNDLED_CATALOG = os.path.join(BUNDLED_SFX_DIR, "sfx_catalog.json")

API_BASE = "https://api.openverse.org/v1/audio/"
USER_AGENT = "Documentary3D-AshuDalal/3.0 (Multi-Source Audio Client; contact@antigravity.ai)"

# Curated search terms derived from investigative/YouTube documentary sound-design research
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
    # Aliases mapped cleanly
    "typing": "typewriter mechanical keys",
    "click": "camera shutter mechanical click",
    "boom": "sub bass drop impact",
    "ding": "typewriter bell ding",
    "pop": "digital interface click blip",
    "footstep": "footsteps concrete corridor"
}

BUNDLED_ALIASES = {
    "typing": "typewriter",
    "click": "shutter",
    "boom": "sub_drop",
    "ding": "typewriter_ding",
    "pop": "ui_click",
    "drone": "drone_dark",
    "music_drone": "drone_dark",
    "vhs": "static_burst",
    "swatch": "paper",
    "highlight": "marker"
}


def load_bundled_catalog():
    if os.path.exists(BUNDLED_CATALOG):
        try:
            with open(BUNDLED_CATALOG, encoding="utf-8-sig") as f:
                return json.load(f)
        except Exception:
            pass
    return []


def list_bundled_sfx():
    cat = load_bundled_catalog()
    print(f"\n=== BUNDLED DOCUMENTARY SFX LIBRARY ({BUNDLED_SFX_DIR}) ===")
    if not cat:
        print("  (No catalog found; run online fetch or check assets/sfx/)")
        return
    for item in cat:
        print(f"  - {item['cue']:16} [{item['category']:10}] ({item['duration_sec']:4.2f}s, {item['license']}) : {item['use']}")
    print("\nAliases supported automatically: typing->typewriter, click->shutter, boom->sub_drop, ding->typewriter_ding, pop->ui_click")
    print("Usage: python studio.py --fetch-sfx='sub_drop,riser,whoosh,paper,typewriter,shutter,stamp' --out=sound\n")


def resolve_bundled_cue(kind):
    norm = BUNDLED_ALIASES.get(kind.lower().strip(), kind.lower().strip())
    cand = os.path.join(BUNDLED_SFX_DIR, f"{norm}.wav")
    if os.path.exists(cand) and os.path.getsize(cand) > 1024:
        return norm, cand
    return None, None


def _http_get_json(url, timeout=25, headers=None):
    hdrs = {"User-Agent": USER_AGENT, "Accept": "application/json"}
    if headers:
        hdrs.update(headers)
    req = urllib.request.Request(url, headers=hdrs)
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        return json.loads(resp.read().decode("utf-8"))


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
        tokens = query.strip().split()
        if not tokens:
            return []
        q_tok = tokens[0]
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
    """Round-robin multi-source audio search across Openverse, Freesound v2, Wikimedia Commons, and Internet Archive."""
    enabled = {"openverse", "wikimedia", "archive", "freesound"} if sources == "all" else {s.strip().lower() for s in sources.split(",")}
    buckets = []
    if "freesound" in enabled and os.environ.get("FREESOUND_API_KEY"):
        buckets.append(search_freesound_v2(query, limit=min(4, page_size)))
    if "openverse" in enabled:
        buckets.append(search_openverse_audio(query, category=category, page_size=page_size, max_duration_ms=max_duration_ms))
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
    """Download remote audio file and normalize to 48 kHz stereo PCM WAV using ffmpeg."""
    os.makedirs(os.path.dirname(os.path.abspath(out_wav)), exist_ok=True)
    tmp_raw = out_wav + ".download"

    req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    try:
        with urllib.request.urlopen(req, timeout=30) as resp, open(tmp_raw, "wb") as f:
            f.write(resp.read())
    except Exception as e:
        print(f"[AUDIO_ENGINE] Download failed ({url}): {e}", file=sys.stderr)
        try:
            os.remove(tmp_raw)
        except OSError:
            pass
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
        print(f"[AUDIO_ENGINE] ffmpeg conversion failed for {url}: {res.stderr}", file=sys.stderr)
        return False

    return True


def fetch_sfx_pack(kinds, out_dir, music_query=None, sources="all", extra_urls=None, online_only=False):
    """
    Resolve documentary SFX cues from pre-bundled CC0 pack first (unless online_only=True),
    then fetch missing/custom cues + music bed from multi-source CC/PD APIs.
    """
    os.makedirs(out_dir, exist_ok=True)
    catalog_by_cue = {item["cue"]: item for item in load_bundled_catalog()}
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
        safe_stem = re.sub(r'[\\/:*?"<>|]+', '_', kind).strip("._ ") or "sfx_cue"
        out_wav = os.path.join(out_dir, f"{safe_stem}.wav")
        if not online_only:
            bundled_key, bundled_path = resolve_bundled_cue(kind)
            if bundled_path:
                shutil.copy2(bundled_path, out_wav)
                fetched[kind] = out_wav
                meta = catalog_by_cue.get(bundled_key, {})
                attributions.append({
                    "role": f"sfx:{kind}",
                    "title": meta.get("title", bundled_key),
                    "creator": meta.get("creator", "Openverse CC0"),
                    "license": meta.get("license", "cc0"),
                    "source": f"bundled:{meta.get('source', 'assets/sfx')}",
                    "url": meta.get("url", bundled_path)
                })
                print(f"  -> Bundled CC0 Ready: {kind}.wav (from assets/sfx/{bundled_key}.wav)")
                continue

        query = DEFAULT_SFX_QUERIES.get(kind, kind)
        max_ms = 12000 if kind not in ("riser", "typing", "typewriter", "projector", "drone_dark") else 20000
        print(f"[AUDIO_ENGINE] Multi-source search ({sources}) for '{kind}' ('{query}')...")
        candidates = search_multi_source_audio(query, category=None, sources=sources, max_duration_ms=max_ms)

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
        print(f"[AUDIO_ENGINE] Multi-source music search: '{music_query}'...")
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
    parser = argparse.ArgumentParser(description="Bundled Documentary SFX + Multi-Source CC/PD Audio Engine")
    parser.add_argument("--list", action="store_true", help="List all 23 pre-bundled CC0 documentary SFX cues")
    parser.add_argument("--search", type=str, help="Search multi-source audio and print matches without downloading")
    parser.add_argument("--sfx", type=str, help="Comma-separated SFX cues/queries to fetch (e.g. sub_drop,riser,whoosh,paper,typewriter,shutter,stamp)")
    parser.add_argument("--music", type=str, help="Ambient music / tension bed search query")
    parser.add_argument("--sources", type=str, default="all", help="all or comma list: openverse,wikimedia,archive,freesound")
    parser.add_argument("--from-urls", type=str, default="", help="Comma-separated direct audio URLs from research")
    parser.add_argument("--online-only", action="store_true", help="Bypass bundled assets/sfx/ and fetch fresh from online APIs")
    parser.add_argument("--category", type=str, default="all", help="Openverse category (all, sound_effects, music)")
    parser.add_argument("--out", type=str, default="sound", help="Output directory for normalized 48kHz WAV files")
    args = parser.parse_args()

    if args.list:
        list_bundled_sfx()
        return

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

    fetch_sfx_pack(kinds, args.out, music_query=args.music, sources=args.sources, extra_urls=urls, online_only=args.online_only)


if __name__ == "__main__":
    main()
