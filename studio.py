#!/usr/bin/env python3
"""
Documentary 3D by Ashu Dalal Version 3 - Master Studio CLI
Clean 3 Independent Engines (Zero Compromised Combos):
  1. MAIN DOCUMENTARY SYSTEM: Ashu Dalal Evidence-Board & Vintage 2D (board_engine.py, vintage_engine.py)
  2. GAP-ONLY VISUAL ENGINE (FULL POTENTIAL): Lemo-Opuscar Studio (99 film styles, DIRECTOR.md, TECHNIQUE.md, core/ post)
     - Used strictly for no-asset documentary gaps after deep internet visual research + plan.md consultation.
  3. ON-DEMAND 3D ENGINE (ANYTIME & FULL POTENTIAL): 3D-Animator / Three.js (skills/3d-animator/kit/)
     - Independent, user-controlled anytime/anywhere at full HDR 48x sub-frame potential + 12 styles.js looks.
  + AUTOMATED INTAKE & AUDIO:
    - WhisperX Word Alignment (audio_sync.py)
    - Zero-Fake Archival Asset Fetcher (asset_fetcher.py) & CC0 3D Model Fetcher (model_fetcher.py)
    - On-Demand YouTube & Multi-Source Free Documentary SFX (openverse_sfx.py; mix.py clamps SFX strictly 15%-20%)
"""
import os
import sys
import json
import argparse
import subprocess

ROOT = os.path.dirname(os.path.abspath(__file__))
DOC_SCRIPTS = os.path.join(ROOT, "skills", "documentary-3d", "scripts")
ANIM_3D_KIT = os.path.join(ROOT, "skills", "3d-animator", "kit")
LEMO_STYLES = os.path.join(ROOT, "skills", "lemo-opuscar", "styles")
SOUND_CONFIG = os.path.join(DOC_SCRIPTS, "sound_config.json")


def get_sound_mode():
    if os.path.exists(SOUND_CONFIG):
        try:
            with open(SOUND_CONFIG, encoding="utf-8-sig") as f:
                return json.load(f).get("active_engine", "openverse")
        except Exception:
            pass
    return "openverse"


def set_sound_mode(mode):
    if mode not in ("openverse", "legacy_synth"):
        raise ValueError("Sound mode must be 'openverse' or 'legacy_synth'")
    cfg = {}
    if os.path.exists(SOUND_CONFIG):
        with open(SOUND_CONFIG, encoding="utf-8-sig") as f:
            cfg = json.load(f)
    cfg["active_engine"] = mode
    with open(SOUND_CONFIG, "w", encoding="utf-8") as f:
        json.dump(cfg, f, indent=2)
    print(f"[STUDIO] Sound engine mode switched to: {mode}")


def list_engines():
    sound_mode = get_sound_mode()
    styles_count = len([s for s in os.listdir(LEMO_STYLES) if os.path.isdir(os.path.join(LEMO_STYLES, s)) and not s.startswith(('_', '.'))]) if os.path.exists(LEMO_STYLES) else 0
    print("\n=== DOCUMENTARY 3D BY ASHU DALAL VERSION 3 - 3 INDEPENDENT ENGINES ===")
    print("\n[1. MAIN DOCUMENTARY SYSTEM (PRIMARY ARCHIVAL BACKBONE)]")
    print("  - Ashu Dalal Evidence-Board & Vintage 2D (board_engine.py, vintage_engine.py, splice.py, mix_and_mux.py)")

    print("\n[2. GAP VISUAL ENGINE (NO-ASSET GAPS ONLY - FULL POTENTIAL)]")
    print(f"  - Lemo-Opuscar Studio ({styles_count} styles + DIRECTOR.md + TECHNIQUE.md + GTAO/DOF + CRT)")
    print("    Always perform deep internet visual research -> write plan.md -> build full Lemo style implementation.")

    print("\n[3. 3D-ANIMATOR ENGINE (ANYTIME / ANYWHERE - 100% FULL POTENTIAL)]")
    print(f"  - Standalone 3D Kit: {ANIM_3D_KIT}")
    print("    Full 48x Halton HDR motion blur, thin-lens bokeh DOF, cosine sky soft shadows & 12 styles.js looks.")

    print("\n[INTAKE, 3D MODELS & DOCUMENTARY AUDIO]")
    print(f"  - WhisperX Speech Sync & Gap Mapping: {os.path.join(DOC_SCRIPTS, 'audio_sync.py')}")
    print(f"  - Zero-Fake Archival Asset Fetcher:   {os.path.join(DOC_SCRIPTS, 'asset_fetcher.py')}")
    print(f"  - CC0 / Open 3D Model Fetcher (.glb): {os.path.join(DOC_SCRIPTS, 'model_fetcher.py')}")
    print("  - Script & Research Gap Planner:      python studio.py --plan")
    print(f"  - Sound System (Active Mode: {sound_mode} | SFX Clamped 15%-20%):")
    print(f"      * YouTube + Free Internet SFX:    {os.path.join(DOC_SCRIPTS, 'openverse_sfx.py')}")
    print("      * Legacy Synth (sound_bed.py):    SILENCED BY DEFAULT (--sound-mode=legacy_synth)\n")


