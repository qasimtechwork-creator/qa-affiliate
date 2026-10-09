# QA Affiliate — Catalog + Import-Workflow Audit (expansion to 10,000)

Date: 2026-10-09 · Read-only audit (nothing deleted or changed in this phase)
Live site: https://qa-affiliate.vercel.app · Catalog file: `~/workspace/affiliate-site/data/products.json`

## 1. Count verification

| Check | Result |
|---|---|
| Live `products.json` count (fetched 2026-10-09) | **6,640** |
| Staged `data/products.json` count | **6,640** |
| Match | ✅ exact |
| `item/*.html` pages on disk | 6,662 (every catalog product has a page; see stale pages below) |
| Sitemap entries | 6,670 `<loc>` (6,640 `/item/` URLs) |

## 2. Duplicates

| Type | Count | Evidence / note |
|---|---|---|
| Duplicate product `id` (slug) | **0** | — |
| Duplicate `affiliate_url` (non-empty) | **17 pairs** | All 17 are `goods.html?goods_id=...&_x_cid=6013029639kol_affiliate` URLs — the same 17 goods_ids each appear twice (e.g. `601100764030720`, `601101496534172`, `601100797414552`, `601099724821487`, `601102109893765`). Per the standing rule, identical affiliate URL ⇒ duplicate product. |
| Exact duplicate product names | **99** | e.g. "creation lamis everyone perfume for men 100ml" ×2, "pack of 4 watch set for men & boys" ×2, "3-tier kitchen organizer rolling utility cart" ×2 — need review (some may be legitimately distinct listings with identical titles; goods_id is the ground truth where knowable). |
| Near-identical names (3+ consecutive distinctive words shared) | **1,558 candidate pairs / 2,261 products** | Too broad to auto-delete — most are legitimate variants (12-piece vs 24-pack yoga blocks, different dresses). Flagged for manual review only. Examples: `temu-openwork-jacket` vs `temu-openwork-cropped-jacket` ("solid color openwork"); `temu-womens-casual-knit-mary-jane-flats` vs `temu-bow-and-pearl-mary-jane-flats`. |
| Knowable goods_ids in catalog | 4,822 of 6,640 | Remaining records use `temu.to` short links (921), Daraz (726), AliExpress (154) — goods_id not recoverable from the stored URL. |

**No deletion performed in this run** (per instructions).

## 3. Broken / missing data

| Issue | Count | Note |
|---|---|---|
| Missing `image_url` | **85** | Mostly `daraz-real-*` records (e.g. `daraz-real-2-in-1-eyebrow-trimmer-for-women-facial-*`). |
| Missing `affiliate_url` | **0** | — |
| Missing `category` | **0** | — |
| Missing `name` | **0** | — |
| Empty `short_description` | 300 | Cosmetic; pages still render. |
| Missing `source` field | 326 | Provenance gap only. |
| Records with a `price` key | 1,594 / 6,640 | Price display is optional in the schema; pages say "check live listing" elsewhere. |
| Broken product images (200-image HEAD sample) | **1 × 404 (0.5%)** | `temu-4d-volumizing-mascara-waterproof-long-lasting-black-mascara` — image `commimg.us.kwcdn.com/...` returns 404. Extrapolation: ≈33 broken images catalog-wide. |

## 4. Category coverage

- **36 raw category values** on products; **12 landing pages** defined in `data/categories.json` (`fashion, shoes, jewelry, bags, beauty, skincare, hair, accessories, lingerie, fitness, trending, home`).
- **773 products map to no landing category**, including **electronics (525 products)** — the 5th-largest group has no category page — plus `toys` (95), `health-fitness` (37), `makeup` (35), `health` (35).
- Case/format drift among raw values: `Beauty` (29) vs `beauty` (608), `Fashion` (15), `Shoes`, `Jewelry`, `Women's Jewelry` (7), `Women's Clothing` (5), `Hair care` variants, `Home & Kitchen`, `Sunglasses` — these products won't match the canonical category pages until normalized.
- Top categories (live counts): fashion 1,970 · home 1,171 · beauty 608 · electronics 525 · jewelry 489 · shoes 379.

## 5. Technical capacity toward 10,000

| Item | Now (6,640) | Projected (10,000) | Verdict |
|---|---|---|---|
| `data/products.json` | 5.0 MB | ~7.5 MB | ⚠️ Client-side rendering fetches the whole file — page weight on listing pages is the main growth risk; consider pagination/lazy data later (not a blocker). |
| `item/` static pages | 6,662 files, 54 MB (22 stale pages for removed products) | ~10,000 files, ~81 MB | OK for Vercel static hosting; prune stale pages in a later cleanup. |
| `sitemap.xml` | 6,670 URLs, 1.3 MB | ~10,030 URLs, ~2 MB | Fine (limit 50,000 URLs / 50 MB). |
| `gen_seo.py` | regenerates all item pages + sitemap + robots each run | ~10k page writes per run | Fine (minutes); unchanged behavior, no experiment needed. |

