"""JWAT 11/11-11/20 videos (9:16), approved by Wayne 2026-11-01 (business/jwat-weeks-1111-1116-drafts.md + Novo slot):
Wed 11/11 Nav "Have you seen it?" · Thu 11/12 Novo "Separate the money before tax season" · Fri 11/13 HighLevel "Holiday leads"
Mon 11/16 ROK "Year-end equipment + Section 179" (NOT for TikTok) · Wed 11/18 Nav "Two credit files" · Fri 11/20 HighLevel "Five inboxes".
Facts checked 11/1/2026: nav.com/nav-prime-2 (free basic ranges D&B/Creditsafe/Experian/Equifax + 1 Experian personal score;
Prime $39.99/$49.99/$74.99), gohighlevel.com/pricing (Starter $97/mo, 14-day trial), rok.biz (equipment $10K-$5M, 2-5 days),
novo.co (no-fee business checking, invoicing, integrations, Reserves; "Novo is a fintech, not a bank"; Middlesex Federal Savings,
F.A., Member FDIC), Section 179 2026 limit $2,560,000 (Rev. Proc. 2025-32 per tax publishers; "ask your tax pro").
"#ad" stays on screen the whole video. Reuses tiktok-week-1102.py / tiktok-week4.py look + tiktok-week1.py render.
Usage: python tiktok-weeks-1111.py [nav2 novo ghl2 rok179 nav3 ghl3]
"""
import sys, importlib.util
from pathlib import Path

spec = importlib.util.spec_from_file_location("w1102", Path(__file__).parent / "tiktok-week-1102.py")
w = importlib.util.module_from_spec(spec); spec.loader.exec_module(w)
W, text, pill, bullets, card, ad_tag, ROK, partner, _cta = w.W, w.text, w.pill, w.bullets, w.card, w.ad_tag, w.ROK, w.partner, w.cta
GOLD, MUTED, RED, GREEN, NAV, GHL, wk1 = w.GOLD, w.MUTED, w.RED, w.GREEN, w.NAV, w.GHL, w.wk1
NOVO = partner("novo.png")
UPF = partner("upfirst.jpg")


