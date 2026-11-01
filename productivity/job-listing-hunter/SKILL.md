---
name: job-listing-hunter
description: "Use when hunting or monitoring job/internship listings."
triggers:
  - cari lowongan magang
  - lowongan kerja akuntansi
  - cari kerja
  - magang akuntansi
version: 1.0.0
author: Hermes
license: MIT
metadata:
  hermes:
    tags: [career, jobs, internship, scraping, cron, alerts]
    related_skills: [hermes-cron-automation, cron-output-style]
---

# Job & Internship Listing Hunter

Use when the user wants openings **found, filtered to their profile, verified as still open, and
alerted on** — one-off ("cari magang yang buka sekarang") or as a recurring silent lane
("kabarin kalau ada lowongan baru"). Proven 6 Okt 2026: lane `magang-hunter` for an Indonesian
accounting student, 71 live listings, cron daily, 0 AI tokens.

Not for: a single "is this one posting real?" lookup (just fetch the URL) or salary/culture
research on a company (that's web_search territory).

## Pipeline

`fetch → filter to profile → dedupe → verify still open → freshness → notify only NEW, else silent`

Scripts of the reference implementation (see `references/indonesia-job-sources.md` for exact
endpoints, query lists and regexes):

| File | Role |
|---|---|
| `~/.hermes/scripts/career_scan.py` | fetch + filter + tier + dedup state; `--notify` mode |
| `~/.hermes/scripts/career_verify.py` | open/closed check per candidate (imported by the scanner) |
| `~/.hermes/scripts/career_lane.sh` | cron wrapper: `python3 career_scan.py --notify 2>>career_scan.err` |
| `~/.hermes/scripts/startup_remote_scan.py` | **lane WFH/startup** (7 board, geo-tiering); imports `career_verify` |

`startup_remote_scan.py` covers the "cari kerja startup / WFH" request. It pulls 7 boards, drops
off-lane roles (ngoding, desain, posisi senior), drops postings that require another language
(Danish/German/Mandarin…), classifies **where the candidate is allowed to live** (🇮🇩 Indonesia /
🌍 worldwide / 🌏 Asia lain / ⚠️ region-locked), verifies tier A still open, and writes
`~/.hermes/data/startup_remote_<date>.md`. Proven 7 Okt 2026: 444 pulled → 168 kept → **21 tier-A
verified open** for a Jakarta student.

## 1. Prefer sources that answer without a browser (0 token)

Guest/JSON endpoints beat headless browsing: they're fast, deterministic, and a `no_agent` cron
can run them forever at zero cost. Proven for job boards:

- **LinkedIn guest jobs API** — `…/jobs-guest/jobs/api/seeMoreJobPostings/search?keywords=<q>&location=<loc>&start=<n>`
  returns HTML card fragments; detail via `…/jobs/view/<slug>-<id>` or `…/jobs-guest/jobs/api/jobPosting/<id>`.
- **Kalibrr** — `https://www.kalibrr.com/kjs/job_board/search?limit=30&offset=<n>&text=<q>` (JSON).
- **Workable / Greenhouse** — apply URLs are directly fetchable (`https://apply.workable.com/j/<CODE>`).

Send a browser `User-Agent`; build URLs with `urllib.parse.quote` (raw spaces/`&` break the query).

## 2. Filter to the person, not to "jobs"

- Role keywords: intern/magang/trainee/apprentice (+ the target function: accounting, audit, tax,
  finance…). Use `intern(?!al)\w*` — a plain `intern` matches **"internal audit"** and pollutes the list.
- Location: regex for the user's country/city; keep remote rows only if they're real.
- Drop senior/manager titles unless the title also carries intern/magang/trainee.
- **Tier** what survives: A = target function at a strong institution (bank, Big-4, fintech,
  listed company), B = adjacent function or decent brand, C = the rest. Tiering is what makes the
  report usable — a flat list of 70 links is not.

## 3. Dedupe before publishing (pitfall)

The same opening arrives from several boards with different company spellings
("Amartha Financial" on LinkedIn vs "Amartha" on Workable). Key = **normalized title + first
alphanumeric token of company name**. When two rows collide, keep the row whose link goes
**directly to the ATS** (workable/kalibrr/company site) over the LinkedIn aggregator URL —
the direct link survives longer and skips a login wall. Without this step the report shows
near-duplicate rows at the top, which reads as sloppy.

## 4. Verify it is still OPEN before alerting

Fetch every candidate: HTTP 200 **and** no "no longer accepting applications / closed" markers ⇒
open. Cap the pool at `ThreadPoolExecutor(3)` with 4 retries — higher concurrency gets you
rate-limited and produces false "closed" verdicts. Never alert on an unverified row, and count
"kept N of M" so the report states how many were dropped and why.

**A plain (non-`--notify`) run writes only the unverified snapshot.** `career_scan.py` verifies
inside the notify branch, so `career_verified.json` keeps the date of the last *alerting* run and can
be days stale while `career_open.json` is fresh. Before building a shortlist by hand, verify the
fresh snapshot yourself instead of reading statuses out of the old file:

```python
sys.path.insert(0, "$HOME/.hermes/scripts")
from career_verify import check
from concurrent.futures import ThreadPoolExecutor
with ThreadPoolExecutor(3) as ex:
    res = list(ex.map(check, filtered_rows))   # filtered_rows from career_open.json['jobs']
```

Write the result to its own dated file (e.g. `career_verified_<date>.json`) — overwriting the lane's
files breaks the union/dedup state.

## 5. Freshness + union snapshots (two pitfalls that bit this lane)

- **Old ≠ dead.** Rolling "talent pool" postings sit open for months. Keep them and tag
  `⚠️ posting lama, cek dulu`; dropping them silently loses the best institutional pipelines.
- **The scan is not reproducible.** Guest search returns a slightly different set run to run —
  a job present in scan N can be absent in scan N+1. **Union the new snapshot with the previous
  one before overwriting the data file**, or verified items vanish from the next report (this
  happened: an item was confirmed live by hand, then disappeared because a later scan rewrote
  the file). Never let ad-hoc scripts clobber the verified/state files without merging first.
- Dedup state lives in one JSON of sent-keys, e.g. `career_state.json['sent']`, keyed
  `li:<id>` / `kalibrr|<title>|<company>` / `workable/<slug>|<title>|<company>`.

## 6. Silent lane wiring

- `cronjob(no_agent=true, script="career_lane.sh", schedule="10 8 * * *", deliver="origin")`
  with `export TZ=Asia/Jakarta` inside the wrapper.
- stdout = the user message; **empty stdout = silent tick** (the 99% case). Push diagnostics to
  stderr (`2>>career_scan.err`) so they never leak into the chat.
- The **first** run against a fresh state file prints the whole backlog. That is expected — do not
  "tune" filters or freshness rules to force silence; test with a *copy* of the state
  (env-overridable state path or a /tmp copy) instead of mutating the real one.
- Format through `~/.hermes/scripts/msgstyle.py` (`--kind report --no-regime --emoji 🎓 --title …`)
  per the `cron-output-style` skill; a lane that invents its own format reads wrong next to the
  user's other alerts.

## 7. Report artifact

Markdown file under `~/.hermes/data/<lane>_<date>.md`, sections per tier, plus:

- **"Kerjakan N teratas hari ini"** — generate this line *from the data* (filter A-tier rows
  matching the target function + city) so the names it prints are always rows that exist in the
  file. Hand-written recommendation lines go stale the moment the snapshot changes.
- Berkas standar: CV 1 halaman, transkrip, KTM, surat pengantar kampus (minta ke prodi, 1–3 hari).
- Reality check for the person: banks/fintech usually want WFO 3–6 months — check the class
  schedule before applying.
- Deliver with `MEDIA:/absolute/path` so the file lands in the chat.

## 7b. Lane for this user

**Establish orientation before shaping the plan, not after.** Ask whether the person wants
client-facing/solo work (consulting, freelance, building their own pipeline) or **employment inside
an existing system** (a defined scope, a senior above them, someone else owning the targets). Getting
this wrong costs the whole session: client-facing artifacts — "case study to sell the implementation",
"find 1-2 businesses to buy this" — read as worthless to someone who never wanted to sell anything.
When the orientation is employment, the same case study is still produced, but as evidence a hiring
manager reads, and the shortlist itself leads the conversation.

This user has said plainly he is **not suited to working alone or instructing others — he prefers working
under an existing system**. So filter *towards*: junior/entry roles with a defined scope and a senior
above him (staff accounting, AR/AP, finance operations, bookkeeping, fintech product/customer
support L1, data/ops entry, implementation support inside a vendor). Filter *away from*:
founder-adjacent, freelance/agency, pure commission sales, and "build your own pipeline" rows — BD
roles especially, even though he has Prudential canvassing on his CV. Drop the "jadi konsultan /
jual jasa" framing entirely. Keep the two delivery tracks visible: internship (his programme places
magang in semester 6/7) and part-time/remote junior work he can run alongside classes.

