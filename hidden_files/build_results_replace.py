#!/usr/bin/env python3
"""Merge round3-pending-replace.json + browser Convert Link results -> round3-results-replace.json."""
import json, os

BASE = os.path.expanduser('~/workspace/affiliate-site')
pend = json.load(open(f'{BASE}/hidden_files/round3-pending-replace.json'))

converted = {
"601102285367687": "https://temu.to/k/ph8j30gsdyy",
"601099575283281": "https://temu.to/k/p1jdsvz8pe8",
"601105778999886": "https://temu.to/k/p0qo458wqdj",
"601101060914975": "https://temu.to/k/p48rdtfdp9k",
"601100076534006": "https://temu.to/k/ppnesppqbhs",
"601099703871688": "https://temu.to/k/peej8oqpbh0",
"601105704335959": "https://temu.to/k/pi4q1tly35o",
"605691653808721": "https://temu.to/k/pdt19qcxpj9",
"601099848111954": "https://temu.to/k/p60bluh2c3s",
"601102236465559": "https://temu.to/k/p9n7injur0o",
"601100822237858": "https://temu.to/k/pcsewggaeff",
"601099712859009": "https://temu.to/k/pcqcxtij5r1",
"601099559292430": "https://temu.to/k/pp57lrq4l89",
"601105453908629": "https://temu.to/k/pbwg3u6c552",
"606863424859348": "https://temu.to/k/p60aorhmulo",
"601099582011027": "https://temu.to/k/pt4w5h6wcs5",
"601102843027587": "https://temu.to/k/pttevtvw9sy",
"601105724231171": "https://temu.to/k/pcgppuyuqkb",
"601103497297187": "https://temu.to/k/pzrr7uawza1",
"601105412489923": "https://temu.to/k/py17080mgf0",
"606665655045706": "https://temu.to/k/p70t7sni4vd",
"601100794850443": "https://temu.to/k/p5rzc7dqk9v",
"601099584486592": "https://temu.to/k/p24cg1r1x7y",
"601102285314506": "https://temu.to/k/p3es85g2mbc",
"601100550525468": "https://temu.to/k/p0j8lms6cqp",
"606517696808902": "https://temu.to/k/pjs70xwy72y",
"606502999928648": "https://temu.to/k/pxe46fhuf4x",
"601099924359126": "https://temu.to/k/p0x5r2sxtow",
"606521740093329": "https://temu.to/k/pfckccob66q",
"601100858729462": "https://temu.to/k/pu0s6zlaaz5",
"601101830530529": "https://temu.to/k/pbya7nckrxz",
"601101810677594": "https://temu.to/k/pawwk6xemnv",
"601099605745834": "https://temu.to/k/prmxmnnj6ni",
"601102948777704": "https://temu.to/k/pm3a7u50vnt",
"601099831491884": "https://temu.to/k/pog42dwk8gh",
"601099516100159": "https://temu.to/k/p7jfz5lxj3i",
"601103657026655": "https://temu.to/k/p30wxpc2zwo",
"601099542311943": "https://temu.to/k/py9ga3k2f9g",
"601099610299627": "https://temu.to/k/phct9bnlzjt",
"601102517842939": "https://temu.to/k/p5f9d6wz5ub",
"601105266840332": "https://temu.to/k/p6o75os036x",
"601100107041758": "https://temu.to/k/pnbsemg6zd5",
"601101997042259": "https://temu.to/k/ph8k6cdd0u3",
"601104543723229": "https://temu.to/k/p2ui6klymgu",
"601099583329401": "https://temu.to/k/pa300um5yiy",
"601104987253787": "https://temu.to/k/ps66ye04ny5",
"605925746291488": "https://temu.to/k/pzj90478ru8",
"601100060061965": "https://temu.to/k/p9b02qdmk33",
"601102196120719": "https://temu.to/k/pd5vk0uoa4u",
"605531750153509": "https://temu.to/k/phywjn8vsfz",
"601099685689451": "https://temu.to/k/pdgwajm546z",
"601099572462426": "https://temu.to/k/pjdynyfbhlz",
"601099527752170": "https://temu.to/k/p03ufiibzhl",
"601102486345891": "https://temu.to/k/pxol011gxfp",
"601099536466202": "https://temu.to/k/p1cofvvtbgx",
}

A = "This item currently cannot be converted to an affiliate link."
B = "This product is not eligible for any discounts at this time."
failed = {
"601100262450979": B, "601102492971756": B, "601099716733310": B, "601102310141059": A,
"601099908174864": B, "601103816940950": B, "601101482226301": B, "601104987663278": A,
"601100251787668": B, "601099750960545": B, "601099548231059": B, "601101097583255": B,
"601099989708200": B, "601101644843104": B, "601103964628465": B, "602861119367334": B,
"601105395291312": B, "606600156821611": A, "601105208245244": A, "601099675971564": A,
"601104895875098": B, "605966414223359": B, "601103148400697": B, "601100473027066": A,
"601104013454735": A, "601099519445901": B, "601101207198800": A, "601099553386479": B,
"601099889173307": B, "601100616934517": A, "601105342466908": B, "601100125607671": B,
"601101129952933": B, "606103718983088": B, "601103888250496": A, "601100041679300": A,
"601103107566218": A, "601105823689076": B, "601099718483459": B, "601102212195489": B,
"601101291927063": B,
}

out = []
for p in pend:
    gid = p['goods_id']
    rec = {'batch': 'temu-replace', 'n': p['n'], 'name': p['name'], 'goods_id': gid,
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

json.dump(out, open(f'{BASE}/hidden_files/round3-results-replace.json', 'w'), indent=2)
acc = [r for r in out if r['status'] == 'accepted']
rej = [r for r in out if r['status'] == 'rejected']
unp = [r for r in out if r['status'] == 'unprocessed']
print(f'records={len(out)} accepted={len(acc)} rejected={len(rej)} unprocessed={len(unp)}')
ids = [r['goods_id'] for r in out]
assert len(ids) == len(set(ids)) == 96
urls = [r['tracked_url'] for r in acc]
assert len(urls) == len(set(urls)) == 55
data = json.load(open(f'{BASE}/data/products.json'))
cat_affs = {p['affiliate_url'] for p in data['products']}
print('affiliate-url collisions with catalog:', [u for u in urls if u in cat_affs])
for f in ['round3-results-temu-1.json', 'round3-results-temu-2.json', 'round3-results-temu-3.json']:
    prev = {r['goods_id'] for r in json.load(open(f'{BASE}/hidden_files/{f}')) if r.get('tracked_url')}
    print(f'overlap with {f}:', [g for g in converted if g in prev])
print('OK')
