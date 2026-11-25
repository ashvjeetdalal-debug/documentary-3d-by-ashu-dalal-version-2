#!/usr/bin/env python3
"""
Documentary 3D by Ashu Dalal - Unified Director Workflow Engine
Implements the Master 5-Step Production System:
  Step 1: Topic & Idea Selection -> Documentary Script Generation
  Step 2: Voiceover Audio Intake (User Upload or Generation)
  Step 3: Zero-Fake Archival Asset Sourcing (Wikimedia Commons / Wikipedia)
  Step 4: WhisperX Word-Level Transcript Alignment & Asset Timeline Mapping
  Step 5 & 5(1): Gap Analysis & Interactive Visual Selection (Lemo-Opuscar, p5.brush, 3D-Animator)
"""

import os
import sys
import json
import re
import argparse
from typing import List, Dict, Any

SCRIPTS_DIR = os.path.dirname(os.path.abspath(__file__))
PLUGIN_ROOT = os.path.abspath(os.path.join(SCRIPTS_DIR, "..", "..", ".."))

# Import sibling modules
sys.path.insert(0, SCRIPTS_DIR)
try:
    import asset_fetcher
    import audio_sync
except ImportError:
    pass

# Curated Style Catalogs for Step 5(1)
LEMO_STYLES_DIR = os.path.join(PLUGIN_ROOT, "skills", "lemo-opuscar", "styles")

STYLES_3D = [
    {"name": "lit", "desc": "Photorealistic PBR materials with soft studio shadows and depth-of-field"},
    {"name": "clay", "desc": "Tactile monochrome matte clay sculpture aesthetic with ambient occlusion"},
    {"name": "blueprint", "desc": "Technical engineering schematic with cyan glowing lines on dark navy grid"},
    {"name": "paper", "desc": "Origami folded paper craft with delicate physical creases and fibrous texture"},
    {"name": "shadow", "desc": "High-contrast film noir chiaroscuro with silhouette geometry"},
    {"name": "toon", "desc": "Cell-shaded graphic novel aesthetic with ink contour outlines"},
    {"name": "synth", "desc": "Retro 1980s neon wireframe grid with scanlines and atmospheric haze"},
    {"name": "chrome", "desc": "Highly reflective metallic mirrored liquid mercury look"},
    {"name": "voxel", "desc": "Volumetric digital voxel cubes building up the subject block by block"},
    {"name": "thermal", "desc": "Infrared thermal surveillance heat-signature color mapping"},
    {"name": "neon", "desc": "Cyberpunk high-intensity glowing tube lighting in pure darkness"},
    {"name": "mix", "desc": "Multi-pass layered aesthetic combining wireframe contours with clay volume"}
]

BRUSH_MEDIA = [
    {"name": "charcoal", "desc": "Expressive rough charcoal silhouette sketches with smudge gradients"},
    {"name": "watercolor", "desc": "Wet-in-wet watercolor washes with organic pigment bleeding and granulation"},
    {"name": "pencil_hb", "desc": "Delicate technical graphite pencil line art on archival paper"},
    {"name": "hatching", "desc": "Architectural cross-hatching and contour shading using rotring pens"},
    {"name": "marker", "desc": "Bold semi-transparent felt marker overlays for highlighting and diagrams"},
    {"name": "flow_field", "desc": "Generative vector flow fields guiding organic directional strokes"}
]

def get_lemo_styles(limit=15) -> List[Dict[str, str]]:
    """Retrieve available Lemo-Opuscar film styles from library."""
    if not os.path.exists(LEMO_STYLES_DIR):
        return []
    all_styles = [s for s in sorted(os.listdir(LEMO_STYLES_DIR)) if os.path.isdir(os.path.join(LEMO_STYLES_DIR, s)) and not s.startswith(('_', '.'))]
    # Curated selection of top documentary and explainer styles
    curated = [
        "dark-documentary", "archive-lighttable", "briefing-board", "blueprint",
        "circuit-board", "comic-history", "halftone-dossier", "woodcut",
        "watercolor", "ink-wash", "colored-pencil", "thermal-camera",
        "text-flash-cuts", "silent-film", "chalkboard", "engraving",
        "vintage-collage", "visual-investigation", "map-explainer", "lidar-survey"
    ]
    results = []
    for s in curated:
        if s in all_styles:
            results.append({"name": s, "type": "Lemo-Opuscar Film Style"})
    for s in all_styles:
        if len(results) >= limit:
            break
        if s not in [r["name"] for r in results]:
            results.append({"name": s, "type": "Lemo-Opuscar Film Style"})
    return results

