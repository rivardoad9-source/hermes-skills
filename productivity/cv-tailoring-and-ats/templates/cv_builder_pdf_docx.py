#!/usr/bin/env python3
"""1-page ATS-friendly CV generator -> PDF + DOCX.

Run:  uv run --quiet --with python-docx --with reportlab python cv_builder_pdf_docx.py
Verify:  uv run --quiet --with pypdf python -c "import pypdf;r=pypdf.PdfReader('CV.pdf');print(len(r.pages));print(r.pages[0].extract_text()[:400])"

Edit ONLY the CONTENT block. Layout is deliberately plain: no columns/icons/tables/text-boxes (ATS-safe).
Rules: never invent employers, clients, revenue or metrics — only real, evidenceable facts. Where a
number is required, leave a marker and tell the user; do not guess.
"""
import os

# ============================ CONTENT (edit this) ============================
OUT = os.path.expanduser("~/career")
NAME = "FULL NAME"
HEAD = "Role Title  |  Second Specialism"
CONTACT = "City, Country  •  +62 8xx xxxx xxxx  •  email@example.com  •  @handle"

SUMMARY = ("Two to three lines: what they are (role + institution), what they can do, and one "
           "concrete thing they actually operate. No adjectives without evidence.")

EXP = [
    ("Job Title — Employer (Unit)", "Year", [
        "Action verb + object + what it was for.",
        "Second bullet; keep each to one line.",
    ]),
]

PROJ = [
    ("Self-directed project title (what it is)", "Ongoing", [
        "Describe the work: what was built/run, the data or scope it covers, the outcome.",
        "Add a bullet only if it is real and checkable — this section is what proves capability.",
    ]),
]

SKILLS = [
    ("Domain A", "tool, tool, method, method"),
    ("Domain B", "tool, tool, method"),
    ("Personal", "communication, discipline, fast learner"),
]

EDU = [
    ("University — Degree", "in progress"),
    ("School — Programme", "graduate"),
]
# ========================== END CONTENT ==========================

os.makedirs(OUT, exist_ok=True)
docx_path = f"{OUT}/CV.docx"
pdf_path = f"{OUT}/CV.pdf"

# ---------------- DOCX ----------------
from docx import Document
from docx.shared import Pt, Cm, RGBColor

d = Document()
n = d.styles["Normal"]; n.font.name = "Calibri"; n.font.size = Pt(10)
for s in d.sections:
    s.top_margin = s.bottom_margin = Cm(1.2); s.left_margin = s.right_margin = Cm(1.5)

def para(text, size=10, bold=False, italic=False, after=2, before=0, color=None):
    p = d.add_paragraph(); p.paragraph_format.space_after = Pt(after); p.paragraph_format.space_before = Pt(before)
    r = p.add_run(text); r.bold = bold; r.italic = italic; r.font.size = Pt(size)
    if color: r.font.color.rgb = color
    return p

def bullets(items):
    for it in items:
        p = d.add_paragraph(it, style="List Bullet"); p.paragraph_format.space_after = Pt(1)
        for r in p.runs: r.font.size = Pt(10)

DARK = RGBColor(0x11, 0x11, 0x11)
H = lambda t: para(t.upper(), size=10, bold=True, before=7, after=3, color=DARK)

para(NAME, size=20, bold=True, after=0)
para(HEAD, size=10.5, after=0)
para(CONTACT, size=9, after=4)
H("Professional Summary"); para(SUMMARY)
H("Experience")
for title, yr, bl in EXP:
    para(f"{title}   |   {yr}", bold=True, after=1, before=3); bullets(bl)
H("Projects — AI & Automation")
for title, yr, bl in PROJ:
    para(f"{title}   |   {yr}", bold=True, after=1, before=3); bullets(bl)
H("Skills")
for k, v in SKILLS:
    p = d.add_paragraph(); p.paragraph_format.space_after = Pt(1)
    r = p.add_run(f"{k}: "); r.bold = True; r.font.size = Pt(10)
    r2 = p.add_run(v); r2.font.size = Pt(10)
H("Education")
for k, v in EDU:
    p = d.add_paragraph(); p.paragraph_format.space_after = Pt(1)
    r = p.add_run(k); r.bold = True; r.font.size = Pt(10)
    r2 = p.add_run(f"   |   {v}"); r2.font.size = Pt(10)
d.save(docx_path)

# ---------------- PDF ----------------
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm
from reportlab.lib import colors
from reportlab.lib.styles import ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, HRFlowable

BODY = ParagraphStyle("b", fontName="Helvetica", fontSize=9.3, leading=12.2, spaceAfter=2)
NAME_S = ParagraphStyle("n", fontName="Helvetica-Bold", fontSize=20, leading=22, spaceAfter=1)
HEAD_S = ParagraphStyle("h", fontName="Helvetica-Oblique", fontSize=10, leading=12, textColor=colors.HexColor("#333333"))
CONT_S = ParagraphStyle("c", fontName="Helvetica", fontSize=8.6, leading=11, textColor=colors.HexColor("#444444"))
SEC_S = ParagraphStyle("s", fontName="Helvetica-Bold", fontSize=9.6, leading=11, spaceBefore=7, spaceAfter=3,
                       textColor=colors.HexColor("#111111"))
ROLE_S = ParagraphStyle("r", fontName="Helvetica-Bold", fontSize=9.6, leading=11.5, spaceBefore=3, spaceAfter=1)
BUL_S = ParagraphStyle("bu", parent=BODY, leftIndent=10, bulletIndent=1, spaceAfter=1.2)

doc = SimpleDocTemplate(pdf_path, pagesize=A4, topMargin=1.15*cm, bottomMargin=1.1*cm,
                        leftMargin=1.5*cm, rightMargin=1.5*cm, title=NAME, author=NAME)
F = [Paragraph(NAME, NAME_S), Paragraph(HEAD, HEAD_S),
     Paragraph(CONTACT.replace("  •  ", " &nbsp;•&nbsp; "), CONT_S), Spacer(1, 4),
     HRFlowable(width="100%", thickness=0.8, color=colors.HexColor("#222222"), spaceAfter=4)]

def section(t):
    F.append(Paragraph(t.upper(), SEC_S))
    F.append(HRFlowable(width="100%", thickness=0.4, color=colors.HexColor("#BBBBBB"), spaceAfter=3))

section("Professional Summary"); F.append(Paragraph(SUMMARY, BODY))
section("Experience")
for title, yr, bl in EXP:
    F.append(Paragraph(f"{title} &nbsp;|&nbsp; {yr}", ROLE_S))
    for b in bl: F.append(Paragraph(b, BUL_S, bulletText="•"))
section("Projects — AI & Automation")
for title, yr, bl in PROJ:
    F.append(Paragraph(f"{title} &nbsp;|&nbsp; {yr}", ROLE_S))
    for b in bl: F.append(Paragraph(b, BUL_S, bulletText="•"))
section("Skills")
for k, v in SKILLS: F.append(Paragraph(f"<b>{k}:</b> {v}", BODY))
section("Education")
for k, v in EDU: F.append(Paragraph(f"<b>{k}</b> &nbsp;|&nbsp; {v}", BODY))

doc.build(F)
for p in (docx_path, pdf_path):
    print(f"{p}  ({os.path.getsize(p)} bytes)")