## 6. Verdict

**No P0 blocker.** Store is intact and verifiable (live = staged = 6,640). Known cleanups queue (not done in this run): the 17 goods_id duplicates, 85 missing images, electronics category page gap, category-value normalization, ~22 stale `/item/` pages.

---
*Phase B of this run uses only pre-verified candidate records already on disk (browser-extracted `round3-pending-temu{2,3}.json`, `round3-pending-replace.json`, `tools/temu-candidates-2026-09-29-*.json`), because Temu now serves generic verification shells to plain curl (HTTP 200 shell, no goods data — same bot-detection behavior noted in prior batches; goods-page titles contradict the shell occasionally but no price/image JSON is served). No CAPTCHA was encountered and none was attempted.*

---

## Phase B — Controlled expansion batch 1 (2026-10-09)

**Sourcing note (blocker, stated honestly):** Temu serves generic verification shells to plain curl (search pages and goods pages return HTTP 200 JS shells with no product JSON; no price/image/metadata extractable by curl). No CAPTCHA challenge was presented to solve and no bypass was attempted. This matches the known Temu bot-detection behavior. Batch 1 therefore used the only verified real-data pool already on disk: the browser-extracted candidate lists `hidden_files/round3-pending-temu2.json`, `hidden_files/round3-pending-temu3.json`, `hidden_files/round3-pending-replace.json` and `tools/temu-candidates-2026-09-29-*.json` (real names, real `img.kwcdn.com` image URLs, real goods_ids). Fresh Temu hunting at volume requires a browser session (parent to delegate) — not attempted here.

**Backups (local, before any change):**
- `~/workspace/affiliate-site/backups/products-20261009-expansion-bak.json` (6,640 records ✓)
- `~/workspace/affiliate-site/backups/pinterest-2pin-ledger-20261009-expansion-bak.json` (5,646 entries, next_index 225 ✓)

**Validation funnel (pool → staged):**
| Stage | Count |
|---|---|
| Candidate pool (goods_id ∉ catalog, name+image present) | 368 |
| Rejected — name matches catalog (3+ consecutive distinctive words) | 287 |
| Rejected — non-English listing | 1 |
| Rejected — dead image URL (HEAD 404/timeout) | 2 |
| **Added** | **78** |

The 287 name-rejections are Temu's seller-variant reality: the catalog already holds same-named products under other goods_ids, and the standing rule treats a matching affiliate URL *or* a 3+-consecutive-distinctive-word name overlap as a duplicate. No record was forced through.

**Added 78 products** across the house categories — shoes 13, accessories 11, jewelry 9, hair 8, skincare 8, trending 7, beauty 7, lingerie 6, bags 4, fitness 3, fashion 2 — each with the house affiliate URL format `https://www.temu.com/goods.html?goods_id=<ID>&_x_cid=6013029639kol_affiliate`, real listing title and image, canonical category id (one of the 12), no invented price/rating (fields omitted where the source data had none).

**Verification (all post-push):**
- Live `https://qa-affiliate.vercel.app/data/products.json` count: **6,718** (6,640 + 78 ✓)
- `tools/gen_seo.py` regenerated: 6,718 item pages, sitemap 6,748 URLs
- Spot-check (5 random new pages, all HTTP 200 with unique titles matching the product):
  - https://qa-affiliate.vercel.app/item/temu-5pcs-chocolate-lip-glaze-set-matte-velvet-long-lasting-liqui — "5pcs Chocolate Lip Glaze Set, Matte Velvet Long-lasting Liquid L…"
  - https://qa-affiliate.vercel.app/item/temu-black-kitten-heel-mule-pumps — "Black Kitten Heel Mule Pumps"
  - https://qa-affiliate.vercel.app/item/temu-womens-slip-on-short-ankle-boots — "Women's Slip-On Short Ankle Boots"
  - https://qa-affiliate.vercel.app/item/temu-womens-bowknot-slip-on-flat-loafers-with-shallow-round-toe — "Women's Bowknot Slip-On Flat Loafers with Shallow Round Toe"

**Pin ledger:** 78 new entries appended (5,646 → 5,724), each `{id, merchant: temu, done: false, note: "Expansion to 10k batch 1 staged 2026-10-09, pin pending"}`. `next_index` left untouched at **225** (pre-existing pinned progress 471 done / 5,175 pending preserved; note the ledger already lagged the catalog by 994 products before this batch — the 78 join the pending queue in catalog order at the end).

**Remaining to 10,000:** 3,282 products (6,718 → 10,000). Next batch needs a browser-extracted candidate pool (the on-disk verified pool is now exhausted by dedup).
