# Cache headers plan v2 — `products.json` + `categories.json` (REVISED, minimal change)

Date: 2026-10-09 · Prepared for Qasim's approval · Supersedes the 1-hour proposal in
`p1-cache-headers-plan-20261009.md` (which Qasim did not approve)
**Nothing in this plan has been implemented. `vercel.json` is untouched.**

## 1. The exact proposed change

Add one `headers` array to the existing `vercel.json` (currently it only sets
`cleanUrls`, `trailingSlash` and two legacy redirects). Nothing else in the file changes.

```json
"headers": [
  {
    "source": "/data/products.json",
    "headers": [
      { "key": "Cache-Control", "value": "public, max-age=300, stale-while-revalidate=86400" }
    ]
  },
  {
    "source": "/data/categories.json",
    "headers": [
      { "key": "Cache-Control", "value": "public, max-age=300, stale-while-revalidate=86400" }
    ]
  }
]
```

Where it goes: top level of `vercel.json`, alongside the existing keys. That is the
complete change — two exact-path rules, one header each.

Payload context (measured locally 2026-10-09):

| File | Raw size | gzip | Current live header |
|---|---|---|---|
| `/data/products.json` | 5,303,862 B (~5.06 MiB) | ~679 KiB | `public, max-age=0, must-revalidate` |
| `/data/categories.json` | 7,262 B | ~2.2 KiB | `public, max-age=0, must-revalidate` |

Both files already carry an `ETag` and are served from Vercel's edge
(`X-Vercel-Cache: HIT` observed live on 2026-10-09), so conditional requests already
work today; this plan adds a short browser freshness window on top of that.

## 2. How the header interacts with Vercel's automatic ETag

From Vercel's own docs (sources in §3):

- Static files are automatically cached on Vercel's global network for the lifetime
  of the deployment after the first request; that edge behavior is not changed by
  this plan, and Vercel states that bypassing the cache for static files is not
  possible by design.
- When `Cache-Control` is set *without* a `CDN-Cache-Control` header, the Vercel CDN
  strips `s-maxage` and `stale-while-revalidate` from the response before sending it
  to the browser. Our rule sets neither `s-maxage` nor `CDN-Cache-Control`, so the
  value the browser actually applies is effectively `public, max-age=300` — a
  5-minute local cache, then revalidation. The edge continues to answer
  revalidations with the `ETag` it already serves (`304 Not Modified` when the file
  is unchanged, full `200` when it changed).
- The proposed value satisfies Vercel's cacheability criteria for these files
  (GET request, `200` status, under the 10 MB response limit, no
  `private`/`no-cache`/`no-store` directive).
- Nothing about this config removes or weakens the ETag: the two mechanisms are
  complementary — max-age covers the first 5 minutes, the ETag covers everything
  after.

## 3. Confirmed Vercel behavior vs. assumed behavior

### Confirmed from official Vercel documentation (read 2026-10-09)

