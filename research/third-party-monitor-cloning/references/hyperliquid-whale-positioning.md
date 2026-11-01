# Hyperliquid perp whale positioning (worked example: bizyugoscan.com → our own monitor)

Session: 5 Okt 2026. Source `https://bizyugoscan.com/` ("bizyugoscan — King of DeFi").

## What the source actually is

A thin UI over the **free, keyless Hyperliquid info API** plus a **hardcoded list of 54 wallets**.
Its metrics: notional tracked, long/short mix ("net bias"), positioning per coin (long/short
notional + whale count each side), top net position. Wallet labels are just `Whale #1`…`Whale #71`
(a subset — numbers are skipped) and each card deep-links to `hypurrscan.io/address/<0x…>`.
No private backend was needed to reproduce it.

## Lifting the config from the HTML (no browser)

```python
h = open('/tmp/page.html', encoding='utf-8', errors='ignore').read()
addrs = sorted(set(re.findall(r'0x[a-fA-F0-9]{40}', h)))          # 54 unique
# label each one: scan forward from its hypurrscan anchor for the nearest ">Whale #N<"
```

`curl -s -A "Mozilla/5.0" https://bizyugoscan.com/` returns ~364 KB of SSR HTML containing the full
rendered board — text extraction (strip `<script>`/`<style>`, split on tags) reproduces every metric
the page shows, which is how the metric definitions were confirmed. See SKILL.md Step 1.

## The API call

`POST https://api.hyperliquid.xyz/info`, no auth, JSON body:

```json
{"type": "clearinghouseState", "user": "0x…"}
```

Response fields used:

| Field | Meaning |
|---|---|
| `marginSummary.accountValue` | account equity (USD) |
| `assetPositions[].position.coin` | ticker (`ETH`, `BTC`, `HYPE`, `kPEPE`, …) |
| `assetPositions[].position.szi` | **signed** size — sign gives LONG/SHORT |
| `assetPositions[].position.positionValue` | notional (USD) for that position |
| `…position.unrealizedPnl`, `…leverage.value` | uPnL, leverage |

54 wallets fetched with a `ThreadPoolExecutor(max_workers=8)` take **~1.3 s** total. Per-position
filter: ignore `< min_position_usd` before aggregating.

## Aggregation maths (what reproduces the board)

```
per coin: long  = Σ abs(positionValue) where szi > 0
          short = Σ abs(positionValue) where szi < 0
          net   = long − short
          count_long / count_short = number of whales on each side
total:    notional = Σ long + Σ short
          bias_pct = 100 × Σ long / notional        # "55.1% long"
top net:  coins ranked by |net|
```

## Parity check (same moment, 5 Okt 2026 ~08:36 WIB)

| Metric | bizyugoscan | our clone |
|---|---|---|
| Notional tracked | $2.25B | $2.25B |
| Long bias | 55.1% | 55.1% |
| ETH net | +$223.4M | +$223.5M |
| BTC net | +$124.4M | +$124.5M |
| HYPE net | −$32.4M | −$32.3M |

Differences of ~0.1M are refresh-timing drift, not modelling error. Quote a table like this before
telling the user the clone works.

## Our implementation

- `~/.hermes/scripts/whale_scan.py` — `--full` card, `--json`, default **delta**, `--force`, `--workers`.
- `~/.hermes/data/whale_scan_config.json` — 54 wallets + our thresholds:
  `min_position_usd 100000`, `min_notional_usd 250000`, `bias_shift_pp 3.0`,
  `coin_net_swing_usd 20000000`, `coins_watch []` (empty = all coins).
- `~/.hermes/data/whale_scan_state.json` — previous aggregate for delta comparison.
- Cron `no_agent`, every 15 min, `deliver: origin`; empty stdout when nothing crossed a threshold.

Alert path verified by editing the **state file** (bias → 50.0, ETH net −$50M) so the next run
reported `bias +5.1pp` and `ETH net $50.0M (nambah long)` while all printed numbers stayed real.

## Extending it

The wallet list is the only thing worth copying from the source — and it is replaceable. To retune:
edit `coins_watch` to the user's own holdings, lower `coin_net_swing_usd` for sensitivity, or swap
the list for the user's own smart-money set. Nothing in the tool depends on bizyugoscan staying up.
