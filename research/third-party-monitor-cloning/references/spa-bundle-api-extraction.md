# Lifting a backend out of a client-rendered SPA bundle

Use when a shared URL returns nothing useful to `curl` because the site is a React/Vite SPA —
typical shapes: `/r/<uuid>` (a shared result), `/job/<id>`, `/p/<handle>`. The HTML is a shell plus
one big bundle; the real data comes from a backend you can call yourself.

Worked case: a "Score my CV" share link (`kerjaweb3.com/r/<uuid>`) that turned out to be the user's
own CV scorecard. Bundle → Supabase project + anon key + tables + two edge functions → full payload
retrieved directly, no browser, no login.

## Steps

1. **Get the bundle path.**
   ```bash
   curl -sL -m 30 -A "Mozilla/5.0 (X11; Linux x86_64) Chrome/126 Safari/537.36" "$URL" -o /tmp/p.html
   grep -oE '(src|href)="[^"]*\.(js|css)[^"]*"' /tmp/p.html
   ```
2. **Download the bundle and grep for backend fingerprints** (one Python pass beats many greps):

   | What | Pattern |
   |---|---|
   | DB host | `https://[a-z0-9]{15,}\.supabase\.co` (also look for `api.`, firebase, railway, render) |
   | anon/public key | `eyJ[A-Za-z0-9_-]{20,}\.[A-Za-z0-9_-]{20,}\.[A-Za-z0-9_-]{10,}` |
   | tables | `\.from\("([a-z_-]+)"\)` |
   | edge functions | `functions/v1/([a-z-]+)` |
   | RPC | `/rpc/([a-z_]+)` |
   | **request body shape** | `body:JSON\.stringify\(\{[^}]{0,400}` ← gives you the exact keys the function wants |

   A Supabase **anon key is public by design** (it ships in every browser client), so using it is not
   a credential leak — but never print it: read it into a variable, send it as `apikey` /
   `Authorization: Bearer` header, and if it must appear in output, mask it. RLS still applies to it.

3. **Call the backend directly.**
   ```bash
   curl -s "$PROJ/rest/v1/<table>?select=*&limit=200" -H "apikey: $KEY" -H "Authorization: Bearer $KEY"
   curl -s -X POST "$PROJ/functions/v1/<fn>" -H "Content-Type: application/json" \
        -H "apikey: $KEY" -H "Authorization: Bearer $KEY" -d '{"id":"<uuid>"}'
   ```
   Edge functions that take an `id` usually bypass row-level security and hand back the shared
   record — that is the path when the tables return `[]`.

4. **Use error codes to enumerate.** `PGRST205` "Could not find the table" = wrong name (try the
   plural/near-miss the hint suggests); a 200 with `[]` = table exists but RLS hides it. Guessing a
   short list of table names costs seconds and maps the schema.

## Pitfalls

- **Find the route's component to learn what the link IS.** Search the bundle for
  `path:"/r/:id",element:` — the element name (minified, e.g. `ole`) resolves via
  `\bole\s*=` to its definition, which shows the copy ("RESULT NOT FOUND", "Score my CV") and the
  fetch helper it calls. That is how you tell a referral link from a shared result before spending
  time on it.
- **Terminal output sanitizers redact `Authorization:` template literals**, which can make the
  request body look truncated/unavailable. Extract with a narrow regex instead
  (`body:JSON\.stringify\(\{[^}]{0,400}`) and print only the match — the payload is there.
- Save the retrieved payload to disk (`~/<dir>/<name>.json`) before printing the next variant of the
  request; a failed retry into the same `-o` file overwrites the good response (this cost one round
  trip: the 400 "Missing result id" body replaced the 200 payload).
- The bundle is ~1.5 MB of minified JS. Never print it; grep for a fixed set of patterns and print
  only matches.

## Finish

Report which layer answered (edge function vs REST table) and quote the retrieved payload as the
source of truth. The claim "the link is X" is only worth making once you have the JSON in hand.
