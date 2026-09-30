#!/usr/bin/env python3
"""Stage 2026-09-30 US-trending Temu batch (round 1): portal-verified products.
Discovery: browser-verified buyable via Quick Look modal, $10+, merchant images.
Affiliate links: portal Convert link tool, signed in as Qasim Mehmood.
Honest data only. No prices stored (site 'Price varies' convention)."""
import json, re, os, subprocess

BASE = os.path.expanduser('~/workspace/affiliate-site')
TODAY = '2026-09-30'
K = "https://img.kwcdn.com/"

def C(name, gid, aff, img, cat, sub, trend):
    return dict(name=name, goods_id=gid, aff=aff, img=img,
                category=cat, subcategory=sub, trend=trend)

D = "Trending bestseller in Women's Clothing on Temu"
B = "Bestseller in Women's Handbags on Temu"
S = "Bestseller in Skincare & Beauty on Temu"
CANDIDATES = [
 C("Racer Sleeveless Ditsy Floral Vacation Cruise Multi Chevron Stripe Yellow, Navy And Mint Sleeveless Maxi Dress With Pocket",
   "603046541101115", "https://temu.to/k/pfwgcydj7k2",
   K+"local-goods-image/2013f778ba8/7f4de076-baf1-47bc-b9ab-2d1455c30e08_1340x1787.jpeg.format.jpg?imageView2/2/w/800/q/70/format/avif",
   "fashion", "dresses", D),
 C("Multi Stripe Orange, Green, And Mint Sleeveless Maxi Dress With Pocket",
   "602571745931226", "https://temu.to/k/peyjlxg13x0",
   K+"local-goods-image/201a0da6f08/e5bb5479-44cb-481c-be6a-e9ed9b1d9140_1340x1787.jpeg.format.jpg?imageView2/2/w/800/q/70/format/avif",
   "fashion", "dresses", D),
 C("Boho Retro Vintage Solid Grey Color Block Stripe Grey Maxi Dress Racer S-3X",
   "602853670237781", "https://temu.to/k/pk2dyuqcgo9",
   K+"local-goods-image/201365d0000/cd6b39be-45a1-4b30-b6e5-e7c722841d8e_1340x1787.jpeg.format.jpg?imageView2/2/w/800/q/70/format/avif",
   "fashion", "dresses", D),
 C("Multi Stripe Orange, Green, And Mint Sleeveless Maxi Dress With Pocket S-3X",
   "602302773561033", "https://temu.to/k/p2405ineez1",
   K+"local-goods-image/1f23586190/cc198e03-353b-448d-84b9-5d8be9ff407d_1340x1785.jpeg?imageView2/2/w/800/q/70/format/avif",
   "fashion", "dresses", D),
 C("Tiered Tropical Sleeveless Leaves Floral Maxi Long Woven Dress",
   "602381366435883", "https://temu.to/k/pht5w3r5s97",
   K+"local-goods-image/2019505520c/d517bad0-a0f0-4230-9bb3-d6190091f13e.jpeg?imageView2/2/w/800/q/70/format/avif",
   "fashion", "dresses", D),
 C("Elegant Floral Maxi Dress With Plunging Neckline Short Sleeve Surplice Sash Versatile Summer Dress For Women",
   "602527621810710", "https://temu.to/k/pes5hvgnehc",
   K+"local-goods-image/2079f659ce/27b18199-127d-4627-bc1b-eae814d755a9_1340x1787.jpeg.format.jpg?imageView2/2/w/800/q/70/format/avif",
   "fashion", "dresses", D),
 C("Printed Patchwork Dress, Elegant Fashion Round Neck Short Sleeve, Pleated Long Skirt",
   "601100129611490", "https://temu.to/k/pau6butuxig",
   K+"product/fancy/69d7d8ce-bee9-4be6-beb8-543e0295aec4.jpg?imageView2/2/w/800/q/70/format/avif",
   "fashion", "dresses", D),
 C("Women's Round Neck Vacation Print Dress, Special Edition, Printed Fabric, Maxi Dress, Short Sleeves, With Pockets",
   "606830742864370", "https://temu.to/k/p6vavfsusnf",
   K+"product/fancy/4794879f-f209-4675-bcb2-a7769e28b3b6.jpg?imageView2/2/w/800/q/70/format/avif",
   "fashion", "dresses", D),
 C("Women's Large-Capacity Tote Bag, Convertible Handbag, Crossbody and Shoulder Bag",
   "607351708995619", "https://temu.to/k/pa9sal8mbhk",
   K+"product/fancy/05f3d1a4-ac97-4b6c-bdb4-26e09f4145b4.jpg?imageView2/2/w/800/q/70/format/avif",
   "bags", None, B),
 C("Genuine Leather Large-capacity Tote and Crossbody Dual-use Bag with Zipper Closure",
   "606330328863045", "https://temu.to/k/p7nsbuk1wda",
   K+"product/fancy/f679e546-bdde-4ca6-bb36-bd0ba620d5b8.jpg?imageView2/2/w/800/q/70/format/avif",
   "bags", None, B),
 C("Women's Genuine Top-Grain Handbag with Multi-Compartment and Detachable Strap",
   "605925058396034", "https://temu.to/k/p0sud6padkf",
   K+"product/fancy/f279e2c1-79b5-4c90-b11d-9da583dba7ab.jpg?imageView2/2/w/800/q/70/format/avif",
   "bags", None, B),
 C("76pcs Korean Skincare Gift Set for All Skin Types - Hydrating Facial and Lip Care",
   "607544680513731", "https://temu.to/k/pkrd8csjf8s",
   K+"product/fancy/4f2489ea-a8ee-4be6-9879-fb44c3878afb.jpg?imageView2/2/w/800/q/70/format/avif",
   "skincare", None, S),
 C("6pcs Facial Skin Care Series - Face Cream, Lotion, Essence, Eye Cream with Retinol, Hyaluronic Acid, Ceramide, Vitamin C",
   "606224632384204", "https://temu.to/k/pyg96qn3tsx",
   K+"product/fancy/46c9ffcb-ba5c-4876-aa10-65a5dcc0a319.jpg?imageView2/2/w/800/q/70/format/avif",
   "skincare", None, S),
 C("Elizabeth Arden 3 Piece Eight Hour Treatment Skin Care Set for Women",
   "602321740228853", "https://temu.to/k/popixug2e6o",
   K+"local-goods-image/5a65d3a6/1607a06f-3286-4d8d-974d-b955b57d467a.jpeg?imageView2/2/w/800/q/70/format/avif",
   "skincare", None, S),
 C("Beauty of Joseon Hanbang Sun Trio Daily Defense Hydrating and Soothing Skincare Set, 3-Piece",
   "610186186045842", "https://temu.to/k/pf01jojcncn",
   K+"local-goods-image/40437766/adc69889-e853-4119-99c5-6642d1be8f39.jpeg?imageView2/2/w/800/q/70/format/avif",
   "skincare", None, S),
]

