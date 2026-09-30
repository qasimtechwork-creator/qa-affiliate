#!/usr/bin/env python3
"""Stage 2026-09-30 trending Temu batch into products.json + pins.json.
Portal-verified affiliate links + browser-verified merchant images.
Honest data only, original merchant images."""
import json, re, os, subprocess

BASE = os.path.expanduser('~/workspace/affiliate-site')
PINS_DIR = os.path.expanduser('~/workspace/pinterest-affiliate')
TODAY = '2026-09-30'

stage = json.load(open(f'{BASE}/hidden_files/trending-stage-final-2026-09-30.json'))
images = {x['goods_id']: x.get('image_url') for x in
          json.load(open(f'{BASE}/hidden_files/trending-images-2026-09-30.json'))}

def slugify(name, merchant):
    s = f"{merchant}-{name}".lower()
    s = re.sub(r"['\u2019]", "", s)
    s = re.sub(r"[^a-z0-9]+", "-", s).strip('-')
    return s[:71].rstrip('-')

def download(url, dest):
    if os.path.exists(dest) and os.path.getsize(dest) > 0:
        return True
    try:
        r = subprocess.run(
            ['curl', '-sL', '-f', '--retry', '3', '--retry-delay', '4',
             '-A', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
             '--max-time', '120', '-o', dest, url],
            capture_output=True, timeout=150)
        return r.returncode == 0 and os.path.exists(dest) and os.path.getsize(dest) > 0
    except Exception as e:
        print(f'DOWNLOAD FAILED {url[:80]}: {e}')
        return False

data = json.load(open(f'{BASE}/data/products.json'))
existing_ids = {p['id'] for p in data['products']}
existing_names = {p['name'].lower() for p in data['products']}

pins = json.load(open(f'{PINS_DIR}/pins.json'))
existing_pin_ids = {p['product_id'] for p in pins}

img_dir = f'{BASE}/images'
os.makedirs(img_dir, exist_ok=True)

def pros_cons_features(cand):
    trend = cand.get('trend_reason') or ''
    features = [trend] if trend else []
    pros = [f"Trending find with {trend}" if trend else "Trending find on Temu"]
    rating_match = re.search(r'(\d\.\d)\s*(star|rating)', str(trend))
    rating = float(rating_match.group(1)) if rating_match else None
    return features, pros, rating

staged, pin_records, skipped = [], [], []
for cand in stage:
    name = cand['name']
    if name.lower() in existing_names:
        skipped.append((name, 'duplicate name')); continue
    img_url = images.get(cand['goods_id'])
    if not img_url:
        skipped.append((name, 'no image')); continue
    pid = slugify(name, 'temu')
    n = 2
    base_pid = pid
    while pid in existing_ids:
        pid = f"{base_pid}-{n}"[:71].rstrip('-')
        n += 1
    ext = '.png' if '.png' in img_url.lower().split('?')[0] else '.jpg'
    site_img = f'{img_dir}/{pid}{ext}'
    if not download(img_url, site_img):
        skipped.append((name, 'image download failed')); continue
    features, pros, rating = pros_cons_features(cand)
    rec = {
        'id': pid,
        'name': name,
        'merchant': 'temu',
        'category': cand['category'],
        'subcategory': None,
        'affiliate_url': cand['affiliate_url'],
        'image_url': img_url,
        'key_features': features,
        'pros': pros,
        'cons': [
            'Temu prices change frequently — confirm the live price before buying',
            'Check the live Temu listing for current colors and sizes',
        ],
        'badges': ['new'],
        'rating': rating,
        'sold_count': None,
        'sample': False,
        'short_description': f"{name} — {features[0]}" if features else name,
        'source': f'Temu public listing — verified {TODAY}',
        'trend_status': 'trending',
        'updated': TODAY,
    }
    data['products'].append(rec)
    existing_ids.add(pid)
    existing_names.add(name.lower())
    staged.append(rec)

    pin_dir = f'{PINS_DIR}/images/temu'
    os.makedirs(pin_dir, exist_ok=True)
    pin_img = f'{pin_dir}/{pid}.jpg'
    ok2 = download(img_url, pin_img)
    desc = f"{name}. " + (' '.join(f'{f}.' for f in features[:1]) or '')
    desc = f"{desc} Trending find. Check the live price on Temu. (Affiliate link)"
    title = name if len(name) <= 80 else name[:77] + '...'
    if pid not in existing_pin_ids:
        pins.append({
            'product_id': pid,
            'title': title,
            'description': desc,
            'destination_url': f'https://qa-affiliate.vercel.app/product.html?id={pid}',
            'image_file': f'~/workspace/pinterest-affiliate/images/temu/{pid}.jpg',
            'image_ready': ok2,
            'category': cand['category'],
        })
        pin_records.append(pid)

with open(f'{BASE}/data/products.json', 'w') as f:
    json.dump(data, f, indent=2, ensure_ascii=False)
with open(f'{PINS_DIR}/pins.json', 'w') as f:
    json.dump(pins, f, indent=2, ensure_ascii=False)

summary = {
    'staged': [{'id': p['id'], 'name': p['name'], 'category': p['category'],
                'affiliate_url': p['affiliate_url']} for p in staged],
    'pin_records': pin_records,
    'skipped': skipped,
    'total_products': len(data['products']),
    'total_pins': len(pins),
}
json.dump(summary, open(f'{BASE}/tools/staged-trending-2026-09-30.json', 'w'), indent=2)
print(f"STAGED: {len(staged)} | PINS: {len(pin_records)} | SKIPPED: {len(skipped)}")
for s in skipped: print('SKIPPED:', s)
print('TOTAL PRODUCTS:', len(data['products']), '| TOTAL PINS:', len(pins))
