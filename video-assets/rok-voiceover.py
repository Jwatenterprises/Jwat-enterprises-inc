"""Generate female voiceover (AriaNeural) for ROK Financial TikTok."""
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
FINAL_VO = SCRIPT_DIR / "rok-funding-voiceover.wav"
FINAL_WITH_BG = SCRIPT_DIR / "rok-funding-beat.wav"  # replaces the old beat

# Voiceover segments timed to slides
# (filename, start_time_sec, text, rate)
SEGMENTS = [
    ("seg1_hook.mp3", 0.0,
     "One point six eight million dollars. Funded in three days.",
     "+10%"),
    ("seg2_case.mp3", 5.0,
     "A retail business went through ROK Financial. Got funded. Grew. "
     "Came back for more. ROK funded them again.",
     "+12%"),
    ("seg3_process.mp3", 12.0,
     "Apply once, five minutes. Three hundred lenders compete. "
     "Offers in twenty four hours. Funded in days.",
     "+12%"),
    ("seg4_compare.mp3", 19.0,
     "Banks take ninety days. ROK takes twenty four hours. "
     "All credit profiles. No hard credit pull.",
     "+12%"),
    ("seg5_who.mp3", 26.0,
     "Construction. Restaurants. Trucking. Any business. Ten K to five million.",
     "+15%"),
    ("seg6_cta.mp3", 30.0,
     "Check what you qualify for. Five minutes. Link in bio.",
     "+10%"),
]


async def generate_segments():
    """Generate each voiceover segment."""
    SEGMENTS_DIR.mkdir(parents=True, exist_ok=True)

    for filename, start, text, rate in SEGMENTS:
        out_path = SEGMENTS_DIR / filename
        print(f"  🎙️  Generating: {filename}")
        communicate = edge_tts.Communicate(
            text=text,
            voice=VOICE,
            rate=rate,
            pitch="+0Hz",
            volume="+0%",
        )
        await communicate.save(str(out_path))
        # Get duration
        probe = subprocess.run(
            ["ffprobe", "-v", "error", "-show_entries", "format=duration",
             "-of", "csv=p=0", str(out_path)],
            capture_output=True, text=True
        )
        dur = float(probe.stdout.strip()) if probe.stdout.strip() else 0
        print(f"       Duration: {dur:.1f}s (starts at {start}s)")


def combine_segments():
    """Combine segments with proper timing into a single 35s WAV."""
    print("\n🔧 Combining segments with timing...")

    # Build complex ffmpeg filter to place each segment at its start time
    inputs = []
    filter_parts = []

    for i, (filename, start, text, rate) in enumerate(SEGMENTS):
        seg_path = SEGMENTS_DIR / filename
        inputs += ["-i", str(seg_path)]
        # Delay each segment to its start time (in milliseconds)
        delay_ms = int(start * 1000)
        filter_parts.append(
            f"[{i}]aformat=sample_rates=44100:channel_layouts=mono,"
            f"adelay={delay_ms}|{delay_ms}[s{i}]"
        )

    # Mix all segments together
    mix_inputs = "".join(f"[s{i}]" for i in range(len(SEGMENTS)))
    filter_parts.append(
        f"{mix_inputs}amix=inputs={len(SEGMENTS)}:duration=longest:normalize=0[vo]"
    )

    # Add padding to ensure exactly 35 seconds
    filter_parts.append(
        "[vo]apad=whole_dur=35[vopad]"
    )

    filter_str = ";".join(filter_parts)

    cmd = ["ffmpeg", "-y"] + inputs + [
        "-filter_complex", filter_str,
        "-map", "[vopad]",
        "-c:a", "pcm_s16le",
        "-ar", "44100",
        str(FINAL_VO),
    ]

    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"❌ Combine failed: {result.stderr[:500]}")
        return False

    size_kb = FINAL_VO.stat().st_size // 1024
    print(f"   ✅ Voiceover: {FINAL_VO.name} ({size_kb} KB)")
    return True


def add_background_music():
    """Layer subtle background music under the voiceover."""
    print("\n🎵 Adding subtle background music...")

    # Generate a quiet, professional ambient pad
    bg_path = SEGMENTS_DIR / "bg_pad.wav"
    bg_cmd = [
        "ffmpeg", "-y",
        "-f", "lavfi", "-i",
        (
            "aevalsrc="
            # Warm ambient pad — very quiet
            "'sin(220*2*PI*t)*0.02"
            "+sin(277*2*PI*t)*0.015"
            "+sin(330*2*PI*t)*0.015"
            # Subtle pulse
            "+sin(110*2*PI*t)*exp(-4*mod(t*120/60,1))*0.03"
            "':s=44100:c=stereo:d=35"
        ),
        "-af", "highpass=f=80,lowpass=f=8000,volume=0.5",
        "-c:a", "pcm_s16le",
        str(bg_path),
    ]
    subprocess.run(bg_cmd, capture_output=True, text=True)

    # Mix voiceover (loud) + background (quiet)
    mix_cmd = [
        "ffmpeg", "-y",
        "-i", str(FINAL_VO),
        "-i", str(bg_path),
        "-filter_complex",
        "[0]volume=1.8[vo];[1]volume=0.3[bg];[vo][bg]amix=inputs=2:duration=first:normalize=0[out]",
        "-map", "[out]",
        "-c:a", "pcm_s16le",
        "-ar", "44100",
        str(FINAL_WITH_BG),
    ]
    result = subprocess.run(mix_cmd, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"❌ Mix failed: {result.stderr[:500]}")
        # Fall back to voiceover only
        import shutil
        shutil.copy2(FINAL_VO, FINAL_WITH_BG)
        print("   Using voiceover only (no background music)")
        return

    size_kb = FINAL_WITH_BG.stat().st_size // 1024
    print(f"   ✅ Final audio: {FINAL_WITH_BG.name} ({size_kb} KB)")


async def main():
    print("=" * 60)
    print("  ROK Financial — Female Voiceover (AriaNeural)")
    print("=" * 60)

    await generate_segments()
    if combine_segments():
        add_background_music()
        print("\n✅ Voiceover ready! Now re-run the video renderer.")


if __name__ == "__main__":
    asyncio.run(main())
