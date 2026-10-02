import { requireAdmin, getBody, getCatalog, saveCatalog, validateProduct } from './_lib.js';

export default async function handler(req, res) {
  const user = requireAdmin(req, res);
  if (!user) return;

  try {
    if (req.method === 'GET') return await handleGet(req, res);
    if (req.method === 'POST') return await handleCreate(req, res);
    if (req.method === 'PUT') return await handleUpdate(req, res);
    if (req.method === 'DELETE') return await handleDelete(req, res);
    res.status(405).json({ ok: false, error: 'Method not allowed.' });
  } catch (e) {
    res.status(500).json({ ok: false, error: e.message || 'Unexpected error.' });
  }
}

// GET list (?q=&category=&merchant=&page=&limit=) or GET one (?id=)
async function handleGet(req, res) {
  const { doc } = await getCatalog();
  const q = (req.query || {}).id;
  if (q) {
    const product = doc.products.find((p) => p.id === String(q));
    if (!product) {
      res.status(404).json({ ok: false, error: `No product found with id "${q}".` });
      return;
    }
    res.status(200).json({ ok: true, product });
    return;
  }

  const query = req.query || {};
  const search = String(query.q || '').trim().toLowerCase();
  const category = String(query.category || '').trim().toLowerCase();
  const merchant = String(query.merchant || '').trim().toLowerCase();

  let list = doc.products;
  if (search) {
    list = list.filter((p) =>
      String(p.id || '').toLowerCase().includes(search) ||
      String(p.name || '').toLowerCase().includes(search) ||
      String(p.short_description || '').toLowerCase().includes(search)
    );
  }
  if (category) list = list.filter((p) => String(p.category || '').toLowerCase() === category);
  if (merchant) list = list.filter((p) => String(p.merchant || '').toLowerCase() === merchant);

  let limit = parseInt(String(query.limit || '50'), 10);
  if (!Number.isFinite(limit) || limit <= 0) limit = 50;
  limit = Math.min(limit, 200);
  let page = parseInt(String(query.page || '1'), 10);
  if (!Number.isFinite(page) || page <= 0) page = 1;

  const total = list.length;
  const start = (page - 1) * limit;
  const products = list.slice(start, start + limit);
  res.status(200).json({ ok: true, total, page, limit, products });
}

// POST: create a product. Body: { product: {...} } or the product itself.
async function handleCreate(req, res) {
  const body = getBody(req);
  const raw = body.product || body;
  const { valid, errors, product } = validateProduct(raw);
  if (!valid) {
    res.status(400).json({ ok: false, error: 'Product validation failed.', errors });
    return;
  }

  const { doc, sha } = await getCatalog();
  if (doc.products.some((p) => p.id === product.id)) {
    res.status(409).json({ ok: false, error: `A product with id "${product.id}" already exists.` });
    return;
  }
  const urlDup = doc.products.find((p) => p.affiliate_url === product.affiliate_url);
  if (urlDup) {
    res.status(409).json({ ok: false, error: `This affiliate URL is already used by product "${urlDup.id}".` });
    return;
  }

  doc.products.push(product);
  await saveCatalog(doc, sha);
  res.status(200).json({ ok: true, product });
}

// PUT: partial update. Query ?id=; body contains fields to merge.
async function handleUpdate(req, res) {
  const id = String((req.query || {}).id || '');
  if (!id) {
    res.status(400).json({ ok: false, error: 'Missing ?id= query parameter.' });
    return;
  }
  const body = getBody(req);
  const patch = body.product || body;

  const { doc, sha } = await getCatalog();
  const idx = doc.products.findIndex((p) => p.id === id);
  if (idx < 0) {
    res.status(404).json({ ok: false, error: `No product found with id "${id}".` });
    return;
  }

  const merged = { ...doc.products[idx], ...patch, id }; // id is immutable
  const { valid, errors, product } = validateProduct(merged);
  if (!valid) {
    res.status(400).json({ ok: false, error: 'Product validation failed.', errors });
    return;
  }

  doc.products[idx] = product;
  await saveCatalog(doc, sha);
  res.status(200).json({ ok: true, product });
}

// DELETE: remove a product. Query ?id=
async function handleDelete(req, res) {
  const id = String((req.query || {}).id || '');
  if (!id) {
    res.status(400).json({ ok: false, error: 'Missing ?id= query parameter.' });
    return;
  }
  const { doc, sha } = await getCatalog();
  const idx = doc.products.findIndex((p) => p.id === id);
  if (idx < 0) {
    res.status(404).json({ ok: false, error: `No product found with id "${id}".` });
    return;
  }
  doc.products.splice(idx, 1);
  await saveCatalog(doc, sha);
  res.status(200).json({ ok: true });
}
