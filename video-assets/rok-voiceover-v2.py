"""Generate female voiceover (AriaNeural) for ROK Financial TikTok.
V2: Time-compress each segment to fit its slide window exactly."""
import asyncio
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

# (filename, slide_start, slide_end, text, rate)
SEGMENTS = [
    ("seg1.mp3", 0.0, 4.8,
     "One point six eight million dollars. Funded in three days.",
     "+5%"),
    ("seg2.mp3", 5.2, 11.5,
     "A retail business went through ROK Financial. Got funded. Grew. "
     "Came back for more. ROK funded them again.",
     "+8%"),
    ("seg3.mp3", 12.3, 18.5,
     "Apply once, five minutes. Three hundred lenders compete. "
     "Offers in twenty four hours. Funded in days.",
     "+8%"),
    ("seg4.mp3", 19.3, 25.5,
     "Banks take ninety days. ROK takes twenty four hours. "
     "All credit profiles. No hard credit pull.",
     "+8%"),
    ("seg5.mp3", 26.2, 29.8,
     "Construction. Restaurants. Trucking. Any business.",
     "+10%"),
    ("seg6.mp3", 30.2, 34.5,
     "Check what you qualify for. Five minutes. Link in bio.",
     "+5%"),
]


def get_duration(path):
    probe = subprocess.run(
        ["ffprobe", "-v", "error", "-show_entries", "format=duration",
         "-of", "csv=p=0", str(path)],
        capture_output=True, text=True
    )
    return float(probe.stdout.strip()) if probe.stdout.strip() else 0


async def generate_segments():
    SEGMENTS_DIR.mkdir(parents=True, exist_ok=True)

    for filename, start, end, text, rate in SEGMENTS:
        out_path = SEGMENTS_DIR / filename
        print(f"  🎙️  Generating: {filename}")
        communicate = edge_tts.Communicate(text=text, voice=VOICE, rate=rate, pitch="+0Hz")
        await communicate.save(str(out_path))
        dur = get_duration(out_path)
        target = end - start
        print(f"       Raw: {dur:.1f}s → Target: {target:.1f}s")

        # Time-compress if needed
        if dur > target + 0.1:
            ratio = dur / target
            # atempo only supports 0.5-2.0, chain if needed
            fitted_path = SEGMENTS_DIR / f"fit_{filename}"
            if ratio <= 2.0:
                tempo_filter = f"atempo={ratio:.3f}"
            else:
                # Chain two atempo filters
                r1 = min(ratio, 2.0)
                r2 = ratio / r1
                tempo_filter = f"atempo={r1:.3f},atempo={r2:.3f}"

            cmd = ["ffmpeg", "-y", "-i", str(out_path),
                   "-af", tempo_filter,
                   "-c:a", "libmp3lame", str(fitted_path)]
            subprocess.run(cmd, capture_output=True, text=True)
            # Replace original
            fitted_path.replace(out_path)
            new_dur = get_duration(out_path)
            print(f"       Compressed: {new_dur:.1f}s ✅")


def combine_and_mix():
    """Combine segments at their start times with subtle background music."""
    print("\n🔧 Combining segments with timing + background...")

    # Generate subtle ambient pad
    bg_path = SEGMENTS_DIR / "bg_ambient.wav"
    bg_cmd = [
        "ffmpeg", "-y",
        "-f", "lavfi", "-i",
        (
            "aevalsrc="
            "'sin(220*2*PI*t)*0.015"
            "+sin(277*2*PI*t)*0.012"
            "+sin(330*2*PI*t)*0.012"
            "+sin(110*2*PI*t)*exp(-4*mod(t*120/60,1))*0.025"
            "':s=44100:c=stereo:d=35"
        ),
        "-af", "highpass=f=80,lowpass=f=8000,volume=0.4",
        "-c:a", "pcm_s16le",
        str(bg_path),
    ]
    subprocess.run(bg_cmd, capture_output=True, text=True)

    # Build ffmpeg filter to place each VO segment at its start time
    inputs = ["-i", str(bg_path)]  # input 0 = background
    filter_parts = ["[0]volume=0.25[bg]"]

    for i, (filename, start, end, text, rate) in enumerate(SEGMENTS):
        seg_path = SEGMENTS_DIR / filename
        inputs += ["-i", str(seg_path)]
        delay_ms = int(start * 1000)
        idx = i + 1  # input index (0 is background)
        filter_parts.append(
            f"[{idx}]aformat=sample_rates=44100:channel_layouts=mono,"
            f"adelay={delay_ms}|{delay_ms},volume=1.8[s{i}]"
        )

    # Mix background + all VO segments
    vo_mix = "".join(f"[s{i}]" for i in range(len(SEGMENTS)))
    n_inputs = len(SEGMENTS) + 1  # VO segments + background
    filter_parts.append(
        f"[bg]{vo_mix}amix=inputs={n_inputs}:duration=longest:normalize=0,"
        f"apad=whole_dur=35,alimiter=limit=0.95[out]"
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
    print("  ROK Financial — AriaNeural Voiceover V2")
    print("  Time-compressed to fit slide windows")
    print("=" * 60)

    await generate_segments()
    if combine_and_mix():
        print("\n✅ Voiceover ready! Re-encoding video...")


if __name__ == "__main__":
    asyncio.run(main())
