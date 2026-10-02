#!/usr/bin/env python3
"""Stage Temu 2-Oct-2026 daily round: 50 portal-verified tracked links.
Source: hidden_files/round4-results-temu-2oct.json (converted 2026-10-02 by
the live Temu Storefront/Convert Link task after Qasim cleared the slider
puzzle; first 3 conversions pre-date the stop).
Dedup: goods_id against all prior staged source files + affiliate-URL
collision + name overlap (consec >= 6 or ratio >= 0.85) against the FULL
staged catalog and within this batch. Records with incomplete image URLs
are skipped, never guessed. Generates go/<id>.html redirect fallbacks and
regenerates sitemap.xml (incl. home)."""
import json, re, os, subprocess, html, glob

BASE = os.path.expanduser('~/workspace/affiliate-site')
TODAY = '2026-10-02'
SITE = 'https://qa-affiliate.vercel.app'

CAT_LABEL = {'bags': "Women's Bags", 'beauty': 'Beauty', 'fashion': "Women's Fashion",
             'skincare': 'Skincare', 'hair': 'Hair Care', 'jewelry': 'Jewelry',
             'shoes': 'Shoes', 'lingerie': 'Lingerie', 'accessories': 'Accessories',
             'home': 'Home & Lifestyle', 'fitness': 'Fitness & Active'}
def cat_label(c):
    return CAT_LABEL.get(c, (c or 'beauty').replace('_', ' ').title())

STOP = {'with', 'and', 'the', 'for', 'from', 'all', 'skin', 'set', 'dress', 'bag',
        'piece', 'type', 'types', 'women', "women's", 'shoe', 'shoes', 'new',
        'fashion', 'ladies', 'bag'}
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
def is_dup(name, others):
    for o in others:
        if consec_run(name, o['name']) >= 6: return o['name']
        if overlap_ratio(name, o['name']) >= 0.85: return o['name']
    return None
def slugify(name):
    s = re.sub(r"['\u2019]", "", f"temu-{name}".lower())
    return re.sub(r"[^a-z0-9]+", "-", s).strip('-')[:71].rstrip('-')
def download(url, dest):
    if os.path.exists(dest) and os.path.getsize(dest) > 0: return True
    try:
        r = subprocess.run(['curl', '-sL', '-f', '--retry', '2', '--retry-delay', '3',
            '-A', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
            '--referer', 'https://www.temu.com/',
            '--max-time', '90', '-o', dest, url], capture_output=True, timeout=120)
        return r.returncode == 0 and os.path.exists(dest) and os.path.getsize(dest) > 0
    except Exception as e:
        print(f'DOWNLOAD FAILED: {e}'); return False

