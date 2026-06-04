import anthropic
import os
import re
from datetime import datetime

PARTNER_CAMPAIGNS = [
    {
        "partner": "Nav",
        "category": "Business Funding",
        "topic": "How to Build Business Credit Before You Need Funding",
        "slug": "build-business-credit-before-funding",
        "url": "https://nav.nkwcmr.net/c/6782322/1849064/2410",
        "cta_headline": "Check Your Business Credit With Nav",
        "cta_body": "Nav helps small business owners monitor business credit, understand funding readiness, and find better financing options before cash gets tight.",
        "cta_label": "Start With Nav",
    },
    {
        "partner": "ROK Financial",
        "category": "Business Funding",
        "topic": "Working Capital vs Line of Credit: Which Funding Option Fits Your Business?",
        "slug": "working-capital-vs-line-of-credit",
        "url": "https://go.mypartner.io/business-financing/?ref=001Qk00000dxUurIAE",
        "cta_headline": "Compare Business Funding Options With ROK Financial",
        "cta_body": "ROK Financial helps small business owners explore working capital, term loans, lines of credit, and other funding options through one application path.",
        "cta_label": "Explore Funding",
    },
    {
        "partner": "Upfirst",
        "category": "Lead Generation",
        "topic": "How Missed Calls Turn Into Lost Revenue for Small Businesses",
        "slug": "missed-calls-lost-revenue-small-business",
        "url": "https://upfirst.ai?plid=135267",
        "cta_headline": "Let Upfirst Answer Every Lead Call",
        "cta_body": "Upfirst gives small businesses an AI receptionist that answers calls, qualifies leads, books appointments, and keeps the front end of the funnel covered.",
        "cta_label": "Try Upfirst",
    },
    {
        "partner": "Tax Services",
        "category": "Financial Management",
        "topic": "Quarterly Tax Planning for Small Business Owners Who Want Fewer Surprises",
        "slug": "quarterly-tax-planning-small-business",
        "url": "https://form.jotform.com/250436502189153",
        "cta_headline": "Start Your Small Business Tax Intake",
        "cta_body": "Get organized before tax season. Use the JWAT tax intake form to start the process for small business tax preparation and planning support.",
        "cta_label": "Complete Tax Intake",
    },
    {
        "partner": "GoHighLevel",
        "category": "Sales Strategy",
        "topic": "How to Build a CRM Follow-Up System That Stops Leads From Slipping Away",
        "slug": "crm-follow-up-system-stop-losing-leads",
        "url": "https://affiliate.gohighlevel.com?sref=lb90qrm",
        "cta_headline": "Build Your Follow-Up System With GoHighLevel",
        "cta_body": "GoHighLevel gives small businesses one place for CRM, pipelines, funnels, email, SMS, calendar booking, and automated follow-up.",
        "cta_label": "Start GoHighLevel",
    },
    {
        "partner": "Nav",
        "category": "Business Funding",
        "topic": "Business Credit Monitoring: What Small Business Owners Should Watch Monthly",
        "slug": "business-credit-monitoring-monthly",
        "url": "https://nav.nkwcmr.net/c/6782322/1849064/2410",
        "cta_headline": "Monitor Your Business Credit With Nav",
        "cta_body": "Nav gives business owners a clearer view of their credit profile, funding matches, and financial health signals.",
        "cta_label": "Check Your Credit",
    },
    {
        "partner": "ROK Financial",
        "category": "Business Funding",
        "topic": "How to Prepare Your Business Before Applying for Funding",
        "slug": "prepare-business-before-applying-funding",
        "url": "https://go.mypartner.io/business-financing/?ref=001Qk00000dxUurIAE",
        "cta_headline": "See What Funding Your Business May Qualify For",
        "cta_body": "ROK Financial can help you compare funding options once your revenue, bank statements, and business basics are ready.",
        "cta_label": "Review Funding Options",
    },
    {
        "partner": "Upfirst",
        "category": "Lead Generation",
        "topic": "The 24/7 Lead Capture System Every Local Service Business Needs",
        "slug": "24-7-lead-capture-local-service-business",
        "url": "https://upfirst.ai?plid=135267",
        "cta_headline": "Capture More Calls With Upfirst",
        "cta_body": "Upfirst helps turn after-hours and missed calls into captured leads, booked appointments, and cleaner follow-up.",
        "cta_label": "Set Up Upfirst",
    },
    {
        "partner": "Tax Services",
        "category": "Financial Management",
        "topic": "Tax Strategy vs Tax Preparation: What Small Business Owners Need to Know",
        "slug": "tax-strategy-vs-tax-preparation",
        "url": "https://form.jotform.com/250436502189153",
        "cta_headline": "Get Your Tax Intake Started",
        "cta_body": "JWAT connects small business owners with tax preparation and planning support so the numbers stay cleaner year-round.",
        "cta_label": "Start Tax Intake",
    },
    {
        "partner": "GoHighLevel",
        "category": "Marketing",
        "topic": "Why Small Businesses Need CRM, Funnels, and Follow-Up in One System",
        "slug": "crm-funnels-follow-up-one-system",
        "url": "https://affiliate.gohighlevel.com?sref=lb90qrm",
        "cta_headline": "Run Your Growth System Inside GoHighLevel",
        "cta_body": "GoHighLevel replaces scattered tools with one operating system for lead capture, nurturing, booking, and sales pipeline management.",
        "cta_label": "Try GoHighLevel",
    },
]

