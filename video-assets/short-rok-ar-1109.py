"""JWAT ROK Short for Mon 11/9 (9:16, YouTube Shorts + FB Reel only; ROK content stays off TikTok since the 10/20 spam flag).
Facts: ROK Financial partner email shared by Wayne 10/30/2026 -- a utilities company (pipeline construction management and
  inspection), referred by a business consultant; ROK secured a $1.25M working capital loan alongside a $5M A/R line of
  credit because its customers can take a while to pay. Never total it as $6.25M, no timeline, no client name.
Caliber QC 10/30: "slow to pay" (not "60 days"), "Example deal. Results vary." on screen, "#ad" tag the whole video (FTC).
Reuses the look, voice and render pipeline from tiktok-week-1102.py.
Usage: python short-rok-ar-1109.py
"""
import importlib.util
from pathlib import Path

spec = importlib.util.spec_from_file_location("wk1102", Path(__file__).parent / "tiktok-week-1102.py")
wk1102 = importlib.util.module_from_spec(spec)
spec.loader.exec_module(wk1102)
wk1 = wk1102.wk1
W, text, pill, bullets, card, ad_tag, ROK = wk1102.W, wk1102.text, wk1102.pill, wk1102.bullets, wk1102.card, wk1102.ad_tag, wk1102.ROK
GOLD, MUTED, RED, GREEN = wk1102.GOLD, wk1102.MUTED, wk1102.RED, wk1102.GREEN


def a1(d, p, img):
    text(d, 470, "PROFITABLE…", 100)
    text(d, 590, "BUT CAN'T MAKE PAYROLL?", 68, GOLD)
    card(d, [90, 720, 525, 1200], "JOB DONE", "SENT", "invoice out", GREEN)
    card(d, [555, 720, 990, 1200], "CUSTOMER", "LATER", "slow to pay", RED)
    text(d, 1320, "Your bills don't wait.", 56, GOLD)


def a2(d, p, img):
    text(d, 470, "ONE PIPELINE SERVICES CO.", 64, GOLD)
    text(d, 560, "TWO TOOLS FROM ROK", 86)
    card(d, [90, 700, 525, 1180], "WORKING CAPITAL", "$1.25M", "loan", GREEN)
    card(d, [555, 700, 990, 1180], "A/R LINE", "$5M", "line of credit", GREEN)
    text(d, 1300, "Example deal. Results vary.", 46, MUTED, bold=False)


def a3(d, p, img):
    text(d, 470, "HOW THEY WORK", 96, GOLD)
    bullets(d, p, ["Loan runs the business", "A/R line covers the wait", "Repay as customers pay", "One cash-flow fix"], 660, step=140, size=56)


def a4(d, p, img):
    text(d, 450, "INVOICE OTHER BUSINESSES?", 62)
    text(d, 570, "See what you qualify for", 58, GOLD)
    img.paste(ROK, ((W - ROK.width) // 2, 660))
    pill(d, 660 + ROK.height + 110, "Link in description →", size=56)
    text(d, 660 + ROK.height + 230, "We may earn a referral fee", 38, MUTED, bold=False)
    text(d, 660 + ROK.height + 290, "Example deal • Not financial advice", 38, MUTED, bold=False)


CFG = dict(key="rok-ar", slug="rok-ar-stack",
    segments=["Profitable, but can't make payroll? That's what happens when your customers are slow to pay and your bills don't wait.",
              "ROK Financial just helped a pipeline services company fix it with two tools: a one point two five million dollar working capital loan, plus a five million dollar A R line of credit.",
              "The loan runs the business. The A R line covers the gap while invoices get paid.",
              "If you invoice other businesses, see what you qualify for with ROK Financial. Link in the description."],
    funcs=[ad_tag(f) for f in (a1, a2, a3, a4)])

if __name__ == "__main__":
    wk1.render(CFG)
