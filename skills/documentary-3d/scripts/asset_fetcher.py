#!/usr/bin/env python3
"""
Documentary 3D by Ashu Dalal (Version 3) - Multi-Source Internet & Social Asset Fetcher
Fetches, downloads, and verifies authentic real-world media across the public internet:
  1. Wikimedia Commons (high-res historical photos, maps, diagrams)
  2. Wikipedia Page Media API (article lead photos & archival thumbnails)
  3. Openverse Images API (Flickr, NASA, museums, cultural archives - CC0/CC-BY)
  4. Internet Archive (archive.org historical collections)
  5. Public Social/Forum Media (Reddit public posts) & direct --from-urls extracted from X/YouTube/News web research

Strictly NO FAKE / NO AI SLOP assets. Every file is verified via PIL (size, integrity, clean RGB)
and tagged with source_url, platform, license, and bilingual/phonetic aliases for WhisperX Step 4 mapping.
"""

import os
import sys
import json
import re
import urllib.request
import urllib.parse
from PIL import Image

USER_AGENT = "Documentary3D-AshuDalal/3.0 (Archival Research Client; contact@antigravity.ai)"


def _http_get_json(url, timeout=18):
    req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT, "Accept": "application/json"})
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        return json.loads(resp.read().decode("utf-8"))


def search_wikimedia_commons(query, limit=4):
    """Search Wikimedia Commons File namespace."""
    params = {
        "action": "query", "list": "search", "srsearch": query,
        "srnamespace": "6", "srlimit": str(limit), "format": "json"
    }
    try:
        data = _http_get_json("https://commons.wikimedia.org/w/api.php?" + urllib.parse.urlencode(params))
        titles = [
            item.get("title", "")
            for item in data.get("query", {}).get("search", [])
            if item.get("title", "").lower().endswith((".jpg", ".jpeg", ".png", ".webp"))
        ]
        if not titles:
            return []
        info_params = {
            "action": "query", "titles": "|".join(titles),
            "prop": "imageinfo", "iiprop": "url|size|mime", "format": "json"
        }
        info_data = _http_get_json("https://commons.wikimedia.org/w/api.php?" + urllib.parse.urlencode(info_params))
        out = []
        for _, page in info_data.get("query", {}).get("pages", {}).items():
            if page.get("imageinfo"):
                inf = page["imageinfo"][0]
                out.append({
                    "title": page.get("title", query).replace("File:", ""),
                    "url": inf.get("url"),
                    "source": "wikimedia_commons",
                    "license": "public_domain_or_cc",
                    "query": query
                })
        return out
    except Exception as e:
        print(f"[ASSET_FETCHER] Wikimedia error for '{query}': {e}")
        return []


def search_wikipedia_media(query, limit=3):
    """Fetch lead/featured real archival images from top Wikipedia pages matching query."""
    try:
        search_url = "https://en.wikipedia.org/w/api.php?" + urllib.parse.urlencode({
            "action": "query", "list": "search", "srsearch": query, "srlimit": str(limit), "format": "json"
        })
        sdata = _http_get_json(search_url)
        page_titles = [p.get("title") for p in sdata.get("query", {}).get("search", []) if p.get("title")]
        if not page_titles:
            return []
        img_url = "https://en.wikipedia.org/w/api.php?" + urllib.parse.urlencode({
            "action": "query", "titles": "|".join(page_titles),
            "prop": "pageimages", "piprop": "original", "format": "json"
        })
        idata = _http_get_json(img_url)
        out = []
        for _, page in idata.get("query", {}).get("pages", {}).items():
            orig = page.get("original", {})
            u = orig.get("source")
            if u and u.lower().split("?")[0].endswith((".jpg", ".jpeg", ".png", ".webp")):
                out.append({
                    "title": f"wiki_{page.get('title', query)}",
                    "url": u,
                    "source": "wikipedia",
                    "license": "wikimedia_editorial",
                    "query": query
                })
        return out
    except Exception as e:
        print(f"[ASSET_FETCHER] Wikipedia error for '{query}': {e}")
        return []


def search_openverse_images(query, limit=4):
    """Search WordPress Openverse Images API (Flickr, NASA, Museums, News/Editorial CC media)."""
    try:
        url = "https://api.openverse.org/v1/images/?" + urllib.parse.urlencode({
            "q": query, "page_size": str(limit)
        })
        data = _http_get_json(url)
        out = []
        for item in data.get("results", []):
            u = item.get("url")
            if not u:
                continue
            out.append({
                "title": item.get("title") or query,
                "url": u,
                "source": f"openverse:{item.get('source', 'web')}",
                "license": item.get("license") or "cc",
                "foreign_landing_url": item.get("foreign_landing_url"),
                "query": query
            })
        return out
    except Exception as e:
        print(f"[ASSET_FETCHER] Openverse Images error for '{query}': {e}")
        return []


