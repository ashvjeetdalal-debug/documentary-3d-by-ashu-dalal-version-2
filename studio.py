#!/usr/bin/env python3
"""
Documentary 3D by Ashu Dalal (Version 2) - Master Studio CLI
Unified command center uniting:
  1. Evidence Board & Vintage 2D Engine
  2. Three.js 3D Procedural Studio (12 Styles + Camera Physics)
  3. p5.brush Natural Generative Media Engine
  4. Lemo-Opuscar Directorial Studio (100 Film Styles)
"""
import os
import sys
import argparse
import subprocess

ROOT = os.path.dirname(os.path.abspath(__file__))
DOC_SCRIPTS = os.path.join(ROOT, "skills", "documentary-3d", "scripts")
KIT_3D = os.path.join(DOC_SCRIPTS, "kit")
KIT_BRUSH = os.path.join(ROOT, "skills", "p5-brush", "kit")
LEMO_STYLES = os.path.join(ROOT, "skills", "lemo-opuscar", "styles")

def list_engines():
    print("\n=== DOCUMENTARY 3D STUDIO VERSION 2 - INTEGRATED ENGINES ===")
    print("1. [Evidence Board & Vintage 2D Engine]")
    print(f"   Scripts: board_engine.py, vintage_engine.py, splice.py, mix_and_mux.py")
    print("2. [Three.js 3D Procedural Studio]")
    print(f"   Offline Renderer: {os.path.join(KIT_3D, 'render.mjs')}")
    print("   12 Aesthetic Shader Looks: lit, clay, paper, shadow, blueprint, toon, voxel, thermal, synth, chrome, neon, mix")
    print("   Camera Physics: phone_motion.py, handheld.py, laptop_reel.py")
    print("3. [p5.brush Natural Generative Media Engine]")
    print(f"   Offline Renderer: {os.path.join(KIT_BRUSH, 'render_brush.mjs')}")
    print("   Media: Pencils, Charcoal, Markers, Watercolor Bleed, Hatching, Vector Flow Fields")
    print("4. [Lemo-Opuscar Directorial Studio]")
    styles_count = len(os.listdir(LEMO_STYLES)) if os.path.exists(LEMO_STYLES) else 0
    print(f"   Film Styles: {styles_count} complete styles in skills/lemo-opuscar/styles/")
    print("   Directorial Manuals: guides/DIRECTOR.md, guides/TECHNIQUE.md, guides/MY-STYLES.md\n")

def list_styles():
    print("\n=== 12 THREE.JS 3D SHADER STYLES ===")
    styles_3d = ['lit', 'clay', 'paper', 'shadow', 'blueprint', 'toon', 'voxel', 'thermal', 'synth', 'chrome', 'neon', 'mix']
    for s in styles_3d:
        print(f"  • {s}")

    print(f"\n=== 100 LEMO-OPUSCAR FILM STYLES ===")
    if os.path.exists(LEMO_STYLES):
        styles = sorted(os.listdir(LEMO_STYLES))
        for i, s in enumerate(styles, 1):
            print(f"  {i:3d}. {s}")
    print("\nUse: python studio.py --render-3d --style=<name> OR inspect styles in skills/lemo-opuscar/styles/<name>/\n")

def main():
    parser = argparse.ArgumentParser(description="Documentary 3D by Ashu Dalal (Version 2) - Studio CLI")
    parser.add_argument("--list-engines", action="store_true", help="Show all integrated engines and tool status")
    parser.add_argument("--list-styles", action="store_true", help="List all 3D styles and 100 Lemo film styles")
    parser.add_argument("--render-3d", action="store_true", help="Render 3D scene via headless Chrome")
    parser.add_argument("--render-brush", action="store_true", help="Render p5.brush generative animation via headless Chrome")
    parser.add_argument("--render-board", action="store_true", help="Render Evidence Board video via OpenCV")
    parser.add_argument("--style", type=str, default="lit", help="Style name for 3D render (lit, clay, paper, toon, blueprint, etc.)")
    parser.add_argument("--out", type=str, default="out/final.mp4", help="Output file path")
    parser.add_argument("--stills", type=str, help="Comma-separated timestamps for still captures (e.g. 1.0,2.5)")

    args, unknown = parser.parse_known_args()

    if args.list_engines:
        list_engines()
        return

    if args.list_styles:
        list_styles()
        return

    if args.render_3d:
        cmd = ["node", "render.mjs"]
        if args.stills:
            cmd.append(f"--stills={args.stills}")
        else:
            cmd.extend(["--video", f"--out={args.out}", f"--style={args.style}"])
        print(f"Running Three.js 3D render in {KIT_3D}...")
        subprocess.run(cmd, cwd=KIT_3D, check=True)
        return

    if args.render_brush:
        cmd = ["node", "render_brush.mjs"]
        if args.stills:
            cmd.append(f"--stills={args.stills}")
        else:
            cmd.extend(["--video", f"--out={args.out}"])
        print(f"Running p5.brush render in {KIT_BRUSH}...")
        subprocess.run(cmd, cwd=KIT_BRUSH, check=True)
        return

    if args.render_board:
        cmd = [sys.executable, "board_engine.py"]
        if args.stills:
            cmd.extend(["stills", args.stills])
        else:
            cmd.extend(["full", "0", "300", args.out])
        print(f"Running Evidence Board engine in {DOC_SCRIPTS}...")
        subprocess.run(cmd, cwd=DOC_SCRIPTS, check=True)
        return

    list_engines()
    print("Run with --help to see execution options.")

if __name__ == "__main__":
    main()
