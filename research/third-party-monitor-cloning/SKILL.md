---
name: third-party-monitor-cloning
description: Use when cloning a public dashboard into a local monitor.
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [reverse-engineering, monitors, alerts, dashboards, config]
    related_skills: [onchain-analytics, hermes-cron-automation, cron-output-style]
---

# Cloning a third-party dashboard into our own monitor

## When to Use

Load when the user shares a dashboard / scanner / leaderboard URL and wants it for us — "lu bisa
catet config atau settingan dia ga, terus bikin buat personal untuk kita", "bikin versi kita dong",
"pantau kayak situs ini", or asks to replicate metrics a site shows but with our own thresholds.
Also load when a wanted metric already exists on some site and the question is "how do we get this
signal ourselves, cheaper, with our own rules".

Core idea: a public dashboard is nearly always **(a) a thin UI over a free public API +
(b) a hardcoded config list (wallets / tickers / filters) + (c) metric definitions you can read off
the rendered numbers**. Lift all three, re-implement locally, then PROVE parity against the source.
Usually the API and the config are both in the page you were already given — no login, no scraping
farm, no paid key.

## Step 1 — Read the page WITHOUT a browser first

Most modern dashboards (Next.js/React SSR) ship their data and config inside the HTML. `curl` is
faster and more reliable than driving a browser, and it works when no browser session is available:

```bash
curl -s -m 25 -A "Mozilla/5.0" https://<site>/ -o /tmp/page.html -w "http=%{http_code} size=%{size_download}\n"
```

Then strip the code and read the payload:

```python
import re, html
h = open('/tmp/page.html', encoding='utf-8', errors='ignore').read()
body = re.sub(r'<script.*?</script>', ' ', h, flags=re.S | re.I)
body = re.sub(r'<style.*?</style>', ' ', body, flags=re.S | re.I)
txt = html.unescape(re.sub(r'<[^>]+>', '\n', body))          # the rendered text
addrs = sorted(set(re.findall(r'0x[a-fA-F0-9]{40}', h)))     # the implied config
```

- **Pair items with their labels** by scanning forward from each item's anchor, e.g. find every
  `hypurrscan.io/address/(0x…)` and take the nearest `>(Whale #\d+)<` after it. That reconstructs
  the site's tracked list with the same labels it displays.
- Grep the JS chunks for the API host (`api.`, `fetch(`, `POST`) and implement against the **raw
  public API the page itself calls** — that removes the site from the critical path permanently.
- Expect "settings" to BE the list plus a few thresholds. There is rarely a hidden backend worth
  imitating; if the numbers match, you already have the whole model.

## Step 2 — Write the config as a file we own

`~/.hermes/data/<tool>_config.json`, containing: source URL + copy date, the lifted list, and
**our** thresholds (min size, delta thresholds, watch-list, ignore-list). Keep thresholds in config,
never hardcoded, so the user can retune without touching code. State the provenance in the file:
"disalin dari <site> (<date>)" — so a future session knows where the baseline came from.

## Step 3 — Re-implement with a delta-only default

- `--full` (readable card) and `--json` (machine-readable) for on-demand inspection; the **default
  mode is delta** against `~/.hermes/data/<tool>_state.json`, silent when nothing crossed a threshold.
- First run is a baseline: only compute deltas against an *existing* state, so the tool boots silent
  instead of firing every threshold as "new".
- Output goes through the shared formatter (skill `cron-output-style`, `msgstyle.py`) and gets
  registered as a `no_agent` cron with `deliver: origin` (see `hermes-cron-automation`).

## Step 4 — Prove parity BEFORE claiming it works

Render our numbers next to the source's for the same moment and quote the differences. Timing drift
of a few 0.1 is expected (their snapshot is seconds old); a 10% gap means you mis-modeled the
aggregation — fix it before reporting. Then test the ALERT path by manipulating the **state file**
(not the data) to force a delta: the printed numbers stay real, and you have proven the message
renders and the thresholds fire.

## Pitfalls

- **The first HTML you fetch is NOT the live numbers.** Next/Vercel pages SSR a cached placeholder and
  hydrate real values with JS seconds later. Reading the static HTML of `btcfundflow.vercel.app` showed
  "745,786 BTC" and "$0.00B AUM" while the hydrated page said "800,736 BTC / $69.04B" — same page, two
  different stories. Always re-check with a real browser (`networkidle` + a few seconds) before quoting
  numbers, and say which render you measured.
- **The data usually lives at a static JSON path, not an API.** Grep the downloaded JS chunks for
  fetch targets: here `/data/etf-flows.json`, `/data/macro-assets.json`, `/data/cointelegraph-news.json`,
  plus one dynamic `/api/news` route. Fetch those files directly and read their `generated_at` /
  `updatedAt` — that timestamp IS the freshness answer (`latestFlowDate` = the realtime ceiling).
- **Cloudflare-fronted upstreams (Farside) 403 direct and throttle `r.jina.ai`.** Build a source CHAIN
  and label which tier answered in the UI: jina → the third party's own public JSON → (optional)
  headless fetch. Never claim "realtime" from a daily source: ETF flows are T+1 EOD, macro was hourly.
- **Validate each series against an independent authority before cloning**: price vs Binance/Coinbase,
  macro vs the TradingView scanner endpoint the site itself calls
  (`POST https://scanner.tradingview.com/global/scan`, columns `close,change,Perf.W,Perf.1M,Perf.3M` —
  note `TVC:USOIL` returns nothing, use `NYMEX:CL1!`), fund holdings vs the issuer's own page
  (iShares IBIT: net assets ÷ benchmark price; the JSON is HTML-escaped — unescape `&quot;` first).
- **If the clone's server has its own `refresh()` instead of calling the tool's `collect()`**, derived
  fields must be added in BOTH places or the page silently shows an empty panel.
- **Restart the child by PORT OWNER, not by name.** `pkill -f "<script>.py"` inside a keeper also
  matches the agent's own shell when its command line mentions the filename (the call dies with exit
  `-15`); use `ss -ltnpH "sport = :$PORT" | grep -oP 'pid=\K[0-9]+'` then `kill $PID`.
- Direction comes from the **signed size** (`szi`), not from the sign of a notional/value field —
  aggregate `abs(notional)` per side and count whales per side.
- Parallelize fetches with a small pool (8 workers read 54 Hyperliquid wallets in ~1.3 s) and always
  report the failure count in the card; silently dropping wallets changes the aggregate.
- Don't present the clone as the source's pipeline. Say plainly: it's a copy of a public config plus
  a public API, with our own thresholds.
- "Success" from a create/list call is not write access — verify the exact path you depend on
  (see the fine-grained-PAT trap in the bundled `github-auth` / `github-repo-management` skills).

## References

- `references/hyperliquid-whale-positioning.md` — the worked example: bizyugoscan's 54-wallet
  config, the Hyperliquid `clearinghouseState` POST, the net-bias / per-coin aggregation maths, and
  the parity table that validated the clone.
