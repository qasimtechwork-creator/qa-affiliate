#!/usr/bin/env python3
"""
AliExpress Affiliate API importer for QA Affiliate.

Fetches REAL women's products from the AliExpress Open Platform Affiliate API,
generates tracked affiliate links, downloads real merchant images, and builds
product entries matching data/products.json's EXACT schema.

HARD RULES (never violated):
  - Never invent prices, ratings, discounts, review counts, or product claims.
  - Only merchant/API-provided data is used. AliExpress `evaluate_rate` is a
    positive-feedback PERCENTAGE, not a star rating -> it is NEVER converted
    into the schema's `rating` field; `rating` is omitted unless the API ever
    returns a true star rating.
  - Real merchant images only, downloaded to assets/images/products/aliexpress/.
  - Secrets (app key/secret) come ONLY from env vars or tools/.alix_secrets.json
    (gitignored). They are NEVER hardcoded and NEVER printed in logs.

CREDENTIALS: see tools/ALIEXPRESS_API_SETUP.md

Usage:
  python3 tools/aliexpress_import.py --dry-run
  python3 tools/aliexpress_import.py --limit 5 --category jewelry
  python3 tools/aliexpress_import.py --limit 20 --merge
  python3 tools/aliexpress_import.py --sign-method md5 --limit 3

API NOTES (assumptions marked [ASSUMED]):
  Endpoint: https://api-sg.aliexpress.com/sync (fallback https://api.aliexpress.com/sync)
  Auth: TOP-style signed requests. sign = HMAC-SHA256(secret, concat(sorted k+v)),
        uppercase hex. md5 variant also supported via --sign-method.
  Methods used:
    - aliexpress.affiliate.product.query   (search products)
    - aliexpress.affiliate.link.generate   (tracked links)
    - aliexpress.affiliate.hotproduct.query (optional, via --hot)
  Response field names below follow the public Open Platform docs as of 2026;
  every one is marked [ASSUMED] and the parser is defensive (.get with fallbacks).
  If the live API returns different shapes, run with --debug to dump raw JSON.
"""

import argparse
import hashlib
import hmac
import json
import os
import re
import sys
import time
from datetime import date
from urllib.parse import urlparse

try:
    import requests
except ImportError:
    sys.exit("ERROR: 'requests' is required. Install with: pip install requests")

try:
    from PIL import Image
    HAVE_PIL = True
except ImportError:
    HAVE_PIL = False

SITE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PRODUCTS_JSON = os.path.join(SITE_DIR, "data", "products.json")
CATEGORIES_JSON = os.path.join(SITE_DIR, "data", "categories.json")
IMG_DIR = os.path.join(SITE_DIR, "assets", "images", "products", "aliexpress")
SECRETS_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), ".alix_secrets.json")
OUTPUT_JSON = os.path.join(os.path.dirname(os.path.abspath(__file__)), "aliexpress_import_output.json")

API_BASES = ["https://api-sg.aliexpress.com/sync", "https://api.aliexpress.com/sync"]
TRACKING_ID = os.environ.get("ALIX_TRACKING_ID", "default")  # portal Tracking ID (not secret)
TODAY = date.today().isoformat()

# Site category -> AliExpress search keywords (women's products)
CATEGORY_QUERIES = {
    "fashion": ["women summer dress", "women casual blouse top"],
    "shoes": ["women high heels sandals", "women white sneakers"],
    "jewelry": ["women gold plated earrings", "women pendant necklace"],
    "bags": ["women leather handbag", "women shoulder bag"],
    "beauty": ["makeup brush set professional", "matte lipstick set women"],
    "skincare": ["vitamin c face serum", "hydrating facial mask"],
    "haircare": ["hair straightener brush", "automatic hair curler"],
    "accessories": ["women polarized sunglasses", "women silk scarf"],
    "lingerie": ["women lace underwear set", "women satin pajama set"],
    "fitness": ["women high waist yoga leggings", "resistance bands set"],
    "viral": ["portable mini blender usb", "led vanity makeup mirror"],
}

