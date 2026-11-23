#!/usr/bin/env python3
"""
Documentary 3D by Ashu Dalal (Version 2) - Master Studio CLI
Unified command center uniting:
  1. Evidence Board & Vintage 2D Engine (board_engine.py, vintage_engine.py)
  2. Three.js 3D Procedural Studio (12 Styles + Camera Physics)
  3. p5.brush Natural Generative Media Engine
  4. Lemo-Opuscar Directorial Studio (100 Film Styles)
  5. WhisperX / Word-Level Speech Sync Engine (audio_sync.py)
  6. Automated Archival Asset Fetcher (asset_fetcher.py)
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
    print("   Directorial Manuals: guides/DIRECTOR.md, guides/TECHNIQUE.md, guides/MY-STYLES.md")
    print("5. [WhisperX / Word-Level Speech Sync Engine]")
    print(f"   Script: {os.path.join(DOC_SCRIPTS, 'audio_sync.py')}")
    print("   Capabilities: Exact word-level forced alignment, subtitle generation (min 1.8s hold), visual cue marks")
    print("6. [Automated Archival Asset Fetcher]")
    print(f"   Script: {os.path.join(DOC_SCRIPTS, 'asset_fetcher.py')}")
    print("   Capabilities: Auto-sources authentic historical assets from Wikimedia Commons/Wikipedia without synthetic slop\n")

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
    parser.add_argument("--workflow", action="store_true", help="Launch the canonical 5-Step Director Workflow")
    parser.add_argument("--suggest-topics", action="store_true", help="Print curated documentary topics and ideas")
    parser.add_argument("--list-gap-styles", action="store_true", help="List styles for the 3 creative engines (Lemo, p5.brush, 3D-Animator) for gap parts")
    parser.add_argument("--sync-audio", type=str, help="Path to voiceover audio file to run word-level forced alignment")
    parser.add_argument("--fetch-assets", type=str, help="Search query or comma-separated keywords to auto-fetch verified archival assets")
    parser.add_argument("--auto-intake", type=str, help="Path to voiceover audio for full auto intake: word sync + asset sourcing")
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

    if args.suggest_topics or args.list_gap_styles or args.workflow:
        director_script = os.path.join(DOC_SCRIPTS, "director_workflow.py")
        if args.suggest_topics:
            subprocess.run([sys.executable, director_script, "--suggest-topics"], check=True)
            return
        if args.list_gap_styles:
            subprocess.run([sys.executable, director_script, "--list-gap-styles"], check=True)
            return
        if args.workflow:
            print("\n=== DOCUMENTARY 3D BY ASHU DALAL - 5-STEP DIRECTOR WORKFLOW ===")
            subprocess.run([sys.executable, director_script, "--suggest-topics"], check=True)
            print("To proceed with intake and mapping:")
            print("  python studio.py --sync-audio=<voiceover.wav>")
            print("  python studio.py --fetch-assets='<keywords>'\n")
            return

    if args.sync_audio:
        sync_script = os.path.join(DOC_SCRIPTS, "audio_sync.py")
        out_json = args.out if args.out.endswith(".json") else "sync_timeline.json"
        cmd = [sys.executable, sync_script, "--audio", args.sync_audio, "--out", out_json]
        print(f"[STUDIO] Executing word-level speech sync on: {args.sync_audio}...")
        subprocess.run(cmd, check=True)
        return

    if args.fetch_assets:
        fetch_script = os.path.join(DOC_SCRIPTS, "asset_fetcher.py")
        out_dir = args.out if not args.out.endswith(".mp4") else "assets"
        cmd = [sys.executable, fetch_script, "--query", args.fetch_assets, "--out", out_dir]
        print(f"[STUDIO] Auto-sourcing verified historical assets for: '{args.fetch_assets}'...")
        subprocess.run(cmd, check=True)
        return

    if args.auto_intake:
        print("=== STAGE 1: AUTOMATED SPEECH FORCED ALIGNMENT (WHISPERX / WHISPER) ===")
        sync_script = os.path.join(DOC_SCRIPTS, "audio_sync.py")
        timeline_path = "sync_timeline.json"
        subprocess.run([sys.executable, sync_script, "--audio", args.auto_intake, "--out", timeline_path], check=True)
        print("\n=== STAGE 2: INTAKE READY FOR SCENE PROGRAMMING ===")
        print("Master timeline established. Assets ready for deterministic 3D choreography.\n")
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
