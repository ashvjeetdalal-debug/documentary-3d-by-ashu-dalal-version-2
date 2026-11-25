#!/usr/bin/env python3
"""
Documentary 3D by Ashu Dalal Version 3 - Master Studio CLI
Strict Hierarchy:
  PRIMARY BACKBONE:
    1. Ashu Dalal Documentary Engine (board_engine.py + code-3d-video) - Used for ALL asset-backed narration
  AUTOMATED INTAKE & AUDIO/ASSET ENGINES:
    2. WhisperX / Word-Level Speech Sync Engine (audio_sync.py)
    3. Zero-Fake Archival Asset Fetcher (asset_fetcher.py)
    4. Openverse Real SFX & Music Engine (openverse_sfx.py) - Active by default
       (Legacy sound_bed.py silenced by default via sound_config.json, preserved intact)
  GAP-ONLY FALLBACK ENGINES (Strictly invoked ONLY when no archival asset exists for spoken words):
    5. Lemo-Opuscar Studio (100 film styles)
    6. p5.brush Natural Generative Media Engine
    7. 3D-Animator / Three.js Procedural Studio (kit/)
"""
import os
import sys
import json
import argparse
import subprocess

ROOT = os.path.dirname(os.path.abspath(__file__))
DOC_SCRIPTS = os.path.join(ROOT, "skills", "documentary-3d", "scripts")
CODE_3D_SKILL = os.path.join(ROOT, "skills", "code-3d-video")
KIT_3D = os.path.join(DOC_SCRIPTS, "kit")
KIT_BRUSH = os.path.join(ROOT, "skills", "p5-brush", "kit")
LEMO_STYLES = os.path.join(ROOT, "skills", "lemo-opuscar", "styles")
SOUND_CONFIG = os.path.join(DOC_SCRIPTS, "sound_config.json")


def get_sound_mode():
    if os.path.exists(SOUND_CONFIG):
        try:
            return json.load(open(SOUND_CONFIG, encoding="utf-8")).get("active_engine", "openverse")
        except Exception:
            pass
    return "openverse"


def set_sound_mode(mode):
    if mode not in ("openverse", "legacy_synth"):
        raise ValueError("Sound mode must be 'openverse' or 'legacy_synth'")
    cfg = {}
    if os.path.exists(SOUND_CONFIG):
        cfg = json.load(open(SOUND_CONFIG, encoding="utf-8"))
    cfg["active_engine"] = mode
    with open(SOUND_CONFIG, "w", encoding="utf-8") as f:
        json.dump(cfg, f, indent=2)
    print(f"[STUDIO] Sound engine mode switched to: {mode}")


def list_engines():
    sound_mode = get_sound_mode()
    print("\n=== DOCUMENTARY 3D BY ASHU DALAL VERSION 3 - ENGINE HIERARCHY ===")
    print("\n[PRIMARY BACKBONE - ALWAYS USED FOR ASSET-BACKED NARRATION]")
    print("  1. Ashu Dalal Evidence-Board Documentary (board_engine.py, splice.py, mix_and_mux.py)")
    print(f"  2. Original Code-3D-Video Kit ({CODE_3D_SKILL})")

    print("\n[INTAKE & OPENVERSE SOUND ENGINES]")
    print(f"  3. WhisperX Speech Alignment & Mapping: {os.path.join(DOC_SCRIPTS, 'audio_sync.py')}")
    print(f"  4. Zero-Fake Internet Archival Asset Fetcher: {os.path.join(DOC_SCRIPTS, 'asset_fetcher.py')}")
    print(f"  5. Sound System (Active Mode: {sound_mode}):")
    print(f"     - Openverse Real SFX/Music: {os.path.join(DOC_SCRIPTS, 'openverse_sfx.py')}")
    print(f"     - Legacy Synth (sound_bed.py): SILENCED BY DEFAULT, preserved intact (--sound-mode=legacy_synth)")

    print("\n[GAP-ONLY FALLBACK ENGINES - USED ONLY WHEN NO REAL ASSET EXISTS]")
    styles_count = len([s for s in os.listdir(LEMO_STYLES) if os.path.isdir(os.path.join(LEMO_STYLES, s)) and not s.startswith(('_', '.'))]) if os.path.exists(LEMO_STYLES) else 0
    print(f"  6. Lemo-Opuscar Studio ({styles_count} styles in skills/lemo-opuscar/styles/)")
    print(f"  7. p5.brush Natural Media ({os.path.join(KIT_BRUSH, 'render_brush.mjs')})")
    print(f"  8. 3D-Animator / Three.js ({os.path.join(KIT_3D, 'render.mjs')})")
    print("\n[UNIVERSAL MODULAR COMBINER - 15 TROUBLE-FREE COMBOS]")
    print(f"  9. Combo Runner: {os.path.join(DOC_SCRIPTS, 'combo_runner.py')} (Guide: guides/COMBINATIONS.md)")
    print("     Flags: --combo --shader=<look|timeline> --brush=<preset> --lemo=<slug> --post=<hdr|gtao|crt|none>\n")


