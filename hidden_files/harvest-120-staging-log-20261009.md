# Harvest-120 Staging Log — 2026-10-09

## Outcome: WAVE ABORTED AT VERIFICATION GATE — 0 products staged (catalog protected)

- Candidates processed: 44 of 120 (homepage group, transcribed from the forked parent messages; the 76-item continuation was not staged for the same reason below).
- Staged: **0** · Rejected: **44** (28 failed image verification HTTP 404; 14 stopped at the name-overlap screen before image check — that screen alone is not decisive (see note), but their images remain unverified too; 2 price anomalies).
- Live catalog unchanged: **6,718 products** (data/products.json restored byte-identical, sha256 `29ca8d46098936167e66759815421abef3cca2eb9ebdfab069620557ec7ea992`).
- gen_seo NOT run; nothing committed to products/sitemap; pin ledger NOT touched (pins queued: 0).

## Why it aborted (verified evidence)

Every candidate that reached the image gate (28 of them) returned **HTTP 404 (HEAD and GET)** for its `img.kwcdn.com` image URL. A control test against a known-good existing catalog image (`product/aisc_image/...`) returned **HEAD 200 `image/jpeg`** on the same host in the same minute — so kwcdn HEAD works, and the failure is in the candidate data itself, not the method.

Root cause: the harvest list reached this agent only as text inside forked conversation messages (no on-disk copy exists — `~/workspace`, `~/workspace/agents/`, goals dirs and `/tmp` were searched for the harvested goods_ids; nothing found). Long hex/UUID image identifiers cannot be transcribed from conversation text with verbatim reliability. Because image URLs cannot be verified, the goods_id ↔ image ↔ title pairing cannot be trusted either. Staging anyway would have injected corrupt products (dead images, possibly wrong affiliate destinations) into the live revenue catalog. Per the never-fabricate rule, all candidates were rejected as **unverifiable** instead.

## Candidate-level results (homepage group)

Method per candidate: goods_id + affiliate_url dedupe vs full 6,718 catalog → price sanity → image HEAD/GET verification.

- Price anomalies (rejected on descriptor evidence alone): two "autographed collectible shoes" cards at $85,524.70 and $26,195.20 — not consumer-catalog fits (also > $1,000 cap).
- All other 42 candidates: failed at image verification (HTTP 404). 12 of them also tripped the name-overlap screen before the image check; that screen alone would not have been decisive (the catalog legitimately holds many near-name seller variants; goods_id is the dedupe ground truth), but the image failure is decisive for all.
- No goods_id duplicates vs catalog were found among the candidates that were checked.

## What is needed to complete this wave

The browser harvest must be saved to a file at harvest time (e.g. the browser task writes `~/workspace/affiliate-site/hidden_files/harvest-120-20261009.json` with exact goods_id | title | price | image_url copied from page data, not retyped through chat). With a file-sourced list, this exact pipeline (backup → dedupe → image HEAD → stage → gen_seo → commit/push → live-verify → pin-ledger append) can run unchanged. The 27 blocked Temu images, mascara 404, duplicates lists and all other approval-gated items were not touched.

## Safety state

- Backup (pre-wave, verified 6,718): `~/workspace/affiliate-site/backups/products-20261009-harvest120-bak.json`
- products.json: restored byte-identical from that backup (git status clean for the file).
- Pin ledger `pinterest-2pin-ledger.json`: untouched, next_index 225 preserved.
- Harvest transcription file `hidden_files/harvest-120-20261009.json`: annotated UNVERIFIED — do not stage from it.
