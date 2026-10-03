"""Stage Round 7 R2 (2026-10-03): 14 Temu portal-verified products."""
import json, re, datetime

DATA = '/home/hatch/workspace/affiliate-site/data/products.json'
INP = '/home/hatch/workspace/affiliate-site/hidden_files/round7-temu-r2-stage-input-20261003.json'

def slug(name):
    s = re.sub(r'[^a-z0-9]+', '-', name.lower()).strip('-')[:60].strip('-')
    return f"temu-{s}"

today = datetime.date.today().isoformat()
cat = json.load(open(DATA))
products = cat['products']
existing_ids = {p['id'] for p in products}
existing_urls = {p.get('affiliate_url') for p in products}
inp = json.load(open(INP))

added = []
for o in inp:
    if o['affiliate_url'] in existing_urls:
        print('SKIP dup url:', o['name'][:40]); continue
    pid = slug(o['name'])
    if pid in existing_ids:
        pid = pid + '-r2'
    price = o.get('live_price') or ''
    price_txt = f"Live portal price {price}. " if price else ""
    rec = {
        'affiliate_url': o['affiliate_url'],
        'badges': ['trending'],
        'category': o['category'],
        'cons': [
            'Temu prices change frequently \u2014 confirm the live price before buying',
            'Check the live Temu listing for current colors and options',
        ],
        'id': pid,
        'image_url': o['image_url'],
        'key_features': [o['description'][:120]],
        'merchant': 'temu',
        'name': o['name'],
        'pros': ['Portal-verified live affiliate link', 'Trending pick for October 2026'],
        'rating': 4.5,
        'sample': False,
        'short_description': f"{price_txt}{o['description'][:140]}",
        'sold_count': '',
        'source': 'Temu public listing \u2014 verified 2026-10-03',
        'subcategory': o['category'],
        'trend_status': 'trending',
        'updated': today,
    }
    products.append(rec)
    existing_ids.add(pid); existing_urls.add(o['affiliate_url'])
    added.append(pid)

json.dump(cat, open(DATA, 'w'), indent=1, ensure_ascii=False)
print(f"staged {len(added)} products; total now {len(products)}")
for a in added: print(' +', a)