# Exact schema contract (mirrors existing products.json entries)
REQUIRED_FIELDS = {
    "id": str, "name": str, "category": str, "merchant": str,
    "affiliate_url": str, "image_url": str, "short_description": str,
    "pros": list, "cons": list, "key_features": list, "badges": list,
    "source": str, "updated": str, "sample": bool,
}
OPTIONAL_FIELDS = {
    "rating": float, "sold_count": str, "subcategory": str,
    "trend_status": (str, type(None)),
}
FORBIDDEN_SUBSTRINGS = ("price", "discount_pct", "review_count", "reviews_count")
ALLOWED_CATEGORIES = None  # loaded from data/categories.json

# ----------------------------------------------------------------------------
# Credentials: env vars first, then gitignored JSON file. Never logged.
# ----------------------------------------------------------------------------
def load_credentials():
    key = os.environ.get("ALIX_APP_KEY")
    secret = os.environ.get("ALIX_APP_SECRET")
    session = os.environ.get("ALIX_SESSION")  # optional OAuth session token [ASSUMED]
    source = "env"
    if not (key and secret) and os.path.exists(SECRETS_FILE):
        try:
            with open(SECRETS_FILE) as f:
                data = json.load(f)
            key = key or data.get("app_key")
            secret = secret or data.get("app_secret")
            session = session or data.get("session")
            source = "tools/.alix_secrets.json"
        except Exception as e:
            sys.exit(f"ERROR: could not read {SECRETS_FILE}: {e}")
    if not (key and secret):
        return None, None, None, None
    return key.strip(), secret.strip(), (session or "").strip() or None, source


def mask(s, keep=4):
    if not s:
        return "(missing)"
    return s[:keep] + "..." + ("<%d chars>" % len(s))


# ----------------------------------------------------------------------------
# Signed API client (TOP-style). [ASSUMED] sign scheme per public docs; the
# script supports md5 and hmac-sha256 and surfaces raw error_response text so
# a wrong assumption fails loudly instead of silently.
# ----------------------------------------------------------------------------
class AlixClient:
    def __init__(self, app_key, app_secret, session=None, sign_method="hmac-sha256", debug=False):
        self.app_key = app_key
        self.app_secret = app_secret
        self.session = session
        self.sign_method = sign_method
        self.debug = debug
        self.base_idx = 0

    def _sign(self, params):
        items = sorted((k, v) for k, v in params.items() if k != "sign" and v not in (None, ""))
        raw = "".join(f"{k}{v}" for k, v in items)
        if self.sign_method == "md5":
            # TOP v2 md5: md5(secret + raw + secret)
            digest = hashlib.md5((self.app_secret + raw + self.app_secret).encode()).hexdigest()
        else:  # hmac-sha256
            digest = hmac.new(self.app_secret.encode(), raw.encode(), hashlib.sha256).hexdigest()
        return digest.upper()

    def call(self, method, biz_params):
        sys_params = {
            "method": method,
            "app_key": self.app_key,
            "timestamp": str(int(time.time() * 1000)),
            "format": "json",
            "v": "2.0",
            "sign_method": self.sign_method,
        }
        if self.session:
            sys_params["session"] = self.session  # [ASSUMED] OAuth session param name
        params = dict(sys_params)
        params.update({k: v for k, v in biz_params.items() if v not in (None, "")})
        params["sign"] = self._sign(params)

        last_err = None
        for attempt in range(len(API_BASES)):
            base = API_BASES[(self.base_idx + attempt) % len(API_BASES)]
            try:
                r = requests.post(base, data=params, timeout=30)
                data = r.json()
            except Exception as e:
                last_err = f"HTTP/parse error on {base}: {e}"
                continue
            if self.debug:
                print(json.dumps(data, indent=1)[:3000])
            err = data.get("error_response")
            if err:
                # Fail LOUDLY: never convert API errors into empty results.
                raise RuntimeError(
                    f"API error_response [{err.get('code')}]: {err.get('msg')}"
                )
            self.base_idx = (self.base_idx + attempt) % len(API_BASES)
            return data
        raise RuntimeError(f"All API bases failed. Last: {last_err}")


