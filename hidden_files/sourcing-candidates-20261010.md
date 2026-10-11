# QA Affiliate sourcing candidates — 14 trend-grounded picks (prepared 2026-10-10)

Trend sources: LTK October 2026 Most Loved list (businesswire.com, ~Oct 1 2026) and TikTok 2026 trend research (accio.com).
Purpose: starting set for the 10,000-product push (catalog at 6,824 live; 3,176 to go).
Status: NONE portal-verified yet — links, eligibility, price, image quality unknown until live portal check.

## Fashion (fall outerwear trend)
1. Women's funnel-neck / turtleneck zip jacket — "funnel-neck jacket" searches up 814% MoM
2. Faux leather / faux suede bomber jacket (women's) — fall's refined moto replacement
3. Oversized blazer, plaid/check (women's) — #FashionTok staple
4. Satin midi skirt or satin pants — satin clicks up 1,164%, "satin pants" searches up 168%
5. Barrel-fit high-waist jeans — searches up 500%

## Jewelry / accessories
6. Beaded statement ring necklace (BaubleBar Janette style) — creator-post velocity very high
7. Cowboy hat (felt, women's) — sales up 49%, Halloween-adjacent
8. Satchel / structured handbag, quilted or croc — sales up 831%

## Beauty
9. Cream-to-powder blush balm / cream blush stick — clicked once every 35 seconds
10. Travel makeup organizer / vanity bag — organization trend, hybrid-work routines

## Home / kitchen / lifestyle
11. Electric pepper grinder set — trending kitchen gadget
12. Wine rack (countertop, metal/wood) — interest up 104%
13. LED flameless candle set — fall home decor; pairs with EventBuzz Thanksgiving decor angle
14. Adult coloring book set — mindfulness trend, searches back to pandemic levels

## Standing rules at delivery
- Verify every link LIVE through the portal before staging (Temu Storefront Convert Link with _x_cid=6013029639 + kol_affiliate suffix; AliExpress Link Generator with Tracking ID "default"). Never construct links.
- Temu Convert Link can reject ineligible items — convert more candidates than needed; can stall mid-batch — spread across days.
- AliExpress Link Generator hit geo-blocking on 2026-10-05 — if blocked again, drop the batch and report, do NOT retry blocked paths.
- Dedupe: goods_id + affiliate_url + 3-word name overlap against full products.json; reject non-English/malformed; main-category women's products only.
- After staging: re-run tools/gen_lite.py && tools/gen_pages.py && tools/gen_seo.py, commit + push (Vercel auto-deploys).
- ONE immediate public pin per product to the correct board (Temu board / AliExpress Women's Finds — Fashion & Beauty), most attractive image, within daily limits.
