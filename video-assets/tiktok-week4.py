"""JWAT Week 4 TikToks (9:16): TT-1 Tax Services "Your tax pro can't fix 2026 in March",
TT-2 ROK "Paid in 60 days, payroll on Friday" (invoice factoring).
Facts: Tax Strategy vs Tax Preparation (9/21) + Invoice Factoring Explained. "#ad" tag stays on screen the whole video (FTC).
Reuses the look, voice and render pipeline from tiktok-week1.py.
Usage: python tiktok-week4.py [tt1|tt2]
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
ROK = partner("rok-financial.png")


# ---------- TT-1: Your tax pro can't fix 2026 in March (Tax Services) ----------
def x1_hook(d, p, img):
    text(d, 470, "YOUR TAX PRO", 104)
    text(d, 590, "CAN'T FIX 2026 IN MARCH", 72, GOLD)
    card(d, [90, 720, 525, 1200], "TAX PREP", "LOOKS", "back", RED)
    card(d, [555, 720, 990, 1200], "TAX STRATEGY", "LOOKS", "ahead", GREEN)
    text(d, 1320, "Most owners only get the first one.", 52, GOLD)


def x2_prep(d, p, img):
    text(d, 470, "TAX PREP", 104, GOLD)
    text(d, 590, "Files what already happened", 60)
    text(d, 760, "TAX STRATEGY", 104, GOLD)
    text(d, 880, "Changes what happens next", 60)
    text(d, 1120, "Strategy has a deadline:", 58)
    text(d, 1200, "December 31", 76, GOLD)


def x3_weeks(d, p, img):
    text(d, 470, "10 WEEKS LEFT", 104, GOLD)
    bullets(d, p, ["Timing of big purchases", "How you pay yourself", "Your Q4 estimate (due Jan 15)"], 660, step=150, size=56)
    text(d, 1200, "Ask a tax pro now,", 60)
    text(d, 1280, "not in March.", 60, GOLD)


def x4_cta(d, p, img):
    text(d, 470, "BOOK A", 100)
    text(d, 590, "YEAR-END TAX REVIEW", 80, GOLD)
    text(d, 760, "With our Tax Services partner", 56)
    pill(d, 900, "Link in bio →", size=60)
    text(d, 1030, "Referral partner • we may earn a fee", 38, MUTED, bold=False)
    text(d, 1090, "General info, not tax advice", 38, MUTED, bold=False)


TT1 = dict(
    key="tt1", slug="tax-strategy-year-end",
    segments=[
        "Your tax pro can't fix twenty twenty-six in March.",
        "Tax prep files what already happened. Tax strategy changes what happens next, and strategy has a deadline: December thirty-first.",
        "There are about ten weeks left. Timing of big purchases, how you pay yourself, your fourth quarter estimate due January fifteenth. Ask a tax pro now, not in March.",
        "Book a year-end tax review with our tax services partner. Link in bio.",
    ],
    funcs=[ad_tag(f) for f in (x1_hook, x2_prep, x3_weeks, x4_cta)],
)


# ---------- TT-2: Paid in 60 days, payroll on Friday (ROK factoring) ----------
def f1_hook(d, p, img):
    text(d, 470, "PAID IN 60 DAYS?", 96)
    text(d, 590, "PAYROLL IS FRIDAY", 82, GOLD)
    card(d, [90, 720, 525, 1200], "YOU INVOICE", "DAY 1", "work is done", GREEN)
    card(d, [555, 720, 990, 1200], "THEY PAY", "DAY 60", "cash is stuck", RED)
    text(d, 1320, "Your customers' cash flow is on your books.", 48, GOLD)


def f2_how(d, p, img):
    text(d, 470, "INVOICE FACTORING", 90, GOLD)
    text(d, 590, "Sell the invoice. Get cash now.", 58)
    bullets(d, p, ["70–90% of the invoice now", "The rest when they pay, less a fee", "Approval leans on your customers"], 720, step=150, size=46)


def f3_who(d, p, img):
    text(d, 470, "WHO IT FITS", 100, GOLD)
    bullets(d, p, ["Staffing agencies", "Construction subs", "B2B service firms"], 640, step=150, size=64)
    text(d, 1150, "Ask one question first:", 58)
    text(d, 1230, "What's the full fee in dollars?", 58, GOLD)


def f4_cta(d, p, img):
    text(d, 450, "COMPARE OPTIONS", 96)
    text(d, 570, "Factoring from $10K • soft pull", 58, GOLD)
    img.paste(ROK, ((W - ROK.width) // 2, 660))
    pill(d, 660 + ROK.height + 110, "Link in bio →", size=60)
    text(d, 660 + ROK.height + 230, "We only get paid if you get funded", 38, MUTED, bold=False)


TT2 = dict(
    key="tt2", slug="rok-invoice-factoring",
    segments=[
        "Your customers pay in sixty days. Your payroll is due Friday.",
        "Invoice factoring sells your unpaid B2B invoices for cash now. You typically get seventy to ninety percent up front, and the rest, minus a fee, when your customer pays.",
        "It fits staffing agencies, construction subs and B2B service firms. Before you sign, ask for the full fee in dollars.",
        "ROK Financial compares factoring with other funding, starting at ten thousand dollars. Checking is a soft pull. Link in bio.",
    ],
    funcs=[ad_tag(f) for f in (f1_hook, f2_how, f3_who, f4_cta)],
)

if __name__ == "__main__":
    for cfg in (TT1, TT2):
        if len(sys.argv) < 2 or sys.argv[1] == cfg["key"]:
            wk1.render(cfg)