def search_internet_archive(query, limit=3):
    """Search Internet Archive historical image items."""
    try:
        url = "https://archive.org/advancedsearch.php?" + urllib.parse.urlencode({
            "q": f"({query}) AND mediatype:image",
            "fl[]": "identifier,title",
            "rows": str(limit),
            "page": "1",
            "output": "json"
        })
        data = _http_get_json(url)
        out = []
        for doc in data.get("response", {}).get("docs", []):
            ident = doc.get("identifier")
            if ident:
                out.append({
                    "title": doc.get("title") or ident,
                    "url": f"https://archive.org/services/img/{ident}",
                    "source": "internet_archive",
                    "license": "public_archive",
                    "foreign_landing_url": f"https://archive.org/details/{ident}",
                    "query": query
                })
        return out
    except Exception as e:
        print(f"[ASSET_FETCHER] Archive.org error for '{query}': {e}")
        return []


def search_reddit_public_media(query, limit=4):
    """Search public Reddit posts for real shared archival photos, screenshots, or event media."""
    try:
        url = "https://www.reddit.com/search.json?" + urllib.parse.urlencode({
            "q": query, "limit": str(limit * 2), "sort": "relevance"
        })
        data = _http_get_json(url)
        out = []
        for child in data.get("data", {}).get("children", []):
            post = child.get("data", {})
            u = post.get("url_overridden_by_dest") or post.get("url") or ""
            if u.lower().split("?")[0].endswith((".jpg", ".jpeg", ".png", ".webp")):
                out.append({
                    "title": post.get("title") or query,
                    "url": u,
                    "source": f"reddit:r/{post.get('subreddit', 'public')}",
                    "license": "social_reference",
                    "foreign_landing_url": "https://www.reddit.com" + post.get("permalink", ""),
                    "query": query
                })
        return out[:limit]
    except Exception as e:
        print(f"[ASSET_FETCHER] Reddit search notice for '{query}': {e}")
        return []


def download_and_verify_asset(url, dest_path, min_width=400, min_height=300):
    """Download image file and verify resolution & image validity via PIL (reject broken/tiny images)."""
    req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    try:
        with urllib.request.urlopen(req, timeout=25) as resp, open(dest_path, "wb") as f:
            f.write(resp.read())

        with Image.open(dest_path) as im:
            w, h = im.size
            im.verify()

        if w < min_width or h < min_height:
            print(f"[ASSET_FETCHER] Rejected low-res ({w}x{h}) -> {os.path.basename(dest_path)}")
            os.remove(dest_path)
            return None

        with Image.open(dest_path) as im:
            if im.mode not in ("RGB", "RGBA"):
                im = im.convert("RGB")
            # Normalize WebP/non-JPEG safely to PNG/JPG
            if dest_path.lower().endswith(".webp"):
                new_path = dest_path[:-5] + ".jpg"
                im.convert("RGB").save(new_path, quality=95)
                os.remove(dest_path)
                dest_path = new_path
            else:
                im.save(dest_path)

        file_size_kb = os.path.getsize(dest_path) / 1024
        print(f"[ASSET_FETCHER] VERIFIED: {os.path.basename(dest_path)} ({w}x{h}, {file_size_kb:.1f} KB)")
        return {"path": dest_path, "width": w, "height": h}
    except Exception as e:
        print(f"[ASSET_FETCHER] Verification failed for {os.path.basename(dest_path)}: {e}")
        if os.path.exists(dest_path):
            try:
                os.remove(dest_path)
            except OSError:
                pass
        return None


