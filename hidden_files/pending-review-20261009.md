# Pending-Review Queue — Products Awaiting Availability Verification

Created: 2026-10-09 (Catalog Expansion run, Phase 1)
Source pool: `~/workspace/affiliate-site/tools/temu-candidates-*.json` (browser-harvested candidate files, Sep 2026, pre-screened 2026-10-09)

## Status summary

- Fresh unique goods_ids on disk NOT in the live catalog: **138**
- Image pre-screen (kwcdn HEAD, read-only): **122/138 images return 200 `image/*`**; 16 image URLs unresolved/failed.
- Name-overlap pre-screen vs full catalog (3+ consecutive distinctive words): 44 candidates have ≥3 overlapping name groups — these need careful human/LLM adjudication against same-name variants before staging (variant vs duplicate), per the standing dedupe rule.
- **Availability of ALL 138 is NOT VERIFIED** — Temu product pages are bot-gated (generic verification shell to curl and to page-text fetch; one cold text-fetch canary on 2026-10-09 returned "no extractable content"). Purchasability can only be confirmed in the signed-in live browser.

## What approval/step unblocks this queue

ONE delegated live-browser pass over `hidden_files/pending-pool-prescreen-20261009.json`:
- Open each candidate's `product_url` (append `&_x_cid=6013029639kol_affiliate` for the managed-account harvest flow, or use the page as served).
- Record: title as displayed, price + currency as displayed, availability state (purchasable / unavailable / sold out / discontinued).
- Any CAPTCHA / Press & Hold / Cloudflare / verify-you-are-human: STOP immediately, report, never solve or bypass.
- Purchasable + fields confirmed → stage with the house schema (category normalized to existing landing categories; `Shoes`/`Jewelry`/`Bags`/`Accessories`/`Fitness`/`Beauty`/`Fashion`/`Lingerie` case-drift corrected to lowercase; `haircare` → `hair`), gen_seo, push, live-verify, then append one pending entry each to the pin ledger.

## Rejected outright (do NOT re-add)

- goods_id 605539736116047, 605712390390884, 607449687913326, 607400631345367, 606682230950099 — Qasim's 5 owner-sent links of 2026-10-09; signed-in browser confirmed **"Unavailable for purchase"/"discontinued"** on all 5 today. Not staged, no pins. (goods data captured in `hidden_files/owner-batch-20261009-intake.json`.)

## Not in this queue (approval-gated, untouched)

- 17 hard-duplicate pairs + 100 exact-name groups (`hidden_files/p1-category-image-duplicate-audit-20261009.md`) — no deletion/merge without Qasim approval.
- 27 Temu products with missing images + 1 verified 404 mascara image — unresolved until original images are verified in a browser pass.
- 13 Part B health products — unmapped by Qasim's decision.
