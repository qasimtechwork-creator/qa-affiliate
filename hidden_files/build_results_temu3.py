#!/usr/bin/env python3
"""Merge round3-pending-temu3.json + browser Convert Link results -> round3-results-temu-3.json."""
import json, os

BASE = os.path.expanduser('~/workspace/affiliate-site')
pend = json.load(open(f'{BASE}/hidden_files/round3-pending-temu3.json'))

converted = {
"601099774750910": "https://temu.to/k/p5f61xr0icf",
"601102537785156": "https://temu.to/k/pwwescfqqc2",
"606388243784825": "https://temu.to/k/phnhfh2kdlb",
"601101185143816": "https://temu.to/k/pbgv5s4uv79",
"601099786541480": "https://temu.to/k/pagsd0tryf6",
"601100625783373": "https://temu.to/k/p8ua4x2su54",
"601099694945363": "https://temu.to/k/plzy1avdz8k",
"601099565270208": "https://temu.to/k/prtaz2ltx1f",
"601099670186204": "https://temu.to/k/pqsvp3liqct",
"601099844117768": "https://temu.to/k/p1ix5un4e8y",
"601101821615152": "https://temu.to/k/pbtuerm31wg",
"601100235452931": "https://temu.to/k/pslvfemvem6",
"601099513176178": "https://temu.to/k/puxhzjaqsk7",
"606014799763104": "https://temu.to/k/ph831p1rjgw",
"601102305748466": "https://temu.to/k/ptcaa8hd18u",
"606097746279065": "https://temu.to/k/pa8rr20h2ri",
"601099570398138": "https://temu.to/k/pupqgjux9e2",
"601099563819895": "https://temu.to/k/p6mddq9h5vm",
"601099657996878": "https://temu.to/k/phwj89drjj4",
"606299542674148": "https://temu.to/k/pghp7m1w0mw",
"601099660535413": "https://temu.to/k/pgjrjg5be99",
"601100066131933": "https://temu.to/k/po262efazep",
"606062514114516": "https://temu.to/k/pti4p2fq3ge",
"605801259356800": "https://temu.to/k/pkhrap373xd",
"601102571023600": "https://temu.to/k/p44uyxc604d",
"601103511152294": "https://temu.to/k/pnfz0g4s1wi",
"607090521285830": "https://temu.to/k/pqa3tsfgctn",
"601102277961649": "https://temu.to/k/p86joips7gx",
"601103145608266": "https://temu.to/k/pz23rbh91xv",
"605928631956225": "https://temu.to/k/pn678fazlsx",
"601100117441433": "https://temu.to/k/pp2jywgp6kb",
"601099739331011": "https://temu.to/k/pnr81oebyqh",
"601099743527151": "https://temu.to/k/p37eua0r8nu",
"601099579663054": "https://temu.to/k/pd80mflxbdv",
"601099775601033": "https://temu.to/k/pxc8l3p5ukm",
"601099813582022": "https://temu.to/k/p3t913z5fer",
"601101145344058": "https://temu.to/k/pt6b8eyhzut",
"601100043757979": "https://temu.to/k/pij7le88e1u",
"601104330204851": "https://temu.to/k/plcpoyhov3n",
"601099708375498": "https://temu.to/k/p992pk0z16a",
"601101844141480": "https://temu.to/k/p38ej7vqet7",
"601099559898610": "https://temu.to/k/pvg354t1qvc",
}

A = "This item currently cannot be converted to an affiliate link."
B = "This product is not eligible for any discounts at this time."
failed = {
"601103168033610": A, "601099714479346": A, "606353833753094": B, "601103407795338": A,
"601099678707554": A, "601105054166941": B, "601101378554749": B, "601105676079350": B,
"601100172741467": B, "601103311352260": B, "606010504791035": B, "606333231275007": A,
"601099872135229": A, "601099723080059": A, "606013658858344": B, "601099927666521": B,
"601103101305531": B, "601099620109495": B, "601099541476287": B,
}

out = []
for p in pend:
    gid = p['goods_id']
    rec = {'batch': 'temu-3', 'n': p['n'], 'name': p['name'], 'goods_id': gid,
           'product_url': p.get('product_url') or f'https://www.temu.com/goods.html?goods_id={gid}',
           'category': p.get('category'), 'image_url': p['image_url'],
           'tracked_url': None, 'status': None, 'reject_reason': None, 'staged': False}
    if gid in converted:
        rec['tracked_url'] = converted[gid]; rec['status'] = 'accepted'
    elif gid in failed:
        rec['status'] = 'rejected'; rec['reject_reason'] = failed[gid]
    else:
        rec['status'] = 'unprocessed'
    out.append(rec)

json.dump(out, open(f'{BASE}/hidden_files/round3-results-temu-3.json', 'w'), indent=2)
acc = [r for r in out if r['status'] == 'accepted']
rej = [r for r in out if r['status'] == 'rejected']
unp = [r for r in out if r['status'] == 'unprocessed']
print(f'records={len(out)} accepted={len(acc)} rejected={len(rej)} unprocessed={len(unp)}')
ids = [r['goods_id'] for r in out]
assert len(ids) == len(set(ids)) == 61
urls = [r['tracked_url'] for r in acc]
assert len(urls) == len(set(urls)) == 42
data = json.load(open(f'{BASE}/data/products.json'))
cat_affs = {p['affiliate_url'] for p in data['products']}
print('affiliate-url collisions with catalog:', [u for u in urls if u in cat_affs])
# goods_id already accepted in earlier batches? cross-check verified files
for f in ['round3-results-temu-1.json', 'round3-results-temu-2.json']:
    prev = {r['goods_id'] for r in json.load(open(f'{BASE}/hidden_files/{f}')) if r.get('tracked_url')}
    print(f'overlap with {f}:', [g for g in converted if g in prev])
print('OK')
