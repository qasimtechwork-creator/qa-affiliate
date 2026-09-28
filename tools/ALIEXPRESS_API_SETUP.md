# AliExpress Affiliate API — Setup & Import Guide

Imports REAL AliExpress products into the QA Affiliate site (`data/products.json`)
with real tracked links (`https://s.click.aliexpress.com/e/_<code>`) and real
merchant images. No prices, ratings, discounts, or review counts are ever invented —
only merchant/API-provided data is used.

## 1. Credentials you need

| Item | Where to get it | Status |
|---|---|---|
| App key (`ALIX_APP_KEY`) | AliExpress Portals > Tools > API > Apply Now > console | ⏳ apply after approval |
| App secret (`ALIX_APP_SECRET`) | Same place, shown once at app creation | ⏳ same |
| Tracking ID | Portals > Account > Tracking ID — already exists: **`default`** | ✅ have it |

The API application steps in the portal are: Apply for API → Get app key →
Development & testing → Online call. **The app key/secret must be handled via
Secure Vault or entered directly by Qasim — never pasted into chat.**

## 2. Where to put the credentials (pick ONE)

**Option A — environment variables (recommended):**
```bash
export ALIX_APP_KEY="your-app-key"
export ALIX_APP_SECRET="your-app-secret"
# optional: export ALIX_SESSION="oauth-token-if-required"
# optional: export ALIX_TRACKING_ID="default"
```

**Option B — local JSON file (gitignored, never committed):**
Create `tools/.alix_secrets.json`:
```json
{
  "app_key": "your-app-key",
  "app_secret": "your-app-secret",
  "session": "oauth-token-if-required"
}
```
`tools/.gitignore` already excludes this file. The script never prints secrets —
logs show only a masked key prefix.

## 3. Exact commands

```bash
cd ~/workspace/affiliate-site

# 1) Always start here: schema validation, zero API calls
python3 tools/aliexpress_import.py --dry-run

# 2) Small real test: 3 jewelry products, review file only
python3 tools/aliexpress_import.py --limit 3 --category jewelry

# 3) One category, more products
python3 tools/aliexpress_import.py --limit 10 --category shoes

# 4) Full import, all 11 categories (writes review file, does NOT touch products.json)
python3 tools/aliexpress_import.py --limit 5

# 5) Append validated entries to data/products.json (after reviewing the output file)
python3 tools/aliexpress_import.py --limit 5 --merge

# 6) If the API rejects hmac-sha256 signatures, try the legacy md5 scheme
python3 tools/aliexpress_import.py --limit 3 --category bags --sign-method md5

# 7) Raw API JSON dump for debugging field shapes
python3 tools/aliexpress_import.py --limit 1 --category viral --debug
```

Dependencies: `pip install requests pillow` (pillow optional — without it images
save as raw downloads).

## 4. What the script outputs

- `assets/images/products/aliexpress/<aliexpress-<product_id>>.jpg` — real merchant
  images, resized to max 1200px JPEG.
- `tools/aliexpress_import_output.json` — the built product entries (review file,
  gitignored). Nothing is merged into `data/products.json` unless `--merge` is passed.
- Console log: per-product progress, skipped items with reasons, final counts.
- Every entry is schema-validated before being kept: correct types, `merchant:
  "aliexpress"`, a real `s.click.aliexpress.com` tracked link, a local image path,
  and no invented price/rating/review fields. Invalid entries are skipped and their
  downloaded image is deleted.

## 5. Honesty rules baked into the script

- `rating` is **omitted** — AliExpress `evaluate_rate` is a feedback *percentage*,
  never converted into star ratings.
- `sold_count` comes only from the API's `lastest_volume` (merchant data).
- `pros` may include "X% positive feedback on AliExpress (merchant data)".
- `cons` always include the "Price varies — see the live AliExpress deal" lines,
  matching the existing Temu entries.
- Products whose tracked link or image can't be obtained are **skipped**, never
  written with placeholder links.

## 6. If the API isn't approved yet (fallback)

Use the portal's Link Generator manually — Tools > Link Generator
(`https://portals.aliexpress.com/affiportals/web/link_generator.htm`):
pick Tracking ID **default** → set Ship-to country → paste the product page URL →
Get Tracking Link → copy the `https://s.click.aliexpress.com/e/_<code>` output.
Save each product's link; the script can then be extended with a `--manual-csv`
mode, or entries can be added to `data/products.json` by hand following the
schema in `tools/aliexpress_import.py` (`REQUIRED_FIELDS`).

## 7. After import (admin)

1. Review `tools/aliexpress_import_output.json`.
2. Re-run with `--merge`, then set `merchants.aliexpress.enabled: true` in
   `config/affiliates.json` once real links are live.
3. `git add`, commit, push → Vercel redeploys.
