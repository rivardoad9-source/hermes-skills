# Re-scoring a rewrite, and publishing the portfolio link

Companion to `references/cv-scorecard-payloads.md`. That file covers READING a scorecard; this one
covers MEASURING a rewrite and fixing the `links` gap for real.

## 1. Re-score through the same analyzer instead of claiming improvement

The analyzer behind a "Score my CV" flow is callable directly. For Kerja Web3:

```
POST <proj>/functions/v1/analyze-cv
Hdr  Content-Type: application/json ; apikey: <anon from bundle> ; Authorization: Bearer <anon>
Body {"cvText": "<text extracted from the NEW cv>", "role": "Finance / Accounting", "githubUrl": ""}
```

Extract `cvText` from the regenerated PDF (`pypdf`) rather than retyping it — the analyzer sees
exactly what an ATS would. Save each response to its own JSON file (`kw_score_original.json`,
`kw_score_new.json`) so before/after is auditable, and report a measured table:

| | before | after |
|---|---|---|
| overall | 42 | 53 |
| ATS | 60 | 75 |
| links | ❌ | ✅ |

## 2. The overall score is noise — say so

Three runs on a near-identical CV returned **52 / 48 / 53** overall. An LLM grades it and wobbles
±5. The ATS sub-block was stable at **75 every run**.

Worse, the flagged `missing` keywords contradicted the text: `DeFi`, `audit` and `budgeting` were
reported missing while all three were literally in the CV, and the missing-set changed between runs
with no edit in between.

Therefore:
- Report the **range** and label the unstable part as noise. Never quote one run as "your score".
- Optimize the **keyword block + structural checklist**; do not iterate until the overall number is
  high — it will disagree with you on the next run.
- When a run flags a keyword the CV already contains, that is evidence about the grader, not about
  the CV. Say it out loud instead of silently stuffing the word again.

## 3. Keyword expansion that stays honest

Turn every missing keyword into a TRUE phrase, and mark study-level claims so the user can defend
them in an interview:

- `Web3 / Blockchain / Cryptocurrency / DeFi` → one labelled line built from real activity:
  "on-chain data analysis, blockchain wallet & transaction tracking, cryptocurrency market
  monitoring, DeFi LP position tracking".
- `Compliance` → the real adjacent work: "tax-reporting document filing (compliance SOP)".
- `GAAP & IFRS / auditing / budgeting / ERP systems` → "…(coursework)" for a student; ERP = the
  accounting systems already listed (Accurate, MYOB).
- **Spelling matters to the matcher**: `financial modelling` did not satisfy `financial modeling` —
  use US spelling in an English CV.

Keywords are only worth adding when the underlying activity exists. This is the same rule as §3 of
the parent SKILL.md: no invented metrics, no invented employers.

## 4. Fixing `contact_completeness.links` — a durable public page

The grader dings `links: false`; the fix is a real URL in the contact block (email + handle +
portfolio). Keep the phone number OFF the public page.

**Permissionless route that worked (telegra.ph — no account, no email, page persists):**

```python
post("https://api.telegra.ph/createAccount", {"short_name": ..., "author_name": ...})   # -> access_token
post("https://api.telegra.ph/createPage", {"access_token": T, "title": ...,
      "author_name": ..., "content": json.dumps(nodes)})                                # -> url, path
post("https://api.telegra.ph/editPage/<path>", {"access_token": T, ...})                # update IN PLACE
```

`content` is Telegraph Node JSON: `{"tag": "h3"/"p"/"ul"/"li"/"b"/"a", "children": [...]}`. Editing
with the **same account token** keeps the URL stable, so the link already printed on the CV never
breaks — update the page when the CV changes instead of creating a new one.

Host ladder for a link that must live for months:
1. A stable domain the user already owns.
2. Static host on a repo you can actually WRITE to — **verify write access first**. A fine-grained
   PAT scoped to *selected repositories* created a repo (`POST /user/repos` → 201) and was then
   denied `git push` ("Permission to … denied to …"); GitHub Pages is also unavailable for private
   repos on the free plan. Confirming "created" is not confirming "can publish".
3. telegra.ph (above) — needs no credentials at all.
4. Quick tunnels (`trycloudflare`, ngrok) — demo only; the URL dies with the process, so never put
   one on a CV.

**Verify before it goes on the CV:** fetch the published URL, require HTTP 200 and real rendered
content, only then write the link into the contact block and regenerate the CV.

## 5. Report the gap that cannot be written in

After the keyword work, the residue is experience and quantified results —
`experience_depth` and `market_readiness` are the lowest sub-scores and no wording fixes them. State
that plainly, and ask for the user's real numbers (pipelines built, reports/month, volume handled)
rather than leaving the CV with invented quantification. Also name items you cannot create for them
(LinkedIn account, real employer history) instead of implying they are handled.
