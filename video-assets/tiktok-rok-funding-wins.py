"""
TikTok: ROK Financial — "$1.68M Funded in 3 Days" (35s, 9:16)
Local render using Pillow + ffmpeg. JWAT Enterprise branding.
"""
import os
import sys
import subprocess
import shutil
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

sys.stdout.reconfigure(encoding='utf-8')

W, H = 1080, 1920
FPS = 30
TIMING_FILE = Path(__file__).parent / "rok-slide-timing.json"

# Load timing from voiceover (or use defaults)
if TIMING_FILE.exists():
    import json as _json
    with open(TIMING_FILE) as _f:
        _timing = _json.load(_f)
    DURATION = int(_timing["total_duration"]) + 1
    print(f"📐 Loaded voiceover timing: {DURATION}s")
else:
    DURATION = 35
TOTAL_FRAMES = FPS * DURATION

SCRIPT_DIR = Path(__file__).parent
OUT_DIR = SCRIPT_DIR / "rok-tiktok-frames"
EXPORT_DIR = Path(os.environ.get("USERPROFILE", "~")) / "OneDrive" / "video-assets" / "exports"
LOGO_PATH = SCRIPT_DIR.parent / "images" / "jwat-logo.png"
AUDIO_PATH = SCRIPT_DIR / "rok-funding-beat.wav"

# JWAT Brand Colors
NAVY = (26, 54, 93)
NAVY_LIGHT = (45, 90, 140)
GOLD = (255, 215, 0)
DARK = (13, 27, 42)
WHITE = (255, 255, 255)
WHITE_80 = (255, 255, 255, 204)
MUTED = (180, 180, 200)
GREEN = (0, 200, 120)
RED = (255, 68, 68)


def get_font(size, bold=False):
    candidates = [
        "C:/Windows/Fonts/arialbd.ttf" if bold else "C:/Windows/Fonts/arial.ttf",
        "C:/Windows/Fonts/segoeui.ttf",
        "C:/Windows/Fonts/calibri.ttf",
    ]
    for f in candidates:
        if os.path.exists(f):
            return ImageFont.truetype(f, size)
    return ImageFont.load_default()


def gradient_bg(top=DARK, mid=NAVY, bot=NAVY_LIGHT):
    """Create JWAT navy gradient background."""
    img = Image.new("RGBA", (W, H), top)
    draw = ImageDraw.Draw(img)
    for y in range(H):
        ratio = y / H
        if ratio < 0.5:
            r = int(top[0] + (mid[0] - top[0]) * (ratio * 2))
            g = int(top[1] + (mid[1] - top[1]) * (ratio * 2))
            b = int(top[2] + (mid[2] - top[2]) * (ratio * 2))
        else:
            r2 = (ratio - 0.5) * 2
            r = int(mid[0] + (bot[0] - mid[0]) * r2)
            g = int(mid[1] + (bot[1] - mid[1]) * r2)
            b = int(mid[2] + (bot[2] - mid[2]) * r2)
        draw.line([(0, y), (W, y)], fill=(r, g, b))
    return img


