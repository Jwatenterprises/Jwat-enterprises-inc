import anthropic
import os
import re
import json
from datetime import datetime

EXISTING_TOPICS = [
    "why-small-business-not-generating-leads",
    "5-step-sales-funnel",
    "cold-leads-to-paying-clients",
    "rok-financial-business-loan-funding",
]

TOPIC_POOL = [
    "How to Build a Personal Brand That Attracts Clients on Autopilot",
    "The Small Business Owner's Guide to Email Marketing in 2026",
    "Why Most Small Business Websites Don't Convert (And How to Fix Yours)",
    "How to Price Your Services Without Leaving Money on the Table",
    "The 7 Financial Metrics Every Small Business Owner Must Track",
    "How to Get Your First 10 Clients Without Paid Advertising",
    "What Is a Sales CRM and Does Your Small Business Need One?",
    "How to Use LinkedIn to Generate B2B Leads for Free",
    "The Small Business Owner's Guide to Building Business Credit",
    "How to Create a 90-Day Revenue Plan for Your Business",
    "Why Your Follow-Up Strategy Is Costing You Clients",
    "How to Write a Business Proposal That Closes Deals",
    "The Truth About SBA Loans: What Banks Won't Tell You",
    "How to Automate Your Client Onboarding Process",
    "5 Signs Your Business Needs a Sales Consultant Right Now",
    "How to Turn Happy Clients Into a Referral Machine",
    "What Every Small Business Owner Needs to Know About Cash Flow",
    "How to Build a Marketing Strategy on a $500 Budget",
    "The Biggest Mistakes Small Business Owners Make With Facebook Ads",
    "How to Scale from $5K to $10K Monthly Revenue",
    "Understanding Business Line of Credit vs. Term Loan: Which Is Right for You?",
    "How to Hire Your First Employee Without Breaking the Bank",
    "The Power of Niche Marketing: Why Trying to Reach Everyone Loses Everyone",
    "How to Set Up Google Analytics for Your Small Business Website",
    "Invoice Factoring Explained: Turn Unpaid Invoices Into Immediate Cash",
]

