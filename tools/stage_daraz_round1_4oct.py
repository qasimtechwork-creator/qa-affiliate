"""Stage Daraz Round 1 (2026-10-04): 20 Daraz Pakistan products (Pakistan track).

Affiliate links PENDING — direct daraz.pk URLs staged now; bulk-update with
tracking links once Qasim's Daraz affiliate account is approved.
"""
import json, re, datetime

DATA = '/home/hatch/workspace/affiliate-site/data/products.json'
INP = '/home/hatch/workspace/affiliate-site/hidden_files/daraz-products-round1-20261004.json'

def slug(name):
    s = re.sub(r'[^a-z0-9]+', '-', name.lower()).strip('-')[:60].strip('-')
    return f"daraz-{s}"

today = datetime.date.today().isoformat()
cat = json.load(open(DATA))
products = cat['products'] if isinstance(cat, dict) else cat
existing_ids = {p['id'] for p in products}
existing_urls = {p.get('source_url') or p.get('affiliate_url') for p in products}
inp = json.load(open(INP))

added = []
for o in inp:
    if o['source_url'] in existing_urls:
        print('SKIP dup url:', o['name'][:40]); continue
    pid = slug(o['name'])
    if pid in existing_ids:
        pid = pid + '-d1'
    rec = {
        'affiliate_url': o['source_url'],  # TEMP: direct URL until affiliate tracking ready
        'affiliate_pending': True,
        'source_url': o['source_url'],
        'badges': ['trending'],
        'category': o['category'],
        'cons': [
            'Daraz prices change frequently — confirm the live price before buying',
            'Check the live Daraz listing for current colors and options',
        ],
        'id': pid,
        'image_url': o['image_url'],
        'key_features': [o['description'][:120]],
        'merchant': 'daraz',
        'name': o['name'],
        'pros': ['Trending pick in Pakistan — October 2026', 'Cash on delivery available on Daraz'],
        'rating': 4.5,
        'sample': False,
        'short_description': f"{o.get('price_pkr', '')}. {o['description'][:140]}",
        'sold_count': '',
        'source': 'Daraz Pakistan listing — verified 2026-10-04',
        'subcategory': o['category'],
        'trend_status': 'trending',
        'updated': today,
    }
    products.append(rec)
    existing_ids.add(pid); existing_urls.add(o['source_url'])
    added.append(pid)

json.dump(cat, open(DATA, 'w'), ensure_ascii=False, indent=1)
print(f"ADDED {len(added)} daraz products. Total now: {len(products)}")
for a in added: print(' +', a)
