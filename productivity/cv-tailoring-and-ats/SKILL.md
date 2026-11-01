---
name: cv-tailoring-and-ats
description: "Use when tailoring a CV or reading a CV-score link."
version: 1.0.0
author: Hermes
license: MIT
metadata:
  hermes:
    tags: [career, cv, resume, ats, docx, pdf]
    related_skills: [job-listing-hunter, docx, pdf, ocr-and-documents]
---

# CV Tailoring & ATS Review

Use when the user hands over a CV/résumé (PDF/DOCX) — alone, with a job link, or with a
"Score my CV"-style share link — and wants it judged, improved, or matched to openings. Proven
7 Okt 2026: Indonesian digital-business student → CV PDF + a `kerjaweb3.com/r/<uuid>` scorecard
link (42/100) → 1-page rewritten CV delivered as PDF + DOCX, paired with 5 live openings pulled
from the board's own API.

Not for: building a CV from scratch with no source material; cover letters; interview prep.

## 0. Extract the source text first

`read_file` on a PDF can come back **mangled** — it splits ligatures and scrambles runs
(`PT Sinar Sosro` → `PT Sinar***A* **S***cc***o**`), which silently corrupts the employer's name.
Re-extract before analysing:

```bash
# env has no pip (PEP 668) and often no pdftotext/pymupdf — use uv with ephemeral deps
uv run --quiet --with pypdf python extract.py
uv run --quiet --with python-docx --with reportlab python cv_builder_pdf_docx.py
```

Keep `--with` explicit per invocation; don't try to install into the system interpreter.

## 1. Read the scorecard as data, not as a verdict

If they sent a share/result link, pull the **raw payload** rather than describing the page. These
scorecards are stored JSON: `overall_score`, sub-scores, `score_labels`, `strengths`,
`improvements`, `summary`, and an `ats` block (`keyword_match.matched/missing`,
`missing_sections`, `parseability_flags`, `contact_completeness`). Restate it, then say plainly what
the tool cannot see: **it grades format, length and keywords — not capability.** Its advice
("quantify achievements", "gain more experience") will otherwise push you into inventing things.

Resolution recipes for client-rendered boards and their endpoints:
`job-listing-hunter/references/kerjaweb3-platform.md`.

## 2. Find the hidden asset

The strongest thing is usually buried in a one-line "skills" row (e.g.
`Implementation AI Agent (Hermes agent)` — while the person actually *operates* scheduled agent
automation). Ask what the person really builds/runs/ships, then give it its own section:
`Projects — <domain>`, with bullets that describe the work, not the interest. That single section
is what moves `technical_skills` and `relevance`.

## 3. Honest rewriting rules (non-negotiable)

- **Never invent** employers, clients, revenue, percentages, dates or durations — no fabricated
  metrics, not even as obviously-fake placeholders inside the CV text.
- Reuse only facts from the source CV plus activity the user can actually evidence.
- Where a number is genuinely required, leave an inline marker and flag it in the report
  ("yang perlu lu isi sendiri: …") instead of guessing.
- Keyword coverage must be earned: add `Web3 / crypto / on-chain / automation` only when the
  underlying activity is real (a person running on-chain monitoring legitimately carries them).
- `contact_completeness.links:false` is a free, honest point — flag the missing LinkedIn/portfolio.

## 4. Structure that survives ATS

Summary (3 lines, role-titled) → Experience (bullets: action + object + outcome) → Projects →
Skills **grouped by theme** (not a flat word cloud) → Education. One page. No columns, icons,
images, tables or text boxes.

## 5. Deliver both formats, then verify

PDF = send-ready, DOCX = editable. Deliver both with `MEDIA:/absolute/path` lines.
`templates/cv_builder_pdf_docx.py` is a working generator (reportlab + python-docx) that produced a
verified 1-page A4 PDF — edit the content block at the top, keep the layout. Then verify with
`pypdf`: page count == 1, and assert the keywords you intended actually appear in the extracted text.

Assert keywords **per language** — a bilingual generator shares one check list only if you build two
lists. Running the English doc against Indonesian expected strings reports phantom "missing" sections
and sends you re-editing a file that was already correct.

Page count and string presence do not prove the page is readable. Render page 1 to an image and look
at it before sending:

```bash
uv run --quiet --with pypdfium2 --with pillow python - <<'PY'
import pypdfium2 as pdfium
pdf = pdfium.PdfDocument("CV_Rivardo_EN.pdf")
print(len(pdf), "pages")
pdf[0].render(scale=1.7).to_pil().save("/tmp/cv_p1.png")
PY
```

Then load the PNG and check: nothing clipped at the bottom edge, closing tagline complete, no orphan
line, headings/rules aligned. Dense-but-legible is expected for a 1-page CV; a skills block that is a
solid wall of text is the usual finding and is acceptable, clipping is not.

Write the new file to a working dir (`~/career/`), never over the user's original upload.

## 5b. Editing the user's own DOCX in place

When the user sends back **their own edited CV** and asks only for fixes, do not regenerate from the
generator — their deletions (dropped projects, added language section) are decisions, and a rebuild
erases them. Patch the file so every byte of formatting survives.