## 8. State coverage limits out loud

Aggregator scans are not the whole market. Company career portals (Indonesian banks:
Mandiri/BNI/BRI/BCA career pages) and government batch programs (MSIB/Kemdikdit) are **not**
covered; MSIB only appears once a batch window opens. Say which portals are missing and what the
lane will and won't catch — an exhaustive-sounding list that misses the biggest employers is worse
than a list with a stated blind spot.

## Pitfalls

- **Never label geo from a global board's `location` field.** On RemoteOK/Arbeitnow that field is
  the company's city or a leftover, not where you may live (a "Hamburg · remote" row is often
  remote *within Germany*; the truth sits in the description: `within Germany`, `US only`,
  `worldwide`). Only Kalibrr (`google_location`), Remotive (`candidate_required_location`),
  Himalayas (`locationRestrictions`), Jobicy (`jobGeo`) and the LinkedIn card location are
  authoritative. Unparseable ⇒ label `❓ cek deskripsi` and demote to tier B — a false 🌍
  sends the user to a job they're auto-rejected from. Asia ≠ Indonesia: India/PH/VN rows are
  local-payroll and belong in their own tier, not under 🇮🇩. The `💰~$70k` badge such rows carry is
  the **board's own estimate**, not the employer's band, and those detail pages are JS-rendered so
  `curl` returns only the headline — tag the row `⚠️` and keep it out of the recommended-N line
  instead of presenting it as a verified find.
- Drop postings whose title demands another language (Danish/German/Mandarin/Somali…) — 0 value
  for the user, and they crowd out the real matches.
- `intern` without `(?!al)` → "Internal Audit" rows counted as internships.
- Publishing before dedupe/verify → duplicate rows and dead links in the user's face.
- Rewriting the snapshot file instead of unioning → verified items silently disappear.
- Raising verify concurrency → rate limits misread as "job closed".
- First-run backlog mistaken for a bug → filters get tightened until the lane misses real jobs.
- Claiming the list is complete when bank career portals aren't scraped.
