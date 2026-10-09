# Catalog Expansion Log — QA Affiliate toward 10,000

## 2026-10-09 — Phase 1 inspection (read-only)

- Live catalog verified: **6,718 products** (served `https://qa-affiliate.vercel.app/data/products.json` == staged `data/products.json`, byte-identical count).
- Remaining to 10,000: **3,282**.
- Source mix: temu 5,838 · daraz 726 · aliexpress 154.
- Category counts (verified): fashion 1,992 · home 1,182 · beauty 682 · electronics 534 · jewelry 505 · accessories 394 · shoes 392 · bags 345 · fitness 205 · hair 185 · skincare 116 · toys 96 · lingerie 53 · trending 24 · health 13.
- Pin ledger: 5,724 entries, 471 done, 5,253 pending, `next_index` 225 untouched.
- Channels canaried this run:
  - **AliExpress API**: `tools/aliexpress_import.py --dry-run` → ALL CHECKS PASSED (schema). Live API calls BLOCKED — no app key/secret supplied (`tools/.alix_secrets.json` absent, no env keys); developer profile previously rejected (non-blocking per standing record). Channel unavailable until credentials exist.
  - **Temu**: pages bot-gated to curl; one cold page-text fetch this run failed ("no extractable content"). Availability purchasability requires the signed-in live browser (not available to this agent session).
- On-disk candidate pool pre-screened: **138** fresh unique goods_ids not in catalog (122/138 images HEAD 200; 44 with ≥3 name-overlap groups needing adjudication). Filed in `hidden_files/pending-review-20261009.md` + `hidden_files/pending-pool-prescreen-20261009.json`. **None staged** — availability unverifiable without the browser pass (quality bar: no unverifiable product published).
- Waves run this session: **0** (no safe verified data source available to this session). Catalog unchanged: 6,718.
- Rejected (browser-confirmed today): owner batch of 5 goods_ids (605539736116047, 605712390390884, 607449687913326, 607400631345367, 606682230950099) — all "Unavailable for purchase"/"discontinued"; not staged, no pins.
- Unchanged/untouched: 17 duplicate pairs + 100 exact-name groups; 27 missing images + 1 mascara 404; 13 Part B health products; `vercel.json`; all workflows.

## 2026-10-09 — Harvest-120 wave ABORTED at verification (0 staged)
- Candidates transcribed from forked chat messages failed verification: 28/28 sampled kwcdn image URLs 404 (control catalog image HEAD 200). Data unverifiable; nothing staged, catalog restored byte-identical (6,718, sha 29ca8d4609893616). gen_seo not run, ledger untouched, pins queued 0. Remedy: browser harvest must write its list to a file. Detail: hidden_files/harvest-120-staging-log-20261009.md
