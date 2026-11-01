# Re-skinning our dashboard to look like a reference product

Trigger: the user sends a screenshot of someone else's site and says "coba buat UI nya kayak gini,
warna Bitcoin" / "bikin tampilannya mirip ini". Meaning: **keep our data, copy their look**. The
deliverable is a screenshot of OUR page that reads like theirs, plus an explicit list of what you
adopted and what you dropped.

## 1. Extract the reference palette from its own CSS (don't eyeball)

Fetch the page and its chunks, regex every colour, count the repeats. The accent is the
most-repeated **non-grey** colour; greys/near-blacks are the surface ramp.

```python
import re, collections, glob
txt = ""
for p in glob.glob('/tmp/refjs/*') + ['/tmp/ref.html']:
    txt += open(p, encoding='utf-8', errors='ignore').read()
hexes = re.findall(r'#[0-9a-fA-F]{3,8}\b', txt) + re.findall(r'rgba?\([^)]*\)', txt)
for c, n in collections.Counter(hexes).most_common(25):
    print(n, c)
```

Worked example (`btcfundflow.vercel.app` → our "ETF Flow Terminal"): accent Bitcoin orange
`#f7931a`; inflow `#22c55e`; outflow `#ef4444`; info/blue `#4a9eff`; dark warm surfaces instead of
blue-greys. Then verify with `vision_analyze` on the user's own screenshot (fonts, badges, clock
format, card order) — the screenshot is the spec, the CSS only supplies exact hexes.

## 2. CSS variable set that produced the "Bitcoin terminal" look

```css
:root{
  --bg:#0b0806; --bg2:#120d09; --card:#17110d;        /* warm near-black, not blue-grey */
  --line:rgba(247,147,26,.16); --line2:rgba(247,147,26,.32);
  --acc:#f7931a; --acc2:#ffb84d;
  --up:#22c55e; --dn:#ef4444; --blue:#4a9eff;
  --txt:#f4ece2; --dim:#c9bba9; --dim2:#a99a86;       /* keep dim2 readable: <10px text dies below this */
  --mono:ui-monospace,SFMono-Regular,"JetBrains Mono",Menlo,Consolas,"DejaVu Sans Mono",monospace;
}
```
- Monospace + uppercase section labels with wide `letter-spacing` + tabular numbers = "terminal".
- Section header: small orange square + uppercase label; hero card gets an inset orange glow.
- Freshness footer per data series (source, cache age, "T+1 / live") — it doubles as the honest
  label for which numbers are realtime.

## 3. Page skeleton that survived real phone + desktop review

Order: header (₿ mark, brand, live dot, refresh) → dual clock + market-state pills → hero spot card
(big number, activity box, two side-by-side stats) → live ticker card → flows board (big total +
canvas chart + aggregates grid) → per-entity (phone cards / desktop table) → macro rows → freshness
footer.

- Phone: each entity = card (`date + total` on line 1, chips under). Desktop: `.cards` becomes
  `grid-template-columns:1fr 1fr; gap:11px` at `@media(min-width:900px)`, hero card
  `grid-column:1/-1`. A 760px column on a 1280px screen looks unfinished.
- Cap chip rows: sort by `abs(value)` desc, show top 6, fold the rest into a `lainnya` residual
  (compute it as `total - sum(shown)`, never let the chips disagree with the total).
- Wrap every `label value` pair in `<span style="white-space:nowrap">` or the mobile line breaks
  between them.
- One number-format helper for the whole page — mixed `$89.8jt` / `-$0.09B` / `+$2.08B` in one
  table reads as a bug. Sign explicit (`+`/`−`/`±`), 2 decimals for `$B`, 1 for `$jt`.
- Dict-valued API fields (`age`, `ttl` as per-section objects) must be formatted, not concatenated —
  otherwise the footer prints `[object Object]`.
- Refresh button: page calls `/api/data?force=1`, and the server must parse it and call
  `refresh(force=True)`; verify by asserting the payload timestamp moved, not that the DOM redrew.

## 4. Review loop (do not skip)

1. `node --check` the extracted inline `<script>` before shipping.
2. Playwright probe at 390×844 (`is_mobile`) and 1280×900: assert `scrollWidth == clientWidth`,
   list `getBoundingClientRect().right > vw` offenders, collect console errors.
3. `vision_analyze` the phone screenshot **and** the desktop screenshot; fix exactly the defects it
   names; re-shoot. Rate the page yourself, then re-check the specific complaints — "7/10 with 5
   named issues" is the normal first pass.
4. `curl` the public tunnel page for 200 + `<title>` before telling the user it's live.
5. Send both screenshots (`MEDIA:`) and state adopted-vs-dropped features.

## 5. Pitfalls

- Don't restart the server to see CSS changes — serve the page file per request.
- Don't let the re-skin change the numbers: re-run the data-parity check after the rewrite; a
  styling pass that silently drops a field is worse than an ugly page.
- Keep the reference's *information design*, not its junk features (games, affiliate/OTC widgets,
  music, theme switchers) — the brief is usually "duplicate yang guna aja".
