# Worked case: @hoteliercrypto's weekly BTC column (11 Sep 2026)

The operator shared an X profile and asked to study how the analyst works. This is the
full result, kept because the *method* is reusable even though the analyst is not.

## The corpus that made it measurable

- X posts are behind **X Super Follows** ("Subscribe to unlock") — 108 K tweets, but the
  timeline is unreadable without a subscription. A logged-out fetch of the profile gives
  only the header and locked post teasers.
- The **free framework tier lives on news.tokocrypto.com**: a weekly column titled
  `Tren Bitcoin <dd-dd bulan yyyy>: <headline>` by Hoteliercrypto, Sep 2024 → Nov 2025.
- Those URLs are not all `-by-hoteliercrypto` suffixed, so grepping only that pattern missed
  ~20 columns. The pattern to grep is `/(tren|trend)d?-bitcoin` across
  `post-sitemap*.xml` (11 sitemaps, ~5.5 MB); 63 columns, ~491 K chars of text.
- Columns stop at Nov 2025 — so the weekly watcher built on top is silent by design until he
  writes again. Say that out loud rather than letting a quiet job look broken.

## What the scoring showed

| Measure | Result |
|---|---|
| Calls | bullish 42 · bearish 13 · neutral 6 (69% long-biased) |
| BTC that period | avg weekly move 1.96%; only 4 weeks > 5%; 36 of 58 weeks flat (±2%) |
| Same-week, decisive | 22 HIT / 7 MISS / 29 flat → 76% of 29 decisive weeks |
| Same-week, sensitivity | 66% (±0.5), 61% (±1), 68% (±2), 60% (±3) |
| **Always-bullish baseline** | **55%** |
| His "lag 1-2 weeks" apology | +1w **54%** · +2w **56%** · +3w **53%** — the excuse is false |

His lens, by keyword frequency: DXY 495 · inflasi 469 · Tiongkok 440 · Fed 280 · claim 259
· suku bunga 200 · liquidity 151 · CPI 146 · NFP 124 · housing 123 · JOLTS 101 · yen 45 ·
carry 19 · **yield 7 · bond 5 · ETF 4** → a US/China macro-liquidity lens, not crypto-native.

His own published self-verdicts (regex over akurat/meleset/zonk/salah) were the strongest
signal in the whole corpus — he grades himself honestly, and repeatedly:

> "Artikel kita minggu ini salah telak." · "Garis kuning itu adalah jejak kesalahan saya
> dalam memprediksi, sehingga terbukti bahwa analisa saya cenderung salah." · "Berkali-kali
> analisa saya salah adalah bukti bahwa posisi saya sama dengan Trader yaitu meraba-raba." ·
> "Ingat, ini semua hanyalah cocoklogi, saya tidak boleh dijadikan acuan, hanya boleh
> dijadikan hiburan." · "Menjadikan saya acuan adalah salah."

## The judgment that came out of it

Adopt: (1) the weekly review loop — but with a **computed hit rate**, which he never does
(that absence is his biggest flaw and the reason "sering benar" stays a feeling); (2)
calendar-discipline as the daily frame; (3) falsifiable numbers; (4) separating *volatility*
(real, measurable around releases) from *direction* (no edge).

Drop: directional narrative as a signal; the lag excuse; unfalsifiable causal chains
(housing starts → US debt → DXY); the free-framework/paid-signal split; long-horizon
monetary sermon.

## The measurement that mattered more than his

Running the same harness on OUR OWN rule table (`src/rule_engine.py` INDICATOR_TABLE) over
74 real releases (CPI 24 / PPI 25 / NFP 25, 26 months, naive-previous baseline, BTC 15m
candles):

| Indicator | avg \|15m\| | avg \|1h\| | avg \|4h\| | hit 1h |
|---|---|---|---|---|
| CPI | 0.78% | 0.83% | 1.46% | 8/16 |
| PPI | 0.62% | 0.77% | 1.25% | 9/20 |
| NFP | 0.85% | 0.83% | 1.36% | 8/19 |
| **TOTAL** | | | | **25/55 = 45%** |

Verdict mix: **74% BEARISH** — the naive-previous baseline (actual − previous) is almost
always positive in level terms, so the verdict collapses to one side: an artefact, not
information. Two durable reads: **volatility around releases is predictably large** (justifies
a blackout gate), **direction is not** (justifies never trading the print).

## Reusable scripts from this case

- `~/.hermes/scripts/hotelier_weekly.py` — sitemap → fetch → classify → score → weekly
  `no_agent` cron (`a3998b3691d6`, Mon 08:15 WIB), silent unless a new column appears.
- `~/.hermes/scripts/macro_direction_test.py` — the rule-table test above (FRED release dates
  + series via **curl**, candles via `data-api.binance.vision`), ~2 min, writes
  `~/.hermes/cache/macro_direction_test.json`.
- `~/.hermes/scripts/na_scorecard.py` — our own verdict-vs-BTC hit rate from
  `NewsAgent/data/live_events.jsonl`, daily cron, silent unless a new release is scored.
- Corpus cache: `~/.hermes/cache/hotelier/` (columns/, scorecard.csv, state.json).
