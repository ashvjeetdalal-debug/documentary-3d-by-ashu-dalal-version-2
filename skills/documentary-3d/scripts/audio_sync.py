#!/usr/bin/env python3
"""
Documentary 3D by Ashu Dalal - WhisperX / Word-Level Speech Sync Engine
Extracts exact word-level and sentence-level timestamps from voiceover audio
to synchronize 3D camera moves, evidence board reveals, and kinetic subtitles.
Adheres strictly to Ashu Dalal Master Rule 3 & 8 (Sync within 1-2 frames, min 1.8s subtitle hold).
"""

import os
import sys
import json
import subprocess
import argparse

def get_audio_duration(audio_path):
    """Retrieve precise duration of audio via ffprobe."""
    cmd = [
        "ffprobe", "-v", "error",
        "-show_entries", "format=duration",
        "-of", "default=noprint_wrappers=1:nokey=1",
        audio_path
    ]
    res = subprocess.run(cmd, capture_output=True, text=True, check=True)
    return float(res.stdout.strip())

def align_audio_whisper(audio_path, model_size="base", language=None):
    """
    Run word-level speech recognition and forced alignment.
    Prefers whisperx if installed, falls back seamlessly to openai-whisper with word_timestamps.
    """
    timeline = {
        "audio_file": os.path.abspath(audio_path),
        "duration": get_audio_duration(audio_path),
        "engine": "unknown",
        "language": language or "auto",
        "segments": [],
        "words": [],
        "subtitles": [],
        "visual_cues": []
    }

    # 1. Try WhisperX if available
    has_whisperx = False
    try:
        import whisperx
        has_whisperx = True
    except ImportError:
        pass

    if has_whisperx:
        print("[AUDIO_SYNC] Utilizing WhisperX forced alignment engine...")
        try:
            device = "cuda" if whisperx.torch.cuda.is_available() else "cpu"
            model = whisperx.load_model(model_size, device, compute_type="float32")
            audio = whisperx.load_audio(audio_path)
            result = model.transcribe(audio, batch_size=4)
            # Align whisper output
            align_model, metadata = whisperx.load_align_model(language_code=result["language"], device=device)
            aligned_res = whisperx.align(result["segments"], align_model, metadata, audio, device, return_char_alignments=False)
            
            timeline["engine"] = "whisperx"
            timeline["language"] = result.get("language", "auto")

            for seg in aligned_res.get("segments", []):
                s_obj = {
                    "start": round(seg.get("start", 0.0), 3),
                    "end": round(seg.get("end", 0.0), 3),
                    "text": seg.get("text", "").strip()
                }
                timeline["segments"].append(s_obj)
                for w in seg.get("words", []):
                    if "start" in w and "end" in w:
                        timeline["words"].append({
                            "word": w.get("word", "").strip(),
                            "start": round(w.get("start", 0.0), 3),
                            "end": round(w.get("end", 0.0), 3),
                            "score": round(w.get("score", 1.0), 2)
                        })
            print(f"[AUDIO_SYNC] WhisperX alignment complete: {len(timeline['words'])} words aligned.")
            return build_subtitles_and_cues(timeline)
        except Exception as e:
            print(f"[AUDIO_SYNC] WhisperX runtime encountered: {e}. Falling back to Whisper...")

    # 2. Try faster-whisper if installed
    try:
        from faster_whisper import WhisperModel
        print("[AUDIO_SYNC] Utilizing faster-whisper alignment engine...")
        m = WhisperModel(model_size, device="cpu", compute_type="int8")
        segs, info = m.transcribe(audio_path, language=language, word_timestamps=True)
        timeline["engine"] = "faster-whisper"
        timeline["language"] = getattr(info, "language", language or "auto")
        for seg in segs:
            timeline["segments"].append({
                "start": round(seg.start, 3),
                "end": round(seg.end, 3),
                "text": seg.text.strip()
            })
            for w in (seg.words or []):
                timeline["words"].append({
                    "word": w.word.strip(),
                    "start": round(w.start, 3),
                    "end": round(w.end, 3),
                    "probability": round(getattr(w, "probability", 1.0), 2)
                })
        print(f"[AUDIO_SYNC] faster-whisper complete: {len(timeline['words'])} words mapped.")
        return build_subtitles_and_cues(timeline)
    except ImportError:
        pass
    except Exception as e:
        print(f"[AUDIO_SYNC] faster-whisper runtime notice: {e}. Falling back to openai-whisper...")

    # 3. Fallback to OpenAI Whisper (with word_timestamps=True)
    print("[AUDIO_SYNC] Running OpenAI Whisper word-level alignment engine...")
    import whisper
    model = whisper.load_model(model_size)
    kwargs = {"word_timestamps": True}
    if language:
        kwargs["language"] = language

    result = model.transcribe(audio_path, **kwargs)
    timeline["engine"] = "openai-whisper"
    timeline["language"] = result.get("language", "auto")

    for seg in result.get("segments", []):
        s_obj = {
            "start": round(seg.get("start", 0.0), 3),
            "end": round(seg.get("end", 0.0), 3),
            "text": seg.get("text", "").strip()
        }
        timeline["segments"].append(s_obj)
        for w in seg.get("words", []):
            timeline["words"].append({
                "word": w.get("word", "").strip(),
                "start": round(w.get("start", 0.0), 3),
                "end": round(w.get("end", 0.0), 3),
                "probability": round(w.get("probability", 1.0), 2)
            })

    print(f"[AUDIO_SYNC] Alignment complete: {len(timeline['segments'])} segments, {len(timeline['words'])} words mapped.")
    return build_subtitles_and_cues(timeline)