def list_styles():
    print("\n=== GAP-ONLY 3D-ANIMATOR SHADER STYLES ===")
    for s in ['lit', 'clay', 'paper', 'shadow', 'blueprint', 'toon', 'voxel', 'thermal', 'synth', 'chrome', 'neon', 'mix']:
        print(f"  - {s}")

    print("\n=== GAP-ONLY LEMO-OPUSCAR FILM STYLES ===")
    if os.path.exists(LEMO_STYLES):
        styles = [s for s in sorted(os.listdir(LEMO_STYLES)) if os.path.isdir(os.path.join(LEMO_STYLES, s)) and not s.startswith(('_', '.'))]
        for i, s in enumerate(styles, 1):
            print(f"  {i:3d}. {s}")
    print("\nUse --list-gap-styles for Step 5(1) consultation options.\n")


def main():
    parser = argparse.ArgumentParser(description="Documentary 3D by Ashu Dalal Version 3 - Master Studio CLI")
    parser.add_argument("--list-engines", action="store_true", help="Show engine hierarchy and active sound mode")
    parser.add_argument("--list-styles", action="store_true", help="List all gap-only Lemo & 3D styles")
    parser.add_argument("--list-combos", action="store_true", help="List all 15 verified modular combinations (see guides/COMBINATIONS.md)")
    parser.add_argument("--combo", action="store_true", help="Run Universal Modular Combo Engine (combine 3D-Animator, p5.brush, Lemo, photos, handheld)")
    parser.add_argument("--shader", type=str, default="lit", help="3D-Animator shader or timeline for --combo (e.g. paper or 0:lit,2.5:blueprint)")
    parser.add_argument("--brush", type=str, default="none", help="p5.brush texture preset for --combo (watercolor, charcoal, hatching, marker, flow_field, pencil_hb)")
    parser.add_argument("--lemo", type=str, default="none", help="Lemo-Opuscar style slug for --combo (e.g. dark-documentary)")
    parser.add_argument("--post", type=str, default="hdr", choices=["hdr", "gtao", "crt", "none"], help="Post-FX pass for --combo")
    parser.add_argument("--photo", type=str, default="", help="Optional /assets/... photo card with readability lock for --combo")
    parser.add_argument("--width", type=int, default=1920, help="Frame width for --combo (e.g. 1920 or 1080)")
    parser.add_argument("--height", type=int, default=1080, help="Frame height for --combo (e.g. 1080 or 1920)")
    parser.add_argument("--total", type=float, default=6.0, help="Duration in seconds for --combo")
    parser.add_argument("--n", type=int, default=4, help="Sub-frame samples for --combo (4=preview, 16=stills, 48=master)")
    parser.add_argument("--video", action="store_true", help="Render MP4 video in --combo mode")
    parser.add_argument("--audio", type=str, help="Mastered audio track to mux in --combo mode")
    parser.add_argument("--handheld-csv", type=str, help="Motion CSV for real handheld camera shake pass")
    parser.add_argument("--project", type=str, default="", help="Project folder path for --combo /assets resolution")
    parser.add_argument("--workflow", action="store_true", help="Show the canonical 5-Step Director Workflow")
    parser.add_argument("--suggest-topics", action="store_true", help="Step 1: Print curated documentary topics")
    parser.add_argument("--list-gap-styles", action="store_true", help="Step 5(1): List styles for the 3 gap fallback engines")
    parser.add_argument("--sync-audio", type=str, help="Step 4: Run WhisperX / Whisper word-level alignment on audio")
    parser.add_argument("--fetch-assets", type=str, help="Step 3: Download & verify real internet/social assets (multi-source)")
    parser.add_argument("--max", type=int, default=8, help="Max assets to download for --fetch-assets")
    parser.add_argument("--sources", type=str, default="all", help="Sources for --fetch-assets (all or wikimedia,wikipedia,openverse,archive,loc,nasa)")
    parser.add_argument("--from-urls", type=str, default="", help="Comma-separated direct image URLs found via full web/social research")
    parser.add_argument("--tags", type=str, default="", help="Bilingual/phonetic alias tags for --fetch-assets (for WhisperX Hindi/Hinglish sync)")
    parser.add_argument("--fetch-sfx", type=str, help="Openverse: Fetch real CC-licensed SFX (comma-separated, e.g. whoosh,paper,stamp)")
    parser.add_argument("--fetch-music", type=str, help="Openverse: Search query for ambient documentary music bed")
    parser.add_argument("--sound-mode", type=str, choices=["openverse", "legacy_synth"], help="Switch default sound engine between openverse and legacy_synth")
    parser.add_argument("--auto-intake", type=str, help="Run Step 4 WhisperX sync intake on audio file")
    parser.add_argument("--render-board", action="store_true", help="PRIMARY: Render Evidence Board via board_engine.py")
    parser.add_argument("--script", type=str, default="", help="Custom project board_engine.py script path for --render-board")
    parser.add_argument("--render-3d", action="store_true", help="GAP FALLBACK: Render Three.js 3D scene via headless Chrome")
    parser.add_argument("--render-brush", action="store_true", help="GAP FALLBACK: Render p5.brush animation via headless Chrome")
    parser.add_argument("--style", type=str, default="lit", help="Style name for 3D render")
    parser.add_argument("--out", type=str, default="out/final.mp4", help="Output file path / directory")
    parser.add_argument("--stills", type=str, help="Comma-separated timestamps for still captures (e.g. 1.0,2.5)")

    args, _ = parser.parse_known_args()

    if args.sound_mode:
        set_sound_mode(args.sound_mode)
        return

    if args.list_engines:
        list_engines()
        return

    if args.list_styles:
        list_styles()
        return

    if args.list_combos or args.combo:
        combo_script = os.path.join(DOC_SCRIPTS, "combo_runner.py")
        if args.list_combos:
            subprocess.run([sys.executable, combo_script, "--list"], check=True)
            return
        cmd = [
            sys.executable, combo_script,
            f"--shader={args.shader}", f"--brush={args.brush}",
            f"--lemo={args.lemo}", f"--post={args.post}",
            f"--width={args.width}", f"--height={args.height}",
            f"--total={args.total}", f"--n={args.n}", f"--out={args.out}"
        ]
        if args.photo:
            cmd.append(f"--photo={args.photo}")
        if args.project:
            cmd.append(f"--project={args.project}")
        if args.stills:
            cmd.append(f"--stills={args.stills}")
        elif args.video:
            cmd.append("--video")
            if args.audio:
                cmd.append(f"--audio={args.audio}")
        if args.handheld_csv:
            cmd.append(f"--handheld-csv={args.handheld_csv}")
        subprocess.run(cmd, check=True)
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
            print("\n=== DOCUMENTARY 3D BY ASHU DALAL - CANONICAL 5-STEP WORKFLOW ===")
            subprocess.run([sys.executable, director_script, "--suggest-topics"], check=True)
            print("Next steps after voiceover audio intake:")
            print("  Step 3 (Zero-Fake Assets): python studio.py --fetch-assets='<keywords>'")
            print("  Step 4 (WhisperX Sync):    python studio.py --sync-audio=<voiceover.wav>")
            print("  Openverse SFX & Music:     python studio.py --fetch-sfx='whoosh,paper,stamp'\n")
            return

    if args.fetch_sfx or args.fetch_music:
        ov_script = os.path.join(DOC_SCRIPTS, "openverse_sfx.py")
        out_dir = args.out if not args.out.endswith(".mp4") else "sound"
        cmd = [sys.executable, ov_script, "--out", out_dir]
        if args.fetch_sfx:
            cmd.extend(["--sfx", args.fetch_sfx])
        if args.fetch_music:
            cmd.extend(["--music", args.fetch_music])
        subprocess.run(cmd, check=True)
        return

    if args.sync_audio:
        sync_script = os.path.join(DOC_SCRIPTS, "audio_sync.py")
        out_json = args.out if args.out.endswith(".json") else "sync_timeline.json"
        subprocess.run([sys.executable, sync_script, "--audio", args.sync_audio, "--out", out_json], check=True)
        return

    if args.fetch_assets:
        fetch_script = os.path.join(DOC_SCRIPTS, "asset_fetcher.py")
        out_dir = args.out if not args.out.endswith(".mp4") else "assets"
        cmd = [sys.executable, fetch_script, "--query", args.fetch_assets, "--out", out_dir, "--max", str(args.max), "--sources", args.sources]
        if args.from_urls:
            cmd.extend(["--from-urls", args.from_urls])
        if args.tags:
            cmd.extend(["--tags", args.tags])
        subprocess.run(cmd, check=True)
        return

    if args.auto_intake:
        sync_script = os.path.join(DOC_SCRIPTS, "audio_sync.py")
        subprocess.run([sys.executable, sync_script, "--audio", args.auto_intake, "--out", "sync_timeline.json"], check=True)
        return

    if args.render_board:
        board_script = os.path.abspath(args.script) if args.script else os.path.join(DOC_SCRIPTS, "board_engine.py")
        cmd = [sys.executable, board_script]
        if args.stills:
            cmd.extend(["stills", args.stills])
        else:
            cmd.extend(["full", "0", "300", args.out])
        subprocess.run(cmd, cwd=os.path.dirname(board_script), check=True)
        return

    if args.render_3d:
        cmd = ["node", "render.mjs"]
        if args.stills:
            cmd.append(f"--stills={args.stills}")
            if args.style:
                cmd.append(f"--style={args.style}")
            if args.out != "out/final.mp4":
                cmd.append(f"--out={args.out}")
        else:
            cmd.extend(["--video", f"--out={args.out}", f"--style={args.style}"])
        subprocess.run(cmd, cwd=KIT_3D, check=True)
        return

    if args.render_brush:
        cmd = ["node", "render_brush.mjs"]
        if args.stills:
            cmd.append(f"--stills={args.stills}")
            if args.out != "out/final.mp4":
                cmd.append(f"--out={args.out}")
        else:
            cmd.extend(["--video", f"--out={args.out}"])
        subprocess.run(cmd, cwd=KIT_BRUSH, check=True)
        return

    list_engines()


if __name__ == "__main__":
    main()
