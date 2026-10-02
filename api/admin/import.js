import { requireAdmin, getBody, getCatalog, saveCatalog, validateProduct, findDuplicate } from './_lib.js';

// Minimal CSV parser: header row plus quoted fields (supports quoted commas
// and escaped double quotes).
export function parseCSV(text) {
  const rows = [];
  let row = [];
  let field = '';
  let inQuotes = false;
  for (let i = 0; i < text.length; i++) {
    const c = text[i];
    if (inQuotes) {
      if (c === '"') {
        if (text[i + 1] === '"') { field += '"'; i++; }
        else inQuotes = false;
      } else {
        field += c;
      }
    } else if (c === '"') {
      inQuotes = true;
    } else if (c === ',') {
      row.push(field); field = '';
    } else if (c === '\n') {
      row.push(field); rows.push(row); row = []; field = '';
    } else if (c === '\r') {
      // skip CR
    } else {
      field += c;
    }
  }
  row.push(field);
  rows.push(row);
  return rows.filter((r) => r.some((f) => String(f).trim() !== ''));
}

const HEADER_ALIASES = {
  url: 'affiliate_url', link: 'affiliate_url', affiliate: 'affiliate_url', affiliatelink: 'affiliate_url',
  affiliateurl: 'affiliate_url', // normalized form of affiliate_url
  image: 'image_url', imageurl: 'image_url', picture: 'image_url',
  title: 'name', productname: 'name',
  desc: 'short_description', description: 'short_description', shortdescription: 'short_description',
  sub: 'subcategory', features: 'key_features', keyfeatures: 'key_features',
  sold: 'sold_count', soldcount: 'sold_count', trend: 'trend_status', trendstatus: 'trend_status',
};

function splitList(v) {
  return String(v || '')
    .split('|')
    .map((s) => s.trim())
    .filter(Boolean);
}

export function csvRowsToObjects(text) {
  const rows = parseCSV(text);
  if (rows.length < 2) return [];
  const headers = rows[0].map((h) => {
    const k = String(h).trim().toLowerCase().replace(/[\s_-]+/g, '');
    return HEADER_ALIASES[k] || k;
  });
  return rows.slice(1).map((row) => {
    const obj = {};
    headers.forEach((h, i) => {
      const raw = row[i] == null ? '' : String(row[i]).trim();
      if (!raw) return;
      if (['pros', 'cons', 'key_features', 'badges'].includes(h)) obj[h] = splitList(raw);
      else if (h === 'rating') obj[h] = Number(raw);
      else if (h === 'sample') obj[h] = /^(true|1|yes)$/i.test(raw);
      else obj[h] = raw;
    });
    return obj;
  });
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
    const format = String(body.format || 'json').toLowerCase();

    let rawItems;
    if (format === 'json') {
      if (!Array.isArray(body.items)) {
        res.status(400).json({ ok: false, error: 'For format "json", body.items must be an array of product objects.' });
        return;
      }
      rawItems = body.items;
    } else if (format === 'csv') {
      if (typeof body.text !== 'string' || !body.text.trim()) {
        res.status(400).json({ ok: false, error: 'For format "csv", body.text must be the CSV text with a header row.' });
        return;
      }
      rawItems = csvRowsToObjects(body.text);
    } else {
      res.status(400).json({ ok: false, error: 'format must be "json" or "csv".' });
      return;
    }

    const { doc, sha } = await getCatalog();
    const seenIds = new Set(doc.products.map((p) => p.id));
    const catalogAndNew = doc.products.slice();

    const added = [];
    const skipped = [];

    for (const raw of rawItems) {
      const { valid, errors, product } = validateProduct(raw);
      const label = String((raw && (raw.name || raw.id)) || 'unnamed');
      if (!valid) {
        skipped.push({ name: label, reason: `invalid: ${errors.join('; ')}` });
        continue;
      }
      if (seenIds.has(product.id)) {
        skipped.push({ name: label, reason: `duplicate id "${product.id}"` });
        continue;
      }
      const dup = findDuplicate(product, catalogAndNew);
      if (dup) {
        skipped.push({ name: label, reason: `duplicate of "${dup.id}"` });
        continue;
      }
      seenIds.add(product.id);
      catalogAndNew.push(product);
      added.push(product);
    }

    if (added.length > 0) {
      for (const p of added) doc.products.push(p);
      await saveCatalog(doc, sha);
    }

    res.status(200).json({ ok: true, added: added.length, skipped });
  } catch (e) {
    res.status(500).json({ ok: false, error: e.message || 'Unexpected error.' });
  }
}
