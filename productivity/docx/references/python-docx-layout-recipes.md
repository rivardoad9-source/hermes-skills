# python-docx layout recipes (designed documents from scratch)

For documents where appearance matters: cover page, shaded table headers,
captions, running footer, shaded callouts. Built by script, regenerated
after every content change — never patched in place.

## Page budget first

A4 is 21 cm wide. Margins 2.5 left + 2.3 right leave **16.2 cm** of usable
width; 2.2 cm margins leave **16.6 cm**. Every table's column widths must
sum to that or less. Do not assert and hand-tune per table — scale the
proportions you want into the budget, so the sixth table cannot overflow:

```python
USABLE_CM = 21.0 - LEFT_CM - RIGHT_CM          # 16.6 at 2.2 cm margins
widths = [w * USABLE_CM / sum(widths) for w in widths]
```

## Helpers worth carrying between documents

```python
from docx.oxml.ns import qn
from docx.oxml import OxmlElement

def shade(cell, hexfill):                      # header / zebra rows
    tcPr = cell._tc.get_or_add_tcPr()
    el = OxmlElement("w:shd")
    el.set(qn("w:val"), "clear"); el.set(qn("w:fill"), hexfill)
    tcPr.append(el)

def cell_margins(tbl, top=60, bottom=60, left=90, right=90):
    mar = OxmlElement("w:tblCellMar")
    for side, val in (("top", top), ("left", left),
                      ("bottom", bottom), ("right", right)):
        e = OxmlElement(f"w:{side}")
        e.set(qn("w:w"), str(val)); e.set(qn("w:type"), "dxa")
        mar.append(e)
    tbl._tbl.tblPr.append(mar)

def repeat_header(row):                        # multi-page tables
    el = OxmlElement("w:tblHeader"); el.set(qn("w:val"), "true")
    row._tr.get_or_add_trPr().append(el)

def no_split(row):                             # keep a row on one page
    el = OxmlElement("w:cantSplit"); el.set(qn("w:val"), "true")
    row._tr.get_or_add_trPr().append(el)
```

Run `repeat_header` + `no_split` on the header row and `no_split` on every
body row: a table whose rows split mid-cell looks like corruption.

Zebra shading (`"F2F4F8"` on odd rows) with a navy `"1F3864"` header and
white bold header text is the combination that reads as professional without
any logo or image work.

## Page-break hygiene

Three defects show up in every long generated report, and each has a
one-line fix:

- **Callout or table row split mid-sentence.** `no_split(row)` on every row,
  including the single-cell shaded callout table. Without `w:cantSplit` the
  box breaks across the page boundary and its last line vanishes under the
  margin.
- **Table header stranded at the page bottom.** `keep_with_next = True` on
  each header-cell paragraph, so the header travels with the first body row
  instead of rendering as a bare navy strip.
- **Figure separated from its caption.** A caption *below* an image cannot
  pull the image with it: set `keep_with_next = True` on the picture
  paragraph and the caption follows. Either both land on the next page or
  both stay — never one on each side.

## Fonts

```python
st = doc.styles["Normal"]
st.font.name = "Times New Roman"
st.element.rPr.rFonts.set(qn("w:eastAsia"), "Times New Roman")   # needed, or
# CJK-capable Word installs substitute a different face
```

Academic Indonesian deliverables: Times New Roman 11–12, line spacing
1.12–1.15, justified body, bold navy headings.

## Footer with a real PAGE field

python-docx has no field API. A `w:fldSimple` element produces a page number
Word recomputes on open:

```python
fld = OxmlElement("w:fldSimple"); fld.set(qn("w:instr"), "PAGE")
r = OxmlElement("w:r"); t = OxmlElement("w:t"); t.text = "1"
r.append(t); fld.append(r); footer_p._p.append(fld)
```

## Cover anatomy that works

Centered institution block, oversized title, subtitle with the topic name,
then the identity table at roughly 50–55% of page height, with the disclaimer
note immediately under it, and the footer at the bottom. Two failure modes:
the block sits in the top third leaving a dead lower half, or a spacer big
enough to fix that pushes the note into the footer. Adjust one spacer at a
time and re-render; do not stack two large spacers.

Leave identity fields (NIM, class, lecturer) as dotted lines — the student
fills those, and a plausible-looking fabricated ID is worse than a blank.

## Verify: render, then read the render

```bash
soffice --headless --convert-to pdf --outdir preview file.docx
```

```python
import pymupdf
d = pymupdf.open("preview/file.pdf")
print(d.page_count, [len(p.get_text().strip()) for p in d])  # chars per page
for i in range(d.page_count):
    d[i].get_pixmap(dpi=95).save(f"preview/p{i+1}.png")
```

Chars-per-page finds the two defects that matter most: a near-blank page
(<600 chars on a body page) and a single line stranded on a final page. Fix
the cause — tighten line spacing by 0.03, trim one sentence — rather than
adding a page break.

Then look at the cover, the figure page, and the last page with
`vision_analyze`. Ask specifically about: columns too narrow and wrapping
badly, tables past the right margin, orphan headings, captions detached from
their table.

**Numbers: check the extracted text, never the image.** Vision OCR of digits
is unreliable (it will report `158,4` for `144,0`, or `botkita.com` for
`botkilat.com`). After any figure changes, assert against `page.get_text()`:

```python
t = "".join(p.get_text() for p in d)
assert "44,2" in t and "5,3" not in t      # new value present, stale gone
```

Do this before delivery every time a number was edited after the first
build; a report that still carries last week's figure is worse than a late
one.

## Table captions

Number every table and figure (`Tabel 1a`, `Gambar 1`) and put the caption in its own
small bold paragraph **above** the table with `keep_with_next = True`, so a page break
can never separate the label from the object. When one logical output needs two tables
(too many columns for 16.2 cm), split it into `Tabel 1a` / `Tabel 1b` and repeat the
row context in the second caption — if the break falls between them, 1b must still be
readable on its own.

Figures caption *below* the image, so the rule inverts: the image paragraph carries
`keep_with_next`, not the caption.

## Data figures

matplotlib → PNG at 260 dpi, `width=Cm(14.6)`, then center the picture
paragraph and put the caption in a separate small italic paragraph below it.
Do not repeat the chart's own `set_title` when a numbered caption sits
underneath.

Place the legend outside the plot area (`bbox_to_anchor=(0.5,-0.22)`, `ncol=2`)
when bars carry value labels at their ends; an in-plot legend sits on top of the
last bar's label and the number becomes unreadable. Leave headroom on the axis
(`set_xlim(0, max*1.15)`) for the label text itself.

matplotlib ≥3.10 renamed `boxplot(labels=...)` to `tick_labels=`; passing the
old keyword raises `AttributeError`.