# -------------------------------------------------------------
# STEP 1: TOPIC & SCRIPT FORMULATION
# -------------------------------------------------------------
def suggest_documentary_topics() -> List[Dict[str, str]]:
    return [
        {
            "id": "stuxnet",
            "title": "Operation Olympic Games (Stuxnet)",
            "logline": "The world's first true cyber weapon: how 500 KB of code physically tore apart Iran's Natanz centrifuges without dropping a bomb."
        },
        {
            "id": "sr71_blackbird",
            "title": "Project Oxcart & The SR-71 Blackbird",
            "logline": "Titanium secretly bought from the USSR to build an aircraft that flew at Mach 3.2 on the edge of space."
        },
        {
            "id": "operation_mincemeat",
            "title": "Operation Mincemeat (1943)",
            "logline": "How British intelligence used a dead tramp and a fake briefcase to deceive Hitler about the invasion of Sicily."
        },
        {
            "id": "apollo_guidance",
            "title": "The Moon Rope Memory (Apollo Guidance Computer)",
            "logline": "How female textile workers literally wove software into copper wire cores to guide humanity to the Moon in 1969."
        },
        {
            "id": "vault_7",
            "title": "Vault 7: The CIA's Cyber Arsenal",
            "logline": "Inside the CIA's secret cyberweapons center in Frankfurt and the software that turned smart TVs into listening posts."
        }
    ]

# -------------------------------------------------------------
# STEP 3: ZERO-FAKE ORIGINAL ASSET SOURCING
# -------------------------------------------------------------
def execute_step3_asset_sourcing(topic_keywords: List[str], assets_dir: str, max_assets: int = 8, sources: str = "all", extra_urls: List[str] = None, alias_tags: List[str] = None) -> List[Dict[str, Any]]:
    print("\n=======================================================")
    print("STEP 3: MULTI-SOURCE INTERNET & SOCIAL ASSET INTAKE (ZERO FAKE ASSETS)")
    print(f"Sourcing authentic media across [{sources}] + verified --from-urls...")
    print("=======================================================")
    downloaded = asset_fetcher.auto_fetch_assets_for_topic(
        topic_keywords, assets_dir, max_assets=max_assets,
        sources=sources, extra_urls=extra_urls, alias_tags=alias_tags
    )
    return downloaded

