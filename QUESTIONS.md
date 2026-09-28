# QA Affiliate — Open Client Inputs

Only genuinely missing items are listed. Everything else is built.

## ✅ Received and integrated (2026-09-28)

- **Official QA logo** — `assets/images/qa-logo.png` (golden QA monogram, 789×591).
  Live in header, footer and favicon. No placeholder logo remains.
- **Founder photo** — `assets/images/founder.png` (Qasim Kayani professional
  portrait, 941×1672). Live on the About page, CSS-fitted to the 800×800
  target frame without distortion.

## ❌ Still needed from the client

1. **Final domain** — not selected yet. Currently `yourdomain.com` placeholder
   in `config/site.json`, `sitemap.xml`, `robots.txt`.
2. **Official social URLs** — Instagram, TikTok, YouTube, Facebook, X.
   Icons stay hidden until URLs are supplied in `config/site.json`.
3. **Professional contact email** — currently `hello@yourdomain.com`
   placeholder. Do not use a personal email as the permanent contact.
4. **Affiliate program links / product feeds / APIs** — Amazon, AliExpress,
   Temu (or permitted access method). Wiring guide in
   `config/affiliates.json`.
5. **Affiliate IDs / tracking parameters** — per merchant, to tag product URLs.
6. **Real product data** — to replace the flagged SAMPLE dataset in
   `data/products.json`: real names, prices, ratings, review counts and
   original merchant images (never AI-generated substitutes).
7. **Google Analytics 4 measurement ID** — optional; add to
   `config/site.json` → `analytics.ga4_measurement_id`.
8. **Newsletter provider** — Beehiiv / Mailchimp / ConvertKit + list/form
   action URL (`config/site.json` → `newsletter`).
9. **Advertising account** (Adsterra or similar) — later stage only, after the
   core experience is stable. Currently disabled.
