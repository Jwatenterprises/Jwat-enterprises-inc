"""JWAT TikTok (9:16): ROK "Bank: weeks. Marketplace: 48-72 hrs." for equipment financing.
Facts: blog/equipment-financing-for-contractors-2026.html (ROK equipment $10K-$5M, often 48-72 hrs after
approval, 500+ credit considered, soft pull). "#ad" tag stays on screen the whole video (FTC).
Reuses the look, voice and render pipeline from tiktok-week1.py via tiktok-week4.py helpers.
Usage: python tiktok-equipment-financing.py
"""
import importlib.util
from pathlib import Path

spec = importlib.util.spec_from_file_location("wk4", Path(__file__).parent / "tiktok-week4.py")
wk4 = importlib.util.module_from_spec(spec)
spec.loader.exec_module(wk4)
wk1 = wk4.wk1
W, text, pill, bullets, card, ad_tag, ROK = wk4.W, wk4.text, wk4.pill, wk4.bullets, wk4.card, wk4.ad_tag, wk4.ROK
GOLD, MUTED, RED, GREEN = wk4.GOLD, wk4.MUTED, wk4.RED, wk4.GREEN


def e1_hook(d, p, img):
    text(d, 470, "TURNING DOWN JOBS?", 84)
    text(d, 590, "FINANCE THE EQUIPMENT", 74, GOLD)
    card(d, [90, 720, 525, 1200], "BANK LOAN", "WEEKS", "sometimes months", RED)
    card(d, [555, 720, 990, 1200], "MARKETPLACE", "48–72", "hours after approval", GREEN)
    text(d, 1320, "The equipment is the collateral.", 54, GOLD)


def e2_what(d, p, img):
    text(d, 470, "WHAT YOU CAN FINANCE", 82, GOLD)
    bullets(d, p, ["Excavators & skid steers", "Dump trucks & work vans", "Generators & compressors", "Trailers, lifts & welders"], 660, step=140, size=54)
    text(d, 1260, "New or used.", 64, GOLD)


def e3_check(d, p, img):
    text(d, 470, "WHAT LENDERS CHECK", 86, GOLD)
    bullets(d, p, ["Credit: 500+ considered", "6+ months in business", "3 months of bank statements", "Make, model, year & price"], 660, step=140, size=52)
    text(d, 1260, "Soft pull to see your rate.", 58, GOLD)


def e4_cta(d, p, img):
    text(d, 450, "COMPARE OFFERS", 96)
    text(d, 570, "$10K–$5M • one application", 58, GOLD)
    img.paste(ROK, ((W - ROK.width) // 2, 660))
    pill(d, 660 + ROK.height + 110, "Link in bio →", size=60)
    text(d, 660 + ROK.height + 230, "We only get paid if you get funded", 38, MUTED, bold=False)
    text(d, 660 + ROK.height + 290, "Not financial advice", 38, MUTED, bold=False)


CFG = dict(
    key="eq", slug="rok-equipment-financing-contractors",
    segments=[
        "Turning down jobs for lack of equipment? A bank loan can take weeks. A lender marketplace often funds in forty-eight to seventy-two hours after approval.",
        "Finance excavators, dump trucks, work vans, generators and trailers. New or used.",
        "Lenders check credit, with five hundred plus considered, six months in business, and three months of bank statements. A soft pull shows your rate.",
        "ROK Financial compares equipment financing from ten thousand to five million dollars with one application. Link in bio.",
    ],
    funcs=[ad_tag(f) for f in (e1_hook, e2_what, e3_check, e4_cta)],
)

if __name__ == "__main__":
    wk1.render(CFG)