# ----------------------------------------------------------------------------
# Product search + link generation.
# [ASSUMED] request/response field names per public Open Platform docs.
# ----------------------------------------------------------------------------
def search_products(client, keywords, page_no=1, page_size=20):
    """[ASSUMED] method aliexpress.affiliate.product.query"""
    resp = client.call("aliexpress.affiliate.product.query", {
        "keywords": keywords,                    # [ASSUMED] param name
        "tracking_id": TRACKING_ID,              # [ASSUMED] param name
        "target_currency": "USD",                # [ASSUMED]
        "target_language": "EN",                 # [ASSUMED]
        "ship_to_country": "US",                 # [ASSUMED]
        "page_no": str(page_no),                 # [ASSUMED]
        "page_size": str(page_size),             # [ASSUMED]
        "sort": "volume_desc",                   # [ASSUMED] best-sellers first
    })
    # [ASSUMED] response path: <method>_response -> resp_result -> result -> products -> product[]
    body = resp.get("aliexpress_affiliate_product_query_response", {})
    result = body.get("resp_result", {}).get("result", {})
    products = result.get("products", {}).get("product", [])
    return products if isinstance(products, list) else [products]


def hot_products(client, category_id=None, page_no=1, page_size=20):
    """[ASSUMED] method aliexpress.affiliate.hotproduct.query"""
    biz = {
        "tracking_id": TRACKING_ID,
        "target_currency": "USD",
        "target_language": "EN",
        "page_no": str(page_no),
        "page_size": str(page_size),
    }
    if category_id:
        biz["category_ids"] = str(category_id)  # [ASSUMED]
    resp = client.call("aliexpress.affiliate.hotproduct.query", biz)
    body = resp.get("aliexpress_affiliate_hotproduct_query_response", {})
    result = body.get("resp_result", {}).get("result", {})
    products = result.get("products", {}).get("product", [])
    return products if isinstance(products, list) else [products]


def generate_tracked_link(client, product_url, link_name="QA Affiliate"):
    """[ASSUMED] method aliexpress.affiliate.link.generate -> s.click.aliexpress.com link."""
    resp = client.call("aliexpress.affiliate.link.generate", {
        "promotion_link_type": "0",            # [ASSUMED] 0 = normal product link
        "promotion_link_name": link_name,      # [ASSUMED]
        "tracking_id": TRACKING_ID,            # [ASSUMED]
        "source_values": product_url,          # [ASSUMED] comma-separated URLs/IDs
        "target_currency": "USD",              # [ASSUMED]
        "target_language": "EN",               # [ASSUMED]
    })
    body = resp.get("aliexpress_affiliate_link_generate_response", {})
    result = body.get("resp_result", {}).get("result", {})
    links = result.get("promotion_links", {}).get("promotion_link", [])
    links = links if isinstance(links, list) else [links]
    for l in links:
        url = l.get("promotion_link") or ""
        if url.startswith("https://s.click.aliexpress.com/"):
            return url
    return None

# ----------------------------------------------------------------------------
# Entry builder — honest fields only. Mirrors the existing products.json schema.
# ----------------------------------------------------------------------------
def clean_title(t):
    t = re.sub(r"\s+", " ", (t or "")).strip()
    return t[:160]


def product_id_from(api_product):
    # [ASSUMED] field: product_id
    pid = str(api_product.get("product_id") or api_product.get("productId") or "")
    pid = re.sub(r"[^a-zA-Z0-9_-]", "", pid)
    return f"aliexpress-{pid}" if pid else ""


