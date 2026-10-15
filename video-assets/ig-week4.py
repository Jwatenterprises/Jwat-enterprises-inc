"""JWAT Week 4 Instagram + Facebook images (1080x1350), same look as Weeks 2-3: navy gradient, partner image on top,
white headline + gold subline, #ad pill, footer bar with logo + site.
Out: ../images/social/week4/  (ig1-01..07 carousel = 5 money moves, ig2 = tax strategy, ig3 = factoring/ROK,
     ig4 = Novo Reserves, fb4 = contractors/ROK). Theme: close 2026 clean, taxes and cash.
Usage: python ig-week4.py
"""
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

D = Path(__file__).parent
IMGS = D.parent / "images"
OUT = IMGS / "social" / "week4"
W, H = 1080, 1350
NAVY, NAVY_L, DARK = (26, 54, 93), (45, 90, 140), (13, 27, 42)
GOLD, WHITE, MUTED = (255, 215, 0), (255, 255, 255), (190, 200, 215)
FOOT = (16, 33, 56)


def font(size, weight="black"):
    f = {"black": "seguibl.ttf", "bold": "segoeuib.ttf", "reg": "segoeui.ttf"}[weight]
    try:
        return ImageFont.truetype(f"C:/Windows/Fonts/{f}", size)
    except OSError:
        return ImageFont.truetype("C:/Windows/Fonts/arialbd.ttf" if weight != "reg" else "C:/Windows/Fonts/arial.ttf", size)