GO_TMPL = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<title>{title} | QA Affiliate</title>
<meta name="robots" content="noindex, nofollow">
<meta http-equiv="refresh" content="0;url={aff}">
<link rel="canonical" href="{aff}">
<script>window.location.replace("{aff}");</script>
</head>
<body>
<p>Redirecting to the store... <a href="{aff}">Click here if you are not redirected</a>.</p>
</body>
</html>
"""

# goods_ids already staged in earlier rounds (source files keep goods_id)
prior_goods = set()
for f in glob.glob(f'{BASE}/hidden_files/round*-results-*.json') + \
         glob.glob(f'{BASE}/tools/staged-*.json'):
    try:
        d = json.load(open(f))
    except Exception:
        continue
    entries = d if isinstance(d, list) else d.get('staged', [])
    for e in entries:
        g = str(e.get('goods_id') or '')
        if g and e.get('staged', True):
            prior_goods.add(g)
print(f'PRIOR STAGED GOODS_IDS KNOWN: {len(prior_goods)}')

res_path = f'{BASE}/hidden_files/round4-results-temu-2oct.json'
results = json.load(open(res_path))
cands = [x for x in results
         if not x.get('staged') and (x.get('affiliate_url') or x.get('tracked_url'))]
print(f'CANDIDATES: {len(cands)}')

data = json.load(open(f'{BASE}/data/products.json'))
existing_ids = {p['id'] for p in data['products']}
existing_affs = {p['affiliate_url'] for p in data['products']}
img_dir = f'{BASE}/images'; os.makedirs(img_dir, exist_ok=True)
go_dir = f'{BASE}/go'; os.makedirs(go_dir, exist_ok=True)

staged, skipped, seen = [], [], []
for cand in cands:
    name = cand['name']
    aff = cand.get('affiliate_url') or cand.get('tracked_url')
    img = cand.get('image_url') or ''
    cat = cand.get('category') or 'beauty'
    label = cat_label(cat)
    gid = str(cand.get('goods_id') or '')
    if not aff:
        skipped.append((name, 'no affiliate link')); continue
    if not img.startswith('https://img.kwcdn.com/'):
        skipped.append((name, f'incomplete image URL (goods {gid})')); continue
    if aff in existing_affs:
        skipped.append((name, 'affiliate URL collision')); continue
    if gid and gid in prior_goods:
        skipped.append((name, f'goods_id {gid} already staged in an earlier round')); continue
    d = is_dup(name, data['products'])
    if d: skipped.append((name, f'duplicate of staged: {d[:60]}')); continue
    d2 = is_dup(name, seen)
    if d2: skipped.append((name, f'near-duplicate in batch: {d2[:60]}')); continue
    pid = slugify(name); base = pid; n = 2
    while pid in existing_ids:
        pid = f"{base}-{n}"[:71].rstrip('-'); n += 1
    if not download(img, f'{img_dir}/{pid}.jpg'):
        skipped.append((name, 'image download failed')); continue
    rec = {'id': pid, 'name': name, 'merchant': 'temu', 'category': cat,
        'subcategory': None, 'affiliate_url': aff,
        'image_url': img, 'key_features': [f"Trending find in {label} on Temu"],
        'pros': [f"Trending find on Temu \u2014 {label}"], 'cons': [
            'Temu prices change frequently \u2014 confirm the live price before buying',
            'Check the live Temu listing for current colors and sizes'],
        'badges': ['new'], 'rating': None, 'sold_count': None, 'sample': False,
        'short_description': f"{name} \u2014 trending find in {label} on Temu",
        'source': f'Temu public listing \u2014 verified {TODAY}',
        'trend_status': 'trending', 'updated': TODAY}
    data['products'].append(rec)
    existing_ids.add(pid); existing_affs.add(aff); seen.append(rec)
    with open(f'{go_dir}/{pid}.html', 'w') as f:
        f.write(GO_TMPL.format(title=html.escape(name), aff=aff))
    cand['staged'] = True
    if gid: prior_goods.add(gid)
    staged.append(rec)

with open(f'{BASE}/data/products.json', 'w') as f:
    json.dump(data, f, indent=2, ensure_ascii=False)
with open(res_path, 'w') as f:
    json.dump(results, f, indent=2, ensure_ascii=False)

static_paths = ['/', '/products.html', '/trending.html', '/deals.html', '/guides.html',
    '/guides/glass-skin-routine.html', '/guides/capsule-wardrobe.html',
    '/guides/heatless-curls-guide.html', '/guides/jewelry-that-doesnt-tarnish.html',
    '/guides/makeup-brush-guide.html',
    '/category.html?cat=fashion', '/category.html?cat=shoes', '/category.html?cat=jewelry',
    '/category.html?cat=bags', '/category.html?cat=beauty', '/category.html?cat=skincare',
    '/category.html?cat=hair', '/category.html?cat=accessories', '/category.html?cat=lingerie',
    '/category.html?cat=fitness', '/category.html?cat=home',
    '/about.html', '/contact.html', '/faq.html',
    '/legal/disclosure.html', '/legal/privacy.html', '/legal/terms.html',
    '/legal/cookies.html', '/legal/advertising.html']
freq_prio = {'/': ('daily', '1.0'), '/products.html': ('daily', '0.9'),
             '/trending.html': ('daily', '0.9'), '/deals.html': ('daily', '0.8'),
             '/guides.html': ('weekly', '0.7')}
lines = ['<?xml version="1.0" encoding="UTF-8"?>',
 '<!-- Canonical domain: https://qa-affiliate.vercel.app (current live Vercel URL, verified 2026-09-28). Replace with the final custom domain when selected. -->',
 '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
for p in static_paths:
    fr, pr = freq_prio.get(p, ('weekly', '0.8') if p.startswith('/category') else ('monthly', '0.6'))
    lines.append(f'  <url><loc>{SITE}{p}</loc><changefreq>{fr}</changefreq><priority>{pr}</priority></url>')
for prod in data['products']:
    lines.append(f'  <url><loc>{SITE}/product.html?id={prod["id"]}</loc><changefreq>weekly</changefreq><priority>0.7</priority></url>')
lines.append('</urlset>')
with open(f'{BASE}/sitemap.xml', 'w') as f:
    f.write('\n'.join(lines) + '\n')

json.dump({'staged': [{'id': p['id'], 'name': p['name'], 'affiliate_url': p['affiliate_url']} for p in staged],
    'skipped': [{'name': s[0], 'reason': s[1]} for s in skipped],
    'total_products': len(data['products'])},
    open(f'{BASE}/tools/staged-round4-temu-2oct.json', 'w'), indent=2)
print(f"STAGED: {len(staged)} | SKIPPED: {len(skipped)}")
for s in skipped: print('SKIPPED:', s[0][:55], '->', s[1][:70])
print('TOTAL PRODUCTS:', len(data['products']))