# -------------------------------------------------------------
# STEP 4: WHISPERX WORD MAPPING & GAP ANALYSIS
# -------------------------------------------------------------
def execute_step4_audio_mapping_and_gaps(audio_path: str, assets_manifest: List[Dict[str, Any]], out_json: str, alias_map: Dict[str, List[str]] = None) -> Dict[str, Any]:
    print("\n=======================================================")
    print("STEP 4: WHISPERX FORCED WORD ALIGNMENT & ASSET MAPPING")
    print("Computing millisecond-accurate word timestamps...")
    print("=======================================================")

    timeline = audio_sync.align_audio_whisper(audio_path, model_size="base")
    total_dur = timeline["duration"]

    # Match assets to sentences using filename tokens, semantic manifest tags, and phonetic Hinglish aliases
    mapped_timeline = []
    occupied_intervals = []
    alias_map = alias_map or {}

    for seg in timeline["segments"]:
        seg_text = seg["text"].lower()
        seg_tokens = set(re.split(r'[^a-zA-Z0-9]+', seg_text))
        matched_asset = None

        for asset in assets_manifest:
            fn_words = [w.lower() for w in re.split(r'[^a-zA-Z0-9]', asset.get("filename", "")) if len(w) > 3]
            tag_words = [str(t).lower() for t in asset.get("tags", []) if len(str(t)) > 2]
            extra_aliases = [str(a).lower() for a in alias_map.get(asset.get("filename", ""), [])]
            all_keys = set(fn_words + tag_words + extra_aliases)

            for key in all_keys:
                if key in seg_tokens or (len(key) >= 4 and key in seg_text):
                    matched_asset = asset
                    break
            if matched_asset:
                break

        mapped_timeline.append({
            "start": seg["start"],
            "end": seg["end"],
            "text": seg["text"],
            "asset": matched_asset["filename"] if matched_asset else None,
            "has_archival_asset": matched_asset is not None,
            "engine_role": "main_ashu_dalal_documentary" if matched_asset else "gap_engine_pending_user_choice"
        })
        if matched_asset:
            occupied_intervals.append((seg["start"], seg["end"]))

    # Detect Empty "Khali" Spaces (Gaps where NO archival asset exists)
    gap_segments = []
    for item in mapped_timeline:
        if not item["has_archival_asset"]:
            gap_segments.append({
                "start": item["start"],
                "end": item["end"],
                "duration": round(item["end"] - item["start"], 2),
                "text": item["text"]
            })

    result = {
        "audio_file": audio_path,
        "duration": total_dur,
        "alignment_engine": timeline.get("engine", "whisper"),
        "sound_engine_default": "openverse",
        "words": timeline.get("words", []),
        "mapped_timeline": mapped_timeline,
        "gap_segments": gap_segments,
        "total_gaps_count": len(gap_segments)
    }

    with open(out_json, "w", encoding="utf-8") as f:
        json.dump(result, f, indent=2, ensure_ascii=False)

    print(f"\n[MAPPING COMPLETE] Duration: {total_dur:.2f}s | Words Synced: {len(result['words'])}")
    print(f"Asset-Backed (MAIN Documentary Engine): {len(mapped_timeline) - len(gap_segments)} | Empty Gaps (Fallback Engines Only): {len(gap_segments)}")
    return result

# -------------------------------------------------------------
# SCRIPT-AWARE plan.md GENERATOR & RESEARCH-DRIVEN GAP PLANNER
# -------------------------------------------------------------
def _infer_gap_recommendation(text: str) -> Dict[str, Any]:
    """Heuristically suggest initial engine/combo/3D-model directions for a gap sentence (to refine via internet research)."""
    low = text.lower()
    if any(k in low for k in ("hack", "code", "cyber", "virus", "worm", "network", "server", "data", "scan", "radar", "gps", "signal", "satellite")):
        return {
            "engines": "3D-Animator (`blueprint`/`thermal` + `styleAt` morph) + Lemo (`lidar-survey` / `hologram-hud` / `circuit-board`)",
            "combo": "--shader=0:lit,1.5:blueprint --brush=flow_field --lemo=dark-documentary --post=hdr",
            "needs_3d_model": "Optional server/satellite/hardware .glb if physical hardware is mentioned",
            "sfx": "whoosh, typing, glitch, click"
        }
    if any(k in low for k in ("centrifuge", "engine", "turbine", "aircraft", "plane", "rocket", "submarine", "weapon", "machine", "camera", "device", "factory", "reactor")):
        return {
            "engines": "code-3d-video / 3D-Animator (`--model=<slug>.glb` + `teardown`/`blueprint`) + Lemo (`precise-mechanism` / `assembly-line-diagram`)",
            "combo": "--shader=paper --model=models/<slug>/<file>.gltf --lemo=blueprint --post=gtao",
            "needs_3d_model": "RECOMMENDED: Fetch real CC0 .glb/.gltf via `model_fetcher.py --query='<subject>'` or `--from-urls`",
            "sfx": "thud, click, riser"
        }
    if any(k in low for k in ("war", "secret", "plan", "letter", "spy", "intelligence", "history", "19", "century", "treaty", "assassination", "murder", "escape")):
        return {
            "engines": "p5.brush (`charcoal` / `watercolor` / `hatching`) + Lemo (`halftone-dossier` / `vintage-collage` / `comic-history` / `silent-film`)",
            "combo": "--shader=paper --brush=charcoal --lemo=halftone-dossier --post=gtao",
            "needs_3d_model": "Optional vintage prop .glb (desk/lantern/radio) via Poly Haven CC0",
            "sfx": "paper, stamp, thud, whoosh"
        }
    return {
        "engines": "Lemo-Opuscar (`dark-documentary` / `briefing-board`) + p5.brush (`watercolor` / `flow_field`) or `--combo`",
        "combo": "--shader=paper --brush=watercolor --lemo=dark-documentary --post=gtao",
        "needs_3d_model": "Decide after internet visual research (use `model_fetcher.py` if concrete 3D object helps clarity)",
        "sfx": "whoosh, click, riser"
    }


