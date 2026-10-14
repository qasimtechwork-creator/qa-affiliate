# Social Media Dead-Link Audit — QA Affiliate (2026-10-14)

Catalog at audit time: 6,210 products. Compared every recorded social post against live product IDs.

## 1. PINTEREST (officialqasimmedia)

### A. Pins pointing to DELETED products — DELETE (127 unique pin URLs)
- 67 website-pins from 2-pin ledger (products removed: 67 Daraz-era + broken-image Temu)
- 60 one-pin entries (Daraz "daraz-real-*" fitness/beauty batch + Daraz round pins)
- Zero overlap with the 126-pin deletion list already handled → these are ADDITIONAL
- Full list: `/tmp/pinterest-all-dead.json` (also `/tmp/pinterest-extra-dead.json` = same 127)

Sample:
- https://www.pinterest.com/pin/608830443423121386/ (daraz-shopmore-pressure-washer-gun-48v)
- https://www.pinterest.com/pin/608830443423106833/ (daraz-real-2-in-1-eyebrow-trimmer-for-women-facial-)
- https://www.pinterest.com/pin/608830443423119247/ (daraz-real-wkshop-26cm-ring-light-with-7ft-aluminiu)

### B. Affiliate pins with DIRECT merchant destinations — REVIEW (99 pin URLs)
Live products, but pins point directly to temu.to / s.click.aliexpress.com instead of /item/ pages.
Created under the old 2-pin system (2026-10-02), superseded by the 2026-10-03 one-pin rule.
Full list: `/tmp/pinterest-affiliate-pins.json`

### C. Stale item pages still on disk — DELETE FILES + PUSH (23 files)
gen_seo.py does not remove item pages of deleted products. These exist in the repo:
`/tmp/stale-item-pages.json` — e.g. item/temu-hunt-coat-temu-temu.html, item/temu-pearl-necklace-jewelry-set.html …
Action: `rm item/<id>.html` for each, commit, push.

## 2. TUMBLR (qaaaffiliate) — CLEAN
- RSS (latest 20 posts): 0 dead product refs, 0 direct merchant links
- Registry-recorded posts (Oct 2–3): all products live
- Ledger: 2 posts, both live

## 3. BLUESKY (@qasimkayani.bsky.social) — CLEAN
- 30 posts verified via public API: all 30 link to qa-affiliate.vercel.app/item/<id>, all IDs live
- 0 direct merchant links

## 4. FLIPBOARD (@qaaaffiliate) — NEEDS BROWSER ENUMERATION
- Magazine https://flipboard.com/@qaaaffiliate/qa-affiliate-trending-finds-haj52suqy has ~60 stories
- Confirmed dead stories visible: Daraz-priced items ("SR Traders Teddy Bear 8 inch Premium Plush" Rs.1,050,
  "Soft Cuddly Teddy Bear 1ft Premium Plush Gift" Rs.933, "11 Piece Gym Power Resistance Band Set" Rs.799)
  → these products were deleted (all Daraz removed)
- flipboard-flip-ledger.json has no per-story records (only next_index: 0)
- Story URLs are JS-paginated; text fetch shows only 6. Parent must enumerate via live browser:
  open magazine → scroll through all stories → remove any whose destination /item/<id> is not in catalog.

## 5. BLOGGER (qaaffiliate.blogspot.com) — 2 FIXES NEEDED
- 2 articles reference dead Daraz products:
  - https://qaaffiliate.blogspot.com/2026/10/2-salicylic-acid-acne-serum.html → daraz-2-salicylic-acid-acne-fighting-serum-15ml-anti-acne-serum-ac
  - https://qaaffiliate.blogspot.com/2026/10/18-colors-eyeshadow-palette-shimmer.html → daraz-18-colors-eyeshadow-palette-shimmer-matte-pressed-pigments-l
  Action: edit articles to remove/replace those product sections (or delete articles if single-product).
- 3 articles contain 25 DIRECT merchant links (temu.to/k/p… + 1 s.click.aliexpress.com):
  - https://qaaffiliate.blogspot.com/2026/10/10-trending-finds-worth-adding-to-your.html (10 links)
  - https://qaaffiliate.blogspot.com/2026/10/10-more-trending-finds-worth-adding-to.html (10 links)
  - https://qaaffiliate.blogspot.com/2026/10/5-trending-finds-worth-adding-to-your.html (5 links)
  Action: replace each direct link with the corresponding https://qa-affiliate.vercel.app/item/<id> page.
  Full link list: `/tmp/blogger-audit.json`

## Files
- /tmp/pinterest-all-dead.json — 127 dead Pinterest pin URLs (DELETE)
- /tmp/pinterest-affiliate-pins.json — 99 affiliate pins w/ direct merchant destinations (REVIEW)
- /tmp/stale-item-pages.json — 23 stale item/*.html files (DELETE + PUSH)
- /tmp/blogger-audit.json — Blogger dead refs + 25 direct merchant links
- /tmp/bsky-audit.json — 30 Bluesky posts, all clean (evidence)
- /tmp/tumblr-rss-audit.json — Tumblr RSS check, clean (evidence)
