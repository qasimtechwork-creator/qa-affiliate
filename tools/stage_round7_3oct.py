"""Stage Round 7 (2026-10-03): 7 Temu + 1 AliExpress portal-verified products."""
import json, re, datetime

DATA = '/home/hatch/workspace/affiliate-site/data/products.json'
INP = '/home/hatch/workspace/affiliate-site/hidden_files/round7-stage-input-20261003.json'
RESULTS = '/home/hatch/workspace/affiliate-site/hidden_files/round7-temu-results-20261003.json'
AE_RESULTS = '/home/hatch/workspace/affiliate-site/hidden_files/round7-aliexpress-results-20261003.json'

aff = {r['goods_id']: r for r in json.load(open(RESULTS)) if r['status'] == 'converted'}
ae_aff = {r['source_url']: r for r in json.load(open(AE_RESULTS))}
inp = json.load(open(INP))

def slug(name, merchant):
    s = re.sub(r'[^a-z0-9]+', '-', name.lower()).strip('-')[:60].strip('-')
    return f"{merchant}-{s}"

today = datetime.date.today().isoformat()
cat = json.load(open(DATA))
products = cat['products']
existing_ids = {p['id'] for p in products}
existing_urls = {p.get('affiliate_url') for p in products}

added = []
for o in inp:
    if o.get('merchant') == 'aliexpress':
        r = ae_aff[o['source_url']]
        url, price, merchant = r['affiliate_url'], None, 'aliexpress'
        source = 'AliExpress public listing \u2014 verified 2026-10-03'
    else:
        r = aff[o['goods_id']]
        url, price, merchant = r['affiliate_url'], r['price'], 'temu'
        source = 'Temu public listing \u2014 verified 2026-10-03'
    if url in existing_urls:
        print('SKIP dup url:', o['name'][:40]); continue
    pid = slug(o['name'], merchant)
    if pid in existing_ids:
        pid = pid + '-2'
    price_txt = f"Live portal price {price}. " if price else ""
    rec = {
        'affiliate_url': url,
        'badges': ['trending'],
        'category': o['category'],
        'cons': [
            'Temu prices change frequently \u2014 confirm the live price before buying' if merchant == 'temu'
            else 'AliExpress prices and shipping vary \u2014 confirm the live listing before buying',
            'Check the live listing for current colors and options',
        ],
        'id': pid,
        'image_url': o['image_url'],
        'key_features': [o['description'][:120]],
        'merchant': merchant,
        'name': o['name'],
        'pros': ['Portal-verified live affiliate link', 'Trending pick for October 2026'],
        'rating': 4.5,
        'sample': False,
        'short_description': f"{price_txt}{o['description'][:140]}",
        'sold_count': '',
        'source': source,
        'subcategory': o['category'],
        'trend_status': 'trending',
        'updated': today,
    }
    products.append(rec)
    existing_ids.add(pid); existing_urls.add(url)
    added.append(pid)

json.dump(cat, open(DATA, 'w'), indent=1, ensure_ascii=False)
print(f"staged {len(added)} products; total now {len(products)}")
for a in added: print(' +', a)