def base():
    img = Image.new("RGB", (W, H))
    d = ImageDraw.Draw(img)
    for y in range(H):
        r = y / H
        a, b, k = (DARK, NAVY, r * 2) if r < .5 else (NAVY, NAVY_L, (r - .5) * 2)
        d.line([(0, y), (W, y)], fill=tuple(int(a[i] + (b[i] - a[i]) * k) for i in range(3)))
    d.rectangle([0, H - 120, W, H], fill=FOOT)
    logo = Image.open(IMGS / "jwat-logo.png").convert("RGBA")
    logo.thumbnail((150, 90))
    img.paste(logo, (50, H - 60 - logo.height // 2), logo)
    d.text((W - 50, H - 60), "jwatenterprisesinc.com", font=font(34, "bold"), fill=GOLD, anchor="rm")
    d.rounded_rectangle([W - 150, 30, W - 40, 80], 25, fill=DARK)
    d.text((W - 95, 55), "#ad", font=font(30, "bold"), fill=WHITE, anchor="mm")
    return img, d


def wrap(d, s, f, maxw):
    words, lines, cur = s.split(), [], ""
    for w in words:
        t = (cur + " " + w).strip()
        if d.textlength(t, font=f) <= maxw:
            cur = t
        else:
            lines.append(cur); cur = w
    lines.append(cur)
    return lines


def block(d, y, s, size, color, weight="black", maxw=W - 120, gap=1.12):
    f = font(size, weight)
    for line in wrap(d, s, f, maxw):
        d.text((60, y), line, font=f, fill=color)
        y += int(size * gap)
    return y


def partner_top(img, name, maxh=420):
    p = Image.open(IMGS / "partners" / name).convert("RGB")
    p.thumbnail((W - 120, maxh))
    img.paste(p, (60, 110))
    return 110 + p.height


def pill(d, x, y, s, size=34):
    f = font(size, "black")
    w = d.textlength(s, font=f)
    d.rounded_rectangle([x, y, x + w + 60, y + size + 34], (size + 34) // 2, fill=GOLD)
    d.text((x + 30, y + (size + 34) // 2), s, font=f, fill=DARK, anchor="lm")


def save(img, name):
    OUT.mkdir(parents=True, exist_ok=True)
    img.save(OUT / name, quality=92)


# ---- IG-1 carousel: 5 money moves before Dec 31 ----
img, d = base()
d.text((60, 190), "2026", font=font(240), fill=GOLD)
y = block(d, 500, "5 money moves before Dec 31", 84, WHITE)
block(d, y + 10, "10 weeks left. One a week.", 56, GOLD, "bold")
d.text((60, H - 200), "Swipe  →", font=font(44, "bold"), fill=WHITE)
save(img, "ig1-01.jpg")

slides = [
    ("Book a year-end tax review", "Not just tax prep. Strategy happens before Dec 31, prep happens after."),
    ("Set aside tax money in its own account", "If it sits in operating, it gets spent."),
    ("Know your Q4 estimated payment", "Due January 15. Ask your tax pro what yours should be."),
    ("Collect or fund unpaid invoices", "Cash stuck in receivables can't make payroll."),
    ("Line up capital before the slow season", "Apply while your numbers are strong, not after the dip."),
]
for i, (head, sub) in enumerate(slides, start=2):
    img, d = base()
    d.text((W - 60, 130), f"{i - 1}/5", font=font(36, "bold"), fill=WHITE, anchor="ra")
    d.text((60, 160), str(i - 1), font=font(260), fill=GOLD)
    y = block(d, 520, head, 70, WHITE)
    block(d, y + 20, sub, 44, MUTED, "reg")
    save(img, f"ig1-0{i}.jpg")

img, d = base()
y = block(d, 260, "Partners for each move", 72, WHITE)
for s in ["Tax review: Tax Services", "Tax money: Novo Reserves", "Invoices + capital: ROK Financial"]:
    y = block(d, y + 26, "• " + s, 46, GOLD, "bold")
pill(d, 60, y + 60, "LINKS IN BIO")
d.text((60, H - 170), "Affiliate links · we may earn a commission or referral fee", font=font(28, "reg"), fill=MUTED)
save(img, "ig1-07.jpg")

# ---- IG-2 / FB-1: Tax strategy ----
img, d = base()
d.text((60, 190), "TAX", font=font(170), fill=GOLD)
y = block(d, 400, "Tax prep looks back.", 86, WHITE)
y = block(d, y + 5, "Tax strategy looks ahead.", 86, GOLD)
y = block(d, y + 30, "The moves that shape your 2026 return happen before Dec 31.", 46, MUTED, "reg")
pill(d, 60, H - 250, "YEAR-END TAX REVIEW · LINK IN BIO", 30)
d.text((60, H - 170), "Referral partner · we may earn a fee", font=font(28, "reg"), fill=MUTED)
save(img, "ig2.jpg")

# ---- IG-3 / FB-2: Factoring (ROK) ----
img, d = base()
y = partner_top(img, "rok-financial.png", 330)
y = block(d, y + 60, "Paid in 60 days.", 82, WHITE)
y = block(d, y + 5, "Payroll on Friday.", 82, GOLD)
for s in ["Factoring can advance 70–90% of a B2B invoice", "Ask for the full fee in dollars", "Soft pull to see your options"]:
    y = block(d, y + 18, "• " + s, 40, WHITE, "bold")
pill(d, 60, H - 250, "LINK IN BIO")
d.text((60, H - 170), "We only get paid if you get funded", font=font(28, "reg"), fill=MUTED)
save(img, "ig3.jpg")

# ---- IG-4 / FB-3: Novo Reserves ----
img, d = base()
y = partner_top(img, "novo.png", 330)
y = block(d, y + 60, "Tax money in your operating account gets spent.", 70, WHITE)
y = block(d, y + 20, "Split it off with Novo Reserves:", 46, GOLD, "bold")
for s in ["Taxes", "Payroll", "Emergency fund"]:
    y = block(d, y + 14, "• " + s, 44, WHITE, "bold")
pill(d, 60, H - 250, "NO MONTHLY FEES · LINK IN BIO", 30)
d.text((60, H - 170), "Referral link · we may earn a bonus", font=font(28, "reg"), fill=MUTED)
save(img, "ig4.jpg")

# ---- FB-4: Contractors (ROK) ----
img, d = base()
y = partner_top(img, "rok-financial.png", 330)
y = block(d, y + 60, "Contractors: fund the winter gap.", 78, WHITE)
y = block(d, y + 10, "The jobs slow down. The truck payment doesn't.", 46, GOLD, "bold")
for s in ["$10K+ monthly revenue", "500+ credit score may qualify", "Working capital as fast as 24 hours"]:
    y = block(d, y + 18, "• " + s, 42, WHITE, "bold")
pill(d, 60, H - 250, "SOFT PULL · SEE OPTIONS")
d.text((60, H - 170), "We only get paid if you get funded", font=font(28, "reg"), fill=MUTED)
save(img, "fb4.jpg")
print("saved to", OUT)
