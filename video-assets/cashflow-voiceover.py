"""Voiceover (AriaNeural) for 'Waiting 60 Days to Get Paid?' — drives slide timing."""
import asyncio, json, subprocess, sys
from pathlib import Path
import edge_tts

sys.stdout.reconfigure(encoding='utf-8')
VOICE = "en-US-AriaNeural"
D = Path(__file__).parent
SEG = D / "cashflow-vo-segments"
OUT = D / "cashflow-voiceover.wav"
TIMING = D / "cashflow-slide-timing.json"
GAP = 0.4

SEGMENTS = [
    "You did the work. Sent the invoice. Now you wait sixty days to get paid.",
    "But payroll is due Friday.",
    "Invoice factoring gets you seventy to ninety percent of that invoice up front, often in about twenty four hours.",
    "No big invoices? Revenue-based funding looks at your monthly sales. Five hundred plus credit considered.",
    "One short application. Soft pull. No hit to your credit.",
    "Stop waiting to get paid. Link in bio.",
]


def dur(p):
    r = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration",
                        "-of", "csv=p=0", str(p)], capture_output=True, text=True)
    return float(r.stdout.strip())


async def main():
    SEG.mkdir(exist_ok=True)
    slides, t, parts = [], 0.4, []
    for i, text in enumerate(SEGMENTS):
        mp3 = SEG / f"seg{i+1}.mp3"
        await edge_tts.Communicate(text, VOICE, rate="+10%").save(str(mp3))
        d = dur(mp3)
        slides.append({"start": round(t - 0.4 if i == 0 else t, 2), "end": round(t + d + GAP, 2)})
        parts.append((mp3, t))
        t += d + GAP
    slides[-1]["end"] = round(t + 1.5, 2)
    total = slides[-1]["end"]
    inputs, filt = [], []
    for i, (mp3, start) in enumerate(parts):
        inputs += ["-i", str(mp3)]
        ms = int(start * 1000)
        filt.append(f"[{i}:a]adelay={ms}|{ms}[a{i}]")
    mix = "".join(f"[a{i}]" for i in range(len(parts)))
    filt.append(f"{mix}amix=inputs={len(parts)}:normalize=0,apad,atrim=0:{total}[out]")
    subprocess.run(["ffmpeg", "-y", *inputs, "-filter_complex", ";".join(filt), "-map", "[out]",
                    "-ar", "44100", "-c:a", "pcm_s16le", str(OUT)], check=True, capture_output=True)
    TIMING.write_text(json.dumps({"total_duration": total, "slides": slides}, indent=2))
    print(f"voiceover {total:.1f}s ->", OUT.name)
    for s in slides:
        print(s)

asyncio.run(main())
