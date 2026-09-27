"""Week 1 TikToks (9:16): TT-1 '$0 Follow-Up Fix' (GoHighLevel) + TT-2 'Bad Credit, Good Sales?' (ROK).
AriaNeural voiceover drives slide timing; Pillow frames piped to ffmpeg. Same look as cashflow-q4.
Usage: python tiktok-week1.py [tt1|tt2]  (no arg = both)
"""
import asyncio, os, subprocess, sys
from pathlib import Path
import edge_tts
from PIL import Image, ImageDraw, ImageFont

sys.stdout.reconfigure(encoding='utf-8')
W, H, FPS = 1080, 1920, 30
D = Path(__file__).parent
IMGS = D.parent / "images"
EXPORTS = Path(os.environ["USERPROFILE"]) / "OneDrive" / "video-assets" / "exports"
VOICE, GAP = "en-US-AriaNeural", 0.4
NAVY, NAVY_L, DARK = (26, 54, 93), (45, 90, 140), (13, 27, 42)
GOLD, WHITE, MUTED, RED, GREEN = (255, 215, 0), (255, 255, 255), (190, 200, 215), (255, 80, 80), (0, 200, 120)


def font(size, bold=True):
    return ImageFont.truetype("C:/Windows/Fonts/arialbd.ttf" if bold else "C:/Windows/Fonts/arial.ttf", size)