def list_styles():
    print("\n=== 3D-ANIMATOR SHADER STYLES (12 - FOR ON-DEMAND 3D SCENES) ===")
    for s in ['lit', 'clay', 'paper', 'shadow', 'blueprint', 'toon', 'voxel', 'thermal', 'synth', 'chrome', 'neon', 'mix']:
        print(f"  - {s}")

    print("\n=== LEMO-OPUSCAR FILM STYLES (FOR DOCUMENTARY GAPS AT FULL POTENTIAL) ===")
    if os.path.exists(LEMO_STYLES):
        styles = [s for s in sorted(os.listdir(LEMO_STYLES)) if os.path.isdir(os.path.join(LEMO_STYLES, s)) and not s.startswith(('_', '.'))]
        for i, s in enumerate(styles, 1):
            print(f"  {i:3d}. {s}")
    print("\nUse --list-gap-styles for Step 5(1) Lemo-Opuscar gap consultation options.\n")


def main():
    parser = argparse.ArgumentParser(description="Documentary 3D by Ashu Dalal Version 3 - Master Studio CLI")
    parser.add_argument("--list-engines", action="store_true", help="Show the 3 independent engines and audio setup")
    parser.add_argument("--list-styles", action="store_true", help="List all Lemo (gap) & 3D-Animator styles")
    parser.add_argument("--workflow", action="store_true", help="Show the canonical 5-Step Director Workflow")
    parser.add_argument("--plan", action="store_true", help="Generate internet-research-ready plan.md mapping script & Lemo gaps")
    parser.add_argument("--topic", type=str, default="Documentary Production", help="Documentary topic for --plan")
    parser.add_argument("--script-file", type=str, default="", help="Script file path for --plan")
    parser.add_argument("--mapping", type=str, default="", help="Step 4 project_mapping.json path for --plan")
    parser.add_argument("--research-file", type=str, default="", help="Internet research notes file for --plan")
    parser.add_argument("--suggest-topics", action="store_true", help="Step 1: Print curated documentary topics")
    parser.add_argument("--list-gap-styles", action="store_true", help="Step 5(1): List Lemo-Opuscar styles for no-asset gaps")
    parser.add_argument("--sync-audio", type=str, help="Step 4: Run WhisperX / Whisper word-level alignment on audio")
    parser.add_argument("--fetch-assets", type=str, help="Step 3: Download & verify real internet/social assets (multi-source)")
    parser.add_argument("--fetch-models", type=str, help="Download CC0 / open 3D .glb/.gltf models via Poly Haven / --from-urls")
    parser.add_argument("--res", type=str, default="1k", choices=["1k", "2k", "4k"], help="Resolution for --fetch-models")
    parser.add_argument("--max", type=int, default=8, help="Max assets/models to download")
    parser.add_argument("--sources", type=str, default="all", help="Sources for --fetch-assets or --fetch-sfx/--fetch-music")
    parser.add_argument("--from-urls", type=str, default="", help="Comma-separated direct URLs (images, 3D models, or YouTube/audio SFX)")
    parser.add_argument("--tags", type=str, default="", help="Bilingual/phonetic alias tags for --fetch-assets / --fetch-models")
    parser.add_argument("--fetch-sfx", type=str, help="Fetch free documentary SFX on demand from YouTube/Openverse/Wikimedia/Archive")
    parser.add_argument("--fetch-music", type=str, help="Search query for ambient documentary music bed")
    parser.add_argument("--sound-mode", type=str, choices=["openverse", "legacy_synth"], help="Switch default sound engine between openverse and legacy_synth")
    parser.add_argument("--auto-intake", type=str, help="Run Step 4 WhisperX sync intake on audio file")
    parser.add_argument("--render-board", action="store_true", help="PRIMARY: Render Evidence Board via board_engine.py")
    parser.add_argument("--script", type=str, default="", help="Custom project board_engine.py script path for --render-board")
    parser.add_argument("--render-3d", action="store_true", help="3D-ANIMATOR: Render standalone Three.js 3D scene via headless Chrome at full potential")
    parser.add_argument("--project", type=str, default="", help="Custom 3D-Animator project folder path for --render-3d")
    parser.add_argument("--style", type=str, default="lit", help="Style name for --render-3d (styles.js)")
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

    if args.plan or args.suggest_topics or args.list_gap_styles or args.workflow:
        director_script = os.path.join(DOC_SCRIPTS, "director_workflow.py")
        if args.plan:
            out_plan = "plan.md" if args.out == "out/final.mp4" else args.out
            cmd = [sys.executable, director_script, "--plan", "--topic", args.topic, "--out", out_plan]
            if args.script_file:
                cmd.extend(["--script-file", args.script_file])
            if args.mapping:
                cmd.extend(["--mapping", args.mapping])
            if args.research_file:
                cmd.extend(["--research-file", args.research_file])
            subprocess.run(cmd, check=True)
            return
        if args.suggest_topics:
            subprocess.run([sys.executable, director_script, "--suggest-topics"], check=True)
            return
        if args.list_gap_styles:
            subprocess.run([sys.executable, director_script, "--list-gap-styles"], check=True)
            return
        if args.workflow:
            print("\n=== DOCUMENTARY 3D BY ASHU DALAL - CANONICAL 5-STEP WORKFLOW ===")
            subprocess.run([sys.executable, director_script, "--suggest-topics"], check=True)
            print("Next steps after topic + script:")
            print("  Step 1B (Gap Plan):        python studio.py --plan --topic='<topic>' --script-file=script.txt")
            print("  Step 3 (Zero-Fake Assets): python studio.py --fetch-assets='<keywords>'")
            print("  Step 4 (WhisperX Sync):    python studio.py --sync-audio=<voiceover.wav>")
            print("  Step 5 (Lemo Gaps):        Deep internet research -> Lemo-Opuscar full potential")
            print("  Free Documentary SFX:      python studio.py --fetch-sfx='whoosh,paper,stamp'\n")
            return

    if args.fetch_models is not None and (args.fetch_models or args.from_urls):
        model_script = os.path.join(DOC_SCRIPTS, "model_fetcher.py")
        out_dir = "models" if args.out == "out/final.mp4" else args.out
        cmd = [sys.executable, model_script, "--query", args.fetch_models, "--out", out_dir, "--max", str(min(args.max, 6)), "--res", args.res]
        if args.from_urls:
            cmd.extend(["--from-urls", args.from_urls])
        if args.tags:
            cmd.extend(["--tags", args.tags])
        subprocess.run(cmd, check=True)
        return

    if args.fetch_sfx or args.fetch_music or (args.from_urls and not args.fetch_assets):
        ov_script = os.path.join(DOC_SCRIPTS, "openverse_sfx.py")
        out_dir = "sound" if args.out == "out/final.mp4" else args.out
        cmd = [sys.executable, ov_script, "--out", out_dir, "--sources", args.sources]
        if args.fetch_sfx:
            cmd.extend(["--sfx", args.fetch_sfx])
        if args.fetch_music:
            cmd.extend(["--music", args.fetch_music])
        if args.from_urls:
            cmd.extend(["--from-urls", args.from_urls])
        subprocess.run(cmd, check=True)
        return

    if args.sync_audio:
        sync_script = os.path.join(DOC_SCRIPTS, "audio_sync.py")
        out_json = "sync_timeline.json" if args.out == "out/final.mp4" else args.out
        subprocess.run([sys.executable, sync_script, "--audio", args.sync_audio, "--out", out_json], check=True)
        return

    if args.fetch_assets is not None and (args.fetch_assets or args.from_urls):
        fetch_script = os.path.join(DOC_SCRIPTS, "asset_fetcher.py")
        out_dir = "assets" if args.out == "out/final.mp4" else args.out
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
            cmd.extend(["full", "0", "300", os.path.abspath(args.out)])
        subprocess.run(cmd, cwd=os.path.dirname(board_script), check=True)
        return

    if args.render_3d:
        target_kit = ANIM_3D_KIT
        if args.project:
            cand = os.path.abspath(args.project)
            if os.path.exists(os.path.join(cand, "render.mjs")):
                target_kit = cand
            else:
                raise FileNotFoundError(f"--project folder does not contain render.mjs: {cand}")
        cmd = ["node", "render.mjs"]
        if args.stills:
            cmd.append(f"--stills={args.stills}")
            if args.style:
                cmd.append(f"--style={args.style}")
            out_dir = os.path.abspath("stills" if args.out == "out/final.mp4" else args.out)
            cmd.append(f"--out={out_dir}")
        else:
            cmd.extend(["--video", f"--out={os.path.abspath(args.out)}", f"--style={args.style}"])
        subprocess.run(cmd, cwd=target_kit, check=True)
        return

    list_engines()


if __name__ == "__main__":
    main()