def center_text(draw, text, y, font, fill=WHITE, anchor="mt"):
    bbox = draw.textbbox((W // 2, y), text, font=font, anchor=anchor)
    draw.text((W // 2 + 2, y + 2), text, font=font, fill=(0, 0, 0, 128), anchor=anchor)
    draw.text((W // 2, y), text, font=font, fill=fill, anchor=anchor)
    return bbox[3]


def draw_stat_card(draw, x, y, number, label, w=280, h=160):
    """Draw a stat card like the blog."""
    draw.rounded_rectangle(
        [(x, y), (x + w, y + h)],
        radius=16, fill=NAVY
    )
    # Gold border
    draw.rounded_rectangle(
        [(x, y), (x + w, y + h)],
        radius=16, outline=GOLD, width=2
    )
    # Number
    font_num = get_font(52, bold=True)
    draw.text((x + w // 2, y + 45), number, font=font_num, fill=GOLD, anchor="mt")
    # Label
    font_label = get_font(18, bold=True)
    draw.text((x + w // 2, y + 115), label, font=font_label, fill=WHITE_80, anchor="mt")


def draw_comparison_row(draw, y, label, rok_val, bank_val, highlight_rok=True):
    """Draw a ROK vs Bank comparison row."""
    font = get_font(26)
    font_bold = get_font(26, bold=True)
    row_h = 70
    pad = 40

    # Background stripe
    draw.rounded_rectangle(
        [(pad, y), (W - pad, y + row_h)],
        radius=10, fill=(20, 35, 60, 200)
    )

    # Label
    draw.text((pad + 20, y + row_h // 2), label, font=font_bold, fill=WHITE, anchor="lm")

    # ROK value (green)
    rok_color = GREEN if highlight_rok else WHITE
    draw.text((W // 2 + 40, y + row_h // 2), rok_val, font=font, fill=rok_color, anchor="lm")

    # Bank value (muted/red)
    draw.text((W - pad - 20, y + row_h // 2), bank_val, font=font, fill=RED, anchor="rm")

    return y + row_h + 8


def add_logo(img):
    """Add JWAT logo watermark to top-right."""
    if not LOGO_PATH.exists():
        return img
    logo = Image.open(LOGO_PATH).convert("RGBA")
    logo_size = 90
    logo = logo.resize((logo_size, logo_size), Image.LANCZOS)
    alpha = logo.split()[3]
    alpha = alpha.point(lambda x: int(x * 0.7))
    logo.putalpha(alpha)
    img.paste(logo, (W - logo_size - 40, 40), logo)
    return img


# ===== SLIDE DEFINITIONS =====

def slide_hook(frame_in_slide, total_slide_frames):
    """Slide 1: "$1.68 MILLION — 3 DAYS" hook (0-5s)"""
    img = gradient_bg()
    draw = ImageDraw.Draw(img)

    progress = frame_in_slide / total_slide_frames

    # Main money amount with scale-in effect
    font_big = get_font(80, bold=True)
    font_sub = get_font(36)
    font_label = get_font(28)

    y = 480
    center_text(draw, "$1.68", y, get_font(140, bold=True), fill=GOLD)
    center_text(draw, "MILLION", y + 150, get_font(64, bold=True), fill=GOLD)

    center_text(draw, "funded in", y + 260, font_sub, fill=MUTED)
    center_text(draw, "3 DAYS", y + 310, get_font(90, bold=True), fill=WHITE)

    # Pulse border effect
    if progress > 0.3:
        draw.rounded_rectangle(
            [(60, y - 40), (W - 60, y + 440)],
            radius=20, outline=GOLD, width=3
        )

    center_text(draw, "Not 3 months. Not 3 weeks.", y + 500, font_label, fill=MUTED)
    center_text(draw, "3 days.", y + 540, get_font(32, bold=True), fill=WHITE)

    img = add_logo(img)
    return img.convert("RGB")


def slide_case_study(frame_in_slide, total_slide_frames):
    """Slide 2: Case study details (5-12s)"""
    img = gradient_bg()
    draw = ImageDraw.Draw(img)

    y = 300
    center_text(draw, "REAL CASE STUDY", y, get_font(24, bold=True), fill=GOLD)
    center_text(draw, "September 2026", y + 40, get_font(22), fill=MUTED)

    # Case study box
    box_y = y + 90
    draw.rounded_rectangle(
        [(50, box_y), (W - 50, box_y + 500)],
        radius=20, fill=(20, 35, 60), outline=GOLD, width=2
    )

    center_text(draw, "Retail Business", box_y + 40, get_font(36, bold=True), fill=WHITE)
    center_text(draw, "Repeat Client", box_y + 85, get_font(28), fill=GREEN)

    # Story
    story_font = get_font(24)
    lines = [
        "Got funded the first time.",
        "Business grew.",
        "Came back for more capital.",
        "ROK funded them again —",
    ]
    for i, line in enumerate(lines):
        center_text(draw, line, box_y + 150 + i * 42, story_font, fill=WHITE_80)

    # Big number
    center_text(draw, "$1,684,000", box_y + 340, get_font(64, bold=True), fill=GOLD)
    center_text(draw, "in just 3 days", box_y + 415, get_font(30), fill=WHITE)

    # Bottom stat cards
    card_y = box_y + 550
    draw_stat_card(draw, 60, card_y, "300+", "LENDERS", w=290, h=140)
    draw_stat_card(draw, W - 350, card_y, "24 hrs", "APPROVAL", w=290, h=140)

    img = add_logo(img)
    return img.convert("RGB")


def slide_how_it_works(frame_in_slide, total_slide_frames):
    """Slide 3: How ROK works — 4 steps (12-19s)"""
    img = gradient_bg()
    draw = ImageDraw.Draw(img)

    progress = frame_in_slide / total_slide_frames

    y = 280
    center_text(draw, "HOW ROK FINANCIAL WORKS", y, get_font(32, bold=True), fill=GOLD)

    steps = [
        ("1", "APPLY", "5 minutes. No hard credit pull.", "📝"),
        ("2", "MATCH", "300+ lenders compete for your deal.", "🔄"),
        ("3", "OFFERS", "Multiple options in 24-48 hours.", "📋"),
        ("4", "FUNDED", "Capital in your account. 24-72 hrs.", "💰"),
    ]

    # Reveal steps progressively
    visible_steps = min(4, int(progress * 5) + 1)

    for i, (num, title, desc, emoji) in enumerate(steps):
        if i >= visible_steps:
            break

        step_y = y + 100 + i * 220
        pad = 60

        # Step card
        draw.rounded_rectangle(
            [(pad, step_y), (W - pad, step_y + 180)],
            radius=16, fill=(20, 35, 60, 220)
        )

        # Step number circle
        cx, cy = pad + 50, step_y + 90
        draw.ellipse([(cx - 30, cy - 30), (cx + 30, cy + 30)], fill=GOLD)
        draw.text((cx, cy), num, font=get_font(32, bold=True), fill=NAVY, anchor="mm")

        # Title + description
        draw.text((cx + 55, step_y + 50), title, font=get_font(34, bold=True), fill=WHITE)
        draw.text((cx + 55, step_y + 100), desc, font=get_font(22), fill=MUTED)

        # Emoji
        draw.text((W - pad - 50, step_y + 90), emoji, font=get_font(40), fill=WHITE, anchor="mm")

    img = add_logo(img)
    return img.convert("RGB")


def slide_comparison(frame_in_slide, total_slide_frames):
    """Slide 4: ROK vs Bank comparison (19-26s)"""
    img = gradient_bg()
    draw = ImageDraw.Draw(img)

    y = 300
    center_text(draw, "ROK FINANCIAL", y, get_font(36, bold=True), fill=GREEN)
    center_text(draw, "vs", y + 50, get_font(24), fill=MUTED)
    center_text(draw, "YOUR BANK", y + 80, get_font(36, bold=True), fill=RED)

    # Header row
    header_y = y + 150
    font_h = get_font(20, bold=True)
    draw.text((W // 2 + 40, header_y), "ROK", font=font_h, fill=GREEN, anchor="lm")
    draw.text((W - 60, header_y), "BANK", font=font_h, fill=RED, anchor="rm")

    # Comparison rows
    row_y = header_y + 40
    row_y = draw_comparison_row(draw, row_y, "Speed", "24-72 hrs", "90 days")
    row_y = draw_comparison_row(draw, row_y, "Approval", "High", "~20%")
    row_y = draw_comparison_row(draw, row_y, "Credit", "All profiles", "680+")
    row_y = draw_comparison_row(draw, row_y, "Amount", "$10K-$5M+", "$50K-$500K")
    row_y = draw_comparison_row(draw, row_y, "Application", "5 min, soft", "Hours, hard pull")
    row_y = draw_comparison_row(draw, row_y, "Repeat", "Built in", "Start over")

    # Verdict
    center_text(draw, "One application → 300+ lenders", row_y + 30, get_font(26, bold=True), fill=GOLD)

    img = add_logo(img)
    return img.convert("RGB")


def slide_who(frame_in_slide, total_slide_frames):
    """Slide 5: Who it's for (26-30s)"""
    img = gradient_bg()
    draw = ImageDraw.Draw(img)

    y = 350
    center_text(draw, "WHO GETS FUNDED?", y, get_font(36, bold=True), fill=GOLD)

    industries = [
        "🏗️  Construction & Trades",
        "🍽️  Restaurants & Food",
        "🛒  Retail & E-commerce",
        "🚚  Trucking & Transport",
        "🏥  Healthcare & Medical",
        "🧹  Service Businesses",
        "💼  Professional Services",
    ]

    for i, ind in enumerate(industries):
        iy = y + 80 + i * 70
        draw.rounded_rectangle(
            [(100, iy), (W - 100, iy + 55)],
            radius=10, fill=(20, 35, 60, 180)
        )
        draw.text((140, iy + 28), ind, font=get_font(28), fill=WHITE, anchor="lm")

    center_text(draw, "$10K to $5M+  •  All credit profiles", y + 590, get_font(24, bold=True), fill=GOLD)

    img = add_logo(img)
    return img.convert("RGB")


def slide_cta(frame_in_slide, total_slide_frames):
    """Slide 6: CTA — check your options (30-35s)"""
    img = gradient_bg()
    draw = ImageDraw.Draw(img)

    y = 400
    center_text(draw, "YOUR BUSINESS", y, get_font(48, bold=True), fill=WHITE)
    center_text(draw, "COULD BE NEXT", y + 60, get_font(48, bold=True), fill=GOLD)

    # CTA box
    cta_y = y + 160
    draw.rounded_rectangle(
        [(80, cta_y), (W - 80, cta_y + 200)],
        radius=20, fill=GOLD
    )
    draw.text(
        (W // 2, cta_y + 60),
        "Check What You Qualify For",
        font=get_font(32, bold=True), fill=NAVY, anchor="mt"
    )
    draw.text(
        (W // 2, cta_y + 110),
        "No hard credit pull • No commitment",
        font=get_font(22), fill=(26, 54, 93, 200), anchor="mt"
    )
    draw.text(
        (W // 2, cta_y + 150),
        "5 minutes →",
        font=get_font(28, bold=True), fill=NAVY, anchor="mt"
    )

    # Link in bio
    center_text(draw, "LINK IN BIO", cta_y + 260, get_font(40, bold=True), fill=WHITE)

    # JWAT branding
    center_text(draw, "JWAT ENTERPRISES INC", cta_y + 340, get_font(20, bold=True), fill=MUTED)
    center_text(draw, "AI-Powered Business Consulting", cta_y + 368, get_font(16), fill=MUTED)

    img = add_logo(img)
    return img.convert("RGB")


# ===== SLIDE TIMING =====

_slide_funcs = [slide_hook, slide_case_study, slide_how_it_works,
                slide_comparison, slide_who, slide_cta]

if TIMING_FILE.exists():
    SLIDES = []
    for i, s in enumerate(_timing["slides"]):
        SLIDES.append((s["start"], s["end"], _slide_funcs[i]))
else:
    SLIDES = [
        (0, 5, slide_hook),
        (5, 12, slide_case_study),
        (12, 19, slide_how_it_works),
        (19, 26, slide_comparison),
        (26, 30, slide_who),
        (30, 35, slide_cta),
    ]


def generate_audio():
    """Generate a professional, confident beat (128 BPM) with ffmpeg."""
    print("🎵 Generating audio beat...")

    # Professional, clean beat - more corporate/confident than the fall sale beat
    audio_cmd = [
        "ffmpeg", "-y",
        "-f", "lavfi", "-i",
        (
            "aevalsrc="
            # Kick drum - deep, clean (55Hz + sub 30Hz)
            "'sin(55*2*PI*t)*exp(-8*mod(t*128/60,1))*0.6"
            "+sin(30*2*PI*t)*exp(-12*mod(t*128/60,1))*0.3"
            # Hi-hat - crisp ticks on off-beats
            "+random(0)*exp(-40*mod(t*256/60,1))*0.15"
            # Bass synth - confident, warm (73Hz = D2)
            "+sin(73.42*2*PI*t)*exp(-3*mod(t*128/60,1))*0.35"
            "+sin(146.83*2*PI*t)*exp(-5*mod(t*128/60,1))*0.15"
            # Pad shimmer - subtle golden warmth
            "+sin(440*2*PI*t)*0.03+sin(554*2*PI*t)*0.02+sin(659*2*PI*t)*0.02"
            # Snap on beats 2 and 4
            "+random(1)*exp(-60*mod(t*256/60+0.5,1))*0.1"
            "':s=44100:c=stereo:d=35"
        ),
        "-af", "highpass=f=30,lowpass=f=15000,volume=1.4,alimiter=limit=0.92",
        "-c:a", "pcm_s16le",
        str(AUDIO_PATH),
    ]

    result = subprocess.run(audio_cmd, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"⚠️  Audio generation failed: {result.stderr[:200]}")
        return False
    size_kb = AUDIO_PATH.stat().st_size // 1024
    print(f"   ✅ Audio: {AUDIO_PATH.name} ({size_kb} KB)")
    return True


def render_frames():
    """Render all frames to the output directory."""
    if OUT_DIR.exists():
        shutil.rmtree(OUT_DIR)
    OUT_DIR.mkdir(parents=True, exist_ok=True)

    print(f"🎬 Rendering {TOTAL_FRAMES} frames ({DURATION}s @ {FPS}fps)...")

    for frame_num in range(TOTAL_FRAMES):
        t = frame_num / FPS  # current time in seconds

        # Find the active slide
        for start, end, slide_func in SLIDES:
            if start <= t < end:
                frame_in_slide = int((t - start) * FPS)
                total_slide_frames = int((end - start) * FPS)
                img = slide_func(frame_in_slide, total_slide_frames)
                break
        else:
            # Past last slide — hold CTA
            img = slide_cta(0, 1)

        img.save(OUT_DIR / f"frame_{frame_num:04d}.png")

        if frame_num % (FPS * 5) == 0:
            print(f"   Frame {frame_num}/{TOTAL_FRAMES} ({int(t)}s)")

    print(f"   ✅ All {TOTAL_FRAMES} frames rendered")


def encode_video():
    """Encode frames + audio into final MP4."""
    EXPORT_DIR.mkdir(parents=True, exist_ok=True)
    output = EXPORT_DIR / "tiktok-rok-funding-wins.mp4"

    print(f"🔧 Encoding video → {output}")

    cmd = [
        "ffmpeg", "-y",
        "-framerate", str(FPS),
        "-i", str(OUT_DIR / "frame_%04d.png"),
    ]

    if AUDIO_PATH.exists():
        cmd += ["-i", str(AUDIO_PATH)]

    cmd += [
        "-c:v", "libx264",
        "-pix_fmt", "yuv420p",
        "-preset", "medium",
        "-crf", "23",
        "-movflags", "+faststart",
    ]

    if AUDIO_PATH.exists():
        cmd += ["-c:a", "aac", "-b:a", "128k", "-shortest"]

    cmd.append(str(output))

    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"❌ Encode failed: {result.stderr[:500]}")
        return None

    size_mb = output.stat().st_size / 1024 / 1024
    print(f"   ✅ Video: {output.name} ({size_mb:.1f} MB)")
    return output


if __name__ == "__main__":
    print("=" * 60)
    print("  ROK Financial — $1.68M in 3 Days — TikTok Render")
    print("  JWAT Enterprise Inc | 35s | 1080×1920 | 9:16")
    print("=" * 60)

    # Skip audio gen if voiceover already exists (rok-voiceover-v2.py creates it)
    if not AUDIO_PATH.exists():
        generate_audio()
    else:
        print(f"🎙️  Using existing audio: {AUDIO_PATH.name} ({AUDIO_PATH.stat().st_size // 1024} KB)")
    render_frames()
    output = encode_video()

    if output:
        # Cleanup frames
        shutil.rmtree(OUT_DIR, ignore_errors=True)
        print(f"\n🎬 DONE! Video ready at:")
        print(f"   {output}")
        print(f"\n📋 TikTok Caption:")
        print("   $1.68 million funded in 3 days. Not 3 months.")
        print("   ROK Financial connects your business to 300+ lenders.")
        print("   24-hour approvals. All credit profiles. No hard pull.")
        print("   Link in bio to check what YOU qualify for 💰")
        print("   #businessfunding #smallbusiness #entrepreneur #ROKFinancial")
        print("   #businessloans #startup #capital #funding #JWAT")
