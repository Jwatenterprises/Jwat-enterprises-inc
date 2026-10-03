"""JWAT Week 2 TikToks (9:16): TT-1 Upfirst "$24.95 vs. one missed call", TT-2 Novo "Still paying your bank?".
Facts: Upfirst review (9/27) + Novo blog (9/27). "#ad" tag stays on screen the whole video (FTC).
Reuses the look, voice and render pipeline from tiktok-week1.py.
Usage: python tiktok-week2.py [tt1|tt2]
"""
import sys
import importlib.util
from pathlib import Path

spec = importlib.util.spec_from_file_location("wk1", Path(__file__).parent / "tiktok-week1.py")
wk1 = importlib.util.module_from_spec(spec)
spec.loader.exec_module(wk1)
W, font, text, pill, bullets, partner = wk1.W, wk1.font, wk1.text, wk1.pill, wk1.bullets, wk1.partner
GOLD, WHITE, MUTED, RED, GREEN, NAVY = wk1.GOLD, wk1.WHITE, wk1.MUTED, wk1.RED, wk1.GREEN, wk1.NAVY
UPFIRST, NOVO = partner("upfirst.jpg"), partner("novo.png")


def ad_tag(fn):
    def wrapped(d, p, img):
        fn(d, p, img)
        d.rounded_rectangle([W - 190, 60, W - 50, 130], 35, fill=(13, 27, 42))
        d.text((W - 120, 95), "#ad", font=font(44), fill=WHITE, anchor="mm")
    return wrapped


def card(d, box, head, big, sub, color):
    x0, y0, x1, y1 = box
    d.rounded_rectangle(box, 30, fill=WHITE)
    d.rounded_rectangle([x0, y0, x1, y0 + 110], 30, fill=color)
    d.rectangle([x0, y0 + 80, x1, y0 + 110], fill=color)
    cx = (x0 + x1) // 2
    hs = 50
    while d.textlength(head, font=font(hs)) > (x1 - x0) - 50:
        hs -= 2
    d.text((cx, y0 + 55), head, font=font(hs), fill=WHITE, anchor="mm")
    d.text((cx, y0 + 260), big, font=font(92), fill=color, anchor="mm")
    d.text((cx, y0 + 380), sub, font=font(40, False), fill=(60, 60, 60), anchor="mm")


# ---------- TT-1: $24.95 vs. one missed call (Upfirst) ----------
def u1_hook(d, p, img):
    text(d, 470, "$24.95/mo vs.", 100, GOLD)
    text(d, 590, "ONE MISSED CALL", 96)
    card(d, [90, 720, 525, 1200], "AI RECEPTIONIST", "$24.95", "per month", GREEN)
    card(d, [555, 720, 990, 1200], "MISSED CALL", "$???", "a lost job", RED)
    text(d, 1320, "Which one costs you more?", 58, GOLD)


def u2_247(d, p, img):
    text(d, 470, "AI ANSWERS 24/7", 96, GOLD)
    text(d, 580, "In your business name", 62)
    img.paste(UPFIRST, ((W - UPFIRST.width) // 2, 680))
    text(d, 680 + UPFIRST.height + 90, "Nights • weekends • mid-job", 56)


def u3_does(d, p, img):
    text(d, 470, "WHAT IT DOES", 96, GOLD)
    bullets(d, p, ["Captures name + need", "Books the appointment", "Transfers urgent calls",
                   "Texts you the recap", "Sends the recording"], 660, step=140, size=62)


def u4_cta(d, p, img):
    text(d, 450, "FROM $24.95/MO", 100)
    text(d, 570, "14-day free trial", 70, GOLD)
    img.paste(UPFIRST, ((W - UPFIRST.width) // 2, 660))
    pill(d, 660 + UPFIRST.height + 110, "Link in bio →", size=60)
    text(d, 660 + UPFIRST.height + 230, "Affiliate link • we earn a commission", 38, MUTED, bold=False)


TT1 = dict(
    key="tt1", slug="upfirst-missed-call",
    segments=[
        "What's one missed call worth to your business? Probably more than a month of this.",
        "Upfirst is an AI receptionist. It answers in your business name, nights and weekends, while you're on the job.",
        "It grabs the caller's name and what they need, books the appointment, sends urgent calls to you, and texts you a summary with the recording.",
        "Plans start at twenty-four ninety-five a month with a fourteen-day free trial. Link in bio.",
    ],
    funcs=[ad_tag(f) for f in (u1_hook, u2_247, u3_does, u4_cta)],
)


# ---------- TT-2: Still paying your bank? (Novo) ----------
def n1_hook(d, p, img):
    text(d, 470, "STILL PAYING YOUR BANK", 74)
    text(d, 580, "A MONTHLY FEE?", 96, GOLD)
    card(d, [90, 720, 525, 1200], "TYPICAL BANK", "$$$", "monthly fees", RED)
    card(d, [555, 720, 990, 1200], "NOVO", "$0", "monthly fees", GREEN)
    text(d, 1320, "Same business. Less overhead.", 58, GOLD)


def n2_zero(d, p, img):
    text(d, 470, "$0 MONTHLY FEES", 100, GOLD)
    text(d, 580, "250,000+ small businesses switched", 50)
    img.paste(NOVO, ((W - NOVO.width) // 2, 680))
    text(d, 680 + NOVO.height + 90, "No minimum balance to keep", 56)


def n3_tools(d, p, img):
    text(d, 470, "BUILT IN", 104, GOLD)
    bullets(d, p, ["Invoicing", "Bill pay", "Reserves for tax money", "FedNow + QuickBooks"], 680, step=150, size=64)


def n4_cta(d, p, img):
    text(d, 450, "OPEN A FREE ACCOUNT", 82)
    text(d, 560, "All in the app • no branches", 56, GOLD)
    img.paste(NOVO, ((W - NOVO.width) // 2, 650))
    pill(d, 650 + NOVO.height + 110, "Link in bio →", size=60)
    text(d, 650 + NOVO.height + 220, "Banking by Middlesex Federal Savings, F.A., Member FDIC", 32, MUTED, bold=False)
    text(d, 650 + NOVO.height + 275, "Referral link • we may earn a bonus", 36, MUTED, bold=False)


TT2 = dict(
    key="tt2", slug="novo-bank-fees",
    segments=[
        "Still paying your bank every month just to hold your business money?",
        "Over two hundred fifty thousand small businesses switched to Novo. No monthly fees and no minimum balance games.",
        "Invoicing and bill pay are built in, and Reserves let you set tax money aside before you accidentally spend it.",
        "Banking through an FDIC-member partner bank. No branches, so it's all in the app. Link in bio.",
    ],
    funcs=[ad_tag(f) for f in (n1_hook, n2_zero, n3_tools, n4_cta)],
)

if __name__ == "__main__":
    for cfg in (TT1, TT2):
        if len(sys.argv) < 2 or sys.argv[1] == cfg["key"]:
            wk1.render(cfg)
