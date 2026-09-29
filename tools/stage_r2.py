#!/usr/bin/env python3
"""Stage Round 2 accepted products (2026-09-29) into products.json + pins.json.
Same pattern as Round 1 staging: honest data only, original merchant images."""
import json, re, os, urllib.request

BASE = os.path.expanduser('~/workspace/affiliate-site')
PINS_DIR = os.path.expanduser('~/workspace/pinterest-affiliate')

accepted = json.load(open(f'{BASE}/tools/tracked-links-2026-09-29-r2.json'))
temu_cands = {c['name']: c for c in json.load(open(f'{BASE}/tools/temu-candidates-2026-09-29-r2.json'))}
alx_cands = {c['name']: c for c in json.load(open(f'{BASE}/tools/aliexpress-candidates-2026-09-29-r2.json'))}

SUBCATS = {
    "2026 Women's Pocket Pleated Skirt": ('fashion', 'bottoms'),
    "3pcs Women's Pearl Necklace, Bracelet and Earrings Set": ('jewelry', 'jewelry-sets'),
    "Mermaid Tail Glass Jewelry Set": ('jewelry', 'jewelry-sets'),
    "2026 Women's Summer 3pcs Handbag Set": ('bags', 'tote'),
    "12-Color Smokey Eyeshadow Palette": ('beauty', 'face'),
    "30 Pairs Natural Wispy False Eyelashes": ('beauty', 'face'),
    "Vitamin C and Niacinamide Hyaluronic Acid Face Serum": ('skincare', 'serums'),
    "6-Pack Satin Scrunchies Set": ('hair', 'hair-accessories'),
    "12-Pack 35-Inch Satin Square Scarves": ('accessories', 'scarves'),
    "7pcs Wire-Free Bralette Set": ('lingerie', 'bralettes'),
    "3-Pack Women's High-Waisted Full-Length Leggings": ('fitness', 'bottoms'),
    "DONLEE QUEEN Women Flats Shoes Low Wooden": ('shoes', 'flats'),
}

def slugify(name, merchant):
    s = f"{merchant}-{name}".lower()
    s = re.sub(r"['’]", "", s)
    s = re.sub(r"[^a-z0-9]+", "-", s).strip('-')
    return s[:71].rstrip('-')

def download(url, dest):
    if os.path.exists(dest) and os.path.getsize(dest) > 0:
        return True
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req, timeout=60) as r, open(dest, 'wb') as f:
            f.write(r.read())
        return os.path.getsize(dest) > 0
    except Exception as e:
        print(f'DOWNLOAD FAILED {url}: {e}')
        return False

data = json.load(open(f'{BASE}/data/products.json'))
existing_ids = {p['id'] for p in data['products']}
existing_names = {p['name'].lower() for p in data['products']}

pins = json.load(open(f'{PINS_DIR}/pins.json'))
existing_pin_ids = {p['product_id'] for p in pins}

img_dir = f'{BASE}/images'
os.makedirs(img_dir, exist_ok=True)

staged, pin_records, skipped = [], [], []
for a in accepted:
    name = a['name']
    if name.lower() in existing_names:
        skipped.append((name, 'duplicate name'))
        continue
    cand = temu_cands.get(name) or alx_cands.get(name) or next(
        (c for c in alx_cands.values() if c['name'].startswith(name)), None)
    if not cand:
        skipped.append((name, 'no candidate data'))
        continue
    merchant = a['platform']
    category, subcategory = SUBCATS.get(name, (a.get('category') or cand['category'], None))
    pid = slugify(name, merchant)
    n = 2
    base_pid = pid
    while pid in existing_ids:
        pid = f"{base_pid}-{n}"[:71].rstrip('-')
        n += 1
    img_url = a['image_url'] or cand['image_url']
    ext = '.jpg'
    if '.png' in img_url.lower().split('?')[0]:
        ext = '.png'
    site_img = f'{img_dir}/{pid}{ext}'
    ok = download(img_url, site_img)
    if not ok:
        skipped.append((name, 'image download failed'))
        continue
    merchant_label = 'Temu' if merchant == 'temu' else 'AliExpress'
    features = cand.get('key_features', [])
    pros = cand.get('pros', [])
    rec = {
        'id': pid,
        'name': name,
        'merchant': merchant,
        'category': category,
        'subcategory': subcategory,
        'affiliate_url': a['tracked_link'],
        'image_url': img_url,
        'key_features': features,
        'pros': pros,
        'cons': [
            f'{merchant_label} prices change frequently — confirm the live price before buying',
            f'Check the live {merchant_label} listing for current colors and sizes',
        ],
        'badges': ['new'],
        'rating': None,
        'sold_count': None,
        'sample': False,
        'short_description': f"{name} — {features[0]}" if features else name,
        'source': f'{merchant_label} public listing — verified 2026-09-29',
        'trend_status': 'trending',
        'updated': '2026-09-29',
    }
    data['products'].append(rec)
    existing_ids.add(pid)
    existing_names.add(name.lower())
    staged.append(rec)

    # Pinterest pin record
    pin_dir = f'{PINS_DIR}/images/{merchant}'
    os.makedirs(pin_dir, exist_ok=True)
    pin_img = f'{pin_dir}/{pid}.jpg'
    ok2 = download(img_url, pin_img)
    desc = f"{name}. " + ' '.join(f'{f}.' for f in features[:2])
    desc = f"{desc} {' '.join(pros[:1])} Check the live price on {merchant_label}. (Affiliate link)"
    title = name if len(name) <= 80 else name[:77] + '...'
    if pid not in existing_pin_ids:
        pins.append({
            'product_id': pid,
            'title': title,
            'description': desc,
            'destination_url': f'https://qa-affiliate.vercel.app/product.html?id={pid}',
            'image_file': f'~/workspace/pinterest-affiliate/images/{merchant}/{pid}.jpg',
            'image_ready': ok2,
            'category': category,
        })
        pin_records.append(pid)

with open(f'{BASE}/data/products.json', 'w') as f:
    json.dump(data, f, indent=2, ensure_ascii=False)
with open(f'{PINS_DIR}/pins.json', 'w') as f:
    json.dump(pins, f, indent=2, ensure_ascii=False)

summary = {
    'staged': [{'id': p['id'], 'name': p['name'], 'merchant': p['merchant'],
                'category': p['category'], 'image_url': p['image_url'],
                'affiliate_url': p['affiliate_url']} for p in staged],
    'pin_records': pin_records,
    'skipped': skipped,
    'total_products': len(data['products']),
    'total_pins': len(pins),
}
json.dump(summary, open(f'{BASE}/tools/staged-2026-09-29-r2.json', 'w'), indent=2)
print(f"STAGED: {len(staged)} | PINS: {len(pin_records)} | SKIPPED: {len(skipped)}")
for s in skipped: print('SKIPPED:', s)
print('TOTAL PRODUCTS:', len(data['products']), '| TOTAL PINS:', len(pins))
