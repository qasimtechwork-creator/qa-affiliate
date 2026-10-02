import { verifySession } from './_auth.js';

// Shared helpers for the QA Affiliate admin API.
// Secrets (ADMIN_USER, ADMIN_PASS, ADMIN_SECRET, GITHUB_TOKEN) are read only
// from process.env and are never logged or included in responses.

const REPO = 'qasimtechwork-creator/qa-affiliate';
const FILE_PATH = 'data/products.json';

export function todayUTC() {
  return new Date().toISOString().slice(0, 10);
}

// Returns the admin username when the session is valid; otherwise sends a
// 401 JSON response and returns null.
export function requireAdmin(req, res) {
  const user = verifySession(req);
  if (!user) {
    res.status(401).json({ ok: false, error: 'Not authorized.' });
    return null;
  }
  return user;
}

// Parse the request body tolerantly: Vercel gives an object for JSON posts,
// a string when the client did not send a JSON content type.
export function getBody(req) {
  let body = req.body;
  if (body == null) return {};
  if (typeof body === 'string') {
    try { return JSON.parse(body || '{}'); } catch (e) { return {}; }
  }
  return body;
}

function ghHeaders() {
  return {
    'Authorization': `Bearer ${process.env.GITHUB_TOKEN}`,
    'Accept': 'application/vnd.github+json',
    'User-Agent': 'qa-affiliate-admin',
  };
}

export function catalogUrl() {
  return `https://api.github.com/repos/${REPO}/contents/${FILE_PATH}`;
}

// Fetch the catalog from GitHub. Returns { doc, sha }.
export async function getCatalog() {
  const token = process.env.GITHUB_TOKEN;
  if (!token) throw new Error('GITHUB_TOKEN is not configured.');
  const res = await fetch(catalogUrl(), { headers: ghHeaders() });
  if (!res.ok) {
    throw new Error(`Failed to read catalog from GitHub (HTTP ${res.status}).`);
  }
  const data = await res.json();
  if (!data.content) throw new Error('GitHub response did not include file content.');
  const doc = JSON.parse(Buffer.from(data.content, 'base64').toString('utf8'));
  if (!doc || !Array.isArray(doc.products)) {
    throw new Error('Catalog is malformed: expected { products: [...] }.');
  }
  return { doc, sha: data.sha };
}

// Write the catalog back to GitHub. On a SHA conflict (stale blob), refetch
// a fresh SHA and retry once, then throw.
export async function saveCatalog(doc, sha) {
  const token = process.env.GITHUB_TOKEN;
  if (!token) throw new Error('GITHUB_TOKEN is not configured.');
  const content = Buffer.from(JSON.stringify(doc, null, 2)).toString('base64');

  const attempt = async (s) => {
    const res = await fetch(catalogUrl(), {
      method: 'PUT',
      headers: { ...ghHeaders(), 'Content-Type': 'application/json' },
      body: JSON.stringify({
        message: `admin: update products (${todayUTC()})`,
        content,
        sha: s,
      }),
    });
    return res;
  };

  let res = await attempt(sha);
  if (!res.ok) {
    let bodyText = '';
    try { bodyText = await res.text(); } catch (e) { /* ignore */ }
    const conflict = res.status === 409 || /sha|conflict/i.test(bodyText);
    if (conflict) {
      const fresh = await getCatalog();
      res = await attempt(fresh.sha);
    }
    if (!res.ok) {
      let retryText = '';
      try { retryText = await res.text(); } catch (e) { /* ignore */ }
      throw new Error(`Failed to save catalog to GitHub (HTTP ${res.status}). ${retryText.slice(0, 200)}`);
    }
  }
  return true;
}

// ---- Product schema ----

const PRODUCT_KEYS = [
  'id', 'name', 'affiliate_url', 'image_url', 'merchant', 'category',
  'subcategory', 'short_description', 'pros', 'cons', 'key_features',
  'badges', 'rating', 'sold_count', 'source', 'trend_status', 'updated', 'sample',
];

function isHttpUrl(v) {
  if (typeof v !== 'string' || !v) return false;
  try {
    const u = new URL(v);
    return u.protocol === 'http:' || u.protocol === 'https:';
  } catch (e) {
    return false;
  }
}