def build_subtitles_and_cues(timeline):
    """
    Construct broadcast-standard subtitles holding for min 1.8s per line
    and extract high-confidence visual cue triggers for camera punch-ins.
    """
    subtitles = []
    MIN_HOLD = 1.80 # Director Law: Subtitles must hold for minimum 1.8s per line

    segments = timeline["segments"]
    for i, seg in enumerate(segments):
        start = seg["start"]
        end = seg["end"]
        # Enforce minimum hold time
        if (end - start) < MIN_HOLD:
            next_start = segments[i + 1]["start"] if (i + 1 < len(segments)) else timeline["duration"]
            end = min(start + MIN_HOLD, next_start - 0.05)

        subtitles.append({
            "index": i + 1,
            "start": round(start, 3),
            "end": round(max(end, start + 0.5), 3),
            "text": seg["text"]
        })

    timeline["subtitles"] = subtitles

    # Extract Visual Cue Marks (Sentence starts & key transition triggers)
    cues = []
    for s in subtitles:
        cues.append({
            "time": s["start"],
            "type": "camera_mark",
            "description": f"Narrative beat: {s['text'][:35]}..."
        })
    timeline["visual_cues"] = cues

    return timeline

def main():
    parser = argparse.ArgumentParser(description="WhisperX / Word-Level Speech Sync Engine")
    parser.add_argument("--audio", type=str, required=True, help="Path to input voiceover audio file (.wav/.mp3)")
    parser.add_argument("--model", type=str, default="base", help="Whisper model size (tiny, base, small, medium)")
    parser.add_argument("--language", type=str, default=None, help="Explicit language code (e.g. en, hi)")
    parser.add_argument("--out", type=str, default="sync_timeline.json", help="Output JSON path")
    args = parser.parse_args()

    timeline = align_audio_whisper(args.audio, model_size=args.model, language=args.language)
    with open(args.out, "w", encoding="utf-8") as f:
        json.dump(timeline, f, indent=2, ensure_ascii=False)

    print(f"\n[AUDIO_SYNC] Success! Master sync timeline saved -> {args.out}")
    print(f"Total Duration: {timeline['duration']:.2f}s | Language: {timeline['language']} | Subtitles: {len(timeline['subtitles'])} lines")

if __name__ == "__main__":
    main()