def generate_plan_md(
    out_path: str = "plan.md",
    topic: str = "Untitled Documentary",
    script_text: str = "",
    mapping: Dict[str, Any] = None,
    research_notes: str = "",
    assets_manifest: List[Dict[str, Any]] = None,
    models_manifest: List[Dict[str, Any]] = None,
) -> str:
    """
    Create a structured, research-driven `plan.md` mapping every spoken line:
      - Asset-backed narration -> Primary Ashu-Dalal Evidence Board / code-3d-video
      - Empty Gaps ('khali parts') -> What is spoken, Mandatory Internet Visual Research brief,
        Engine + Style + --combo blueprint, and downloadable .glb/.gltf 3D model plan.
    """
    assets_manifest = assets_manifest or []
    models_manifest = models_manifest or []
    lines = [
        f"# Documentary Production & Gap Visual Plan (`plan.md`) — {topic}\n",
        "> **System Law:** Real archival asset sections use the **Primary Ashu-Dalal Backbone (`board_engine.py` / `code-3d-video`)**.",
        "> **Gap Law:** For every no-asset *khali* part, AI **MUST research on the internet** (mechanics, real architecture, historical visual references, documentary staging) and update this plan BEFORE generating animations or choosing final styles.\n",
        "---",
        "\n## 1. Timeline Overview & Asset Coverage\n",
    ]

    gaps = []
    if mapping and mapping.get("mapped_timeline"):
        lines.append("| # | Time | Spoken Line | Mode / Role | Matched Asset |")
        lines.append("|---|---|---|---|---|")
        for idx, item in enumerate(mapping["mapped_timeline"], 1):
            t_range = f"`{item['start']:.1f}s - {item['end']:.1f}s`"
            role = "**Primary Backbone** (Archival)" if item.get("has_archival_asset") else "**GAP — Research & Custom Visual**"
            asset = item.get("asset") or "*(none — gap)*"
            safe_txt = str(item.get("text", "")).replace("|", "/")
            lines.append(f"| {idx} | {t_range} | {safe_txt} | {role} | {asset} |")
            if not item.get("has_archival_asset"):
                gaps.append(item)
    else:
        sents = [s.strip() for s in re.split(r"(?<=[.!?।])\s+|\n+", script_text.strip()) if s.strip()]
        lines.append("| # | Beat (Est.) | Spoken Script Sentence | Status / Next Check |")
        lines.append("|---|---|---|---|")
        for idx, sent in enumerate(sents, 1):
            safe_txt = sent.replace("|", "/")
            lines.append(f"| {idx} | Sentence {idx} | {safe_txt} | Verify archival match in Step 3–4; treat as Gap if none found |")
            gaps.append({"start": (idx - 1) * 4.0, "end": idx * 4.0, "text": sent})

    sec_num = 2
    if research_notes:
        lines.append(f"\n---\n\n## {sec_num}. Internet & Social Media Research Summary\n")
        lines.append(research_notes.strip())
        sec_num += 1

    lines.append(f"\n---\n\n## {sec_num}. Gap Segments — Internet-Researched Visual Design & Engine Plan\n")
    sec_num += 1
    if not gaps:
        lines.append("*No empty gaps detected — 100% of spoken narration is backed by verified archival assets (use Primary Backbone).*")
    else:
        for i, g in enumerate(gaps, 1):
            txt = g.get("text", "").strip()
            rec = _infer_gap_recommendation(txt)
            ts_label = f"{g['start']:.1f}s - {g['end']:.1f}s" if "start" in g and "end" in g else f"Segment {i}"
            lines.append(f"### Gap {i}: [{ts_label}]")
            lines.append(f"- **Kya Bola Ja Raha Hai (Spoken Narration):** *\"{txt}\"*")
            lines.append("- **Internet Visual Research Checklist (AI Fill-In Before Build):**")
            lines.append("  - [ ] Search real-world mechanics / architecture / geography / historical look behind this sentence.")
            lines.append("  - [ ] Decide exact hero composition, animated metaphor, camera move, and 1–2 frame WhisperX trigger word.")
            lines.append(f"- **Suggested Engines & Styles:** {rec['engines']}")
            lines.append(f"- **Ready `--combo` Recipe:** `python studio.py --combo {rec['combo']} --stills=1.5,3.0`")
            lines.append(f"- **3D Model Plan (`.glb` / `.gltf`):** {rec['needs_3d_model']}")
            lines.append(f"- **Sound Cues (Multi-Source Openverse+Archive+Wikimedia):** `{rec['sfx']}`\n")

    if models_manifest:
        lines.append(f"\n---\n\n## {sec_num}. Verified Downloaded 3D Models (`models_manifest.json`)\n")
        for m in models_manifest:
            lines.append(f"- `{m.get('id')}` ({m.get('format')}, license: `{m.get('license')}`) -> `{m.get('file')}`")

    content = "\n".join(lines) + "\n"
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"[PLAN] Generated research & gap visual blueprint -> {out_path} ({len(gaps)} gap segment(s))")
    return out_path


