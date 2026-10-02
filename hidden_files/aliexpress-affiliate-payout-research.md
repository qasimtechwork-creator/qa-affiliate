# AliExpress Portals Affiliate: Payouts, Pakistan Specifics, and Link Attribution
Research date: 2026-10-02. All facts cited with source URLs below.

## 1. How Portals pays affiliates based in Pakistan

- **Payout method: international bank (wire) transfer, in USD.** The official Portals FAQ states the system "currently only supports international bank transfers" and "transactions are handled in USD only."
  Source: https://www.scribd.com/document/449249733/How-to-Make-Money-with-AliExpress-Affiliate-Program-pdf (copy of the official Portals FAQ)
- Some third-party guides also list PayPal as an option ("payment options include PayPal or an international bank account transfer"). However, **PayPal does not operate in Pakistan** ("PayPal still does not support Pakistan officially"; "PayPal, the other major global payment platform, also does not operate in Pakistan"), so for a Pakistan-based affiliate the practical payout route is the international USD wire transfer regardless.
  Sources: https://richniches.com/aliexpress-affiliate-program/ ; https://webstudy.pk/paypal-account-in-pakistan/ ; https://www.techjuice.pk/did-pakistan-finally-get-a-stripe-alternative/
- **Minimum payout threshold: balance must exceed US $16.** ("In order to withdraw your commission, the balance must exceed US $16.")
  Source: https://www.scribd.com/document/449249733/How-to-Make-Money-with-AliExpress-Affiliate-Program-pdf
- **Processing fee: US $15 per withdrawal.** ("There is a US $15 processing fee for withdrawals."; also reported as "$15 per transaction" via Strackr.)
  Sources: https://adswikia.com/aliexpress-affiliate-program-revenue-share/ ; https://richniches.com/aliexpress-affiliate-program/
  Practical consequence: withdrawing at exactly $16 nets about $1. It is only worth withdrawing once the balance is well above ~$31.
- **Payout schedule: withdraw between the 10th and 20th of each month.** ("You can withdraw your commission between the 10th and 20th of each month." Commissions and bonuses are viewable "on, or before, the 20th of each month.")
  Source: https://www.scribd.com/document/449249733/How-to-Make-Money-with-AliExpress-Affiliate-Program-pdf
- **Order completion lag:** a "completed order" means the buyer is satisfied and releases payment to the seller within 60 days of the original purchase date; report data also lags ~3 days (e.g., on March 27 the latest data is March 24).
  Source: https://www.scribd.com/document/449249733/How-to-Make-Money-with-AliExpress-Affiliate-Program-pdf
- **Cookie window: 30 days** per the official FAQ ("AliExpress tracks all valid transactions occurring up to 30 days after a visitor is directed to AliExpress from your affiliate link"). One third-party guide says 7 days; treat the official FAQ figure (30 days) as authoritative and the 7-day figure as unconfirmed.
  Sources: https://www.scribd.com/document/449249733/How-to-Make-Money-with-AliExpress-Affiliate-Program-pdf ; https://cdn.beacons.ai/user_content/oliIiILoOTayaPqB2paOdUKbged2/store_files/ad4fba16-f1a7-4711-9ec5-98b387ddefa0__e3b268cd-1529-4c69-a4c6-5118562aab55.pdf?t=1743442692576

## 2. Where to add bank details in the Portals dashboard (step by step)

1. Sign in at **portals.aliexpress.com** with the AliExpress account used for the affiliate application.
   Source: https://blog.freshstore.com/aliexpress-affiliate-login/
2. In the dashboard navigation, open the **Account** tab (labelled **Settings** in some accounts).
3. Payment/bank details live under **Account** alongside tracking IDs ("Account holds your tracking IDs and payment details").
   Source: https://blog.freshstore.com/aliexpress-affiliate-login/
4. Enter the details for an international USD wire transfer. The standard field set for a cross-border wire is: **beneficiary (account holder) name, beneficiary complete address, bank name, bank address, country, and SWIFT/BIC code** (plus the account number / IBAN).
   Source for generic wire field list: https://leelinesourcing.com/how-to-pay-on-alibaba-payment/comment-page-1/
5. Pakistani banks use **IBAN** (PK + 22 characters, 24 total) for incoming international transfers plus the bank's **SWIFT/BIC code**; the account title must match the bank account holder's name exactly.

Note: the exact on-screen field labels inside Portals can only be confirmed from the logged-in dashboard; the steps above reflect the documented navigation and the standard international-wire field set.

## 3. Do s.click.aliexpress.com/e/... short links carry Tracking ID attribution?

