# QA Affiliate Admin Panel — Deploy Notes (2026-10-02)

Built 2026-10-02: `/admin/` static UI + `/api/admin/*` serverless functions (Node ESM).
No secrets are stored anywhere in code or git. All sensitive values are read only from environment variables.

## Required env vars (set on the Vercel project serving qa-affiliate.vercel.app)

| Var | Purpose |
|---|---|
| `ADMIN_USER` | Admin username for /admin/ login |
| `ADMIN_PASS` | Admin password for /admin/ login |
| `ADMIN_SECRET` | Long random string for HMAC-SHA256 session signing (generate fresh, e.g. 64 random bytes hex) |
| `GITHUB_TOKEN` | GitHub personal access token with **repo** scope on `qasimtechwork-creator/qa-affiliate`. Used by /api/admin/products and /api/admin/import to write `data/products.json` via the GitHub Contents API. No other permission needed. |

Set these in Vercel: Project → Settings → Environment Variables (apply to Production).
After setting env vars, REDEPLOY (Vercel picks up env changes on a new deployment, not automatically).

## Admin login flow
- Open https://qa-affiliate.vercel.app/admin/ → login form.
- On success a `qa_aff_admin` cookie is set (HttpOnly, Secure, SameSite=Lax, 7-day expiry, HMAC-SHA256 signed).
- Session endpoints: `/api/admin/me` (check), `/api/admin/logout` (clear).

## Security checks (main agent verified live 2026-10-02)
- `/admin/` loads (HTML, noindex/nofollow meta; robots.txt Disallows /admin/).
- `POST /api/admin/login` with no creds → 401; wrong creds → 401.
- `GET /api/admin/stats`, `/api/admin/products`, `/api/admin/backup`, `POST /api/admin/import`, `POST /api/admin/test-url` → 401 without a valid session cookie.
- Do NOT test with the real admin credentials — main agent will set the env vars and do the authenticated test separately.

## Operational notes
- Product writes go through the GitHub Contents API with fresh-SHA-per-write and one retry on 409. The daily sourcing scripts write via git locally — if a sourcing commit lands between the admin's SHA read and PUT, the retry handles it; worst case the admin gets a clear error and can retry.
- Product writes preserve the exact 18-key products.json schema (id, name, affiliate_url, image_url, merchant, category, subcategory, short_description, pros, cons, key_features, badges, rating, sold_count, source, trend_status, updated, sample).
- Bulk import dedupe: exact affiliate_url match OR 3+ consecutive distinctive words in the name = duplicate → skipped with reason in the import report.
- `/api/admin/test-url` fetches server-side (max 10 redirects, 20s timeout, 64KB body cap); never logs or returns any token.
- The Pinterest pipeline card in the dashboard is read-only info only — pin posting stays with the assistant's existing pipeline, not this admin.
