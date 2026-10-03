#!/usr/bin/env python3
"""Round 5 (2026-10-03): select FRESH candidates from all prior candidate pools,
deduped against the full staged catalog (478), all prior goods_ids, and all
previously-failed product names. Output: conversion payload for the portal
browser task (Temu Convert Link / AliExpress Link Generator)."""
import json, re, glob, os

BASE = os.path.expanduser('~/workspace/affiliate-site')

def goods_id(url):
    if not url: return ''
    m = re.search(r'-g-(\d+)\.html', url)
    if m: return m.group(1)
    m = re.search(r'goods_id=(\d+)', url)
    if m: return m.group(1)
    return ''

STOP = {'with', 'and', 'the', 'for', 'from', 'all', 'skin', 'set', 'dress', 'bag',
        'piece', 'type', 'types', 'women', "women's", 'shoe', 'shoes', 'new',
        'fashion', 'ladies', 'bag', 'temu', 'aliexpress'}
def toks(name):
    return [t for t in re.sub(r'[^a-z0-9 ]', ' ', name.lower()).split()
            if len(t) > 2 and t not in STOP]
def consec_run(a, b):
    ta, tb = toks(a), toks(b); sb = set(tb); best = cur = 0
    for t in ta:
        cur = cur + 1 if t in sb else 0; best = max(best, cur)
    return best
def overlap_ratio(a, b):
    ta, tb = toks(a), toks(b)
    if not ta or not tb: return 0.0
    return len(set(ta) & set(tb)) / min(len(set(ta)), len(set(tb)))
def is_dup(name, others):
    for o in others:
        on = o['name'] if isinstance(o, dict) else o
        if consec_run(name, on) >= 6: return on
        if overlap_ratio(name, on) >= 0.85: return on
    return None

# 1. Full staged catalog
data = json.load(open(f'{BASE}/data/products.json'))
catalog = data['products']
print('CATALOG:', len(catalog))

# 2. Prior goods_ids (staged + converted)
prior_goods = set()
for f in glob.glob(f'{BASE}/hidden_files/round*-results-*.json') + glob.glob(f'{BASE}/tools/staged-*.json'):
    try: d = json.load(open(f))
    except Exception: continue
    entries = d if isinstance(d, list) else d.get('staged', d.get('products', []))
    for e in entries:
        g = str(e.get('goods_id') or goods_id(e.get('product_url', '')) or '')
        if g: prior_goods.add(g)
print('PRIOR GOODS_IDS:', len(prior_goods))

# 3. Previously failed names (portal conversion failures)
failed_names = []
for f in glob.glob(f'{BASE}/tools/failed-links-*.json'):
    d = json.load(open(f))
    if isinstance(d, dict):
        failed_names += d.get('temu_failed', []) + d.get('aliexpress_failed', [])
    elif isinstance(d, list):
        failed_names += [(x.get('name') if isinstance(x, dict) else str(x)) for x in d]
print('FAILED NAMES:', len(failed_names))

# 4. Scan candidate pools
cand_files = (glob.glob(f'{BASE}/tools/temu-candidates-*.json') +
              glob.glob(f'{BASE}/tools/aliexpress-candidates-*.json') +
              glob.glob(f'{BASE}/hidden_files/round3-*.json') +
              glob.glob(f'{BASE}/hidden_files/aliexpress-round1-50.json'))
seen_urls, fresh, skipped_reasons = set(), [], {}
for f in cand_files:
    try: d = json.load(open(f))
    except Exception: continue
    items = d if isinstance(d, list) else d.get('products', d.get('candidates', d.get('items', [])))
    for it in items:
        url = it.get('product_url', '')
        if not url or url in seen_urls: continue
        seen_urls.add(url)
        name = (it.get('name') or '').strip()
        if not name: continue
        gid = str(it.get('goods_id') or goods_id(url) or '')
        merchant = it.get('merchant') or ('aliexpress' if 'aliexpress' in url else 'temu')
        reason = None
        if gid and gid in prior_goods:
            reason = 'goods_id already converted/staged'
        elif is_dup(name, catalog):
            reason = f"dup of staged: {is_dup(name, catalog)[:50]}"
        elif is_dup(name, failed_names):
            reason = 'previously failed portal conversion'
        elif is_dup(name, fresh):
            reason = f"near-dup in batch: {is_dup(name, fresh)[:50]}"
        if reason:
            skipped_reasons[reason.split(':')[0]] = skipped_reasons.get(reason.split(':')[0], 0) + 1
            continue
        fresh.append({
            'name': name, 'merchant': merchant, 'goods_id': gid,
            'product_url': url, 'image_url': it.get('image_url', ''),
            'category': it.get('category', 'beauty'),
            'key_features': it.get('key_features', []),
            'pros': it.get('pros', []),
        })

print('FRESH CANDIDATES:', len(fresh))
for k, v in sorted(skipped_reasons.items(), key=lambda x: -x[1]):
    print(f'  skipped [{k}]: {v}')

# 5. Write conversion payload (Temu first, then AliExpress)
temu = [c for c in fresh if c['merchant'] == 'temu']
ali = [c for c in fresh if c['merchant'] != 'temu']
print('TEMU:', len(temu), '| ALIEXPRESS:', len(ali))
payload = {'date': '2026-10-03', 'note': 'Feed each product_url to the portal (Temu Storefront Convert Link / AliExpress Link Generator) and record the returned tracked affiliate_url per goods_id.',
           'temu': temu, 'aliexpress': ali}
out = f'{BASE}/hidden_files/round5-convert-payload-20261003.json'
json.dump(payload, open(out, 'w'), indent=2, ensure_ascii=False)
print('WROTE:', out)
