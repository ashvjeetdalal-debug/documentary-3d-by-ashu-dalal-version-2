#!/usr/bin/env python3
"""
Cross-platform audio mixing and multiplexing script.
Usage: python mix_and_mux.py video.mp4 voiceover.(mp3|wav) bed.wav out.mp4
Ducks the sound bed under the voice, normalises to -14 LUFS, and encodes shareable H.264 (CRF 24).
"""
import sys, subprocess

if len(sys.argv) < 5:
    print("Usage: python mix_and_mux.py video.mp4 voiceover.(mp3|wav) bed.wav out.mp4")
    sys.exit(1)

video, vo, bed, out = sys.argv[1:5]
filter_complex = (
    "[1:a]aresample=48000,asplit=2[v1][v2];"
    "[2:a]aformat=channel_layouts=mono[b];"
    "[b][v1]sidechaincompress=threshold=0.05:ratio=6:attack=20:release=300[bd];"
    "[bd][v2]amix=inputs=2:normalize=0,loudnorm=I=-14:TP=-1.5[a]"
)
cmd = [
    "ffmpeg", "-loglevel", "error", "-y",
    "-i", video, "-i", vo, "-i", bed,
    "-filter_complex", filter_complex,
    "-map", "0:v", "-map", "[a]",
    "-c:v", "libx264", "-preset", "veryfast", "-crf", "24", "-pix_fmt", "yuv420p",
    "-c:a", "aac", "-b:a", "192k", "-movflags", "+faststart",
    out
]
subprocess.run(cmd, check=True)
print(f"Delivered multiplexed video: {out}")
