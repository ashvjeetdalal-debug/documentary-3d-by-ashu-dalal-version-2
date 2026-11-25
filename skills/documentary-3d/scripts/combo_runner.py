#!/usr/bin/env python3
"""
Documentary 3D by Ashu Dalal (Version 3) - Universal Modular Combo Runner
Supports ALL 15 verified trouble-free combinations across:
  - Evidence Board (board_engine.py) & Vintage Silent-Film (vintage_engine.py)
  - Code-3D-Video (character.js / builders.js)
  - 3D-Animator (styles.js 12 shaders + HDR accumulation)
  - p5.brush (BrushTextureTarget 3D textures + 2D overlay compositing)
  - Lemo-Opuscar (STYLE.md palettes + post.js GTAO/DOF + crt.js VHS)
  - Universal Finishers (handheld.py, phone_motion.py, laptop_reel.py, Openverse SFX)
"""

import os
import sys
import json
import argparse
import subprocess

SCRIPTS_DIR = os.path.dirname(os.path.abspath(__file__))
KIT_DIR = os.path.join(SCRIPTS_DIR, "kit")

COMBO_CATALOG = [
    {"id": "board-brush-overlay", "group": "A", "name": "Evidence Board + p5.brush Overlay", "when": "Archival maps/photos par hand-drawn charcoal wobble circles, watercolor map tints & marker swipes chahiye"},
    {"id": "board-handheld", "group": "A", "name": "Evidence Board + Handheld Physics", "when": "Flat digital pan ki jagah real smartphone human shake & micro-wander chahiye"},
    {"id": "board-crt", "group": "A", "name": "Evidence Board + Lemo VHS/CRT", "when": "Retro TV newsroom, 1980s-2000s cyber/intel broadcast look chahiye"},
    {"id": "board-3d-reel", "group": "A", "name": "Evidence Board + 3D-Animator / Laptop Reel", "when": "Archival photos 3D space me DOF/shadows ke saath dikhane ho ya 9:16 device mockup reel banani ho"},
    {"id": "3d-code-shaders", "group": "B", "name": "Code-3D-Video + 3D-Animator Shaders", "when": "Walking 3D characters aur streets ko clay, paper, blueprint, toon, ya voxel look + motion blur dena ho"},
    {"id": "3d-brush-surface", "group": "B", "name": "3D-Animator + p5.brush Live Textures", "when": "3D models & walls par animated watercolor, charcoal, ya hatching textures chahiye"},
    {"id": "3d-gtao-dof", "group": "B", "name": "3D-Animator + Lemo GTAO & Bokeh DOF", "when": "Studio-grade corner contact shadows (GTAO) aur 96-tap physical camera blur chahiye"},
    {"id": "3d-lemo-palette", "group": "B", "name": "3D-Animator + Lemo 99 Style Palettes", "when": "Lemo library ke exact dark-documentary / blueprint / comic-history color palettes 3D stage me lagane ho"},
    {"id": "code3d-post-crt", "group": "B", "name": "Code-3D-Video + Lemo post.js / crt.js", "when": "Original code-3d-video stories par GTAO bokeh upgrade ya CRT videotape pass lagana ho"},
    {"id": "3d-whisperx-morph", "group": "B", "name": "3D-Animator Live Style Morph (WhisperX)", "when": "Bina cut kiye spoken word aate hi scene ko lit se blueprint/thermal/synth me morph karna ho"},
    {"id": "3d-mix-archival", "group": "B", "name": "3D-Animator Mix + Archival Photo + p5.brush", "when": "Ek hi frame me background lit, photo card 100% crisp readable, aur hero prop clay/blueprint rakhna ho"},
    {"id": "vintage-brush", "group": "C", "name": "Vintage Silent-Film + p5.brush Boiling", "when": "Historical flashbacks me 12 fps hand-drawn charcoal boiling lines + sepia flicker chahiye"},
    {"id": "brush-crt", "group": "C", "name": "p5.brush + Lemo VHS/CRT", "when": "Hand-drawn ink/watercolor animations par phosphor halation glow & CRT scanlines chahiye"},
    {"id": "lemo-whisperx-openverse", "group": "C", "name": "Lemo Style + WhisperX + Openverse + Handheld", "when": "Kisi bhi Lemo film style me exact word sync, CC-licensed SFX (-14 LUFS), aur camera shake lagana ho"},
    {"id": "master-4in1-hybrid", "group": "D", "name": "Master 4-in-1 Fusion (3D + p5.brush + Lemo + Handheld)", "when": "Flagship gap scene: 3D geometry + animated brush textures + Lemo palette/GTAO + human shake"}
]


def list_combos():
    print("\n=== DOCUMENTARY 3D VERSION 3 - 15 VERIFIED TROUBLE-FREE COMBINATIONS ===")
    for i, c in enumerate(COMBO_CATALOG, 1):
        print(f" {i:2d}. [{c['id']:22}] ({c['group']}) {c['name']}")
        print(f"     Kab use karein: {c['when']}")
    print("\nGuide file: guides/COMBINATIONS.md")
    print("Combo CLI example: python studio.py --combo --shader=paper --brush=watercolor --lemo=dark-documentary --post=gtao --stills=1.5,3.5\n")


