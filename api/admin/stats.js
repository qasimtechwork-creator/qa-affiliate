import { requireAdmin, getCatalog } from './_lib.js';

export default async function handler(req, res) {
  const user = requireAdmin(req, res);
  if (!user) return;

  if (req.method !== 'GET') {
    res.status(405).json({ ok: false, error: 'Method not allowed.' });
    return;
  }

  try {
    const { doc } = await getCatalog();
    const byCategory = {};
    const byMerchant = {};
    for (const p of doc.products) {
      const c = String(p.category || 'uncategorized');
      const m = String(p.merchant || 'unknown');
      byCategory[c] = (byCategory[c] || 0) + 1;
      byMerchant[m] = (byMerchant[m] || 0) + 1;
    }
    const newest = doc.products
      .slice()
      .sort((a, b) => String(b.updated || '').localeCompare(String(a.updated || '')))
      .slice(0, 10);
    res.status(200).json({ ok: true, total: doc.products.length, byCategory, byMerchant, newest });
  } catch (e) {
    res.status(500).json({ ok: false, error: e.message || 'Unexpected error.' });
  }
}
