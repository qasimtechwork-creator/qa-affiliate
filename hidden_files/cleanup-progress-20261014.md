# QA Affiliate Website Cleanup — Progress Tracker

**Date:** 2026-10-14
**Owner:** Hassan (documentation)
**Ordered by:** Qasim (user)
**Status:** IN PROGRESS

---

## 1. Starting State

| Metric | Value |
|---|---|
| Total products (audit start) | 7,005 |
| Temu | ~5,984 |
| AliExpress | ~295 |
| Daraz | ~726 |

---

## 2. Audit Phase (Qasim + Sohail)

### Qasim — Part 1 (products 0–3502)
- Checked: 3,503
- Verified live: 25 (Daraz only)
- Confirmed dead: 1
- Broken images: 35
- Non-affiliate / bad tracking: 2,710
- Availability unknown (bot protection): 739
- Platform split: Temu 2,623 / AliExpress 154 / Daraz 726

### Sohail — Part 2 (products 3503–7004)
- Checked: 3,502
- Verified live: 0 (no browser access)
- Confirmed dead: 0
- Broken images: 35
- Non-affiliate / bad tracking: 3,367
- Availability unknown: 3,502
- Platform split: Temu 3,361 / AliExpress 141 / Daraz 0

### Key Audit Findings
1. **5,865 Temu products** with corrupted tracking `_x_cid=...kol_affiliate` (invalid affiliate ID — zero commission)
2. **130 Daraz products** with wrong affiliate account IDs (4094161287 / 4094090864 — commission going to someone else)
3. **70 products** with broken images (HTTP 404 / empty / malformed)
4. Temu/AliExpress availability could NOT be auto-verified (bot protection) — marked UNKNOWN, never deleted on guess

---

## 3. Cleanup Actions Completed

### 3a. Broken Image Fix/Remove ✅ DONE
- 70 products processed
- **3 fixed** (new image from source)
- 1 already valid (kept)
- 2 already removed by Daraz cleanup
- **64 deleted** (unfixable)
- Products: 6,436 → **6,372**

