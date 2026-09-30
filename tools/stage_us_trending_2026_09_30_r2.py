#!/usr/bin/env python3
"""Stage 2026-09-30 US-trending Temu batch (round 2): portal-verified products.
Discovery: 18 browser-verified buyable (Quick Look modal), $10+, merchant images.
Fill AFF_LINKS (product number -> temu.to/k/... link) before running.
Honest data only. No prices stored (site 'Price varies' convention)."""
import json, re, os, subprocess

BASE = os.path.expanduser('~/workspace/affiliate-site')
TODAY = '2026-09-30'
K = "https://img.kwcdn.com/"
Q = "?imageView2/2/w/800/q/70/format/avif"

# --- FILL THESE IN from the portal convert-link handoff (1-18) ---
# Round-2 handoff 2026-09-30 11:08 UTC: 16 ok, #1 and #14 FAILED (not eligible)
AFF_LINKS = {
 2: "https://temu.to/k/pzjugvy7hmr",
 3: "https://temu.to/k/pm11gdcuy9r",
 4: "https://temu.to/k/p6r4x0ccjub",
 5: "https://temu.to/k/ptu32x2bs7h",
 6: "https://temu.to/k/pszolwaf936",
 7: "https://temu.to/k/p0e10x4omvv",
 8: "https://temu.to/k/pkrliejmrey",
 9: "https://temu.to/k/pry4ys33op8",
 10: "https://temu.to/k/pqtgq46dgme",
 11: "https://temu.to/k/pke1pemqy67",
 12: "https://temu.to/k/pxbugvvwwn1",
 13: "https://temu.to/k/pvk6wvhabl1",
 15: "https://temu.to/k/prwqnjkfycl",
 16: "https://temu.to/k/pvwk1dd7i46",
 17: "https://temu.to/k/p4vry6x2j0u",
 18: "https://temu.to/k/pnxouxjvf73",
}

def C(n, name, gid, img, cat, sub, trend):
    return dict(n=n, name=name, goods_id=gid, img=img,
                category=cat, subcategory=sub, trend=trend)