def download_image(img_url, entry_id):
    """Download the REAL merchant image. Returns the site-absolute image_url."""
    os.makedirs(IMG_DIR, exist_ok=True)
    dest = os.path.join(IMG_DIR, f"{entry_id}.jpg")
    try:
        r = requests.get(img_url, timeout=30, headers={"User-Agent": "Mozilla/5.0"})
        r.raise_for_status()
        raw = r.content
        if HAVE_PIL:
            from io import BytesIO
            im = Image.open(BytesIO(raw)).convert("RGB")
            im.thumbnail((1200, 1200), Image.LANCZOS)
            im.save(dest, "JPEG", quality=88)
        else:
            with open(dest, "wb") as f:
                f.write(raw)
        return f"/assets/images/products/aliexpress/{entry_id}.jpg"
    except Exception as e:
        print(f"  !! image download failed for {entry_id}: {e}")
        return None


def build_entry(api_product, category, subcategory, affiliate_url, image_url):
    """Build one products.json entry from API data. No invented fields, ever."""
    # [ASSUMED] API field names below; each has a defensive fallback.
    title = clean_title(api_product.get("product_title") or api_product.get("productTitle"))
    pid = product_id_from(api_product)
    entry = {
        "id": pid,
        "name": title,
        "category": category,
        "merchant": "aliexpress",
        "affiliate_url": affiliate_url,
        "image_url": image_url,
        "short_description": f"{title} — available on AliExpress with buyer protection.",
        "pros": ["Covered by AliExpress buyer protection on every order"],
        "cons": [
            "Price varies — see the live AliExpress deal before buying",
            "Check the live AliExpress listing for current colors, sizes and shipping times",
        ],
        "key_features": [],
        "badges": [],
        "source": f"AliExpress Open Platform API — imported {TODAY}",
        "updated": TODAY,
        "sample": False,
    }
    if subcategory:
        entry["subcategory"] = subcategory

    # Merchant-provided positive-feedback % -> honest pro (NOT a star rating).
    # [ASSUMED] field: evaluate_rate like "95.3%"
    ev = api_product.get("evaluate_rate") or api_product.get("evaluateRate")
    if ev:
        m = re.search(r"([\d.]+)", str(ev))
        if m:
            entry["pros"].append(
                f"{m.group(1)}% positive feedback on AliExpress (merchant data)"
            )

    # Merchant-provided order volume -> sold_count (same pattern as existing entries).
    # [ASSUMED] field: lastest_volume (sic, as in public docs)
    vol = api_product.get("lastest_volume") or api_product.get("volume")
    if vol:
        try:
            n = int(str(vol).replace(",", ""))
            entry["sold_count"] = f"{n // 1000}K+ sold" if n >= 1000 else f"{n} sold"
            entry["key_features"].append(
                f"{entry['sold_count'].replace(' sold', '')} orders on AliExpress (per listing)"
            )
        except ValueError:
            pass

    # Merchant-listed discount % -> honest key feature (NOT an invented claim).
    # [ASSUMED] field: discount like "20%"
    disc = api_product.get("discount")
    if disc and str(disc).strip() not in ("", "0", "0%"):
        entry["key_features"].append(
            f"Merchant-listed discount {disc} on the live AliExpress listing"
        )

    # NOTE: `rating` is deliberately omitted. AliExpress returns evaluate_rate
    # (a feedback percentage), which must never be presented as a star rating.
    return entry


# ----------------------------------------------------------------------------
# Schema validation — the exact contract data/products.json consumers expect.
# ----------------------------------------------------------------------------
def load_allowed_categories():
    global ALLOWED_CATEGORIES
    try:
        with open(CATEGORIES_JSON) as f:
            ALLOWED_CATEGORIES = {c["id"] for c in json.load(f)["categories"]}
    except Exception:
        ALLOWED_CATEGORIES = set(CATEGORY_QUERIES)