No `python-docx` and no LibreOffice needed: rewrite the text inside `word/document.xml`, one run at a
time.

```python
import zipfile
src, dst = "upload.docx", "$HOME/career/CV ... Final.docx"
zin = zipfile.ZipFile(src); x = zin.read("word/document.xml").decode("utf8")
reps = [("<w:t>Automisasi</w:t>", "<w:t>Otomasi</w:t>"), ...]   # assert count == 1 per replacement
for a, b in reps:
    assert x.count(a) == 1, a
    x = x.replace(a, b, 1)
with zipfile.ZipFile(dst, "w", zipfile.ZIP_DEFLATED) as z:
    for it in zin.infolist():
        z.writestr(it, x.encode() if it.filename == "word/document.xml" else zin.read(it.filename))
```

Then verify in the same pass: `xml.dom.minidom.parseString(x)` (well-formed), re-extract the text and
print **only the changed lines**, and `file -b` must say `Microsoft Word 2007+`.

- Word splits a sentence across `<w:r>` runs, so target one `<w:t>` fragment, never the visible
  sentence. Dump ~300 chars of raw XML around the target first to see the run boundaries.
- A replacement whose text starts or ends with a space needs `xml:space="preserve"` on that `<w:t>`,
  otherwise Word silently trims it (`personal:mengolah`).
- Editing inside the run keeps bold/italic/size; rebuilding the paragraph loses it.
- Indonesian text uses straight apostrophes here, so copy the exact characters from the XML rather
  than retyping the sentence.

Checklist for a user-edited CV (the damage manual editing leaves):

- Sentences that stop mid-clause — a deleted run leaves `... dengan notifikasi Telegram` with no
  period. Most common defect, and it reads as a CV that was never re-read.
- Typos Indonesian spellcheck ignores (`Automisasi` → Otomasi).
- Vague closers (`dan sebagainya`) and category mismatch (Word/Excel filed under *Akuntansi*).
- A project the user removed is **not** restored silently: name what is lost in one line and let them
  decide.
- `"Kodenya dibangun vibe coding"` reads to HR as "no process". Keep the work, change the phrasing to
  "dibangun dengan AI coding agent di bawah arahan saya, termasuk pengujian dan serah terima".
- Patch wording only. Adding a project, a metric, or a skill is a separate, explicit decision by the
  user.

## 6. Pair it with real openings — don't hand back just the CV

If the CV arrived with a job-board link, pull that board's live listings and match them to the
profile (see `job-listing-hunter`, incl. §9 for reading a board's backing API and its apply path —
an empty `apply_url` means the user must register on the board's own portal before applying).
Judge fit on the person's **actual portfolio**, and name the requirement each match still has to
clear instead of scattering bare ✓s.

## 7. Report shape (this user)

Indonesian, casual, listing comparisons in a table, honest about what the scorecard missed, and
close with the artifacts attached — never "mau gw buatkan?". Lead with what the link actually is
(e.g. "itu hasil score CV lu sendiri, gw tarik payload-nya") so the answer is grounded, not a guess.

## 8. Positioning label (this user — fixed 14 Okt 2026)

The label is **"AI Implementation & Automation — finance & accounting operations"**
(ID: "Implementasi & Otomasi AI — Operasional Keuangan & Akuntansi"). Reasons that must survive any
later rewrite: `automation` alone reads as an n8n/Zapier tool operator, while `implementation` is a
real posting keyword (Glints "AI Implementation & Automation Specialist" Rp8–10jt, Jobstreet "AI
Implementation & System Analyst", Telmark "AI Transformation Consultant") and describes the work he
actually does — map the process, write requirements, test, hand over, then operate it. Keep
`automation` in second position as the search keyword. Mirror the label everywhere or the mismatch
is visible: GitHub profile README, portfolio site, GitHub bio, CV.

Sources of truth: `~/career/github_profile/{README.md,portfolio-index.html}` (pushed to
`rivardoad9-source/rivardoad9-source` and `rivardoad9-source/rivardo-portfolio` via the `gh api`
contents PUT + read-back), CV generator `~/career/build_cv_2lang_v2.py`.

Do **not** claim n8n proficiency anywhere — he has said plainly he is not good at it yet; n8n is the
stated gap to close, not a credential. Do not re-open the fintech-vs-AI question unless he does.

## Pitfalls

- Adding bullets to a 1-page CV and silently shipping 2 pages → after this repositioning the content
  hit 2 pages; fix by merging skills rows and trimming the summary to a single tight paragraph,
  not by dropping font below 8.6pt/10.3 leading. Always re-assert `len(reader.pages) == 1`.
- Trusting `read_file`'s PDF extraction when it returns scrambled text → re-extract with `pypdf`.
- Treating the scorecard's score as the diagnosis → it grades format/keywords; capability is elsewhere.
- Inventing metrics to satisfy "quantify your achievements" → refuse; marker + tell the user.
- Shipping DOCX only (or PDF only) → the user needs one to edit and one to send.
- Overwriting the original upload → keep it, write the new CV beside it.
- Presenting the scorecard's keyword list as the goal → it rewards stuffing; keep it honest.
