#!/usr/bin/env python3
"""Generate data/products-lite.json — slim catalog for listing pages.

Listing pages (home, browse, category, deals, trending) only need card fields.
The full products.json (5.5MB) is then loaded ONLY on product detail pages.
Re-run after every product staging batch.
"""
import json, os

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(BASE, "data", "products.json")
DST = os.path.join(BASE, "data", "products-lite.json")

LITE_FIELDS = [
    "id", "name", "price", "currency", "original_price", "old_price",
    "image_url", "category", "subcategory", "merchant", "badges",
    "trend_status", "rating", "sold_count", "status", "affiliate_url",
    "short_description", "updated",
]

def main():
    with open(SRC, encoding="utf-8") as f:
        data = json.load(f)
    lite = {"products": []}
    for p in data.get("products", []):
        lite["products"].append({k: p.get(k) for k in LITE_FIELDS if k in p})
    with open(DST, "w", encoding="utf-8") as f:
        json.dump(lite, f, ensure_ascii=False, separators=(",", ":"))
    s_src = os.path.getsize(SRC)
    s_dst = os.path.getsize(DST)
    print(f"full: {s_src/1e6:.2f} MB -> lite: {s_dst/1e6:.2f} MB "
          f"({100*(1-s_dst/s_src):.0f}% smaller), {len(lite['products'])} products")

if __name__ == "__main__":
    main()
