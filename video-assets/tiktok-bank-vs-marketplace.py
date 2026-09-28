"""TikTok (9:16): 'Bank: 6 weeks. Marketplace: 48 hrs.' price-comparison hook (ROK Financial).
Reuses the Week 1 look, voice and render pipeline from tiktok-week1.py.
Usage: python tiktok-bank-vs-marketplace.py
"""
import importlib.util
from pathlib import Path

spec = importlib.util.spec_from_file_location("wk1", Path(__file__).parent / "tiktok-week1.py")
wk1 = importlib.util.module_from_spec(spec)
spec.loader.exec_module(wk1)
W, font, text, pill = wk1.W, wk1.font, wk1.text, wk1.pill
GOLD, WHITE, MUTED, RED, GREEN, NAVY = wk1.GOLD, wk1.WHITE, wk1.MUTED, wk1.RED, wk1.GREEN, wk1.NAVY
ROK = wk1.ROK


def card(d, box, head, big, sub, color, sub_above=False):
    x0, y0, x1, y1 = box
    d.rounded_rectangle(box, 30, fill=WHITE)
    d.rounded_rectangle([x0, y0, x1, y0 + 110], 30, fill=color)
    d.rectangle([x0, y0 + 80, x1, y0 + 110], fill=color)
    cx = (x0 + x1) // 2
    d.text((cx, y0 + 55), head, font=font(54), fill=WHITE, anchor="mm")
    d.text((cx, y0 + 270), big, font=font(108), fill=color, anchor="mm")
    d.text((cx, y0 + (175 if sub_above else 385)), sub, font=font(44, False), fill=(60, 60, 60), anchor="mm")


def s1_hook(d, p, img):
    text(d, 470, "SAME BUSINESS.", 92)
    text(d, 580, "SAME LOAN.", 92, GOLD)
    card(d, [90, 720, 525, 1200], "BANK", "6 WKS", "to get funded", RED)
    card(d, [555, 720, 990, 1200], "MARKETPLACE", "48 HRS", "as fast as", GREEN, sub_above=True)
    text(d, 1320, "Why wait 6 weeks?", 70, GOLD)


def s2_table(d, p, img):
    text(d, 470, "BANK  vs  MARKETPLACE", 76, GOLD)
    rows = [("Speed", "6–8 weeks", "24–48 hrs"),
            ("Paperwork", "Stacks of it", "1 short app"),
            ("Check rate", "Hard pull", "Soft pull"),
            ("Offers", "1 bank", "Many lenders")]
    for i, (k, a, b) in enumerate(rows):
        if p > i * .15:
            y = 640 + i * 170
            d.rounded_rectangle([60, y - 70, 1020, y + 70], 18, fill=WHITE)
            d.text((95, y), k, font=font(44), fill=NAVY, anchor="lm")
            d.text((560, y), a, font=font(46, False), fill=RED, anchor="mm")
            d.text((860, y), b, font=font(46), fill=(0, 150, 90), anchor="mm")


def s3_how(d, p, img):
    text(d, 500, "HOW IT'S SO FAST", 90, GOLD)
    steps = ["Apply once (5 min)", "Lenders compete", "Offers in ~24 hrs", "Funded in days"]
    for i, s in enumerate(steps):
        if p > i * .18:
            y = 700 + i * 150
            d.ellipse([130, y - 45, 220, y + 45], fill=GOLD)
            d.text((175, y), str(i + 1), font=font(56), fill=NAVY, anchor="mm")
            d.text((260, y), s, font=font(62), fill=WHITE, anchor="lm")


def s4_cta(d, p, img):
    text(d, 470, "CHECK YOUR RATE", 100)
    text(d, 590, "Soft pull • No hit to your credit", 58, GOLD)
    img.paste(ROK, ((W - ROK.width) // 2, 700))
    pill(d, 700 + ROK.height + 110, "Link in bio →", size=60)


CFG = dict(
    key="bvm", slug="bank-vs-marketplace",
    segments=[
        "Same business. Same loan. The bank takes six weeks. A lending marketplace can fund you in as little as forty eight hours.",
        "The bank wants stacks of paperwork, a hard credit pull, and you get one answer. A marketplace is one short application, a soft pull to check your rate, and lenders competing for your deal.",
        "Apply once in about five minutes. Lenders compete. Offers can come in around twenty four hours, and funding lands in days.",
        "Checking your rate won't hit your credit. Link in bio.",
    ],
    funcs=[s1_hook, s2_table, s3_how, s4_cta],
)

if __name__ == "__main__":
    wk1.render(CFG)