// Normalize a raw product object to the exact catalog key set with defaults.
export function normalizeProduct(p) {
  const src = p && typeof p === 'object' ? p : {};
  const str = (v) => (v == null ? '' : String(v));
  const arr = (v) => (Array.isArray(v) ? v.map(String) : []);
  const rawRating = src.rating == null || src.rating === '' ? null : Number(src.rating);
  const updated = str(src.updated).trim();
  return {
    id: str(src.id).trim(),
    name: str(src.name).trim(),
    affiliate_url: str(src.affiliate_url).trim(),
    image_url: str(src.image_url).trim(),
    merchant: str(src.merchant).trim().toLowerCase(),
    category: str(src.category).trim(),
    subcategory: str(src.subcategory).trim(),
    short_description: str(src.short_description).trim(),
    pros: arr(src.pros),
    cons: arr(src.cons),
    key_features: arr(src.key_features),
    badges: arr(src.badges),
    rating: Number.isFinite(rawRating) ? rawRating : null,
    sold_count: str(src.sold_count).trim(),
    source: str(src.source).trim() || 'Admin panel',
    trend_status: str(src.trend_status).trim(),
    updated: /^\d{4}-\d{2}-\d{2}$/.test(updated) ? updated : todayUTC(),
    sample: src.sample === true || src.sample === 'true' || src.sample === 1 || src.sample === '1',
  };
}

// Validate a product record (raw or normalized). Returns
// { valid, errors[], product } where product is the normalized record.
export function validateProduct(p) {
  const errors = [];
  const record = normalizeProduct(p);
  if (!/^[a-z0-9-]+$/.test(record.id)) {
    errors.push('id must be a lowercase slug using only a-z, 0-9 and hyphens.');
  }
  if (!record.name) errors.push('name is required.');
  if (!isHttpUrl(record.affiliate_url)) errors.push('affiliate_url must be a valid http(s) URL.');
  if (!isHttpUrl(record.image_url)) errors.push('image_url must be a valid http(s) URL.');
  if (!['temu', 'aliexpress', 'amazon'].includes(record.merchant)) {
    errors.push("merchant must be one of: temu, aliexpress, amazon.");
  }
  if (!record.category) errors.push('category is required.');
  return { valid: errors.length === 0, errors, product: record };
}

// ---- Duplicate detection helpers ----

const STOPWORDS = new Set([
  'the', 'a', 'an', 'for', 'with', 'and', 'or', 'of', 'to', 'in', 'on',
  'new', 'free', 'best', 'top', 'women', 'womens', 'mens', 'kids', 'set',
  'kit', 'pack', 'lot', 'sale', 'hot', 'mini', 'plus', 'pro', 'max',
  'pcs', 'pc', '1pc', '2pcs', '3pcs', '4pcs', '5pcs', '10pcs',
]);

// Lowercase the name, strip punctuation, drop stopwords, keep tokens of
// length >= 4.
export function distinctiveWords(name) {
  return String(name || '')
    .toLowerCase()
    .replace(/[^a-z0-9\s]/g, ' ')
    .split(/\s+/)
    .filter((t) => t.length >= 4 && !STOPWORDS.has(t));
}

// True when the two names share 3 or more consecutive distinctive tokens.
export function nameOverlap(a, b) {
  const A = distinctiveWords(a);
  const B = distinctiveWords(b);
  if (A.length < 3 || B.length < 3) return false;
  for (let i = 0; i + 2 < A.length; i++) {
    for (let j = 0; j + 2 < B.length; j++) {
      if (A[i] === B[j] && A[i + 1] === B[j + 1] && A[i + 2] === B[j + 2]) return true;
    }
  }
  return false;
}

// Find an existing catalog product that duplicates the candidate: exact
// affiliate_url match, or name-overlap match. Returns the existing product
// (or null).
export function findDuplicate(candidate, products) {
  for (const p of products) {
    if (p.affiliate_url && candidate.affiliate_url && p.affiliate_url === candidate.affiliate_url) {
      return p;
    }
  }
  for (const p of products) {
    if (nameOverlap(candidate.name, p.name)) return p;
  }
  return null;
}
