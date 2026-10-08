# Temu Affiliate Eligibility Pre-Filter — 2026-10-08

## Problem (observed today)
Qasim's 46-product batch (31 Temu + 15 AliExpress) was dropped after sampling: products were not affiliate-link eligible (discontinued, or not enrolled in the affiliate program). On 2026-10-01 the Convert link tool rejected 22 of 50 candidates. Sourcing from the general Temu catalog wastes the browser session's link-generation time.

## Official rule (Temu affiliate FAQ, temu.com/affiliate_question.html)
Commission-eligible products are displayed in the **share-items section of the Temu affiliate page**, and products can be shared directly from the Temu app when marked with the **affiliate/commission icon**. Product eligibility changes with regional promotions, market conditions, and program policy updates.

## Pre-filter checklist for Qasim / Suhail (Temu sourcing)
1. **Source from the affiliate page first** — the share-items/commission section shows only pre-qualified products (commission amount visible). Batches sourced from here convert at near 100%.
2. **General catalog fallback** — open each candidate's product page and confirm the affiliate/share icon or commission info is present BEFORE adding it to the batch. No icon = do not source.
3. **Live stock check** — discontinued/sold-out items are ineligible (observed 2026-10-06: magnetic phone holder showed SOLD OUT; 3 discontinued items in the 2026-10-08 batch).
4. **Over-source by 1.5x** — even with filtering, expect rejections (Security Verification interrupts, regional blocks). Convert more candidates than the batch target.
5. **Log eligibility proof** — for each candidate record the goods_id and the page/section where the commission icon was seen, so a rejected batch can be audited later.

## Expected effect
Batches sourced via this filter should convert at 80%+ instead of today's ~0%, saving roughly one full browser session per batch.
