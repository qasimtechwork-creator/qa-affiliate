# QA Affiliate — P1 Listing Performance Technical Plan (READ-ONLY)

Date: 2026-10-09 · Scope: **plan only — no changes were made** to code, config, data, or deployment by this document.
Site: https://qa-affiliate.vercel.app · Repo: `~/workspace/affiliate-site` · All production changes need Qasim's separate approval.

## 1. How the site renders today **[verified — code + live fetch]**

| Piece | Size / count | Notes |
|---|---|---|
| `data/products.json` (live) | **5,295,187 bytes raw / ≈700 KB gzip** | One file, all **6,718** products, avg ≈788 bytes/record |
| Listing shells (`index`, `products`, `category`, `trending`, `deals`) | 2.7–10.8 KB HTML each | Static shells; content injected by JS |
| `assets/js/app.js` | 27.8 KB (≈18 KB gzip with css/categories combined measure) | Fetches `/data/products.json` + `/data/categories.json` + config, filters in browser (`category === id`), renders cards with `loading="lazy"` images |
| `assets/css/main.css` | 26.5 KB | Single stylesheet |
| `item/` static pages | 6,740 files on disk, 54 MB (6,718 current + ≈22 stale from Phase A) | Pre-rendered by `tools/gen_seo.py`; each with canonical + JSON-LD + og tags |
| `sitemap.xml` | 6,748 URLs, ≈1.3 MB | Includes 12 `category?cat=` URLs + all item pages |

**First-load cost of a listing page (mobile):** HTML shell (~3-11 KB) → app.js + CSS (~20 KB gz) → **products.json ~700 KB gz (TTFB 0.9 s, full download 2.4 s measured from this VM [verified])** → JS parses 5.3 MB of JSON, builds product cards, then lazy product images flow in from `img.kwcdn.com` / Daraz CDNs. The cards cannot paint before the full JSON downloads and parses — that download *is* the listing LCP path.

## 2. Impact at 10,000 products (linear scaling of measured values)

| Metric | Now (6,718) | At 10,000 | Assessment |
|---|---|---|---|
| products.json raw | 5.30 MB | ≈7.9 MB (788 B × 10k) | Gzip ≈1.04 MB transfer on *every* cold listing visit |
| JSON parse (mid-tier Android) | ~0.3–0.8 s main-thread **[estimate]** | ~0.5–1.2 s **[estimate]** | Noticeable input-delay on low-end phones |
| Item pages / disk | 6,740 files / 54 MB | ~10,000 files / ≈80 MB | Fine for Vercel static hosting |
| sitemap.xml | 6,748 URLs / 1.3 MB | ~10,030 URLs / ≈2 MB | Well under the 50k-URL / 50 MB limit |
| gen_seo.py run | Regenerates all item pages + sitemap | ~10k page writes per run | Still fine (minutes); unchanged |
| Crawl budget | Sitemap advertises ~6.7k pages | ~10k pages is routine for sitemaps | No blocker; per-page quality matters more than count |

**Bottleneck verdict:** the only real growth risk is the **monolithic products.json download+parse on listing pages**. Item pages (the URLs Google indexes and Pinterest lands on) are static and unaffected. Nothing blocks the 10,000 milestone; the client payload just gets steadily worse for mobile visitors from Pakistan on budget Android devices.

## 3. Recommendations — ordered by impact/effort (all require Qasim's approval before implementation)

| # | Change | What changes | Expected benefit | Risk | Approval needed? |
|---|---|---|---|---|---|
| 1 | **HTTP caching headers for products.json** (verify/set long `Cache-Control` + ETag on Vercel) | `vercel.json` headers block only | Repeat visits skip the ~700 KB download entirely — instant listings for returning traffic | Low. Stale data window = cache TTL (mitigate with `stale-while-revalidate`) | Yes |
| 2 | **Category-scoped JSON shards** | Split one 5.3 MB file into per-category files (~534 max products each); category pages fetch only their shard; a slim index shard (id/name/image/category, ≈40% size) for Search/Home | Category LCP payload drops ~85% on big categories (≈90 KB gz for beauty vs 700 KB) | Medium. app.js fetch logic + gen_seo output naming must stay consistent; Pinterest/item pages untouched | Yes |
| 3 | **Render-window pagination ("Load more")** | app.js renders first ~48 cards, appends on click/scroll instead of injecting entire filtered sets (home lists up to several thousand DOM nodes) | Faster first paint and scrolling; less memory on low-end phones | Low. Pure client-side; must preserve existing filter/search behavior | Yes |
| 4 | **Card-image sizing hints** (`width`/`height` or aspect-ratio CSS on card media) | Template in app.js + CSS | Kills layout shift (CLS) as lazy images arrive | Low | Yes |
| 5 | **Precomputed search index** (offline-built, shipped as the slim shard from #2) | Replace in-browser substring scan over 6.7k records with name/category/subcategory index fetch | Instant search on mobile; CPU saving scales with catalog | Low–medium (build step inside gen_seo) | Yes |
| 6 | **Full-catalog image health sweep + 404 repair loop** (read-only HEAD sweep, then approved per-image patches) | Operations, not code | Fixes the known 404 class (~33 est.); prevents Pinterest landing pages with broken hero images | None for the sweep; patches already covered by Qasim's image-fix permission | Sweep: this plan; patches: standing permission |

**Deliberately NOT recommended now:** server-side rendering migration, database/API backend, image CDN rewrite (hotlinking merchant CDNs is the current design; Pinterest requires the *original* merchant image URL on pins anyway), and lazy-loading everything indiscriminately — product images already lazy-load; the JSON is the payload problem, not the images.

## 4. Sequencing proposal

1. Land the category fixes + image fixes (done this run) and the plan-only decisions (new Electronics/Toys pages, dedup approvals).
2. With Qasim's approval, implement #1 (headers) — 15-minute change, immediate repeat-visit win.
3. Then #2 + #3 together (one app.js pass), verified against live category counts before/after.
4. Resume controlled catalog expansion in small batches; re-measure JSON size after each 1,000 products and re-run this plan's table.

## 5. Statement of state

**No changes were made by this plan.** The only production writes in this P1 run were the permitted category/image fixes documented in the audit file and change log (backup: `~/workspace/affiliate-site/backups/products-20261009-p1mapping-bak.json`; commit `196149e` on `qa-affiliate`, verified live: 6,718 products, missing-image count 27, changed pages HTTP 200). Everything in section 3 awaits Qasim's explicit approval.
