# P1 — Remaining 667 unmapped products: category / landing-page recommendations

Date: 2026-10-09 (live-recounted this run) · Site: https://qa-affiliate.vercel.app

Evidence basis: live `data/products.json` (6,718 products, fetched this run) grouped by raw `category` value; the 12 existing landing ids are `fashion, shoes, jewelry, bags, beauty, skincare, hair, accessories, lingerie, fitness, trending, home` (verified live from `data/categories.json`).

**Nothing in this file was applied.** New landing pages, category merges, and canonical changes all require Qasim's approval (plan-only per scope).

## Group inventory (live counts)

| Raw value | Products | Recommendation |
|---|---|---|
| `electronics` | 525 | **New Electronics landing page** (with the 3 small groups below, 534 total) |
| `Electronics` | 3 | Merge raw value into the new Electronics page (recategorize with the page build — plan-only) |
| `Phone Accessories` | 3 | Merge raw value into the new Electronics page (plan-only) |
| `Mobile Accessories` | 3 | Merge raw value into the new Electronics page (plan-only) |
| `toys` | 95 | **New Toys & Kids landing page** |
| `toys-wellness` | 2 | Split by product — see note below (does not justify a page) |
| `health` | 35 | **New Wellness & Personal Care landing page** (36 with `Health` below) |
| `Health` | 1 | Merge raw value into the Wellness page (plan-only) |

Total: **667 products**.

## Recommendations

### ELECTRONICS-1 — Build new Electronics landing page (534 products)
`electronics` 525 + `Electronics` 3 + `Phone Accessories` 3 + `Mobile Accessories` 3 = **534 products**.
Content: smartwatches, earbuds, phone cases/mounts, chargers, ring lights/tripods — a coherent gadget catalog; currently invisible from every category page (strict `category === id` filter).
- Proposed slug: `/category?cat=electronics` (same URL pattern as the 12 existing pages — no URL scheme change).
- Title: "Electronics Deals — Best Gadgets, Smartwatches & Phone Accessories | QA Affiliate"
- H1: "Electronics"
- Meta: "Affordable gadgets, smartwatches, earbuds and phone accessories — trending tech picks with honest pros and cons."
- Internal-link anchors (3–5): Fashion & Clothing · Home & Lifestyle · Viral & Trending · Bags & Handbags.
- Eligibility: 534 ≥ 4 — clears the page threshold easily.

### TOYS-1 — Build new Toys & Kids landing page (95 products)
`toys` 95.
Content: plush/teddies, DIY/craft kits, art supplies, party favors — reads as a single coherent kids+crafter catalog.
- Proposed slug: `/category?cat=toys`.
- Title: "Toys & Kids Finds — Viral Play, Learning & Gift Ideas | QA Affiliate"
- H1: "Toys & Kids"
- Meta: "Trending toys and kid-friendly finds — squishies, learning toys and gift ideas parents actually rebuy."
- Internal-link anchors (3–5): Fitness & Lifestyle (active play) · Viral & Trending · Home & Lifestyle · Fashion & Clothing (kids-wear crossovers).
- Eligibility: 95 ≥ 4 — clears the threshold.

### HEALTH-1 — Wellness: dedicated small page (36 products) or fold into fitness (operator choice)
`health` 35 + `Health` 1 = **36 products**.
Content: posture belts/correctors, massage tools, heat pads, knee/wrist supports — wellness/personal-care, adjacent to but distinct from exercise gear.
- Proposed slug: `/category?cat=wellness`.
- Title: "Wellness & Personal Care — Posture, Massage & Pain-Relief Tools | QA Affiliate"
- H1: "Wellness & Personal Care"
- Meta: "Posture correctors, massage tools, heat therapy and everyday wellness gear — practical picks with honest limitations."
- Internal-link anchors (3–5): Fitness & Lifestyle · Beauty & Cosmetics · Home & Lifestyle.
- Alternative (if Qasim prefers fewer pages): fold into `fitness` (renaming it "Fitness & Lifestyle" — it already is named "Fitness & Lifestyle") — 36 products is past the eligibility threshold either way, so both options stay open; the choice is editorial.

### Note on small raw values (never silent)
- `toys-wellness` (2): `daraz-real-magic-color-changeable-grape-mesh-squish-ball-stress-relief` (squish/sensory toy) and `daraz-real-hand-exercise-stress-relief-smiley-emoji-physio-ball-yellow` (physio/exercise ball). Recommendation: split by product — squish ball into the new Toys & Kids page, physio ball into fitness — when those pages/recategorizations are approved. Two products never justified a landing page of their own.
- No product was deleted, hidden, or dropped. Every recommendation above keeps all 667 products reachable.

## Threshold rule check
Eligibility = ≥4 products, an operator-approved destination, and a diverse (non-duplicate-cluster) product set. Results: Electronics 534 ✅, Toys 95 ✅, Wellness 36 ✅ (or merge into fitness), small accessory raw values (3 each) fold into an approved destination rather than their own pages.