def cta(d, img, head, sub, logo, size=74):   # local copy of the 1102 CTA with a smaller headline (long headlines were clipped)
    text(d, 450, head, size)
    text(d, 570, sub, 58, GOLD)
    img.paste(logo, ((W - logo.width) // 2, 660))
    pill(d, 660 + logo.height + 110, "Link in bio →", size=60)
    text(d, 660 + logo.height + 230, "We may earn a commission", 38, MUTED, bold=False)
    text(d, 660 + logo.height + 290, "Not financial advice", 38, MUTED, bold=False)


def novo_cta(d, img):
    text(d, 450, "OPEN A NOVO ACCOUNT", 72)
    text(d, 570, "No-fee business checking", 58, GOLD)
    img.paste(NOVO, ((W - NOVO.width) // 2, 660))
    y = 660 + NOVO.height
    pill(d, y + 110, "Link in bio →", size=60)
    text(d, y + 230, "We may get a referral bonus", 38, MUTED, bold=False)
    text(d, y + 285, "Novo is a fintech, not a bank. Banking services:", 34, MUTED, bold=False)
    text(d, y + 335, "Middlesex Federal Savings, F.A., Member FDIC", 34, MUTED, bold=False)


# ---------- Wed 11/11 Nav: have you seen it? ----------
def a1(d, p, img):
    text(d, 470, "YOUR BUSINESS HAS", 92)
    text(d, 590, "A CREDIT REPORT", 92, GOLD)
    text(d, 760, "Lenders check it.", 70)
    text(d, 870, "Have you?", 96, GOLD)


def a2(d, p, img):
    text(d, 470, "NAV'S FREE PLAN SHOWS", 66, GOLD)
    bullets(d, p, ["Business credit ranges", "D&B · Experian", "Equifax · Creditsafe", "+ 1 personal score (Experian)"], 660, step=140, size=54)


def a3(d, p, img):
    cta(d, img, "SEE WHERE YOU STAND", "Free to start · before Q1", NAV)


# ---------- Thu 11/12 Novo: separate the money ----------
def v1(d, p, img):
    text(d, 470, "MIXING BUSINESS", 96)
    text(d, 590, "+ PERSONAL MONEY?", 80, GOLD)
    card(d, [90, 720, 525, 1200], "ONE ACCOUNT", "MESSY", "tax time", RED)
    card(d, [555, 720, 990, 1200], "SEPARATE", "CLEAN", "books", GREEN)
    text(d, 1320, "Fix it before tax season.", 56, GOLD)


def v2(d, p, img):
    text(d, 470, "NOVO BUSINESS CHECKING", 64, GOLD)
    bullets(d, p, ["No-fee business checking", "Send invoices, get paid", "Connects to your tools", "Reserves to set money aside"], 660, step=140, size=54)


def v3(d, p, img):
    novo_cta(d, img)


# ---------- Fri 11/13 HighLevel: holiday leads ----------
def h1(d, p, img):
    text(d, 470, "MISSED CALL", 100)
    text(d, 590, "= MISSED JOB", 100, GOLD)
    card(d, [90, 720, 525, 1200], "ON A JOB", "MISSED", "they call the next guy", RED)
    card(d, [555, 720, 990, 1200], "AUTO TEXT-BACK", "MINUTES", "they hear from you", GREEN)
    text(d, 1320, "The holiday rush won't wait.", 54, GOLD)


def h2(d, p, img):
    text(d, 470, "HIGHLEVEL STARTER", 90, GOLD)
    text(d, 640, "$97", 180)
    text(d, 790, "a month", 58)
    text(d, 960, "14-DAY FREE TRIAL", 80, GOLD)


def h3(d, p, img):
    cta(d, img, "NEVER MISS A LEAD", "14-day free trial", GHL)


# ---------- Fri 11/13 Upfirst: missed call = missed job (Wayne 11/1: Upfirst, not HighLevel) ----------
# upfirst.ai/pricing 11/1: Starter $24.95/mo (30 calls), 14-day free trial; 24/7 answering (all calls, overflow or after hours),
# call summaries by text/email, books appointments into Google/Outlook/Calendly etc., warm call transfer, spam blocking.
def u1(d, p, img):
    text(d, 470, "MISSED CALL", 100)
    text(d, 590, "= MISSED JOB", 100, GOLD)
    card(d, [90, 720, 525, 1200], "VOICEMAIL", "GONE", "they call the next guy", RED)
    card(d, [555, 720, 990, 1200], "UPFIRST", "24/7", "even on a job", GREEN)
    text(d, 1320, "The holiday rush won't wait.", 54, GOLD)


def u2(d, p, img):
    text(d, 470, "UPFIRST ANSWERS FOR YOU", 66, GOLD)
    bullets(d, p, ["Picks up 24/7 or after hours", "Texts you a call summary", "Books the appointment", "Blocks spam calls"], 660, step=140, size=54)


def u3(d, p, img):
    text(d, 470, "UPFIRST STARTER", 90, GOLD)
    text(d, 640, "$24.95", 160)
    text(d, 790, "a month · 30 calls", 58)
    text(d, 960, "14-DAY FREE TRIAL", 80, GOLD)


def u4(d, p, img):
    cta(d, img, "NEVER MISS A CALL", "14-day free trial", UPF)


# ---------- Mon 11/16 ROK: year-end equipment ----------
def k1(d, p, img):
    text(d, 470, "BUYING EQUIPMENT?", 92)
    text(d, 590, "DEC 31 MATTERS", 92, GOLD)
    text(d, 760, "Section 179 may let you deduct", 54)
    text(d, 840, "qualifying equipment placed", 54)
    text(d, 920, "in service this year.", 54)
    text(d, 1060, "2026 limit: $2.56M", 76, GOLD)
    text(d, 1160, "Ask your tax pro.", 50, MUTED, bold=False)


def k2(d, p, img):
    text(d, 470, "ROK EQUIPMENT FINANCING", 62, GOLD)
    bullets(d, p, ["$10K–$5M", "Funding in 2–5 days (per ROK)", "Use it now, spread the cost", "6 months in business, $10K+/mo"], 660, step=140, size=54)


def k3(d, p, img):
    cta(d, img, "CHECK YOUR OPTIONS", "Before Dec 31 · results vary", ROK)


# ---------- Wed 11/18 Nav: two credit files ----------
def b1(d, p, img):
    text(d, 470, "LENDERS CHECK", 100)
    text(d, 590, "TWO CREDIT FILES", 92, GOLD)
    card(d, [90, 720, 525, 1200], "YOURS", "1", "you know it", GREEN)
    card(d, [555, 720, 990, 1200], "YOUR BUSINESS", "?", "never seen it", RED)
    text(d, 1320, "Know both before you apply.", 54, GOLD)


def b2(d, p, img):
    cta(d, img, "SEE BOTH IN ONE PLACE", "Nav · free to start", NAV)


# ---------- Fri 11/20 HighLevel: five inboxes ----------
def f1(d, p, img):
    text(d, 470, "5 INBOXES", 110)
    text(d, 600, "1 MISSED CUSTOMER", 78, GOLD)
    bullets(d, p, ["Texts", "Email", "Facebook messages", "Instagram DMs", "Website forms"], 760, step=110, size=52)


def f2(d, p, img):
    text(d, 470, "ONE INBOX", 110, GOLD)
    text(d, 620, "+ automatic follow-up", 66)
    text(d, 820, "HighLevel Starter", 70)
    text(d, 920, "$97/mo · 14-day free trial", 60, GOLD)


def f3(d, p, img):
    cta(d, img, "NOTHING SLIPS THROUGH", "14-day free trial", GHL)


CFGS = {
    "nav2": dict(key="nav2", slug="nav-have-you-seen-it", segments=[
        "Your business has its own credit report, and lenders check it. Have you ever seen yours?",
        "Nav's free plan shows basic business credit ranges from Dun and Bradstreet, Experian, Equifax and Creditsafe, plus one personal score from Experian.",
        "See where you stand before you apply in the new year. Free to start, link in bio."],
        funcs=[ad_tag(f) for f in (a1, a2, a3)]),
    "novo": dict(key="novo", slug="novo-separate-money", segments=[
        "Still running business and personal money through one account? Tax time gets messy fast.",
        "Novo is no-fee business checking: send invoices, get paid, connect your tools, and set money aside with reserves.",
        "Separate your money before tax season. Novo is a fintech, not a bank. Link in bio."],
        funcs=[ad_tag(f) for f in (v1, v2, v3)]),
    "ghl2": dict(key="ghl2", slug="highlevel-holiday-leads", segments=[
        "A missed call is a missed job. You're on a ladder, they get voicemail, and they call the next company.",
        "HighLevel texts and emails new leads back automatically. The Starter plan is ninety seven dollars a month, with a fourteen day free trial.",
        "Don't let the holiday rush cost you jobs. Free trial, link in bio."],
        funcs=[ad_tag(f) for f in (h1, h2, h3)]),
    "upf": dict(key="upf", slug="upfirst-missed-call", segments=[
        "A missed call is a missed job. You're on a job, the call goes to voicemail, and they call the next company.",
        "Upfirst answers your business line for you, around the clock or just after hours. You get a text with the call summary, and it can book the appointment.",
        "The Starter plan is twenty four ninety five a month for thirty calls, with a fourteen day free trial.",
        "Never miss a call this holiday rush. Free trial, link in bio."],
        funcs=[ad_tag(f) for f in (u1, u2, u3, u4)]),
    "rok179": dict(key="rok179", slug="rok-year-end-equipment", segments=[
        "Buying equipment anyway? December thirty first matters. Section one seventy nine may let you deduct qualifying equipment you place in service this year, up to two point five six million dollars in twenty twenty six. Ask your tax pro.",
        "ROK Financial's equipment financing runs from ten thousand to five million dollars, with funding in two to five days according to ROK.",
        "Check your options before year end. Results vary. Link in the description."],
        funcs=[ad_tag(f) for f in (k1, k2, k3)]),
    "nav3": dict(key="nav3", slug="nav-two-credit-files", segments=[
        "Lenders often check two credit files: yours, and your business's. Most owners have only seen one.",
        "Nav shows both in one place, free to start. Link in bio."],
        funcs=[ad_tag(f) for f in (b1, b2)]),
    "ghl3": dict(key="ghl3", slug="highlevel-five-inboxes", segments=[
        "Five inboxes. Texts, email, Facebook, Instagram and your website. Miss one, and you miss a customer.",
        "HighLevel brings them into one inbox and follows up automatically. Starter is ninety seven dollars a month, with a fourteen day free trial.",
        "Nothing slips through. Free trial, link in bio."],
        funcs=[ad_tag(f) for f in (f1, f2, f3)]),
}

if __name__ == "__main__":
    for k in (sys.argv[1:] or list(CFGS)):
        wk1.render(CFGS[k])
