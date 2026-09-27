"""TikTok/Shorts/Reels: 'Waiting 60 Days to Get Paid?' (9:16). Pillow frames piped to ffmpeg."""
import json, os, subprocess, sys
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

sys.stdout.reconfigure(encoding='utf-8')
W, H, FPS = 1080, 1920, 30
D = Path(__file__).parent
timing = json.loads((D / "cashflow-slide-timing.json").read_text())
TOTAL = timing["total_duration"]
AUDIO = D / "cashflow-voiceover.wav"
OUT_LOCAL = D / "cashflow-q4-tiktok.mp4"
EXPORT = Path(os.environ["USERPROFILE"]) / "OneDrive" / "video-assets" / "exports" / "jwat-cashflow-q4-tiktok.mp4"
LOGO = D.parent / "images" / "jwat-logo.png"

NAVY, NAVY_L, DARK = (26, 54, 93), (45, 90, 140), (13, 27, 42)
GOLD, WHITE, MUTED, RED, GREEN = (255, 215, 0), (255, 255, 255), (190, 200, 215), (255, 80, 80), (0, 200, 120)


def font(size, bold=True):
    p = "C:/Windows/Fonts/arialbd.ttf" if bold else "C:/Windows/Fonts/arial.ttf"
    return ImageFont.truetype(p, size)


def make_bg():
    img = Image.new("RGB", (W, H))
    d = ImageDraw.Draw(img)
    for y in range(H):
        r = y / H
        a, b, k = (DARK, NAVY, r * 2) if r < .5 else (NAVY, NAVY_L, (r - .5) * 2)
        d.line([(0, y), (W, y)], fill=tuple(int(a[i] + (b[i] - a[i]) * k) for i in range(3)))
    logo = Image.open(LOGO).convert("RGBA")
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


def s_hook(d, p):
    text(d, 560, "WAITING", 120, GOLD)
    text(d, 700, "60 DAYS", 170)
    text(d, 850, "TO GET PAID?", 110, GOLD)
    d.rounded_rectangle([190, 1020, 890, 1420], 24, fill=WHITE)
    d.text((250, 1080), "INVOICE #1047", font=font(46), fill=NAVY)
    d.text((250, 1160), "Terms: NET 60", font=font(42, False), fill=(90, 90, 90))
    d.text((250, 1230), "Work: COMPLETED", font=font(42, False), fill=(90, 90, 90))
    if p > .35:
        d.rounded_rectangle([420, 1300, 840, 1390], 14, outline=RED, width=8)
        d.text((630, 1345), "UNPAID", font=font(58), fill=RED, anchor="mm")


def s_payroll(d, p):
    text(d, 720, "MEANWHILE...", 80, MUTED)
    text(d, 900, "PAYROLL", 170, RED)
    text(d, 1070, "DUE FRIDAY", 130)


def s_factoring(d, p):
    text(d, 520, "INVOICE FACTORING", 84, GOLD)
    text(d, 780, "70-90%", 230)
    text(d, 940, "of the invoice up front", 58, WHITE, False)
    if p > .45:
        pill(d, 1160, "Often in ~24 hours")


def s_rbf(d, p):
    text(d, 500, "NO BIG INVOICES?", 76, MUTED)
    text(d, 640, "REVENUE-BASED", 96, GOLD)
    text(d, 760, "FUNDING", 96, GOLD)
    items = ["Based on monthly sales", "$10K - $500K", "500+ credit considered"]
    for i, s in enumerate(items):
        if p > i * .22:
            y = 960 + i * 130
            d.ellipse([150, y - 16, 182, y + 16], fill=GOLD)
            d.text((215, y), s, font=font(60), fill=WHITE, anchor="lm")


def s_process(d, p):
    items = [("1", "Short application"), ("2", "Soft pull only"), ("3", "No hit to your credit")]
    text(d, 540, "HOW IT WORKS", 90, GOLD)
    for i, (n, s) in enumerate(items):
        if p > i * .2:
            y = 760 + i * 190
            d.ellipse([150, y - 60, 270, y + 60], fill=GOLD)
            d.text((210, y), n, font=font(70), fill=NAVY, anchor="mm")
            d.text((320, y), s, font=font(66), fill=WHITE, anchor="lm")


def s_cta(d, p):
    text(d, 600, "STOP WAITING", 120)
    text(d, 740, "TO GET PAID", 120, GOLD)
    pill(d, 1000, "Check what you qualify for", size=56)
    text(d, 1180, "\u2191 LINK IN BIO \u2191", 80)
    text(d, 1330, "Full guides on our blog", 50, MUTED, False)


FUNCS = [s_hook, s_payroll, s_factoring, s_rbf, s_process, s_cta]


def frame(t):
    for (sl, fn) in zip(timing["slides"], FUNCS):
        if sl["start"] <= t < sl["end"] or fn is s_cta and t >= sl["start"]:
            p = (t - sl["start"]) / (sl["end"] - sl["start"])
            img = BG.copy()
            fn(ImageDraw.Draw(img), p)
            fade = min(1, (t - sl["start"]) / 0.25)
            return Image.blend(BG, img, fade) if fade < 1 else img
    return BG


def main():
    n = int(TOTAL * FPS)
    cmd = ["ffmpeg", "-y", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-",
           "-i", str(AUDIO), "-c:v", "libx264", "-preset", "medium", "-crf", "20", "-pix_fmt", "yuv420p",
           "-c:a", "aac", "-b:a", "160k", "-shortest", "-movflags", "+faststart", str(OUT_LOCAL)]
    ff = subprocess.Popen(cmd, stdin=subprocess.PIPE, stderr=subprocess.DEVNULL)
    for i in range(n):
        ff.stdin.write(frame(i / FPS).tobytes())
    ff.stdin.close()
    ff.wait()
    frame(0.2 + 1.5).save(D / "cashflow-q4-thumb.png")
    EXPORT.parent.mkdir(parents=True, exist_ok=True)
    EXPORT.write_bytes(OUT_LOCAL.read_bytes())
    print("rendered", OUT_LOCAL, f"{OUT_LOCAL.stat().st_size // 1024} KB ->", EXPORT)


if __name__ == "__main__":
    main()
