# BTC ETF flow — data source landscape & validation anchors

Verified 6 Oct 2026 while cloning `btcfundflow.vercel.app` ("Bitcoin ETF Terminal") into our own
**ETF Flow Desk** (`~/.hermes/scripts/btc_etf_collect.py` + `btc_etf_server.py`, port 8788).
Everything below was checked against an independent authority, not taken on faith.

## Where a Next/Vercel dashboard hides its data

Read the page without a browser first, then grep the downloaded JS chunks for fetch targets. This one
turned out to be a thin UI over static JSON + a handful of free APIs:

| Path | Nature |
|---|---|
| `/data/etf-flows.json` | static snapshot, `generated_at` + `latestFlowDate`; regenerated ~once/day |
| `/data/macro-assets.json` | `updatedAt` + `dailyHistory[]` + `intradayHistory[]` (hourly) |
| `/data/cointelegraph-news.json` | static news file |
| `/api/news` | the only dynamic route (server-side fetch) |

Its live numbers come from Binance / Coinbase / CoinGecko (price), **koinsayang** (USDT-IDR),
the **TradingView scanner** endpoint (macro), and a Coinglass scrape (IBIT holdings).

## Freshness verdict (the actual answer to "realtime & valid?")

| Series | Realtime? | Valid? | Evidence |
|---|---|---|---|
| BTC price | ✅ live | ✅ | theirs $86,198 vs Binance $86,222 (0.03%) |
| USD/IDR | ✅ live | ✅ | theirs Rp 17,890 vs koinsayang Rp 17,877 |
| Macro DXY/GOLD/WTI/US10Y | ⚠️ hourly snapshot (~1 h) | ✅ | DXY 101.99 vs TradingView 101.85 · GOLD 4,178.8 vs 4,169.9 |
| **BTC ETF flows** | ❌ daily, T+1 EOD | ✅ | file generated 11:11 WIB but latest row = previous US session; total −89.8 matched Farside exactly |
| IBIT holdings | ❌ daily | ⚠️ −0.5% | theirs 800,736 BTC vs official iShares 805,044 BTC |
| News | ✅ | ✅ | Cointelegraph RSS; their `generatedAt` ran ~1 h ahead of real UTC (double offset bug) |

Rule: read `generated_at` **and** the latest data date. A fresh file timestamp with a one-day-old last
row is T+1 EOD, not realtime. Say which render you measured (see the stale-SSR trap below).

## Validation anchors (use these, they work)

- **Fund holdings — the issuer's own page beats any scrape.** iShares IBIT
  (`https://www.ishares.com/us/products/333011/ishares-bitcoin-trust-fund`):
  `BTC held = "Net Assets of Fund" ÷ benchmark price` →
  `68,987,769,571 ÷ 85,694.41 = 805,044 BTC` (as of Oct 05, 2026).
  Parser gotchas: the embedded JSON is **HTML-escaped** (`&quot;` → unescape before regex), and
  only `Net Assets of Fund` sits in JSON-LD `additionalProperty`; `sharesOutstanding` and the
  benchmark (`levelAmount`) live in the escaped keyFacts blob.
- **Macro — the TradingView scanner the site itself calls:**
  `POST https://scanner.tradingview.com/global/scan`, `Content-Type: text/plain`, body
  `{"symbols":{"tickers":[…] ,"query":{"types":[]}},"columns":["close","change","Perf.W","Perf.1M","Perf.3M","Perf.6M","Perf.Y"]}`.
  `TVC:DXY`, `TVC:GOLD`, `TVC:US10Y` work; **`TVC:USOIL` returns nothing — use `NYMEX:CL1!`**.
  These `Perf.*` columns save you from storing your own history.
- **Crypto price:** Binance `api.binance.com/api/v3/ticker/24hr?symbol=BTCUSDT`; cross-check Coinbase.
  Daily closes for BTC-equivalent flows / BTC perf: `api.binance.com/api/v3/klines?symbol=BTCUSDT&interval=1d&limit=400`.
- **USDT/IDR:** `https://api.koinsayang.com/api/v2/spot/market/tickers?symbol=USDTIDR` — the rate is in
  **`lastPr`**, not `last` (guessing `last` silently yields 0.0).

## Farside access chain (the upstream is Cloudflare-fronted)

- `https://farside.co.uk/bitcoin-etf-flow-all-data/` → **403 direct** (Cloudflare).
- `https://r.jina.ai/https://farside.co.uk/bitcoin-etf-flow-all-data/` → **works, then rate-limits to
  403** after a few calls; retry-friendly but not reliable enough to be the only tier.
- Fallback that was verified equivalent: the third party's own `/data/etf-flows.json` (its daily total
  matched Farside exactly for the same session). Ship the chain **jina → public JSON** and label which
  tier answered in the UI header, so the provenance is never hidden.
- Farside's full table is the richer one: 12 per-fund columns (adds `MSBT` Morgan Stanley and `BTC`
  Grayscale Mini). The third-party JSON itemizes only 10 → those two arrive as a residual, which is
  why the UI needs the `lainnya +X` reconciliation chip.

## Dashboard implementation notes that carried over

- TTLs used: prices 60 s · macro 10 min · flows 3 h · issuer holdings 1 h.
- Farside flow rows are USD millions; BTC-equivalent = `usd_m * 1e6 ÷ that day's BTC close` (state the
  price used, since the third party's `+815 BTC` implies a slightly different benchmark).
- Sanity-check the source's own internals: 10 of their last 40 rows had `total != sum(perFund)` —
  quote the total, and reconcile the detail rather than reproducing their mismatch.
- Static SSR placeholder trap: before hydration that page showed `745,786 BTC`, `AUM $0.00B` and a
  `$77,028` BTC ticker; hydrated it showed `800,736 BTC / $69.04B / ~$86,198`. Never quote a
  server-rendered number without re-rendering in a real browser.
