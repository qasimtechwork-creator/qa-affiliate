import { verifySession } from './_auth.js';

export default async function handler(req, res) {
  if (req.method !== 'GET') {
    res.status(405).json({ ok: false, error: 'Method not allowed.' });
    return;
  }
  const user = verifySession(req);
  if (!user) {
    res.status(401).json({ ok: false, error: 'Not authorized.' });
    return;
  }
  res.status(200).json({ ok: true, user });
}
