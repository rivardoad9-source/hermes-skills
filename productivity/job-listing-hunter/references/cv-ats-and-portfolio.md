# CV / ATS optimization + a portfolio link that survives

Two artifacts get an interview: the listing (see parent skill) and the **CV + a public link**. Most
job-board platforms also ship a free CV grader — which means you can MEASURE a rewrite instead of
claiming it improved.

## 1. The grader is usually callable

Platform "Score my CV" flows are a thin UI over an analyzer endpoint; the public share link
(`/<platform>/r/<uuid>`) is just the stored result. Pull the payload (recipe:
`third-party-monitor-cloning/references/spa-bundle-api-extraction.md`) to get the real numbers:

```
overall_score, scores{relevance, clarity, experience_depth, technical_skills, market_readiness},
ats{ats_score, keyword_match{matched, missing}, contact_completeness{email, phone, links}}, improvements[]
```

The analyzer endpoint itself was `functions/v1/analyze-cv` with body `{cvText, role, githubUrl}` —
so a rewritten CV can be **re-scored before the user uploads anything**. Always report a measured
before/after, never "this should score better".

## 2. The overall score is noise; the keyword block is signal

Same CV, three runs: **52 / 48 / 53 overall** — an LLM grades it and wobbles ±5. The ATS block was
stable at 75 in every run, and its "missing" list contradicted the text (it flagged `DeFi`, `audit`,
`budgeting` as missing while all three were literally in the CV).

Rules that follow:
- Report the RANGE, not a single number, and say plainly which part is unstable.
- Optimize the keyword block and the structural checklist; **do not chase the overall number** — you
  will loop forever and the next run will disagree with your last fix.
- Keyword matching is spelling-sensitive (`financial modelling` did not match `financial modeling`) —
  use the US spelling in an international/English CV.

## 3. Fix keywords honestly

Expand each missing keyword into a TRUE phrase, and mark study-level claims so the user can defend
them in interview:

- `Web3 / Blockchain / Cryptocurrency / DeFi` → one labelled skill line built from what they really
  do: "on-chain data analysis, blockchain wallet & transaction tracking, cryptocurrency market
  monitoring, DeFi LP position tracking".
- `Compliance` → the actual compliance-adjacent work ("tax-reporting document filing (compliance SOP)").
- `GAAP & IFRS / auditing / budgeting / ERP` → "…(coursework)" for a student; ERP = the accounting
  systems they already list (Accurate, MYOB).
- **Never invent metrics, employers or revenue.** Ask the user for real numbers; the standing rule is
  no fabricated sales/revenue claims.

Structure changes that moved the score: role line under the name; a **Projects section** (for a
student, self-directed AI/automation work is the differentiator — it converts "interested in AI" into
evidence); expand two-word bullets ("File-ing", "Laporan pajak") into outcome lines; group skills into
labelled lines instead of a comma blob; keep it to **one page**.

## 4. The "links" checkbox

Graders ding `contact_completeness.links = false`. Fix = publish a portfolio page and put its URL in
the CV's contact block (email + handle + URL). Keep the phone number OFF the public page.

**Publishing permissionlessly (verified durable route): telegra.ph.** No account, no email, page
persists, URL is stable across edits:

```python
# 1. account (once) -> access_token
post("https://api.telegra.ph/createAccount", {"short_name": "X", "author_name": "X"})
# 2. page: content is Node JSON: {"tag":"h3"/"p"/"ul"/"b"/"a", "children":[...]}
post("https://api.telegra.ph/createPage", {"access_token": T, "title": ..., "author_name": ...,
                                           "content": json.dumps(nodes)})
# 3. update later IN PLACE with the SAME account token (URL does not change)
post("https://api.telegra.ph/editPage/<path>", {"access_token": T, "title": ..., "content": ...})
```

Host ladder, in order of preference for a link that must live for months:
1. Anything with a stable domain the user already owns.
2. Static host on a repo you can actually WRITE to — **check write access first**: a fine-grained PAT
   scoped to *selected repositories* can create a repo (`POST /user/repos` → 201) and still be denied
   `git push` to it ("Permission to … denied"), and GitHub Pages is unavailable for private repos on
   the free plan. Never promise a `github.io` URL before a push succeeds.
3. telegra.ph (above) — no credentials needed at all.
4. Quick tunnels (`trycloudflare`/ngrok) — demo only; the URL dies with the process.

**Verify before it goes on a CV:** fetch the published URL, require HTTP 200 and real content, and
only then write the link into the CV.

## 5. Report shape that worked

Measured before/after table · the honest noise caveat · what remains real work (experience depth,
quantitative results — cannot be written in) · the live link · the deliverable files
(`.pdf` for sending + `.docx` so the user can edit), delivered with `MEDIA:` paths.
