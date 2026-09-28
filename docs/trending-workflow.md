# QA Affiliate — Trending & Viral Discovery Workflow (Operator Runbook)

This is the repeatable process for keeping QA Affiliate's trending collections
fresh, honest and commercially useful. It implements PDF §6 (Trending and Viral
Product Discovery System).

## 1. Inputs (per refresh cycle)

Gather from permitted sources only — never scrape against a merchant's terms.

| Signal | Source | What to capture |
|---|---|---|
| Bestseller / popularity flags | Amazon / AliExpress / Temu category pages | product URL, rank movement |
| Rating & review momentum | Merchant product pages / feeds | rating, review_count, delta vs last cycle |
| Price & discount movement | Merchant pages / feeds | price, original_price, discount % |
| Availability / eligibility | Merchant pages / affiliate dashboards | in-stock?, affiliate link works? |
| Social attention | TikTok / Instagram / YouTube search, trend roundups | post volume, engagement on product themes |
| Search interest | Google Trends (category-level) | rising queries in women's fashion/beauty |
| Seasonality | Editorial calendar | upcoming events (festivals, wedding season, winter…) |

## 2. Candidate scoring (momentum, not size)

A product is a **candidate** when it beats its category baseline on ≥2 signals:

- `trending`: clear rising momentum (e.g. review velocity up, new discount, fresh social attention).
- `viral`: exceptional spike across signals — social buzz AND merchant momentum together.

Score in a working sheet; keep the sheet — it is the audit trail that a tag
was earned, not invented.

## 3. Editorial review (mandatory — no auto-tagging)

For each candidate verify:
- [ ] Product is in stock and the affiliate link resolves to the correct item
- [ ] Price/discount matches the merchant page right now
- [ ] Rating/review count copied exactly (never rounded up, never invented)
- [ ] Product image is the merchant's original asset (never AI-generated substitutes)
- [ ] Fits QA Affiliate's audience and category taxonomy

Reject anything that fails. Note rejections in the sheet.

## 4. Publishing

Edit `data/products.json`:
- Set `trend_status` to `"trending"` or `"viral"` (or `null` to demote)
- Update `updated` to today's date
- Add/remove `badges` (`best-seller`, `top-rated`, `best-deal`, `new`) on evidence

No code changes needed — homepage modules, `/trending.html` and category
pages render from the data layer automatically. Commit + push; Vercel redeploys.

## 5. Refresh cadence

- **Trending collections:** review weekly
- **Viral tags:** review as signals move (daily during spikes)
- **Demotion:** remove tags when momentum fades, stock runs out, or the
  affiliate link breaks. Manual override anytime.

## 6. Hard rules (from the master brief)

- NEVER fabricate a trend, popularity claim or viral status.
- NEVER tag because a merchant paid — paid placement is not a signal.
- NEVER present sample/demo data as real trend evidence.
- Keep product data separate from presentation; keep affiliate URLs central.
- Use real merchant imagery only.

## 7. Using findings beyond the site

Approved trends feed: homepage modules, category highlights, buying guides,
newsletter themes ("This week's viral finds"), and social content pillars.
Each reuse links back to the site collection page.