STOP = {'with','and','the','for','from','all','skin','set','dress','bag','piece','type','types'}
def toks(name):
    return [t for t in re.sub(r'[^a-z0-9 ]', ' ', name.lower()).split()
            if len(t) > 2 and t not in STOP]

def overlap_ratio(a, b):
    ta, tb = toks(a), toks(b)
    if not ta or not tb: return 0.0
    sa, sb = set(ta), set(tb)
    return len(sa & sb) / min(len(sa), len(sb))

def consec_run(a, b):
    ta, tb = toks(a), toks(b)
    sb = set(tb)
    best = cur = 0
    for t in ta:
        cur = cur + 1 if t in sb else 0
        best = max(best, cur)
    return best

def is_dup(cand, others):
    for o in others:
        if consec_run(cand['name'], o['name']) >= 6: return o['name']
        if overlap_ratio(cand['name'], o['name']) >= 0.7: return o['name']
    return None

def slugify(name):
    s = re.sub(r"['\u2019]", "", f"temu-{name}".lower())
    return re.sub(r"[^a-z0-9]+", "-", s).strip('-')[:71].rstrip('-')

def download(url, dest):
    if os.path.exists(dest) and os.path.getsize(dest) > 0: return True
    try:
        r = subprocess.run(['curl', '-sL', '-f', '--retry', '3', '--retry-delay', '4',
            '-A', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
            '--max-time', '120', '-o', dest, url], capture_output=True, timeout=150)
        return r.returncode == 0 and os.path.exists(dest) and os.path.getsize(dest) > 0
    except Exception as e:
        print(f'DOWNLOAD FAILED {url[:70]}: {e}'); return False

data = json.load(open(f'{BASE}/data/products.json'))
existing_ids = {p['id'] for p in data['products']}
existing_affs = {p['affiliate_url'] for p in data['products']}
img_dir = f'{BASE}/images'; os.makedirs(img_dir, exist_ok=True)

staged, skipped, seen = [], [], []
for cand in CANDIDATES:
    name = cand['name']
    if cand['aff'] in existing_affs:
        skipped.append((name, 'affiliate URL collision')); continue
    d = is_dup(cand, data['products'])
    if d: skipped.append((name, f'duplicate of staged: {d[:60]}')); continue
    d2 = is_dup(cand, seen)
    if d2: skipped.append((name, f'near-duplicate in batch: {d2[:60]}')); continue
    pid, base, n = slugify(name), None, 2
    base = pid
    while pid in existing_ids:
        pid = f"{base}-{n}"[:71].rstrip('-'); n += 1
    if not download(cand['img'], f'{img_dir}/{pid}.jpg'):
        skipped.append((name, 'image download failed')); continue
    rec = {'id': pid, 'name': name, 'merchant': 'temu', 'category': cand['category'],
        'subcategory': cand['subcategory'], 'affiliate_url': cand['aff'],
        'image_url': cand['img'], 'key_features': [cand['trend']],
        'pros': [f"Trending find on Temu — {cand['trend']}"], 'cons': [
            'Temu prices change frequently \u2014 confirm the live price before buying',
            'Check the live Temu listing for current colors and sizes'],
        'badges': ['new'], 'rating': None, 'sold_count': None, 'sample': False,
        'short_description': f"{name} \u2014 {cand['trend']}",
        'source': f'Temu public listing \u2014 verified {TODAY}',
        'trend_status': 'trending', 'updated': TODAY}
    data['products'].append(rec)
    existing_ids.add(pid); existing_affs.add(cand['aff']); seen.append(cand)
    staged.append(rec)

with open(f'{BASE}/data/products.json', 'w') as f:
    json.dump(data, f, indent=2, ensure_ascii=False)
json.dump({'staged': [{'id': p['id'], 'name': p['name'], 'category': p['category'],
    'affiliate_url': p['affiliate_url']} for p in staged],
    'skipped': skipped, 'total_products': len(data['products'])},
    open(f'{BASE}/tools/staged-us-trending-2026-09-30-r1.json', 'w'), indent=2)
print(f"STAGED: {len(staged)} | SKIPPED: {len(skipped)}")
for s in skipped: print('SKIPPED:', s[0][:60], '->', s[1][:70])
print('TOTAL PRODUCTS:', len(data['products']))