SH = "Trending bestseller in Women's Shoes on Temu"
JW = "Trending in Women's Jewelry on Temu"
AC = "Trending in Women's Accessories on Temu"
HR = "Trending in Hair Care & Styling on Temu"
BT = "Trending in Beauty on Temu"
CANDIDATES = [
 C(1, "Nike Air Force 1 Low '07 SE Women's Sneaker, Rust Pink / Metallic Red Bronze",
   "603028262329513", K+"local-goods-image/21137b23908/2d198e27-3184-4e86-ba7c-b38a5395a33a_1023x1023.png"+Q,
   "shoes", "sneakers", SH),
 C(2, "Velvet Double-Buckle Mary Jane Ballet Flats for Women",
   "607153335200696", K+"product/open/52d0d3e74cc544e39b3698c505366072-goods.jpeg"+Q,
   "shoes", None, SH),
 C(3, "Vans Checkerboard Slip-On, Black / Off White",
   "602775933025001", K+"local-goods-image/d5896f31/5c869586-8bc3-40c0-a009-3b67a16b0e14.jpeg"+Q,
   "shoes", "sneakers", SH),
 C(4, "UGG Tazz Slipper 'Chestnut' for Women",
   "610650579386096", K+"local-goods-image/217a7c2178/1f8820fa-f0b8-4188-97df-f2eed9d9004e_1254x1254.png"+Q,
   "shoes", None, SH),
 C(5, "Women's Western Cowgirl Boots, Embroidered Pointed Toe Knee-High",
   "606992072591837", K+"product/open/0a77d20d1d62481cb5ebd5a9eb6e4897-goods.jpeg"+Q,
   "shoes", "boots", SH),
 C(6, "Women's Knee-High Lace-Up Hollow Flat Sandals, Black",
   "607329764401505", K+"product/open/16b12945c4cc45c68d79a6955ba2ee78-goods.jpeg"+Q,
   "shoes", "sandals", SH),
 C(7, "Red Pointed-Toe Stiletto Wedding Heels for Women",
   "601103333920697", K+"product/fancy/e94402a7-f466-4aa4-9e90-19af0b1748f7.jpg"+Q,
   "shoes", "heels", SH),
 C(8, "Swarovski Matrix Pink Crystal Bracelet for Women",
   "610843316083737", K+"local-goods-image/4202d0e1/6762fb91-3b7b-4e20-b0b1-1b7bdda2475a/bbc89baf015724a53b0e4d1754e0136a.jpeg"+Q,
   "jewelry", "bracelets", JW),
 C(9, "Marc Jacobs Dark Tortoise Sunglasses for Women",
   "602578364530817", K+"local-goods-image/8b16267f/f296ab32-b78a-4efd-8f3c-79912c94bfea/25be66713834a0b1933f2ff7ad34339d.jpeg"+Q,
   "accessories", None, AC),
 C(10, "Invicta Pro Diver Women's Watch, Silver Tone with Blue Bezel",
   "603264485549652", K+"local-goods-image/5d82be7/571c7cd3-506e-4c93-b83b-8763130b42eb/1a11ccf89021ffd19691f19c26c5005f.jpeg"+Q,
   "accessories", None, AC),
 C(11, "Marc Jacobs Beige Black Sunglasses for Women, 55mm",
   "610368722173810", K+"local-goods-image/82a75ee6/3bfd57ae-95e6-4e66-a817-8da6faada9ec.jpeg"+Q,
   "accessories", None, AC),
 C(12, "Swarovski Dulcis Blue Crystal Earrings for Women",
   "610156121276911", K+"local-goods-image/a6cdea9/6495f32d-4071-4435-a165-77dc7932c1b5/6f98a2a00145f863f562a7b4ae1cbb35.jpeg"+Q,
   "jewelry", "earrings", JW),
 C(13, "Lacoste Neocroc Pink Dial Women's Watch, 38mm Silicone Strap",
   "610495960553116", K+"local-goods-image/e6a0b6cb/4990327a-b5a3-4779-9d50-dfd06368bd0d.jpeg"+Q,
   "accessories", None, AC),
 C(14, "BaBylissPRO Nano Titanium Oval Ionic Blowout Brush 2.5 inch",
   "602258020343009", K+"local-goods-image/de5b0898/6635a6f4-eb71-4c04-a7f7-7e7cea30e6ce.jpeg"+Q,
   "hair", None, HR),
 C(15, "13pcs Rhinestone-Studded Makeup Brush Set with Holder",
   "601101857514342", K+"product/fancy/0e193e03-a8e6-44a3-8ced-b1b1ee43e461.jpg"+Q,
   "beauty", None, BT),
 C(16, "Portable Cosmetic Bag for Women with Mirror and Removable Organizer",
   "606492145096098", K+"product/algo_framework/ImageCm2InAlgo/753690f8-e151-11f0-8750-0a580aa83d90.jpg"+Q,
   "beauty", None, BT),
 C(17, "BaBylissPRO Super Turbo Blow Dryer 2000W with 6 Heat and Speed Settings",
   "602327813603339", K+"local-goods-image/de8d0ba0/308ddafb-61a1-4ee-b583-3f21b17183de.jpeg"+Q,
   "hair", None, HR),
 C(18, "Alo Yoga Accolade Crew Neck Sweatshirt for Women",
   "602805997797154", K+"local-goods-image/217a7c329a/5c10059a-2d5b-4e66-a817-8da6faada9ec.jpeg.format.jpg"+Q,
   "fashion", "tops", "Trending bestseller in Women's Clothing on Temu"),
]

STOP = {'with','and','the','for','from','all','skin','set','dress','bag','piece','type','types',
        'women','women\'s','shoe','shoes'}
def toks(name):
    return [t for t in re.sub(r'[^a-z0-9 ]', ' ', name.lower()).split()
            if len(t) > 2 and t not in STOP]
