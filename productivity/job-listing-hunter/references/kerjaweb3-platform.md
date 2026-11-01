# Kerja Web3 (kerjaweb3.com) — platform internals

Indonesian Web3/remote job board (SPA, React + Supabase). Verified 7 Okt 2026 while resolving a
user-supplied `https://www.kerjaweb3.com/r/<uuid>` link.

## Shape of the app

- Static React SPA. Plain fetch returns a ~8 KB HTML shell + `/assets/index-<hash>.js` (≈1.5 MB).
- Routes seen in the bundle: `/`, `/learn/:slug`, `/jobs`, `/jobs/:slug`, `/admin`, `/admin/jobs`,
  `/admin/articles`, `/r/:id`, `/:slug` (catch-all article/404).
- Backend: Supabase project `https://<ref>.supabase.co` — the **anon key is embedded in the JS
  bundle** (as it must be for a browser app). Grep the bundle for `eyJ...` to get it at runtime.
  Treat it as a credential: use it, never echo/print/store it.

## REST (PostgREST) — readable with the anon key

Tables: `jobs`, `candidates`, `cvs`, `articles`, `article-covers`. `jobs` is readable directly:

```
GET  <proj>/rest/v1/jobs?select=*&status=eq.open&order=posted_at.desc
Hdr  apikey: <anon>     Authorization: Bearer <anon>
```

`jobs` columns: `id, title, role_category, responsibilities, employment_type, work_arrangement,
status, salary_range, apply_url, posted_at, updated_at, created_by`.

- `responsibilities` holds the whole posting (responsibilities + requirements + location) as one
  text blob — parse it, don't expect separate columns.
- `apply_url` is frequently `null`: the board then routes applications through its **built-in apply
  portal**, which requires a logged-in account. Tell the user to register before they can apply.
- Unknown table/column → `PGRST205` (schema-cache error); `[]` with HTTP 200 means RLS returned no
  rows (not an error). `candidates` was RLS-blocked, `jobs` was not.

## Edge functions

- `POST <proj>/functions/v1/analyze-cv` — the "Score my CV" flow. The app uploads the file to
  storage bucket `cvs` first, then calls this with the file/consent/job context.
- `POST <proj>/functions/v1/get-result` with body `{"id":"<shareId>"}` — resolves a public
  scorecard. Body must be exactly `id`; `{"shareId":...}` returns `{"error":"Missing result id."}`.

`get-result` response shape (that is what `/r/<uuid>` renders):

```json
{"id":"...","overall_score":42,
 "scores":{"relevance":45,"clarity":50,"experience_depth":40,"technical_skills":40,"market_readiness":35},
 "score_labels":{"clarity":"...","relevance":"..."},
 "strengths":["..."],"improvements":["..."],
 "summary":"...",
 "ats":{"ats_score":60,
        "keyword_match":{"matched":["Akuntansi","MYOB"],"missing":["Web3","DeFi"]},
        "missing_sections":[],"length_assessment":"...","parseability_flags":[],
        "contact_completeness":{"email":true,"links":false,"phone":true}},
 "role":"Finance / Accounting","created_at":"..."}
```

### How to use it
The scorecard grades **format, length and keywords — not capability**. Always: (a) re-verify by
reading the source CV yourself, (b) restate the sub-scores, (c) name what the tool could not see,
(d) never let its "quantify your achievements" line push you into inventing numbers.
`contact_completeness.links:false` is a free, honest point to fix (add LinkedIn/portfolio).
Full rewriting workflow: skill `cv-tailoring-and-ats`.

## Other endpoints seen

- Public socials/footer: `x.com/kerjaweb3`, Instagram, Threads, Discord `discord.gg/2vX7GRdpwE`.
- Jobs are curated/admin-inserted, so the live table can be **very small** (5 open rows on
  7 Okt 2026). Do not present it as the whole market.
