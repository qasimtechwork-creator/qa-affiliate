import { requireAdmin, getCatalog, todayUTC } from './_lib.js';

export default async function handler(req, res) {
  const user = requireAdmin(req, res);
  if (!user) return;

  if (req.method !== 'GET') {
    res.status(405).json({ ok: false, error: 'Method not allowed.' });
    return;
  }

  try {
    const { doc } = await getCatalog();
    const filename = `products-backup-${todayUTC()}.json`;
    res.setHeader('Content-Type', 'application/json; charset=utf-8');
    res.setHeader('Content-Disposition', `attachment; filename="${filename}"`);
    res.status(200).send(JSON.stringify(doc, null, 2));
  } catch (e) {
    res.status(500).json({ ok: false, error: e.message || 'Unexpected error.' });
  }
}