1. **Static file caching is automatic for all deployments** and lasts for the
   lifetime of the deployment after the first request; if a static file is
   unchanged it can persist across deployments when its filename carries a hash.
   — Vercel CDN Cache docs (https://vercel.com/docs/caching/cdn-cache)
2. **Route `Cache-Control` headers may be defined in `vercel.json`** and apply to
   static routes exactly as in the docs' own examples; headers returned by a
   Vercel Function would override `vercel.json` for the same route (not applicable
   here — the catalog files are static). — same page, "Using `vercel.json` and
   `next.config.js`"
3. **Without `CDN-Cache-Control`, the CDN strips `s-maxage` and
   `stale-while-revalidate` from the browser-bound response** and the
   `x-vercel-cache` header reports the cache state (HIT/MISS). — same page,
   "CDN-Cache-Control"
4. **Cacheable responses** must be GET/HEAD, status `200` (among others), ≤ 10 MB,
   and must not carry `private`, `no-cache` or `no-store` — our value complies.
   `proxy-revalidate` is not supported by Vercel's CDN (we do not use it).
   — same page, "Cacheable response criteria" / "Limits"
5. **`vercel.json` `headers` rules apply to every matching path by default** (the
   old `routes` + `continue: true` dance is unnecessary with `headers`); **`source`
   path matching for `headers` is case-sensitive.** Our two sources are disjoint
   exact paths, so rule-overlap behavior cannot arise.
   — vercel.json reference (https://vercel.com/docs/project-configuration/vercel-json),
   "Headers" and "Case sensitivity"
6. **Current live baseline on this site:** both JSON files return
   `Cache-Control: public, max-age=0, must-revalidate` with an ETag; the products
   file shows `X-Vercel-Cache: HIT`, `Age: 29` on a repeat fetch — i.e., the edge
   already holds the file and only the browser revalidation is unbounded today.
   (Verified with `curl -I` on 2026-10-09 before this plan was written.)

### Assumed / to verify empirically after approval (honestly flagged)

- **How Vercel's CDN internally treats a plain `max-age=300, stale-while-revalidate=86400`
  on a static-file route** (as opposed to a Function response): the docs do not
  draw the static/function distinction explicitly for this combination. The
  conservative reading is that the edge simply continues serving the current
  deployment's file (confirmed default behavior #1) while the header governs the
  browser — which is already the desired outcome. The post-approval checks in §6
  confirm this with `Age`/`x-vercel-cache` observations instead of assumptions.
- **Same-key conflict resolution between overlapping header rules** is not
  unambiguously documented on the pages read; not relied upon here (disjoint
  sources), noted for completeness only.
- **CDN cache lifetime is best-effort and region-segmented** per the docs ("cache
  times are best-effort and not guaranteed"); we make no promise about edge cache
  residency beyond what the verification step observes.

## 4. Freshness trade-off: 300s vs 3600s vs today's `max-age=0`

How the catalog actually changes: only when we deliberately edit catalog data and
push it (batch adds, category mappings like today's). There is no automatic
minute-level mutation — historically a handful of deploys per week at most,
operator-triggered.

| Policy | Freshness behavior | Cost/benefit |
|---|---|---|
| **Current** `max-age=0, must-revalidate` | Every repeat listing view triggers a revalidation round trip (`304`, small) before the grid can paint; if the catalog changed, a full 679 KiB download. Freshness is effectively instant after a deploy. | Fine on desktop; on mobile each category/listing view pays a network wait before products can render, even when nothing changed. |
| **Proposed** `max-age=300` (+ SWR 86400) | A browser may reuse its local copy for up to 5 minutes after any fetch, with no request at all. After the window, the next fetch revalidates via ETag (`304`, tiny) or downloads the new file (`200`, 679 KiB) if the catalog changed in the meantime. | Repeat views inside a browsing session render the grid instantly; freshness lag capped at ~5 minutes per browser (see below). |
| **Previously proposed (rejected)** `max-age=3600` | Same shape as above, window stretched to an hour. | Only helps very slow/multi-hour sessions marginally more; freshness lag up to an hour. Not recommended as a first step. |

**What "stale" can cost here, honestly:**

- *Price/availability:* this site's JSON carries product identity, images and the
  affiliate destination. Many records deliberately carry no live price at all and
  the product pages tell visitors to confirm the live price on the merchant site
  (the merchant page is what opens on click and always shows the current price).
  A ≤5-minute-old catalog snapshot therefore creates no price-accuracy risk beyond
  the pre-existing "check the live listing" caveat.
- *Catalog edits/removals:* if we deploy a catalog fix (e.g., a category
  correction), a visitor who fetched the JSON up to 5 minutes earlier may still see
  the pre-fix grouping until their copy expires or they revalidate. No 404 risk:
  the item pages are static files that continue to exist regardless of the JSON
  version, and the JSON itself never disappears mid-deploy (see §5).
- *This is the whole trade-off:* up to ~5 minutes of per-browser staleness in
  exchange for eliminating the repeated 679 KiB downloads / revalidation waits in
  normal browsing. Given the operator-driven, low-frequency catalog change rate,
  the staleness window costs effectively nothing in practice.

## 5. Does a new deployment bust the cached file?

By layer, because the answer differs:

- **Vercel edge (CDN):** deployments are immutable and the edge caches static files
  per deployment; once the new deployment is promoted, the edge serves the new
  deployment's `products.json` under the same URL. The old deployment's copy is no
  longer what new requests resolve to. (Docs basis: static files are cached "for
  the lifetime of the deployment", and the site is served from the current
  production deployment.)
- **Browser:** URL stability means the browser key is unchanged — but this is
  exactly what `max-age` governs. A browser inside its 5-minute freshness window
  will keep using its local copy across the deployment boundary; the first fetch
  *after* the window revalidates, sees a new ETag (the file changed), and gets the
  new body with a `200`. So: **yes for the edge immediately, yes for browsers
  within ≤ 5 minutes — never longer, and never silently stale beyond that.** The
  ETag guarantees correctness after the window; nothing pins an old version
  indefinitely.
- **Practical consequence for our workflow:** deploy catalog changes as usual
  (commit → push → Vercel auto-deploy). Returning visitors pick up the change on
  their next post-window fetch; no cache purge action is required or planned.

## 6. Expected benefit at `max-age=300` (honest estimate, not a promise)

Baseline per repeat listing view today: either one revalidation round trip
(sub-second on a good connection, noticeably more on mobile) or, when the catalog
changed, the full ~679 KiB gzip payload. Listing pages (home grid, every category
page) each fetch the full `products.json`, so a normal multi-category session
multiplies this.

With `max-age=300`, every repeat fetch of `/data/products.json` within 5 minutes of
the previous one — the common case for a visitor paging through
fashion → beauty → electronics — is served from the browser's own cache with **no
network request at all**: ~679 KiB of payload avoided per repeat view, and the
product grid can paint immediately instead of waiting on the round trip before
rendering. `categories.json` (~2.2 KiB gzip) benefits trivially.

Estimated session arithmetic for a typical 3–6 listing-view session lasting a few
minutes:

- Today: up to 6 × 679 KiB ≈ 4.1 MB worst case (full downloads), or ≥ 6
  revalidation round trips when nothing changed.
- With this plan: 1 download (~679 KiB) + local cache hits ≈ 679 KiB total —
  roughly **75–85% less JSON traffic** for such sessions, plus the perceived-speed
  win of instant repeat grids on mobile connections.
- Single-page, single-visit sessions: **no change** (first fetch is identical).
- Realistic audience-weighted estimate: **~50–80% reduction in repeat-view
  `products.json` transfers**, dominated by multi-category browsers. This is a
  payload-arithmetic estimate, not a measured benchmark; §7 item 2 measures the
  real effect if the change is approved.

## 7. Verification steps (to run ONLY after approval and deployment — not run now)

1. `curl -sI https://qa-affiliate.vercel.app/data/products.json` and the same for
   `/data/categories.json`: expect `Cache-Control: public, max-age=300,
   stale-while-revalidate=86400` (accept the browser-facing variant
   `public, max-age=300` per docs note §2 and record what actually arrives),
   an `ETag` present, and `x-vercel-cache: HIT` on a second fetch.
2. Repeat-view timing sample: first GET vs immediate second GET of
   `products.json` — record `time_total` and `size_download`; expected: full
   5.3 MB (679 KiB gzip) first fetch, then a cached/`304`-class second fetch
   (~0 payload) inside the window.
3. Category-page regression sweep: `/`, `/category?cat=fashion`,
   `/category?cat=electronics`, `/category?cat=toys`, `/category?cat=fitness`,
   `/category?cat=beauty`, `/category?cat=home` (and the remaining categories) —
   all HTTP 200 with grids rendering from the same JSON.
4. Item-page spot check: 3 today-mapped fitness items + 3 general items — HTTP
   200, images present, labels correct.
5. `sitemap.xml` — HTTP 200, URL count 6,750 (unchanged); live `products.json`
   count still 6,718 with fitness 205.

## 8. Rollback

Delete the `headers` array from `vercel.json` (or revert that one commit) and
push. Vercel redeploys and the platform default
`Cache-Control: public, max-age=0, must-revalidate` resumes automatically for both
files. The rollback touches no data, no URLs, no dashboard settings, and no other
configuration; catalog content and all pages are exactly as before either way.

---
Status: plan only — approval required (Qasim) before any vercel.json edit.
