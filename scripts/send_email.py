import anthropic
import os
import requests
from datetime import datetime

BREVO_KEY = os.environ["BREVO_API_KEY"]
BREVO_BASE = "https://api.brevo.com/v3"
BREVO_HEADERS = {"api-key": BREVO_KEY, "Content-Type": "application/json"}

LIST_ID = 3  # JWAT Newsletter

EMAIL_SYSTEM_PROMPT = """You are a business growth advisor writing the weekly email newsletter for JWAT Enterprises Inc, an AI-powered consulting firm in Riverview, FL that helps small businesses with sales, marketing, financial management, and sales funnel consulting.

Write direct, value-first content. Every email must give the reader something they can use today. Tone: like a trusted business advisor talking to a fellow entrepreneur. No fluff.

Business: JWAT Enterprises Inc | CEO: Wayne | biz@jwatenterprisesinc.com | 813-321-5686 | https://www.jwatenterprisesinc.com | Book: https://calendly.com/biz-jwatenterprisesinc"""

EMAIL_TOOL = {
    "name": "send_weekly_email",
    "description": "Generate a complete weekly email newsletter for JWAT Enterprises Inc",
    "input_schema": {
        "type": "object",
        "properties": {
            "subject":      {"type": "string", "description": "Subject line, under 60 chars, compelling but not clickbait"},
            "preview_text": {"type": "string", "description": "Inbox preview text, under 90 chars"},
            "greeting":     {"type": "string", "description": "Opening line, e.g. Hope your week is off to a strong start."},
            "intro_html":   {"type": "string", "description": "1-2 paragraph intro using <p> tags"},
            "tip_1_title":  {"type": "string", "description": "First tip headline"},
            "tip_1_body":   {"type": "string", "description": "First tip, 2-4 sentences, actionable"},
            "tip_2_title":  {"type": "string", "description": "Second tip headline"},
            "tip_2_body":   {"type": "string", "description": "Second tip, 2-4 sentences, actionable"},
            "tip_3_title":  {"type": "string", "description": "Third tip headline"},
            "tip_3_body":   {"type": "string", "description": "Third tip, 2-4 sentences, actionable"},
            "cta_headline": {"type": "string", "description": "CTA headline, e.g. Ready to put this into action?"},
            "cta_body":     {"type": "string", "description": "1-2 sentence CTA supporting copy"},
            "closing_line": {"type": "string", "description": "Sign-off line before signature, e.g. To your growth,"}
        },
        "required": ["subject","preview_text","greeting","intro_html","tip_1_title","tip_1_body","tip_2_title","tip_2_body","tip_3_title","tip_3_body","cta_headline","cta_body","closing_line"]
    }
}

WEEKLY_THEMES = [
    "turning cold leads into paying clients",
    "building a sales funnel that works while you sleep",
    "pricing your services for profit, not just revenue",
    "getting clients through LinkedIn without paid ads",
    "the 90-day revenue plan every small business needs",
    "why your follow-up strategy is leaking money",
    "building business credit from zero",
    "automating your client onboarding process",
    "how to write proposals that close deals",
    "turning happy clients into a referral machine",
    "the financial metrics you must track every month",
    "running Facebook ads that actually convert",
]


def pick_theme(week_number):
    return WEEKLY_THEMES[week_number % len(WEEKLY_THEMES)]


def get_subscriber_count():
    resp = requests.get(f"{BREVO_BASE}/contacts/lists/{LIST_ID}", headers=BREVO_HEADERS)
    resp.raise_for_status()
    return resp.json().get("uniqueSubscribers", 0)


def generate_email(theme, pub_date):
    client = anthropic.Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"])
    message = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=3000,
        system=EMAIL_SYSTEM_PROMPT,
        tools=[EMAIL_TOOL],
        tool_choice={"type": "any"},
        messages=[{"role": "user", "content": f"Write this week newsletter. Theme: {theme}. Date: {pub_date.strftime('%B %d, %Y')}."}]
    )
    tool_block = next(b for b in message.content if b.type == "tool_use")
    return tool_block.input