def validate_entry(e):
    errors = []
    for field, typ in REQUIRED_FIELDS.items():
        if field not in e:
            errors.append(f"missing required field '{field}'")
        elif not isinstance(e[field], typ):
            errors.append(f"field '{field}' must be {typ.__name__}, got {type(e[field]).__name__}")
        elif typ is str and not e[field].strip():
            errors.append(f"field '{field}' must not be empty")
        elif typ is list and field != "badges" and not e[field]:
            errors.append(f"field '{field}' must not be empty")
        # NOTE: 'badges' may legitimately be [] (product has no badge).
    for field, typ in OPTIONAL_FIELDS.items():
        if field in e and e[field] is not None and not isinstance(e[field], typ):
            errors.append(f"optional field '{field}' wrong type")
    if e.get("merchant") != "aliexpress":
        errors.append("merchant must be 'aliexpress'")
    if e.get("category") not in (ALLOWED_CATEGORIES or set()):
        errors.append(f"unknown category '{e.get('category')}'")
    url = e.get("affiliate_url", "")
    if not url.startswith("https://s.click.aliexpress.com/"):
        errors.append("affiliate_url must be a real s.click.aliexpress.com tracked link")
    if not (e.get("image_url") or "").startswith("/assets/images/products/aliexpress/"):
        errors.append("image_url must be a local /assets/images/products/aliexpress/ path")
    blob = json.dumps(e).lower()
    for bad in FORBIDDEN_SUBSTRINGS:
        if f'"{bad}"' in blob:
            errors.append(f"forbidden invented-data field '{bad}'")
    if "rating" in e:
        r = e["rating"]
        if not isinstance(r, (int, float)) or isinstance(r, bool) or not (0 <= r <= 5):
            errors.append("rating must be a 0-5 star number or omitted")
    if not re.fullmatch(r"aliexpress-[A-Za-z0-9_-]+", e.get("id", "")):
        errors.append("id must look like 'aliexpress-<product-id>'")
    return errors

# ----------------------------------------------------------------------------
# Import flow
# ----------------------------------------------------------------------------
def import_category(client, category, limit, args):
    queries = CATEGORY_QUERIES[category]
    entries, seen = [], set()
    for qi, q in enumerate(queries):
        if len(entries) >= limit:
            break
        page = 1
        while len(entries) < limit:
            try:
                prods = search_products(client, q, page_no=page, page_size=20)
            except RuntimeError as e:
                print(f"  !! search failed for '{q}': {e}")
                break
            if not prods:
                break
            for p in prods:
                if len(entries) >= limit:
                    break
                pid = product_id_from(p)
                # [ASSUMED] fields: product_detail_url, product_main_image_url
                detail = p.get("product_detail_url") or p.get("productDetailUrl") or ""
                img = (p.get("product_main_image_url")
                       or p.get("productMainImageUrl") or "")
                title = clean_title(p.get("product_title") or p.get("productTitle"))
                if not (pid and detail and img and title) or pid in seen:
                    continue
                seen.add(pid)
                print(f"  + {pid}: {title[:70]}")
                try:
                    link = generate_tracked_link(client, detail)
                except RuntimeError as e:
                    print(f"    !! link generation failed: {e}")
                    link = None
                if not link:
                    print("    !! skipped: no tracked link (use portal Link Generator manually, see SETUP doc)")
                    continue
                time.sleep(0.6)  # polite pacing between API calls
                image_url = download_image(img, pid)
                if not image_url:
                    print("    !! skipped: image download failed")
                    continue
                subcat = CATEGORY_QUERIES[category][qi].split()[-1]
                entry = build_entry(p, category, subcat, link, image_url)
                errs = validate_entry(entry)
                if errs:
                    print(f"    !! schema errors, skipped: {errs}")
                    try:
                        os.remove(os.path.join(IMG_DIR, f"{pid}.jpg"))
                    except OSError:
                        pass
                    continue
                entries.append(entry)
                time.sleep(0.6)
            page += 1
            if page > 5:
                break
    return entries


