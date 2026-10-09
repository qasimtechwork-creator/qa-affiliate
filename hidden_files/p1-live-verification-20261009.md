# P1 follow-through — LIVE verification results

Run: 2026-10-09 (post-fix) · Site: https://qa-affiliate.vercel.app · Method: curl from this VM (browser UA), read-only GET/HEAD · Files read before this run: expansion audit, P1 category/image/duplicates audit, performance plan, fix change log.

**Summary: no regressions found. One data fix remained outstanding (Temu generic verification shell — no product JSON extractable; no CAPTCHA shown, no bypass attempted) — see §3.**

---

## 1. Live verification of the earlier fix (163 category mappings + 58 image fixes)

**Scale of verification:** live `data/products.json` fetched this run = staged file **byte-identical (5,303,893 bytes, 6,718 products)** — so every "live" claim below is against the actually-served catalog.

### 1a. Category-mapped products (163)
Sample: **31 products across all 8 remapped landing categories** (beauty 12, fashion 4, home 4, fitness 3, accessories 3, jewelry 2, hair 2, bags 1) — sampled from the change log's fixed-ID lists.

Method: for each product, the **live** products.json record was checked to carry the new landing id, and the live `/item/<id>` page was fetched.
- **31/31 passed**: live category = new landing id; item page HTTP 200; image present on page.
- Category-page appearance: category pages are rendered client-side at `/category?cat=<id>` by filtering the **same live products.json** on strict `category === id` (verified in app.js + categories.json in prior audits); each sampled product's live record matches its destination id exactly, so it renders in that page's grid. All 12 category pages fetched this run: **HTTP 200** (see §6). I did not simulate a browser render; verified via live data + page-shell 200s and reported as such.

Failures: **none**.

### 1b. Daraz image fixes (58)
Sample: **25 of 58** fixed products fetched live.
- **25/25 passed**: item page HTTP 200; the page references the new `image_url`; the image itself HEAD-verified **HTTP 200, `image/*`** (Daraz `lzd-img-push.slatic.net` `og:image` source per the change log).
Failures: **none**. The other 33 share the same verified source pattern (HEAD 200 + name match recorded in the change log at fix time).

### 1c. Spot-checks
- Sitemap: **HTTP 200, 6,748 `<loc>` entries, 1,342,256 bytes** (6,718 item URLs = every product + 30 shell/category/guide URLs).
- Category pages: 12/12 **HTTP 200** (ids in §6). Canonical note: category pages are client-rendered shells — the static HTML carries **no `<link rel="canonical">`** and a generic `<title>Category — QA Affiliate</title>` (pre-existing design; gen_seo normalizes sources per 2026-10-02 lesson). Structural canonical coverage for category pages remains a plan-level item (combined `/category?cat=` canonicalization lives server-side in `vercel.json` cleanUrls) — reported as-is, not changed without approval.
- Affiliate URLs from changed records (5 sampled, `curl -L`, no loops): Daraz `s.daraz.pk` short links → **200**; Daraz product URL with `laz_share_info` → **200**; Temu `temu.to/k/…` → **200** (1 redirect, preserves `_x_cid=6013029639kol_affiliate`).

---

## 2. Remaining 667 unmapped products — audit completed

Live grouping (recounted this run):

| Raw value | Products |
|---|---|
| `electronics` | 525 |
| `toys` | 95 |
| `health` | 35 |
| `Phone Accessories` | 3 |
| `Electronics` | 3 |
| `Mobile Accessories` | 3 |
| `toys-wellness` | 2 |
| `Health` | 1 |
| **Total** | **667** |