# -------------------------------------------------------------
# STEP 5 & 5(1): INTERACTIVE VISUAL SELECTION CONSULTATION
# -------------------------------------------------------------
def format_step5_consultation_prompt(gap_segments: List[Dict[str, Any]]) -> str:
    """
    Constructs the exact interactive consultation message to present to the user/operator
    as specified in handwritten Step 5 & Substep 5(1).
    """
    msg = []
    msg.append("## 🎨 STEP 5 & 5(1): VISUAL ENGINE SELECTION FOR NO-ASSET GAPS ONLY\n")
    msg.append("**Note:** Jahan-jahan real archival assets available hain, wahan strictly aapki **Main Ashu-Dalal 3D Documentary Engine** hi chalegi.\n")
    msg.append("Sirf neeche diye gaye *'khali parts'* (missing-asset gaps) jinke liye koi real asset nahi mila, unke liye **3 Fallback Visual Engines** available hain:\n")

    msg.append("### 1. Lemo-Opuscar Studio (Curated Film Styles)")
    for s in get_lemo_styles(8):
        msg.append(f"  - `{s['name']}`: Cinematic thematic style preset")

    msg.append("\n### 2. p5.brush (Natural Generative Media)")
    for m in BRUSH_MEDIA:
        msg.append(f"  - `{m['name']}`: {m['desc']}")

    msg.append("\n### 3. 3D-Animator / Three.js (Procedural 3D World)")
    for s in STYLES_3D[:6]:
        msg.append(f"  - `{s['name']}`: {s['desc']}")

    msg.append("\n### 4. Combined Hybrid Mode (`studio.py --combo` — Multi-Engine Fusion)")
    msg.append("  - Combine `3D-Animator` shaders + `p5.brush` animated CanvasTextures + `Lemo-Opuscar` palettes/GTAO/CRT (`guides/COMBINATIONS.md`).")
    msg.append("  - Optional Classic Insert: `Vintage 2D Silent-Film` (`vintage_engine.py`).")

    msg.append("\n---\n")
    msg.append("### Identified No-Asset Gap Segments Waiting for Your Choice:")
    for i, gap in enumerate(gap_segments, 1):
        msg.append(f"{i}. **[{gap['start']:.1f}s - {gap['end']:.1f}s]** ({gap['duration']}s): *\"{gap['text']}\"*")

    msg.append("\n*Note: Detailed internet-researched gap designs & 3D `.glb` model suggestions `plan.md` me saved hain.*")
    msg.append("*Batayein in khali parts ke liye konsa engine, combo aur style use karna hai? Agar aapko **aur styles** chahiye toh bas bolen — hum poori 99 styles ki list dikha denge.*")
    return "\n".join(msg)