def dry_run():
    """Validate the schema against 2 synthetic sample entries. No API calls."""
    load_allowed_categories()
    samples = [
        {
            "id": "aliexpress-1005009999999999",
            "name": "Women's Floral Summer Midi Dress — Bohemian Beach Sundress",
            "category": "fashion",
            "merchant": "aliexpress",
            "affiliate_url": "https://s.click.aliexpress.com/e/_sampleA1",
            "image_url": "/assets/images/products/aliexpress/aliexpress-1005009999999999.jpg",
            "short_description": "Women's Floral Summer Midi Dress — Bohemian Beach Sundress — available on AliExpress with buyer protection.",
            "pros": ["Covered by AliExpress buyer protection on every order",
                     "96.2% positive feedback on AliExpress (merchant data)"],
            "cons": ["Price varies — see the live AliExpress deal before buying",
                     "Check the live AliExpress listing for current colors, sizes and shipping times"],
            "key_features": ["12K+ orders on AliExpress (per listing)"],
            "badges": [],
            "sold_count": "12K+ sold",
            "subcategory": "dress",
            "trend_status": None,
            "source": "AliExpress Open Platform API — imported 2026-09-28 (DRY-RUN SAMPLE)",
            "updated": TODAY,
            "sample": False,
        },
        {
            "id": "aliexpress-1005008888888888",
            "name": "Gold Plated Zircon Drop Earrings for Women — Fashion Jewelry",
            "category": "jewelry",
            "merchant": "aliexpress",
            "affiliate_url": "https://s.click.aliexpress.com/e/_sampleB2",
            "image_url": "/assets/images/products/aliexpress/aliexpress-1005008888888888.jpg",
            "short_description": "Gold Plated Zircon Drop Earrings for Women — Fashion Jewelry — available on AliExpress with buyer protection.",
            "pros": ["Covered by AliExpress buyer protection on every order"],
            "cons": ["Price varies — see the live AliExpress deal before buying",
                     "Check the live AliExpress listing for current colors, sizes and shipping times"],
            "key_features": ["Merchant-listed discount 30% on the live AliExpress listing"],
            "badges": [],
            "subcategory": "earrings",
            "trend_status": None,
            "source": "AliExpress Open Platform API — imported 2026-09-28 (DRY-RUN SAMPLE)",
            "updated": TODAY,
            "sample": False,
        },
    ]
    ok = True
    for s in samples:
        errs = validate_entry(s)
        status = "PASS" if not errs else f"FAIL: {errs}"
        if errs:
            ok = False
        print(f"[dry-run] {s['id']}: {status}")
    # Also validate the negative case: a bad entry MUST be rejected.
    bad = dict(samples[0])
    bad["affiliate_url"] = "https://www.aliexpress.com/item/123.html"  # untracked
    bad_errs = validate_entry(bad)
    print(f"[dry-run] negative test (untracked URL rejected): {'PASS' if bad_errs else 'FAIL — bad entry accepted!'}")
    if not bad_errs:
        ok = False
    bad2 = dict(samples[0])
    bad2["rating"] = 4.8  # rating present but evaluate_rate-style % would be wrong
    # rating as a proper 0-5 float is allowed by schema; the rule is enforced in
    # build_entry which never sets it from evaluate_rate. Just show it validates.
    print(f"[dry-run] rating-type check: {'PASS' if not validate_entry(bad2) else 'FAIL'}")
    with open("/tmp/aliexpress_dryrun_sample.json", "w") as f:
        json.dump(samples, f, indent=2)
    print("[dry-run] sample entries written to /tmp/aliexpress_dryrun_sample.json (NOT added to products.json)")
    print(f"[dry-run] overall: {'ALL CHECKS PASSED' if ok else 'FAILURES PRESENT'}")
    return 0 if ok else 1