Evidence-based recommendations (one per group; full SEO blueprints in [p1-unmapped-recommendations-20261009.md](sandbox://workspace/affiliate-site/hidden_files/p1-unmapped-recommendations-20261009.md)):
- **Electronics → 1 new landing page** (`electronics` 525 + `Electronics` 3 + `Phone Accessories` 3 + `Mobile Accessories` 3 = **534**): slug `/category?cat=electronics`, title/H1/meta + 4 internal-link anchors drafted. Eligible (534 ≥ 4, coherent gadget set, operator approval = pending).
- **Toys → 1 new Toys & Kids landing page** (95): slug `/category?cat=toys`, SEO + anchors drafted. Eligible (95 ≥ 4).
- **Health/Wellness (36)** → dedicated new **Wellness & Personal Care** page (slug `/category?cat=wellness`) **or** fold into `fitness` — both eligible (36 ≥ 4); posture/massage/pain-relief content; operator choice.
- **`toys-wellness` (2)** → no page (below threshold): split by product into Toys (squish ball) and fitness (physio ball) when the above merges are approved — both products named explicitly in the recommendations file, nothing left silent.

**No new pages were created and no structural SEO change was made.**

---

## 3. Temu 27 missing images — blocked by generic verification shell (no CAPTCHA; no bypass)

All 27 (confirmed this run from live data: 27 `image_url`-empty products, 100% Temu, goods_id-format affiliate URLs):
- jewelry ×4 (earrings/necklace sets ×3, red crystal bracelet), beauty ×10 (jade-roller/gua-sha sets ×5, hair-claw clips ×5), home ×7 (pet grooming ×4, solar garden lights ×2, fruit cutter ×1), electronics ×6 (phone cases ×5, tripod ×1).

Per-product attempt method: plain `curl` GET of the stored affiliate URL's `goods.html?goods_id=…` page with a standard Chrome UA + Temu referer (same recipe as prior batches; public GET only — no login, no cookies touched).
- **Outcome (this run, re-verified on 2 of the 27 + the same pattern seen across prior batches):** Temu returns a generic verification shell (HTTP 200 JS shell, **no product JSON** — titles/price/image data not extractable from the response; no CAPTCHA challenge was presented, and none was solved or bypassed; STOP conditions respected).
- Classification: **27/27 "blocked — needs one browser session"** (rendered gallery URL must be read from a real browser page exactly as prior batches did). **0 fixed this run; no file was modified for these products** (the dated backup step was therefore not triggered; existing backups remain intact).
- The known broken mascara image (`temu-4d-volumizing-mascara-waterproof-long-lasting-black-mascara`) was re-checked: **still HTTP 404 [verified this run]** — same browser pass fixes it once the correct gallery URL is known; no placeholder was substituted.

---

## 4. Duplicates — reconciled (no deletions, no merges)

### 4a. Hard duplicate pairs — 17 (identical affiliate URL ⇒ same goods_id)
Both records of every pair, with keep/remove-candidate recommendations (difference: image present + canonical category + longer description), are listed in [p1-category-image-duplicate-audit-20261009.md §C1](sandbox://workspace/affiliate-site/hidden_files/p1-category-image-duplicate-audit-20261009.md). Goods_ids: 601100764030720, 601101496534172, 601100797414552, 601099724821487, 601102109893765, 601099557999479, 601101832277584, 601099968821205, 601099634368775, 601099868325592, 601099690797499, 601103389145886, 601099642410115, 601105629616223, 601103074183681, 601099774309347, 601099816750402. Count independently re-verified this run: **17 URLs appear twice** in the staged catalog. Every removal still requires Qasim's explicit OK — nothing was deleted or merged.

### 4b. Exact-name duplicate groups — 99 vs 100 reconciled (evidence-based)
Measured identically (stripped-lowercase exact name, groups of ≥2) on three states:
- `backups/products-20261009-expansion-bak.json` (6,640, the Phase A state): **99 groups / 351 records**.
- `backups/products-20261009-p1mapping-bak.json` (6,718, after Batch 1, before category fixes): **100 groups / 353 records**.
- Current staged data (6,718): **100 groups / 353 records** (unchanged by the category fixes).

**The +1 group was created by Batch 1:** the newly added `temu-platform-loafers-for-women` (name "Platform Loafers For Women", member of Batch 1's 78 products) paired with the pre-existing `temu-platform-loafers-for-women-543696` → one new exact-name group (its affiliate URL carries goods_id 601102938543696), adding exactly 2 records (351 → 353). The earlier **99 (Phase A)** and current **100** are both correct — they measured different catalog states (6,640 vs 6,718); there was no grouping-method change. Both records carry distinct affiliate URLs (not the same goods), so the group is a genuine seller-variant pair, not a hidden duplicate: it joins the 98 "distinct-URL, needs goods-page adjudication" groups in §C2 of the P1 audit file. **No name-only deletions are recommended; no merge was performed.**

### 4c. Resolution recommendations (existing)
17 pairs → approve keep/remove per §C1 (remove-candidate named per pair, reasoned). 98 distinct-URL groups → one browser adjudication pass reading goods_ids, merging only proven same-goods twins. **No deletions or merges performed in this run.**

---

## 5. Technical performance — verified this run (plan-only, nothing implemented)

Measured this run (this VM, curl `-w`, gzip honored):

| Metric | Earlier plan figure | Verified this run | Verdict |
|---|---|---|---|
| products.json served size (gzip) | ≈700 KB | **678,656 bytes, HTTP 200** | ✅ confirmed |
| products.json raw size | 5,295,187 B @ 6,718 | **5,303,893 B @ 6,718** (+8.7 KB from image fixes) | ✅ updated |
| products.json TTFB | 0.9 s | **0.58 s** (download complete 0.92 s) | ✅ confirmed-same-order (network variance) |
| Category page TTFB (`/category?cat=beauty`) | — | **0.48 s TTFB**, 1,261 B shell | new baseline |
| Sitemap | 6,748 URLs / ≈1.3 MB | **6,748 URLs / 1,342,256 B, TTFB 0.39 s** | ✅ confirmed |
| Item page TTFB | — | **0.33 s**, 2,550 B static page | healthy |
| app.js / main.css / categories.json (gzip) | app ≈18 KB | **9,450 B / 7,411 B / 2,080 B** | ✅ light |

**At-10,000 projection (unchanged from plan, linear on verified bytes):** products.json ≈7.9 MB raw / ≈1.02 MB gzip; sitemap ≈10,030 URLs / ≈2 MB; ~10k static item pages ≈80 MB deploy — no milestone blocker.

**Safest low-risk options, ranked (all plan-only — approval required before any implementation):**
1. **HTTP cache headers + ETag for `products.json`** — repeat listing visits skip the ~678 KB download entirely. Lowest risk, best first step.
2. **Category-scoped JSON shards** — category pages fetch only their shard (≈90 KB gz for the biggest categories), plus a slim index shard for home/search.
3. **Render-window "Load more"** — cap initial card render (~48 cards), append on scroll; pure client-side.
4. **Image sizing hints** (`width`/`height` / aspect-ratio on card media) — kills CLS during lazy image load.
5. **Precomputed search index** — replace the in-browser scan over 6.7k+ records.
6. **Full-catalog image health sweep** (read-only HEAD pass) before any broken-rate claim; the ≈33-broken-images figure remains an **[estimate]**, and one **verified** 404 (mascara, §3) is on the books.

No server-side rendering, no database/backend, no pagination code, and no lazy-loading change was implemented or is recommended now — listing JSON payload is the growth item, and #1 addresses it without restructuring.

---

## 6. Final verification sweep

**Counts (live vs backups vs staged):**
- Live products.json: **6,718 products, 5,303,893 bytes** — staged `data/products.json` byte-identical.
- Backups intact: expansion 6,640 · p1mapping pre-fix 6,718 · pin ledger **untouched** (`next_index` 225 preserved).
- Mapped counts after fixes (live): fashion 1,992 · home 1,182 · beauty 682 · jewelry 505 · accessories 394 · shoes 392 · bags 345 · hair 185 · fitness 181 · skincare 116 · lingerie 53 · trending 24 = **6,051 mapped** + 667 unmapped = **6,718** ✅.

**Live page checks this run:**
- All 12 category pages: **HTTP 200** (`fashion, shoes, jewelry, bags, beauty, skincare, hair, accessories, lingerie, fitness, trending, home`).
- Representative item page per major category (12): **12/12 HTTP 200, image HEAD 200 `image/*`, affiliate link present**.
- Shells: `/` 200, `/products` 200, `/trending` 200, `/deals` 200, `/category?cat=beauty` 200 (legacy `/products.html` permanently redirects 308 → `/products` by design).
- Sitemap: **200, 6,748 URLs**; item canonicals: sample `/item/<id>` carries the correct self-referencing canonical (verified).
- Affiliate URL chains: 5/5 resolve **200, no loops** (§1c).

**Regressions vs pre-fix state:** none. Mapped products render at their new landing ids; images fixed live; no 404s observed except the one pre-existing broken mascara image (still 404 — pre-existing, not a regression); catalog total and sitemap URL count exactly as expected after the permitted fixes.