def main():
    parser = argparse.ArgumentParser(description="Unified 5-Step Director Workflow Engine")
    parser.add_argument("--suggest-topics", action="store_true", help="Print curated documentary topics")
    parser.add_argument("--list-gap-styles", action="store_true", help="Print all styles across the 3 engines for Step 5(1)")
    parser.add_argument("--run-intake", nargs=2, metavar=("AUDIO_PATH", "TOPIC_KEYWORDS"), help="Execute Steps 3 & 4: Audio intake, asset fetch, mapping, and plan.md generation")
    parser.add_argument("--plan", action="store_true", help="Generate script-aware & research-ready plan.md for topic/script or mapping JSON")
    parser.add_argument("--topic", type=str, default="Documentary Production", help="Topic title for --plan")
    parser.add_argument("--script-file", type=str, default="", help="Path to narration script text file for early --plan")
    parser.add_argument("--mapping", type=str, default="", help="Optional project_mapping.json from Step 4 for timestamped --plan")
    parser.add_argument("--research-file", type=str, default="", help="Optional markdown/text file with Step 1 internet research notes")
    parser.add_argument("--out", type=str, default="plan.md", help="Output plan path (default: plan.md)")
    args = parser.parse_args()

    if args.suggest_topics:
        topics = suggest_documentary_topics()
        print("\n=== CURATED DOCUMENTARY TOPICS ===")
        for t in topics:
            print(f"- [{t['id']}] {t['title']}\n  {t['logline']}\n")
        return

    if args.list_gap_styles:
        print("\n=== STEP 5(1) VISUAL ENGINES & STYLES CATALOG ===")
        print("\n1. THREE.JS 3D SHADER LOOKS:")
        for s in STYLES_3D:
            print(f"  --style={s['name']:12} : {s['desc']}")

        print("\n2. P5.BRUSH NATURAL MEDIA:")
        for m in BRUSH_MEDIA:
            print(f"  --media={m['name']:12} : {m['desc']}")

        print("\n3. LEMO-OPUSCAR FILM STYLES (99 STYLES AVAILABLE):")
        for s in get_lemo_styles(20):
            print(f"  --style={s['name']:20}")
        print("\n")
        return

    if args.plan:
        script_txt = open(args.script_file, encoding="utf-8").read() if args.script_file and os.path.exists(args.script_file) else ""
        mapping_obj = json.load(open(args.mapping, encoding="utf-8")) if args.mapping and os.path.exists(args.mapping) else None
        research_txt = open(args.research_file, encoding="utf-8").read() if args.research_file and os.path.exists(args.research_file) else ""
        models_obj = json.load(open("models/models_manifest.json", encoding="utf-8")) if os.path.exists("models/models_manifest.json") else []
        generate_plan_md(
            out_path=args.out, topic=args.topic, script_text=script_txt,
            mapping=mapping_obj, research_notes=research_txt, models_manifest=models_obj
        )
        return

    if args.run_intake:
        audio_file, keywords = args.run_intake
        assets_dir = "assets"
        assets = execute_step3_asset_sourcing(keywords.split(","), assets_dir)
        mapping = execute_step4_audio_mapping_and_gaps(audio_file, assets, "project_mapping.json")
        generate_plan_md(out_path=args.out, topic=keywords, mapping=mapping, assets_manifest=assets)
        prompt = format_step5_consultation_prompt(mapping["gap_segments"])
        print("\n" + prompt)

if __name__ == "__main__":
    main()