def make_bg():
    img = Image.new("RGB", (W, H))
    d = ImageDraw.Draw(img)
    for y in range(H):
        r = y / H
        a, b, k = (DARK, NAVY, r * 2) if r < .5 else (NAVY, NAVY_L, (r - .5) * 2)
        d.line([(0, y), (W, y)], fill=tuple(int(a[i] + (b[i] - a[i]) * k) for i in range(3)))
    logo = Image.open(IMGS / "jwat-logo.png").convert("RGBA")
    logo.thumbnail((260, 260))
    img.paste(logo, ((W - logo.width) // 2, 110), logo)
    d.text((W // 2, H - 110), "jwatenterprisesinc.com", font=font(34, False), fill=MUTED, anchor="mm")
    return img


BG = make_bg()


def text(d, y, s, size, fill=WHITE, bold=True):
    f = font(size, bold)
    d.text((W // 2 + 3, y + 3), s, font=f, fill=(0, 0, 0), anchor="mm")
    d.text((W // 2, y), s, font=f, fill=fill, anchor="mm")


def pill(d, y, s, fill=GOLD, fg=NAVY, size=52):
    f = font(size)
    w = d.textlength(s, font=f) + 90
    d.rounded_rectangle([(W - w) / 2, y - 55, (W + w) / 2, y + 55], 55, fill=fill)
    d.text((W // 2, y), s, font=f, fill=fg, anchor="mm")


def bullets(d, p, items, y0, step=130, size=60):
    for i, s in enumerate(items):
        if p > i * .2:
            y = y0 + i * step
            d.ellipse([150, y - 16, 182, y + 16], fill=GOLD)
            d.text((215, y), s, font=font(size), fill=WHITE, anchor="lm")


def partner(img_name):
    im = Image.open(IMGS / "partners" / img_name).convert("RGB")
    im.thumbnail((940, 560))
    return im


# ---------- TT-1: The $0 Follow-Up Fix ----------
GHL = partner("gohighlevel.png")


def t1_hook(d, p, img):
    text(d, 560, "YOU'RE LOSING", 110, GOLD)
    text(d, 720, "$$$", 220, GREEN)
    text(d, 880, "IN YOUR INBOX", 110, GOLD)
    if p > .3:
        d.rounded_rectangle([190, 1040, 890, 1380], 24, fill=WHITE)
        d.text((250, 1090), "New quote request", font=font(46), fill=NAVY)
        d.text((250, 1170), "Received: 12 days ago", font=font(40, False), fill=(90, 90, 90))
        d.rounded_rectangle([250, 1250, 700, 1330], 14, outline=RED, width=7)
        d.text((475, 1290), "NO REPLY", font=font(54), fill=RED, anchor="mm")


def t1_math(d, p, img):
    text(d, 520, "DO THE MATH", 100, GOLD)
    rows = ["Leads with 0-1 replies", "\u00d7  your close rate", "\u00d7  your average sale"]
    for i, s in enumerate(rows):
        if p > i * .2:
            text(d, 720 + i * 150, s, 66)
    if p > .65:
        pill(d, 1260, "= Your follow-up leak", fill=RED, fg=WHITE, size=58)


def t1_seq(d, p, img):
    text(d, 500, "THE 5-TOUCH FIX", 96, GOLD)
    rows = [("Day 0", "Instant text + email"), ("Day 1", "Check-in text"), ("Day 3", "Testimonial"),
            ("Day 7", "\"Still interested?\""), ("Day 14", "Close the file")]
    for i, (a, b) in enumerate(rows):
        if p > i * .12:
            y = 670 + i * 150
            d.rounded_rectangle([110, y - 60, 970, y + 60], 18, fill=WHITE)
            d.text((150, y), a, font=font(54), fill=NAVY, anchor="lm")
            d.text((400, y), b, font=font(50, False), fill=(40, 40, 40), anchor="lm")


def t1_cta(d, p, img):
    text(d, 470, "SET IT UP ONCE", 104)
    text(d, 590, "IT RUNS WITHOUT YOU", 76, GOLD)
    img.paste(GHL, ((W - GHL.width) // 2, 700))
    y = 700 + GHL.height + 110
    pill(d, y, "Free trial \u2192 link in bio", size=56)


TT1 = dict(
    key="tt1", slug="followup-fix",
    segments=[
        "Most small businesses aren't short on leads. They're losing them after the first message.",
        "Count the leads from the last ninety days that got one reply or none. Multiply by your close rate and your average sale. That's your leak.",
        "The fix is a five touch sequence. Instant text. A check-in the next day. A testimonial on day three. Still interested on day seven. Close the file on day fourteen.",
        "Set it up once in a CRM with missed call text-back, and it runs by itself. Free trial at the link in bio.",
    ],
    funcs=[t1_hook, t1_math, t1_seq, t1_cta],
)

# ---------- TT-2: Bad Credit, Good Sales? ----------
ROK = partner("rok-financial.png")


def t2_hook(d, p, img):
    text(d, 560, "DENIED BY", 120)
    text(d, 700, "THE BANK?", 140, RED)
    if p > .35:
        text(d, 900, "Your sales say", 76, MUTED, False)
        text(d, 1010, "OTHERWISE.", 120, GOLD)


def t2_rbf(d, p, img):
    text(d, 500, "REVENUE-BASED", 96, GOLD)
    text(d, 620, "FUNDING", 96, GOLD)
    text(d, 760, "looks at your deposits,", 60, WHITE, False)
    text(d, 840, "not just your credit score", 60, WHITE, False)
    bullets(d, p, ["Salons & auto shops", "Clinics & home services", "Ecommerce sellers"], 1010)


def t2_numbers(d, p, img):
    text(d, 620, "$10K \u2013 $500K", 130)
    if p > .35:
        text(d, 820, "Funding in as little as", 60, MUTED, False)
        text(d, 940, "24\u201348 HOURS", 130, GOLD)


def t2_cta(d, p, img):
    text(d, 470, "SOFT PULL", 120)
    text(d, 590, "No hit to your credit", 66, GOLD)
    img.paste(ROK, ((W - ROK.width) // 2, 700))
    y = 700 + ROK.height + 110
    pill(d, y, "Check your rate \u2192 link in bio", size=52)


TT2 = dict(
    key="tt2", slug="bad-credit-good-sales",
    segments=[
        "Your bank said no, but you're doing steady sales every month?",
        "Revenue-based funding looks at your deposits, not just your credit score. Salons, auto shops, clinics, ecommerce. If the money's coming in, you may qualify.",
        "Amounts from ten thousand to five hundred thousand, and funding can land in twenty four to forty eight hours.",
        "Checking your rate is a soft pull, with no hit to your credit. Link in bio.",
    ],
    funcs=[t2_hook, t2_rbf, t2_numbers, t2_cta],
)


def dur(p):
    r = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(p)],
                       capture_output=True, text=True)
    return float(r.stdout.strip())


async def voiceover(cfg):
    seg = D / f"{cfg['slug']}-vo-segments"
    seg.mkdir(exist_ok=True)
    slides, parts, t = [], [], 0.4
    for i, s in enumerate(cfg["segments"]):
        mp3 = seg / f"seg{i + 1}.mp3"
        await edge_tts.Communicate(s, VOICE, rate="+10%").save(str(mp3))
        d = dur(mp3)
        slides.append([0.0 if i == 0 else round(t, 2), round(t + d + GAP, 2)])
        parts.append((mp3, t))
        t += d + GAP
    slides[-1][1] = round(t + 1.5, 2)
    total = slides[-1][1]
    wav = seg / "voiceover.wav"
    inputs, filt = [], []
    for i, (mp3, start) in enumerate(parts):
        inputs += ["-i", str(mp3)]
        ms = int(start * 1000)
        filt.append(f"[{i}:a]adelay={ms}|{ms}[a{i}]")
    filt.append("".join(f"[a{i}]" for i in range(len(parts))) +
                f"amix=inputs={len(parts)}:normalize=0,apad,atrim=0:{total}[out]")
    subprocess.run(["ffmpeg", "-y", *inputs, "-filter_complex", ";".join(filt), "-map", "[out]",
                    "-ar", "44100", "-c:a", "pcm_s16le", str(wav)], check=True, capture_output=True)
    return slides, total, wav


def render(cfg):
    slides, total, wav = asyncio.run(voiceover(cfg))
    funcs = cfg["funcs"]

    def frame(t):
        for i, ((a, b), fn) in enumerate(zip(slides, funcs)):
            if a <= t < b or (i == len(funcs) - 1 and t >= a):
                img = BG.copy()
                fn(ImageDraw.Draw(img), (t - a) / (b - a), img)
                fade = 1 if i == 0 else min(1, (t - a) / 0.25)
                return Image.blend(BG, img, fade) if fade < 1 else img
        return BG

    out = D / f"{cfg['slug']}-tiktok.mp4"
    cmd = ["ffmpeg", "-y", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-",
           "-i", str(wav), "-c:v", "libx264", "-preset", "medium", "-crf", "20", "-pix_fmt", "yuv420p",
           "-c:a", "aac", "-b:a", "160k", "-shortest", "-movflags", "+faststart", str(out)]
    ff = subprocess.Popen(cmd, stdin=subprocess.PIPE, stderr=subprocess.DEVNULL)
    for i in range(int(total * FPS)):
        ff.stdin.write(frame(i / FPS).tobytes())
    ff.stdin.close()
    ff.wait()
    for i, (a, b) in enumerate(slides):
        frame(a + (b - a) * 0.9).save(D / f"{cfg['slug']}-slide{i + 1}.png")
    EXPORTS.mkdir(parents=True, exist_ok=True)
    (EXPORTS / f"jwat-{cfg['slug']}-tiktok.mp4").write_bytes(out.read_bytes())
    print(f"{cfg['key']}: {total:.1f}s, {out.stat().st_size // 1024} KB -> {out.name} (+ OneDrive export)")


if __name__ == "__main__":
    want = sys.argv[1:] or ["tt1", "tt2"]
    for cfg in (TT1, TT2):
        if cfg["key"] in want:
            render(cfg)