- Yes in effect: AliExpress Portals deep links are generated **using your aff_short_key** (your affiliate short key), which is the publisher identity the system tracks. The s.click.aliexpress.com/e/_xxxx code is that encoded key; the identity is server-side, not human-readable in the URL.
  Source: https://github.com/rishibanota/affiliate-links-generator/blob/HEAD/README.md ("AliExpress Portals: Generates deep links using your aff_short_key")
- Links are produced in the dashboard under **Promo Tools > link generator** ("paste a product URL and get an affiliate link back"). Tracking IDs themselves are managed under **Account > Tracking ID** ("labelled Settings in some accounts"); publishers are advised to create a separate tracking ID per store or traffic source, and reporting is broken down per tracking ID.
  Source: https://blog.freshstore.com/aliexpress-affiliate-login/
- **How to verify attribution:** (a) click your own generated link, then check **Reports** in the Portals dashboard — clicks, orders and commission are reported there, filterable by tracking ID; a test click should appear in the click report within the ~3-day data lag. (b) Confirm the link was generated while signed into the correct Portals account / with the intended tracking ID selected.
  Source: https://blog.freshstore.com/aliexpress-affiliate-login/ ("Reports show clicks, orders and commission")

## 4. Does AliExpress serve shoppers in Pakistan? What a Pakistani visitor sees

- Yes, AliExpress still serves Pakistan, but **budget shipping was suspended on July 7, 2025**: "AliExpress has officially stopped offering several low-cost shipping methods to Pakistan after Pakistani and Sri Lankan authorities imposed new customs tax reforms," blocking "AliExpress Standard Shipping and Cainiao." Sellers were told routes to Pakistan would be "processed offline" due to "unclear tax policies." No timeline was given for restoration.
  Sources: https://www.techjuice.pk/aliexpress-halts-budget-shipping-to-pakistan-amid-new-tax-rules/ ; https://thepublictribune.com/aliexpress-limits-shipping-to-pakistan-amid-customs-crackdown-on-low-cost-deliveries/ ; https://cwpakistan.com/aliexpress-blocks-cheap-shipping-to-pakistan-after-customs-enforce-new-tax-rules/ ; https://thecatchline.com/aliexpress-removes-cheap-shipping-for-pakistan-after-new-customs-rules/
- Remaining options are expensive express carriers (DHL ~14 days, FedEx/UPS ~11 days, EMS ~25 days, e-EMS ~30 days).
  Source: https://www.dropshippinghustle.com/aliexpress-shipping-times/
- Practical result for a Pakistani visitor clicking an AliExpress affiliate product link: many products show **very high shipping fees or "cannot be shipped to your address,"** and some listings appear unavailable in Pakistan. This matches the observed "product not available" behavior when opening affiliate links from a Pakistani IP. Commissions come overwhelmingly from buyers in countries with normal AliExpress shipping (US, Europe, etc.), not from Pakistani clicks.

## 5. Any known problem with a Portals account created/used from a Pakistani IP?

- **No documented Pakistan-specific restriction found.** Portals "is not split by country, and there is no separate affiliate site" by region; the login and program are the same worldwide.
  Source: https://blog.freshstore.com/aliexpress-affiliate-login/
- Approval depends on having a working site with real content ("An empty domain or a placeholder page usually gets turned down"), not on the applicant's country.
  Source: https://blog.freshstore.com/aliexpress-affiliate-login/
- No source found describing bans, earning blocks, or payout blocks specifically for Pakistani IPs or Pakistani-based affiliates. Payout is a USD international wire, which Pakistani banks can receive.
- Caution: this is an absence-of-evidence finding from public sources, not a guarantee. The previously rejected AliExpress **Open Platform** developer profile (API keys) is a separate system from Portals affiliate approval and does not affect affiliate link tracking or payouts.
  Source on API vs Portals separation: https://blog.freshstore.com/aliexpress-affiliate-login/ (API keys are applied for separately under Tools > API)

## 6. Earning reality check (for the parent agent's user question)

- Commission rates: up to ~9% on regular products, up to ~50% on select hot products (per Lasso, via richniches). All products are commission-eligible "if the sale of that product was completed via an affiliate link" and the item is in stock and the transaction completes.
  Sources: https://richniches.com/aliexpress-affiliate-program/ ; https://www.scribd.com/document/449249733/How-to-Make-Money-with-AliExpress-Affiliate-Program-pdf
- The links in use are the standard Portals affiliate links, so they are "real" affiliate links. Whether earnings materialize depends on referred buyers completing purchases within the 30-day cookie window — overwhelmingly non-Pakistani buyers given the Pakistan shipping situation above.
- Bottom line for Pakistan withdrawals: use any Pakistani bank account that can receive USD international wires (IBAN + SWIFT/BIC + exact account title), add it under Portals > Account > payment details, and withdraw between the 10th–20th of a month once the balance exceeds $16 (practically, once it is comfortably above $31 given the $15 fee).