def overlap_ratio(a, b):
    ta, tb = toks(a), toks(b)
    if not ta or not tb: return 0.0
    return len(set(ta) & set(tb)) / min(len(set(ta)), len(set(tb)))
def consec_run(a, b):
    ta, tb = toks(a), toks(b); sb = set(tb); best = cur = 0
    for t in ta:
        cur = cur + 1 if t in sb else 0; best = max(best, cur)
    return best
def is_dup(cand, others):
    for o in others:
        if consec_run(cand['name'], o['name']) >= 6: return o['name']
        if overlap_ratio(cand['name'], o['name']) >= 0.85: return o['name']
    return None
def slugify(name):
    s = re.sub(r"['\u2019]", "", f"temu-{name}".lower())
    return re.sub(r"[^a-z0-9]+", "-", s).strip('-')[:71].rstrip('-')
def download(url, dest):
    if os.path.exists(dest) and os.path.getsize(dest) > 0: return True
    try:
        r = subprocess.run(['curl', '-sL', '-f', '--retry', '2', '--retry-delay', '3',
            '-A', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
            '--max-time', '90', '-o', dest, url], capture_output=True, timeout=120)
        return r.returncode == 0 and os.path.exists(dest) and os.path.getsize(dest) > 0
    except Exception as e:
        print(f'DOWNLOAD FAILED #{cand_n}: {e}'); return False

data = json.load(open(f'{BASE}/data/products.json'))
existing_ids = {p['id'] for p in data['products']}
existing_affs = {p['affiliate_url'] for p in data['products']}
img_dir = f'{BASE}/images'; os.makedirs(img_dir, exist_ok=True)

staged, skipped, seen = [], [], []
for cand in CANDIDATES:
    cand_n = cand['n']; name = cand['name']
    aff = AFF_LINKS.get(cand_n)
    if not aff:
        skipped.append((name, 'no affiliate link')); continue
    if aff in existing_affs:
        skipped.append((name, 'affiliate URL collision')); continue
    d = is_dup(cand, data['products'])
    if d: skipped.append((name, f'duplicate of staged: {d[:60]}')); continue
    d2 = is_dup(cand, seen)
    if d2: skipped.append((name, f'near-duplicate in batch: {d2[:60]}')); continue
    pid, base, n = slugify(name), None, 2
    base = pid
    while pid in existing_ids:
        pid = f"{base}-{n}"[:71].rstrip('-'); n += 1
    if not download(cand['img'], f'{img_dir}/{pid}.jpg'):
        skipped.append((name, 'image download failed')); continue
    rec = {'id': pid, 'name': name, 'merchant': 'temu', 'category': cand['category'],
        'subcategory': cand['subcategory'], 'affiliate_url': aff,
        'image_url': cand['img'], 'key_features': [cand['trend']],
        'pros': [f"Trending find on Temu \u2014 {cand['trend']}"], 'cons': [
            'Temu prices change frequently \u2014 confirm the live price before buying',
            'Check the live Temu listing for current colors and sizes'],
        'badges': ['new'], 'rating': None, 'sold_count': None, 'sample': False,
        'short_description': f"{name} \u2014 {cand['trend']}",
        'source': f'Temu public listing \u2014 verified {TODAY}',
        'trend_status': 'trending', 'updated': TODAY}
    data['products'].append(rec)
    existing_ids.add(pid); existing_affs.add(aff); seen.append(cand)
    staged.append(rec)

with open(f'{BASE}/data/products.json', 'w') as f:
    json.dump(data, f, indent=2, ensure_ascii=False)
json.dump({'staged': [{'id': p['id'], 'name': p['name'], 'category': p['category'],
    'affiliate_url': p['affiliate_url']} for p in staged],
    'skipped': skipped, 'total_products': len(data['products'])},
    open(f'{BASE}/tools/staged-us-trending-2026-09-30-r2.json', 'w'), indent=2)
print(f"STAGED: {len(staged)} | SKIPPED: {len(skipped)}")
for s in skipped: print('SKIPPED:', s[0][:55], '->', s[1][:70])
print('TOTAL PRODUCTS:', len(data['products']))
