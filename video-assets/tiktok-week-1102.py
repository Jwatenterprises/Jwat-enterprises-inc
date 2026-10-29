"""JWAT week of 11/2 TikToks (9:16): ROK "Bank said no?", Nav "Scores you've never seen", HighLevel "Leads go cold".
Facts checked 10/29/2026 on the partners' own sites:
  ROK (rok.biz): working capital / business loans $10K-$5M, funding in as little as 1-3 days; qualify with 6 months in
    business, $10K+ monthly sales, 500 credit score.
  Nav (nav.com/nav-prime-2): free plan = basic business credit ranges from D&B, Creditsafe, Experian and Equifax + 1
    personal Experian score; Nav Prime from $39.99/mo adds a business tradeline and 7 credit scores.
  HighLevel (gohighlevel.com/pricing): Starter $97/mo, 14-day free trial; CRM & pipelines, email + SMS, booking calendars,
    website & funnel builder.
"#ad" tag stays on screen the whole video (FTC). Reuses the look, voice and render pipeline from tiktok-week4.py.
Usage: python tiktok-week-1102.py [rok|nav|ghl]
"""
import sys
import importlib.util
from pathlib import Path

spec = importlib.util.spec_from_file_location("wk4", Path(__file__).parent / "tiktok-week4.py")
wk4 = importlib.util.module_from_spec(spec)
spec.loader.exec_module(wk4)
wk1 = wk4.wk1
W, text, pill, bullets, card, ad_tag, ROK, partner = wk4.W, wk4.text, wk4.pill, wk4.bullets, wk4.card, wk4.ad_tag, wk4.ROK, wk4.partner
GOLD, MUTED, RED, GREEN = wk4.GOLD, wk4.MUTED, wk4.RED, wk4.GREEN
NAV = partner("nav.png")
GHL = partner("gohighlevel.png")


