# HTML/Markdown → PDF with headless Chrome

Use this when the deliverable needs real CSS layout, embedded screenshots, or many pages. reportlab is for structured specs; a designed report comes from HTML printed by Chromium.

## Pipeline

1. Author each document as Markdown (one file per document) so edits stay reviewable.
2. Convert with `python-markdown`:

```python
body = markdown.markdown(text, extensions=["extra", "tables", "fenced_code", "sane_lists"])
```

3. Inline every local image as a base64 data URI before printing. Headless Chrome frequently will not resolve `file://` subresources, and data URIs make the HTML self-contained for archiving:

```python
def img_to_data_uri(m):
    p = (DOCS / m.group(1)).resolve()
    if not p.exists():
        print(f"! missing image: {m.group(1)}")
        return m.group(0)
    data = base64.b64encode(p.read_bytes()).decode()
    return f'src="data:image/png;base64,{data}"'

body = re.sub(r'src="([^"]+)"', img_to_data_uri, body)
```

4. Print with Chromium directly (no wkhtmltopdf, no puppeteer):

```bash
chrome --headless=new --no-sandbox --disable-gpu --no-pdf-header-footer \
  --print-to-pdf=out.pdf file:///abs/path/doc.html
```

Always pass `--print-to-pdf` an absolute output path; a relative path lands next to the Chrome binary.

## A4 CSS that survives print

```css
@page { size: A4; margin: 16mm 15mm 18mm 15mm; }
body { font-family: "DejaVu Sans", sans-serif; font-size: 10.5pt; line-height: 1.55; }
h1 { font-size: 22pt; margin: 0 0 4mm; }
h2 { font-size: 13pt; margin: 8mm 0 2.5mm; border-bottom: 1.2pt solid #17181c;
     page-break-after: avoid; }
img { max-width: 100%; height: auto; display: block; margin: 3mm 0 4mm;
      border: 1pt solid #d8d8d8; border-radius: 2mm; page-break-inside: avoid; }
table { width: 100%; border-collapse: collapse; font-size: 9.5pt; page-break-inside: avoid; }
th { background: #17181c; color: #fff; text-align: left; padding: 2mm 2.5mm; }
td { padding: 1.8mm 2.5mm; border-bottom: .6pt solid #ddd; }
pre { background: #17181c; color: #eaeaea; padding: 4mm; font-size: 8.6pt;
      page-break-inside: avoid; }
```

## Pitfalls

- **Markdown collapses consecutive lines into one paragraph.** A metadata block written as three bare `**Status:**` / `**Role:**` / `**Size:**` lines prints as one run-on sentence. Use list items or explicit `<br>`.
- **Broken images print silently.** Chrome renders a gap and still exits 0. Log missing `src` values during conversion and fix them before printing.
- **Chrome exits 0 on a blank page.** Check the PDF size and inspect the rendered page; never report "generated" from the exit code alone.
- **No poppler for inspection.** `pdftoppm`/`pdfinfo` are often absent. Screenshot the HTML instead — same layout engine, no extra install:

```bash
chrome --headless=new --no-sandbox --disable-gpu --hide-scrollbars \
  --window-size=794,1400 --virtual-time-budget=5000 \
  --screenshot=/tmp/page.png file:///abs/path/doc.html
```

A4 at 96 dpi is 794 px wide, so the screenshot matches the page width. Inspect it with `vision_analyze` for clipping, overlap, and missing images.
- **Keep screenshots ~1200 px wide.** Full-page captures at native resolution inflate a 6-page PDF past 1 MB with no visible gain.
- **Headings break badly at page edges.** `page-break-after: avoid` on `h2`/`h3` and `page-break-inside: avoid` on tables/images is what keeps a heading from sitting alone at the bottom of a page.

## Batch behaviour

Render every document from one script that takes filename filters, so a fix to the CSS or a replaced screenshot is one command. Re-render only the affected documents when iterating, then re-upload those files.