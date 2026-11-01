# Honest attribution & claims you must confirm (CV, ID + EN)

Companion to `SKILL.md` §3. Two corrections landed on 10 Oct 2026, both caused by MY defaults
rather than the user's claims. Apply these rules before the first draft, not after he objects.

## 1. AI-assisted builds: describe the role, never the stack

The source CV and the profile said the person "builds AI-agent automations". I wrote
`Python, TypeScript/Node.js, Next.js, SQLite` into a "Software & Data" skill row. He rejected it:

> "gw ga punya basic programming" — he directs AI coding agents; he does not write code.

Replace the stack with the activity, and add one note under the Projects heading:

```
AI coding agents & tooling
directs and operates AI coding agents (Hermes Agent, Claude Code) to build and test applications;
runs, tests and maintains the results; working familiarity with Git/GitHub, database structure and
API/webhook flows at user level
```

```
AI coding agents & perkakas
mengarahkan dan mengoperasikan AI coding agent untuk membangun dan menguji aplikasi; menjalankan,
menguji, dan merawat sistem hasilnya; Git/GitHub, struktur basis data, dan alur API/webhook di
level pengguna
```

Note line (EN / ID), placed under the projects heading in italic small type:

- *"Everything below was built with AI coding agents (Claude Code, Hermes Agent) under my direction:
  I set the requirements, test the behaviour, and operate the systems. I direct and test, rather than
  write code from scratch."*
- *"Semua proyek di bawah ini dibangun bersama AI coding agent (Claude Code, Hermes Agent) atas
  arahan saya: saya menetapkan kebutuhan, menguji perilaku, dan menjalankannya, bukan menulis kode
  dari nol."*

Also strip stack names from one-line project bullets (`built with Next.js and TypeScript` →
`in a web app used on a phone`); the project's stack belongs in a README, not on the person's CV.
Per-project stack mention in a table is fine when the table is about the artefact.

Why this is a strength, not a compromise: an overstated stack survives ATS and dies in the first
technical question. "I direct and test AI-built systems" is defensible, checkable, and scarce.
Target the jobs that match the honest claim — automation/operations, finance ops, accounting-firm
and tax-office process roles — not "junior developer".

## 2. Never assume a self-rated level

`English (professional working)` was my guess and had to be walked back to
`English (basic: reads technical documents and terminology)` / `Inggris (dasar: bisa baca dokumen
dan istilah teknis)`. Rule: self-rated fields are the user's to state, never the agent's to polish.

Confirm-with-the-user list (put it in the report, do not invent): language level, phone, address
granularity, current semester, GPA if included, LinkedIn existence, notice period, licence.
Where a plausible default exists, ship the CONSERVATIVE version and flag it as
"yang perlu lu konfirmasi" — an honest CV plus one question beats a strong CV the user cannot
defend.

Keep the English CV even when English is weak: many Indonesian employers and startups ask for an
English CV while interviewing in Indonesian. Deliver both, let him pick per application.

## 3. One claim set, corrected together

CV, GitHub profile README, profile bio and the Pages portfolio repeat the same claims. When the user
corrects one, fix all four in the same pass and re-verify each (see
`github-account-ops/references/claim-honesty-non-programmer.md` for the GitHub-side commands).

## 4. Two-language build, verified

Generator pattern that worked (`~/career/build_cv_2lang.py`): one `DATA = {"ID": {...}, "EN": {...}}`
dict holding name/head/contact/links/summary/`proj_note`/section titles/exp/proj/skills/edu/lang/
tagline, then two renderers (`python-docx` for the editable file, `reportlab` for the send-ready
A4 PDF). Build with:

```bash
uv run --quiet --with python-docx --with reportlab --with pypdf python build_cv_2lang.py
```

Then verify with pypdf — page count **1**, required keywords present, and removed claims ABSENT:

```python
for kw in ("AI coding agent", "bukan menulis kode", "rather than", "Python", "TypeScript", "SQLite"):
    print(kw, kw in text)   # last three must be False
```

Trim order when the wording change pushes it to 2 pages: drop stack names and shrink one-line
project bullets first, shorten the italic note second, and only then tighten layout
(`BODY leading` 11.6 → 11.1, `spaceAfter` 2 → 1.8, margins 1.05/0.9 → 1.0/0.8 cm). Verified: 2 pages
→ exactly 1 page with every keyword still present. Never drop the Experience or Education section to
win the page.

Deliver PDF + DOCX for both languages, and put the DOCX paths in the message so he can edit without
asking.
