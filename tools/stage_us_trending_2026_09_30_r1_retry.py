#!/usr/bin/env python3
"""Retry staging for the Multi Stripe dress (false-positive dup under 0.7 rule).
Refined dedup: 0.85 overlap ratio or 6+ consecutive tokens."""
import json, re, os, subprocess

BASE = os.path.expanduser('~/workspace/affiliate-site')
TODAY = '2026-09-30'
cand = dict(
    name="Multi Stripe Orange, Green, And Mint Sleeveless Maxi Dress With Pocket",
    aff="https://temu.to/k/peyjlxg13x0",
    img="https://img.kwcdn.com/local-goods-image/201a0da6f08/e5bb5479-44cb-481c-be6a-e9ed9b1d9140_1340x1787.jpeg.format.jpg?imageView2/2/w/800/q/70/format/avif",
    category="fashion", subcategory="dresses",
    trend="Trending bestseller in Women's Clothing on Temu")

STOP = {'with','and','the','for','from','all','skin','set','dress','bag','piece','type','types'}
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

data = json.load(open(f'{BASE}/data/products.json'))
if cand['aff'] in {p['affiliate_url'] for p in data['products']}:
    print('SKIP: affiliate collision'); raise SystemExit
dups = [p['name'] for p in data['products']
        if consec_run(cand['name'], p['name']) >= 6 or overlap_ratio(cand['name'], p['name']) >= 0.85]
if dups:
    print('SKIP: duplicate of:', dups[0][:70]); raise SystemExit

def slugify(name):
    s = re.sub(r"['\u2019]", "", f"temu-{name}".lower())
    return re.sub(r"[^a-z0-9]+", "-", s).strip('-')[:71].rstrip('-')
pid, base, n = slugify(cand['name']), None, 2
base = pid
ids = {p['id'] for p in data['products']}
while pid in ids:
    pid = f"{base}-{n}"[:71].rstrip('-'); n += 1
dest = f'{BASE}/images/{pid}.jpg'
r = subprocess.run(['curl', '-sL', '-f', '--retry', '3', '--retry-delay', '4',
    '-A', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
    '--max-time', '120', '-o', dest, cand['img']], capture_output=True, timeout=150)
if r.returncode != 0 or not os.path.exists(dest) or os.path.getsize(dest) == 0:
    print('SKIP: image download failed'); raise SystemExit
rec = {'id': pid, 'name': cand['name'], 'merchant': 'temu', 'category': cand['category'],
    'subcategory': cand['subcategory'], 'affiliate_url': cand['aff'],
    'image_url': cand['img'], 'key_features': [cand['trend']],
    'pros': [f"Trending find on Temu \u2014 {cand['trend']}"], 'cons': [
        'Temu prices change frequently \u2014 confirm the live price before buying',
        'Check the live Temu listing for current colors and sizes'],
    'badges': ['new'], 'rating': None, 'sold_count': None, 'sample': False,
    'short_description': f"{cand['name']} \u2014 {cand['trend']}",
    'source': f'Temu public listing \u2014 verified {TODAY}',
    'trend_status': 'trending', 'updated': TODAY}
data['products'].append(rec)
with open(f'{BASE}/data/products.json', 'w') as f:
    json.dump(data, f, indent=2, ensure_ascii=False)
print('STAGED:', pid)
print('TOTAL PRODUCTS:', len(data['products']))
