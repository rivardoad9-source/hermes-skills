# Bilingual CV generation — one generator, N languages

Worked example: 10 Oct 2026, Indonesian + English CVs (PDF + DOCX each) produced from one script
(`~/career/build_cv_2lang.py`), both verified as exactly 1 page A4 with the intended keywords.

## Shape that works

One `DATA` dict per language, one shared layout:

```python
DATA = {}
DATA["ID"] = dict(name=..., head=..., contact=..., links=..., summary=...,
                  sec_sum="Ringkasan", sec_exp="Pengalaman Kerja", sec_proj="Proyek — AI & Otomasi",
                  sec_skill="Keahlian", sec_edu="Pendidikan", sec_lang="Bahasa",
                  exp=[(title, year, [bullets])], proj=[...], skills=[(group, text)],
                  edu=[...], lang="...", tagline="...")
DATA["EN"] = dict(...)   # same keys
for lang in ("ID", "EN"):
    build_docx(DATA[lang], f"CV_Name_{lang}.docx")
    build_pdf(DATA[lang],  f"CV_Name_{lang}.pdf")
```

- Section headings live **in the data** (`sec_*`), never hardcoded per language — including the
  summary heading ("Ringkasan" / "Professional Summary").
- Never fork the layout into two scripts: the two CVs drift (different bullets, different ordering)
  within a week and the pair stops being a pair.
- **Localise every string, including the closing tagline.** Real defect caught by verification: the
  Indonesian CV ended with the English "Open to remote internships in Web3, fintech, or AI
  automation…" because the tagline was one shared constant. A bilingual reviewer spots that instantly.

## Run and verify

```bash
~/.hermes/bin/uv run --quiet --with python-docx --with reportlab --with pypdf python build_cv_2lang.py
```

Verify per file with `pypdf`: `len(pages) == 1` and the intended keywords present. Use a
**per-language keyword list**: assert `25 dari 25` in the ID text and `25 of 25` in the EN text. A
single shared list produces false "missing" flags for the other language's variant, which reads as a
content gap when it is only a translation.

Naming: `CV_<Name>_<LANG>.pdf` / `.docx` in `~/career/`, never overwriting the previous generation
(keep the old pair to compare). Deliver PDF (send-ready) + DOCX (editable) for BOTH languages with
`MEDIA:` lines in one message.

## Content rules for this user

- Facts come only from the previous CV plus work that can be evidenced. The user's own confirmation is
  the source of truth, so end with an explicit short list of the things you could not know and must
  not invent: English level, LinkedIn presence, phone number, address, current semester.
- Newest, strongest project first, with only checkable numbers ("25 of 25 local test scenarios pass"),
  and describe private/commercial code as the WHAT with "demo on request" instead of publishing it.
- Once the GitHub Pages portfolio is live, use it (and the GitHub profile) as the contact link instead
  of the older telegra.ph page — the Pages site is the asset that gets updated, so the CV link stays
  true.
- Same headline structure as the previous accepted CV ("Digital Business Student | Accounting &
  AI-Agent Automation"), only the body gets richer. ATS keyword coverage is earned by naming real
  tools used (Accurate, MYOB, SQLite, REST APIs, Telegram Bot API, WhatsApp Cloud API).

## Pitfalls

- Patching a multi-dict generator with find/replace where `old_string` ends on the line that closes a
  dict (`)`) or on the following `DATA["EN"] = dict(` line: the replacement swallows the boundary and
  silently merges the two dicts. Symptom is a runtime `KeyError` or the EN CV rendering ID content.
  After any edit, grep the `DATA[` markers and each closing paren, then rerun and re-verify both PDFs.
- Six projects with 1-3 one-line bullets each is what fits one page at 9-9.3pt with ~1.05cm margins.
  Adding a seventh project means trimming a bullet elsewhere, never shrinking the font.
- Don't vary section titles between generations ("Ringkasan" one week, "Profil Singkat" the next):
  consistency is worth more than variety for anything that gets parsed.
