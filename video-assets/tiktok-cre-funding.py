"""TikTok (9:16): commercial real estate funding — 'Bank: 45-90 days. ROK: as little as 30.' (ROK Financial).
Facts: ROK CRE page/home page (accessed 2026-10-01); SBA 504 (sba.gov); bank/504 close times = industry estimates.
Reuses the Week 1 look, voice and render pipeline from tiktok-week1.py.
Usage: python tiktok-cre-funding.py
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
    d.text((cx, y0 + 270), big, font=font(96), fill=color, anchor="mm")
    d.text((cx, y0 + (175 if sub_above else 385)), sub, font=font(42, False), fill=(60, 60, 60), anchor="mm")


def s1_hook(d, p, img):
    text(d, 470, "BUYING A BUILDING?", 88)
    text(d, 580, "Don't lose it to a slow loan.", 62, GOLD)
    card(d, [90, 720, 525, 1200], "BANK", "45-90", "days, typical", RED)
    card(d, [555, 720, 990, 1200], "ROK", "~30", "days, as little as", GREEN, sub_above=True)
    text(d, 1320, "Commercial real estate funding", 58, GOLD)


def s2_table(d, p, img):
    text(d, 470, "YOUR 3 MAIN OPTIONS", 80, GOLD)
    d.text((560, 590), "Down", font=font(40), fill=MUTED, anchor="mm")
    d.text((860, 590), "Close", font=font(40), fill=MUTED, anchor="mm")
    rows = [("SBA 504", "10%", "60-90 days", RED),
            ("Bank", "Varies", "45-90 days", RED),
            ("ROK", "~15%*", "~30 days", (0, 150, 90))]
    for i, (k, a, b, col) in enumerate(rows):
        if p > i * .2:
            y = 720 + i * 180
            d.rounded_rectangle([60, y - 75, 1020, y + 75], 18, fill=WHITE)
            d.text((95, y), k, font=font(48), fill=NAVY, anchor="lm")
            d.text((560, y), a, font=font(48, False), fill=NAVY, anchor="mm")
            d.text((860, y), b, font=font(48), fill=col, anchor="mm")
    text(d, 1300, "*investment property, per ROK", 40, MUTED, bold=False)
    text(d, 1360, "Close times: industry estimates", 40, MUTED, bold=False)


def s3_rok(d, p, img):
    text(d, 470, "ROK CRE AT A GLANCE", 84, GOLD)
    items = ["$250K - $10M", "10 - 30 year terms", "Purchase, refi, cash-out", "650+ FICO minimum"]
    for i, s in enumerate(items):
        if p > i * .18:
            y = 660 + i * 150
            d.ellipse([130, y - 45, 220, y + 45], fill=GOLD)
            d.text((175, y), str(i + 1), font=font(56), fill=NAVY, anchor="mm")
            d.text((260, y), s, font=font(62), fill=WHITE, anchor="lm")
    text(d, 1300, "Source: rok.biz", 40, MUTED, bold=False)


def s4_cta(d, p, img):
    text(d, 430, "SEE WHAT YOU", 92)
    text(d, 540, "QUALIFY FOR", 92)
    text(d, 640, "One application • many lenders", 54, GOLD)
    img.paste(ROK, ((W - ROK.width) // 2, 730))
    pill(d, 730 + ROK.height + 110, "Link in bio →", size=60)
    text(d, 730 + ROK.height + 230, "Affiliate link • JWAT is not a lender", 38, MUTED, bold=False)


CFG = dict(
    key="cre", slug="cre-funding",
    segments=[
        "Buying a building? Banks typically take forty-five to ninety days to close. ROK Financial says it can fund in as little as thirty.",
        "SBA 504: ten percent down, about sixty to ninety days. A bank: forty-five to ninety. ROK: around thirty.",
        "ROK covers two hundred fifty thousand to ten million dollars, with ten to thirty year terms, for purchase, refinance, and cash-out.",
        "See what you qualify for. Link in bio.",
    ],
    funcs=[s1_hook, s2_table, s3_rok, s4_cta],
)

if __name__ == "__main__":
    wk1.render(CFG)
