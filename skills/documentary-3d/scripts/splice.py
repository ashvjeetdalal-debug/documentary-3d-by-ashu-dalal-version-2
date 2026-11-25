#!/usr/bin/env python3
"""
Cross-platform frame splicing script.
Replace frames [start_frame, end_frame) of board.mp4 with insert.mp4 (same size/fps).
Usage: python splice.py board.mp4 insert.mp4 start_frame end_frame out.mp4
"""
import os, sys, subprocess

if len(sys.argv) < 6:
    print("Usage: python splice.py board.mp4 insert.mp4 start_frame end_frame out.mp4")
    sys.exit(1)

board, insert, sf, ef, out = sys.argv[1:6]
os.makedirs(os.path.dirname(os.path.abspath(out)), exist_ok=True)
filter_complex = f"[0:v]trim=end_frame={sf},setpts=PTS-STARTPTS[a];[0:v]trim=start_frame={ef},setpts=PTS-STARTPTS[c];[a][1:v][c]concat=n=3:v=1[v]"
cmd = [
    "ffmpeg", "-loglevel", "error", "-y",
    "-i", board, "-i", insert,
    "-filter_complex", filter_complex,
    "-map", "[v]",
    "-c:v", "libx264", "-preset", "veryfast", "-crf", "18", "-pix_fmt", "yuv420p",
    out
]
subprocess.run(cmd, check=True)
print(f"Spliced video written to {out}")