def cta(d, img, head, sub, logo):
    text(d, 450, head, 96)
    text(d, 570, sub, 58, GOLD)
    img.paste(logo, ((W - logo.width) // 2, 660))
    pill(d, 660 + logo.height + 110, "Link in bio →", size=60)
    text(d, 660 + logo.height + 230, "We may earn a commission", 38, MUTED, bold=False)
    text(d, 660 + logo.height + 290, "Not financial advice", 38, MUTED, bold=False)


# ---------- ROK: Bank said no? ----------
def r1(d, p, img):
    text(d, 470, "BANK SAID NO?", 100)
    text(d, 590, "THAT'S ONE LENDER", 76, GOLD)
    card(d, [90, 720, 525, 1200], "ONE BANK", "1", "yes or no", RED)
    card(d, [555, 720, 990, 1200], "MARKETPLACE", "MANY", "lenders compete", GREEN)
    text(d, 1320, "One application. Several offers.", 54, GOLD)


def r2(d, p, img):
    text(d, 470, "THIS WEEK, DO THIS", 86, GOLD)
    bullets(d, p, ["Get the reason in writing", "Check your business credit", "Know your exact cash need", "Gather 3–6 months of statements"], 660, step=140, size=52)


def r3(d, p, img):
    text(d, 470, "WHAT ROK ASKS FOR", 86, GOLD)
    bullets(d, p, ["6 months in business", "$10K+ in monthly sales", "500+ credit score"], 660, step=150, size=58)
    text(d, 1200, "Funding in as little as", 58)
    text(d, 1290, "1–3 DAYS", 96, GOLD)


def r4(d, p, img):
    cta(d, img, "SEE YOUR OFFERS", "$10K–$5M • one application", ROK)


# ---------- Nav: scores you've never seen ----------
def n1(d, p, img):
    text(d, 470, "LENDERS CHECK", 100)
    text(d, 590, "SCORES YOU'VE NEVER SEEN", 66, GOLD)
    card(d, [90, 720, 525, 1200], "PERSONAL", "1", "score you know", RED)
    card(d, [555, 720, 990, 1200], "BUSINESS", "4+", "bureaus watching", GREEN)
    text(d, 1320, "Your business has its own credit file.", 50, GOLD)


def n2(d, p, img):
    text(d, 470, "WHO TRACKS IT", 96, GOLD)
    bullets(d, p, ["Dun & Bradstreet", "Experian Business", "Equifax Business", "Creditsafe"], 660, step=140, size=58)
    text(d, 1260, "Check before you apply.", 60, GOLD)


def n3(d, p, img):
    text(d, 470, "SEE IT FREE", 100, GOLD)
    bullets(d, p, ["Business credit ranges: $0", "Prime from $39.99/mo", "Adds a business tradeline", "Shows 7 credit scores"], 660, step=140, size=54)
    text(d, 1260, "No guesswork at the bank.", 58, GOLD)


def n4(d, p, img):
    cta(d, img, "KNOW YOUR SCORES", "Start with a free Nav account", NAV)


# ---------- HighLevel: leads go cold ----------
def g1(d, p, img):
    text(d, 470, "LEADS GO COLD", 100)
    text(d, 590, "WHILE YOU'RE ON THE JOB", 70, GOLD)
    card(d, [90, 720, 525, 1200], "NO SYSTEM", "LATER", "you forget", RED)
    card(d, [555, 720, 990, 1200], "AUTOMATED", "NOW", "text + email", GREEN)
    text(d, 1320, "Reply fast. Win the job.", 56, GOLD)


def g2(d, p, img):
    text(d, 470, "ONE PLACE FOR", 96, GOLD)
    bullets(d, p, ["Every lead and contact", "Follow-up texts and emails", "Booking calendar", "Website and funnels"], 660, step=140, size=56)


def g3(d, p, img):
    text(d, 470, "HIGHLEVEL STARTER", 90, GOLD)
    text(d, 640, "$97", 180)
    text(d, 790, "a month", 58)
    text(d, 960, "14-DAY FREE TRIAL", 80, GOLD)
    text(d, 1080, "Try it before you pay.", 56)


def g4(d, p, img):
    cta(d, img, "STOP LOSING LEADS", "14-day free trial", GHL)


CFGS = {
    "rok": dict(key="rok", slug="rok-bank-said-no",
        segments=["The bank said no? That's one lender's answer. A lending marketplace sends one application to many lenders, so they compete for your deal.",
                  "This week: get the reason in writing, check your business credit, know exactly how much you need, and gather three to six months of bank statements.",
                  "ROK Financial asks for six months in business, ten thousand dollars a month in sales, and a five hundred credit score. Funding can come in as little as one to three days.",
                  "See your offers from ten thousand to five million dollars with one application. Link in bio."],
        funcs=[ad_tag(f) for f in (r1, r2, r3, r4)]),
    "nav": dict(key="nav", slug="nav-business-credit-scores",
        segments=["Lenders check credit scores you've probably never seen. Your business has its own credit file, separate from your personal score.",
                  "Dun and Bradstreet, Experian, Equifax and Creditsafe all track your business. Check before you apply.",
                  "Nav shows your business credit ranges for free. Nav Prime, from thirty nine ninety nine a month, adds a business tradeline and seven credit scores.",
                  "Know your scores before the bank does. Free Nav account, link in bio."],
        funcs=[ad_tag(f) for f in (n1, n2, n3, n4)]),
    "ghl": dict(key="ghl", slug="highlevel-leads-go-cold",
        segments=["Leads go cold while you're on the job. Without a system, you call back later. With automation, they get a text and an email right away.",
                  "HighLevel keeps every lead, your follow-up texts and emails, a booking calendar and your website in one place.",
                  "The Starter plan is ninety seven dollars a month, with a fourteen day free trial.",
                  "Stop losing leads. Start your free trial, link in bio."],
        funcs=[ad_tag(f) for f in (g1, g2, g3, g4)]),
}

if __name__ == "__main__":
    for k in (sys.argv[1:] or list(CFGS)):
        wk1.render(CFGS[k])
