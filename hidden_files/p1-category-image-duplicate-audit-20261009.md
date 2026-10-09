# QA Affiliate — P1 Audit: Category Mapping, Missing Images, Duplicates + cleanup (2026-10-09)

Site: https://qa-affiliate.vercel.app · Data: `data/products.json` · Run date: 2026-10-09 · Catalog state: **6,718 products** (6,640 verified Phase A + 78 batch-1, verified live after this run).
Scope per Qasim's Master Instruction: audit first; then apply ONLY the explicitly-permitted fixes (unambiguous category mapping onto EXISTING landing pages + verifiable original-image fixes); duplicates remain recommendation-only; pagination stays plan-only. Backups and change log referenced below. Production edits beyond that: **none**.
> Verified/estimate discipline: **[verified]** = measured from products.json, HEAD/GET, or live fetch in this run; **[estimate]** = extrapolated; figures that could not be checked are marked **NOT VERIFIED** inline.

STOP-condition watch: no CAPTCHA / Press & Hold / Cloudflare / verification wall encountered (Temu goods pages returned full HTML 200 to curl; Daraz public pages fetched cleanly). Nothing was bypassed; no logins; no cookies cleared.

---
# A. Category mapping audit (36 raw values → 12 landing pages)

Landing pages are rendered client-side at `https://qa-affiliate.vercel.app/category?cat=<id>` from `data/categories.json`; category filtering uses strict `category === id` matching (app.js), so any raw value that is not exactly a landing id — including pure case drift like `Beauty` — never renders on its category page. **[verified — code read + live category JSON counts]**

Counts below are from the pre-fix backup (6,718). 12 raw values already match landing ids (5,888 products); 24 raw values did not (830 products). Note on the earlier **773** figure (Phase A, 6,640) **[verified]**: that count excluded pure case-drift spellings (`Beauty`, `Fashion`, …); the strict every-unmatched-value count is 830 at 6,718 (56–57 are case/wording drift of an existing landing id). Both are true under their definitions; this report uses the strict count.

## A1. Raw category inventory — all 36 values
| # | Raw value | Products | Landing page? | Status / recommendation |
|---|---|---|---|---|
| 1 | `fashion` | 1972 | yes — https://qa-affiliate.vercel.app/category?cat=fashion | — landing exists; canonical id |
| 2 | `home` | 1171 | yes — https://qa-affiliate.vercel.app/category?cat=home | — landing exists; canonical id |
| 3 | `beauty` | 615 | yes — https://qa-affiliate.vercel.app/category?cat=beauty | — landing exists; canonical id |
| 4 | `electronics` | 525 | no | **NEW page needed** — Electronics |
| 5 | `jewelry` | 498 | yes — https://qa-affiliate.vercel.app/category?cat=jewelry | — landing exists; canonical id |
| 6 | `shoes` | 392 | yes — https://qa-affiliate.vercel.app/category?cat=shoes | — landing exists; canonical id |
| 7 | `accessories` | 384 | yes — https://qa-affiliate.vercel.app/category?cat=accessories | — landing exists; canonical id |
| 8 | `bags` | 342 | yes — https://qa-affiliate.vercel.app/category?cat=bags | — landing exists; canonical id |
| 9 | `hair` | 177 | yes — https://qa-affiliate.vercel.app/category?cat=hair | — landing exists; canonical id |
| 10 | `fitness` | 144 | yes — https://qa-affiliate.vercel.app/category?cat=fitness | — landing exists; canonical id |
| 11 | `skincare` | 116 | yes — https://qa-affiliate.vercel.app/category?cat=skincare | — landing exists; canonical id |
| 12 | `toys` | 95 | no | **NEW page needed** — Toys & Kids (plan-only) |
| 13 | `lingerie` | 53 | yes — https://qa-affiliate.vercel.app/category?cat=lingerie | — landing exists; canonical id |
| 14 | `health-fitness` | 37 | no | → fitness (applied) |
| 15 | `makeup` | 35 | no | → beauty (applied) |
| 16 | `health` | 35 | no | Qasim decision — new Wellness page OR merge into fitness (plan-only) |
| 17 | `Beauty` | 29 | no | → beauty (applied) |
| 18 | `trending` | 24 | yes — https://qa-affiliate.vercel.app/category?cat=trending | — landing exists; canonical id |
| 19 | `Fashion` | 15 | no | → fashion (applied) |
| 20 | `hair care` | 8 | no | → hair (applied) |
| 21 | `Women's Jewelry` | 7 | no | → jewelry (applied) |
| 22 | `Home & Kitchen` | 5 | no | → home (applied) |
| 23 | `Women's Clothing` | 5 | no | → fashion (applied) |
| 24 | `Sunglasses` | 4 | no | → accessories (applied) |
| 25 | `Kitchen Gadgets` | 3 | no | → home (applied) |
| 26 | `Phone Accessories` | 3 | no | merge into new Electronics page (plan-only) |
| 27 | `Electronics` | 3 | no | merge into new Electronics page (plan-only) |
| 28 | `Mobile Accessories` | 3 | no | merge into new Electronics page (plan-only) |
| 29 | `Handbags & Clutches` | 3 | no | → bags (applied) |
| 30 | `Hijabs & Scarves` | 3 | no | → accessories (applied) |
| 31 | `Women's Watches` | 3 | no | → accessories (applied) |
| 32 | `nail art` | 3 | no | → beauty (applied) |
| 33 | `Cleaning` | 2 | no | → home (applied) |
| 34 | `toys-wellness` | 2 | no | Qasim decision — Toys or Fitness (items are mixed; 2 only) |
| 35 | `Home Lighting` | 1 | no | → home (applied) |
| 36 | `Health` | 1 | no | merge with `health` (plan-only) |

