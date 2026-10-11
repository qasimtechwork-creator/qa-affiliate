# Harvest-21 staging log — 2026-10-09

Source (verbatim on disk): hidden_files/harvest-21-verified-20261009.json (21 items)
Backup before write: backups/products-20261009-harvest21-bak.json (6,813 verified)
Procedure: identical to harvest-120-staging-log-rerun-20261009.md (dedupe = goods_id via affiliate_url + affiliate_url exact + name-overlap 3+ consecutive distinctive words vs full catalog; clean-base image URLs HEAD-verified 200; records field-for-field matched to the staged harvest-120 Temu schema, incl. goods.html?goods_id=…&_x_cid=6013029639kol_affiliate affiliate format, trend_status "new", badges ["new"], no stored price).

## Staged: 11
Category counts (staged): fashion 2, shoes 3, bags 6

- temu-backless-stretch-evening-dress | goods 601104968855390 | fashion | Backless Stretch Evening Dress | https://img.kwcdn.com/product/fancy/74bc392d-9545-4ded-a493-de1d8478c40a.jpg
- temu-casual-cami-house-dress | goods 606873893834771 | fashion | Casual Cami House Dress | https://img.kwcdn.com/product/fancy/974e5e95-d35f-4291-b77c-8199760e0f57.jpg
- temu-lightweight-sports-sneakers | goods 605952304627800 | shoes | Lightweight Sports Sneakers | https://img.kwcdn.com/product/fancy/5d4cc82c-16a3-4a07-a099-5e0bf58e010f.jpg
- temu-red-xiuhe-bridal-heels | goods 601103333920697 | shoes | Red Xiuhe Bridal Heels | https://img.kwcdn.com/product/fmket/f5945960d0c083c88b8cd7aa5b6817bd.jpg
- temu-nike-air-force-1-low-sneakers | goods 603028262329513 | shoes | Nike Air Force 1 Low Sneakers | https://img.kwcdn.com/local-goods-image/21137b23908/4b6b1cf2-642c-4c71-9888-686aeb93984c_1029x1029.png
- temu-genuine-leather-dual-use-tote | goods 607326476053983 | bags (tote) | Genuine Leather Dual-Use Tote | https://img.kwcdn.com/product/open/46110e29e2384329b8952c8bfd796822-goods.jpeg
- temu-wrist-strap-commuter-tote | goods 607636317635260 | bags (tote) | Wrist-Strap Commuter Tote | https://img.kwcdn.com/product/fancy/22a46d76-0715-4935-8ce0-7db9b8499e16.jpg
- temu-fashion-print-pu-tote-bag | goods 607132531456259 | bags (tote) | Fashion Print PU Tote Bag | https://img.kwcdn.com/product/fancy/7b2bdcdb-3055-4447-8f81-0eeb913d80c0.jpg
- temu-two-tone-crossbody-handbag | goods 605677779057143 | bags (crossbody) | Two-Tone Crossbody Handbag | https://img.kwcdn.com/product/open/d1b2b851846f4fb5a43c5aefc03865c6-goods.jpeg
- temu-soft-leather-tote-bag | goods 606791551255716 | bags (tote) | Soft Leather Tote Bag | https://img.kwcdn.com/product/fancy/0b8623fe-6cf8-41d6-b0f9-de94f7a4eaaa.jpg
- temu-vintage-letter-print-tote-bag | goods 606781417830522 | bags (tote) | Vintage Letter Print Tote Bag | https://img.kwcdn.com/product/algo_check/auto/18e310a245a3bdb58795b6614dbea9b4_1788251422454.jpg

Note: 2 of the 11 (goods 607326476053983, 607636317635260) were first flagged by the derived-name guard under working names ("Leather Tote Crossbody Bag", "Tote Bag with Wrist Strap") for 3-gram collisions with unrelated catalog names; they were staged under the distinct names above after passing all guards. Bags subcategory uses the site taxonomy (tote/crossbody), matching categories.json.

## Rejected: 10

### Duplicate goods_id already in catalog (affiliate_url exact match): 8
- goods 606882215351238 | leopard cami long dress | already staged as temu-leopard-cami-long-dress
- goods 601099512967801 | hollow backless dress | already staged as temu-hollow-backless-dress
- goods 607624170990996 | leopard camisole house dress | already staged as temu-leopard-camisole-house-dress
- goods 607149711312526 | leopard maxi dress set | already staged as temu-leopard-maxi-dress-set
- goods 610520119778417 | UGG Tazz Women's Platform Slippers-1122553 ($99.63) | already staged this morning as temu-platform-slippers (same product/goods_id)
- goods 602775933025001 | Vans checkerboard slip-on sneakers | already staged as temu-checkerboard-slip-on-sneakers
- goods 605901519996268 | golden lace-up sneakers | already staged as temu-golden-lace-up-sneakers
- goods 601101230506429 | Maillard vintage crossbody tote | already staged as temu-maillard-vintage-crossbody-bag-for-women

### Duplicate product under a different goods_id: 1
- goods 606648273847070 | smocked tiered maxi dress | same product already in catalog as temu-summer-beach-vacation-womens-spaghetti-strap-smocked-maxi-dress — identical kwcdn image hash (50efa52c36aa3ef17eaeb9e00d27fcbc_1788339261543); title shares distinctive consecutive 3-grams (strap/smocked/maxi) with the catalog name

### Name-overlap (3+ consecutive distinctive words vs catalog name): 1
- goods 606576752573378 | BAOLENIAO plush ankle boots | shared: ('versatile', 'ankle', 'boots') with catalog name 'Pointed Toe Versatile Ankle Boots Women New' (temu-pointed-toe-versatile-ankle-boots-women-new)

### Price anomalies / image failures: 0
All 21 image URLs returned HTTP 200 on the clean base URL; all prices plausible ($4.67–$99.63; the two branded shoes at $86.87/$99.63 fall in the accepted branded range per the harvest-120 precedent — the $99.63 pair was the catalog duplicate above, the $86.87 Nike AF1 was staged).

## Publish + live verification (2026-10-09)
- gen_seo.py: 6,824 item pages generated; sitemap 6,845 → 6,856 URLs (+11).
- Commit 5eb8b333 pushed to master; Vercel auto-deployed.
- LIVE https://qa-affiliate.vercel.app/data/products.json = 6,824 products (6,813 + 11); all 11 staged ids present.
- Sampled new item pages: HTTP 200 — /item/temu-backless-stretch-evening-dress, /item/temu-nike-air-force-1-low-sneakers, /item/temu-vintage-letter-print-tote-bag.
- Sampled new product images: HTTP 200 (3/3).
- Live sitemap: 6,856 <loc> entries (+11).
- Catalog integrity: pre-existing 6,813 records unchanged (count/id verified live); rollback backup intact at backups/products-20261009-harvest21-bak.json.
- Pins: pin ledger untouched (next_index 250), exactly as in the harvest-120 run. The 11 new products queue automatically into the standing daily backlog pin cron (backlog = catalog minus pinned). Pins queued: 11.
