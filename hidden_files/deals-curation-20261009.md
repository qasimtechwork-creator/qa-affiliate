# Deals Curation — 2026-10-09

Selection rule (in order, capped at 60 total):
1. Badge includes `best-seller` (requires image_url + affiliate_url), sorted by rating desc, then sold_count desc.
2. `rating >= 4.7`, sorted by rating desc, then sold_count desc.
3. Fill only if the union above is < 60: `rating >= 4.5`, sorted by sold_count (parsed numeric) desc.

Dedupe: by `goods_id` where present, else product `id`. Records store no price; no discount, percentage-off or countdown framing is used anywhere — deal framing is verified bestseller / top-rated status only, with live price confirmed on Temu at checkout.

Selected: 60 products (`data/products.json` read-only, untouched).

| # | Product ID | Name | Category | Rating | Badges | Selection tier |
|---|-----------|------|----------|--------|--------|----------------|
| 1 | temu-makeup-brush-set-15 | 15pcs Makeup Brush Set — Blush, Powder, Concealer & Eyeshadow Brushes | beauty | 5 | best-seller, top-rated | best-seller badge |
| 2 | temu-4pcs-jewelry-set-necklace-earrings-ring | 4pcs Women's Pink Heart Jewelry Set - Necklace, Earrings and Ring, Elegant Gift for Valentine's Day and Weddings | jewelry | 5 | best-seller | best-seller badge |
| 3 | temu-genuine-leather-crossbody-bag-8-card-slots | Phone Crossbody Bag, Single Shoulder Bag with 8 Card Slots, ID and Document Holder, Women's Zippered Pocket, New Summer Litchi Pattern Cowhi | bags | 5 | best-seller | best-seller badge |
| 4 | temu-womens-breathable-slip-on-sneakers | Fashionable and Comfortable Mesh Breathable Slip-on Sneakers, Trendy Casual Outdoor Walking Shoes for Women | shoes | 5 | best-seller | best-seller badge |
| 5 | temu-hollow-heart-pendant-clavicle-necklace | Women's Hollow Heart Pendant Clavicle Necklace - Light Luxury Niche Design, Brass Gold-Plated | jewelry | 5 | best-seller | best-seller badge |
| 6 | temu-fashion-layered-necklace-14k | Women's Fashion Layered Necklace - 14K Golden Plated Cubic Zirconia Pendant | jewelry | 5 | best-seller | best-seller badge |
| 7 | temu-2-piece-satin-pillowcase-set | 2-Piece Satin Pillowcase Set for Skin and Hair - Soft Breathable Cooling | beauty | 4.9 | best-seller | best-seller badge |
| 8 | temu-white-sneakers | Women's Low-Top White Sneakers — Flat Sole Lace-Up, Round Toe | shoes | 4.9 | best-seller, top-rated | best-seller badge |
| 9 | temu-jewelry-set-elegant-geometric | Women's Jewelry Set - Elegant Geometric Link Necklace & Earrings, KC Golden Plated | jewelry | 4.9 | best-seller | best-seller badge |
| 10 | temu-elegant-womens-zipper-tote | Fashionable Women's Handbag, Elegant and Stylish Tote for Ladies | bags | 4.9 | best-seller | best-seller badge |
| 11 | temu-46pcs-makeup-tool-set-brushes | 46pcs Makeup Tool Set - Brushes, Toiletry Bag, Eyelash Curler, Sponges | beauty | 4.9 | best-seller | best-seller badge |
| 12 | temu-elegant-crossbody-phone-wallet | Women's Elegant Crossbody Phone Wallet Handbag - Multi-Layer Large Capacity, Magnetic Closure | bags | 4.9 | best-seller | best-seller badge |
| 13 | temu-v-neck-high-waist-floral-maxi-dress | Women's Elegant Floral Print Maxi Dress - V-Neck, Short Sleeves, High-Waisted Flowy A-Line | fashion | 4.9 | best-seller | best-seller badge |
| 14 | temu-vitamin-c-e-facial-capsules | 50 Vitamin C E Facial Essence Capsules - Concentrated Lifting Hydration, Firming Moisturizing Essence | beauty | 4.9 | best-seller | best-seller badge |
| 15 | temu-brazilian-arabian-four-piece-jewelry-set | Brazil/Arabia Popular 4pcs Set of Elegant Women's Jewelry Including Square Earrings, Rings, Pendant Necklace | jewelry | 4.9 | best-seller | best-seller badge |
| 16 | temu-vintage-luxury-4pcs-jewelry-set | 4pcs elegant artificial Women's jewelry set, featuring a vintage French classic style with luxurious design, including necklace, bracelet, a | jewelry | 4.9 | best-seller | best-seller badge |
| 17 | temu-precision-eye-makeup-brush-set-5pcs | Precision Eye Makeup Brush Set, 5pcs With Sickle-Shaped Eyeliner Brush, Angled Eyeliner Brush and Eyebrow Brush | beauty | 4.8 | best-seller, new | best-seller badge |
| 18 | temu-jade-roller-gua-sha | 3pcs Jade Roller & Gua Sha Set — Facial Massage Beauty Tools | skincare | 4.8 | best-seller | best-seller badge |
| 19 | temu-3-pack-s-sports-bras | 3-Pack Women's Sports Bras - High Support, No Padding, Seamless | fitness | 4.8 | best-seller | best-seller badge |
| 20 | temu-18pcs-heatless-hair-curler-set | 18pcs Heatless Hair Curler Set with Clips - Self-Adhesive No-Heat Curls for All Hair Lengths | hair | 4.8 | best-seller | best-seller badge |
| 21 | temu-square-pendant-and-teardrop-earrings-jewelry-set | Elegant Women's Jewelry Set - Chic Square Pendant Necklace & Teardrop Earrings, Golden-Tone | jewelry | 4.8 | best-seller | best-seller badge |
| 22 | temu-smooth-lip-liner-gloss-set | Smooth Lip Liner and Gloss Set Lip Combo - Long-Lasting, Vibrant Color | beauty | 4.8 | best-seller | best-seller badge |
| 23 | temu-set-8-liquid-matte-lipsticks | Set of 8 Liquid Matte Lipsticks - Long-Lasting Waterproof, Pink & Red Tones | beauty | 4.8 | best-seller | best-seller badge |
| 24 | temu-sophisticated-jewelry-set | Sophisticated Jewelry Set — Rhinestone Necklace & Earrings, Vintage Luxe Style | jewelry | 4.8 | best-seller | best-seller badge |
| 25 | temu-5-pair-sparkling-golden-hoop | 5-Pair Sparkling Golden Hoop Earrings Set for Women - Multi-Piece Jewelry | jewelry | 4.8 | best-seller | best-seller badge |
| 26 | temu-high-waist-seamless-yoga | Women's High-Waist Seamless Yoga & Workout Leggings - Stretchy Solid Pants for Running | fitness | 4.8 | best-seller | best-seller badge |
| 27 | temu-20-vitamin-c-and-hyaluronic-serum | 30ml 20% Vitamin C Liquid Serum with Hyaluronic Acid - Brightening Moisturizing Face Serum | beauty | 4.8 | best-seller | best-seller badge |
| 28 | temu-platform-open-toe-wedge-sandals | Women's Platform Open-Toe Wedge Sandals - Lightweight Summer Casual with Sequin Accents | shoes | 4.8 | best-seller | best-seller badge |
| 29 | temu-pink-french-3d-bow-coffin-press-on-nails | 24pcs Pink French Press-On Nails - Long Coffin with 3D Bow and Rhinestones, Glossy Reusable | beauty | 4.8 | best-seller | best-seller badge |
| 30 | temu-5-pack-s-seamless-underwear | 5-Pack Women's Seamless Underwear - Low Waist Breathable Quick-Dry Briefs, Solid Color | lingerie | 4.8 | best-seller | best-seller badge |
| 31 | temu-2pcs-quilted-large-capacity-tote-bag | 2pcs Large Capacity Women's Tote Bag, New Quilted Bag, Trendy and Versatile Women's Handbag, Suitable for Work, Travel, Sports, and Gym, Lig | bags | 4.8 | best-seller | best-seller badge |
| 32 | temu-elegant-flowy-floral-maxi-dress | Women's Elegant Flowy Floral Maxi Dress - Formal and Casual Event Gown, Flared A-Line Skirt | fashion | 4.8 | best-seller | best-seller badge |
| 33 | temu-fashionable-golden-necklace-high-end | Fashionable Golden Necklace - Luxurious High-End Jewelry, Best Gift | jewelry | 4.8 | best-seller | best-seller badge |
| 34 | temu-2pcs-corduroy-tote-bag-hobo-crossbody | 2pcs Set: Women's Large Corduroy Tote Bag, Perfect as a Laptop Bag, Crossbody Shoulder Bag, Hobo Messenger Bag, Handbag, Travel Bag, Gym Tot | bags | 4.8 | best-seller | best-seller badge |
| 35 | temu-glutathione-niacinamide-hyaluronic-face-serum | Glutathione Brightening Face Serum with Niacinamide, Hyaluronic Acid and Vitamin C - Dark Spots and Fine Lines | beauty | 4.8 | best-seller | best-seller badge |
| 36 | temu-openwork-jacket | Women's Elegant Solid Color Openwork Jacket — 2026 Spring/Summer Cardigan | fashion | 4.8 | best-seller | best-seller badge |
| 37 | temu-shorts-3pack | 3-Pack Women's Solid Color Shorts — Elastic Waist with Side Pockets | fashion | 4.7 | best-seller | best-seller badge |
| 38 | temu-1-6m-extended-no-heat | 1.6m Extended No-Heat Hair Curling Rod for Women - Manual Overnight Curler for Braids & Ponytails | hair | 4.7 | best-seller | best-seller badge |
| 39 | temu-openwork-cropped-jacket | Summer Elegant Solid Color Openwork Knit Cropped Jacket | fashion | 4.7 | best-seller | best-seller badge |
| 40 | temu-multi-pocket-hot-selling-vintage | Multi-Pocket Hot Selling Vintage Crossbody Bag - Adjustable Shoulder Strap, Large Capacity | bags | 4.7 | best-seller | best-seller badge |
| 41 | temu-heatless-curling-and-satin-cap-set | 4/5pcs Women's Heatless Hair Curling Set with Glossy Cap, No-Heat Rollers, Clips & Rings | hair | 4.7 | best-seller | best-seller badge |
| 42 | temu-4pcs-s-high-support-seamless | 4pcs Women's High Support Seamless Sports Bras - Breathable Mesh Panels | fitness | 4.7 | best-seller | best-seller badge |
| 43 | temu-youngcome-vitamin-c-retinol-serum | YOUNGCOME Vitamin C Facial Serum with Retinol, Hyaluronic Acid and Aloe - Moisturizing Firming Serum | beauty | 4.7 | best-seller | best-seller badge |
| 44 | temu-purple-short-square-press-on-nails | 24pcs Short Square Press-On Nails - Purple Floral Design with Glossy Finish, Reusable | beauty | 4.7 | best-seller | best-seller badge |
| 45 | temu-pearl-tassel-necklace-bracelet-earrings-set | 3pcs Elegant Faux Imitation Pearl Jewelry Set for Women - Tassel Drop Earrings + Necklace + Bracelet | jewelry | 4.7 | best-seller | best-seller badge |
| 46 | temu-floral-short-oval-press-on-nails | 24pcs Square Press-on Nails Full Coverage Fake Nails - Short Oval French Nails, Multicolor Flowers | beauty | 4.7 | best-seller | best-seller badge |
| 47 | temu-bohemian-wide-strap-large-tote | Women's Fashion Solid Color Tote Bag, Large Capacity Bohemian Style Wide Woven Shoulder Bag | bags | 4.7 | best-seller | best-seller badge |
| 48 | temu-artistic-fashion-print-canvas-tote | Artistic Fashion Print Canvas Tote Bag with Removable Shoulder Strap - Zipper Closure | bags | 4.7 | best-seller | best-seller badge |
| 49 | temu-high-quality-stainless-steel-golden | High-Quality Stainless Steel Golden Layered Necklace for Women - Fade-Resistant | jewelry | 4.7 | best-seller | best-seller badge |
| 50 | temu-3-4fl-oz-s-luxury | 3.4fl.oz Women's Luxury Perfume - Long-Lasting Floral Scent, Golden Heart-Shaped Accent Bottle | beauty | 4.7 | best-seller | best-seller badge |
| 51 | temu-120-piece-pink-gradient-press-on-nails | 120pcs Square Press-On Nails Medium Length - Pink & White Gradient Glossy Fake Nails with Jelly Glue | beauty | 4.7 | best-seller | best-seller badge |
| 52 | temu-elegant-floral-print-line | Women's Elegant Floral Print A-Line Midi Dress - Short Sleeve, Round Neck, Beach Vacation Dress | fashion | 4.7 | best-seller | best-seller badge |
| 53 | temu-jewelry-set-4pcs | 4pcs Fashion Jewelry Set — Shining Earrings, Pendant Necklace & Ring | jewelry | 4.6 | best-seller | best-seller badge |
| 54 | temu-4pcs-commemorative-fashion-shining-earri | 4pcs Commemorative Fashion Shining Earrings Pendant Necklace Ring Set | jewelry | 4.6 | best-seller | best-seller badge |
| 55 | temu-large-handbag | Women's Large Capacity Handbag — Solid Color Faux-Leather Shoulder Bag | bags | 4.6 | best-seller | best-seller badge |
| 56 | temu-burgundy-short-almond-press-on-nails | 30pcs Luxury Burgundy Short Almond Shaped Press-On Nails Set - Glossy, Waterproof, Removable | beauty | 4.6 | best-seller | best-seller badge |
| 57 | temu-blue-moon-and-star-almond-press-on-nails | Almond Shaped Short Press-On Nails - Blue Moon and Star French Manicure, Glossy Removable | beauty | 4.6 | best-seller | best-seller badge |
| 58 | temu-professional-tote-bag-convertible | Women's Professional Tote Bag - Convertible Crossbody, Large Capacity Work Bag | bags | 4.6 | best-seller | best-seller badge |
| 59 | temu-luxury-magnetic-metal-phone-case-iphone-17-magsafe | Luxury Magnetic Metal Phone Case iPhone 17 MagSafe | electronics | 5.0 | trending | rating >= 4.7 |
| 60 | temu-spring-double-sided-pet-deshedding-brush | Spring Double-sided Pet Deshedding Brush | home | 4.9 | trending | rating >= 4.7 |