BLOG_SYSTEM_PROMPT = """You are a business growth expert writing for JWAT Enterprises Inc — an affiliate service partner platform based in Riverview, FL that helps small businesses choose practical tools for funding, credit, lead capture, CRM automation, and tax intake.

Write SEO-optimized, value-first blog content that positions JWAT as the authority on small business growth. Tone: direct, professional, practical. No fluff. Every post must deliver real, actionable value.

Business details:
- Company: JWAT Enterprises Inc
- Owner: Wayne (CEO), Tiesha M Walters (President)
- Website: https://www.jwatenterprisesinc.com
- Email: biz@jwatenterprisesinc.com
- Phone: 813-321-5686
- Target: Startups and small/medium businesses
- Revenue model: JWAT Enterprise Inc's main income is affiliate service partnerships.
- Content priority: Every scheduled post must reinforce one service partner, educate the reader around a buying problem, and drive qualified clicks to that partner's link.
- Partner posts should read like useful business guidance, not thin ads. Mention the assigned partner naturally and include the assigned partner link in the body at least twice.
- Do not invite readers to book calls, strategy sessions, audits, consultations, or meetings with Wayne/JWAT. The CTA must send readers to the assigned service partner.
- Do not repeat the same topic angle week after week. Rotate partner/service categories so Nav, ROK Financial, Upfirst, Tax Services, and GoHighLevel each receive ongoing lead-generation content.

Design system (match exactly):
- Navy: #1a365d
- Navy light: #2d5a8c
- Gold: #ffd700
- Font: Segoe UI, Tahoma, Geneva, Verdana, sans-serif"""