BLOG_SYSTEM_PROMPT = """You are a business growth expert writing for JWAT Enterprises Inc — an AI-powered business consulting firm based in Riverview, FL that helps small businesses and startups with sales, marketing, financial management, and sales funnel consulting.

Write SEO-optimized, value-first blog content that positions JWAT as the authority on small business growth. Tone: direct, professional, practical. No fluff. Every post must deliver real, actionable value.

Business details:
- Company: JWAT Enterprises Inc
- Owner: Wayne (CEO), Tiesha M Walters (President)
- Website: https://www.jwatenterprisesinc.com
- Booking: https://calendly.com/biz-jwatenterprisesinc
- Email: biz@jwatenterprisesinc.com
- Phone: 813-321-5686
- Target: Startups and small/medium businesses

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
    <title>{title} — JWAT Enterprises Inc</title>
    <meta name="description" content="{meta_description}">
    <meta name="keywords" content="{meta_keywords}">
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        :root {{ --navy: #1a365d; --navy-light: #2d5a8c; --gold: #ffd700; --dark: #0d1b2a; --gray-bg: #f8f9fa; --text: #333; --text-muted: #666; }}
        body {{ font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; line-height: 1.7; color: var(--text); }}
        header {{ background: linear-gradient(135deg, var(--navy) 0%, var(--navy-light) 100%); color: white; padding: 15px 0; position: sticky; top: 0; z-index: 1000; box-shadow: 0 2px 10px rgba(0,0,0,0.2); }}
        .header-container {{ max-width: 1200px; margin: 0 auto; padding: 0 20px; display: flex; justify-content: space-between; align-items: center; }}
        .logo {{ font-size: 22px; font-weight: 800; letter-spacing: 1px; color: var(--gold); }}
        .logo span {{ display: block; font-size: 11px; color: rgba(255,255,255,0.8); font-weight: 400; letter-spacing: 2px; text-transform: uppercase; }}
        nav a {{ color: white; text-decoration: none; margin-left: 25px; font-size: 14px; font-weight: 500; transition: color 0.2s; }}
        nav a:hover {{ color: var(--gold); }}
        .nav-cta {{ background: var(--gold); color: var(--navy) !important; padding: 8px 18px; border-radius: 4px; font-weight: 700 !important; }}
        .post-hero {{ background: linear-gradient(135deg, var(--navy) 0%, var(--navy-light) 100%); color: white; padding: 70px 20px; text-align: center; }}
        .post-tag {{ background: var(--gold); color: var(--navy); font-size: 12px; font-weight: 700; text-transform: uppercase; letter-spacing: 1px; padding: 5px 12px; border-radius: 3px; display: inline-block; margin-bottom: 18px; }}
        .post-hero h1 {{ font-size: 38px; font-weight: 800; max-width: 820px; margin: 0 auto 16px; line-height: 1.3; }}
        .post-meta {{ font-size: 14px; color: rgba(255,255,255,0.75); }}
        .post-body {{ max-width: 760px; margin: 60px auto; padding: 0 20px; }}
        .post-body p {{ font-size: 17px; margin-bottom: 22px; color: var(--text); }}
        .post-body h2 {{ font-size: 26px; color: var(--navy); margin: 44px 0 14px; font-weight: 700; }}
        .post-body h3 {{ font-size: 20px; color: var(--navy-light); margin: 30px 0 10px; font-weight: 700; }}
        .post-body strong {{ color: var(--navy); }}
        .post-body ul {{ margin: 0 0 22px 24px; }}
        .post-body ul li {{ font-size: 17px; margin-bottom: 10px; }}
        .post-body ol {{ margin: 0 0 22px 24px; }}
        .post-body ol li {{ font-size: 17px; margin-bottom: 10px; }}
        .highlight-box {{ border-left: 5px solid var(--gold); background: #fffbea; padding: 18px 22px; border-radius: 0 8px 8px 0; margin: 28px 0; font-size: 17px; color: var(--navy); }}
        .gray-box {{ background: var(--gray-bg); border-radius: 8px; padding: 24px; margin: 28px 0; }}
        .cta-box {{ background: linear-gradient(135deg, var(--navy) 0%, var(--navy-light) 100%); color: white; border-radius: 10px; padding: 40px; text-align: center; margin: 50px 0; }}
        .cta-box h3 {{ font-size: 24px; margin-bottom: 12px; }}
        .cta-box p {{ font-size: 16px; color: rgba(255,255,255,0.85); margin-bottom: 24px; }}
        .cta-btn {{ background: var(--gold); color: var(--navy); font-weight: 700; padding: 14px 32px; border-radius: 5px; text-decoration: none; font-size: 16px; display: inline-block; }}
        .cta-btn:hover {{ background: #ffed4e; }}
        .back-link {{ display: inline-block; margin-bottom: 30px; color: var(--navy); font-weight: 600; text-decoration: none; border-bottom: 2px solid var(--gold); padding-bottom: 2px; }}
        footer {{ background: var(--dark); color: rgba(255,255,255,0.7); text-align: center; padding: 30px 20px; font-size: 14px; margin-top: 60px; }}
        footer a {{ color: var(--gold); text-decoration: none; }}
        @media(max-width:768px) {{ .post-hero h1 {{ font-size: 26px; }} nav {{ display: none; }} }}
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
            <a href="../index.html#contact" class="nav-cta">Get Started</a>
        </nav>
    </div>
</header>
<section class="post-hero">
    <span class="post-tag">{category}</span>
    <h1>{title}</h1>
    <div class="post-meta">{date} &nbsp;·&nbsp; JWAT Enterprises Inc</div>
</section>
<article class="post-body">
    <a href="index.html" class="back-link">← Back to Blog</a>
    {body}
    <div class="cta-box">
        <h3>{cta_headline}</h3>
        <p>{cta_body}</p>
        <a href="https://calendly.com/biz-jwatenterprisesinc" class="cta-btn">Book Your Free Audit →</a>
    </div>
    <a href="index.html" class="back-link">← Back to Blog</a>
</article>
<footer>
    <p>&copy; {year} JWAT Enterprises Inc &nbsp;·&nbsp; <a href="https://www.jwatenterprisesinc.com">jwatenterprisesinc.com</a> &nbsp;·&nbsp; <a href="mailto:biz@jwatenterprisesinc.com">biz@jwatenterprisesinc.com</a></p>
</footer>
</body>
</html>"""


