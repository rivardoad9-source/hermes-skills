# Head-to-head: two signal sources on identical rails

Companion to ladder step 11. Worked case (2 Oct 2026): a Telegram call broadcaster
(@kolsignal, 795 calls) vs our own engine's signal ledger (211 ENTER signals over 6 pools).
Numbers below are from that run, included so a future session can sanity-check the *shape*
of its own output — do not reuse them as facts about any other pair of sources.

## 1. Same rails, or it is not a comparison

For BOTH sources, identical:
- **baseline** = close of the candle that contains the signal/call timestamp;
- **horizons** = +5m / +15m / +30m / +1h / +6h / now;
- **outputs** = median multiple, % in profit at each horizon, peak within 6h,
  drawdown within 6h, % that touched −8%, cumulative peak ≥1.05x / 1.1x / 1.5x / 2x / 5x;
- **dedupe** = one signal per pool/symbol per hour, and report both the full and the
  deduped pass (the engine emitted 211 ENTER rows over only 6 distinct pools).

A source that is scored on nicer horizons than the other is not a comparison, it is an ad.

## 2. Price-unit trap (this bit us)

Internal ledgers (engine signal ledger, trade DB) store a **pool-internal quote**, not the USD
market price. Ledger `entryPrice` vs the same-instant market candle close differed by ×85–200
and the ratio **drifted per signal**, so it is not a constant you can divide out either.

Rule: never mix two price series inside one ratio. Build the baseline and every forward point
from **one** series (market candles); keep the ledger price as metadata only, and flag the
mismatch rather than "fixing" it.

## 3. "Now" is not the last candle

OHLCV windows end early — one pool's 5m data stopped on 23 Sep while signals ran to 29 Sep, so
"last candle close" silently answered a different question. Pull the current price from the
live pool endpoint (`/networks/solana/pools/<pool>` → `base_token_price_usd`) and use it for
the "hold to now" column. Note in the report if a pool's data window ends before the signal.

## 4. Cross-validation that proves an exit rule

Replay-derived hit rate should approximate the realized book win rate. Here: **76.8%** of
signals touched +5% within 6h ↔ **75%** win rate (6/8, every win a TP +5%) in live closed
positions. Two independent samples, same mechanic ⇒ the rule is real, not small-sample luck.
Use this whenever realized n < 10 — it is the honest way to say "the mechanic checks out"
without pretending 8 trades are evidence.

## 5. Break-even win rate from the payoff ratio

State it explicitly: `BE = avg_loss / (avg_win + avg_loss)` → 15.85 / (9.72 + 15.85) = **62%**
vs a realized 75%. Without that line, "75% win rate" reads as a big edge even though avg win
was *smaller* than avg loss.

## 6. Mechanism caveat: token price ≠ LP equity

When one source broadcasts spot calls and the other runs LP (or any fee-earning strategy), the
LP's equity path is not the token price path — fees offset decay. Say this **before** the
table, or the reader takes the price comparison as P&L. Deliver two layers:
price-path (apple-to-apple) **and** each source's realized money.

## 7. Fetch recipe — GeckoTerminal pool OHLCV

- `https://api.geckoterminal.com/api/v2/networks/solana/pools/<pool>/ohlcv/minute?aggregate=5&limit=1000&before_timestamp=<unix>`
  → paginate backwards using the minimum ts of the batch just returned; 1000 candles per call.
- 429 is routine on the free tier: pace ≥3.5–4s between calls, retry with sleep `8+4i` seconds.
- A 6-pool × 4-page pull takes minutes → run it as a **background process with completion
  notification**, and dump the accumulated JSON after *each* pool so a killed run is resumable
  (a foreground call was killed mid-fetch and the partial file saved the re-run).
- Bad/truncated pool addresses show up as identical pools differing in the last character
  (log-truncation artifacts) — normalise by prefix before counting "unique pools".
- Tokens with 1h-only history exist: fall back to `aggregate=1&interval=hour` and skip the
  sub-hour horizons rather than dropping the pool.

## 8. Shape of the result (channel vs systematic engine)

| metric | broadcaster (795 calls) | engine signals (211) |
|---|---|---|
| +5m median | −26% (24% green) | 0% (40% green) |
| +6h median | −54% (14%) | −10% (27%) |
| peak ≥1.5x | 44.9% | 3.3% |
| peak ≥5x | 10.2% | 0% |
| drawdown median | −76% | −21% |
| hold to now | −70% (8% green) | −41% (0.5% green) |

Expected pattern: a high-frequency broadcaster buys late into a pump ⇒ fat right tail, brutal
median, near-total stop-out rate. A systematic engine that screens for liquidity/fee flow
enters flat ⇒ safe median, no tail at all, and its money comes from fees rather than price.

## 9. Verdict framing (three columns, not one winner)

- **entry quality** — median path + drawdown right after the signal
- **upside tail** — % of calls reaching ≥1.5x / ≥5x
- **realized money** — closed-trade win rate and net P&L of each source

A source routinely wins one column and loses another; the useful answer names which column the
user actually cares about. Also flag dead liquidity (pools at signal vs now: $272k → $27k,
$148k → $8.8k) so a "hold to now" column is not read as a live position.
