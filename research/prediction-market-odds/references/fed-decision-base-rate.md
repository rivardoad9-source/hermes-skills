# Fed/FOMC: decision base rate vs market reaction (worked case: 16 Sep 2026)

Question that produced this: *"malam ini news, hampir semua orang yakin suku bunga naik … apakah wise
untuk shorting sekarang, atau wait and see? Berdasarkan data backtest kita, ketika probabilitasnya
setinggi ini pernah ga malah ga sesuai?"*

## The distinction to make first

| Part of the event | Is it tradeable? | Evidence |
|---|---|---|
| **The decision itself** | Effectively yes — but priced, so no edge | Favorite-bucket resolved **9/9** across the last 9 FOMC decisions in Polymarket closed markets (Jan 2025 → Jan 2026: hold ×5, cut25 ×3, hold Jan-26; the Dec-2025 ≥2-dissent sub-market resolved too) |
| **The price reaction** | **No measured edge** | Our own event study: 24 combos, all `NO_EDGE_DETECTED` (below). Third-party: BTC fell after 7 of 8 FOMC meetings in 2025, *including the cutting meetings* |

So a high-consensus macro event is a *fact*, not a *trade*. Say this before answering "should I
short?" — otherwise the user hears "88.5% sure = 88.5% easy money".

## Recipes (all keyless)

**1. Live bucket odds** — `gamma-api.polymarket.com/markets?limit=60&active=true&closed=false&order=volume24hr&ascending=false`;
pull every bucket of the same meeting (hike25 / hike50+ / hold / cut25 / cut50+) and check they sum to ~1.
Worked case (fetched 2026-09-16 14:23 UTC): hike25 **88.5%** ($4.39M 24h vol), hold **11.5%** ($6.16M),
hike50+ 0.9%, cut25 0.15%, cut50+ 0.05% (Σ 100.6%). Also useful: "Fed rate hike in 2026" 95%,
"Fed Rate Hike by October 2026 Meeting?" 92%.

**2. Base rate from CLOSED markets** — `?limit=200&closed=true&order=volumeNum&ascending=false`
(and the same loop against `public-search?q=<term>&limit_per_type=40`), then **filter client-side** for
`Fed`/`FOMC` + a year. The server-side `question=` filter returns **0 rows** — do not conclude
"no history exists" from it. Every closed bucket prints resolved prices, so `{'Yes': '1', 'No': '0'}`
is the outcome and `vol=$` is the credibility weight (top meetings carry $100M+).

**3. What the Fed actually did, without a macro calendar** — FRED `DFEDTARU` (upper target range),
printed on change only:
`api.stlouisfed.org/fred/series/observations?series_id=DFEDTARU&api_key=<key>&file_type=json&observation_start=YYYY-MM-DD`
(NewsAgent's `.env` holds a working FRED key). Worked case: flat at 3.75 for all of 2026 → the
16 Sep meeting would have been the first move of the year, consistent with the 88.5% hike pricing.
Note FOMC *dates* are not in FRED — `~/NewsAgent/src/calendar.py` carries `FOMC_SCHEDULE`
(2026: Mar 17-18, Jun 16-17, **Sep 15-16**, Dec 8-9) and the statement is 14:00 ET = **18:00 UTC**.

**4. Realized reaction, per meeting** — Binance 1h klines with explicit window
(`/api/v3/klines?symbol=BTCUSDT&interval=1h&startTime=<release−6h>&endTime=<release+30h>`), then read
the **open of the release hour** as the base and compute +1h / +4h / +24h. Measured:
Mar 18 2026 −0.7 / −0.46 / −2.43%; Jun 17 2026 −0.9 / −2.8 / **−5.3%**. Same method works for
CPI/PPI/NFP at 12:30 UTC.

**5. Our own event study** — `~/NewsAgent/data/calibration.json` (+ `data/live_events.jsonl`):
4 indicators (CPI/PPI/NFP/UNEMPLOYMENT) × BTC/ETH × 15m/1h/4h = **24 combos, every one
`NO_EDGE_DETECTED`**: alignment 40.6%–53.9%, |z| < 1.2, n≈83–97 per pair, period 2019-01 → 2026-08/09.
What *is* measurable is **magnitude**, not direction: avg |move| 0.30–0.79% (15m), 0.51–1.36% (1h),
1.13–2.09% (4h). Two honest gaps to state: (a) that backtest uses a **naive random-walk surprise**,
not real market consensus; (b) **FOMC has no pair in the calibration** — CPI/PPI/NFP/Unemployment only,
so "our backtest" has never tested an FOMC directly.

**6. Third-party pattern (cite as third-party, never as ours)** — the CoinGecko-derived table quoted by
Phemex (Mar 2026): BTC 48h after each meeting fell in 7 of 8 2025 meetings (holds *and* cuts: Sep −4.9%,
Oct −3.0%), the only green print was **Dec 2025 +1.9%** — after BTC had already fallen ~24% from its
ATH. Jan 2026 hold → **−7.3% / 48h**. Reading: the pre-positioned crowd, not the decision, sets the
drift; sell-the-news happens *after* the release/presser, not before.

## Findings from the worked case

- "Almost everyone is sure" = **88.5%**, i.e. ~1-in-9 chance of a hold. Say the tail number, not the vibe.
- **Counterexample living in the same repricing:** hike odds went 35% → 60% (29 Jul 2026) while BTC rose
  **+26%** from $63,756 (27 Jul) to $80,342 (6 Sep, incl. +8.8%/+14.5%/+22.9% in three days); the
  give-back came later (→ $75,640 = −5.9% in 10 days). So "hike ⇒ USD up ⇒ risk down" had already
  failed once that quarter.
- Our live events contradicted the hawkish-bearish mapping too: PPI 10 Sep (5.41 vs 4.8 prior) →
  BTC **+1.48%**/24h; NFP 4 Sep → +0.31%.
- Report shape that landed: odds table (timestamped + venue) → decision track record → realized
  reaction table → the counterexample → "couldn't pull" line → then the engine.
- Could **not** pull: DXY and US10Y (stooq blocked from this host, Yahoo 429) → the "USD strengthening"
  half of the premise was left explicitly unverified rather than asserted.
- Engine tie-in (after the market facts, never before): FlowMetrix auto-blackouts new entries in the
  FOMC window from `data/news_blackout.json` (worked case 17:00–18:45 UTC = **00:00–01:45 WIB**) while
  monitoring continues, holds 0 positions, and is spot-LP only — it **cannot short**, so a short is a
  manual discretionary trade and there is nothing to reconfigure in the engine.