def pick_topic(existing):
    for topic in TOPIC_POOL:
        slug = re.sub(r'[^a-z0-9]+', '-', topic.lower()).strip('-')
        if not any(slug[:20] in e for e in existing):
            return topic
    return f"Small Business Growth Strategy: Key Insights for {datetime.now().strftime('%B %Y')}"


def slugify(title):
    return re.sub(r'[^a-z0-9]+', '-', title.lower()).strip('-')[:60]


def generate_post(topic, pub_date):
    client = anthropic.Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"])

    prompt = f"""Write a complete blog post for JWAT Enterprises Inc on this topic: "{topic}"

Return a JSON object with these exact keys:
- title: the full post title (string)
- slug: URL-friendly filename slug, no extension (string, max 60 chars)
- category: short category label like "Sales Strategy", "Business Funding", "Marketing", "Lead Generation" (string)
- meta_description: 150-char SEO meta description (string)
- meta_keywords: comma-separated SEO keywords (string)
- excerpt: 2-sentence summary for the blog listing page (string)
- body_html: the full article body as HTML (string) — use <p>, <h2>, <h3>, <ul>, <ol>, <li>, <strong> tags only. Use class="highlight-box" on a <div> for key callouts. Use class="gray-box" on a <div> for lists or structured info. Do NOT include the title, hero, CTA box, or nav — just the article body content. Minimum 600 words.
- cta_headline: compelling CTA headline (string)
- cta_body: 1-2 sentence CTA supporting copy (string)

Return only valid JSON. No markdown fences."""

    message = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=4000,
        system=BLOG_SYSTEM_PROMPT,
        messages=[{"role": "user", "content": prompt}]
    )

    raw = message.content[0].text.strip()
    raw = re.sub(r'^```json\s*', '', raw)
    raw = re.sub(r'^```\s*', '', raw)
    raw = re.sub(r'```$', '', raw).strip()
    data = json.loads(raw)

    html = HTML_TEMPLATE.format(
        title=data["title"],
        meta_description=data["meta_description"],
        meta_keywords=data["meta_keywords"],
        category=data["category"],
        date=pub_date.strftime("%B %d, %Y"),
        body=data["body_html"],
        cta_headline=data["cta_headline"],
        cta_body=data["cta_body"],
        year=pub_date.year,
    )

    return {
        "slug": data.get("slug") or slugify(data["title"]),
        "title": data["title"],
        "category": data["category"],
        "excerpt": data["excerpt"],
        "html": html,
        "date": pub_date.strftime("%B %d, %Y"),
    }


def update_blog_index(index_path, post):
    with open(index_path, "r", encoding="utf-8") as f:
        content = f.read()

    new_card = f"""
    <div class="blog-card">
        <span class="card-tag">{post['category']}</span>
        <div class="card-body">
            <div class="card-meta">{post['date']} &nbsp;·&nbsp; JWAT Enterprises Inc</div>
            <h2>{post['title']}</h2>
            <p>{post['excerpt']}</p>
            <a href="{post['slug']}.html">Read Article →</a>
        </div>
    </div>
"""

    content = content.replace("<div class=\"blog-grid\">", "<div class=\"blog-grid\">" + new_card, 1)

    with open(index_path, "w", encoding="utf-8") as f:
        f.write(content)


if __name__ == "__main__":
    blog_dir = os.path.join(os.path.dirname(__file__), "..", "blog")
    index_path = os.path.join(blog_dir, "index.html")
    pub_date = datetime.now()

    topic = pick_topic(EXISTING_TOPICS)
    print(f"Generating post: {topic}")

    post = generate_post(topic, pub_date)
    print(f"Slug: {post['slug']}")

    post_path = os.path.join(blog_dir, f"{post['slug']}.html")
    with open(post_path, "w", encoding="utf-8") as f:
        f.write(post["html"])
    print(f"Written: {post_path}")

    update_blog_index(index_path, post)
    print("Blog index updated.")
