#!/usr/bin/env python3
"""
Documentary 3D by Ashu Dalal - Automated Archival Asset Fetcher
Automatically fetches, downloads, and verifies real historical assets from public archives
(Wikimedia Commons, Wikipedia) when assets are not explicitly provided by the user.
"""

import os
import sys
import json
import re
import urllib.request
import urllib.parse
from PIL import Image

USER_AGENT = "AntigravityDocuBot/2.0 (Historical Documentary Production; contact@antigravity.ai)"

def search_wikimedia_commons(query, limit=5):
    """Search Wikimedia Commons for authentic media matching query."""
    params = {
        "action": "query",
        "list": "search",
        "srsearch": query,
        "srnamespace": "6", # File namespace
        "srlimit": str(limit),
        "format": "json"
    }
    url = "https://commons.wikimedia.org/w/api.php?" + urllib.parse.urlencode(params)
    req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    try:
        with urllib.request.urlopen(req, timeout=15) as resp:
            data = json.loads(resp.read().decode("utf-8"))
            results = []
            for item in data.get("query", {}).get("search", []):
                title = item.get("title", "")
                if title.lower().endswith((".jpg", ".jpeg", ".png")):
                    results.append(title)
            return results
    except Exception as e:
        print(f"[ASSET_FETCHER] Error searching Commons for '{query}': {e}")
        return []

def get_image_direct_url(file_title):
    """Retrieve direct high-resolution file URL and metadata from Commons."""
    params = {
        "action": "query",
        "titles": file_title,
        "prop": "imageinfo",
        "iiprop": "url|size|mime",
        "format": "json"
    }
    url = "https://commons.wikimedia.org/w/api.php?" + urllib.parse.urlencode(params)
    req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    try:
        with urllib.request.urlopen(req, timeout=15) as resp:
            data = json.loads(resp.read().decode("utf-8"))
            pages = data.get("query", {}).get("pages", {})
            for pid, page in pages.items():
                if "imageinfo" in page and len(page["imageinfo"]) > 0:
                    info = page["imageinfo"][0]
                    return {
                        "url": info.get("url"),
                        "width": info.get("width"),
                        "height": info.get("height"),
                        "mime": info.get("mime")
                    }
    except Exception as e:
        print(f"[ASSET_FETCHER] Error fetching info for '{file_title}': {e}")
    return None

def download_and_verify_asset(url, dest_path, min_width=400, min_height=300):
    """Download image file and verify resolution & image validity with PIL."""
    req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    try:
        with urllib.request.urlopen(req, timeout=25) as resp, open(dest_path, "wb") as f:
            f.write(resp.read())

        # Verify with PIL
        with Image.open(dest_path) as im:
            w, h = im.size
            if w < min_width or h < min_height:
                print(f"[ASSET_FETCHER] Warning: {os.path.basename(dest_path)} below recommended resolution ({w}x{h})")
            # Verify clean RGB
            im.verify()

        # Re-open and convert to clean RGB if needed
        with Image.open(dest_path) as im:
            if im.mode not in ("RGB", "RGBA"):
                im.convert("RGB").save(dest_path, quality=95)

        file_size_kb = os.path.getsize(dest_path) / 1024
        print(f"[ASSET_FETCHER] VERIFIED: {os.path.basename(dest_path)} ({w}x{h}, {file_size_kb:.1f} KB)")
        return True
    except Exception as e:
        print(f"[ASSET_FETCHER] Verification failed for {dest_path}: {e}")
        if os.path.exists(dest_path):
            try:
                os.remove(dest_path)
            except:
                pass
        return False

def auto_fetch_assets_for_topic(topic_or_keywords, dest_dir, max_assets=6):
    """Main automated pipeline: takes topic or list of keywords and populates dest_dir."""
    os.makedirs(dest_dir, exist_ok=True)
    if isinstance(topic_or_keywords, str):
        queries = [q.strip() for q in topic_or_keywords.split(",") if q.strip()]
    else:
        queries = topic_or_keywords

    downloaded = []
    print(f"[ASSET_FETCHER] Auto-sourcing historical archival assets for queries: {queries}")

    seen_titles = set()
    for q in queries:
        if len(downloaded) >= max_assets:
            break
        titles = search_wikimedia_commons(q, limit=4)
        for title in titles:
            if title in seen_titles:
                continue
            seen_titles.add(title)
            info = get_image_direct_url(title)
            if not info or not info.get("url"):
                continue

            clean_name = re.sub(r'[^a-zA-Z0-9_\.-]', '_', title.replace("File:", ""))
            dest_file = os.path.join(dest_dir, clean_name)

            if download_and_verify_asset(info["url"], dest_file):
                downloaded.append({
                    "title": title,
                    "file": dest_file,
                    "filename": clean_name,
                    "width": info.get("width"),
                    "height": info.get("height"),
                    "url": info.get("url")
                })
                if len(downloaded) >= max_assets:
                    break

    manifest_path = os.path.join(dest_dir, "assets_manifest.json")
    with open(manifest_path, "w", encoding="utf-8") as f:
        json.dump(downloaded, f, indent=2)

    print(f"[ASSET_FETCHER] Successfully downloaded and verified {len(downloaded)} authentic assets -> {dest_dir}")
    return downloaded

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Automated Archival Asset Fetcher")
    parser.add_argument("--query", type=str, required=True, help="Topic keywords (comma-separated)")
    parser.add_argument("--out", type=str, default="assets", help="Destination directory")
    parser.add_argument("--max", type=int, default=5, help="Maximum assets to download")
    args = parser.parse_args()

    auto_fetch_assets_for_topic(args.query, args.out, max_assets=args.max)
