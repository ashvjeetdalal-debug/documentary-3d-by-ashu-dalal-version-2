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
        "circuit-board", "comic-history", "claymation", "woodcut-print",
        "sand-art", "origami-journey", "infrared-surveillance", "kinetic-typography",
        "analog-film", "chalkboard-lecture", "copper-engraving"
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
def execute_step3_asset_sourcing(topic_keywords: List[str], assets_dir: str, max_assets: int = 8) -> List[Dict[str, Any]]:
    print("\n=======================================================")
    print("STEP 3: ZERO-FAKE ARCHIVAL ASSET INTAKE")
    print("Sourcing authentic historical media from Wikimedia Commons...")
    print("=======================================================")
    downloaded = asset_fetcher.auto_fetch_assets_for_topic(topic_keywords, assets_dir, max_assets=max_assets)
    return downloaded

# -------------------------------------------------------------
# STEP 4: WHISPERX WORD MAPPING & GAP ANALYSIS
# -------------------------------------------------------------
def execute_step4_audio_mapping_and_gaps(audio_path: str, assets_manifest: List[Dict[str, Any]], out_json: str) -> Dict[str, Any]:
    print("\n=======================================================")
    print("STEP 4: WHISPERX FORCED WORD ALIGNMENT & ASSET MAPPING")
    print("Computing millisecond-accurate word timestamps...")
    print("=======================================================")

    timeline = audio_sync.align_audio_whisper(audio_path, model_size="base")
    total_dur = timeline["duration"]

    # Match assets to sentences based on keyword overlap
    mapped_timeline = []
    occupied_intervals = []

    for seg in timeline["segments"]:
        seg_text = seg["text"].lower()
        matched_asset = None
        for asset in assets_manifest:
            title_words = [w.lower() for w in re.split(r'[^a-zA-Z0-9]', asset["filename"]) if len(w) > 3]
            for tw in title_words:
                if tw in seg_text:
                    matched_asset = asset
                    break
            if matched_asset:
                break

        mapped_timeline.append({
            "start": seg["start"],
            "end": seg["end"],
            "text": seg["text"],
            "asset": matched_asset["filename"] if matched_asset else None,
            "has_archival_asset": matched_asset is not None
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
        "mapped_timeline": mapped_timeline,
        "gap_segments": gap_segments,
        "total_gaps_count": len(gap_segments)
    }

    with open(out_json, "w", encoding="utf-8") as f:
        json.dump(result, f, indent=2, ensure_ascii=False)

    print(f"\n[MAPPING COMPLETE] Duration: {total_dur:.2f}s")
    print(f"Total Sentences: {len(mapped_timeline)} | Asset-Backed: {len(mapped_timeline) - len(gap_segments)} | Gap Spaces: {len(gap_segments)}")
    return result

# -------------------------------------------------------------
# STEP 5 & 5(1): INTERACTIVE VISUAL SELECTION CONSULTATION
# -------------------------------------------------------------
def format_step5_consultation_prompt(gap_segments: List[Dict[str, Any]]) -> str:
    """
    Constructs the exact interactive consultation message to present to the user/operator
    as specified in handwritten Step 5 & Substep 5(1).
    """
    msg = []
    msg.append("## 🎨 STEP 5 & 5(1): VISUAL ENGINE SELECTION FOR GAP SEGMENTS\n")
    msg.append("Transcript aur audio analysis ke baad kuch aise parts identify hue hain jinke liye **koi original archival photo/asset exist nahi karta** (Khali space).\n")
    msg.append("Hamare Master Plugin me aisi situations ke liye **3 World-Class Visual Engines** available hain. Aap bataiye in khali parts ke liye aapko konsa visual approach chahiye:\n")

    msg.append("### 1️⃣ Engine 1: Lemo-Opuscar Studio (Curated Film Styles)")
    for s in get_lemo_styles(8):
        msg.append(f"  • `{s['name']}`: Cinematic thematic style preset")

    msg.append("\n### 2️⃣ Engine 2: p5.brush (Natural Generative Media)")
    for m in BRUSH_MEDIA:
        msg.append(f"  • `{m['name']}`: {m['desc']}")

    msg.append("\n### 3️⃣ Engine 3: 3D-Animator / Three.js (Procedural 3D World)")
    for s in STYLES_3D[:6]:
        msg.append(f"  • `{s['name']}`: {s['desc']}")

    msg.append("\n---\n")
    msg.append("### 📌 Identified Gap Segments Waiting for Your Decision:")
    for i, gap in enumerate(gap_segments, 1):
        msg.append(f"{i}. **[{gap['start']:.1f}s – {gap['end']:.1f}s]** ({gap['duration']}s): *\"{gap['text']}\"*")

    msg.append("\n💡 *Aap inme se koi bhi engine choose kar sakte hain, aur agar aapko **aur styles** dekhne hain toh bas bolen — hum poori 100+ styles ki list provide karenge!*")
    return "\n".join(msg)

def main():
    parser = argparse.ArgumentParser(description="Unified 5-Step Director Workflow Engine")
    parser.add_argument("--suggest-topics", action="store_true", help="Print curated documentary topics")
    parser.add_argument("--list-gap-styles", action="store_true", help="Print all styles across the 3 engines for Step 5(1)")
    parser.add_argument("--run-intake", nargs=2, metavar=("AUDIO_PATH", "TOPIC_KEYWORDS"), help="Execute Steps 3 & 4: Audio intake, asset fetch, and gap detection")
    args = parser.parse_args()

    if args.suggest_topics:
        topics = suggest_documentary_topics()
        print("\n=== CURATED DOCUMENTARY TOPICS ===")
        for t in topics:
            print(f"• [{t['id']}] {t['title']}\n  {t['logline']}\n")
        return

    if args.list_gap_styles:
        print("\n=== STEP 5(1) VISUAL ENGINES & STYLES CATALOG ===")
        print("\n1. THREE.JS 3D SHADER LOOKS:")
        for s in STYLES_3D:
            print(f"  --style={s['name']:12} : {s['desc']}")

        print("\n2. P5.BRUSH NATURAL MEDIA:")
        for m in BRUSH_MEDIA:
            print(f"  --media={m['name']:12} : {m['desc']}")

        print("\n3. LEMO-OPUSCAR FILM STYLES (100 STYLES AVAILABLE):")
        for s in get_lemo_styles(20):
            print(f"  --style={s['name']:20}")
        print("\n")
        return

    if args.run_intake:
        audio_file, keywords = args.run_intake
        assets_dir = "assets"
        assets = execute_step3_asset_sourcing(keywords.split(","), assets_dir)
        mapping = execute_step4_audio_mapping_and_gaps(audio_file, assets, "project_mapping.json")
        prompt = format_step5_consultation_prompt(mapping["gap_segments"])
        print("\n" + prompt)

if __name__ == "__main__":
    main()
