#!/usr/bin/env python3
"""
Cross-platform laptop reel generator.
Puts the film on the screen of a laptop photo, creates a 1080x1920 reel,
adds optional realistic hand shake via handheld.py, and applies fixed overlays.

Usage:
  python laptop_reel.py <laptop_photo.png> <film.mp4> <SX> <SY> <SW> <SH> <out.mp4> [motion.csv] [overlay.png]

Parameters:
  laptop_photo.png: 1080x1920 background mockup photo
  film.mp4: Rendered film/documentary clip
  SX SY SW SH: Screen rectangle coordinates in pixels (X, Y, Width, Height)
  out.mp4: Output 1080x1920 video path
  motion.csv: Optional camera motion data from phone_motion.py
  overlay.png: Optional 1080x1920 transparent overlay PNG
"""
import os
import sys
import subprocess

if len(sys.argv) < 8:
    print("Usage: python laptop_reel.py <laptop_photo.png> <film.mp4> <SX> <SY> <SW> <SH> <out.mp4> [motion.csv] [overlay.png]")
    sys.exit(1)

photo = sys.argv[1]
film = sys.argv[2]
sx = int(sys.argv[3])
sy = int(sys.argv[4])
sw = int(sys.argv[5])
sh = int(sys.argv[6])
out = sys.argv[7]
motion = sys.argv[8] if len(sys.argv) > 8 and sys.argv[8] and sys.argv[8] != "-" else None
overlay = sys.argv[9] if len(sys.argv) > 9 and sys.argv[9] else None

here = os.path.dirname(os.path.abspath(__file__))
handheld_script = os.path.join(here, "handheld.py")

# Calculate frame dimensions & anchors
fh = int(sw * 9 / 16 / 2) * 2
fy = int(sy + (sh - fh) / 2)
ax = float(sx + sw / 2)
ay = float(sy + sh / 2)

comp = (
    f"[1:v]fps=30,scale={sw}:{fh}:flags=lanczos,format=rgba[film];"
    f"[0:v]scale=1080:1920,format=rgba[pl];"
    f"[pl][film]overlay={sx}:{fy}:shortest=1,format=rgb24[v]"
)

if motion and os.path.exists(motion):
    print(f"Applying realistic hand motion from {motion}...")
    p1_cmd = [
        "ffmpeg", "-v", "error", "-loop", "1", "-framerate", "30",
        "-i", photo, "-i", film,
        "-filter_complex", comp,
        "-map", "[v]", "-f", "rawvideo", "-"
    ]
    p2_cmd = [
        sys.executable, handheld_script, motion, "1080", "1920", str(ax), str(ay)
    ]
    p3_inputs = ["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", "1080x1920", "-r", "30", "-i", "-", "-i", film]
    
    if overlay and os.path.exists(overlay):
        p3_inputs.extend(["-i", overlay])
        f_comp = "[0:v][2:v]overlay=0:0,format=yuv420p[o]"
    else:
        f_comp = "[0:v]format=yuv420p[o]"
        
    p3_cmd = p3_inputs + [
        "-filter_complex", f_comp,
        "-map", "[o]", "-map", "1:a?",
        "-c:v", "libx264", "-crf", "16", "-preset", "slow",
        "-c:a", "aac", "-b:a", "256k", "-shortest", "-movflags", "+faststart",
        out
    ]
    
    p1 = subprocess.Popen(p1_cmd, stdout=subprocess.PIPE)
    p2 = subprocess.Popen(p2_cmd, stdin=p1.stdout, stdout=subprocess.PIPE)
    p1.stdout.close()
    p3 = subprocess.Popen(p3_cmd, stdin=p2.stdout)
    p2.stdout.close()
    p3.communicate()
else:
    print("Encoding stationary laptop reel...")
    inputs = ["ffmpeg", "-v", "error", "-y", "-loop", "1", "-framerate", "30", "-i", photo, "-i", film]
    if overlay and os.path.exists(overlay):
        inputs.extend(["-i", overlay])
        f_comp = f"{comp};[v][2:v]overlay=0:0,format=yuv420p[o]"
    else:
        f_comp = f"{comp};[v]format=yuv420p[o]"
        
    cmd = inputs + [
        "-filter_complex", f_comp,
        "-map", "[o]", "-map", "1:a?",
        "-c:v", "libx264", "-crf", "16", "-preset", "slow",
        "-c:a", "aac", "-b:a", "256k", "-shortest", "-movflags", "+faststart",
        out
    ]
    subprocess.run(cmd, check=True)

print(f"Reel successfully created: {out}")
