#!/usr/bin/env python3
"""Merge round3-pending-temu2.json + browser Convert Link results -> round3-results-temu-2.json.
Converted/fails from the retry run (59); n=32,33 failed in the first (errored) run."""
import json, os

BASE = os.path.expanduser('~/workspace/affiliate-site')
pend = json.load(open(f'{BASE}/hidden_files/round3-pending-temu2.json'))

converted = {
"606372087340634": "https://temu.to/k/pvq0cg15ouf",
"601099614726403": "https://temu.to/k/p0s2hd2amae",
"601099796769273": "https://temu.to/k/p28vj679u87",
"601105687271114": "https://temu.to/k/pugvcxxgwqu",
"601100200937018": "https://temu.to/k/px6ov0bjwbk",
"601099551611376": "https://temu.to/k/pcj2xzuu9bq",
"601102440189995": "https://temu.to/k/pz2j5jo4q10",
"601099563869434": "https://temu.to/k/pxhhfd61h78",
"601100250711666": "https://temu.to/k/p008ge22t4i",
"605817365478935": "https://temu.to/k/pd3xmbpsqe0",
"601099864378102": "https://temu.to/k/pni4cjd5zai",
"605528931585109": "https://temu.to/k/p4yj042njc0",
"601101997687140": "https://temu.to/k/ptukn4c66bn",
"601099586833293": "https://temu.to/k/plgvdpubkc4",
"601099525157660": "https://temu.to/k/ppauqftiirn",
"601102731947773": "https://temu.to/k/psvfdpoc3xp",
"605885413863907": "https://temu.to/k/pivyd186tsz",
"601101591777665": "https://temu.to/k/pikz7v0swng",
"601099792000269": "https://temu.to/k/px66wyqbw30",
"601102311105479": "https://temu.to/k/pnzhwqgtetv",
"601099947744326": "https://temu.to/k/pebs2bmnta6",
"601099974760776": "https://temu.to/k/pn53chf8uq0",
"601100703904090": "https://temu.to/k/ptcxue3bude",
"601099891798936": "https://temu.to/k/ptj3zfnoezz",
"607597394542500": "https://temu.to/k/pnuk3lq87tp",
"601103492049281": "https://temu.to/k/pueizv9ktsu",
"606249747861632": "https://temu.to/k/pd2e7bvi8jp",
"601105263833224": "https://temu.to/k/p3znysv9vhl",
"601102318195134": "https://temu.to/k/pi8sor3hsvt",
"601099609469615": "https://temu.to/k/pdn0c7tii9q",
"601104555690787": "https://temu.to/k/pch433294yl",
"601099751101189": "https://temu.to/k/pw1ox20qfwf",
"606124254272945": "https://temu.to/k/p1nq592cjac",
"601105772738391": "https://temu.to/k/pxghli9gox0",
}

A = "This item currently cannot be converted to an affiliate link."
B = "This product is not eligible for any discounts at this time."
failed = {
"601099514290838": A, "601100350796783": A, "601105558991749": B, "601103082898030": B,
"601099753609466": B, "601099651956145": B, "601102340534058": B, "601100262132836": B,
"601099625208125": A, "601100576373662": B, "601103729843106": A, "601099700335614": A,
"601099832759116": A, "601105700170589": A, "601101339600442": B, "601099949956005": B,
"601099546910735": B, "601103209907112": B, "605700394720495": A, "601102796845574": B,
"601103076715097": B, "605610183646651": A, "601102186001262": B, "601099593592401": A,
"601099562759432": B,
"601102980657963": A,  # n=32, failed in first (errored) run
"601100082922797": A,  # n=33, failed in first (errored) run
}

out = []
for p in pend:
    gid = p['goods_id']
    rec = {'batch': 'temu-2', 'n': p['n'], 'name': p['name'], 'goods_id': gid,
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

json.dump(out, open(f'{BASE}/hidden_files/round3-results-temu-2.json', 'w'), indent=2)
acc = [r for r in out if r['status'] == 'accepted']
rej = [r for r in out if r['status'] == 'rejected']
unp = [r for r in out if r['status'] == 'unprocessed']
print(f'records={len(out)} accepted={len(acc)} rejected={len(rej)} unprocessed={len(unp)}')
ids = [r['goods_id'] for r in out]
assert len(ids) == len(set(ids)) == 61
urls = [r['tracked_url'] for r in acc]
assert len(urls) == len(set(urls)) == 34
# collision against staged catalog
data = json.load(open(f'{BASE}/data/products.json'))
cat_affs = {p['affiliate_url'] for p in data['products']}
print('affiliate-url collisions with catalog:', [u for u in urls if u in cat_affs])
print('OK')
