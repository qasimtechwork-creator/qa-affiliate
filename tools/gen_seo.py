#!/usr/bin/env python3
"""
gen_seo.py — SEO static-page + sitemap + robots generator for QA Affiliate.

WHAT IT DOES
  1. Generates one fully server-rendered HTML page per product at item/<id>.html
     (served as /item/<id> via Vercel cleanUrls). Each page carries a unique
     <title>, meta description, canonical URL, Open Graph tags, Product +
     Breadcrumb JSON-LD, an H1, the full product content and related-product
     internal links — everything Googlebot needs WITHOUT running JavaScript.
  2. Regenerates sitemap.xml using FINAL canonical URLs only (no .html
     redirect chains, no query-string legacy product URLs).
  3. Rewrites robots.txt so Googlebot may fetch /data/products.json and
     /data/categories.json (needed for JS listing pages) while /config/,
     /admin/ and /go/ stay blocked.

RUN THIS after every product-staging batch, then commit + push (Vercel
auto-deploys). New products get their /item/ pages on the next run.
"""
import json, os, re, html, sys
from datetime import date

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DOMAIN = "https://qa-affiliate.vercel.app"
TODAY = date.today().isoformat()

def esc(s):
    return html.escape(str(s or ""), quote=True)

def load(name, default):
    p = os.path.join(ROOT, name)
    try:
        with open(p, encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return default

products = load("data/products.json", {}).get("products", [])
cats_raw = load("data/categories.json", {})
categories = cats_raw.get("categories", []) if isinstance(cats_raw, dict) else cats_raw
cat_name = {c.get("id"): c.get("name", c.get("id")) for c in categories}
site = load("config/site.json", {})
affiliates = load("data/affiliates.json", load("config/affiliates.json", {}))
merchants = affiliates.get("merchants", {})
brand = site.get("brand", {})
BRAND_NAME = brand.get("name", "QA Affiliate")
LOGO = brand.get("logo", "/assets/images/logo.png")
LOGO_ALT = brand.get("logo_alt", "QA Affiliate logo")
TAGLINE = brand.get("tagline", "Discover trending women's products worth your money")

def merchant_name(m):
    return (merchants.get(m) or {}).get("display_name") or (merchants.get(m) or {}).get("name") or m.title()

def disclosure(m):
    return (merchants.get(m) or {}).get("disclosure_short") or "QA Affiliate may earn a commission on qualifying purchases."

def stars(rating):
    try:
        r = float(rating)
    except (TypeError, ValueError):
        return ""
    full = int(round(r))
    return "★" * full + "☆" * (5 - full)

def trunc(s, n):
    s = re.sub(r"\s+", " ", str(s or "")).strip()
    return s if len(s) <= n else s[: n - 1].rstrip() + "…"

HEADER = f"""<header class="site-header"><div class="container header-inner"><a class="brand" href="/"><img src="{esc(LOGO)}" alt="{esc(LOGO_ALT)}"><span class="brand-name">{esc(BRAND_NAME)}<small>{esc(TAGLINE)}</small></span></a><nav class="main-nav"><a href="/">Home</a><a href="/products">Shop All</a><a href="/trending">Trending</a><a href="/deals">Deals</a><a href="/guides">Guides</a><a href="/about">About</a></nav></div></header>"""

def footer_html():
    cats = "".join(
        f'<li><a href="/category?cat={esc(c.get("id"))}">{esc(c.get("name"))}</a></li>'
        for c in categories[:6]
    )
    return (
        '<footer class="site-footer"><div class="container"><div class="footer-grid">'
        f'<div class="footer-brand"><img src="{esc(LOGO)}" alt="{esc(LOGO_ALT)}"><p>{esc(TAGLINE)}. Transparent affiliate discovery for women\'s fashion, beauty and lifestyle.</p></div>'
        f"<div><h4>Shop</h4><ul>{cats}</ul></div>"
        '<div><h4>Company</h4><ul><li><a href="/about">About</a></li><li><a href="/contact">Contact</a></li>'
        '<li><a href="/faq">FAQ</a></li><li><a href="/legal/disclosure">Affiliate Disclosure</a></li>'
        '<li><a href="/legal/privacy">Privacy</a></li></ul></div>'
        "</div></div></footer>"
    )

FOOTER = footer_html()

# index products by category for related links
by_cat = {}
for p in products:
    by_cat.setdefault(p.get("category"), []).append(p)

def related(p, n=4):
    out = [x for x in by_cat.get(p.get("category"), []) if x.get("id") != p.get("id")]
    return out[:n]

def item_page(p):
    pid = p["id"]
    url = f"{DOMAIN}/item/{pid}"
    name = p.get("name", pid)
    title = trunc(name, 65) + f" | {BRAND_NAME}"
    desc = trunc(p.get("short_description") or name, 155)
    img = p.get("image_url", "") or (p.get("images") or [""])[0]
    mname = merchant_name(p.get("merchant"))
    cat = p.get("category")
    catlabel = cat_name.get(cat, cat or "")
    rating = p.get("rating")
    sold = p.get("sold_count")
    badges = "".join(f'<span class="badge">{esc(b)}</span>' for b in (p.get("badges") or []))
    feats = "".join(f"<li>{esc(f)}</li>" for f in (p.get("key_features") or []))
    pros = "".join(f"<li>{esc(x)}</li>" for x in (p.get("pros") or []))
    cons = "".join(f"<li>{esc(x)}</li>" for x in (p.get("cons") or []))
    feats_html = f'<div class="pd-features"><h2>Key features</h2><ul>{feats}</ul></div>' if feats else ""
    if pros or cons:
        pc = '<div class="pros-cons">'
        if pros:
            pc += f'<div class="pros"><h2>Pros</h2><ul>{pros}</ul></div>'
        if cons:
            pc += f'<div class="cons"><h2>Cons</h2><ul>{cons}</ul></div>'
        pc += "</div>"
    else:
        pc = ""
    rel = related(p)
    rel_html = ""
    if rel:
        cards = "".join(
            f'<a class="product-card" href="/item/{esc(r["id"])}"><div class="product-media"><img loading="lazy" src="{esc(r.get("image_url",""))}" alt="{esc(r.get("name",""))}"></div><div class="product-body"><h3 class="product-name">{esc(r.get("name",""))}</h3></div></a>'
            for r in rel
        )
        rel_html = f'<section class="related-section"><h2 class="related-h">You may also like</h2><div class="product-grid">{cards}</div></section>'

    ld_product = {
        "@context": "https://schema.org",
        "@type": "Product",
        "name": name,
        "image": img,
        "description": p.get("short_description") or name,
        "category": catlabel,
        "brand": {"@type": "Brand", "name": mname},
        "url": url,
        "offers": {"@type": "Offer", "url": p.get("affiliate_url", url)},
    }
    if rating:
        try:
            ld_product["aggregateRating"] = {
                "@type": "AggregateRating",
                "ratingValue": str(rating),
                "bestRating": "5",
            }
        except Exception:
            pass
    ld_breadcrumb = {
        "@context": "https://schema.org",
        "@type": "BreadcrumbList",
        "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "Home", "item": DOMAIN + "/"},
            {"@type": "ListItem", "position": 2, "name": catlabel, "item": f"{DOMAIN}/category?cat={esc(cat)}"},
            {"@type": "ListItem", "position": 3, "name": name},
        ],
    }
    meta_row = f'<span>{stars(rating)} {esc(str(rating))}</span>' if rating else ""
    if sold:
        meta_row += f"<span>{esc(sold)} on {esc(mname)}</span>"
    meta_row += f"<span>Sold by {esc(mname)}</span>"

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{esc(title)}</title>
<meta name="description" content="{esc(desc)}">
<link rel="canonical" href="{url}">
<meta name="robots" content="index, follow">
<meta property="og:type" content="product">
<meta property="og:title" content="{esc(title)}">
<meta property="og:description" content="{esc(desc)}">
<meta property="og:image" content="{esc(img)}">
<meta property="og:url" content="{url}">
<meta property="og:site_name" content="{esc(BRAND_NAME)}">
<meta name="twitter:card" content="summary_large_image">
<link rel="icon" type="image/png" href="/assets/images/favicon-64.png">
<link rel="stylesheet" href="/assets/css/main.css">
<script type="application/ld+json">{json.dumps(ld_product, ensure_ascii=False)}</script>
<script type="application/ld+json">{json.dumps(ld_breadcrumb, ensure_ascii=False)}</script>
</head>
<body>
{HEADER}
<main class="container"><div class="breadcrumb"><a href="/">Home</a> / <a href="/category?cat={esc(cat)}">{esc(catlabel)}</a> / {esc(trunc(name, 60))}</div>
<div class="pd-layout"><div><div class="pd-media"><img src="{esc(img)}" alt="{esc(name)}" fetchpriority="high"></div></div>
<div class="pd-info"><div class="badge-row" style="position:static;margin-bottom:10px">{badges}</div>
<h1>{esc(name)}</h1>
<div class="pd-meta">{meta_row}</div>
<p class="pd-desc">{esc(p.get("short_description") or "")}</p>
<div class="pd-cta-row"><a class="btn btn-rose" href="{esc(p.get("affiliate_url") or url)}" target="_blank" rel="nofollow sponsored noopener">View Deal at {esc(mname)}</a></div>
<div class="disclosure-box"><strong>Affiliate disclosure:</strong> {esc(disclosure(p.get("merchant")))}</div>
{feats_html}
{pc}
</div></div>
{rel_html}
</main>
{FOOTER}
</body>
</html>
"""

def main():
    item_dir = os.path.join(ROOT, "item")
    os.makedirs(item_dir, exist_ok=True)
    n = 0
    for p in products:
        if not p.get("id"):
            continue
        with open(os.path.join(item_dir, p["id"] + ".html"), "w", encoding="utf-8") as f:
            f.write(item_page(p))
        n += 1

    # ---- sitemap.xml (canonical URLs only) ----
    urls = []
    def add(loc, changefreq="weekly", priority="0.5"):
        urls.append(f'  <url><loc>{loc}</loc><lastmod>{TODAY}</lastmod><changefreq>{changefreq}</changefreq><priority>{priority}</priority></url>')
    add(DOMAIN + "/", "daily", "1.0")
    for slug, pr in (("products", "0.9"), ("trending", "0.9"), ("deals", "0.8"), ("guides", "0.9")):
        add(f"{DOMAIN}/{slug}", "daily", pr)
    guides_dir = os.path.join(ROOT, "guides")
    if os.path.isdir(guides_dir):
        for fn in sorted(os.listdir(guides_dir)):
            if fn.endswith(".html"):
                add(f"{DOMAIN}/guides/{fn[:-5]}", "monthly", "0.7")
    for p in products:
        if p.get("id"):
            add(f"{DOMAIN}/item/{p['id']}", "weekly", "0.8")
    for c in categories:
        if c.get("id"):
            add(f"{DOMAIN}/category?cat={c['id']}", "weekly", "0.6")
    for slug, pr in (("about", "0.5"), ("contact", "0.5"), ("faq", "0.5")):
        add(f"{DOMAIN}/{slug}", "monthly", pr)
    for slug in ("disclosure", "privacy", "terms", "cookies", "advertising"):
        add(f"{DOMAIN}/legal/{slug}", "yearly", "0.3")
    sitemap = '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + "\n".join(urls) + "\n</urlset>\n"
    with open(os.path.join(ROOT, "sitemap.xml"), "w", encoding="utf-8") as f:
        f.write(sitemap)

    # ---- robots.txt ----
    robots = (
        "User-agent: *\n"
        "Allow: /data/products.json\n"
        "Allow: /data/categories.json\n"
        "Disallow: /config/\n"
        "Disallow: /data/\n"
        "Disallow: /admin/\n"
        "Disallow: /go/\n"
        "\n"
        f"Sitemap: {DOMAIN}/sitemap.xml\n"
    )
    with open(os.path.join(ROOT, "robots.txt"), "w", encoding="utf-8") as f:
        f.write(robots)

    print(f"item pages: {n} | sitemap urls: {len(urls)} | robots.txt updated")

if __name__ == "__main__":
    sys.exit(main())
