#!/usr/bin/env python3
"""QA Affiliate full-catalog affiliate-link audit (2026-10-02).
For every staged product: open affiliate_url (follow redirects, browser UA),
record final URL/status, classify OK / CHALLENGE / BROKEN / ERROR.
Also verifies go/<id>.html exists locally and matches the affiliate_url.
Output: hidden_files/link-audit-2026-10-02.json + stdout summary."""
import json, os, re, sys, time
import urllib.request, urllib.error
from concurrent.futures import ThreadPoolExecutor, as_completed

BASE = os.path.expanduser('~/workspace/affiliate-site')
UA = ('Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 '
      '(KHTML, like Gecko) Chrome/126.0 Safari/537.36')

def check(item):
    pid, url, merchant = item
    req = urllib.request.Request(url, headers={'User-Agent': UA,
        'Accept': 'text/html,application/xhtml+xml', 'Accept-Language': 'en-US,en;q=0.9'})
    try:
        with urllib.request.urlopen(req, timeout=25) as r:
            final, code = r.geturl(), r.status
            r.read(2048)
    except urllib.error.HTTPError as e:
        final, code = e.geturl() or url, e.code
        try: e.read(2048)
        except Exception: pass
    except Exception as e:
        return {'id': pid, 'merchant': merchant, 'affiliate_url': url,
                'http': None, 'final_url': url, 'verdict': 'ERROR', 'detail': str(e)[:120]}
    host = re.sub(r'^https?://', '', final).split('/')[0]
    low = final.lower()
    if 'bgn_verification' in low or 'security-verification' in low or 'captcha' in low:
        verdict = 'CHALLENGE'
    elif code and code < 400 and (('temu.com' in host and merchant == 'temu') or
                                   ('aliexpress.com' in host and merchant == 'aliexpress')):
        verdict = 'OK'
    elif code and code < 400:
        verdict = 'OK-OTHER-HOST'
    else:
        verdict = 'BROKEN'
    return {'id': pid, 'merchant': merchant, 'affiliate_url': url,
            'http': code, 'final_url': final[:200], 'verdict': verdict, 'detail': ''}

def main():
    data = json.load(open(f'{BASE}/data/products.json'))
    prods = data['products']
    items = [(p['id'], p['affiliate_url'], p.get('merchant', '')) for p in prods]
    print(f'AUDITING {len(items)} affiliate links...', flush=True)
    results = []
    with ThreadPoolExecutor(max_workers=12) as ex:
        futs = {ex.submit(check, it): it for it in items}
        done = 0
        for f in as_completed(futs):
            results.append(f.result()); done += 1
            if done % 100 == 0: print(f'  {done}/{len(items)}', flush=True)
    # go/ page consistency
    go_missing, go_mismatch = [], []
    for p in prods:
        gp = f"{BASE}/go/{p['id']}.html"
        if not os.path.exists(gp):
            go_missing.append(p['id']); continue
        txt = open(gp, encoding='utf-8', errors='ignore').read()
        if p['affiliate_url'] not in txt: go_mismatch.append(p['id'])
    out = {'checked_at': '2026-10-02', 'total': len(results),
           'go_missing': go_missing, 'go_mismatch': go_mismatch, 'results': results}
    json.dump(out, open(f'{BASE}/hidden_files/link-audit-2026-10-02.json', 'w'), indent=1)
    from collections import Counter
    c = Counter(r['verdict'] for r in results)
    print('VERDICTS:', dict(c))
    print(f'GO PAGES: missing={len(go_missing)} mismatch={len(go_mismatch)}')
    for r in results:
        if r['verdict'] in ('BROKEN', 'ERROR'):
            print(r['verdict'], r['merchant'], r['id'], r['http'], r['detail'][:80], r['final_url'][:120])

if __name__ == '__main__':
    main()
