#!/usr/bin/env python3
"""
Documentary 3D by Ashu Dalal (Version 3) - Real CC0 / Open 3D Model (.glb / .gltf) Fetcher
Searches and downloads verified real 3D geometry for gap scenes when primitive shapes are not enough:
  1. Poly Haven Public 3D Models API (500+ CC0 photogrammetry & studio props with 1k/2k glTF + .bin + textures)
  2. Direct --from-urls (.glb or .gltf from Sketchfab CC0/CC-BY, NASA 3D, Smithsonian 3D, Kenney, Quaternius)

Validates glTF JSON / glb binary magic header (b'glTF') and writes models_manifest.json for combo_film.js & 3d-animator.
"""

import os
import sys
import json
import re
import urllib.request
import urllib.parse
import argparse

USER_AGENT = "Documentary3D-AshuDalal/3.0 (CC0 3D Model Client; contact@antigravity.ai)"
POLYHAVEN_ASSETS = "https://api.polyhaven.com/assets?type=models"
POLYHAVEN_FILES = "https://api.polyhaven.com/files/{asset_id}"


def _http_get_json(url, timeout=25):
    req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT, "Accept": "application/json"})
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        return json.loads(resp.read().decode("utf-8"))


def _download_binary(url, dest_path, timeout=45):
    os.makedirs(os.path.dirname(os.path.abspath(dest_path)), exist_ok=True)
    req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    with urllib.request.urlopen(req, timeout=timeout) as resp, open(dest_path, "wb") as f:
        f.write(resp.read())
    return dest_path


def search_polyhaven_models(query, limit=5):
    """Search Poly Haven's CC0 3D model catalog by matching id, name, categories, and tags."""
    try:
        catalog = _http_get_json(POLYHAVEN_ASSETS)
    except Exception as e:
        print(f"[MODEL_FETCHER] Poly Haven API error: {e}", file=sys.stderr)
        return []

    tokens = [t.lower() for t in re.split(r"[^a-zA-Z0-9]+", query) if len(t) >= 2]
    scored = []
    for asset_id, meta in catalog.items():
        hay_id = asset_id.lower()
        name = str(meta.get("name", "")).lower()
        cats = [str(c).lower() for c in meta.get("categories", [])]
        tags = [str(t).lower() for t in meta.get("tags", [])]
        blob = " ".join([hay_id, name] + cats + tags)

        score = 0
        for tok in tokens:
            if tok == hay_id or tok in tags:
                score += 4
            elif tok in name or any(tok in c for c in cats):
                score += 3
            elif tok in blob:
                score += 1
        if score > 0:
            scored.append((score, asset_id, meta))

    scored.sort(key=lambda x: (-x[0], -int(x[2].get("download_count", 0))))
    out = []
    for score, asset_id, meta in scored[:limit]:
        out.append({
            "id": asset_id,
            "name": meta.get("name") or asset_id,
            "categories": meta.get("categories", []),
            "tags": meta.get("tags", []),
            "source": "polyhaven",
            "license": "cc0",
            "url": f"https://polyhaven.com/a/{asset_id}",
            "score": score
        })
    return out


def download_polyhaven_gltf(asset_id, dest_dir, resolution="1k"):
    """Download a Poly Haven model's glTF + .bin + textures cleanly into dest_dir/<asset_id>/."""
    try:
        files = _http_get_json(POLYHAVEN_FILES.format(asset_id=urllib.parse.quote(asset_id)))
    except Exception as e:
        print(f"[MODEL_FETCHER] Failed fetching files metadata for '{asset_id}': {e}", file=sys.stderr)
        return None

    gltf_map = files.get("gltf") or {}
    if not gltf_map:
        print(f"[MODEL_FETCHER] No glTF entry for '{asset_id}'", file=sys.stderr)
        return None

    chosen_res = resolution if resolution in gltf_map else next(iter(gltf_map.keys()))
    entry = (gltf_map.get(chosen_res) or {}).get("gltf") or {}
    gltf_url = entry.get("url")
    if not gltf_url:
        return None

    model_folder = os.path.abspath(os.path.join(dest_dir, asset_id))
    os.makedirs(model_folder, exist_ok=True)
    gltf_name = os.path.basename(urllib.parse.urlparse(gltf_url).path) or f"{asset_id}.gltf"
    gltf_path = os.path.join(model_folder, gltf_name)

    try:
        _download_binary(gltf_url, gltf_path)
        with open(gltf_path, encoding="utf-8-sig") as f:
            parsed = json.load(f)
        if "asset" not in parsed:
            raise ValueError("Invalid glTF JSON (missing 'asset' key)")

        includes = entry.get("include") or {}
        for rel_path, inc_meta in includes.items():
            inc_url = (inc_meta or {}).get("url")
            if not inc_url:
                continue
            target_inc = os.path.abspath(os.path.join(model_folder, rel_path))
            if os.path.commonpath([model_folder, target_inc]) != model_folder:
                continue
            _download_binary(inc_url, target_inc)

        size_kb = sum(
            os.path.getsize(os.path.join(dp, fn))
            for dp, _, fns in os.walk(model_folder) for fn in fns
        ) / 1024
        print(f"[MODEL_FETCHER] VERIFIED CC0 3D: {asset_id}/{gltf_name} ({chosen_res}, {len(includes)} deps, {size_kb:.1f} KB)")
        return {
            "id": asset_id,
            "title": asset_id,
            "file": gltf_path,
            "filename": gltf_name,
            "format": "gltf",
            "resolution": chosen_res,
            "source": "polyhaven",
            "license": "cc0",
            "url": f"https://polyhaven.com/a/{asset_id}"
        }
    except Exception as e:
        print(f"[MODEL_FETCHER] Failed downloading Poly Haven glTF '{asset_id}': {e}", file=sys.stderr)
        return None