def apply_handheld_filter(in_mp4, out_mp4, motion_csv, width=1920, height=1080):
    """Pipes an existing MP4 through present/handheld.py using real 2D-FFT phone motion data."""
    hh = os.path.join(KIT_DIR, "present", "handheld.py")
    if not os.path.exists(motion_csv):
        raise FileNotFoundError(f"Motion CSV not found: {motion_csv}")
    dec = subprocess.Popen(
        ["ffmpeg", "-v", "error", "-i", in_mp4, "-f", "rawvideo", "-pix_fmt", "rgb24", "-"],
        stdout=subprocess.PIPE
    )
    shk = subprocess.Popen(
        [sys.executable, hh, motion_csv, str(width), str(height), str(width / 2), str(height / 2)],
        stdin=dec.stdout, stdout=subprocess.PIPE
    )
    enc = subprocess.Popen(
        ["ffmpeg", "-y", "-v", "error", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{width}x{height}",
         "-r", "30", "-i", "-", "-i", in_mp4, "-map", "0:v", "-map", "1:a?", "-c:v", "libx264",
         "-preset", "veryfast", "-crf", "18", "-pix_fmt", "yuv420p", "-c:a", "copy", out_mp4],
        stdin=shk.stdout
    )
    dec.stdout.close()
    shk.stdout.close()
    enc.communicate()
    if enc.returncode != 0:
        raise RuntimeError("Handheld ffmpeg pipeline failed")
    print(f"[COMBO] Handheld motion pass applied -> {out_mp4}")


def overlay_brush_on_video(base_mp4, brush_mp4, out_mp4, mode="screen"):
    """Cleanly composites a p5.brush pass over an Evidence Board or 3D base MP4."""
    if mode == "colorkey":
        flt = "[1:v]colorkey=0x0a0c10:0.15:0.12[ov];[0:v][ov]overlay=shortest=1[v]"
    else:
        flt = f"[0:v][1:v]blend=all_mode={mode}:all_opacity=0.85[v]"
    subprocess.run([
        "ffmpeg", "-y", "-v", "error", "-i", base_mp4, "-i", brush_mp4,
        "-filter_complex", flt, "-map", "[v]", "-map", "0:a?",
        "-c:v", "libx264", "-preset", "veryfast", "-crf", "18", "-pix_fmt", "yuv420p", "-c:a", "copy", out_mp4
    ], check=True)
    print(f"[COMBO] Composited brush overlay ({mode}) -> {out_mp4}")


def main():
    parser = argparse.ArgumentParser(description="Universal Modular Combo Runner (Version 3)")
    parser.add_argument("--list", action="store_true", help="List all 15 verified combinations")
    parser.add_argument("--shader", type=str, default="lit", help="3D-Animator shader or timeline (e.g. paper or 0:lit,2.5:blueprint)")
    parser.add_argument("--brush", type=str, default="none", help="p5.brush preset (watercolor, charcoal, hatching, marker, flow_field, pencil_hb)")
    parser.add_argument("--lemo", type=str, default="none", help="Lemo-Opuscar style slug (e.g. dark-documentary, blueprint, archive-lighttable)")
    parser.add_argument("--post", type=str, default="hdr", choices=["hdr", "gtao", "crt", "none"], help="Clean single-pass post-FX")
    parser.add_argument("--photo", type=str, default="", help="Optional /assets/... archival image mapped onto readable 3D card")
    parser.add_argument("--width", type=int, default=1920)
    parser.add_argument("--height", type=int, default=1080)
    parser.add_argument("--total", type=float, default=6.0)
    parser.add_argument("--n", type=int, default=4)
    parser.add_argument("--stills", type=str, help="Render verification stills (comma-separated timestamps)")
    parser.add_argument("--video", action="store_true", help="Render MP4 video")
    parser.add_argument("--out", type=str, default="out/combo.mp4")
    parser.add_argument("--audio", type=str, help="Optional mastered audio track to mux")
    parser.add_argument("--handheld-csv", type=str, help="Optional motion.csv to inject real handheld shake after render")
    args = parser.parse_args()

    if args.list:
        list_combos()
        return

    cmd = [
        "node", os.path.join(KIT_DIR, "combo_render.mjs"),
        f"--width={args.width}", f"--height={args.height}",
        f"--shader={args.shader}", f"--brush={args.brush}",
        f"--lemo={args.lemo}", f"--post={args.post}",
        f"--total={args.total}", f"--n={args.n}", f"--out={args.out}"
    ]
    if args.photo:
        cmd.append(f"--photo={args.photo}")
    if args.stills:
        cmd.append(f"--stills={args.stills}")
    elif args.video:
        cmd.append("--video")
        if args.audio:
            cmd.append(f"--audio={args.audio}")

    print("[COMBO] Launching modular renderer:", " ".join(cmd))
    subprocess.run(cmd, check=True)

    if args.video and args.handheld_csv and os.path.exists(args.out):
        shaken = args.out.replace(".mp4", "_handheld.mp4")
        apply_handheld_filter(args.out, shaken, args.handheld_csv, args.width, args.height)


if __name__ == "__main__":
    main()
