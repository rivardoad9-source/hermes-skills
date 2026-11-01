# CV scorecards: reading the raw payload

Many "Score my CV / ATS check" tools are SPAs that store the result server-side and expose it at a
share URL like `/<x>/<uuid>`. That page renders a JSON record — fetch the record, don't describe the
page. The jobs side of a board (listing REST, apply path) is documented in
skill `job-listing-hunter` → `references/kerjaweb3-platform.md`.

## Worked example — Kerja Web3

- Share page: `https://www.kerjaweb3.com/r/<uuid>` → route `/r/:id`, resolves via the edge function
  `POST <proj>/functions/v1/get-result` with body `{"id":"<uuid>"}`.
- Body key must be exactly `id`; `{"shareId":...}` / `{"share_id":...}` → `{"error":"Missing result id."}`.
- Endpoint discovery: `web_extract` on the share URL returns the empty SPA shell; grep the bundled
  `/assets/index-*.js` for `functions/v1`, `.from("<table>")` and the embedded Supabase anon key
  (extract at runtime — never print or store it).
- `created_at` in the payload is UTC; convert before comparing with what the user says
  ("upload 12:25 WIB" = `05:25Z`) — it is how you can tell the link is the user's *own* result.

## Payload shape

```json
{"overall_score": 42,
 "scores": {"relevance":45,"clarity":50,"experience_depth":40,"technical_skills":40,"market_readiness":35},
 "score_labels": {"clarity":"...","relevance":"..."},
 "strengths": ["..."],
 "improvements": ["Detail specific projects...","Quantify achievements...","Include LinkedIn"],
 "summary": "...",
 "ats": {"ats_score":60,
         "keyword_match": {"matched":["Akuntansi","MYOB"],"missing":["Web3","DeFi"]},
         "missing_sections": [], "length_assessment": "...", "parseability_flags": [],
         "contact_completeness": {"email":true,"links":false,"phone":true}},
 "role": "Finance / Accounting", "created_at": "2026-10-07T05:25:00Z"}
```

## How to use it in the reply

1. Restate the sub-scores so the user sees the two real axes: **content score** (relevance, clarity,
   experience_depth, technical_skills, market_readiness) and **ATS/parse score** (keyword match,
   sections, length, contacts).
2. Name the tool's blind spot explicitly: it grades format, length and keywords — it cannot see what
   the person actually operates. Low `technical_skills` usually means "not evidenced", not "not held".
3. Cross-check every claim against the CV text you extracted yourself; the label text is generated
   and can be generic.
4. Do **not** let `improvements` drive fabrication. "Quantify achievements" becomes "mark the spots
   where the user must supply real numbers", not invented percentages.
5. `contact_completeness.links:false` and `missing_sections` are the cheapest honest wins — call them
   out as must-fix before the next submission.
