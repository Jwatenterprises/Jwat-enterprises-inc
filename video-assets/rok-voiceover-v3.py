"""Generate female voiceover (AriaNeural) for ROK Financial TikTok.
V3: Natural pacing — voiceover drives the slide timing."""
import asyncio
import json
import os
import sys
import subprocess
from pathlib import Path

sys.stdout.reconfigure(encoding='utf-8')

import edge_tts

VOICE = "en-US-AriaNeural"
SCRIPT_DIR = Path(__file__).parent
SEGMENTS_DIR = SCRIPT_DIR / "rok-vo-segments"
FINAL_AUDIO = SCRIPT_DIR / "rok-funding-beat.wav"
TIMING_FILE = SCRIPT_DIR / "rok-slide-timing.json"

# Natural pacing — no compression. Slight speed boost for TikTok energy.
SEGMENTS = [
    ("seg1.mp3",
     "One point six eight million dollars. Funded in three days.",
     "+2%"),
    ("seg2.mp3",
     "A retail business went through ROK Financial. Got funded. Grew. "
     "Came back for more. ROK funded them again.",
     "+5%"),
    ("seg3.mp3",
     "Apply once, five minutes. Three hundred lenders compete. "
     "Offers in twenty four hours. Funded in days.",
     "+5%"),
    ("seg4.mp3",
     "Banks take ninety days. ROK takes twenty four hours. "
     "All credit profiles. No hard credit pull.",
     "+5%"),
    ("seg5.mp3",
     "Construction. Restaurants. Trucking. Any business. Ten K to five million.",
     "+5%"),
    ("seg6.mp3",
     "Check what you qualify for. Five minutes. Link in bio.",
     "+2%"),
]

GAP = 0.5  # seconds between segments


def get_duration(path):
    probe = subprocess.run(
        ["ffprobe", "-v", "error", "-show_entries", "format=duration",
         "-of", "csv=p=0", str(path)],
        capture_output=True, text=True
    )
    return float(probe.stdout.strip()) if probe.stdout.strip() else 0


async def generate_segments():
    SEGMENTS_DIR.mkdir(parents=True, exist_ok=True)

    durations = []
    for filename, text, rate in SEGMENTS:
        out_path = SEGMENTS_DIR / filename
        print(f"  🎙️  Generating: {filename}")
        communicate = edge_tts.Communicate(text=text, voice=VOICE, rate=rate, pitch="+0Hz")
        await communicate.save(str(out_path))
        dur = get_duration(out_path)
        durations.append(dur)
        print(f"       Duration: {dur:.1f}s (natural)")

    return durations


def calculate_timing(durations):
    """Calculate slide start/end times from natural VO durations."""
    timing = []
    t = 0.0
    for i, dur in enumerate(durations):
        start = t
        end = t + dur + 0.3  # small visual buffer after speech ends
        timing.append({
            "slide": i + 1,
            "start": round(start, 1),
            "end": round(end, 1),
            "vo_duration": round(dur, 1),
        })
        t = end + GAP

    total = timing[-1]["end"]
    print(f"\n📐 Slide Timing (total: {total:.1f}s):")
    for s in timing:
        print(f"   Slide {s['slide']}: {s['start']}s → {s['end']}s (VO: {s['vo_duration']}s)")

    # Save timing for the renderer
    with open(TIMING_FILE, "w") as f:
        json.dump({"slides": timing, "total_duration": round(total, 1)}, f, indent=2)
    print(f"   Saved to: {TIMING_FILE.name}")

    return timing, total


def combine_and_mix(timing, total_duration):
    """Combine VO segments at calculated times with subtle background."""
    print("\n🔧 Combining segments with background...")

    total_dur_ceil = int(total_duration) + 1

    # Generate subtle ambient pad
    bg_path = SEGMENTS_DIR / "bg_ambient.wav"
    bg_cmd = [
        "ffmpeg", "-y",
        "-f", "lavfi", "-i",
        (
            f"aevalsrc="
            f"'sin(220*2*PI*t)*0.015"
            f"+sin(277*2*PI*t)*0.012"
            f"+sin(330*2*PI*t)*0.012"
            f"+sin(110*2*PI*t)*exp(-4*mod(t*120/60,1))*0.025"
            f"':s=44100:c=stereo:d={total_dur_ceil}"
        ),
        "-af", "highpass=f=80,lowpass=f=8000,volume=0.4",
        "-c:a", "pcm_s16le",
        str(bg_path),
    ]
    subprocess.run(bg_cmd, capture_output=True, text=True)

    # Build ffmpeg filter
    inputs = ["-i", str(bg_path)]
    filter_parts = ["[0]volume=0.25[bg]"]

    for i, slide in enumerate(timing):
        seg_path = SEGMENTS_DIR / SEGMENTS[i][0]
        inputs += ["-i", str(seg_path)]
        delay_ms = int(slide["start"] * 1000)
        idx = i + 1
        filter_parts.append(
            f"[{idx}]aformat=sample_rates=44100:channel_layouts=mono,"
            f"adelay={delay_ms}|{delay_ms},volume=1.6[s{i}]"
        )

    vo_mix = "".join(f"[s{i}]" for i in range(len(timing)))
    n_inputs = len(timing) + 1
    filter_parts.append(
        f"[bg]{vo_mix}amix=inputs={n_inputs}:duration=longest:normalize=0,"
        f"apad=whole_dur={total_dur_ceil},alimiter=limit=0.95[out]"
    )

    filter_str = ";".join(filter_parts)

    cmd = ["ffmpeg", "-y"] + inputs + [
        "-filter_complex", filter_str,
        "-map", "[out]",
        "-c:a", "pcm_s16le", "-ar", "44100",
        str(FINAL_AUDIO),
    ]

    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"❌ Mix failed: {result.stderr[:500]}")
        return False

    size_kb = FINAL_AUDIO.stat().st_size // 1024
    print(f"   ✅ Final audio: {FINAL_AUDIO.name} ({size_kb} KB)")
    return True


async def main():
    print("=" * 60)
    print("  ROK Financial — AriaNeural Voiceover V3")
    print("  Natural pacing — VO drives slide timing")
    print("=" * 60)

    durations = await generate_segments()
    timing, total = calculate_timing(durations)
    if combine_and_mix(timing, total):
        print(f"\n✅ Voiceover ready ({total:.0f}s). Slide timing saved.")
        print("   Re-run the video renderer to pick up new timing.")


if __name__ == "__main__":
    asyncio.run(main())