### 3b. Daraz Cleanup #1 (wrong/unverifiable IDs) ✅ DONE
- **571 deleted** (130 explicit wrong IDs + 441 unverifiable short links)
- 157 kept (Qasim's correct ID `600023484053`)
- Pin deletion list prepared: 102 pin URLs → `pin-deletion-571daraz-20261014.txt`

### 3c. Daraz Cleanup #2 (remove ALL — Qasim's explicit order) ✅ DONE
- **157 deleted** (all remaining Daraz products)
- **0 Daraz products remain** (verified)
- 157 `/item/<id>.html` SEO pages deleted
- Products: 6,372 → **6,215**
- Pin deletion list prepared: 24 pin URLs → `daraz-all-pins-to-delete-20261014.json`
- Commit: `27fd1358` — pushed to GitHub

### 3d. Temu Corrupted Link Fix ✅ DONE
- **4,908 products** fixed: `_x_cid=6013029639kol_affiliate` → `_x_cid=6013029639`
- **0 corrupted links remain** (verified)
- Site regenerated (gen_lite + gen_pages + gen_seo) and pushed
- Commit: `accb7eaa` — pushed to GitHub

### 3e. New Daraz Products Added (Qasim's own links) ✅ DONE
- `daraz-makeup-organizer-acrylic-box` — Rs.359 — https://qa-affiliate.vercel.app/item/daraz-makeup-organizer-acrylic-box
- `daraz-patex-melamine-dinner-set` — Rs.6,784 — https://qa-affiliate.vercel.app/item/daraz-patex-melamine-dinner-set
- NOTE: Both were later removed in Cleanup #2 (Qasim ordered ALL Daraz removed)

---

## 4. Current State (as of 2026-10-14)

| Metric | Value |
|---|---|
| **Total products** | **6,215** |
| Temu | 5,920 |
| AliExpress | 295 |
| Daraz | 0 |

### Temu Breakdown
| Category | Count |
|---|---|
| Clean US ID (`6013029639`) | 4,924 |
| Pakistani ID (`2056251191`) mentioned | 108 |
| Short links (unverifiable tracking) | 996 |
| Corrupted `kol_affiliate` remaining | 0 ✅ |

### AliExpress Breakdown
| Category | Count |
|---|---|
| Proper affiliate (`s.click.aliexpress.com`) | 289 |
| No tracking (non-affiliate) | 6 ⚠️ |

---

## 5. Remaining Issues

### 🔴 HIGH PRIORITY
1. **Pinterest pin deletion blocked** — Pinterest returns Access Denied on managed browser
   - 102 pins pending (571-product batch) → `pin-deletion-571daraz-20261014.txt`
   - 24 pins pending (157-product batch) → `daraz-all-pins-to-delete-20261014.json`
   - Qasim's PC has working Pinterest — he may need to delete manually, or retry later

### 🟡 MEDIUM PRIORITY
2. **6 AliExpress non-affiliate products** — plain `aliexpress.com/item/` URLs with zero tracking (earn no commission)
   - `aliexpress-glcmyaya-women-sleevelss-halter-v-neck-ruffles-ball-gow`
   - `aliexpress-women-autumn-winter-blouses-t-shirt-geometric-contrast`
   - `aliexpress-women-genuine-leather-hobo-bag-soft-curved-shoulder-pur`
   - `aliexpress-asnora-fashion-cz-bride-indian-jewelry-set-for-women-wa`
   - `aliexpress-asnora-gorgeous-cubic-zirconia-stone-choker-fashion-pea`
   - `aliexpress-rose-gold-silver-plated-diamond-studded-bangle-bracelet`
   - Action: regenerate affiliate links or remove

3. **996 Temu short links unverifiable** — `temu.to/k/` URLs can't be checked without resolving each one individually (bot protection blocks automated resolution at scale)

### 🟢 LOW PRIORITY / MONITORING
4. **Temu availability audit** — Temu product pages trigger security verification on managed browser; availability checks need Qasim's PC/takeover
5. **New product sourcing rules** (Qasim's standing orders):
   - AliExpress: assistant adds (proper affiliate links)
   - Daraz: NEVER add on own — ONLY Qasim's app links
   - Temu: both add — assistant uses only organic/original links

---

## 6. Chronology

| Time (PKT) | Event |
|---|---|
| 2026-10-14 ~03:30 | Qasim + Sohail audit spawned |
| 2026-10-14 ~03:50 | Sohail Part 2 complete |
| 2026-10-14 ~04:15 | Qasim Part 1 complete |
| 2026-10-14 ~04:20 | Broken image fix/remove complete (64 deleted) |
| 2026-10-14 ~04:22 | 2 new Daraz products added (Qasim's links) |
| 2026-10-14 ~04:25 | Daraz cleanup #1 complete (571 deleted) |
| 2026-10-14 ~04:26 | Qasim ordered ALL Daraz removed |
| 2026-10-14 ~04:47 | Daraz cleanup #2 complete (157 deleted, 0 remain) |
| 2026-10-14 ~04:52 | Temu 4,908 corrupted links fixed |
| 2026-10-14 ~05:00 | Pinterest pin deletion blocked (Access Denied) |

---

## 7. Files Reference

| File | Purpose |
|---|---|
| `hidden_files/audit-qasim-part1.json` | Qasim audit results (products 0-3502) |
| `hidden_files/audit-sohail-part2.json` | Sohail audit results (products 3503-7004) |
| `hidden_files/pin-deletion-571daraz-20261014.txt` | 102 pin URLs to delete (batch 1) |
| `hidden_files/pin-deletion-571daraz-20261014.json` | Same, with product ID mapping |
| `hidden_files/daraz-all-pins-to-delete-20261014.json` | 24 pin URLs to delete (batch 2) |
| `hidden_files/daraz-all-removed-ids-20261014.json` | 157 removed Daraz product IDs |
| `/tmp/pins-to-delete.json` | 571 deleted product IDs (ephemeral) |
| `/tmp/broken-images-combined.json` | 70 broken-image product list (ephemeral) |
| `/tmp/daraz-deleted.json` | 571 deleted Daraz products (ephemeral) |

---

*Last updated: 2026-10-14 by Hassan. This is a living document — update as cleanup progresses.*
