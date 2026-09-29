#!/usr/bin/env python3
"""Stage Round 3 accepted Temu products (2026-09-29) into products.json + pins.json.
Same pattern as Round 2 staging: honest data only, original merchant images."""
import json, re, os, urllib.request

BASE = os.path.expanduser('~/workspace/affiliate-site')
PINS_DIR = os.path.expanduser('~/workspace/pinterest-affiliate')

accepted = json.load(open(f'{BASE}/tools/tracked-links-2026-09-29-r3.json'))  # {name: tracked_link}
temu_cands = {c['name']: c for c in json.load(open(f'{BASE}/tools/temu-candidates-2026-09-29-r3.json'))}

SUBCATS = {
    "Women's Satin Lace-Trim Midi Skirt with Front Slit": ('fashion', 'bottoms'),
    "Hydrocolloid Pimple Patch Multipack": ('trending', None),
    "Women's Geometric Cable Cardigan with Buttons": ('fashion', 'outerwear'),
    "Women's Slip-On Canvas Loafers": ('shoes', 'flats'),
    "Personalized Heart Initial Pendant Necklace": ('jewelry', 'necklaces'),
    "Bohemian Beaded Anklet Set with Pearl and Shell": ('jewelry', 'bracelets'),
    "LED Vanity Makeup Mirror": ('beauty', 'face'),
    "Portable Nano Facial Steamer": ('skincare', 'treatments'),
    "Large Matte Claw Clips Set": ('hair', 'accessories'),
    "Bohemian Straw Sun Hat": ('accessories', 'hats'),
    "Pashmina Shawl Wrap": ('accessories', 'scarves'),
    "High-Waist Tummy Control Shapewear Shorts": ('lingerie', 'shapewear'),
    "Pilates Bar Resistance Kit": ('fitness', 'gear'),
}

def slugify(name, merchant):
    s = f"{merchant}-{name}".lower()
    s = re.sub(r"['\u2019]", "", s)
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
for name, tracked_link in accepted.items():
    if name.lower() in existing_names:
        skipped.append((name, 'duplicate name'))
        continue
    cand = temu_cands.get(name)
    if not cand:
        skipped.append((name, 'no candidate data'))
        continue
    merchant = 'temu'
    category, subcategory = SUBCATS.get(name, (cand['category'], None))
    pid = slugify(name, merchant)
    n = 2
    base_pid = pid
    while pid in existing_ids:
        pid = f"{base_pid}-{n}"[:71].rstrip('-')
        n += 1
    img_url = cand['image_url']
    ext = '.jpg'
    if '.png' in img_url.lower().split('?')[0]:
        ext = '.png'
    site_img = f'{img_dir}/{pid}{ext}'
    ok = download(img_url, site_img)
    if not ok:
        skipped.append((name, 'image download failed'))
        continue
    merchant_label = 'Temu'
    features = cand.get('key_features', [])
    pros = cand.get('pros', [])
    rec = {
        'id': pid,
        'name': name,
        'merchant': merchant,
        'category': category,
        'subcategory': subcategory,
        'affiliate_url': tracked_link,
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
json.dump(summary, open(f'{BASE}/tools/staged-2026-09-29-r3.json', 'w'), indent=2)
print(f"STAGED: {len(staged)} | PINS: {len(pin_records)} | SKIPPED: {len(skipped)}")
for s in skipped: print('SKIPPED:', s)
print('TOTAL PRODUCTS:', len(data['products']), '| TOTAL PINS:', len(pins))