## A2. Fixes applied in this run (permitted scope only)
163 products normalized onto EXISTING landing ids (no new pages, no URL/canonical changes). Details per product: [p1-fix-changelog-20261009.md](sandbox://workspace/affiliate-site/hidden_files/p1-fix-changelog-20261009.md) · Backup: `~/workspace/affiliate-site/backups/products-20261009-p1mapping-bak.json` (6,718 records; sha256 matches pre-edit data file) **[verified]**.

Post-fix verified product totals (live data/products.json re-fetched after deploy): beauty 682 · fashion 1,992 · hair 185 · fitness 181 **[verified — live fetch]**.

## A3. Recommended final category set (16 landing pages — well under the ≤24 cap)

Keep the 12 current pages and add four (plan-only; new pages and canonicals require Qasim's approval):
| Recommended page | URL (proposed structure) | Absorbs | Products after mapping |
|---|---|---|---|
| Electronics (NEW) | `/category?cat=electronics` | electronics 525 + Electronics 3 + Phone Accessories 3 + Mobile Accessories 3 | 534 |
| Toys & Kids (NEW) | `/category?cat=toys` | toys 95 (+ toys-wellness 2 if Qasim agrees) | 95–97 |
| Wellness (NEW, optional) | `/category?cat=wellness` | health 35 + Health 1 | 36 |
| Beauty & Cosmetics (existing, widened) | `/category?cat=beauty` | already absorbed makeup 35, Beauty 29, nail art 3 | 682 |

Alternative for Wellness: fold its 36 products into `fitness` ('Fitness & Lifestyle') instead of a new page — recommended only if Qasim wants the page count minimal; the products are wellness/personal-care (posture belts, heat pads, massage tools), so a small dedicated page reads better to shoppers. **Decision = Qasim's.**

### SEO structure per recommended page (title / H1 / meta) + internal-link anchors

*(New pages only need these as blueprints; loop when built: title formula `{Name} — QA Affiliate`, H1 = name, meta = the line below.)*

- **Electronics** — title: "Electronics Deals — Best Gadgets, Smartwatches & Phone Accessories | QA Affiliate" · H1: "Electronics" · meta: "Affordable gadgets, smartwatches, earbuds and phone accessories — trending tech picks with honest pros and cons." · internal-link anchors (3-5): Fashion & Clothing · Home & Lifestyle · Viral & Trending · Bags & Handbags (chargers travel cases).
- **Toys & Kids** — title: "Toys & Kids Finds — Viral Play, Learning & Gift Ideas | QA Affiliate" · H1: "Toys & Kids" · meta: "Trending toys and kid-friendly finds — squishies, learning toys and gift ideas parents actually rebuy." · internal-link anchors (3-5): Fitness & Lifestyle (active play) · Viral & Trending · Home & Lifestyle · Fashion & Clothing (kids wear crossovers).
- **Wellness** — title: "Wellness & Personal Care — Posture, Massage & Pain-Relief Tools | QA Affiliate" · H1: "Wellness & Personal Care" · meta: "Posture correctors, massage tools, heat therapy and everyday wellness gear — practical picks with honest limitations." · internal-link anchors (3-5): Fitness & Lifestyle · Beauty & Cosmetics · Home & Lifestyle.
- **Beauty & Cosmetics (widened)** — title: "Beauty & Makeup — Best Affordable Makeup & Beauty Tools | QA Affiliate" · H1: "Beauty & Cosmetics" · meta: "Makeup, nail art and beauty tools that perform above their price — palettes, lash kits, brushes and more." · internal-link anchors (3-5): Skincare · Hair Care & Styling · Jewelry · Viral & Trending.

Internal-linking pattern (applies to every category page): breadcrumb Home → Category, 4 related-category cards at footer, and cross-links from the 4 nearest `/item/` pages' breadcrumbs — no change to existing URLs proposed anywhere in this plan.

## A4. Products with NO landing page — full inventory (post-fix state: 667) **[verified counts]**

Remaining non-landing raw values after the permitted fixes: `electronics` 525 · `toys` 95 · `health` 35 · `Phone Accessories` 3 · `Electronics` 3 · `Mobile Accessories` 3 · `toys-wellness` 2 · `Health` 1 = **667**.

### electronics — 525 products (full list; id | name)

- `daraz-real-gt1-smart-watch-smartwatch-smartwatches-` | GT1 Smart Watch – Smartwatch – smartwatches – Smart Watch for Boys – Ultra Smartwatch – Bluetooth Call, Fitness Tracker, Heart Rate Monitor, Sports Modes, Waterproof, Long Battery, Smart Watch for Boys & Men – Android & iOS Compatible – Smartwatch gift
- `daraz-real-overhead-tripod-diy-stand-scissor-arm-st` | Overhead Tripod DIY Stand Scissor Arm Stand Mobile Stand Mobile Holder Mount Flexible Table tripod Stand for Sketching Baking Vlogging Crafting Demo Videos
- `daraz-real-mini-fan-rechargeable-hand-held-electric` | Mini Fan Rechargeable Hand Held Electric Portable Mini Outdoor Desk Fan For Makeup Travel Long Battery with Adjustable Speed (Random color)
- `daraz-real-wkshop-26cm-ring-light-with-7ft-aluminiu` | WKSHOP 26cm Ring Light with 7ft Aluminium Tripod Stand Mobile Holder 3 Color Modes Dimmable LED for Makeup Video Tiktok YouTube Live Streaming Photography Selfie Studio Light
- `daraz-real-zero-luna-smart-watch` | Zero Luna Smart Watch - 1.39" TFT, Calling, 100+ Faces, IP67, SpO2 & Heart Rate
- `daraz-real-t10-ultra-smartwatch` | T10 Ultra Smartwatch 2.09" HD - Magnetic Charging, Bluetooth Call, Sleep Monitor
- `daraz-real-xiaomi-mi-band-7-amoled` | Xiaomi Mi Band 7/6/5 - AMOLED Color Screen, Bluetooth 5.0, 5ATM Fitness Band
- `daraz-real-s8-max-ultra-sim-smartwatch` | S8 Max Ultra SIM Smart Watch PTA Approved - 1.99" Display, 24 Sports Modes, Waterproof
- `daraz-real-zero-ignite-smart-watch` | Zero Ignite Smart Watch - 1.83" IPS Curved, Calling, 100+ Faces, IP67, SpO2
- `daraz-real-t800-ultra-smart-watch` | T800 Ultra Smart Watch Series 8 - 1.99" Bluetooth Call, Sleep Monitor, IP67
- `daraz-real-p9-ultra-smart-watch-multi` | P9 Ultra Smart Watch - Heart Rate, Blood Oxygen, BP, Sleep Monitor, Waterproof Fitness Tracker
- `daraz-real-t10-ultra-smartwatch-v2` | T10 Ultra Smartwatch 2.09" HD Big Screen - Magnetic Wireless Charging, Bluetooth Calling
- `daraz-real-dz09-smart-watch-sim` | DZ09 Smart Watch - SIM Supported, Calling for Men & Women
- `daraz-real-t10-ultra-smartwatch-v3` | T10 Ultra Smartwatch 2.09" HD - Magnetic Wireless Charging, Bluetooth Call, Sleep Monitor
- `daraz-real-t10-ultra-2-smartwatch` | T10 Ultra 2 Smartwatch 2.09" HD - Magnetic Wireless Charging, Bluetooth Call
- `daraz-real-y99-germany-ultra-smart-watch` | Y99 Germany Ultra Smart Watch 10+1 Bundle - 8 Straps, 2.05" Display, 200mAh
- `daraz-real-zero-elite-smart-watch-amoled` | Zero Elite Smart Watch - 2.04" AMOLED, Bluetooth 5.3, Health Monitoring, IP67
- `daraz-real-zero-bolt-pro-smart-watch` | Zero Bolt Pro Smart Watch 1.83" HD - Bluetooth Calling, 100+ Sports Modes, SpO2
- `daraz-real-t900-ultra-smartwatch` | T900 Ultra Smartwatch Series 8 - 2.09" Full Touch, Bluetooth Call, Sleep Monitor
- `daraz-real-watch-9-11-max-smartwatch` | Watch 9/10/11 Max Smartwatch - Bluetooth Calling, Wireless Charging, Full Touch
- `daraz-real-zero-qube-smartwatch` | Zero Qube Smartwatch 1.83" Fluid Display - Bluetooth Fitness Tracker, 1 Year Warranty
- `daraz-real-dt900-y60-t800-ultra-watch-bundle` | Ultra Smart Watch Bundle - DT900/Y60/T800/T900/T10 7 Straps with Earbuds, Low Rate
- `daraz-real-i8-pro-max-smart-watch` | i8 Pro Max Smart Watch Series 8 - 1.75" Full Screen, Bluetooth Call, Waterproof
- `daraz-real-bulls-i20-ultra-smart-watch` | Bulls Pvt i20 Ultra Smart Watch - 100% Original Ultra Series
- `daraz-real-samsung-galaxy-watch7-classic-47mm` | Samsung Galaxy Watch 7 Classic 47mm - Classic Style, Latest Innovation
- `daraz-real-green-laser-pointer-303` | High Power Green Laser Pointer Pen 303 - Rechargeable, Long Range
- `daraz-zero-nexus-pro-anc-earbuds` | Zero Nexus Pro Wireless ANC Earbuds Bluetooth 5.4
- `daraz-zero-wave-anc-earbuds` | Zero Wave ANC Wireless Earbuds Bluetooth 5.4 Gaming
- `daraz-zero-wave-pro-earbuds` | Zero Wave Pro Wireless Earbuds Bluetooth 5.3 Gaming
- `daraz-zero-wave-elite-earbuds` | Zero Wave Elite Wireless Earbuds Bluetooth 5.4
- `daraz-zero-flow-earbuds-150h` | Zero Flow Wireless Earbuds Bluetooth 5.4 150H Playtime
- `daraz-baseus-bowie-wm01-earbuds` | BASEUS Bowie WM01 Wireless Earbuds TWS Bluetooth 5.3
- `daraz-zero-rover-elite-earbuds` | Zero Rover Elite Wireless Earbuds Bluetooth 5.4
- `daraz-zero-aura-earbuds` | Zero Aura Wireless Earbuds Bluetooth 5.3 Gaming
- `daraz-pro2-tws-anc-earbuds` | Pro 2 TWS Wireless Bluetooth Earbuds ANC White
- `daraz-lenovo-xt88-earbuds` | Lenovo XT88 Wireless Earbuds Bluetooth 5.3 Touch Control
- `daraz-buds-3-pro-anc` | Buds 3 Pro ANC True Wireless Earbuds Gaming
- `daraz-wireless-earbuds-54-led-enc` | Wireless Earbuds 5.4 TWS Gaming LED ENC Waterproof
- `daraz-ear-hook-headphones-54-led` | Bluetooth 5.4 Ear Hook Headphones LED Display HiFi
- `daraz-tws-earbuds-2nd-gen-titanium` | TWS Wireless Earbuds 2nd Generation Titanium Bluetooth 5.0
- `daraz-wireless-earbuds-high-bass` | Wireless Earbuds Bluetooth High Bass Waterproof
- `daraz-u39-wireless-earbuds-gaming` | U39 Wireless Earbuds Gaming Beast Bluetooth 5.4 TWS
- `daraz-wireless-bt-earbuds-hd-999` | Wireless Bluetooth Earbuds HD Sound Long Battery
- `daraz-zero-bolt-pro-smartwatch` | Zero Bolt Pro Smart Watch 1.83 Inch Bluetooth Calling
- `daraz-zero-qube-smartwatch` | Zero Qube Smartwatch 1.83 Inch Fluid Display
- `daraz-i20-ultra-smartwatch` | I20 Ultra Smart Watch Fitness Tracker Bluetooth Calling
- `daraz-gt1-smartwatch` | GT1 Smart Watch Bluetooth Call Fitness Tracker Waterproof
- `daraz-d20-smartwatch-men` | D20 Bluetooth Smart Watch Waterproof Fitness Tracker
- `daraz-m3-smart-bracelet` | M3 Smart Bracelet Color Screen IP68 Fitness Tracker
- `daraz-energy-tripod-45ft` | Energy Aluminium Tripod Stand 4.5 Feet Mobile Holder
- `daraz-selfie-stick-tripod-led` | 4 in 1 Wireless Selfie Stick Tripod with LED Light Bluetooth
- `daraz-selfie-ring-light-tripod` | Selfie Ring Light 7 Feet Tripod Stand 3 Shades Adjustable
- `daraz-mini-air-cooler-fan` | Mini Air Cooler Fan Rechargeable USB with Water Mist
- `daraz-mini-handheld-fan-stand` | 2-in-1 Mini Handheld Fan with Mobile Stand USB Rechargeable
- `daraz-bladeless-neck-fan` | Portable Bladeless Neck Fan USB Rechargeable 360 Cooling
- `daraz-neck-fan-dual-head` | Neck Fan Hands Free Rechargeable Dual Adjustable Heads
- `daraz-portable-ac-mist-fan` | Portable Air Conditioner Mist Fan 3-in-1 Mini AC 10 inches
- `daraz-rechargeable-desk-fan` | Rechargeable Fan Portable Mini Desk Fan USB Battery
- `daraz-ka-mini-fan-handheld` | K.A Mini Fan Rechargeable Handheld Desktop USB Fan
- `daraz-rechargeable-mini-fan-usb` | Rechargeable Mini Fan Portable Handheld USB Charging
- `daraz-gimbal-selfie-stick-led` | 5.6ft Gimbal Selfie Stick Tripod with LED Light Bluetooth
- `aliexpress-cat-plush-phone-case` | 3D Cute Cartoon Cat Furry Plush Phone Case for iPhone
- `aliexpress-bear-plush-phone-case` | Korean 3D Cartoon Bear Fluffy Plush Couple Phone Case for iPhone
- `aliexpress-leopard-plush-phone-case` | Luxury Leopard Print Plush Phone Case for iPhone
- `aliexpress-miniso-ai-translator-earbuds` | MINISO MS190 AI Voice Translator Earbuds 135 Languages Wireless Bluetooth
- `aliexpress-htc-gaming-bluetooth-headphones` | HTC Gaming Bluetooth Headphones Microphone Translation Low Latency HiFi
- `aliexpress-htc-open-ear-sport-headset` | HTC Bluetooth Headset Open Ear Sport Running Comfort Fit HiFi Stereo
- `aliexpress-screen-auto-clicker-gadget` | Screen Auto Clicker for Smartphone Apps Live Streaming Game Gadget
- `aliexpress-smart-led-fuse-beads-set` | Smart LED Fuse Beads Pegboard Set Electronic DIY Craft Supplies
- `aliexpress-tamagotchi-smart-watch` | Tamagotchi Smart Electronic Watch Student Gift Christmas Birthday
- `temu-luxury-magnetic-metal-phone-case-iphone-17-magsafe` | Luxury Magnetic Metal Phone Case iPhone 17 MagSafe
- `temu-2-in-1-magnetic-phone-case-with-stand-magsafe` | 2-in-1 Magnetic Phone Case with Stand MagSafe
- `temu-magnetic-phone-case-black-kittens-iphone` | Magnetic Phone Case Black Kittens iPhone
- `temu-magnetic-phone-case-small-blue-iphone` | Magnetic Phone Case Small Blue iPhone
- `temu-magnetic-phone-case-kitten-balancing-iphone` | Magnetic Phone Case Kitten Balancing iPhone
- `temu-2-in-1-bear-pattern-magnetic-phone-case-with-card-holder` | 2-in-1 Bear Pattern Magnetic Phone Case with Card Holder
- `temu-luxury-magnetic-shockproof-phone-case-iphone-17` | Luxury Magnetic Shockproof Phone Case iPhone 17
- `temu-mini-portable-wireless-handheld-vacuum-cleaner` | Mini Portable Wireless Handheld Vacuum Cleaner
- `temu-55-inch-aluminum-camera-tripod-with-phone-clip` | 55 inch Aluminum Camera Tripod with Phone Clip
- `temu-10-inch-led-ring-fill-light-with-tripod-stand` | 10 inch LED Ring Fill Light with Tripod Stand
- `temu-item-picture-new-wireless-earbuds-for-running-spor` | Item Picture New Wireless Earbuds For Running Sports Wireless Earphones With Earhooks H...
- `temu-solid-long-sleeve-cable-cardigan-womens-temu-temu` | Solid Long Sleeve Cable Cardigan Womens | Temu Temu
- `temu-new-womens-pink-lazy-style-v-neck-chunky-cable` | New Womens Pink Lazy Style V Neck Chunky Cable
- `temu-hunt-usb-powered-led-strip-lights-warm-white-a-switch` | Usb Powered Led Strip Lights Warm White A Switch
- `temu-hunt-3-2ft-rgb-led-strip-lights-with-usb-cable-mini-controll` | 3.2Ft Rgb Led Strip Lights With Usb Cable & Mini Controller - Color Changing , Led Lights For Bedroo
- `temu-hunt-new-wireless-earbuds-2025-featuring-led-display-touch` | New Wireless Earbuds 2025 Featuring Led Display Touch
- `temu-hunt-wireless-earbuds-bt-headphones-35hrs-playtime` | Wireless Earbuds Bt Headphones 35Hrs Playtime
- `temu-hunt-new-wireless-earbuds-running-sports-wireless` | New Wireless Earbuds Running Sports Wireless
- `temu-hunt-wireless-earbuds-bt-5-3-headphones-35h-playtime-earphon` | Wireless Earbuds, Bt 5.3 Headphones, 35H Playtime Earphones Lcd Display Cvc 8.0 Noise Cancelling Cle
- `temu-hunt-03-wireless-earbuds-feature-an-led-display-and-a-high-c` | 03 Wireless Earbuds Feature An Led Display And A High-Capacity Charging Case, Allowing For Music . A
- `temu-hunt-new-fashionable-smartwatch-compatible-iphone-phones` | New Fashionable Smartwatch Compatible Iphone Phones
- `temu-hunt-smartwatch-wireless-calling-19-sports` | Smartwatch Wireless Calling 19 Sports
- `temu-hunt-smartwatch-pro-pantalla-completa-1-83-pulgadas-temu-spa` | Smartwatch Pro 1.83 inch Full Screen Display
- `temu-hunt-smartwatch-men-women-answer-make-calls-sleep-temu-unite` | smartwatch men women answer make calls sleep - Temu United Kingdom
- `temu-hunt-headset-wireless-headphone-hd-headphones-with-microphon` | headset wireless headphone, hd headphones with microphone | Shop On Temu And Start Saving | Temu Uni
- `temu-hunt-ear-wireless-headphones-active-noise-cancellation-built` | Ear Wireless Headphones Active Noise Cancellation Built
- `temu-women-s-premium-sequin-lace-v-neck-puff-long-sleev` | Women's Premium Sequin Lace V-Neck Puff Long Sleeve Double-Layer Ruffled
- `temu-new-wireless-earphones-headphones-led-display` | New Wireless Earphones Headphones Led Display
- `temu-wireless-earbuds-headphones` | Wireless Earbuds Headphones
- `temu-wireless-earbuds-headphones-5094` | Wireless Earbuds Headphones
- `temu-wireless-earbuds-headphones-2310` | Wireless Earbuds Headphones
- `temu-wireless-wireless-ear-headphones-noise-cancelling-40h-long` | Wireless Wireless Ear Headphones Noise Cancelling 40H Long
- `temu-smart-watch-fitness` | Smart Watch Fitness
- `temu-smart-watch-fitness-0720` | Smart Watch Fitness
- `temu-smart-watch-fitness-4193` | Smart Watch Fitness
- `temu-phone-case-accessories` | Phone Case Accessories
- `temu-phone-case-accessories-2204` | Phone Case Accessories
- `temu-phone-case-accessories-8432` | Phone Case Accessories
- `temu-phone-case-accessories-5365` | Phone Case Accessories
- `temu-phone-case-accessories-9646` | Phone Case Accessories
- `temu-phone-case-accessories-6616` | Phone Case Accessories
- `temu-mini-projector` | Mini Projector
- `temu-mini-projector-9980` | Mini Projector
- `temu-mini-projector-2326` | Mini Projector
- `temu-mini-projector-6531` | Mini Projector
- `temu-mini-projector-7751` | Mini Projector
- `temu-mini-projector-1302` | Mini Projector
- `temu-mini-projector-1605` | Mini Projector
- `temu-square-air-fryer-baking-tray-square-waffle-mold-reusable-non` | Square Air Fryer Baking Tray Square Waffle Mold Reusable Non
- `temu-30-100-pieces-non-stick-air-fryer-liners-easy` | 30 100 Pieces Non Stick Air Fryer Liners Easy
- `temu-3pcs-multifunctional-rectangular-baking-molds-cake-air-fryer` | 3Pcs Multifunctional Rectangular Baking Molds Cake Air Fryer
- `temu-smartwatch-with-full-touch-high-definition-screen-and-fitnes` | smartwatch with full touch high-definition screen and fitness - real-time activity tracking, sleep monitoring, pedometer, distance and calorie counters - suitable for and iphone smartwatches | Shop Now For Limited-time Deals | Temu
- `temu-smartwatch-fitness-tracking-device-multiple-exercise` | Smartwatch Fitness Tracking Device Multiple Exercise
- `temu-3pcs-smart-watch-set-led-screen-sports-style` | 3Pcs Smart Watch Set Led Screen Sports Style
- `temu-smart-watch-compatible-iphone-amoled-display-australia` | smart watch compatible iphone amoled display Australia
- `temu-latest-bluetooth-earbuds-high-quality-in-ear-wireless-austra` | latest bluetooth earbuds high quality in ear wireless Australia
- `temu-wireless-earbuds-compatible-wireless-stereo-headphones-deep` | Wireless Earbuds Compatible Wireless Stereo Headphones Deep
- `temu-wireless5-3-earbuds-earhook-wireless-sport-headset-tws` | Wireless5 3 Earbuds Earhook Wireless Sport Headset Tws
- `temu-new-tws-wireless-headset-earbuds-unrivalled-true` | New Tws Wireless Headset Earbuds Unrivalled True
- `temu-wireless-charger-station` | Wireless Charger Station
- `temu-wireless-charger-station-5280` | Wireless Charger Station
- `temu-wireless-charger-station-4098` | Wireless Charger Station
- `temu-wireless-charger-station-8386` | Wireless Charger Station
- `temu-wireless-charger-station-8004` | Wireless Charger Station
- `temu-wireless-charger-station-0150` | Wireless Charger Station
- `temu-portable-wireless-charger-a-foldable-stand-featuring-a` | Portable Wireless Charger A Foldable Stand Featuring A
- `temu-3000w-portable-wireless-bluetooth-speaker-sound-system-party` | 3000W Portable Wireless Bluetooth Speaker Sound System Party
- `temu-mini-portable-small-speaker-metal-heavy-small-steel` | Mini Portable Small Speaker Metal Heavy Small Steel
- `temu-portable-speaker-usb-loudspeaker-usb-high-volume-karaoke-gym` | Portable Speaker Usb Loudspeaker Usb High Volume Karaoke Gym
- `temu-bluetooth-speaker-portable` | Bluetooth Speaker Portable
- `temu-bluetooth-speakers-powerful-dual-woofer-portable` | Bluetooth Speakers Powerful Dual Woofer Portable
- `temu-bluetooth-speaker-portable-8937` | Bluetooth Speaker Portable
- `temu-go-3-portable-mini-bluetooth-speaker-big` | Go 3 Portable Mini Bluetooth Speaker Big
- `temu-ring-light-selfie` | Ring Light Selfie
- `temu-ring-light-selfie-4865` | Ring Light Selfie
- `temu-ring-light-selfie-6425` | Ring Light Selfie
- `temu-10-12-inch-led-selfie-ring-light-compatible-dual-phone` | 10 12 Inch Led Selfie Ring Light Compatible Dual Phone
- `temu-ring-light-selfie-1902` | Ring Light Selfie
- `temu-portable-usb-humidifier-featuring-a-7-color-led-night-light` | Portable Usb Humidifier Featuring A 7 Color Led Night Light
- `temu-a-usb-rechargeable-aromatherapy-humidifier-colorful-lights` | A Usb Rechargeable Aromatherapy Humidifier Colorful Lights
- `temu-single-unit-compact-humidifier-usb-powered-desktop-philippin` | single unit compact humidifier usb powered desktop Philippines
- `temu-full-smartwatch-men-women-alloy-case` | Full Smartwatch Men Women Alloy Case
- `temu-2025-new-wireless-earbuds-wireless-earphones` | 2025 New Wireless Earbuds Wireless Earphones
- `temu-wireless-earphones-hifi` | Wireless Earphones Hifi
- `temu-sized-wireless-wireless-audio-headphones24h-battery` | Sized Wireless Wireless Audio Headphones24h Battery
- `temu-portable-mini-wireless-speaker-electronics` | Portable Mini Wireless Speaker - Electronics
- `temu-s79-powerful-wireless-speaker-with-handle-hifi-rgb-light-tws` | S79 Powerful Wireless Speaker with Handle, Hifi , Rgb Light, Tws Dual Pairing, Fast Charging, Long , Playtime Loud Stereo, . Charging Cable, Connect with Mobile Phone/tablet/tv. for Halloween - Electronics
- `temu-ultra-long-smart-led-light-strips-44-keys-remote-app-voice` | Ultra Long Smart Led Light Strips 44 Keys Remote App Voice
- `temu-intelligente-led-lichtleisten-schlafzimmer-rgb-led-leuchten` | Intelligente Led Lichtleisten Schlafzimmer Rgb Led Leuchten
- `temu-modern-led-simple-luxury-long-strip-lighting` | Modern Led Simple Luxury Long Strip Lighting
- `temu-volcano-shaped-diffuser-humidifier-a-perfect-christmas` | Volcano Shaped Diffuser Humidifier a Perfect Christmas
- `temu-an-ultra-compact-massage-gun-for-deep-muscle-relief-back-and` | An Ultra-compact Massage Gun for Deep Muscle Relief, Back and Neck Relaxation - High-torque , Elegant Design - Appliances
- `temu-fascia-gun-1800mah-lithium` | Fascia Gun 1800mah Lithium
- `temu-2pcs-cell-phone-stand-desk-foldable-desktop-cute-phone-stand` | 2pcs Cell Phone Stand Desk Foldable Desktop Cute Phone Stand
- `temu-adjustable-universal-metal-phone-stand-multi-angle-desktop` | Adjustable Universal Metal Phone Stand Multi Angle Desktop
- `temu-adjustable-fold-desktop-phone-tablet-stand-universal-holder` | Adjustable Fold Desktop Phone Tablet Stand Universal Holder
- `temu-an-office-organizer-wooden-desktop-phone-stands-featuring-a` | An Office Organizer Wooden Desktop Phone Stands Featuring A
- `temu-tv-stand-mobile-phone-stand-a-thick-bathroom-tv-stand-360` | Tv Stand Mobile Phone Stand a Thick Bathroom Tv Stand 360
- `temu-rotating-universal-phone-holder-adjustable-angle-ergonomic` | Rotating Universal Phone Holder Adjustable Angle Ergonomic
- `temu-aluminum-alloy-universal-vehicle-phone-holder` | Aluminum Alloy Universal Vehicle Phone Holder
- `temu-electric-toothbrush-set-featuring-4-brush-heads` | Electric Toothbrush Set Featuring 4 Brush Heads
- `temu-electric-tooth-cleaner-led-two-replacement-heads-3` | Electric Tooth Cleaner Led Two Replacement Heads 3
- `temu-tooth-cleaning-brush-portable-electric-toothbrush-home-use` | Tooth Cleaning Brush Portable Electric Toothbrush Home Use
- `temu-spazzola-multifunzione-pulizia-e-ricarica-set-professionale` | Spazzola Multifunzione Pulizia E Ricarica Set Professionale
- `temu-usb-rechargeable-electric-toothbrush-4-nozzles-3` | Usb Rechargeable Electric Toothbrush 4 Nozzles 3
- `temu-electric-tooth-polisher-plaque-remover-suitable-teeth` | Electric Tooth Polisher Plaque Remover Suitable Teeth
- `temu-50000mah-large-capacity-fast-charging-power-bank` | 50000mah Large Capacity Fast Charging Power Bank
- `temu-portable-power-bank-20000mah-10000mah-pd20w-fast-charger-led` | Portable Power Bank 20000mah 10000mah Pd20w Fast Charger Led
- `temu-fast-charging-power-bank-22-5w-pd-fast-charging-power-bank` | Fast Charging Power Bank 22 5w Pd Fast Charging Power Bank
- `temu-10000mah-22-5w-fast-charging-power-bank-ultra-thin` | 10000mah 22 5w Fast Charging Power Bank Ultra Thin
- `temu-20000mah-portable-power-bank-22-5w-fast-charging-dual-usb` | 20000mah Portable Power Bank 22 5w Fast Charging Dual Usb
- `temu-power-bank-10000mah-22-5w-fast-charge-external-battery-porta` | Power Bank 10000mah 22.5w Fast Charge External Battery Portable Charger Power Bank for Iphone/ Xiaomi/ Samsung - Cell Phones & Accessories
- `temu-power-bank-a-capacity-30000mah-50000mah-featuring-an-led` | Power Bank a Capacity 30000mah 50000mah Featuring an Led
- `temu-38880mah-capacity-power-bank-magnetic-power-bank-wireless` | 38880mah Capacity Power Bank Magnetic Power Bank Wireless
- `temu-magnetic-powerbank-10000mah-wireless-charger` | Magnetic Powerbank 10000mah Wireless Charger
- `temu-22-5w-fast-charging-5000mah-mini-portable-power-bank-usb-c` | 22 5w Fast Charging 5000mah Mini Portable Power Bank Usb C
- `temu-phone-case-trendy-pattern-iphone-model-suitable` | Phone Case Trendy Pattern Iphone Model Suitable
- `temu-etui-na-telefon-pasuje-do-galaxy-m52-etui-ochronne` | Etui Na Telefon Pasuje Do Galaxy M52 Etui Ochronne
- `temu-10-inch-55cm-tripod-photography` | 10 Inch 55cm Tripod Photography
- `temu-ultra-thin-led-intelligent-human-body-sensing-light-strip` | Ultra Thin Led Intelligent Human Body Sensing Light Strip
- `temu-1pc-portable-mini-usb-handheld-cooling-fan-spray-function` | 1pc Portable Mini Usb Handheld Cooling Fan Spray Function
- `temu-1pc-usb-portable-fan-5-speed-270-rotation-high` | 1pc Usb Portable Fan 5 Speed 270 Rotation High
- `temu-portable-handheld-fan-compatible-usb-mini-cooling-fan` | Portable Handheld Fan Compatible Usb Mini Cooling Fan
- `temu-usb-personal-mini-air-conditioner-fan-evaporative` | Usb Personal Mini Air Conditioner Fan Evaporative
- `temu-cordless-electric-rotary-scrubber-3-adjustable` | Cordless Electric Rotary Scrubber 3 Adjustable
- `temu-scrubber-elettrico-multifunzione-pavimenti-3-7-9-testine-a` | Scrubber Elettrico Multifunzione Pavimenti 3/7/9 Testine A
- `temu-cycling-wearable-wireless-speaker-tws-mini` | Cycling Wearable Wireless Speaker Tws Mini
- `temu-tg192-a-large-capacity-2400mah-outdoor-wireless-speaker` | Tg192 A Large Capacity 2400Mah Outdoor Wireless Speaker
- `temu-30000mah-power-bank-portable-charger-dual-usb-type-c-output` | 30000mah power bank portable charger dual usb type c output Saudi Arabia
- `temu-1pc-shiatsu-foot-massager-circulation-relaxation-electric` | 1Pc Shiatsu Foot Massager Circulation Relaxation Electric
- `temu-leg-foot-massager-heat-3-intensities-3-air-compression` | Leg Foot Massager Heat 3 Intensities 3 Air Compression
- `temu-hot-compress-kneading-neck-massager-deep-tissue-4-massage-he` | Hot Compress Kneading Neck Massager Deep Tissue 4 Massage Heads Neck Massager Electric Massager Holiday Gift For Family - Beauty & Health
- `temu-usb-powered-neck-shoulder-heat-massager` | Usb Powered Neck Shoulder Heat Massager
- `temu-electric-massager-acupressure-kneading-in-a` | Electric Massager Acupressure Kneading In A
- `temu-a-neck-massager-a-hand-massage-wireless-designed-neck` | A Neck Massager A Hand Massage Wireless Designed Neck
- `temu-usb-heating-massager-device-suction-cups-usb-rechargeable-ir` | usb heating massager device suction cups usb rechargeable Ireland
- `temu-usb-rechargeable-flameless-electronic-lighter-windproof` | Usb Rechargeable Flameless Electronic Lighter Windproof
- `temu-vintage-metal-windproof-lighter-reusable` | Vintage Metal Windproof Lighter Reusable
- `temu-smart-mini-key-finder-key-finder-wireless-pet-dog` | Smart Mini Key Finder Key Finder Wireless Pet Dog
- `temu-e0c-air-suitable-christmas` | E0c Air Suitable Christmas
- `temu-2026-bladeless-portable-neck-fan-360-rotatable` | 2026 Bladeless Portable Neck Fan 360 Rotatable
- `temu-5200mah-neck-fan-portable-air-conditioning-fan-ergonomic` | 5200mah Neck Fan Portable Air Conditioning Fan Ergonomic
- `temu-3in-1-wireless-charger-iphone-foldable-charging-station` | 3in 1 Wireless Charger Iphone Foldable Charging Station
- `temu-3in-1-magnetic-wireless-charger-stand-15w-fast` | 3in 1 Magnetic Wireless Charger Stand 15w Fast
- `temu-3-in-1-phone-watch-earphone-wireless-charger-stand-suitable` | 3 in 1 Phone Watch Earphone Wireless Charger Stand Suitable
- `temu-car-phone-mount-air-vent-car-mount-anti-shake-gravity-car` | Car Phone Mount Air Vent Car Mount Anti Shake Gravity Car
- `temu-1pc-home-night-light-reading-essential-led-flat-book-light` | 1pc Home Night Light Reading Essential Led Flat Book Light
- `temu-round-led-book-clip-light-reading-desk-lamp-rechargeable` | Round Led Book Clip Light Reading Desk Lamp Rechargeable
- `temu-book-lights-reading-bed-rechargeable-book-light` | Book Lights Reading Bed Rechargeable Book Light
- `temu-reading-light-adjustable-bedside-night-light-dimmable-clip` | Reading Light Adjustable Bedside Night Light Dimmable Clip
- `temu-1pc-mini-usb-rechargeable-reading-light-portable-foldable-wa` | 1pc Mini Usb Rechargeable Reading Light - Portable Foldable, Warm & , Eye Protection, 3 Adjustable Brightness Levels, Clip-on Book Light, Space-saving Design, Ideal for Readers, Rechargeable for Reading, Work, Bedroom, Dorm Night Light - Tools & Home Improvement
- `temu-2025-newly-hd-projector-1080p-compatible-hdtv` | 2025 Newly Hd Projector 1080p Compatible Hdtv
- `temu-2026-heated-gloves-women-men-5000mah` | 2026 Heated Gloves Women Men 5000mah
- `temu-hand-warmers-rechargeable-3500mah-2-electric-hand-warmers-20` | Hand Warmers Rechargeable, 3500mah*2 Electric Hand Warmers, 20hrs Long Heat, Portable Pocket Heater,hand Warmers Great Gift for Christmas, Outdoor, Hunting, Camping,men and Women,it a Gift for Students Beginning Year. for Winter | Shop On
- `temu-2pack-rechargeable-electric-hand-warmers-charging-case` | 2pack Rechargeable Electric Hand Warmers Charging Case
- `temu-6000mah-portable-hand-warmer-20-hour-heating-usb` | 6000mah Portable Hand Warmer 20 Hour Heating Usb
- `temu-2pcs-portable-hand-warmer-rechargeable-4000mah-2-electric` | 2pcs Portable Hand Warmer Rechargeable 4000mah 2 Electric
- `temu-wireless-mouse-silent-office-rgb-backlit-battery` | Wireless Mouse Silent Office Rgb Backlit Battery
- `temu-a-universal-wireless-game-mouse-hands-rechargeable-silent` | A Universal Wireless Game Mouse Hands Rechargeable Silent
- `temu-wireless-bluetooth-charging-silent-1000hz` | Wireless Bluetooth Charging Silent 1000hz
- `temu-t-wireless-mouse-free-office-voice` | T Wireless Mouse Free Office Voice
- `temu-2-4g-bt-wireless-mouse-portable-rechargeable` | 2 4g Bt Wireless Mouse Portable Rechargeable
- `temu-ergonomic-wireless-vertical-mouse-silent-buttons-convenient` | Ergonomic Wireless Vertical Mouse Silent Buttons Convenient
- `temu-2-4g-bluetooth-wireless-mouse-silent-compatible` | 2 4g Bluetooth Wireless Mouse Silent Compatible
- `temu-lightweight-wireless-game-mouse-rgb-charging-base-third-mock` | Lightweight Wireless Game Mouse Rgb Charging Base Third Mock
- `temu-ergonomic-wireless-gaming-mouse-rechargeable-2-4g-wireless-w` | Ergonomic Wireless Gaming Mouse, Rechargeable 2.4g&wireless Wireless Mouse, Compatible with Ios/ Windows/ System, Pc Computer Laptop Desktop Tablet Gaming Office Home, Stable and Smooth, Low Latency, Portable Wireless Mouse - Electronics
- `temu-wireless-gaming-mouse-compatible-pc-laptop` | Wireless Gaming Mouse Compatible Pc Laptop
- `temu-adjustable-ergonomic-laptop-stand-compatible` | Adjustable Ergonomic Laptop Stand Compatible
- `temu-adjustable-laptop-stand-adjustable-height-ergonomic` | Adjustable Laptop Stand Adjustable Height Ergonomic
- `temu-adjustable-laptop-stand-a-portable-stand-suitable-17-3-inch` | Adjustable Laptop Stand a Portable Stand Suitable 17 3 Inch
- `temu-handmade-cable-management-box-durable-rattan-cable-organizer` | Handmade Cable Management Box Durable Rattan Cable Organizer
- `temu-desk-cable-management-tray-no-drill-metal-mesh-cable` | Desk Cable Management Tray No Drill Metal Mesh Cable
- `temu-alarm-clock-with-projection-led-display-temperature-humidity` | Alarm Clock with Projection, Led Display, Temperature & Humidity Monitoring, Usb Powered, Abs Plastic Rectangular Desk Clock with Sleep Timer, Flat , Ideal for Valentine's & New Year Gift - Home & Kitchen
- `temu-1pc-multifunctional-digital-alarm-clock-large-led-screen` | 1pc Multifunctional Digital Alarm Clock Large Led Screen
- `temu-digital-alarm-clock-colorful-led-alarm-clock-usb-battery` | Digital Alarm Clock Colorful Led Alarm Clock Usb Battery
- `temu-app-control-light-multifunctional-wireless` | App Control Light Multifunctional Wireless
- `temu-2026-new-mini-humidifier-colors-silent` | 2026 New Mini Humidifier Colors Silent
- `temu-abs-tablet-stand-foldable-height-adjustable` | Abs Tablet Stand Foldable Height Adjustable
- `temu-phone-holder-tablet-stand-desktop-support-stand-360-rotating` | Phone Holder Tablet Stand Desktop Support Stand 360 Rotating
- `temu-adjustable-clip-stand-phones-tablets-tablet-clip-support` | Adjustable Clip Stand Phones Tablets Tablet Clip Support
- `temu-30-60-100pcs-webcam-cover-camera-privacy-phone` | 30 60 100pcs Webcam Cover Camera Privacy Phone
- `temu-compact-and-handy-mini-air-conditioning-unit-designed-for-de` | Compact and Handy Mini Air Conditioning Unit, Designed for Desktop Use with Water Cooling, Ideal for Home, Office, and Room Settings, Portable ( ) | Today's Deals
- `temu-10pcs-absorventes-de-1pc-umidificador-mini` | 10pcs Absorventes De + 1pc Umidificador Mini
- `temu-2-pcs-lens-protector-compatible-iphone-11-11-pro-11-pro-max` | 2 Pcs Lens Protector Compatible Iphone 11 11 Pro 11 Pro Max
- `temu-1pc-lens-protector-iphone-17-pro-max-iphone-17` | 1pc Lens Protector Iphone 17 Pro Max Iphone 17
- `temu-phone-luxury-camera-protective-phone-case` | Phone Luxury Camera Protective Phone Case
- `temu-camera-lens-protective-film-iphone-17` | Camera Lens Protective Film Iphone 17
- `temu-full-coverage-metal-lens-film-suitable-iphone-17-pro` | Full Coverage Metal Lens Film Suitable Iphone 17 Pro
- `temu-1080p-wireless-smart-camera-artificial-intelligence-human` | 1080p Wireless Smart Camera Artificial Intelligence Human
- `temu-1920p-wireless-camera-two-way-night` | 1920p Wireless Camera Two Way Night
- `temu-mini-wireless-security-camera-2-4ghz-wifi-indoor-outdoor-use` | Mini Wireless Security Camera - 2.4ghz Wifi, Indoor/outdoor Use, App, Usb Rechargeable, Sd Card Not Included, Abs Material, 480p Resolution, Wi-fi , Rechargeable Battery, Compact Size, , Waterproo - Smart Home
- `temu-1080p-video-doorbell-night-vision-hd-cloud-storage-2-way-aud` | 1080p Video Doorbell, Night Vision, Hd , Cloud Storage, 2 Way Audio, Security Camera for Home, with App | Shop On
- `temu-smart-visual-doorbell-camera-front-door-monitoring-2-4g-wifi` | Smart Visual Doorbell Camera Front Door Monitoring 2 4g Wifi
- `temu-wireless-mini-camera-audio-video-camera` | Wireless Mini Camera Audio Video Camera
- `temu-portable-rechargeable-lint-remover-cleaning-brush-effective` | Portable Rechargeable Lint Remover Cleaning Brush Effective
- `temu-mini-fridge-bedroom-skincare-led` | Mini Fridge Bedroom Skincare Led
- `temu-15l-22l-15-8qt-23-3qt-mini-fridge-bedroom-car-office` | 15l 22l 15 8qt 23 3qt Mini Fridge Bedroom Car Office
- `temu-6-refrigerator-car-household-dual-use-mini-fridge-refrigerat` | 6 Refrigerator, Car Household Dual-use Mini Fridge, Refrigerator, Lightweight Design, Meeting the Needs of Commuting, Travel, and Home Scenes, , and Energy-saving - Appliances
- `temu-portable-mini-fridge-6-capacity-freon-free` | Portable Mini Fridge 6 Capacity Freon Free
- `temu-10l-digital-mini-fridge-thermoelectric-car-cooler` | 10l Digital Mini Fridge Thermoelectric Car Cooler
- `temu-compact-fridge-versatile-use-portable-suitable` | Compact Fridge Versatile Use Portable Suitable
- `temu-130-25-50-100-ft-40-7-5-meter-led-strip-lights-smart` | 130 25 50 100 Ft 40 7 5 Meter Led Strip Lights Smart
- `temu-usb-powered-led-strip-lights-home-decoration-bedroom` | Usb Powered Led Strip Lights Home Decoration Bedroom
- `temu-flexible-car-interior-led-strip-lights-5m-196-85inch-usb` | Flexible Car Interior Led Strip Lights 5M 196 85Inch Usb
- `temu-lqhzmyy-3aa-battery-powered-cob-led-strip-warm` | Lqhzmyy 3Aa Battery Powered Cob Led Strip Warm
- `temu-1m-30-led-strip-light-room-decor-remote-app-control` | 1M 30 Led Strip Light Room Decor Remote App Control
- `temu-lqhzmyy-5v-led-diy-strip-light-rgb-scenes-double` | Lqhzmyy 5V Led Diy Strip Light Rgb Scenes Double
- `temu-diy-neon-led-strip-light-warm-white-usb-powered-light-strip` | Diy Neon Led Strip Light Warm White Usb Powered Light Strip
- `temu-usb-powered-led-strip-control-dimmable-function` | Usb Powered Led Strip Control Dimmable Function
- `temu-new-wireless-earbuds-active-noise-cancellation-calls-ultra` | New Wireless Earbuds Active Noise Cancellation Calls Ultra
- `temu-buds-wireless-in-ear-headphones-360` | Buds Wireless In Ear Headphones 360
- `temu-c-for-direct-mobile-phone-insertion-phone-no-conversion-need` | c for direct mobile phone insertion, phone no conversion needed, easy external listening, ergonomic design more stylish, with multiple colors | Shop Trends | Temu
- `temu-wireless-earbuds-a-stylish-design-featuring-detachable` | Wireless Earbuds A Stylish Design Featuring Detachable
- `temu-new-wireless-earbuds-high-fidelity-stereo-earphones-in-ear` | New Wireless Earbuds High Fidelity Stereo Earphones In Ear
- `temu-true-wireless-bluetooth-headphones-microphone-in-ear` | True Wireless Bluetooth Headphones Microphone In Ear
- `temu-wireless-headphones-wireless-earbuds` | Wireless Headphones Wireless Earbuds
- `temu-true-wireless-clip-sports-earphones-tws-hifi-stereo-hd` | True Wireless Clip Sports Earphones Tws Hifi Stereo Hd
- `temu-bezprzewodowe-s-uchawki-bezprzewodowe-s-uchawki` | Bezprzewodowe Słuchawki Bezprzewodowe Słuchawki
- `temu-valentines-day-gift-smartwatch-women-men-wireless` | Valentines Day Gift Smartwatch Women Men Wireless
- `temu-ceas-smart-elegant-pentru-femei-hd-de-1-27-inch` | Ceas Smart Elegant Pentru Femei Hd De 1 27 Inch
- `temu-new-smart-watch-1-83-inch-wireless-call-sedentary` | New Smart Watch 1 83 Inch Wireless Call Sedentary
- `temu-smartwatch-designed-for-women-and-men-allowing-to-answer-and` | smartwatch designed for women and men, allowing to answer and make calls, text replies, and features. compatible with iphone, samsung, and devices, it functions as | Check Out Today's Deals Now | Temu
- `temu-womens-watch-a-1-84-inch-touchscreen-classic-strap-featuring` | Womens Watch A 1 84 Inch Touchscreen Classic Strap Featuring
- `temu-smart-watch-with-1-39-full-smartwatch-and-100-exercise-sport` | smart watch with 1.39 full smartwatch and 100+ exercise sports , weather, music controls, fitness body monitoring watches | Free Shipping On Items Shipped From Temu | Temu Saudi Arabia
- `temu-smart-watch-1-83-full-display-message-answer` | Smart Watch 1 83 Full Display Message Answer
- `temu-new-smartwatch-men-women-valentines-day-gift-wireless` | New Smartwatch Men Women Valentines Day Gift Wireless
- `temu-60w-fast-charging-cable-iphone-17-usb-c-usb-c-charger-cord` | 60W Fast Charging Cable Iphone 17 Usb C Usb C Charger Cord
- `temu-high-speed-micro-usb-charging-cable-universal` | High Speed Micro Usb Charging Cable Universal
- `temu-1-2-3-5pcs-0-3-type-c-phone-charger-cable-camera` | 1 2 3 5Pcs 0 3 Type C Phone Charger Cable Camera
- `temu-original-pd-60w-fast-charger-usb-c-c-type-cable-suitable` | Original Pd 60W Fast Charger Usb C C Type Cable Suitable
- `temu-type-c-hurtigladekabel-usb-c-telefonladekabel-for-rask` | Type C Hurtigladekabel Usb C Telefonladekabel For Rask
- `temu-charging-cable-2-4a-iphone-charger` | Charging Cable 2 4A Iphone Charger
- `temu-type-c-charger-fast-charging-right-angle-usb-usb-c` | Type C Charger Fast Charging Right Angle Usb Usb C
- `temu-universal-201-17cm-usb-c-charger-cable-with-adapter-for-ipho` | Universal 201.17Cm Usb-C Charger Cable With Adapter For Iphone 16/15/Plus/Pro Max, Ipad 12.9/11/10/Mini - Fast Charging, 5-10W Output, 110V/220V Compatible, European Standard Plug, Travel Charging Solution| |Durable Cable, Charging Cable - Cell Phones & Accessories
- `temu-240w-usb-a-type-c-fast-charging-cable-led-display-iphone-17` | 240W Usb A Type C Fast Charging Cable Led Display Iphone 17
- `temu-240w-fast-charging-type-c-type-c-lanyard-data-cable-supports` | 240W Fast Charging Type C Type C Lanyard Data Cable Supports
- `temu-usb-a-charger-cable-14-13-12-11-xs` | Usb A Charger Cable 14 13 12 11 Xs
- `temu-5-cartoon-lightning-charger-protector-sleeves` | 5 Cartoon Lightning Charger Protector Sleeves
- `temu-offered-in-lengths-1-meter-2-meters-3-meters` | Offered In Lengths 1 Meter 2 Meters 3 Meters
- `temu-usb-c-cable-usb-c-charger-cable-mobile-phones` | Usb C Cable Usb C Charger Cable Mobile Phones
- `temu-fast-charging-micro-usb-cable-nylon-braided-data-cable` | Fast Charging Micro Usb Cable Nylon Braided Data Cable
- `temu-1pc-2pcs-22-5cm-8-86inch-fashion-bracelet-charger-cable` | 1Pc 2Pcs 22 5Cm 8 86Inch Fashion Bracelet Charger Cable
- `temu-travel-electronics-organizer-portable-cable-charger-storage` | travel electronics organizer portable cable charger storage
- `temu-10pcs-adjustable-magnetic-cable-clips-durable-abs-resin-wire` | 10pcs adjustable magnetic cable clips durable abs resin wire
- `temu-1pc-25w-rv-fast-charging-port-usb-hub-4-usb-a-4` | 1pc 25w rv fast charging port usb hub 4 usb a 4
- `temu-1pc-0hub-extender-3-port-expansion-usb-splitter-usb` | 1pc 0hub extender 3 port expansion usb splitter usb
- `temu-2-4ghz-wireless-mouse-optical-mice-mouse-gaming-usb-receiver` | 2 4ghz wireless mouse optical mice mouse gaming usb receiver
- `temu-ultra-portable-rechargeable-wireless-keyboard` | ultra portable rechargeable wireless keyboard
- `temu-portable-speaker-wireless-30h-playtime-24w-hi-fi` | portable speaker wireless 30h playtime 24w hi fi
- `temu-100-50-20-bulbs-smart-fairy-light-solar-powered-bubble-ball` | 100 50 20 bulbs smart fairy light solar powered bubble ball
- `temu-set-2-wireless-lights-remote-control-rechargeable` | set 2 wireless lights remote control rechargeable
- `temu-17-in-1-power-strip-protector-outlets-4usb-2type` | 17 in 1 power strip protector outlets 4usb 2type
- `temu-car-vacuum-portable-23000pa-high-power-handheld-vacuum` | car vacuum portable 23000pa high power handheld vacuum
- `temu-4-channel-car-dash-cam-1080p-front-720p-rear-led` | 4 channel car dash cam 1080p front 720p rear led
- `temu-solar-powered-magnetic-camera-for-car-truck-dash-cam-wifi-reversing-ba` | solar powered magnetic camera for car truck dash cam wifi reversing backup system - 1 x wireless camera 1 x charging cable - automotive
- `temu-portable-usb-water-flosser-oral-irrigator-usb-odor` | portable usb water flosser oral irrigator usb odor
- `temu-portable-electric-water-flosser-rechargeable-oral-irrigator` | portable electric water flosser rechargeable oral irrigator
- `temu-40000mah-capacity-mobile-power-portable-charger-pd-20w` | 40000Mah Capacity Mobile Power Portable Charger Pd 20W
- `temu-10000mah-power-bank-battery-pack-portable-charger-travel` | 10000Mah Power Bank Battery Pack Portable Charger Travel
- `temu-5000mah-ultra-thin-power-bank-portable-charger-dual-usb` | 5000Mah Ultra Thin Power Bank Portable Charger Dual Usb
- `temu-mini-portable-charger-for-iphone-6000mah-power-bank-battery` | Mini Portable Charger For Iphone, 6000Mah Power Bank Battery Pack, Ultra-Compact Battery Pack, Compatible Portable Charging Bank With Other Lightning Phones/Devices - Cell Phones & Accessories
- `temu-power-bank-30000mah-portable-power-bank-usb-c-fast-charger-s` | power bank 30000mah portable power bank, usb-c fast charger, suitable for mobile phones compatible with iphone, samsung, tablet mini, ., support huawei, suitable for outdoor use, travel, office work, home, live broadcast | Shop Trends | Temu Australia
- `temu-10-000mah-mobile-phone-power-bank-charger-2-4a-9347` | 10 000Mah Mobile Phone Power Bank Charger 2 4A
- `temu-bo-tier-charge-stockage-batterie-18650-piles` | Boîtier Charge Stockage Batterie 18650 Piles
- `temu-portable-charger-22-5w-10000-20000mah-usb-c-power-bank-fast` | Portable Charger, 22.5W 10000/20000Mah Usb C Power Bank Fast Charging, Pd 3.0+Qc 4.0 Led Display Phone Battery Pack Compatible With Iphone 15/14/13/12 Pro, For Samsung S21, For Google/Ipad Tablet, Etc - Cell Phones & Accessories
- `temu-40000mah-mini-cute-5v2a-fast-charging-multifunctional-power` | 40000Mah Mini Cute 5V2A Fast Charging Multifunctional Power
- `temu-a-portable-power-bank-a-capacity-4500mah-featuring-a` | A Portable Power Bank A Capacity 4500Mah Featuring A
- `temu-speakers-portable-small-steel-gun-metal` | Speakers Portable Small Steel Gun Metal
- `temu-portable-wireless-speaker-rugged` | Portable Wireless Speaker Rugged
- `temu-wireless-mini-speaker-portable-bt5-4-speaker-hi-fi-stereo` | Wireless Mini Speaker Portable Bt5 4 Speaker Hi Fi Stereo
- `temu-official-led-wireless-bluetooth-microphone-speaker` | Official Led Wireless Bluetooth Microphone Speaker
- `temu-portable-wireless-speaker-wireless-dual` | Portable Wireless Speaker Wireless Dual
- `temu-wireless-mini-speaker-rechargeable-portable` | Wireless Mini Speaker Rechargeable Portable
- `temu-portable-8000w-wireless-bluetooth-speaker` | Portable 8000W Wireless Bluetooth Speaker
- `temu-led-light-up-bt-wireless-speaker-fm-radio-usb-tf-mp3-tws-pai` | led light-up bt wireless speaker | fm radio, usb/tf mp3 , tws pairing, rechargeable battery, fun party & for adults, teen, outdoor | Today's Deals | Temu
- `temu-portable-wireless-speaker-a-microphone-a-subwoofer-featuring` | Portable Wireless Speaker A Microphone A Subwoofer Featuring
- `temu-altavoz-port-til-alaxe-altavoz-inal-mbrico` | Altavoz Portátil Alaxe Altavoz Inalámbrico.
- `temu-vanity-mirror-lights-smart-touch-control-3-colors-adjustable` | Vanity Mirror Lights Smart Touch Control 3 Colors Adjustable
- `temu-illuminated-makeup-light-features-3-color-lighting` | Illuminated Makeup Light Features 3 Color Lighting
- `temu-three-adjustable-led-lights-a-gift-for-women-a-birthday-pres` | three adjustable led lights, a gift for women, a birthday present, a white makeup vanity featuring a and dimmable light, a makeup vanity accompanied chair and a storage drawer for , along with a stool | Shop On Temu And Start Saving | Temu United Kingdom
- `temu-1pc-adjustable-phone-stand-holder-abs-material-foldable` | 1Pc Adjustable Phone Stand Holder Abs Material Foldable
- `temu-mobile-phone-stand-adjustable-foldable-holder` | Mobile Phone Stand Adjustable Foldable Holder
- `temu-a-creative-wooden-desktop-phone-stand-a-stable-rotatable` | A Creative Wooden Desktop Phone Stand A Stable Rotatable
- `temu-foldable-cell-phone-stand-desk-fully-adjustable-phone-holder` | Foldable Cell Phone Stand Desk Fully Adjustable Phone Holder
- `temu-new-portable-mobile-phone-stand-with-vacuum-magnetic-base-fe` | new portable mobile phone stand with vacuum magnetic base, featuring - suction that won't come off , suitable for office desks, gym use, bathrooms, kitchens, and car dashboard navigation | Shop Now For Limited-time Deals | Temu
- `temu-universal-metal-phone-tablet-stand-adjustable-flexible` | Universal Metal Phone Tablet Stand Adjustable Flexible
- `temu-mobile-phone-stand-set-2-3-phone-stand-desktop` | Mobile Phone Stand Set 2 3 Phone Stand Desktop
- `temu-universal-phone-holder-suitable-bedside-table-gooseneck` | Universal Phone Holder Suitable Bedside Table Gooseneck
- `temu-a-desktop-phone-stand-lazy-live-streaming-adjustable` | A Desktop Phone Stand Lazy Live Streaming Adjustable
- `temu-phone-screen-magnifier-stand-instantly-turns-phone-a-tablet` | Phone Screen Magnifier Stand Instantly Turns Phone A Tablet
- `temu-1pc-universal-car-mobile-phone-holder-360-rotation-car` | 1Pc Universal Car Mobile Phone Holder 360 Rotation Car
- `temu-car-dashboard-phone-holder-adjustable-in-vertical-and-horizo` | Car Dashboard Phone Holder, Adjustable In Vertical And Horizontal Directions, High Stability And Strong , Bonus Pads, Car Phone Holder Mount Compatible With All Phones - Automotive
- `temu-automotive-universal-phone-holder-15w-fast-charging-wireless` | Automotive Universal Phone Holder 15W Fast Charging Wireless
- `temu-universal-4-13-car-cup-holder-mount-stable-adjustable-mobile` | Universal 4 13 Car Cup Holder Mount Stable Adjustable Mobile
- `temu-1-magnetic-car-phone-holder-detachable-flexible-aluminum-arm` | 1 Magnetic Car Phone Holder Detachable Flexible Aluminum Arm
- `temu-a-universal-mobile-phone-holder-made-pvc-car-dashboards` | A Universal Mobile Phone Holder Made Pvc Car Dashboards
- `temu-magnetic-mobile-phone-holder-extendable-and-foldable-360-deg` | Magnetic Mobile Phone Holder, Extendable And Foldable, 360-Degree Rotatable, Motor Vacuum Adsorption Car Mobile Phone Holder, Super Strong Suction, Small And Lightweight Design, Suitable For Car/Indoor/Gym/Travel/Bathroom And Smooth Glass , Suitable For Iphone16/15/14/13/12 Compatible With All Smartphones - Cell Phones & Accessories
- `temu-a-car-headrest-rotating-mount-tablet-holder-phone-stand-rear` | A Car Headrest Rotating Mount | Tablet Holder, Phone Stand, Rear Seat Entertainment Rack, Headrest Hook, Multifunctional Fastener | 360° Omnidirectional Rotation, | Adjustable From 12 To 32 Cm | Ideal For Long Trips, Family , And Business Vehicles | A Must-Have For Travel, Perfect As A Holiday Gift - Automotive
- `temu-metal-magnetic-car-mobile-phone-holder-folding-magnet-cell` | Metal Magnetic Car Mobile Phone Holder Folding Magnet Cell
- `temu-a-multifunctional-car-phone-holder-degrees` | A Multifunctional Car Phone Holder Degrees
- `temu-car-suction-cup-tablet-holder-phone-mount-car-base` | Car Suction Cup Tablet Holder Phone Mount Car Base
- `temu-1-set-car-phone-holder-suitablefor-b-a` | 1 Set Car Phone Holder Suitablefor B A
- `temu-upgrade-a-car-phone-holder-compatible` | Upgrade A Car Phone Holder Compatible
- `temu-1pc-magnetic-car-phone-holder-adjustable-rotating-dual-sided` | 1Pc Magnetic Car Phone Holder Adjustable Rotating Dual Sided
- `temu-adjustable-magnetic-car-phone-holder-sturdy-multi-angle` | Adjustable Magnetic Car Phone Holder Sturdy Multi Angle
- `temu-upgrade-car-magnetic-phone-holder-suitable-iphone-xiaomi` | Upgrade Car Magnetic Phone Holder Suitable Iphone Xiaomi
- `temu-1pc-universal-360-rotating-car-phone-holder` | 1Pc Universal 360 Rotating Car Phone Holder
- `temu-live-tripod-360-extendable-mobile-phone-metal-stand-foldable` | Live Tripod 360 Extendable Mobile Phone Metal Stand Foldable
- `temu-selfie-light-phone-light-clip-2200mah-usb` | Selfie Light Phone Light Clip 2200Mah Usb
- `temu-1pc-usb-rechargeable-portable-360-rotating-tower-fan-led` | 1Pc Usb Rechargeable Portable 360 Rotating Tower Fan Led
- `temu-portable-usb-desktop-fan-3000-mah-battery-5` | Portable Usb Desktop Fan 3000 Mah Battery 5
- `temu-mini-b-rbar-vifte-h-ndholdt-vifte-personlig-minivifte-usb-op` | mini bærbar vifte, håndholdt vifte personlig minivifte usb oppladbar med 5 hastigheter, 90° sammenleggbar batteridrevet minivifte med led-skjerm, skrivebordsvifte arbeidstid for kontor soverom utendørs reise camping tilbake til rekvisita | Rask Og Utsjekking På | Temu
- `temu-portable-air-conditioner-fan-usb-rechargeable-fan-5-speed` | Portable Air Conditioner Fan Usb Rechargeable Fan 5 Speed
- `temu-ventilatore-portatile-usb-a-ricarica-batteria-a` | Ventilatore Portatile Usb A Ricarica Batteria A
- `temu-single-pack-handheld-turbo-fan-usb-rechargeable-led-display` | Single Pack Handheld Turbo Fan Usb Rechargeable Led Display
- `temu-1pc-compact-usb-rechargeable-minimalist-wall-mounted-mini-fa` | 1Pc Compact Usb-Rechargeable Minimalist Wall Mounted Mini Fan With Three Adjustable Suitable For Multifunctional Portable Handheld For And Outdoor Exploration - Jewelry & Accessories
- `temu-a-versatile-portable-fan-combines-mobile-power-usb-charging` | A Versatile Portable Fan Combines Mobile Power Usb Charging
- `temu-5200mah-rechargeable-handheld-portable-fan-100-speed` | 5200Mah Rechargeable Handheld Portable Fan 100 Speed
- `temu-fashion-usb-charging-fan-night-light-100` | Fashion Usb Charging Fan Night Light 100
- `temu-high-speed-portable-handheld-fan-rechargeable-usb-fan` | High Speed Portable Handheld Fan Rechargeable Usb Fan
- `temu-outdoor-camping-fan-tent-ceiling-fan-lighting-large-capacity` | Outdoor Camping Fan Tent Ceiling Fan Lighting Large Capacity
- `temu-usb-quiet-cooling-fan-with-detachable-base-wall-mount-usb-re` | Usb- Quiet Cooling Fan With Detachable Base & Wall-Mount - Usb Rechargeable - Desktop Fan, 3-Speed , 360° Tilt, Low Voltage For /, For Home/Office/Bedroom (Black/Purple /Golden) - Appliances
- `temu-portable-9-rechargeable-oscillating-fan-8000mah-battery-usb` | Portable 9 Rechargeable Oscillating Fan 8000Mah Battery Usb
- `temu-storm-outdoor-fan-30ft-cold-wind-20000mah-battery-led` | Storm Outdoor Fan 30Ft Cold Wind 20000Mah Battery Led
- `temu-portable-usb-charging-mini-desktop-fan-a-u-shaped-base` | Portable Usb Charging Mini Desktop Fan A U Shaped Base
- `temu-3-cordless-battery-powered-portable-fan-with-powerbank-10000` | 3 Cordless Battery Powered Portable Fan With Powerbank, 10000Mah Rechargeable Solar Camping Fan With Led Lantern, Quiet Desk Fan For Tent Hurricane - Appliances
- `temu-multi-portable-handheld-usb-charging-octopus-fan-an` | Multi Portable Handheld Usb Charging Octopus Fan An
- `temu-versatile-2000mah-rechargeable-fan-features` | Versatile 2000Mah Rechargeable Fan Features
- `temu-portable-handheld-turbo-fan-fast-cooling-46-f-usb` | Portable Handheld Turbo Fan Fast Cooling 46 F Usb
- `temu-2-4ghz-wireless-gaming-mouse-with-usb-receiver-comfortable-t` | 2.4ghz wireless gaming mouse with usb receiver, comfortable touch , curved surface design that fits against , suitable for gaming, office and entertainment, portable computer mouse | Shop Trends | Temu
- `temu-wireless-bt-mouse-2-4-ghz-type-c-wired-third` | Wireless Bt Mouse 2 4 Ghz Type C Wired Third
- `temu-wireless-gaming-mouse-a-2-4ghz-connection-usb-receiver` | Wireless Gaming Mouse A 2 4Ghz Connection Usb Receiver
- `temu-1-set-11-drawers-12-led-lights-makeup-vanity-table-set-chair` | 1 Set 11 Drawers 12 Led Lights Makeup Vanity Table Set Chair
- `temu-makeup-vanity-3-color-dimmable-large-vanity-desk-side-glass` | Makeup Vanity 3 Color Dimmable Large Vanity Desk Side Glass
- `temu-makeup-vanity-desk-large-led-charging-station-makeup` | Makeup Vanity Desk Large Led Charging Station Makeup
- `temu-vanity-desk-makeup-vanity-desk-sliding-mirror-lights-makeup` | Vanity Desk Makeup Vanity Desk Sliding Mirror Lights Makeup
- `temu-vanity-desk-lights-makeup-vanity-lights-large-vanity` | Vanity Desk Lights Makeup Vanity Lights Large Vanity
- `temu-vanity-desk-set-lights-white-vanity-table-stool-7` | Vanity Desk Set Lights White Vanity Table Stool 7
- `temu-productos-point-temu` | PRODUCTOS_ | _POINT | temu
- `temu-new-mini-micro-projector-with-360-rotation-1080p-home-theate` | new mini micro projector with 360° rotation, 1080p home theater video projector, supporting 1920*1080p video , 15.75inch projection distance, screen mirroring with iphone, | Shop Trends | Temu
- `temu-professional-mini-projector-suitable-home-outdoor` | Professional Mini Projector Suitable Home Outdoor
- `temu-mini-portable-projector-supports-smartphone-wired-screen` | Mini Portable Projector Supports Smartphone Wired Screen
- `temu-home-theater-projector-hd-portable-projector-usb-plug-in-sup` | home theater projector, , hd portable projector, usb plug-in, supports phone, tv, computer, tablet connection, suitable for scenes, with hdtv hd interface | Check Out Today's Deals Now | Temu Georgia
- `temu-1x-pro-mini-portable-projector-11-0-os-4k` | 1X Pro Mini Portable Projector 11 0 Os 4K
- `temu-built-in-apps-2026-mini-portable-smart-projector` | Built In Apps 2026 Mini Portable Smart Projector
- `temu-mini-portable-projector-portable-video-projector-full-hd-4k` | Mini Portable Projector Portable Video Projector Full Hd 4K
- `temu-pro-portable-mini-projector-4k-1080p-hd-dual-band-wifi6-bt5` | pro portable mini projector - 4k & 1080p hd, dual band wifi6 bt5.0 11.0, ° rotatable, auto keystone correction, 40"-130" screen projection, compact home theater projector for smartphones, tablets & laptops | High-quality & Affordable | Temu Canada
- `temu-mini-projector-us-plug-projection-portable-home-outdoor-thea` | mini projector us plug projection, portable home outdoor theater ° projection angle adjustable, compatible with usb/sd/av suitable for birthday gifts, christmas, halloween, thanksgiving gifts | Check Out Today's Deals Now | Temu
- `temu-portable-mini-projector-compatible-ios-windows` | Portable Mini Projector Compatible Ios Windows
- `temu-de-productos-gato` | _De Productos - _Gato
- `temu-graffiti-smart-wifi-holder-e26-e27-ac110v-220v` | Graffiti Smart Wifi Holder E26 E27 Ac110V 220V
- `temu-wi-fi-repeater-home-network-booster-wifi6-system-plug` | Wi Fi Repeater Home Network Booster Wifi6 System Plug
- `temu-10-1-inch-silvery-tablet-13-64gb-rom-6gb` | 10 1 Inch Silvery Tablet 13 64Gb Rom 6Gb
- `temu-keyboard-mouse-sets-color-matching-wireless` | Keyboard Mouse Sets Color Matching Wireless
- `temu-wireless-keyboard-mouse-silent-keyboard-mouse-combo-full` | Wireless Keyboard Mouse Silent Keyboard Mouse Combo Full
- `temu-ultra-portable-wireless-keyboard-mouse-combo-suitable` | Ultra Portable Wireless Keyboard Mouse Combo Suitable
- `temu-combo-full-sized-ergonomic-computer-keyboard-with-phone-tabl` | Combo, Full-Sized Ergonomic Computer Keyboard With Phone Tablet Holder, 2.4Ghz Silent Cordless Keyboard Mouse Set For Windows Laptop, Pc, Desktop - Electronics
- `temu-wireless-foldable-keyboard-set-mouse-64-silent-keys` | Wireless Foldable Keyboard Set Mouse 64 Silent Keys
- `temu-wired-illuminated-keyboard-mouse-set-gaming-computer-desktop` | Wired Illuminated Keyboard Mouse Set Gaming Computer Desktop
- `temu-random-thickened-reinforced-folding-umbrella-windproof-ultra` | random thickened reinforced folding umbrella windproof ultra
- `temu-2026-smart-rings-men-women-health-monitoring-ring` | 2026 smart rings men women health monitoring ring
- `temu-smart-ring-sleep-tracking-wearable-activity-fitness` | smart ring sleep tracking wearable activity fitness
- `temu-2025-smart-ring-women-men-ring-ip68` | 2025 smart ring women men ring ip68
- `temu-portable-handheld-ice-mouse-fan-semiconductor-cooling-3` | portable handheld ice mouse fan semiconductor cooling 3
- `temu-starry-sky-projector-led-star-projector` | starry sky projector led star projector
- `temu-projection-light-led-nebula-effect-lighting-device-powered` | projection light led nebula effect lighting device powered
- `temu-packing-organizers-luggage-organizers-suitable` | packing organizers luggage organizers suitable
- `temu-2pcs-car-seat-filler-set-leak-proof-anti-fall-car` | 2pcs car seat filler set leak proof anti fall car
- `temu-phone-case-chic-note-10s-lanyard-design` | phone case chic note 10s lanyard design
- `temu-phone-case-2-set-1-case-1-lanyard-luxury-cowboy-pattern` | phone case 2 set 1 case 1 lanyard luxury cowboy pattern
- `temu-phone-around-protective-magnetic-metal` | phone around protective magnetic metal
- `temu-phone-ring-holder-stand-diamond-transparent-finger` | phone ring holder stand diamond transparent finger
- `temu-phone-case-luxury-shockproof-magnetic-ring` | phone case luxury shockproof magnetic ring
- `temu-suction-cup-holder-mobile-phone-case-protective-case` | suction cup holder mobile phone case protective case
- `temu-floating-phone-pouch-strap-universal-case-iphone-15-pro-max` | floating phone pouch strap universal case iphone 15 pro max
- `temu-14-inch-screen-enhancer-1-1-coaxial-amplifier` | 14 inch screen enhancer 1 1 coaxial amplifier
- `temu-1pc-star-projector-light-ceiling` | 1pc star projector light ceiling
- `temu-projector-13-in-1-hd-planetarium-star` | projector 13 in 1 hd planetarium star
- `temu-instant-print-portable-printer-prints-pictures-take` | instant print portable printer prints pictures take
- `temu-kids-camera-instant-print-christmas-birthday-gifts` | kids camera instant print christmas birthday gifts
- `temu-pm-241-wireless-shipping-label-printer-designed-small` | pm 241 wireless shipping label printer designed small
- `temu-professional-wall-scanning-instrument-high-definition-lcd` | professional wall scanning instrument high definition lcd
- `temu-2-3-5-7pcs-mini-keychain-flashlight-1200lm-bright-led` | 2 3 5 7pcs mini keychain flashlight 1200lm bright led
- `temu-laptop-stand-height-adjustable-stand-cooling-support-10-17` | laptop stand height adjustable stand cooling support 10 17
- `temu-ultra-thin-wireless-sleep-earbuds-invisible-earphones-bt5-3` | ultra thin wireless sleep earbuds invisible earphones bt5 3
- `temu-phone-case-merry-christmas-raccoon-cute` | phone case merry christmas raccoon cute
- `temu-watercolor-pattern-phone-case-compatible-iphone-17` | watercolor pattern phone case compatible iphone 17
- `temu-luxury-diamond-winter-warm-handmade-soft-fur-fluffy-plush` | luxury diamond winter warm handmade soft fur fluffy plush
- `temu-chain-phone-case-iphone14-14plus-14pro-14pro-max` | chain phone case iphone14 14plus 14pro 14pro max
- `temu-1-pack-compatible-for-3rd-gen-case-with-keychain-shockproof-cover-soft` | 1 pack compatible for 3rd gen case with keychain & shockproof cover - soft protective cover compatible for 3, wireless charging, front display window, scratch/drop - electronics
- `temu-professional-portable-earbud-holder-lightweight-silicone` | professional portable earbud holder lightweight silicone
- `temu-premium-silicone-bands-watch-38mm-40mm-42mm-44mm-45mm` | premium silicone bands watch 38mm 40mm 42mm 44mm 45mm
- `temu-magnetic-loop-strap-watch-series-11-bands-in` | magnetic loop strap watch series 11 bands in
- `temu-case-band-set-watch-42mm-46mm-45mm-41mm-44mm-40mm` | case band set watch 42mm 46mm 45mm 41mm 44mm 40mm
- `temu-cinturino-in-tessuto-nylon-watch-serie-10-46mm` | cinturino in tessuto nylon watch serie 10 46mm/
- `temu-stainless-iwatch-band-42mm-46mm-49mm-45mm-44mm` | stainless iwatch band 42mm 46mm 49mm 45mm 44mm
- `temu-a-mandala-flower-engraved-printed-watch-band-suitable` | a mandala flower engraved printed watch band suitable
- `temu-extra-large-waterproof-mouse-pad-faux-leather-rectangular` | extra large waterproof mouse pad faux leather rectangular
- `temu-a-small-desk-lamp-a-clip-suitable-reading-featuring-a` | a small desk lamp a clip suitable reading featuring a
- `temu-a-white-led-clip-reading-lamp-three-color-temperatures` | a white led clip reading lamp three color temperatures
- `temu-set-2-touch-control-table-lamp-2-usb-ports-3-way-dimmable` | set 2 touch control table lamp 2 usb ports 3 way dimmable
- `temu-12-filmdiscs-multicolor-led-astronaut-projector-powered` | 12 filmdiscs multicolor led astronaut projector powered
- `temu-super-dual-4-inch-outdoor-speakers-led-lights` | super dual 4 inch outdoor speakers led lights
- `temu-sound-bar-subwoofer-soundbar-smart-tv-wireless-speaker-deep` | sound bar subwoofer soundbar smart tv wireless speaker deep
- `temu-tv-stand-featuring-led-lighting-160cm-contemporary` | tv stand featuring led lighting 160cm contemporary
- `temu-10000mah-portable-solar-external` | 10000mah portable solar external
- `temu-solar-charger-10000mah-solar-mobile-power-bank-external` | solar charger 10000mah solar mobile power bank external
- `temu-batterie-externe-solaire-10000-20000mah-batterie` | batterie externe solaire 10000/20000mah batterie
- `temu-portable-66w-120-fast-charger-retractable-cable` | portable 66w 120 fast charger retractable cable
- `temu-w-o-retractable-gan-120w-fast-charger-dual-120cm-47inch` | w o retractable gan 120w fast charger dual 120cm 47inch
- `temu-1-2pcs-retractable-charging-cord-3in-1-multiple` | 1 2pcs retractable charging cord 3in 1 multiple
- `temu-usb-3-0-fast-car-charger-type-c-port-led-digital-voltmeter` | usb 3 0 fast car charger type c port led digital voltmeter
- `temu-car-electric-fan-kit-cooling-car-air-fan-mini-car-cooling-fan-rv-backs` | car electric fan kit | cooling car air fan | mini car cooling fan, rv backseat fan with adjustable for trucks sedans electric cooling accessory usb plug for car/vehicle, without battery - automotive
- `temu-vehicle-waste-bin-easy-suspended-car-rubbish` | vehicle waste bin easy suspended car rubbish
- `temu-1-car-seat-storage-bag-table-organizer-back` | 1 car seat storage bag table organizer back
- `temu-sun-portable-foldable-car-windshield-sunshade` | sun portable foldable car windshield sunshade
- `temu-upgrade-universal-car-windshield-sun-visor-front-glass` | upgrade universal car windshield sun visor front glass
- `temu-compressor-de-ar-port-til-para-pneus-com-man-metro-digital` | compressor de ar portátil para pneus com manómetro digital
- `temu-portable-tire-inflator-led-light-air-compressor` | portable tire inflator led light air compressor
- `temu-tire-inflator-portable-air-compressor-150psi-car-tire-pump` | tire inflator portable air compressor 150psi car tire pump
- `temu-jump-starter-air-compressor-8000a-car-battery-jump` | jump starter air compressor 8000a car battery jump
- `temu-4500a-automotive-jump-starter-150psi-tire` | 4500a automotive jump starter 150psi tire
- `temu-3000a-jump-starter-portable-voiture-12v-5-4l` | 3000a jump starter portable voiture 12v 5 4l
- `temu-newest-scanner-code-reader-car-engine-fault-scanner` | newest scanner code reader car engine fault scanner
- `temu-advanced-diagnostic-scanner-cars-10-languages` | advanced diagnostic scanner cars 10 languages
- `temu-a-set-2-multi-colored-automatic-cat-feeders-water-dispensers` | a set 2 multi colored automatic cat feeders water dispensers
- `temu-ensemble-distributeur-automatique-nourriture-chat` | ensemble distributeur automatique nourriture chat
- `temu-otomatik-kedi-mama-ve-su-dispanseri-pil-gerekmez` | otomatik kedi mama ve su dispanseri pil gerekmez
- `temu-stainless-steel-cat-water-fountain-2-2l-74oz-automatic` | stainless steel cat water fountain 2 2l 74oz automatic
- `temu-elektrischer-nagelfeile-katzen-hunde-leise-nagelknipser` | elektrischer nagelfeile katzen hunde leise nagelknipser
- `temu-foldable-baby-stroller-lightweight-foldable-baby-stroller` | foldable baby stroller lightweight foldable baby stroller
- `temu-portable-stroller-seat-cushion-travel-multi` | portable stroller seat cushion travel multi
- `temu-prenosivi-aparat-za-beli-um-sa-21-prirodnog-umiruju-eg` | prenosivi aparat za beli šum sa 21 prirodnog umirujućeg
- `temu-1-set-nursery-wind-chime-bed-chimes-baby-mobile-crib-bells` | 1 set nursery wind chime bed chimes baby mobile crib bells
- `temu-1pc-weather-station-clock-backlit-large-screen-real-time` | 1pc weather station clock backlit large screen real time
- `temu-2024-wireless-talking-smart-watch-hd-screen` | 2024 wireless talking smart watch hd screen
- `temu-new-2026-smartwatch-unisex-wireless-calling-multiple` | new 2026 smartwatch unisex wireless calling multiple
- `temu-multi-layer-travel-digital-accessories-storage-bag-power` | multi layer travel digital accessories storage bag power
- `temu-gaming-laptop-cooling-pad-dual-powerful` | gaming laptop cooling pad dual powerful
- `temu-daisy-car-tissue-holder-paper-fit-cup-holders` | daisy car tissue holder paper fit cup holders
- `temu-a-side-storage-made-faux-leather-a` | a side storage made faux leather a
- `temu-5-seat-seat-covers-full-set-waterproof-car` | 5 seat seat covers full set waterproof car
- `temu-multi-functional-data-cable-organizer-desktop` | multi functional data cable organizer desktop
- `temu-emergency-two-in-hammer-automotive-temu` | emergency two in hammer automotive temu
- `temu-faltbarer-wasserdichter-kofferraum-organizer-4` | faltbarer wasserdichter kofferraum organizer 4
- `temu-aufbewahrungskorb-vielseitiger-kofferraum-organizer-tragbare` | aufbewahrungskorb vielseitiger kofferraum organizer tragbare
- `temu-smart-glasses-electronics` | smart glasses - electronics
- `temu-2026-couteurs-fil-avec-tactile-du-volume-micro-condensateur-chargement` | 2026 écouteurs fil avec tactile, du volume, micro condensateur, chargement type-c, batterie lithium polymère 300mah, chargement usb, écouteurs pour smartphones /ios, charge rapide, chargeur non – électroniques – Temu
- `temu-2026-newly-large-screen-full-touch-smartwatch` | 2026 newly large screen full touch smartwatch
- `temu-2026-new-model-smart-watch-men-women-wireless-calling-step` | 2026 new model smart watch men women wireless calling step
- `temu-phone-case-cover-56-a55-a54-a53-a52s-a52-a35` | phone case cover 56 a55 a54 a53 a52s a52 a35
- `temu-phone-case-2019-y9s-y9-prime-2019-y7a-p40-lite-p30` | phone case 2019 y9s y9 prime 2019 y7a p40 lite p30
- `temu-ultra-2026-latest-unlocked-smartphone-built` | ultra 2026 latest unlocked smartphone built
- `temu-latest-2026-model-usb-a-usb-c-data-1-5-meter` | latest 2026 model usb a usb c data 1 5 meter
- `temu-phone-case-transparent-magnetic-phone-cover-17` | phone case transparent magnetic phone cover 17

### toys — 95 products (full list)

- `daraz-real-diy-bracelet-kit-girls-kids` | DIY Bracelet Kit for Girls & Kids - Jewellery Making Beads Box with Charms & Tools
- `daraz-real-diy-bracelet-kit-round-box` | DIY Bracelet Kit Round Box - Large Beads Kit, Multiple Designs for Girls & Kids
- `daraz-real-diy-pearls-kit-girls` | DIY Pearls Kit for Girls - Pearls & Beads with Charms, Bracelet Making Box
- `daraz-real-diy-bracelet-making-kit-multicolor` | DIY Bracelet Making Kit for Girls - Jewellery Making Bead Set, Multicolor
- `daraz-real-gajra-bracelet-kit-crystal` | Gajra Bracelet Kit Crystal Diamond Pearls 4mm - DIY Making Set for Girls
- `daraz-real-speed-racing-rc-sports-car` | Speed Racing 1:20 RC Sports Car - Remote Control Drifting, 2.4GHz
- `daraz-real-teddy-bear-soft-plush` | Teddy Bear Soft Plush Toy - Large Stuffed Bear for Kids, Gift
- `daraz-real-red-teddy-bear-couple-heart` | Red Teddy Bear Couple with Love Heart - Soft Plush Pair, Gift
- `daraz-singing-baby-girl-doll-40cm` | Singing Songs and Poem Baby Girl Doll - 40cm Plush
- `daraz-teddy-bear-40inch` | Large Size Teddy Bear 40 inch Premium Plush Washable
- `daraz-teddy-bear-18inch` | Teddy Bear 18 inch Premium Plush Soft Washable
- `daraz-panda-teddy-stitch` | Cute Panda Teddy Bear Stitch Transforming Plush Toy
- `daraz-love-teddy-bear-imported` | Cutest Love Teddy Bear Imported Soft Stuffed Toy
- `daraz-strawberry-bunny-toy` | Zipper Reversible Strawberry Bunny Soft Toy
- `daraz-teddy-bear-1ft` | Soft Cuddly Teddy Bear 1ft Premium Plush Gift
- `daraz-sr-teddy-bear-8inch` | SR Traders Teddy Bear 8 inch Premium Plush
- `daraz-teddy-bear-12inch` | Teddy Bear 12 inch Premium Plush Soft Washable
- `daraz-teddy-bear-large-55ft` | Teddy Bear Soft Plush Toy Large 1ft to 5.5ft
- `temu-inflatable-tanning-pool-lounger-float-85-x-57-extra-large` | inflatable tanning pool lounger float 85 x 57 extra large
- `temu-fully-automatic-machine-kids-electric-toy-light` | fully automatic machine kids electric toy light
- `temu-chaleco-salvavidas-reflectante-perros-asa-rescate-chaleco` | chaleco salvavidas reflectante perros asa rescate chaleco
- `temu-sniffing-paradise-interactive-snuffle-mat-dogs` | sniffing paradise interactive snuffle mat dogs
- `temu-small-pet-snuffle-mat-dog-puzzle-mat-training-blanket-pet` | small pet snuffle mat dog puzzle mat training blanket pet
- `temu-snuffle-ball-dogs-breed-size-age-slow-feeding-interactive` | snuffle ball dogs breed size age slow feeding interactive
- `temu-xl-vertical-sisal-mushroom-shape-cat-scratching-station-cat` | xl vertical sisal mushroom shape cat scratching station cat
- `temu-solid-wood-cat-scratching-post-a-durable-furniture-protector` | solid wood cat scratching post a durable furniture protector
- `temu-4-8pcs-silicone-sensory-sticks-flexible` | 4 8pcs silicone sensory sticks flexible
- `temu-toy-made-food-grade-silicone-featuring-a` | toy made food grade silicone featuring a
- `temu-30pcs-party-favors-fidget-keychain-mini-fidget-toys-birthday-party-fav` | 30pcs party favors fidget keychain, mini fidget toys, birthday party favors, small classroom prizes box fidgets toys, birthday/halloween/christmas/valentine's gifts - toys & games
- `temu-a-compact-wrist-designed-tactile-stimulation` | a compact wrist designed tactile stimulation
- `temu-self-made-bubble-making-octopus-shaped-toy-squeezing` | self made bubble making octopus shaped toy squeezing
- `temu-bouncy-fun-diy-bubble-octopus-toy-slow-rising-bubble` | bouncy fun diy bubble octopus toy slow rising bubble
- `temu-mesondy-gesture-sensing-toy-for-2-4ghz-hand-control-led-lights-music-4` | mesondy gesture-sensing toy for , 2.4ghz hand control, led lights & music, 4wd off-road vehicle, teal with black accents - ideal birthday gift for boys ages 6-12, offroad rc car|illuminated wheels| - toys & games
- `temu-2025-new-gesture-controlled-flying-toy-lightweight-airplane` | 2025 new gesture controlled flying toy lightweight airplane
- `temu-a-kit-making-bracelets-16-000-3mm-glass-seed-beads-including` | a kit making bracelets 16 000 3mm glass seed beads including
- `temu-1260pcs-diy-metal-accessory-material-set-beading-jewelry` | 1260pcs diy metal accessory material set beading jewelry
- `temu-diamond-painting-kit-featuring-an-angel-girl` | diamond painting kit featuring an angel girl
- `temu-paint-numbers-kit-adults-beginners-16x20in-40x50cm-color` | paint numbers kit adults beginners 16x20in 40x50cm color
- `temu-professional-art-use-adult-paint-number-kits-art` | professional art use adult paint number kits art
- `temu-a-beginners-crochet-kit-adults-featuring-a-written` | a beginners crochet kit adults featuring a written
- `temu-complete-adult-beginner-embroidery-kit-tree-floral-hoop` | complete adult beginner embroidery kit tree floral hoop
- `temu-3-sets-flower-pattern-embroidery-stitches-practice-kit` | 3 sets flower pattern embroidery stitches practice kit
- `temu-3pcs-super-soft-yarn-diy-hand-knitting-8-ply-yarn` | 3pcs super soft yarn diy hand knitting 8 ply yarn
- `temu-6pcs-set-5-layer-color-gradient-acrylic-yarn-hand-knitted` | 6pcs set 5 layer color gradient acrylic yarn hand knitted
- `temu-18pcs-900g-1-pack-high-quality-mixed-colors-4-combed` | 18pcs 900g 1 pack high quality mixed colors 4 combed
- `temu-300g-90-wool-10-acrylic-fiber-yarn-12-vibrant-colors` | 300g 90 wool 10 acrylic fiber yarn 12 vibrant colors
- `temu-diy-3d-wooden-puzzle-rotating-music-box-puzzle` | diy 3d wooden puzzle rotating music box puzzle
- `temu-54pcs-wooden-brain-teaser-puzzle-cube-wooden-puzzles` | 54pcs wooden brain teaser puzzle cube wooden puzzles
- `temu-dopamine-infinite-irregular-wooden-brain` | dopamine infinite irregular wooden brain
- `temu-ludo-game-board-dice-pieces-suitable-family` | ludo game board dice pieces suitable family
- `temu-55-playing-cards-suitable-parties-team-building` | 55 playing cards suitable parties team building
- `temu-adult-playing-cards-24-packs-decks-cards-bulk-poker-size` | adult playing cards 24 packs decks cards bulk poker size
- `temu-size-playing-cards-waterproof-plastic-poker` | size playing cards waterproof plastic poker
- `temu-1-set-wooden-chess-board-game-storage-slots` | 1 set wooden chess board game storage slots
- `temu-vintage-gemstone-feather-pen-set-calligraphy-drawing-pen` | vintage gemstone feather pen set calligraphy drawing pen
- `temu-set-36-rolls-pink-washi-tape-featuring-adorable` | set 36 rolls pink washi tape featuring adorable
- `temu-4pcs-spring-valentines-day-themed-washi-tape-pink-floral-bow` | 4pcs spring valentines day themed washi tape pink floral bow
- `temu-20-rolls-tiny-colorful-washi-tape-set-basic-skinny-masking` | 20 rolls tiny colorful washi tape set basic skinny masking
- `temu-stickers-book-50-sheets-journaling-stickers-pre` | stickers book 50 sheets journaling stickers pre
- `temu-a-pack-6-sheets-series-transparent-high-quality` | a pack 6 sheets series transparent high quality
- `temu-1-bag-total-100-sheets-4-bags-sheets-material` | 1 bag total 100 sheets 4 bags sheets material
- `temu-garden-ivy-scrapbooking-paper-pack-24-sheets-12x12-inch` | garden ivy scrapbooking paper pack 24 sheets 12x12 inch
- `temu-vintage-supplies-aesthetic-journaling-kit` | vintage supplies aesthetic journaling kit
- `temu-1pc-transparent-acrylic-3-7-layer-stepped-hand-ledger-tape` | 1pc transparent acrylic 3 7 layer stepped hand ledger tape
- `temu-384pcs-resin-earring-pendants-silicone-mold-set-create` | 384pcs resin earring pendants silicone mold set create
- `temu-32pcs-jewelry-resin-bead-mold-set-2pcs-round-bead` | 32pcs jewelry resin bead mold set 2pcs round bead
- `temu-kit-making-candle-wax-home-a-long-handled-mini` | kit making candle wax home a long handled mini
- `temu-105pcs-1-set-candle-making-kit-supplies-including-1-43-96` | 105pcs 1 set candle making kit supplies including 1 43 96
- `temu-2pcs-4-rectangle-silicone-soap-molds-3oz` | 2pcs 4 rectangle silicone soap molds 3oz
- `temu-a-set-3-soap-molds-shaped-like-butterflies-dragonflies-bees` | a set 3 soap molds shaped like butterflies dragonflies bees
- `temu-1-2pcs-4-mold-silicone-heart-mold-bath-soap` | 1 2pcs 4 mold silicone heart mold bath soap
- `temu-1-oval-bee-themed-silicone-soap-mold-6-handmade-tool` | 1 oval bee themed silicone soap mold 6 handmade tool
- `temu-11pcs-turquoise-feather-element-bracelet-set-gift-friends` | 11pcs turquoise feather element bracelet set gift friends
- `temu-2650pcs-bands-craft-kit-rubber-bands-bracelet` | 2650pcs bands craft kit rubber bands bracelet
- `temu-200pcs-new-handmade-rubber-loom-bands-diy` | 200pcs new handmade rubber loom bands diy
- `temu-origami-kit-kids-colorful-paper-airplane-craft-set-36-sheets` | origami kit kids colorful paper airplane craft set 36 sheets
- `temu-zhenyan-three-brush-set-sheep-hair-jade-bamboo` | zhenyan three brush set sheep hair jade bamboo
- `temu-6pcs-calligraphy-brush-pen-set-golden-accents-ergonomic-grip` | 6pcs calligraphy brush pen set golden accents ergonomic grip
- `temu-12-24-48-watercolor-paint-48-color` | 12 24 48 watercolor paint 48 color
- `temu-new-288-pack-acrylic-markers-layered-coloring` | new 288 pack acrylic markers layered coloring
- `temu-80-60-48-36-24-12-colors-acrylic-marker-set` | 80 60 48 36 24 12 colors acrylic marker set
- `temu-1-book-22-page-thick-paper-themed-coloring-book-s` | 1 book 22 page thick paper themed coloring book s
- `temu-adult-coloring-book-8-3-11-2-inches-22` | adult coloring book 8 3 11 2 inches 22
- `temu-1-5-100pages-flower-vintage-watercolor` | 1 5 100pages flower vintage watercolor
- `temu-175pcs-set-2-drawing-pads-crayons-acrylic-paints` | 175pcs set 2 drawing pads crayons acrylic paints
- `temu-180-colored-pencils-set-professional` | 180 colored pencils set professional
- `temu-33-drawing-sketching-kit-portable-artist-supplies` | 33 drawing sketching kit portable artist supplies
- `temu-6pcs-white-sketch-charcoal-pencils-professional-high-quality` | 6pcs white sketch charcoal pencils professional high quality
- `temu-33pcs-professional-drawing-sketch-set-portable-artist-travel` | 33pcs professional drawing sketch set portable artist travel
- `temu-canvas-painting-painting-art-supplies-art-supplies-14pcs-1` | canvas painting painting art supplies art supplies 14pcs 1
- `temu-8-art-painting-canvas-panels-blank-canvas-boards` | 8 art painting canvas panels blank canvas boards
- `temu-stretched-canvas-multi-pack-sizes-12x16-11x14-10x12-8x10-5x7` | stretched canvas multi pack sizes 12x16 11x14 10x12 8x10 5x7
- `temu-7pcs-painting-palette-knife-set-gouache-watercolor-acrylic` | 7pcs painting palette knife set gouache watercolor acrylic
- `temu-professional-painting-kit-unframed` | professional painting kit unframed
- `temu-3-set-high-definition-spray-painted-canvas-art-custom-photo` | 3 set high definition spray painted canvas art custom photo

### health — 35 products (full list)

- `daraz-real-posture-belt-posture-corrector-belt-back` | Posture belt, Posture corrector belt, Back support belt, Backbone Belt, Spine Support Belt, Back Pain Relief Shoulder Back Support Belt
- `daraz-electric-hot-water-bottle-heat-pad-multicolour` | Electric Hot Water Bottle Heat Pad (Heat Bag) For Pain Relief - Multicolour
- `daraz-reflexology-massage-slippers` | Reflexology Acupressure Massage Slippers Foot Pain Relief
- `daraz-heel-care-slippers-eva` | Heel Care Slippers Soft Cushion EVA Anti-Crack
- `temu-back-posture-support-clavicle-support-new` | Back Posture Support Clavicle Support New
- `temu-heating-pad-a-3d-kneading-back-massager-designed` | Heating Pad a 3d Kneading Back Massager Designed
- `temu-pressure-monitor-rate-detection` | Pressure Monitor Rate Detection
- `temu-digital-fingertip-oximeter-blood-oxygen` | Digital Fingertip Oximeter Blood Oxygen
- `temu-postpartum-belly-belt-womens-breathable-waist-belt` | postpartum belly belt womens breathable waist belt
- `temu-postpartum-belt-strong-waist-trainer-shaping` | postpartum belt strong waist trainer shaping
- `temu-1-2pcs-luxury-neck-massager-experience-pillow-support` | 1 2pcs luxury neck massager experience pillow support
- `temu-masaj-electric-de-acas-instrument-gua-sha-cu` | masaj electric de acasă instrument gua sha cu
- `temu-heating-massage-chair-cushion-adjustable-lumbar-support-9` | heating massage chair cushion adjustable lumbar support 9
- `temu-vibration-massage-seat-cushion-car-w-10-vibration-motors-seat-back-mas` | vibration massage seat cushion car w/ 10 vibration motors seat back massager - automotive
- `temu-hand-massager-heat-compression-3-finger-wrist-relax` | hand massager heat compression 3 finger wrist relax
- `temu-portable-deep-tissue-massage-gun-with-9-massage-heads-handheld-suitabl` | portable deep tissue massage gun with 9 massage heads - handheld suitable for body, back, neck, for gym, for use - long-lasting massager device for s & athletes - health & household
- `temu-1pc-hand-massager-cordless-electric` | 1pc hand massager cordless electric
- `temu-1pc-2pcs-portable-cordless-heated-knee-massager-usb` | 1pc 2pcs portable cordless heated knee massager usb
- `temu-rechargeable-electric-leg-massager-a-calf-air-pressure` | rechargeable electric leg massager a calf air pressure
- `temu-8pcs-ear-care-set-visual-ear-pick-earwax-removal-tool-earwax` | 8pcs ear care set visual ear pick earwax removal tool earwax
- `temu-2pcs-stainless-steel-tongue-scrapers-large-case-tongue` | 2pcs stainless steel tongue scrapers large case tongue
- `temu-klips-na-nos-przeciw-chrapaniu-magnetyczny-klips-na-nos` | klips na nos przeciw chrapaniu magnetyczny klips na nos
- `temu-matelas-lit-matelas-design` | matelas lit matelas à design
- `temu-pair-supportive-knee-sleeves-weightlifting-squats` | pair supportive knee sleeves weightlifting squats
- `temu-1pc-small-size-3d-knitted-elastic-breathable-unisex` | 1pc small size 3d knitted elastic breathable unisex
- `temu-1pc-sports-wrist-support-relieve-compression` | 1pc sports wrist support relieve compression
- `temu-hunchback-posture-support-chest-shoulder-neck` | hunchback posture support chest shoulder neck
- `temu-cintura-supporto-lombare-e-donne-posteriore` | cintura supporto lombare e donne posteriore
- `temu-8x-powerful-lumbar-support-back-brace-massage-pad-breathable` | 8x powerful lumbar support back brace massage pad breathable
- `temu-set-2-pillows-designed-sleep-neck-support-pillow-cores` | set 2 pillows designed sleep neck support pillow cores
- `temu-pillow-use-neck-support` | pillow use neck support
- `temu-1-reusable-ice-pack-cold-wisdom-teeth` | 1 reusable ice pack cold wisdom teeth
- `temu-5pcs-soft-gel-ice-patch-ice-cold-good` | 5pcs soft gel ice patch ice cold good
- `temu-wrist-blood-pressure-monitor-digital-bp-monitor-rechargeable` | wrist blood pressure monitor digital bp monitor rechargeable
- `temu-forehead-thermometer-digital-infrared-thermometer` | forehead thermometer digital infrared thermometer

### Small groups (full: id | name)


**Phone Accessories — 3:**
- `temu-3-in-1-magnetic-phone-holder-for-magsafe-iphone-12-17-foldab` | 3-in-1 Magnetic Phone Holder for MagSafe iPhone 12-17, Foldable 360 Rotation
- `temu-15w-fast-wireless-charging-phone-mount-vacuum-suction-magnet` | 15W Fast Wireless Charging Phone Mount, Vacuum Suction Magnetic for MagSafe iPhone
- `temu-360-adjustable-vacuum-magnetic-car-phone-holder-for-magsafe` | 360 Adjustable Vacuum Magnetic Car Phone Holder for MagSafe, N52 Magnet Anti-Shake

**Electronics — 3:**
- `daraz-zero-evo-wireless-earbuds-bluetooth-5-4` | Zero Evo Wireless Earbuds Bluetooth 5.4
- `daraz-air31-wireless-earbuds-bluetooth-5-3` | AIR31 Wireless Earbuds Bluetooth 5.3
- `daraz-m10-tws-wireless-bluetooth-earbuds` | M10 TWS Wireless Bluetooth Earbuds

**Mobile Accessories — 3:**
- `daraz-remax-rpp-87-20000mah-power-bank` | Remax RPP-87 20000mAh Power Bank
- `daraz-mi-power-bank-3-20000mah` | Mi Power Bank 3 20000mAh
- `daraz-r1s-bluetooth-selfie-stick-3-in-1-tripod` | R1s Bluetooth Selfie Stick 3-in-1 Tripod

**toys-wellness — 2:**
- `daraz-real-magic-color-changeable-grape-mesh-squish-ball-stress-relief` | Magic Color-Changeable Grape Mesh Squish Ball - Stress Relief Squeezing Toy | Hand and Wrist Exercise Rubber Grape Ball for Anxiety, Fidgeting & Fun | Sensory Toy for Kids and Adults
- `daraz-real-hand-exercise-stress-relief-smiley-emoji-physio-ball-yellow` | Hand Exercise Stress Relief Smiley Emoji Physio Ball Yellow Smile Face, Kids Birthday Gift

**Health — 1:**
- `daraz-posture-corrector-belt-back-support` | Posture Corrector Belt Back Support Belt

---
# B. Missing / broken images

Pre-fix: **85 products with no `image_url`** **[verified — catalog scan]**: 58 Daraz, 27 Temu. Item pages for these rendered blank media blocks (`<img src="">` seen in generated related-cards — verified in git diff).

## B1. Fix applied — Daraz (58 of 58 verified, all fixed)
Each product's own official Daraz landing page (via its stored `s.daraz.pk` affiliate link, public GET, no login) exposed an `og:image`. All 58: HEAD 200 with `image/*` content type; product name on the fetched page matched the catalog product (3 strict-string flags resolved as title typos/spacing only — same products). Original `og:image` URL written to `image_url`. Full per-product list + URLs: [p1-fix-changelog-20261009.md](sandbox://workspace/affiliate-site/hidden_files/p1-fix-changelog-20261009.md) — representative fixed IDs: `daraz-real-2-in-1-eyebrow-trimmer-for-women-facial-`, `daraz-real-ear-wax-cleaning-kit-6-pcs-ear-pick-tool`, `daraz-real-loreal-paris-loreal-elvive-6-oil-nourish`, `daraz-real-gt1-smart-watch-smartwatch-smartwatches-`. **[verified]**
Post-fix live state: only **27** products (all Temu) remain without an image **[verified — live products.json recount]**.

## B2. Not fixable in this run — Temu 27 (needs browser pass)
Temu goods pages returned full HTML (HTTP 200) but embed **no static product image or og:image** (client-rendered) — no CAPTCHA was served, nothing was bypassed. These need one browser session (parent-delegated) to read the rendered gallery URLs. **[verified — 2 goods pages fetched; pattern confirmed on both]**

| id/slug | category | merchant/source | image status |
|---|---|---|---|
| `temu-12-pack-medium-hair-claw-clips-matte` | beauty | temu / temu-affiliate | needs browser pass |
| `temu-2-in-1-bear-pattern-magnetic-phone-case-with-card-holder` | electronics | temu / temu-affiliate | needs browser pass |
| `temu-2-in-1-magnetic-phone-case-with-stand-magsafe` | electronics | temu / temu-affiliate | needs browser pass |
| `temu-30-led-outdoor-solar-lawn-lights-waterproof` | home | temu / temu-affiliate | needs browser pass |
| `temu-3pcs-beauty-tool-gift-box-jade-roller-gua-sha-set` | beauty | temu / temu-affiliate | needs browser pass |
| `temu-3pcs-flower-garland-zirconia-necklace-earrings-ring-set` | jewelry | temu / temu-affiliate | needs browser pass |
| `temu-3pcs-jade-roller-gua-sha-massage-set` | beauty | temu / temu-affiliate | needs browser pass |
| `temu-55-inch-aluminum-camera-tripod-with-phone-clip` | electronics | temu / temu-affiliate | needs browser pass |
| `temu-5pcs-luxury-facial-care-set-with-jade-roller` | beauty | temu / temu-affiliate | needs browser pass |
| `temu-6pcs-ice-face-roller-jade-roller-gua-sha-set` | beauty | temu / temu-affiliate | needs browser pass |
| `temu-6pcs-plumeria-flower-hair-claw-clips` | beauty | temu / temu-affiliate | needs browser pass |
| `temu-8-pack-solar-torch-lights-outdoor-flickering-flame` | home | temu / temu-affiliate | needs browser pass |
| `temu-8pcs-flower-shape-hair-claw-clips-frosted` | beauty | temu / temu-affiliate | needs browser pass |
| `temu-dual-sided-pet-grooming-brush-stainless-steel` | home | temu / temu-affiliate | needs browser pass |
| `temu-ladies-floral-zirconia-earrings-necklace-jewelry-set` | jewelry | temu / temu-affiliate | needs browser pass |
| `temu-large-hair-claw-clips-12-pack-flower-for-thick-hair` | beauty | temu / temu-affiliate | needs browser pass |
| `temu-luxury-jade-roller-rose-quartz-gua-sha-gift-set` | beauty | temu / temu-affiliate | needs browser pass |
| `temu-magnetic-phone-case-black-kittens-iphone` | electronics | temu / temu-affiliate | needs browser pass |
| `temu-magnetic-phone-case-kitten-balancing-iphone` | electronics | temu / temu-affiliate | needs browser pass |
| `temu-magnetic-phone-case-small-blue-iphone` | electronics | temu / temu-affiliate | needs browser pass |
| `temu-pet-comb-stainless-steel-bristle-grooming-tool` | home | temu / temu-affiliate | needs browser pass |
| `temu-pet-grooming-comb-deshedding-brush-hair-removal` | home | temu / temu-affiliate | needs browser pass |
| `temu-pet-massage-comb-deshedding-grooming-brush` | home | temu / temu-affiliate | needs browser pass |
| `temu-set-of-3-small-hair-claw-clips-for-ponytail` | beauty | temu / temu-affiliate | needs browser pass |
| `temu-stainless-steel-fruit-cutting-machine-french-fry-cutter` | home | temu / temu-affiliate | needs browser pass |
| `temu-sunflower-zirconia-pendant-necklace-stud-earrings-set` | jewelry | temu / temu-affiliate | needs browser pass |
| `temu-women-red-crystal-beads-support-bracelet` | jewelry | temu / temu-affiliate | needs browser pass |

## B3. Broken-image re-verification
- Known broken item from Phase A: `temu-4d-volumizing-mascara-waterproof-long-lasting-black-mascara`, image `https://commimg.us.kwcdn.com/goods-detail-image/35b7c2/yeUWmfsNGd/83205a5071d748aa8b0d12cbd753c745.png` → **still HTTP 404 [verified this run]**. Fix path: same browser pass as B2 (correct Temu gallery URL), then a one-product `image_url` patch — Qasim approval already covered by the image-fix permission; not applied here because the correct URL is not yet known.
- Catalog-wide broken-rate: 1 broken of 200 sampled (0.5%) **[verified as a sample stat — Phase A]**; extrapolation ≈33 broken images across 6,718 is an **[estimate]**, not a verified count. A full-catalog image HEAD sweep is recommended (read-only, ~6.6k HEADs at polite pacing) before any claim is made.

---
# C. Duplicates — lists + recommendations only (NO deletions made)

## C1. Hard duplicates — 17 pairs (identical affiliate URL ⇒ same goods_id, listed twice) **[verified]**

Both records of each pair; recommendation = keep the record whose slug/category is canonical (right-hand column), remove the other — **every pair requires Qasim's explicit OK before any deletion**.

| # | goods_id | Keep candidate (record A) | Remove candidate (record B) | Note |
|---|---|---|---|---|
| 1 | 601100764030720 | `temu-smart-watch-fitness-0720` (electronics, img y) | `temu-smartwatch-with-full-touch-high-definition-screen-and-fitnes` (electronics, img y) | same affiliate URL `https://www.temu.com/goods.html?goods_id=601100764030720&_x_cid=601302…`; both item pages live; removal of B pending approval |
| 2 | 601101496534172 | `temu-lipstick-makeup-beauty-4172` (beauty, img y) | `temu-lip-products-in-including-two-tone` (fashion, img y) | same affiliate URL `https://www.temu.com/goods.html?goods_id=601101496534172&_x_cid=601302…`; both item pages live; removal of B pending approval |
| 3 | 601100797414552 | `temu-vintage-style-womens-shoulder-bag-chic-shoulder-handbag-geor` (fashion, img y) | `temu-vintage-style-womens-shoulder-bag-chic-shoulder-handbag` (bags, img y) | same affiliate URL `https://www.temu.com/goods.html?goods_id=601100797414552&_x_cid=601302…`; both item pages live; removal of B pending approval |
| 4 | 601099724821487 | `temu-womens-warm-ankle-snow-boots-winter-lace-fleece-lined-non` (fashion, img y) | `temu-womens-winter-boots-1487` (shoes, img y) | same affiliate URL `https://www.temu.com/goods.html?goods_id=601099724821487&_x_cid=601302…`; both item pages live; removal of B pending approval |
| 5 | 601102109893765 | `temu-snow-boots-women-winter-shoes-womens-work-warm-womens-boot-d` (fashion, img y) | `temu-snow-boots-womens-winter-shoes-womens-work-warm-womens-boot` (shoes, img y) | same affiliate URL `https://www.temu.com/goods.html?goods_id=601102109893765&_x_cid=601302…`; both item pages live; removal of B pending approval |
| 6 | 601099557999479 | `temu-dames-herfst-winter-eenvoudige-lichtgewicht-gevoerde-netherl` (fashion, img y) | `temu-womens-puffer-jacket-winter-9479` (fashion, img y) | same affiliate URL `https://www.temu.com/goods.html?goods_id=601099557999479&_x_cid=601302…`; both item pages live; removal of B pending approval |
| 7 | 601101832277584 | `temu-synthetic-leather-zipper-wallet-women-suitable-a-4-season-qa` (fashion, img y) | `temu-synthetic-leather-zipper-wallet-womens-suitable-a-4-season` (bags, img y) | same affiliate URL `https://www.temu.com/goods.html?goods_id=601101832277584&_x_cid=601302…`; both item pages live; removal of B pending approval |
| 8 | 601099968821205 | `temu-hoop-earrings-womens` (jewelry, img y) | `temu-a-pair-minimalist-versatile-hollow-earrings-a-fashionable` (jewelry, img y) | same affiliate URL `https://www.temu.com/goods.html?goods_id=601099968821205&_x_cid=601302…`; both item pages live; removal of B pending approval |
| 9 | 601099634368775 | `temu-hoop-earrings-womens-8775` (jewelry, img y) | `temu-mobius-shape-hoop-earrings-minimalist-golden` (jewelry, img y) | same affiliate URL `https://www.temu.com/goods.html?goods_id=601099634368775&_x_cid=601302…`; both item pages live; removal of B pending approval |
| 10 | 601099868325592 | `temu-womens-gloves-winter` (accessories, img y) | `temu-2pcs-womens-touchscreen-gloves-winter-fashionable-warm-plush` (fashion, img y) | same affiliate URL `https://www.temu.com/goods.html?goods_id=601099868325592&_x_cid=601302…`; both item pages live; removal of B pending approval |
| 11 | 601099690797499 | `temu-womens-gloves-winter-7499` (accessories, img y) | `temu-womens-thermal-winter-cycling-ski-gloves-windproof-snowproof` (fashion, img y) | same affiliate URL `https://www.temu.com/goods.html?goods_id=601099690797499&_x_cid=601302…`; both item pages live; removal of B pending approval |
| 12 | 601103389145886 | `temu-womens-gloves-winter-5886` (accessories, img y) | `temu-womens-mens-winter-thermal-gloves-touchscreen` (fashion, img y) | same affiliate URL `https://www.temu.com/goods.html?goods_id=601103389145886&_x_cid=601302…`; both item pages live; removal of B pending approval |
| 13 | 601099642410115 | `temu-phone-wallet-ladies-bag-fashion-lock` (bags, img y) | `temu-phone-wallet-ladies-bag-fashion-lock-australia` (fashion, img y) | same affiliate URL `https://www.temu.com/goods.html?goods_id=601099642410115&_x_cid=601302…`; both item pages live; removal of B pending approval |
| 14 | 601105629616223 | `temu-2026-new-comfortable-slip-loafers-versatile-soft-sole-shoes` (shoes, img y) | `temu-new-comfortable-slip-loafers-versatile-soft-sole-shoes` (fashion, img y) | same affiliate URL `https://www.temu.com/goods.html?goods_id=601105629616223&_x_cid=601302…`; both item pages live; removal of B pending approval |
| 15 | 601103074183681 | `temu-fashionable-slip-small-flat-shoes-season-versatile` (shoes, img y) | `temu-fashionable-slip-small-flat-shoes-season-versatile-pakistan` (fashion, img y) | same affiliate URL `https://www.temu.com/goods.html?goods_id=601103074183681&_x_cid=601302…`; both item pages live; removal of B pending approval |
| 16 | 601099774309347 | `temu-10-000mah-mobile-phone-power-bank-charger-2-4a` (fashion, img y) | `temu-10-000mah-mobile-phone-power-bank-charger-2-4a-9347` (electronics, img y) | same affiliate URL `https://www.temu.com/goods.html?goods_id=601099774309347&_x_cid=601302…`; both item pages live; removal of B pending approval |
| 17 | 601099816750402 | `temu-aura-bracelet-chakra-lotus-jewelry-featuring-6mm-rose-quartz` (jewelry, img y) | `temu-aura-bracelet-chakra-lotus-jewelry-featuring-6mm-rose-quartz-0402` (jewelry, img y) | same affiliate URL `https://www.temu.com/goods.html?goods_id=601099816750402&_x_cid=601302…`; both item pages live; removal of B pending approval |

Observed pattern: one twin usually sits in a drifted/off category (`fashion` instead of `shoes`/`bags`/`electronics`) — several of these twins were NOT touched by the category fixes above because both spellings were pre-existing canonical ids; category clean-up and dedup should be approved together.

## C2. Exact-duplicate names — 100 name groups, 353 records **[verified — current catalog]** (Phase A said 99 groups at the 6,640 state; Batch 1 additions created the 100th group **[verified by recount]**.)

Triage (from stored fields only): **2 of 100** groups share an identical affiliate URL (already inside C1). The other **98** have distinct affiliate URLs — same display title, different listings **[evidence: distinct goods_ids/short links]**. On Temu that usually means seller variants of the same product, sometimes genuinely different goods (different size/pack). Without reading each goods page (browser pass) the same-vs-variant call cannot be made honestly for all 98 — marked **needs adjudication pass**, not guesswork.

| Name (lowercased key) | Records | Slugs | Triage |
|---|---|---|---|
| flat 1pc xmas christmas vintage snow for man throw pillow covers red | 8 | `temu-flat-1pc-xmas-christmas-vintage-snow-for-man-throw`, `temu-flat-1pc-xmas-christmas-vintage-snow-for-man-throw-2`, `temu-flat-1pc-xmas-christmas-vintage-snow-for-man-throw-3`, `temu-flat-1pc-xmas-christmas-vintage-snow-for-man-throw-4`, `temu-flat-1pc-xmas-christmas-vintage-snow-for-man-throw-5`, `temu-flat-1pc-xmas-christmas-vintage-snow-for-man-throw-6`, `temu-flat-1pc-xmas-christmas-vintage-snow-for-man-throw-7`, `temu-flat-1pc-xmas-christmas-vintage-snow-for-man-throw-8` | distinct URLs — seller-variant or relist; needs goods pass |
| curtains blackout window | 8 | `temu-curtains-blackout-window`, `temu-curtains-blackout-window-7135`, `temu-curtains-blackout-window-1314`, `temu-curtains-blackout-window-0534`, `temu-curtains-blackout-window-6020`, `temu-curtains-blackout-window-4711`, `temu-curtains-blackout-window-8122`, `temu-curtains-blackout-window-2888` | distinct URLs — seller-variant or relist; needs goods pass |
| women's shapewear | 8 | `temu-womens-shapewear`, `temu-womens-shapewear-4784`, `temu-womens-shapewear-4766`, `temu-womens-shapewear-9578`, `temu-womens-shapewear-8706`, `temu-womens-shapewear-7773`, `temu-womens-shapewear-8505`, `temu-womens-shapewear-8767` | distinct URLs — seller-variant or relist; needs goods pass |
| women's kimono cardigan | 8 | `temu-womens-kimono-cardigan`, `temu-womens-kimono-cardigan-5011`, `temu-womens-kimono-cardigan-2707`, `temu-womens-kimono-cardigan-4896`, `temu-womens-kimono-cardigan-3676`, `temu-womens-kimono-cardigan-7886`, `temu-womens-kimono-cardigan-2896`, `temu-womens-kimono-cardigan-6474` | distinct URLs — seller-variant or relist; needs goods pass |
| nail polish gel set | 7 | `temu-nail-polish-gel-set`, `temu-nail-polish-gel-set-0039`, `temu-nail-polish-gel-set-5675`, `temu-nail-polish-gel-set-1556`, `temu-nail-polish-gel-set-4360`, `temu-nail-polish-gel-set-5552`, `temu-nail-polish-gel-set-6381` | distinct URLs — seller-variant or relist; needs goods pass |
| mini projector | 7 | `temu-mini-projector`, `temu-mini-projector-9980`, `temu-mini-projector-2326`, `temu-mini-projector-6531`, `temu-mini-projector-7751`, `temu-mini-projector-1302`, `temu-mini-projector-1605` | distinct URLs — seller-variant or relist; needs goods pass |
| humidifier diffuser | 7 | `temu-humidifier-diffuser`, `temu-humidifier-diffuser-2535`, `temu-humidifier-diffuser-1894`, `temu-humidifier-diffuser-2380`, `temu-humidifier-diffuser-5861`, `temu-humidifier-diffuser-4372`, `temu-humidifier-diffuser-6583` | distinct URLs — seller-variant or relist; needs goods pass |
| women's blazer jacket | 7 | `temu-womens-blazer-jacket`, `temu-womens-blazer-jacket-2052`, `temu-womens-blazer-jacket-9979`, `temu-womens-blazer-jacket-0708`, `temu-womens-blazer-jacket-0508`, `temu-womens-blazer-jacket-4402`, `temu-womens-blazer-jacket-2984` | distinct URLs — seller-variant or relist; needs goods pass |
| item picture 2pcs post apocalyptic distressed scarf shawl and brooch set medieval renai... | 6 | `temu-item-picture-2pcs-post-apocalyptic-distressed-scar`, `temu-item-picture-2pcs-post-apocalyptic-distressed-scar-2`, `temu-item-picture-2pcs-post-apocalyptic-distressed-scar-3`, `temu-item-picture-2pcs-post-apocalyptic-distressed-scar-4`, `temu-item-picture-2pcs-post-apocalyptic-distressed-scar-5`, `temu-item-picture-2pcs-post-apocalyptic-distressed-scar-6` | distinct URLs — seller-variant or relist; needs goods pass |
| led lamp light decor | 6 | `temu-led-lamp-light-decor`, `temu-led-lamp-light-decor-5638`, `temu-led-lamp-light-decor-1468`, `temu-led-lamp-light-decor-2084`, `temu-led-lamp-light-decor-7941`, `temu-led-lamp-light-decor-2919` | distinct URLs — seller-variant or relist; needs goods pass |
| phone case accessories | 6 | `temu-phone-case-accessories`, `temu-phone-case-accessories-2204`, `temu-phone-case-accessories-8432`, `temu-phone-case-accessories-5365`, `temu-phone-case-accessories-9646`, `temu-phone-case-accessories-6616` | distinct URLs — seller-variant or relist; needs goods pass |
| women's shoes heels | 6 | `temu-womens-shoes-heels`, `temu-womens-shoes-heels-4140`, `temu-womens-shoes-heels-1949`, `temu-womens-shoes-heels-4536`, `temu-womens-shoes-heels-1414`, `temu-womens-shoes-heels-2289` | distinct URLs — seller-variant or relist; needs goods pass |
| women's sunglasses | 6 | `temu-womens-sunglasses`, `temu-womens-sunglasses-7716`, `temu-womens-sunglasses-0528`, `temu-womens-sunglasses-6860`, `temu-womens-sunglasses-3406`, `temu-womens-sunglasses-6697` | distinct URLs — seller-variant or relist; needs goods pass |
| led strip lights room | 6 | `temu-led-strip-lights-room`, `temu-led-strip-lights-room-0122`, `temu-led-strip-lights-room-4280`, `temu-led-strip-lights-room-6335`, `temu-led-strip-lights-room-5949`, `temu-led-strip-lights-room-1086` | distinct URLs — seller-variant or relist; needs goods pass |
| spice jars organizer kitchen | 6 | `temu-spice-jars-organizer-kitchen`, `temu-spice-jars-organizer-kitchen-9563`, `temu-spice-jars-organizer-kitchen-8487`, `temu-spice-jars-organizer-kitchen-2675`, `temu-spice-jars-organizer-kitchen-3541`, `temu-spice-jars-organizer-kitchen-9453` | distinct URLs — seller-variant or relist; needs goods pass |
| wireless charger station | 6 | `temu-wireless-charger-station`, `temu-wireless-charger-station-5280`, `temu-wireless-charger-station-4098`, `temu-wireless-charger-station-8386`, `temu-wireless-charger-station-8004`, `temu-wireless-charger-station-0150` | distinct URLs — seller-variant or relist; needs goods pass |
| women's work office outfit | 6 | `temu-womens-work-office-outfit`, `temu-womens-work-office-outfit-7140`, `temu-womens-work-office-outfit-4934`, `temu-womens-work-office-outfit-1032`, `temu-womens-work-office-outfit-9670`, `temu-womens-work-office-outfit-1927` | distinct URLs — seller-variant or relist; needs goods pass |
| women's swimsuit bikini | 6 | `temu-womens-swimsuit-bikini`, `temu-womens-swimsuit-bikini-8497`, `temu-womens-swimsuit-bikini-4223`, `temu-womens-swimsuit-bikini-0844`, `temu-womens-swimsuit-bikini-3807`, `temu-womens-swimsuit-bikini-1657` | distinct URLs — seller-variant or relist; needs goods pass |
| makeup foundation concealer | 5 | `temu-makeup-foundation-concealer`, `temu-makeup-foundation-concealer-3000`, `temu-makeup-foundation-concealer-2535`, `temu-makeup-foundation-concealer-1769`, `temu-makeup-foundation-concealer-6663` | distinct URLs — seller-variant or relist; needs goods pass |
| throw blanket fleece | 5 | `temu-throw-blanket-fleece`, `temu-throw-blanket-fleece-0721`, `temu-throw-blanket-fleece-6079`, `temu-throw-blanket-fleece-4282`, `temu-throw-blanket-fleece-9403` | distinct URLs — seller-variant or relist; needs goods pass |
| women's hat cap | 5 | `temu-womens-hat-cap`, `temu-womens-hat-cap-7485`, `temu-womens-hat-cap-6814`, `temu-womens-hat-cap-8102`, `temu-womens-hat-cap-4054` | distinct URLs — seller-variant or relist; needs goods pass |
| women's gloves winter | 5 | `temu-womens-gloves-winter`, `temu-womens-gloves-winter-9486`, `temu-womens-gloves-winter-8397`, `temu-womens-gloves-winter-7499`, `temu-womens-gloves-winter-5886` | distinct URLs — seller-variant or relist; needs goods pass |
| women's gym leggings yoga | 5 | `temu-womens-gym-leggings-yoga`, `temu-womens-gym-leggings-yoga-8180`, `temu-womens-gym-leggings-yoga-1291`, `temu-womens-gym-leggings-yoga-4794`, `temu-womens-gym-leggings-yoga-7339` | distinct URLs — seller-variant or relist; needs goods pass |
| women's beach cover up | 5 | `temu-womens-beach-cover-up`, `temu-womens-beach-cover-up-0469`, `temu-womens-beach-cover-up-2697`, `temu-womens-beach-cover-up-7071`, `temu-womens-beach-cover-up-1987` | distinct URLs — seller-variant or relist; needs goods pass |
| women's elegant maxi dress | 4 | `temu-womens-elegant-maxi-dress`, `temu-womens-elegant-maxi-dress-9809`, `temu-womens-elegant-maxi-dress-9938`, `temu-womens-elegant-maxi-dress-2778` | distinct URLs — seller-variant or relist; needs goods pass |
| women's jewelry necklace | 4 | `temu-womens-jewelry-necklace`, `temu-womens-jewelry-necklace-1146`, `temu-womens-jewelry-necklace-5724`, `temu-womens-jewelry-necklace-8551` | distinct URLs — seller-variant or relist; needs goods pass |
| women's earrings | 4 | `temu-womens-earrings`, `temu-womens-earrings-0124`, `temu-womens-earrings-9490`, `temu-womens-earrings-3517` | distinct URLs — seller-variant or relist; needs goods pass |
| skincare set serum | 4 | `temu-skincare-set-serum`, `temu-skincare-set-serum-1381`, `temu-skincare-set-serum-5031`, `temu-skincare-set-serum-6709` | distinct URLs — seller-variant or relist; needs goods pass |
| women's perfume fragrance | 4 | `temu-womens-perfume-fragrance`, `temu-womens-perfume-fragrance-2367`, `temu-womens-perfume-fragrance-9582`, `temu-womens-perfume-fragrance-2389` | distinct URLs — seller-variant or relist; needs goods pass |
| facial cleansing brush | 4 | `temu-facial-cleansing-brush`, `temu-facial-cleansing-brush-3639`, `temu-facial-cleansing-brush-0193`, `temu-facial-cleansing-brush-2317` | distinct URLs — seller-variant or relist; needs goods pass |
| women's scarf hijab | 4 | `temu-womens-scarf-hijab`, `temu-womens-scarf-hijab-4807`, `temu-womens-scarf-hijab-3855`, `temu-womens-scarf-hijab-3593` | distinct URLs — seller-variant or relist; needs goods pass |
| makeup sponge beauty blender | 4 | `temu-makeup-sponge-beauty-blender`, `temu-makeup-sponge-beauty-blender-8304`, `temu-makeup-sponge-beauty-blender-2949`, `temu-makeup-sponge-beauty-blender-7918` | distinct URLs — seller-variant or relist; needs goods pass |
| bathroom organizer shelf | 4 | `temu-bathroom-organizer-shelf`, `temu-bathroom-organizer-shelf-6012`, `temu-bathroom-organizer-shelf-9000`, `temu-bathroom-organizer-shelf-3552` | distinct URLs — seller-variant or relist; needs goods pass |
| rug carpet living room | 4 | `temu-rug-carpet-living-room`, `temu-rug-carpet-living-room-9946`, `temu-rug-carpet-living-room-7560`, `temu-rug-carpet-living-room-7562` | distinct URLs — seller-variant or relist; needs goods pass |
| ring light selfie | 4 | `temu-ring-light-selfie`, `temu-ring-light-selfie-4865`, `temu-ring-light-selfie-6425`, `temu-ring-light-selfie-1902` | distinct URLs — seller-variant or relist; needs goods pass |
| car accessories organizer | 4 | `temu-car-accessories-organizer`, `temu-car-accessories-organizer-5323`, `temu-car-accessories-organizer-8908`, `temu-car-accessories-organizer-1795` | distinct URLs — seller-variant or relist; needs goods pass |
| women's ring jewelry | 4 | `temu-womens-ring-jewelry`, `temu-womens-ring-jewelry-3688`, `temu-womens-ring-jewelry-9713`, `temu-womens-ring-jewelry-4711` | distinct URLs — seller-variant or relist; needs goods pass |
| women's puffer jacket winter | 4 | `temu-womens-puffer-jacket-winter`, `temu-womens-puffer-jacket-winter-9047`, `temu-womens-puffer-jacket-winter-5597`, `temu-womens-puffer-jacket-winter-9479` | distinct URLs — seller-variant or relist; needs goods pass |
| women's hoodie sweatshirt | 4 | `temu-womens-hoodie-sweatshirt`, `temu-womens-hoodie-sweatshirt-1678`, `temu-womens-hoodie-sweatshirt-9935`, `temu-womens-hoodie-sweatshirt-8364` | distinct URLs — seller-variant or relist; needs goods pass |
| womens casual two piece set featuring a color design with printed patterns long sleeves... | 3 | `temu-womens-casual-two-piece-set-featuring-a-color-desi`, `temu-womens-casual-two-piece-set-featuring-a-color-desi-2`, `temu-womens-casual-two-piece-set-featuring-a-color-desi-3` | distinct URLs — seller-variant or relist; needs goods pass |
| item picture ladies elegant and exquisite collar chinese black and white contrast spell... | 3 | `temu-item-picture-ladies-elegant-and-exquisite-collar-c`, `temu-item-picture-ladies-elegant-and-exquisite-collar-c-2`, `temu-item-picture-ladies-elegant-and-exquisite-collar-c-3` | distinct URLs — seller-variant or relist; needs goods pass |
| elegant dress set geometric pattern print fashionable vacation outer jacket vest maxi d... | 3 | `temu-elegant-dress-set-geometric-pattern-print-fashiona`, `temu-elegant-dress-set-geometric-pattern-print-fashiona-2`, `temu-elegant-dress-set-geometric-pattern-print-fashiona-3` | distinct URLs — seller-variant or relist; needs goods pass |
| wireless earbuds headphones | 3 | `temu-wireless-earbuds-headphones`, `temu-wireless-earbuds-headphones-5094`, `temu-wireless-earbuds-headphones-2310` | distinct URLs — seller-variant or relist; needs goods pass |
| smart watch fitness | 3 | `temu-smart-watch-fitness`, `temu-smart-watch-fitness-0720`, `temu-smart-watch-fitness-4193` | distinct URLs — seller-variant or relist; needs goods pass |
| women's sandals slippers | 3 | `temu-womens-sandals-slippers`, `temu-womens-sandals-slippers-0729`, `temu-womens-sandals-slippers-0122` | distinct URLs — seller-variant or relist; needs goods pass |
| lipstick makeup beauty | 3 | `temu-lipstick-makeup-beauty`, `temu-lipstick-makeup-beauty-4172`, `temu-lipstick-makeup-beauty-7078` | distinct URLs — seller-variant or relist; needs goods pass |
| women's abaya modest dress | 3 | `temu-womens-abaya-modest-dress`, `temu-womens-abaya-modest-dress-6882`, `temu-womens-abaya-modest-dress-0610` | distinct URLs — seller-variant or relist; needs goods pass |
| women's denim jeans | 3 | `temu-womens-denim-jeans`, `temu-womens-denim-jeans-9297`, `temu-womens-denim-jeans-1098` | distinct URLs — seller-variant or relist; needs goods pass |
| blue plaid belted maxi shirt dress | 3 | `temu-blue-plaid-belted-maxi-shirt-dress-b4-006`, `temu-blue-plaid-belted-maxi-shirt-dress-b4-011`, `temu-blue-plaid-belted-maxi-shirt-dress-b4-033` | distinct URLs — seller-variant or relist; needs goods pass |
| white statement flower ruffle sleeve blouse | 3 | `temu-white-statement-flower-ruffle-sleeve-blouse-b4-016`, `temu-white-statement-flower-ruffle-sleeve-blouse-b4-020`, `temu-white-statement-flower-ruffle-sleeve-blouse-b4-037` | distinct URLs — seller-variant or relist; needs goods pass |
| gold metallic one-shoulder top 2pcs party set | 3 | `temu-gold-metallic-one-shoulder-top-2pcs-party-set-b4-023`, `temu-gold-metallic-one-shoulder-top-2pcs-party-set-b4-032`, `temu-gold-metallic-one-shoulder-top-2pcs-party-set-b4-054` | distinct URLs — seller-variant or relist; needs goods pass |
| gold bracelet women's | 3 | `temu-gold-bracelet-womens`, `temu-gold-bracelet-womens-9286`, `temu-gold-bracelet-womens-1988` | distinct URLs — seller-variant or relist; needs goods pass |
| eyeshadow palette makeup | 3 | `temu-eyeshadow-palette-makeup`, `temu-eyeshadow-palette-makeup-8237`, `temu-eyeshadow-palette-makeup-8946` | distinct URLs — seller-variant or relist; needs goods pass |
| hair straightener curler | 3 | `temu-hair-straightener-curler`, `temu-hair-straightener-curler-0703`, `temu-hair-straightener-curler-2639` | distinct URLs — seller-variant or relist; needs goods pass |
| women's anklet bracelet | 3 | `temu-womens-anklet-bracelet`, `temu-womens-anklet-bracelet-5811`, `temu-womens-anklet-bracelet-6700` | distinct URLs — seller-variant or relist; needs goods pass |
| women's underwear lingerie set | 3 | `temu-womens-underwear-lingerie-set`, `temu-womens-underwear-lingerie-set-4096`, `temu-womens-underwear-lingerie-set-4541` | distinct URLs — seller-variant or relist; needs goods pass |
| women's winter boots | 3 | `temu-womens-winter-boots`, `temu-womens-winter-boots-1487`, `temu-womens-winter-boots-1561` | distinct URLs — seller-variant or relist; needs goods pass |
| women's sports bra | 3 | `temu-womens-sports-bra`, `temu-womens-sports-bra-1371`, `temu-womens-sports-bra-4305` | distinct URLs — seller-variant or relist; needs goods pass |
| women's wallet purse | 3 | `temu-womens-wallet-purse`, `temu-womens-wallet-purse-4301`, `temu-womens-wallet-purse-8247` | distinct URLs — seller-variant or relist; needs goods pass |
| pearl necklace jewelry set | 3 | `temu-pearl-necklace-jewelry-set`, `temu-pearl-necklace-jewelry-set-4235`, `temu-pearl-necklace-jewelry-set-0095` | distinct URLs — seller-variant or relist; needs goods pass |
| platform loafers for women | 2 | `temu-platform-loafers-for-women`, `temu-platform-loafers-for-women-543696` | distinct URLs — seller-variant or relist; needs goods pass |
| creation lamis everyone perfume for men 100ml - premium long lasting fragrance | 2 | `daraz-real-creation-lamis-everyone-men-100ml`, `daraz-real-creation-lamis-everyone-men-100ml-v2` | distinct URLs — seller-variant or relist; needs goods pass |
| pack of 4 watch set for men & boys - steel quartz, bracelet, ring & locket | 2 | `daraz-real-pack4-watch-set-men-boys`, `daraz-real-pack4-watch-set-bracelet-locket` | distinct URLs — seller-variant or relist; needs goods pass |
| 3pcs fashion synthetic zirconia imitation pendant earrings and necklace set | 2 | `temu-3pcs-fashion-synthetic-zirconia-jewelry-set`, `temu-3pcs-zirconia-earrings-necklace-set` | distinct URLs — seller-variant or relist; needs goods pass |
| double cabinet dish drying rack over sink steel | 2 | `daraz-double-cabinet-dish-drying-rack`, `daraz-double-cabinet-dish-drying-rack-over-sink-steel` | distinct URLs — seller-variant or relist; needs goods pass |
| 3-tier kitchen organizer rolling utility cart | 2 | `daraz-3tier-kitchen-organizer-rolling`, `daraz-3-tier-kitchen-organizer-rolling-utility-cart` | distinct URLs — seller-variant or relist; needs goods pass |
| women's ribbed underwear multi-color (1pc random) | 2 | `temu-s-ribbed-underwear-multi-color-1pc-p007`, `temu-s-ribbed-underwear-multi-color-1pc-p035` | distinct URLs — seller-variant or relist; needs goods pass |
| women's seamless underwear multi-color (1pc random) | 2 | `temu-s-seamless-underwear-multi-color-1pc-p010`, `temu-s-seamless-underwear-multi-color-1pc-p022` | distinct URLs — seller-variant or relist; needs goods pass |
| casual solid color double breasted decorative belt long sleeve womens cardigan relaxed ... | 2 | `temu-casual-solid-color-double-breasted-decorative-belt`, `temu-casual-solid-color-double-breasted-decorative-belt-2` | distinct URLs — seller-variant or relist; needs goods pass |
| women's bracelet watch | 2 | `temu-womens-bracelet-watch`, `temu-womens-bracelet-watch-6554` | distinct URLs — seller-variant or relist; needs goods pass |
| hair styling tools | 2 | `temu-hair-styling-tools`, `temu-hair-styling-tools-2668` | distinct URLs — seller-variant or relist; needs goods pass |
| kitchen gadgets organizer | 2 | `temu-kitchen-gadgets-organizer`, `temu-kitchen-gadgets-organizer-8296` | distinct URLs — seller-variant or relist; needs goods pass |
| air fryer accessories | 2 | `temu-air-fryer-accessories`, `temu-air-fryer-accessories-6794` | distinct URLs — seller-variant or relist; needs goods pass |
| home storage boxes | 2 | `temu-home-storage-boxes`, `temu-home-storage-boxes-7330` | distinct URLs — seller-variant or relist; needs goods pass |
| women's blouse tops | 2 | `temu-womens-blouse-tops`, `temu-womens-blouse-tops-1373` | distinct URLs — seller-variant or relist; needs goods pass |
| women's wide leg pants | 2 | `temu-womens-wide-leg-pants`, `temu-womens-wide-leg-pants-3368` | distinct URLs — seller-variant or relist; needs goods pass |
| women's sweater cardigan | 2 | `temu-womens-sweater-cardigan`, `temu-womens-sweater-cardigan-6554` | distinct URLs — seller-variant or relist; needs goods pass |
| stainless steel hammered non-stick frying pan | 2 | `temu-stainless-steel-hammered-non-stick-frying-pan-b4-001`, `temu-stainless-steel-hammered-non-stick-frying-pan-b4-009` | distinct URLs — seller-variant or relist; needs goods pass |
| women's knee-high slouch boots with buckle strap | 2 | `temu-women-s-knee-high-slouch-boots-with-buckle-strap-b4-003`, `temu-women-s-knee-high-slouch-boots-with-buckle-strap-b4-030` | distinct URLs — seller-variant or relist; needs goods pass |
| red tartan plaid pleated maxi skirt | 2 | `temu-red-tartan-plaid-pleated-maxi-skirt-b4-004`, `temu-red-tartan-plaid-pleated-maxi-skirt-b4-007` | distinct URLs — seller-variant or relist; needs goods pass |
| black pinstripe blazer & wide-leg pants suit set | 2 | `temu-black-pinstripe-blazer-wide-leg-pants-suit-set-b4-017`, `temu-black-pinstripe-blazer-wide-leg-pants-suit-set-b4-046` | distinct URLs — seller-variant or relist; needs goods pass |
| 100,000 whys kids science book set — 5 volumes | 2 | `temu-100-000-whys-kids-science-book-set-5-volumes-b4-019`, `temu-100-000-whys-kids-science-book-set-5-volumes-b4-036` | distinct URLs — seller-variant or relist; needs goods pass |
| outdoor insulated cat house pet shelter | 2 | `temu-outdoor-insulated-cat-house-pet-shelter-b4-021`, `temu-outdoor-insulated-cat-house-pet-shelter-b4-040` | distinct URLs — seller-variant or relist; needs goods pass |
| lavender butterfly print hoodie & joggers set | 2 | `temu-lavender-butterfly-print-hoodie-joggers-set-b4-048`, `temu-lavender-butterfly-print-hoodie-joggers-set-b4-052` | distinct URLs — seller-variant or relist; needs goods pass |
| hoop earrings women's | 2 | `temu-hoop-earrings-womens`, `temu-hoop-earrings-womens-8775` | distinct URLs — seller-variant or relist; needs goods pass |
| hair dryer brush | 2 | `temu-hair-dryer-brush`, `temu-hair-dryer-brush-9211` | distinct URLs — seller-variant or relist; needs goods pass |
| kitchen knife set | 2 | `temu-kitchen-knife-set`, `temu-kitchen-knife-set-8578` | distinct URLs — seller-variant or relist; needs goods pass |
| women's party evening dress | 2 | `temu-womens-party-evening-dress`, `temu-womens-party-evening-dress-1909` | distinct URLs — seller-variant or relist; needs goods pass |
| bed sheets pillowcase set | 2 | `temu-bed-sheets-pillowcase-set`, `temu-bed-sheets-pillowcase-set-9447` | distinct URLs — seller-variant or relist; needs goods pass |
| bluetooth speaker portable | 2 | `temu-bluetooth-speaker-portable`, `temu-bluetooth-speaker-portable-8937` | distinct URLs — seller-variant or relist; needs goods pass |
| led desk lamp | 2 | `temu-led-desk-lamp`, `temu-led-desk-lamp-7163` | distinct URLs — seller-variant or relist; needs goods pass |
| women's hair clips accessories | 2 | `temu-womens-hair-clips-accessories`, `temu-womens-hair-clips-accessories-5775` | distinct URLs — seller-variant or relist; needs goods pass |
| women's belt fashion | 2 | `temu-womens-belt-fashion`, `temu-womens-belt-fashion-6799` | distinct URLs — seller-variant or relist; needs goods pass |
| women's trench coat | 2 | `temu-womens-trench-coat`, `temu-womens-trench-coat-0637` | distinct URLs — seller-variant or relist; needs goods pass |
| women's tank top camisole | 2 | `temu-womens-tank-top-camisole`, `temu-womens-tank-top-camisole-3464` | distinct URLs — seller-variant or relist; needs goods pass |
| review details | 2 | `temu-review-details`, `temu-review-details-3694` | distinct URLs — seller-variant or relist; needs goods pass |
| clip in hair extensions hair extensions thick long lace weft | 2 | `temu-clip-in-hair-extensions-hair-extensions-thick-long-lace-weft`, `temu-clip-in-hair-extensions-hair-extensions-thick-long-lace-weft-2` | distinct URLs — seller-variant or relist; needs goods pass |
| spice carousel set featuring 20 spice jars kitchen spice | 2 | `temu-spice-carousel-set-featuring-20-spice-jars-kitchen-spice`, `temu-spice-carousel-set-featuring-20-spice-jars-kitchen-spice-2` | distinct URLs — seller-variant or relist; needs goods pass |
| 10 000mah mobile phone power bank charger 2 4a | 2 | `temu-10-000mah-mobile-phone-power-bank-charger-2-4a`, `temu-10-000mah-mobile-phone-power-bank-charger-2-4a-9347` | identical URL — in C1 |
| aura bracelet chakra lotus jewelry featuring 6mm rose quartz | 2 | `temu-aura-bracelet-chakra-lotus-jewelry-featuring-6mm-rose-quartz`, `temu-aura-bracelet-chakra-lotus-jewelry-featuring-6mm-rose-quartz-0402` | identical URL — in C1 |

Recommendation: (1) Qasim approves removing the 17 B-records above; (2) one browser adjudication pass extracts goods_ids for the 98 groups and merges only same-goods twins (keep richer record: image + canonical category + longer description); (3) no name-only deletions ever.

---
# D. Verified vs unverified ledger

| Figure | Status | Basis |
|---|---|---|
| Live catalog total 6,718 | [verified] | live products.json fetch + staged file, both counted |
| Category fixes applied: 163 | [verified] | applied by script on hash-backed-up copy; per-product changelog |
| Image fixes applied: 58 Daraz | [verified] | og:image from each product's own page; HEAD 200 image/*; names matched |
| Temu missing-image: 27 | [verified] | 2 goods pages fetched: no static image tags; full 27 flagged from catalog scan |
| Known broken mascara image still 404 | [verified] | HEAD fetched this run |
| Unmapped after fixes: 667 | [verified] | recount on live products.json after deploy |
| Hard duplicates: 17 pairs | [verified] | identical affiliate_url strings in catalog; goods_ids from URL |
| Exact-name groups: 100 / 353 records | [verified] | grouped on stripped lowercase name |
| ≈33 broken images catalog-wide | [estimate] | extrapolated from Phase A 1/200 sample — full sweep NOT done |
| Category landing-page conversion/CTR uplift from fixes | NOT VERIFIED | no analytics available (GSC verification pending on Qasim's side) |
| Price/rating correctness of any listing | NOT VERIFIED | out of scope; prices not shown or asserted anywhere in this run |

**Bottom line:** the catalog is structurally clean enough to resume controlled expansion once Qasim decides the two plan-only items (new Electronics/Toys pages; 17-pair dedup approvals). Remaining catalog hygiene backlog: 27 Temu images (browser pass), 1 known 404 image, 100 name groups pending adjudication, ≈22 stale item pages from Phase A (prune only with approval).

---
# E. Follow-through addendum (2026-10-09, later run)

- **Live verification of all permitted fixes completed**: 31/31 sampled category-mapped products live-verified at their new landing ids with item page 200 + image; 25/25 sampled Daraz image fixes live-verified (page 200, correct image URL, image HEAD 200). Full evidence: [p1-live-verification-20261009.md](sandbox://workspace/affiliate-site/hidden_files/p1-live-verification-20261009.md).
- **667 unmapped products recounted live** (electronics 525 · toys 95 · health 35 · Phone Accessories 3 · Electronics 3 · Mobile Accessories 3 · toys-wellness 2 · Health 1) with per-group landing-page recommendations in [p1-unmapped-recommendations-20261009.md](sandbox://workspace/affiliate-site/hidden_files/p1-unmapped-recommendations-20261009.md). **No new pages created; no structural SEO change made.**
- **Duplicate reconciliation (99 vs 100)**: both counts correct for their catalog states — 99 groups / 351 records at 6,640 (Phase A) → 100 groups / 353 records at 6,718. Batch 1 created the extra group: `temu-platform-loafers-for-women` (batch-1 addition) pairs with pre-existing `temu-platform-loafers-for-women-543696`; distinct affiliate URLs → genuine seller variant, joins the 98 adjudication groups above. Evidence: expansion backup vs p1mapping backup, identical grouping method. No grouping-method change; no deletion or merge anywhere.
- **Temu 27 missing images**: re-attempted via the established public-GET recipe this run; Temu served a generic verification shell (no product JSON extractable; no CAPTCHA presented, none attempted). **0 fixed; all 27 remain "blocked — needs one browser session."** No data was modified for these products. Known 404 mascara image independently re-verified: **still 404**.
- **Nothing new deleted, merged, or repointed; no new landing pages; no structural changes.** Expansion remains paused pending Qasim's decision on the plan-only items.
