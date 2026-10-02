import { requireAdmin, getBody } from './_lib.js';

// Merchant domain patterns for the final landing host.
const MERCHANT_HOSTS = {
  temu: /temu\.(to|com)$/i,
  aliexpress: /(aliexpress\.(com|us)|s\.click\.aliexpress\.com)$/i,
  amazon: /amazon\.(com|co\.uk|de)$/i,
};

const VALID_MERCHANTS = Object.keys(MERCHANT_HOSTS);
const MAX_HOPS = 10;
const TIMEOUT_MS = 20000;
const MAX_BODY_BYTES = 64 * 1024;

function hostOf(url) {
  try { return new URL(url).hostname.toLowerCase(); }
  catch (e) { return ''; }
}

function inferMerchant(url) {
  const host = hostOf(url);
  for (const m of VALID_MERCHANTS) {
    if (MERCHANT_HOSTS[m].test(host)) return m;
  }
  return null;
}

// Read at most MAX_BODY_BYTES from the response, then discard the rest.
async function drainBody(res) {
  try {
    if (!res.body) return;
    const reader = res.body.getReader();
    let total = 0;
    for (;;) {
      const { done, value } = await reader.read();
      if (done) break;
      total += value ? value.byteLength : 0;
      if (total >= MAX_BODY_BYTES) break;
    }
    try { await reader.cancel(); } catch (e) { /* ignore */ }
  } catch (e) { /* ignore */ }
}

export default async function handler(req, res) {
  const user = requireAdmin(req, res);
  if (!user) return;

  if (req.method !== 'POST') {
    res.status(405).json({ ok: false, error: 'Method not allowed.' });
    return;
  }

  try {
    const body = getBody(req);
    const url = String(body.url || '').trim();
    if (!url) {
      res.status(400).json({ ok: false, error: 'url is required.' });
      return;
    }
    let parsed;
    try { parsed = new URL(url); } catch (e) {
      res.status(400).json({ ok: false, error: 'url is not a valid URL.' });
      return;
    }
    if (parsed.protocol !== 'http:' && parsed.protocol !== 'https:') {
      res.status(400).json({ ok: false, error: 'url must be an http(s) URL.' });
      return;
    }
    if (body.merchant != null && !VALID_MERCHANTS.includes(String(body.merchant).toLowerCase())) {
      res.status(400).json({ ok: false, error: `merchant must be one of: ${VALID_MERCHANTS.join(', ')}.` });
      return;
    }

    const expectedMerchant = body.merchant
      ? String(body.merchant).toLowerCase()
      : inferMerchant(url);
    const expectedRe = expectedMerchant ? MERCHANT_HOSTS[expectedMerchant] : null;

    const chain = [];
    let current = url;
    let finalUrl = url;
    let finalStatus = null;
    let fetchError = null;

    const ctrl = new AbortController();
    const timer = setTimeout(() => ctrl.abort(), TIMEOUT_MS);
    try {
      let hops = 0;
      for (;;) {
        let resp;
        try {
          resp = await fetch(current, {
            method: 'GET',
            redirect: 'manual',
            signal: ctrl.signal,
            headers: { 'User-Agent': 'Mozilla/5.0 (QA Affiliate admin link checker)' },
          });
        } catch (e) {
          fetchError = e.name === 'AbortError' ? 'request timed out after 20s' : String(e.message || e);
          break;
        }
        finalStatus = resp.status;
        finalUrl = current;
        chain.push({ status: resp.status, url: current });
        await drainBody(resp);

        const loc = resp.headers.get('location');
        if (resp.status >= 300 && resp.status < 400 && loc && hops < MAX_HOPS) {
          try {
            current = new URL(loc, current).toString();
          } catch (e) {
            break;
          }
          hops++;
          continue;
        }
        break;
      }
    } finally {
      clearTimeout(timer);
    }

    const merchantMatch = expectedRe ? expectedRe.test(hostOf(finalUrl)) : false;
    const anyMerchantHop = expectedRe ? chain.some((h) => expectedRe.test(hostOf(h.url))) : false;

    let verdict;
    if (fetchError && finalStatus == null) {
      // Network-level failure before any response arrived.
      verdict = anyMerchantHop ? 'attention' : 'broken';
    } else if (!merchantMatch) {
      verdict = 'broken';
    } else if (finalStatus >= 400) {
      verdict = 'broken';
    } else if (finalStatus >= 200 && finalStatus < 400) {
      verdict = 'ok';
    } else {
      verdict = 'attention';
    }

    res.status(200).json({
      ok: true,
      url,
      chain,
      finalUrl,
      finalStatus,
      fetchError,
      expectedMerchant,
      merchantMatch,
      verdict,
    });
  } catch (e) {
    res.status(500).json({ ok: false, error: e.message || 'Unexpected error.' });
  }
}
