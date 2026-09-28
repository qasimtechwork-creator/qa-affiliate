# QA Affiliate — Women's Product Discovery & Affiliate Platform

Premium, scalable, static affiliate website per the master brief
(`~/workspace/user/files/QA_Affiliate_Master_Launch_Document.pdf`).
Women's fashion, shoes, jewelry, bags, beauty, skincare, hair care,
accessories, lingerie, fitness/lifestyle + viral/trending collections.

## What's integrated

- **Official QA logo** (`assets/images/qa-logo.png`, golden QA monogram) —
  used in header, footer and favicon (favicon-64.png, apple-touch-icon.png).
- **Founder photo** (`assets/images/founder.png`, Qasim Kayani portrait) —
  used on the About page, CSS-cropped to a square frame (no distortion).

## Quick start (local preview)

```bash
cd ~/workspace/affiliate-site
python3 -m http.server 8080
# open http://localhost:8080
```

> JSON fetches require http(s) — `file://` will not load the data layer.

## Going live — configuration only, zero code changes

1. **Domain:** replace `yourdomain.com` in `config/site.json` (+ sitemap.xml,
   robots.txt) with the final domain.
2. **Brand/social/contact:** edit `config/site.json` (social URLs unhide icons
   automatically; contact email; GA4 measurement ID for analytics).
3. **Affiliate links:** join Amazon Associates / AliExpress Portals / Temu
   Affiliate. In `data/products.json`, replace each `affiliate_url`
   (`example.com/...` placeholders) with your real tagged product URL, set the
   merchant `enabled: true` in `config/affiliates.json`, and replace all
   `sample: true` entries with verified merchant data (real name, price,
   rating, review count, original merchant image).
4. **Demo mode:** set `demo_mode: false` in `config/site.json` once real
   products are wired — removes the demo notice and sample tags stop
   appearing (they only render for `sample: true` entries).
5. **Newsletter:** set `newsletter.provider` + `action_url` in
   `config/site.json` (Beehiiv / Mailchimp / ConvertKit). Until then, signups
   queue locally and visitors are told the provider is being connected.
6. **Product images:** replace `assets/img/placeholder-*.svg` usage by adding
   real merchant image URLs to each product's `image` field (supported by the
   renderer; falls back to placeholder when absent).

## GitHub → Vercel deploy

```bash
cd ~/workspace/affiliate-site
git init && git add -A && git commit -m "QA Affiliate launch"
gh repo create qa-affiliate --public --source=. --push
# Vercel: import the repo, framework preset "Other", no build command,
# output directory "."  → deploy. Add custom domain later in Vercel dashboard.
```

## Trending workflow

See `docs/trending-workflow.md` (operator runbook) and the public explainer at
`/docs/trending-workflow.html`. Tag products via `trend_status` in
`data/products.json` — pages update automatically.

## Structure

```
config/site.json          brand, domain, socials, contact, GA4, newsletter, demo_mode
config/affiliates.json    merchant configs + wiring instructions (no secrets in frontend)
data/categories.json      11-category taxonomy (add categories here, pages auto-render)
data/products.json        product data layer — SAMPLE dataset, every entry flagged
assets/images/            qa-logo.png, founder.png, favicons (official client assets)
assets/img/               neutral SVG placeholders with exact size labels
assets/css/main.css       design system (mobile-first)
assets/js/app.js          render engine: components, search/filters, tracking, GA4
```

## Strict rules honored

- No fake product images — neutral labeled SVG placeholders only.
- No invented product data presented as real — sample dataset, every entry
  flagged `sample: true`, "Sample listing" tags in UI, demo-mode notice.
- No hardcoded affiliate links — central data layer only.
- No private credentials in frontend — affiliates.json carries wiring docs only.
- All copy in English.