def build_html(d, pub_date):
    tips_rows = ""
    for i in range(1, 4):
        tips_rows += (
            "<tr><td style='padding:0 40px 28px;'>"
            "<table width='100%' cellpadding='0' cellspacing='0' style='background:#f8f9fa;border-radius:8px;border-left:4px solid #ffd700;'>"
            "<tr><td style='padding:20px 24px;'>"
            f"<div style='font-size:13px;font-weight:700;color:#1a365d;text-transform:uppercase;letter-spacing:0.5px;margin-bottom:6px;'>Tip {i}</div>"
            f"<div style='font-size:17px;font-weight:700;color:#1a365d;margin-bottom:10px;'>{d[f'tip_{i}_title']}</div>"
            f"<div style='font-size:15px;color:#444;line-height:1.7;'>{d[f'tip_{i}_body']}</div>"
            "</td></tr></table></td></tr>"
        )

    return f"""<!DOCTYPE html>
<html lang="en">
<head><meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1.0">
<title>{d["subject"]}</title></head>
<body style="margin:0;padding:0;background:#f0f2f5;font-family:'Segoe UI',Arial,Helvetica,sans-serif;">
<table width="100%" cellpadding="0" cellspacing="0" style="background:#f0f2f5;">
<tr><td align="center" style="padding:24px 16px;">
<table width="600" cellpadding="0" cellspacing="0" style="max-width:600px;width:100%;background:#ffffff;border-radius:10px;overflow:hidden;box-shadow:0 2px 12px rgba(0,0,0,0.08);">
<tr><td style="background:linear-gradient(135deg,#1a365d 0%,#2d5a8c 100%);padding:32px 40px;text-align:center;">
  <div style="font-size:22px;font-weight:800;color:#ffd700;letter-spacing:1px;">JWAT ENTERPRISES INC</div>
  <div style="font-size:11px;color:rgba(255,255,255,0.75);letter-spacing:2px;text-transform:uppercase;margin-top:6px;">Weekly Business Growth Brief</div>
  <div style="font-size:12px;color:rgba(255,255,255,0.5);margin-top:8px;">{pub_date.strftime("%B %d, %Y")}</div>
</td></tr>
<tr><td style="padding:36px 40px 8px;">
  <p style="font-size:16px;color:#555;margin:0;">{d["greeting"]}</p>
</td></tr>
<tr><td style="padding:16px 40px 28px;font-size:16px;color:#333;line-height:1.8;">{d["intro_html"]}</td></tr>
<tr><td style="padding:0 40px 28px;">
  <div style="border-top:2px solid #ffd700;"></div>
  <div style="font-size:13px;font-weight:700;color:#1a365d;text-transform:uppercase;letter-spacing:1px;margin-top:20px;">This Week's Growth Tips</div>
</td></tr>
{tips_rows}
<tr><td style="padding:8px 40px 36px;">
  <table width="100%" cellpadding="0" cellspacing="0" style="background:linear-gradient(135deg,#1a365d,#2d5a8c);border-radius:10px;">
  <tr><td style="padding:32px;text-align:center;">
    <div style="font-size:20px;font-weight:700;color:#ffffff;margin-bottom:10px;">{d["cta_headline"]}</div>
    <div style="font-size:15px;color:rgba(255,255,255,0.85);margin-bottom:24px;">{d["cta_body"]}</div>
    <a href="https://calendly.com/biz-jwatenterprisesinc" style="background:#ffd700;color:#1a365d;font-weight:700;padding:14px 32px;border-radius:5px;text-decoration:none;font-size:15px;display:inline-block;">Book Your Free Audit &#8594;</a>
  </td></tr></table>
</td></tr>
<tr><td style="padding:0 40px 32px;">
  <p style="font-size:15px;color:#555;margin:0 0 6px;">{d["closing_line"]}</p>
  <p style="font-size:15px;font-weight:700;color:#1a365d;margin:0;">Wayne</p>
  <p style="font-size:13px;color:#888;margin:4px 0 0;">CEO, JWAT Enterprises Inc</p>
  <p style="font-size:13px;color:#888;margin:2px 0 0;">813-321-5686 &nbsp;|&nbsp; <a href="https://www.jwatenterprisesinc.com" style="color:#2d5a8c;text-decoration:none;">jwatenterprisesinc.com</a></p>
</td></tr>
<tr><td style="background:#0d1b2a;padding:20px 40px;text-align:center;">
  <p style="color:rgba(255,255,255,0.5);font-size:12px;margin:0;line-height:1.8;">
    &copy; {pub_date.year} JWAT Enterprises Inc &nbsp;&middot;&nbsp; 6520 U.S. 301 HWY #112B, Riverview, FL 33578<br>
    <a href="https://www.jwatenterprisesinc.com" style="color:#ffd700;text-decoration:none;">jwatenterprisesinc.com</a>
    &nbsp;&middot;&nbsp;
    <a href="{{unsubscribeLink}}" style="color:rgba(255,255,255,0.4);text-decoration:none;">Unsubscribe</a>
  </p>
</td></tr>
</table>
</td></tr>
</table>
</body>
</html>"""


def create_and_send_campaign(email_data, html, pub_date):
    campaign = {
        "name": f"JWAT Weekly — {pub_date.strftime('%B %d, %Y')}",
        "subject": email_data["subject"],
        "previewText": email_data["preview_text"],
        "sender": {"name": "Wayne at JWAT Enterprises", "email": "biz@jwatenterprisesinc.com"},
        "type": "classic",
        "htmlContent": html,
        "recipients": {"listIds": [LIST_ID]},
    }
    resp = requests.post(f"{BREVO_BASE}/emailCampaigns", headers=BREVO_HEADERS, json=campaign)
    resp.raise_for_status()
    campaign_id = resp.json()["id"]
    print(f"Campaign created: ID {campaign_id}")
    send_resp = requests.post(f"{BREVO_BASE}/emailCampaigns/{campaign_id}/sendNow", headers=BREVO_HEADERS)
    send_resp.raise_for_status()
    print(f"Campaign sent to list {LIST_ID}")
    return campaign_id


if __name__ == "__main__":
    pub_date = datetime.now()
    week_number = pub_date.isocalendar()[1]

    count = get_subscriber_count()
    print(f"Subscribers: {count}")

    theme = pick_theme(week_number)
    print(f"Theme: {theme}")

    email_data = generate_email(theme, pub_date)
    print(f"Subject: {email_data['subject']}")

    html = build_html(email_data, pub_date)

    if count > 0:
        campaign_id = create_and_send_campaign(email_data, html, pub_date)
        print(f"Done. Campaign ID: {campaign_id}")
    else:
        print("No subscribers yet. Email generated but not sent.")
        print("Add subscribers to Brevo list ID 3 to enable sending.")
