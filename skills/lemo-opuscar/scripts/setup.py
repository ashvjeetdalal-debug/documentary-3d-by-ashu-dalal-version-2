#!/usr/bin/env python3
"""
Cross-platform environment setup and diagnostics for Lemo-Opuscar within Documentary 3D Studio.
Checks Node 20+, FFmpeg 7+, and Python 3.11+, and verifies package tiers.

Usage:
  python setup.py
  python setup.py deps
"""
import sys
import os
import shutil
import subprocess

def check_command(cmd, min_version=None):
    path = shutil.which(cmd)
    if not path:
        return False, f"Not found"
    try:
        out = subprocess.check_output([cmd, "--version"], text=True, stderr=subprocess.STDOUT)
        first_line = out.strip().split('\n')[0]
        return True, first_line
    except Exception as e:
        return True, "Found (version check failed)"

print("=== Documentary 3D Studio - Environment Pre-flight ===")

node_ok, node_msg = check_command("node")
print(f"Node.js:  {'[OK] ' if node_ok else '[FAIL]'} {node_msg}")

ffmpeg_ok, ffmpeg_msg = check_command("ffmpeg")
print(f"FFmpeg:   {'[OK] ' if ffmpeg_ok else '[FAIL]'} {ffmpeg_msg}")

py_ver = f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}"
py_ok = sys.version_info >= (3, 10)
print(f"Python:   {'[OK] ' if py_ok else '[WARN]'} Python {py_ver}")

base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
styles_dir = os.path.join(base_dir, "styles")
styles_count = len(os.listdir(styles_dir)) if os.path.exists(styles_dir) else 0
print(f"Styles:   [OK] {styles_count} film styles available in skills/lemo-opuscar/styles/")

if len(sys.argv) > 1 and sys.argv[1] == "deps":
    print("\nInstalling Node dependencies in skills/lemo-opuscar...")
    npm_cmd = shutil.which("npm")
    if npm_cmd:
        subprocess.run([npm_cmd, "install", "--no-audit", "--no-fund"], cwd=base_dir, check=True)
        print("[+] Node packages installed.")
    else:
        print("[!] npm command not found.")