HTML_TEMPLATE = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>TITLE_PLACEHOLDER &mdash; JWAT Enterprises Inc</title>
    <meta name="description" content="META_DESC_PLACEHOLDER">
    <meta name="keywords" content="META_KW_PLACEHOLDER">
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        :root { --navy: #1a365d; --navy-light: #2d5a8c; --gold: #ffd700; --dark: #0d1b2a; --gray-bg: #f8f9fa; --text: #333; --text-muted: #666; }
        body { font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; line-height: 1.7; color: var(--text); }
        header { background: linear-gradient(135deg, var(--navy) 0%, var(--navy-light) 100%); color: white; padding: 15px 0; position: sticky; top: 0; z-index: 1000; box-shadow: 0 2px 10px rgba(0,0,0,0.2); }
        .header-container { max-width: 1200px; margin: 0 auto; padding: 0 20px; display: flex; justify-content: space-between; align-items: center; }
        .logo { font-size: 22px; font-weight: 800; letter-spacing: 1px; color: var(--gold); }
        .logo span { display: block; font-size: 11px; color: rgba(255,255,255,0.8); font-weight: 400; letter-spacing: 2px; text-transform: uppercase; }
        nav a { color: white; text-decoration: none; margin-left: 25px; font-size: 14px; font-weight: 500; transition: color 0.2s; }
        nav a:hover { color: var(--gold); }
        .nav-cta { background: var(--gold); color: var(--navy) !important; padding: 8px 18px; border-radius: 4px; font-weight: 700 !important; }
        .post-hero { background: linear-gradient(135deg, var(--navy) 0%, var(--navy-light) 100%); color: white; padding: 70px 20px; text-align: center; }
        .post-tag { background: var(--gold); color: var(--navy); font-size: 12px; font-weight: 700; text-transform: uppercase; letter-spacing: 1px; padding: 5px 12px; border-radius: 3px; display: inline-block; margin-bottom: 18px; }
        .post-hero h1 { font-size: 38px; font-weight: 800; max-width: 820px; margin: 0 auto 16px; line-height: 1.3; }
        .post-meta { font-size: 14px; color: rgba(255,255,255,0.75); }
        .post-body { max-width: 760px; margin: 60px auto; padding: 0 20px; }
        .post-body p { font-size: 17px; margin-bottom: 22px; color: var(--text); }
        .post-body h2 { font-size: 26px; color: var(--navy); margin: 44px 0 14px; font-weight: 700; }
        .post-body h3 { font-size: 20px; color: var(--navy-light); margin: 30px 0 10px; font-weight: 700; }
        .post-body strong { color: var(--navy); }
        .post-body ul { margin: 0 0 22px 24px; }
        .post-body ul li { font-size: 17px; margin-bottom: 10px; }
        .post-body ol { margin: 0 0 22px 24px; }
        .post-body ol li { font-size: 17px; margin-bottom: 10px; }
        .highlight-box { border-left: 5px solid var(--gold); background: #fffbea; padding: 18px 22px; border-radius: 0 8px 8px 0; margin: 28px 0; font-size: 17px; color: var(--navy); }
        .gray-box { background: var(--gray-bg); border-radius: 8px; padding: 24px; margin: 28px 0; }
        .cta-box { background: linear-gradient(135deg, var(--navy) 0%, var(--navy-light) 100%); color: white; border-radius: 10px; padding: 40px; text-align: center; margin: 50px 0; }
        .cta-box h3 { font-size: 24px; margin-bottom: 12px; }
        .cta-box p { font-size: 16px; color: rgba(255,255,255,0.85); margin-bottom: 24px; }
        .cta-btn { background: var(--gold); color: var(--navy); font-weight: 700; padding: 14px 32px; border-radius: 5px; text-decoration: none; font-size: 16px; display: inline-block; }
        .cta-btn:hover { background: #ffed4e; }
        .back-link { display: inline-block; margin-bottom: 30px; color: var(--navy); font-weight: 600; text-decoration: none; border-bottom: 2px solid var(--gold); padding-bottom: 2px; }
        footer { background: var(--dark); color: rgba(255,255,255,0.7); text-align: center; padding: 30px 20px; font-size: 14px; margin-top: 60px; }
        footer a { color: var(--gold); text-decoration: none; }
        @media(max-width:768px) { .post-hero h1 { font-size: 26px; } nav { display: none; } }
    </style>
</head>
<body>
<header>
    <div class="header-container">
        <div class="logo">JWAT ENTERPRISES INC<span>AI-Powered Business Consulting</span></div>
        <nav>
            <a href="../index.html#services">Services</a>
            <a href="../index.html#why-us">Why Us</a>
            <a href="../index.html#partners">Partners</a>
            <a href="../index.html#tax">Tax Services</a>
            <a href="index.html">Blog</a>
            <a href="../index.html#partners" class="nav-cta">Choose a Partner</a>
        </nav>
    </div>
</header>
<section class="post-hero">
    <span class="post-tag">CATEGORY_PLACEHOLDER</span>
    <h1>TITLE_PLACEHOLDER</h1>
    <div class="post-meta">DATE_PLACEHOLDER &nbsp;&middot;&nbsp; JWAT Enterprises Inc</div>
</section>
<article class="post-body">
    <a href="index.html" class="back-link">&larr; Back to Blog</a>
    BODY_PLACEHOLDER
    <div class="cta-box">
        <h3>CTA_HEADLINE_PLACEHOLDER</h3>
        <p>CTA_BODY_PLACEHOLDER</p>
        <a href="CTA_URL_PLACEHOLDER" target="_blank" rel="sponsored noopener" class="cta-btn">CTA_LABEL_PLACEHOLDER &rarr;</a>
    </div>
    <a href="index.html" class="back-link">&larr; Back to Blog</a>
</article>
<footer>
    <p>&copy; YEAR_PLACEHOLDER JWAT Enterprises Inc &nbsp;&middot;&nbsp; <a href="https://www.jwatenterprisesinc.com">jwatenterprisesinc.com</a> &nbsp;&middot;&nbsp; <a href="mailto:biz@jwatenterprisesinc.com">biz@jwatenterprisesinc.com</a> &nbsp;&middot;&nbsp; <a href="https://www.facebook.com/profile.php?id=61567645495673" target="_blank" rel="noopener">Facebook</a> &nbsp;&middot;&nbsp; <a href="https://www.instagram.com/jwatenterprise/" target="_blank" rel="noopener">Instagram</a> &nbsp;&middot;&nbsp; <a href="https://www.linkedin.com/in/tiesha-m-walters-057994402/" target="_blank" rel="noopener">LinkedIn</a></p>
</footer>
</body>
</html>"""

PUBLISH_TOOL = {
    "name": "publish_blog_post",
    "description": "Publish a complete structured blog post for JWAT Enterprises Inc",
    "input_schema": {
        "type": "object",
        "properties": {
            "title":            {"type": "string", "description": "Full post title"},
            "slug":             {"type": "string", "description": "URL-friendly filename slug, max 60 chars, no extension, lowercase hyphens only"},
            "category":         {"type": "string", "description": "Short category label: Sales Strategy, Marketing, Business Funding, Lead Generation, or Financial Management"},
            "meta_description": {"type": "string", "description": "SEO meta description, max 155 characters"},
            "meta_keywords":    {"type": "string", "description": "Comma-separated SEO keywords"},
            "excerpt":          {"type": "string", "description": "2-sentence summary for the blog listing page"},
            "body_html":        {"type": "string", "description": "Full article body as HTML. Use p, h2, h3, ul, ol, li, strong tags. Add class=highlight-box to div for key callouts, class=gray-box to div for structured lists. Minimum 600 words. Do NOT include the title, hero section, CTA box, header, or footer."},
            "cta_headline":     {"type": "string", "description": "Compelling CTA headline for the end of the post"},
            "cta_body":         {"type": "string", "description": "1-2 sentence CTA supporting copy"}
        },
        "required": ["title", "slug", "category", "meta_description", "meta_keywords", "excerpt", "body_html", "cta_headline", "cta_body"]
    }
}


def load_existing_slugs(blog_dir):
    return {
        os.path.splitext(name)[0]
        for name in os.listdir(blog_dir)
        if name.endswith(".html") and name != "index.html"
    }


def pick_campaign(existing_slugs, pub_date):
    week_index = int(pub_date.strftime("%U"))
    campaigns = PARTNER_CAMPAIGNS[week_index % len(PARTNER_CAMPAIGNS):] + PARTNER_CAMPAIGNS[:week_index % len(PARTNER_CAMPAIGNS)]

    for campaign in campaigns:
        if campaign["slug"] not in existing_slugs:
            return campaign

    fallback = PARTNER_CAMPAIGNS[week_index % len(PARTNER_CAMPAIGNS)].copy()
    fallback["topic"] = f"{fallback['topic']} ({pub_date.strftime('%B %Y')} Update)"
    fallback["slug"] = f"{fallback['slug']}-{pub_date.strftime('%Y-%m-%d')}"
    return fallback


def slugify(title):
    return re.sub(r'[^a-z0-9]+', '-', title.lower()).strip('-')[:60]


def render_html(data, pub_date, campaign):
    html = HTML_TEMPLATE
    html = html.replace("TITLE_PLACEHOLDER", data["title"])
    html = html.replace("META_DESC_PLACEHOLDER", data["meta_description"])
    html = html.replace("META_KW_PLACEHOLDER", data["meta_keywords"])
    html = html.replace("CATEGORY_PLACEHOLDER", data["category"])
    html = html.replace("DATE_PLACEHOLDER", pub_date.strftime("%B %d, %Y"))
    html = html.replace("BODY_PLACEHOLDER", data["body_html"])
    html = html.replace("CTA_HEADLINE_PLACEHOLDER", data["cta_headline"])
    html = html.replace("CTA_BODY_PLACEHOLDER", data["cta_body"])
    html = html.replace("CTA_URL_PLACEHOLDER", campaign["url"])
    html = html.replace("CTA_LABEL_PLACEHOLDER", campaign["cta_label"])
    html = html.replace("YEAR_PLACEHOLDER", str(pub_date.year))
    return html


def generate_post(campaign, pub_date):
    client = anthropic.Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"])

    message = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=4000,
        system=BLOG_SYSTEM_PROMPT,
        tools=[PUBLISH_TOOL],
        tool_choice={"type": "any"},
        messages=[{
            "role": "user",
            "content": (
                f'Write a complete blog post for JWAT Enterprises Inc on this topic: "{campaign["topic"]}".\n'
                f'Assigned service partner: {campaign["partner"]}\n'
                f'Partner link to include naturally in the body: {campaign["url"]}\n'
                f'Category: {campaign["category"]}\n'
                f'End CTA headline: {campaign["cta_headline"]}\n'
                f'End CTA body: {campaign["cta_body"]}\n'
                "The post must be written to generate qualified clicks to the service partner while still giving practical advice."
            )
        }]
    )

    tool_block = next(b for b in message.content if b.type == "tool_use")
    data = tool_block.input

    return {
        "slug":     campaign["slug"],
        "title":    data["title"],
        "category": campaign["category"],
        "excerpt":  data["excerpt"],
        "html":     render_html(data, pub_date, campaign),
        "date":     pub_date.strftime("%B %d, %Y"),
    }


def update_blog_index(index_path, post):
    with open(index_path, "r", encoding="utf-8") as f:
        content = f.read()

    new_card = f"""
    <div class="blog-card">
        <span class="card-tag">{post['category']}</span>
        <div class="card-body">
            <div class="card-meta">{post['date']} &nbsp;&middot;&nbsp; JWAT Enterprises Inc</div>
            <h2>{post['title']}</h2>
            <p>{post['excerpt']}</p>
            <a href="{post['slug']}.html">Read Article &rarr;</a>
        </div>
    </div>
"""

    content = content.replace('<div class="blog-grid">', '<div class="blog-grid">' + new_card, 1)

    with open(index_path, "w", encoding="utf-8") as f:
        f.write(content)


if __name__ == "__main__":
    blog_dir = os.path.join(os.path.dirname(__file__), "..", "blog")
    index_path = os.path.join(blog_dir, "index.html")
    pub_date = datetime.now()

    existing_slugs = load_existing_slugs(blog_dir)
    campaign = pick_campaign(existing_slugs, pub_date)
    print(f"Generating partner post: {campaign['partner']} — {campaign['topic']}")

    post = generate_post(campaign, pub_date)
    print(f"Slug: {post['slug']}")

    post_path = os.path.join(blog_dir, f"{post['slug']}.html")
    with open(post_path, "w", encoding="utf-8") as f:
        f.write(post["html"])
    print(f"Written: {post_path}")

    update_blog_index(index_path, post)
    print("Blog index updated.")
