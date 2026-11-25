#!/usr/bin/env python3
"""
Documentary 3D by Ashu Dalal (Version 3) - Glitch-Free Modular Combo Runner
Supports ALL 10 verified trouble-free combinations strictly across:
  - Ashu Dalal Evidence Board (board_engine.py) & Vintage Silent-Film (vintage_engine.py)
  - 3D-Animator (styles.js 12 shaders + HDR accumulation)
  - Lemo-Opuscar (99 STYLE.md palettes + post.js GTAO/DOF + crt.js VHS)
  - Universal Finishers (handheld.py, phone_motion.py, laptop_reel.py, Bundled CC0 Documentary SFX)
"""

import os
import sys
import argparse
import subprocess

SCRIPTS_DIR = os.path.dirname(os.path.abspath(__file__))
KIT_DIR = os.path.join(SCRIPTS_DIR, "kit")

COMBO_CATALOG = [
    {"id": "board-handheld", "group": "A", "name": "Evidence Board + Handheld Physics", "when": "Flat digital pan ki jagah real smartphone human shake & micro-wander chahiye"},
    {"id": "board-crt", "group": "A", "name": "Evidence Board + Lemo VHS/CRT", "when": "Retro TV newsroom, 1980s-2000s cyber/intel broadcast look chahiye"},
    {"id": "board-3d-reel", "group": "A", "name": "Evidence Board + 3D-Animator / Laptop Reel", "when": "Archival photos 3D space me DOF/shadows ke saath dikhane ho ya 9:16 device mockup reel banani ho"},
    {"id": "3d-gtao-dof", "group": "B", "name": "3D-Animator + Lemo GTAO & Bokeh DOF", "when": "Studio-grade corner contact shadows (GTAO) aur 96-tap physical camera blur chahiye"},
    {"id": "3d-lemo-palette", "group": "B", "name": "3D-Animator + Lemo 99 Style Palettes", "when": "Lemo library ke exact dark-documentary / blueprint / comic-history color palettes 3D stage me lagane ho"},
    {"id": "3d-whisperx-morph", "group": "B", "name": "3D-Animator Live Style Morph + Lemo (WhisperX)", "when": "Bina cut kiye spoken word aate hi scene ko lit se blueprint/thermal/synth me morph karna ho"},
    {"id": "3d-mix-archival", "group": "B", "name": "3D-Animator Mix + Archival Photo + .glb Model + Lemo", "when": "Ek hi frame me background lit, photo card 100% crisp readable, aur hero .glb prop blueprint/clay + Lemo palette me rakhna ho"},
    {"id": "lemo-whisperx-audio", "group": "C", "name": "Lemo Style + WhisperX + Documentary SFX + Handheld", "when": "Kisi bhi Lemo film style me exact word sync, CC0 documentary SFX (-14 LUFS), aur camera shake lagana ho"},
    {"id": "3d-lemo-crt", "group": "C", "name": "3D-Animator + Lemo Palette + Lemo VHS/CRT", "when": "3D scenes par phosphor halation glow, chroma bleed, aur CRT scanlines chahiye"},
    {"id": "master-3d-lemo-fusion", "group": "D", "name": "Master 3D-Animator + Lemo + .glb + Handheld Fusion", "when": "Flagship gap/custom 3D scene: 3D geometry/model + 3D shader + Lemo palette/GTAO + human shake"}
]


def list_combos():
    print("\n=== DOCUMENTARY 3D VERSION 3 - 10 VERIFIED GLITCH-FREE COMBINATIONS ===")
    for i, c in enumerate(COMBO_CATALOG, 1):
        print(f" {i:2d}. [{c['id']:22}] ({c['group']}) {c['name']}")
        print(f"     Kab use karein: {c['when']}")
    print("\nGuide file: guides/COMBINATIONS.md")
    print("Combo CLI example: python studio.py --combo --shader=paper --lemo=dark-documentary --post=gtao --stills=1.5,3.5 --out=stills\n")


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
    dec_rc = dec.wait()
    shk_rc = shk.wait()
    if dec_rc != 0 or shk_rc != 0 or enc.returncode != 0:
        raise RuntimeError(f"Handheld ffmpeg pipeline failed (dec={dec_rc}, shk={shk_rc}, enc={enc.returncode})")
    print(f"[COMBO] Handheld motion pass applied -> {out_mp4}")


def main():
    parser = argparse.ArgumentParser(description="Glitch-Free 3D-Animator + Lemo-Opuscar Modular Combo Runner")
    parser.add_argument("--list", action="store_true", help="List all 10 verified combinations")
    parser.add_argument("--shader", type=str, default="lit", help="3D-Animator shader or timeline (e.g. paper or 0:lit,2.5:blueprint)")
    parser.add_argument("--lemo", type=str, default="none", help="Lemo-Opuscar style slug (e.g. dark-documentary, blueprint, archive-lighttable)")
    parser.add_argument("--post", type=str, default="hdr", choices=["hdr", "gtao", "crt", "none"], help="Clean single-pass post-FX")
    parser.add_argument("--photo", type=str, default="", help="Optional /assets/... or local file path mapped onto readable 3D card")
    parser.add_argument("--model", type=str, default="", help="Optional /models/... or local .glb/.gltf 3D model path")
    parser.add_argument("--project", type=str, default="", help="Optional project folder root for resolving /assets/...")
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

    out_arg = args.out
    if args.stills and out_arg.lower().endswith(".mp4"):
        out_arg = "stills"

    cmd = [
        "node", os.path.join(KIT_DIR, "combo_render.mjs"),
        f"--width={args.width}", f"--height={args.height}",
        f"--shader={args.shader}",
        f"--lemo={args.lemo}", f"--post={args.post}",
        f"--total={args.total}", f"--n={args.n}", f"--out={out_arg}"
    ]
    if args.photo:
        cmd.append(f"--photo={args.photo}")
    if args.model:
        cmd.append(f"--model={args.model}")
    if args.project:
        cmd.append(f"--project={args.project}")
    if args.stills:
        cmd.append(f"--stills={args.stills}")
    elif args.video:
        cmd.append("--video")
        if args.audio:
            cmd.append(f"--audio={args.audio}")

    print("[COMBO] Launching modular renderer:", " ".join(cmd))
    subprocess.run(cmd, check=True)

    if args.video and args.handheld_csv and os.path.exists(out_arg):
        stem, ext = os.path.splitext(out_arg)
        shaken = f"{stem}_handheld{ext or '.mp4'}"
        apply_handheld_filter(out_arg, shaken, args.handheld_csv, args.width, args.height)


if __name__ == "__main__":
    main()