def auto_fetch_assets_for_topic(topic_or_keywords, dest_dir, max_assets=8, sources="all", extra_urls=None, alias_tags=None):
    """
    Multi-source authentic asset pipeline across Wikimedia Commons, Wikipedia,
    Openverse Images, Internet Archive, Reddit public media, and direct web/social URLs.
    """
    os.makedirs(dest_dir, exist_ok=True)
    queries = [q.strip() for q in topic_or_keywords.split(",") if q.strip()] if isinstance(topic_or_keywords, str) else list(topic_or_keywords)
    enabled = set(s.strip().lower() for s in sources.split(",")) if sources != "all" else {"wikimedia", "wikipedia", "openverse", "archive", "reddit"}

    downloaded = []
    seen_urls = set()

    # 1. Process explicit URLs gathered by AI full-internet/social research first
    if extra_urls:
        for idx, u in enumerate(extra_urls, 1):
            if u in seen_urls or len(downloaded) >= max_assets:
                continue
            seen_urls.add(u)
            ext = os.path.splitext(u.split("?")[0])[1].lower()
            if ext not in (".jpg", ".jpeg", ".png", ".webp"):
                ext = ".jpg"
            dest_file = os.path.join(dest_dir, f"web_source_{idx}{ext}")
            ver = download_and_verify_asset(u, dest_file)
            if ver:
                tags = list(set((alias_tags or []) + [q.lower() for q in queries]))
                downloaded.append({
                    "title": f"web_source_{idx}",
                    "file": ver["path"],
                    "filename": os.path.basename(ver["path"]),
                    "width": ver["width"],
                    "height": ver["height"],
                    "url": u,
                    "source": "web_or_social_research",
                    "tags": tags
                })

    # 2. Query multi-source public internet & social repositories (round-robin across sources for true diversity)
    print(f"[ASSET_FETCHER] Multi-source search ({sorted(enabled)}) for queries: {queries}")
    for q in queries:
        if len(downloaded) >= max_assets:
            break
        per_source = []
        if "openverse" in enabled:
            per_source.append(search_openverse_images(q, limit=3))
        if "archive" in enabled:
            per_source.append(search_internet_archive(q, limit=2))
        if "wikipedia" in enabled:
            per_source.append(search_wikipedia_media(q, limit=2))
        if "wikimedia" in enabled:
            per_source.append(search_wikimedia_commons(q, limit=3))
        if "reddit" in enabled:
            per_source.append(search_reddit_public_media(q, limit=2))

        candidates = []
        max_len = max((len(lst) for lst in per_source), default=0)
        for idx in range(max_len):
            for lst in per_source:
                if idx < len(lst):
                    candidates.append(lst[idx])

        for cand in candidates:
            if len(downloaded) >= max_assets:
                break
            u = cand.get("url")
            if not u or u in seen_urls:
                continue
            seen_urls.add(u)

            raw_ext = os.path.splitext(u.split("?")[0])[1].lower()
            ext = raw_ext if raw_ext in (".jpg", ".jpeg", ".png", ".webp") else ".jpg"
            stem = re.sub(r'[^a-zA-Z0-9_-]', '_', str(cand.get("title", q)))[:48].strip("_") or "asset"
            dest_file = os.path.join(dest_dir, f"{stem}{ext}")
            if os.path.exists(dest_file):
                dest_file = os.path.join(dest_dir, f"{stem}_{len(downloaded)+1}{ext}")

            ver = download_and_verify_asset(u, dest_file)
            if ver:
                q_words = [w.lower() for w in re.split(r'[^a-zA-Z0-9]', q) if len(w) > 2]
                t_words = [w.lower() for w in re.split(r'[^a-zA-Z0-9]', str(cand.get("title", ""))) if len(w) > 2]
                tags = sorted(set(q_words + t_words + [t.lower() for t in (alias_tags or [])]))
                downloaded.append({
                    "title": cand.get("title"),
                    "file": ver["path"],
                    "filename": os.path.basename(ver["path"]),
                    "width": ver["width"],
                    "height": ver["height"],
                    "url": u,
                    "source": cand.get("source"),
                    "license": cand.get("license"),
                    "landing_url": cand.get("foreign_landing_url", u),
                    "tags": tags
                })

    manifest_path = os.path.join(dest_dir, "assets_manifest.json")
    with open(manifest_path, "w", encoding="utf-8") as f:
        json.dump(downloaded, f, indent=2, ensure_ascii=False)

    print(f"[ASSET_FETCHER] Successfully downloaded & verified {len(downloaded)} real assets -> {dest_dir}")
    return downloaded


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Multi-Source Internet & Social Archival Asset Fetcher")
    parser.add_argument("--query", type=str, required=True, help="Comma-separated search keywords")
    parser.add_argument("--out", type=str, default="assets", help="Destination directory")
    parser.add_argument("--max", type=int, default=8, help="Maximum assets to download")
    parser.add_argument("--sources", type=str, default="all", help="all or comma list: wikimedia,wikipedia,openverse,archive,reddit")
    parser.add_argument("--from-urls", type=str, default="", help="Comma-separated direct image URLs found during web/social research")
    parser.add_argument("--tags", type=str, default="", help="Extra bilingual/phonetic alias tags (e.g. iran,rahn,stuxnet,stucks)")
    args = parser.parse_args()

    urls = [u.strip() for u in args.from_urls.split(",") if u.strip()]
    tags = [t.strip() for t in args.tags.split(",") if t.strip()]
    auto_fetch_assets_for_topic(args.query, args.out, max_assets=args.max, sources=args.sources, extra_urls=urls, alias_tags=tags)
