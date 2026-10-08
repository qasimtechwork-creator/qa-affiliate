#!/usr/bin/env python3
"""Check all affiliate links: HTTP status + final redirect destination."""
import json, urllib.request, urllib.error, concurrent.futures, sys
from pathlib import Path

HOME = Path.home()
SITE = HOME / "workspace/affiliate-site"
OUT = SITE / "hidden_files/link-check-results.json"

def check(pid, url):
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 Chrome/120 Safari/537.36"}, method="HEAD")
    try:
        with urllib.request.urlopen(req, timeout=15) as r:
            return {"id": pid, "url": url, "status": r.status, "final": r.url, "ok": True}
    except urllib.error.HTTPError as e:
        return {"id": pid, "url": url, "status": e.code, "final": e.url if hasattr(e, 'url') else url, "ok": False, "err": f"HTTP {e.code}"}
    except Exception as e:
        return {"id": pid, "url": url, "status": 0, "final": url, "ok": False, "err": str(e)[:80]}

def main():
    d = json.load(open(SITE / "data/products.json"))
    prods = d["products"] if isinstance(d, dict) else d
    items = [(p["id"], p["affiliate_url"]) for p in prods if p.get("affiliate_url")]
    print(f"Checking {len(items)} links...", flush=True)
    results = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=20) as ex:
        futs = {ex.submit(check, pid, url): pid for pid, url in items}
        for i, f in enumerate(concurrent.futures.as_completed(futs)):
            results.append(f.result())
            if (i+1) % 200 == 0:
                print(f"  {i+1}/{len(items)} done", flush=True)
    bad = [r for r in results if not r["ok"]]
    json.dump({"total": len(results), "bad": len(bad), "results": results}, open(OUT, "w"), indent=1)
    print(f"DONE: {len(results)} checked, {len(bad)} failed")
    for r in bad[:20]:
        print(f"  FAIL {r['id']}: {r.get('err')}")

if __name__ == "__main__":
    main()