def merge_into_products(entries):
    with open(PRODUCTS_JSON) as f:
        data = json.load(f)
    existing = {p["id"] for p in data["products"]}
    added = 0
    for e in entries:
        if e["id"] in existing:
            print(f"  -- skipped duplicate {e['id']}")
            continue
        data["products"].append(e)
        existing.add(e["id"])
        added += 1
    with open(PRODUCTS_JSON, "w") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
        f.write("\n")
    print(f"Merged {added} new AliExpress products into data/products.json (total {len(data['products'])})")
    return added


def main():
    ap = argparse.ArgumentParser(description="Import real AliExpress affiliate products into QA Affiliate.")
    ap.add_argument("--dry-run", action="store_true", help="Validate schema on 2 samples; no API calls.")
    ap.add_argument("--limit", type=int, default=5, help="Max products PER category (default 5).")
    ap.add_argument("--category", choices=list(CATEGORY_QUERIES), help="Import one category only.")
    ap.add_argument("--hot", action="store_true", help="Use hotproduct.query instead of keyword search (fewer categories).")
    ap.add_argument("--merge", action="store_true", help="Append validated entries to data/products.json (default: write review file only).")
    ap.add_argument("--sign-method", choices=["hmac-sha256", "md5"], default="hmac-sha256")
    ap.add_argument("--debug", action="store_true", help="Dump raw API JSON (truncated).")
    args = ap.parse_args()

    load_allowed_categories()

    if args.dry_run:
        return dry_run()

    key, secret, session, source = load_credentials()
    if not (key and secret):
        sys.exit(
            "ERROR: no AliExpress credentials found.\n"
            "  Set ALIX_APP_KEY and ALIX_APP_SECRET env vars, or create\n"
            "  tools/.alix_secrets.json (gitignored) — see tools/ALIEXPRESS_API_SETUP.md"
        )
    print(f"Credentials loaded from {source} (key {mask(key)}; secret never shown)")
    if session:
        print("OAuth session token present (will be sent as 'session' param).")

    client = AlixClient(key, secret, session=session, sign_method=args.sign_method, debug=args.debug)
    cats = [args.category] if args.category else list(CATEGORY_QUERIES)
    all_entries = []
    for cat in cats:
        print(f"[{cat}] importing up to {args.limit} products...")
        if args.hot:
            prods, entries, seen = [], [], set()
            for page in range(1, 4):
                try:
                    batch = hot_products(client, page_no=page, page_size=20)
                except RuntimeError as e:
                    print(f"  !! hotproduct query failed: {e}")
                    break
                if not batch:
                    break
                for p in batch:
                    if len(entries) >= args.limit:
                        break
                    pid = product_id_from(p)
                    detail = p.get("product_detail_url") or ""
                    img = p.get("product_main_image_url") or ""
                    title = clean_title(p.get("product_title"))
                    if not (pid and detail and img and title) or pid in seen:
                        continue
                    seen.add(pid)
                    link = generate_tracked_link(client, detail)
                    if not link:
                        continue
                    image_url = download_image(img, pid)
                    if not image_url:
                        continue
                    e = build_entry(p, cat, None, link, image_url)
                    if validate_entry(e):
                        continue
                    entries.append(e)
                    time.sleep(0.6)
            all_entries.extend(entries)
        else:
            all_entries.extend(import_category(client, cat, args.limit, args))

    print(f"\nImported {len(all_entries)} validated AliExpress products.")
    with open(OUTPUT_JSON, "w") as f:
        json.dump(all_entries, f, indent=2, ensure_ascii=False)
    print(f"Review file: {OUTPUT_JSON}")
    if args.merge and all_entries:
        merge_into_products(all_entries)
    elif all_entries:
        print("Tip: re-run with --merge to append these to data/products.json")
    return 0


if __name__ == "__main__":
    sys.exit(main())
