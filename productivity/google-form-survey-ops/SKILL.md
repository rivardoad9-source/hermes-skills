---
name: google-form-survey-ops
description: Use when a coursework Google Form survey needs QA or reach.
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [survey, google-forms, research, data-quality]
    related_skills: [academic-practicum-deliverables, xlsx]
---

# Google Form survey ops (coursework / thesis)

## When to Use

- The user shares a `forms.gle` or `docs.google.com/forms` link for a class or thesis questionnaire.
- The user asks for help filling it, or asks for "dummy" respondents.
- The user needs respondents fast and wants distribution channels or message copy.
- Responses are in and need a quality check before analysis.

Covers the full loop: audit the instrument, QA-test it, distribute it, then QC the data before analysis.

## Hard rule: never fabricate responses
Refuse dummy/fake submissions, even "just 10", and even when the user asks twice. Reason to give (once, briefly, no lecture): fake rows shift means and tighten variance in exactly the cells being tested, and answer patterns (identical durations, straight-lined matrices, same-minute timestamps, same IP) are what a marketing-research grader looks for. Offer a QA test instead — that is the real need behind the ask.

## Step 1: audit the instrument (5 min, before spreading)
Read the form structure from `FB_PUBLIC_LOAD_DATA_` in the viewform HTML (see Step 2). Check and report:
- **Eligibility gates not enforced**: a screening question with age/buyer criteria is just a recorded answer by default. Options outside the target band still submit. Flag it, and say the sample must be filtered manually unless a real gate is added.
- Required flags per question, number of sections, estimated minutes.
- Whether it collects email / forces login (affects response rate and dedupe).
- Long matrices (8 brands x 4 columns) are the drop-off point; recommend cutting to the core brands.
- "Open text" questions that are actually checkbox lists without a "Lainnya" option.
- Typos in question text: cheap to fix, and they make respondents distrust the form.

## Step 2: QA test with two real submissions
Agree with the user first that the two rows will be deleted. Submit two visibly different profiles (different age band, occupation, spend, brand set) so both branching and matrices get exercised.

Two submission paths:
1. **Browser** (works but flaky): click through each section, dispatch clicks on `[role=radio]` by `data-value`, `[role=checkbox]` for multi-select. Verify `document.querySelectorAll('[role=radio][aria-checked=true]')` equals the radiogroup count before hitting Next/Submit. Rapid click loops can crash the CDP session and lose progress.
2. **Direct POST** (fast, headless, survives browser death) — preferred:
   - `curl -sL --compressed -A "Mozilla/5.0" https://docs.google.com/forms/d/e/<ID>/viewform -o form.html`
   - Parse `FB_PUBLIC_LOAD_DATA_ = (\[.*?\]);` — `data[1][1]` is the item list. For type 2/4/5 the entry id is `item[4][0][0]`. For type 7 grids every row in `item[4]` carries its own entry id (`row[0]`) and label (`row[3][0]`). Type 8 = section header, type 6 = closing message.
   - Build `entry.<id>=<option text>` pairs (option text must match the form text exactly), then add `fvv=1`, `pageHistory=0,1,2,3`, `fbzx=<value from name="fbzx" in form.html>`.
   - POST urlencoded to `https://docs.google.com/forms/d/e/<ID>/formResponse`. Success = HTTP 200 and the confirmation string ("recorded" / "已记录") in the HTML; validation failures leave the question error markup instead.
- Report to the user: exact submit timestamps, the answers used per row, and the deletion path (Responses tab → Sheets icon → delete the two bottom rows, **delete rows, not filter**), plus "response count must drop by 2".
- A successful bare POST also proves there is no bot protection: mention it and suggest limiting to one response or deduping in the sheet.

## Step 3: distribution
Broadcast to groups is the lowest-yield channel; personal DM is what actually converts. Order:
1. 20 personal DMs to people who clearly match the criteria, asking each to forward to two others (snowball).
2. Class/angkatan and alumni WhatsApp groups, sent 19:00–21:00 local, not morning.
3. IG Story / Threads with a screenshot and one line of reason, not a bare link.
4. Ask 3–5 people with relevant followers to repost.
5. Lecturer or class coordinator forwarding to other classes — usually the biggest single-day jump.

Sample size rules to quote: PLS-SEM ≈ 10 x the largest indicator count (typically n=100–150); plain regression ≈ 5–10 x number of variables (n=50–80). Screening pass rate is roughly 70–80% of clicks, so seed about 1.4x the target.

## Step 4: QC before analysis
Ask for view access to the response sheet, then check: completion duration outliers, straight-lining across matrices, eligibility-question distribution (who slipped through the ungated question), duplicate submissions, and clean n vs target.

## Pitfalls
- Do not treat an ungated screening question as a filter — it is not.
- Do not leave QA rows in the sheet; if the user forgets, the rows are the newest two with known timestamps.
- The form's language follows the browser locale, so section labels can appear in Chinese/English; the question text stays as authored.
- `forms.gle` short links 302 to the `docs.google.com/forms/d/<ID>/viewform` URL — resolve it before parsing.