def download_direct_model(url, dest_dir, stem_hint="custom_model"):
    """Download and validate a direct .glb or .gltf model URL (rejecting HTML/error responses)."""
    os.makedirs(dest_dir, exist_ok=True)
    clean_path = urllib.parse.urlparse(url).path
    ext = os.path.splitext(clean_path)[1].lower()
    if ext not in (".glb", ".gltf"):
        ext = ".glb"
    stem = re.sub(r"[^a-zA-Z0-9_-]", "_", os.path.splitext(os.path.basename(clean_path))[0] or stem_hint)[:48]
    out_path = os.path.join(dest_dir, f"{stem}{ext}")
    if os.path.exists(out_path):
        out_path = os.path.join(dest_dir, f"{stem}_{abs(hash(url)) % 9999}{ext}")

    try:
        _download_binary(url, out_path)
        with open(out_path, "rb") as f:
            raw = f.read(64)
        if ext == ".glb":
            if raw[:4] != b"glTF":
                raise ValueError("Invalid GLB magic header (not a binary glTF file)")
        else:
            with open(out_path, encoding="utf-8-sig") as f:
                parsed = json.load(f)
            if "asset" not in parsed:
                raise ValueError("Invalid glTF JSON")
        size_kb = os.path.getsize(out_path) / 1024
        print(f"[MODEL_FETCHER] VERIFIED Direct 3D: {os.path.basename(out_path)} ({size_kb:.1f} KB)")
        return {
            "id": stem,
            "title": stem,
            "file": out_path,
            "filename": os.path.basename(out_path),
            "format": ext.lstrip("."),
            "source": "direct_url",
            "license": "verify_source_license",
            "url": url
        }
    except Exception as e:
        print(f"[MODEL_FETCHER] Rejected direct model ({url}): {e}", file=sys.stderr)
        if os.path.exists(out_path):
            try:
                os.remove(out_path)
            except OSError:
                pass
        return None


def fetch_models_for_topic(queries, dest_dir, max_models=3, resolution="1k", extra_urls=None, alias_tags=None):
    """Download CC0 Poly Haven models and/or direct .glb/.gltf URLs and save models_manifest.json."""
    os.makedirs(dest_dir, exist_ok=True)
    q_list = [q.strip() for q in queries.split(",") if q.strip()] if isinstance(queries, str) else list(queries)
    downloaded = []
    seen_ids = set()

    if extra_urls:
        for i, u in enumerate(extra_urls, 1):
            if len(downloaded) >= max_models:
                break
            ver = download_direct_model(u, dest_dir, stem_hint=f"web_model_{i}")
            if ver:
                ver["tags"] = sorted(set([t.lower() for t in (alias_tags or [])] + [q.lower() for q in q_list]))
                downloaded.append(ver)

    for q in q_list:
        if len(downloaded) >= max_models:
            break
        matches = search_polyhaven_models(q, limit=max_models)
        for m in matches:
            if len(downloaded) >= max_models or m["id"] in seen_ids:
                continue
            seen_ids.add(m["id"])
            ver = download_polyhaven_gltf(m["id"], dest_dir, resolution=resolution)
            if ver:
                ver["tags"] = sorted(set([t.lower() for t in (alias_tags or [])] + [t.lower() for t in m.get("tags", [])] + [q.lower()]))
                downloaded.append(ver)

    manifest = os.path.join(dest_dir, "models_manifest.json")
    with open(manifest, "w", encoding="utf-8") as f:
        json.dump(downloaded, f, indent=2, ensure_ascii=False)
    print(f"[MODEL_FETCHER] Saved {len(downloaded)} verified 3D model(s) -> {dest_dir}")
    return downloaded


def main():
    parser = argparse.ArgumentParser(description="CC0 / Open 3D Model (.glb/.gltf) Fetcher for Documentary 3D")
    parser.add_argument("--search", type=str, help="Search Poly Haven CC0 3D models without downloading")
    parser.add_argument("--query", type=str, default="", help="Comma-separated model keywords (e.g. 'camera,desk,lantern')")
    parser.add_argument("--from-urls", type=str, default="", help="Comma-separated direct .glb/.gltf URLs found via internet research")
    parser.add_argument("--out", type=str, default="models", help="Output folder")
    parser.add_argument("--max", type=int, default=3, help="Max models to download")
    parser.add_argument("--res", type=str, default="1k", choices=["1k", "2k", "4k"], help="Texture resolution for Poly Haven models")
    parser.add_argument("--tags", type=str, default="", help="Optional comma-separated tags for manifest mapping")
    args = parser.parse_args()

    if args.search:
        res = search_polyhaven_models(args.search, limit=8)
        print(json.dumps(res, indent=2, ensure_ascii=False))
        return

    urls = [u.strip() for u in (args.from_urls or "").split(",") if u.strip()]
    tags = [t.strip() for t in (args.tags or "").split(",") if t.strip()]
    if not args.query and not urls:
        parser.print_help()
        return

    fetch_models_for_topic(args.query, args.out, max_models=args.max, resolution=args.res, extra_urls=urls, alias_tags=tags)


if __name__ == "__main__":
    main()
