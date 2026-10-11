#!/usr/bin/env python3
"""Generate paginated chunk files + precomputed section data for listing pages.

Reads data/products-lite.json (run tools/gen_lite.py FIRST after every
product staging batch) and writes:
  data/pages/all/page-N.json          full catalog, 48/page, catalog order
  data/pages/cat-<id>/page-N.json     per-category chunks, 48/page
  data/pages/trending/page-N.json     trending (viral first), 48/page
  data/home.json                      precomputed home sections
  data/deals.json                     QA_DEAL_IDS order (parsed from deals.html)

Chunk format: {"products":[...], "page":N, "pages":T, "total":C}
Dead listings (status=="dead") are excluded, matching applyFilters in app.js.
Re-run after every product staging batch, right after gen_lite.py.
"""
import json
import os
import re

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LITE = os.path.join(BASE, "data", "products-lite.json")
PAGES_DIR = os.path.join(BASE, "data", "pages")
HOME_JSON = os.path.join(BASE, "data", "home.json")
DEALS_JSON = os.path.join(BASE, "data", "deals.json")
DEALS_HTML = os.path.join(BASE, "deals.html")

PAGE_SIZE = 48


def write_chunk(path, products, page, pages, total):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(
            {"products": products, "page": page, "pages": pages, "total": total},
            f,
            ensure_ascii=False,
            separators=(",", ":"),
        )


def paginate(products, out_dir):
    total = len(products)
    pages = max(1, (total + PAGE_SIZE - 1) // PAGE_SIZE)
    for n in range(1, pages + 1):
        chunk = products[(n - 1) * PAGE_SIZE : n * PAGE_SIZE]
        write_chunk(os.path.join(out_dir, f"page-{n}.json"), chunk, n, pages, total)
    return pages


def main():
    with open(LITE, encoding="utf-8") as f:
        products = json.load(f)["products"]
    live = [p for p in products if p.get("status") != "dead"]
    print(f"live products: {len(live)} (excluded {len(products) - len(live)} dead)")

    # 1. Full catalog chunks (catalog order)
    n_all = paginate(live, os.path.join(PAGES_DIR, "all"))
    print(f"all: {n_all} pages")

    # 2. Per-category chunks (catalog order within category)
    cats = sorted({p.get("category") for p in live if p.get("category")})
    for cat in cats:
        cat_products = [p for p in live if p.get("category") == cat]
        n = paginate(cat_products, os.path.join(PAGES_DIR, f"cat-{cat}"))
        print(f"cat-{cat}: {n} pages ({len(cat_products)} products)")

    # 3. Trending chunks (viral first, stable within groups — mirrors app.js)
    trending = [p for p in live if p.get("trend_status")]
    trending.sort(key=lambda p: 0 if p.get("trend_status") == "viral" else 1)
    n_tr = paginate(trending, os.path.join(PAGES_DIR, "trending"))
    print(f"trending: {n_tr} pages ({len(trending)} products)")

    # 4. Home sections (mirrors pages.home in app.js)
    by_rating = sorted(live, key=lambda p: p.get("rating") or 0, reverse=True)
    home = {
        "trending": [p for p in live if p.get("trend_status")][:8],
        "best": [p for p in live if "best-seller" in (p.get("badges") or [])][:4],
        "top": by_rating[:4],
        "editors": by_rating[:4],
    }
    with open(HOME_JSON, "w", encoding="utf-8") as f:
        json.dump(home, f, ensure_ascii=False, separators=(",", ":"))
    print(f"home.json: {sum(len(v) for v in home.values())} section products")

    # 5. Deals (QA_DEAL_IDS order from deals.html)
    with open(DEALS_HTML, encoding="utf-8") as f:
        html = f.read()
    m = re.search(r"window\.QA_DEAL_IDS\s*=\s*(\[.*?\]);", html, re.S)
    if not m:
        raise SystemExit("QA_DEAL_IDS not found in deals.html")
    deal_ids = json.loads(m.group(1))
    by_id = {p["id"]: p for p in live}
    deals = []
    missing = []
    for did in deal_ids:
        if did in by_id:
            deals.append(by_id[did])
        else:
            missing.append(did)
    with open(DEALS_JSON, "w", encoding="utf-8") as f:
        json.dump({"products": deals}, f, ensure_ascii=False, separators=(",", ":"))
    print(f"deals.json: {len(deals)} products" + (f" (missing: {len(missing)})" if missing else ""))
    if missing:
        print("  missing ids:", ", ".join(missing[:10]))

    # Size report
    import glob

    total_bytes = sum(
        os.path.getsize(p)
        for p in glob.glob(os.path.join(PAGES_DIR, "**", "*.json"), recursive=True)
    )
    first = os.path.getsize(os.path.join(PAGES_DIR, "all", "page-1.json"))
    lite_bytes = os.path.getsize(LITE)
    print(f"pages total on disk: {total_bytes/1e6:.2f} MB in {len(glob.glob(os.path.join(PAGES_DIR, '**', '*.json'), recursive=True))} files")
    print(f"page-1 chunk: {first/1e3:.1f} KB vs full lite: {lite_bytes/1e6:.2f} MB")


if __name__ == "__main__":
    main()
