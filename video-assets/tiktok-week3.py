"""JWAT Week 3 TikToks (9:16): TT-1 Nav "Your business has a credit score", TT-2 ROK "$75K oven vs. $75K in the bank".
Facts: Nav business credit guide + Restaurant Equipment Financing (9/21). "#ad" tag stays on screen the whole video (FTC).
Reuses the look, voice and render pipeline from tiktok-week1.py.
Usage: python tiktok-week3.py [tt1|tt2]
"""
import sys
import importlib.util
from pathlib import Path

spec = importlib.util.spec_from_file_location("wk2", Path(__file__).parent / "tiktok-week2.py")
wk2 = importlib.util.module_from_spec(spec)
spec.loader.exec_module(wk2)
wk1 = wk2.wk1
W, font, text, pill, bullets, partner = wk1.W, wk1.font, wk1.text, wk1.pill, wk1.bullets, wk1.partner
GOLD, WHITE, MUTED, RED, GREEN, NAVY = wk1.GOLD, wk1.WHITE, wk1.MUTED, wk1.RED, wk1.GREEN, wk1.NAVY
ad_tag, card = wk2.ad_tag, wk2.card
NAV, ROK = partner("nav.png"), partner("rok-financial.png")


# ---------- TT-1: Your business has a credit score (Nav) ----------
def v1_hook(d, p, img):
    text(d, 470, "YOUR BUSINESS", 100)
    text(d, 590, "HAS A CREDIT SCORE", 82, GOLD)
    card(d, [90, 720, 525, 1200], "YOUR SCORE", "SSN", "you've seen it", GREEN)
    card(d, [555, 720, 990, 1200], "BUSINESS SCORE", "EIN", "have you?", RED)
    text(d, 1320, "Lenders check it. Do you?", 58, GOLD)


def v2_bureaus(d, p, img):
    text(d, 470, "TIED TO YOUR EIN", 96, GOLD)
    text(d, 580, "Not your Social", 62)
    bullets(d, p, ["Dun & Bradstreet", "Experian", "Equifax"], 720, step=150, size=66)
    text(d, 1240, "All three keep a file on you", 54)


def v3_who(d, p, img):
    text(d, 470, "WHO CHECKS IT", 96, GOLD)
    bullets(d, p, ["Lenders", "Suppliers", "Leasing companies"], 660, step=150, size=66)
    text(d, 1180, "Errors are common.", 60)
    text(d, 1260, "Fixes take time.", 60, GOLD)


def v4_cta(d, p, img):
    text(d, 450, "CHECK IT FIRST", 100)
    text(d, 570, "Free to start with Nav", 66, GOLD)
    img.paste(NAV, ((W - NAV.width) // 2, 660))
    pill(d, 660 + NAV.height + 110, "Link in bio →", size=60)
    text(d, 660 + NAV.height + 230, "Affiliate link • we may earn a commission", 38, MUTED, bold=False)


TT1 = dict(
    key="tt1", slug="nav-business-credit",
    segments=[
        "Your business has its own credit score, and you've probably never seen it.",
        "It's tied to your EIN, not your Social. Dun and Bradstreet, Experian and Equifax all keep a file on your business.",
        "Lenders, suppliers and leasing companies check it. Errors are common, and fixing them takes time.",
        "Check it before you apply for anything. Nav shows all three in one place, free to start. Link in bio.",
    ],
    funcs=[ad_tag(f) for f in (v1_hook, v2_bureaus, v3_who, v4_cta)],
)


# ---------- TT-2: $75K oven vs. $75K in the bank (ROK) ----------
def r1_hook(d, p, img):
    text(d, 470, "PAY CASH FOR", 96)
    text(d, 590, "RESTAURANT EQUIPMENT?", 74, GOLD)
    card(d, [90, 720, 525, 1200], "PAY CASH", "$0", "left in the bank", RED)
    card(d, [555, 720, 990, 1200], "FINANCE IT", "$75K", "stays in the bank", GREEN)
    text(d, 1320, "Same kitchen. Different cash flow.", 54, GOLD)


def r2_costs(d, p, img):
    text(d, 470, "IT ADDS UP FAST", 96, GOLD)
    bullets(d, p, ["Walk-in cooler: $8K–$20K", "Commercial oven: $5K–$25K", "POS system: $3K–$15K"], 680, step=150, size=58)
    text(d, 1220, "Cash spent = empty account", 56)


def r3_math(d, p, img):
    text(d, 470, "$75K FINANCED", 100, GOLD)
    text(d, 600, "≈ $1,830/mo", 110)
    text(d, 720, "8% over 4 years", 58)
    text(d, 900, "The $75K stays in the business", 54, GOLD)
    text(d, 980, "for payroll + surprises", 54)
    text(d, 1160, "Example only. Rates and terms vary.", 40, MUTED, bold=False)


def r4_cta(d, p, img):
    text(d, 450, "FROM $10K", 104)
    text(d, 570, "1–6 year terms • soft pull", 60, GOLD)
    img.paste(ROK, ((W - ROK.width) // 2, 660))
    pill(d, 660 + ROK.height + 110, "Link in bio →", size=60)
    text(d, 660 + ROK.height + 230, "We only get paid if you get funded", 38, MUTED, bold=False)


TT2 = dict(
    key="tt2", slug="rok-restaurant-equipment",
    segments=[
        "Opening a restaurant? Don't pay cash for the kitchen.",
        "A walk-in cooler, a commercial oven, a POS system. It adds up fast, and paying cash leaves you opening with an empty account.",
        "For example, seventy-five thousand financed at eight percent over four years is about eighteen thirty a month. The cash stays in the business for payroll.",
        "Equipment financing from ten thousand dollars, one-to-six-year terms. Checking your options is a soft pull. Link in bio.",
    ],
    funcs=[ad_tag(f) for f in (r1_hook, r2_costs, r3_math, r4_cta)],
)

if __name__ == "__main__":
    for cfg in (TT1, TT2):
        if len(sys.argv) < 2 or sys.argv[1] == cfg["key"]:
            wk1.render(cfg)
