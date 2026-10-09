# P1 — Cache headers + ETag plan for `data/products.json` (PLAN ONLY — NOT IMPLEMENTED)

Date: 2026-10-09 · Scope: **plan only, no changes made** — awaiting Qasim's approval.
Context references: `hidden_files/p1-listing-performance-plan-20261009.md` §3 #1 and §4 #2
(verified ranking puts this first: biggest repeat-visit payload win, smallest risk).

## Current state (verified this run)

- Deployment: pure static Vercel — repo root served as-is, manifest `vercel.json` =
  `{cleanUrls, trailingSlash, redirects}` only (no `headers`, no `functions`, no `routes`).
  No build step, no Vercel CLI needed for a header change (dashboard-free: headers come
  from `vercel.json`).
- `GET https://qa-affiliate.vercel.app/data/products.json` today returns:
  `Cache-Control: public, max-age=0, must-revalidate`, `ETag: "02347708bf98549b11b013a2733c2a9f"`,
  `Last-Modified: ...`, `X-Vercel-Cache: HIT`, `Content-Length: 5303893`
  → i.e., Vercel's static-default: **ETag exists already**, the origin validates cheaply,
  and every browser repeat fetch still asks the origin (must-revalidate + edge revalidation)
  before using local cache. The ~679 KB gz payload returns only when the ETag changed.
- `app.js` (line 448) fetches `/data/products.json` on every listing/search/home/category
  load. Item pages (`/item/<id>`) are fully static and don't fetch it.

## Proposed change (exact)

One `headers` block appended to `vercel.json` — nothing else in the repo changes:

```json
"headers": [
  {
    "source": "/data/products.json",
    "headers": [
      { "key": "Cache-Control", "value": "public, max-age=3600, stale-while-revalidate=86400" }
    ]
  },
  {
    "source": "/data/categories.json",
    "headers": [
      { "key": "Cache-Control", "value": "public, max-age=3600, stale-while-revalidate=86400" }
    ]
  }
]
```

- `max-age=3600`: a returning browser reuses its local copy for 1 hour **without any
  network fetch at all** (vs today's always-revalidate + possible 304 round trip).
- `stale-while-revalidate=86400` (SWIV): after the hour, the browser serves the cached
  file instantly and refreshes in the background — visitors never wait on the origin
  re-check, yet stay at most ~1 day behind.
- **ETag is automatic on Vercel static files and is already being served** (verified
  above). No ETag configuration work exists; the open item is only the `Cache-Control`
  policy. (If additional defense-in-depth is wanted, Vercel also honors `immutable`, but
  `immutable` is wrong for a file that changes weekly — do NOT use it.)

## Expected benefit

| Metric | Today | After |
|---|---|---|
| Repeat listing visit within 1 h (nav to home→category→products→search) | One ETag revalidation round trip per page load (~150–600 ms on budget 4G) + 0 bytes if ETag matches, full ~679 KB gz if catalog changed | **0 network fetches for products.json at all** — instant grid paint from local cache (typical saving: the entire listing LCP wait, app.js still ~9.5 KB gz) |
| Between 1 h and 1 day | Same as above | Served instantly from cache + SWIV background refresh; one conditional (304) round trip in the background, no content download |
| After >1 day stale or hard reload | Full ~679 KB gz as today | Same as today (ETag/conditional or full download on change) |
| Mobile data | Repeat visits ~0–679 KB depending on origin state | Repeat visits ≈0 KB for the payload file |
| TTFB of the listing | ~0.48–0.58 s measured + parse | Listing shell continues to load, but the ~700 KB-class payload wait disappears on cached visits |

Worst case (no improvement): a visitor who always arrives cold (first-ever or >stale)
still downloads the same file — the change can only help, never hurt, a first visit.

## Risk assessment

- **Stale catalog window**: a product change (price, affiliate URL, new batch) takes up
  to ~1 h to become visible to a returning browser, with SWIV making the real visibility
  window typically one visit after the change. Mitigation options if needed:
  `max-age=300` (5 min) still kills same-session revalidations; or cache-bust per deploy
  by version-bumping the filename (heavier — needs deploy tooling; not recommended first).
- **Correctness paths**: Item pages are unaffected (static HTML). Pinterest pins land on
  item pages — unaffected. Search comes from the same cached JSON — consistent within a
  visitor's session; no new failure mode.
- **Deploy timing**: `vercel.json` redeploys automatically on push; headers apply at the
  edge instantly. No code rebuild step exists to break.

## Rollback (exact)

1. Delete the `headers` array from `vercel.json` (or just the two entries) and push —
  the site reverts to today's `max-age=0, must-revalidate` behavior, byte-identical to now.
2. If a full revert of the P1 landing-page run is also needed: restore
  `~/workspace/affiliate-site/backups/products-20261009-p1electronics-toys-bak.json`
  over `data/products.json` and restore `data/categories.json` from git
  (`git checkout HEAD~1 -- data/categories.json`), re-run `python3 tools/gen_seo.py`,
  commit + push. Catalog total stays 6,718 through the whole cycle.
3. No data migration, no URL-change, and no Vercel dashboard setting is involved anywhere
  in this plan — every step is a git file edit.

## Verification steps to run after the change (once approved)

1. `curl -sI https://qa-affiliate.vercel.app/data/products.json` (twice, 2nd run on
   the same URL after the edge caches) → assert `Cache-Control: public, max-age=3600,
   stale-while-revalidate=86400` and the ETag is still present.
2. Conditional check: `curl -sI -H 'If-None-Match: "<etag>"'` → 304 when unchanged,
   200 after the next deploy that edits products.json (confirms ETag invalidation works).
3. Regression sampling: `/category?cat=electronics` (200, title "Electronics"),
   `/category?cat=toys` (200), one old category (`?cat=beauty`),
   home `/`, 3 item pages (one electronics, one toys, one beauty)
   → all 200, item pages still render images, item-page canonicals unchanged.
4. Repeat-view timing sample: fetch `products.json` twice back-to-back from a cold shell
   (curl with cache-disabled) and note TTFB/full-download vs the verified 0.58 s / 0.92 s
   baseline in `p1-listing-performance-plan-20261009.md`; then with a cookie/prefetch
   primed browser-proxy equivalent (`curl` conditional GET) confirm near-instant reuse.
5. Live products.json count after deploy: still **6,718**; electronics 534, toys 96.

## Files/settings the change would touch (concrete)

- `~/workspace/affiliate-site/vercel.json` — one `headers` block (only file).
- Nothing in `tools/`, `assets/`, `data/`, `config/`, or the Vercel dashboard.
- One commit + push (Vercel auto-deploys).

**Status: implementation NOT authorized by this plan.** It sits with the operational
decisions (Electronics/Toys pages already built in this run) for Qasim's call.
