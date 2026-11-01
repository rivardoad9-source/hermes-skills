---
name: prediction-market-odds
description: "Answer 'how likely is X' from prediction-market odds."
version: 1.0.0
author: Hermes Agent
license: MIT
platforms: [linux, macos]
metadata:
  hermes:
    tags: [prediction-markets, polymarket, kalshi, macro, probability, bitcoin, fed]
    related_skills: [gmgn-market, analyst-claim-verification]
---

# Prediction-Market Odds (answering probability questions from real market prices)

Use when the question is a **probability**: "kenapa/berapa kemungkinan Fed cut", "odds X jadi
next project", "is Y likely", "what does the market think of Z". Also use it before explaining a
market move that is supposedly caused by an expected event.

**Hard rule for this user: a probability question is answered from market-implied odds, not from
opinion.** Quote the market, its price, and its volume — then interpret.

## 1. Pull the odds (Polymarket, no key, works from a plain VM)

```bash
curl -s "https://gamma-api.polymarket.com/markets?limit=60&active=true&closed=false&order=volume24hr&ascending=false" \
  | python3 -c "import sys,json;[print(m['question'],m.get('outcomes'),m.get('outcomePrices'),m.get('volume24hr'),m.get('endDate')) for m in json.load(sys.stdin)]"
```

- Read `outcomePrices` as decimals of probability: `["0.145","0.855"]` on
  `outcomes=["Yes","No"]` = **14.5% yes**. A price of `0.845` on "increase rates" is 84.5%.
- `volume24hr` is the credibility weight — a 0.25% bucket with huge volume is a real market
  saying "almost never", not an untraded line.
- **Always pull every bucket of the same event** (cut / hold / hike / ±50bps). They should sum to
  ~1; if you quote one bucket alone you can invert the story.
- Two markets on the same event can exist (September meeting vs "a hike in 2026") — quote which
  one, and `endDate`/resolution date, or the number is meaningless.
- Cross-check with Kalshi/CME FedWatch **via dated reporting**, not from memory: a figure like
  "hike odds 79%" is only usable with its date. `scripts/pull_prediction_markets.py` also prints
  the realized price path so the odds can be checked against what the asset actually did.

Ready to run: `scripts/pull_prediction_markets.py` (Polymarket keyword filter + Binance spot and
daily closes). Run it before answering; don't hand-type endpoints each time.

## 1b. Siapa pemain atasnya (leaderboard + dossier wallet, tanpa key)

Diverifikasi 20 Sep 2026 dari VM ini. Endpoint publik, tidak butuh API key:

| Butuh | Endpoint |
|---|---|
| PnL board | `https://lb-api.polymarket.com/profit?window={all\|30d\|7d\|1d}&limit=N` |
| Volume board | `https://lb-api.polymarket.com/volume?window={all\|30d\|1d}&limit=N` |
| Padanan data-api | `data-api.polymarket.com/v1/leaderboard?timePeriod=<...>&orderBy=pnl\|vol&limit=N` |
| Portfolio value | `data-api.polymarket.com/value?user=0x...` |
| Posisi terbuka | `data-api.polymarket.com/positions?user=0x...&limit=200&sortBy=CURRENT&sortDirection=DESC` |
| Posisi closed | `data-api.polymarket.com/closed-positions?user=0x...&limit=50&offset=N` (maks 50/halaman) |
| Aktivitas | `data-api.polymarket.com/activity?user=0x...&limit=50&type=TRADE` |

⚠️ **Pitfall yang mahal:** di `data-api`/`lb-api` parameternya `timePeriod` (untuk data-api) —
kalau salah nama (`window=all` di data-api) dia **tidak error**, tapi diam-diam mengembalikan jendela
1d, jadi semua window tampak berisi orang yang sama. `lb-api` pakai `window` dan hanya menerima
`all|30d|7d|1d` (1y/1m/1w/24h → HTTP 400). Cek selalu: angka window berbeda harus berbeda.

Angka acuan 20 Sep 2026 (all-time): swisstony $23,6M · Theo4 $22,1M · Fredi9999 $16,6M · RN1 $13,9M.
30d: 00gringo00 $3,65M · totoro3miyazaki $2,46M · TheReturnOfDarthMaul $2,00M.
Volume all-time: swisstony $1,85B.

**Baca board ini dengan skeptis:** papan PnL teratas itu whale olahraga/politik (sports spread,
"Zelenskyy out", US Open) dengan modal jutaan dolar — bukan sinyal yang bisa diikuti dengan modal
$100-200 (gates: ukuran klip + jangkauan latency). Dan `winrate` dari sample `closed-positions`
**survivor-biased** (banyak wallet "WR 100%" karena yang muncul cuma posisi yang sudah diredeem) —
jangan laporkan WR dari situ sebagai fakta; rekonstruksi dari `activity`/redeem lebih dulu.

Siap pakai: `~/.hermes/scripts/pm_top_players.py` (snapshot 4 window + dossier value/posisi/kategori,
simpan ke `~/.hermes/data/pm_top_players.json`) dan `scripts/price_ladder_distribution.py`.

## 2. Companions you can actually get without a key

- **Crypto spot & history**: Binance public REST — `api.binance.com/api/v3/ticker/24hr?symbol=BTCUSDT`
  and `/api/v3/klines?symbol=BTCUSDT&interval=1d&limit=14`. Works from a server, no key.
  Fallback host if geo-blocked: `data-api.binance.vision`.
- **Equity/ETF/FX feeds**: benchmark index endpoints (Yahoo `query1.finance.yahoo.com`) can return
  `429` and stooq can return empty from a datacenter IP. **If you cannot pull DXY or US10Y, say so** —
  do not assert "the dollar weakened" as the explanation for a move you could not measure. Naming a
  data gap is a correct answer; inventing a driver is not.

## 3. Interpret: what the premise usually gets wrong

Worked example (14 Sep 2026, the session that created this skill): the user asked *"why is bitcoin
rising when the probability of a rate cut is very low?"*. Facts pulled: Polymarket priced
**hike 84.5% / hold 14.5% / cut 0.25%** for the 16 Sep FOMC, and BTC was **$78.6k, +1.85% in 24h but
still ~4.5% below its 3 Sep spike**, i.e. chopping in a 76–81k range, not rallying.

So the answer was not "here is why BTC ignores the Fed". It was:

1. **Correct the premise first.** The market was not pricing "no cut" — it was pricing a *hike*.
   Precision here changes the whole explanation.
2. **Check whether the asset is even doing the thing the premise says.** A 2% bounce inside a
   three-week range is not a contradiction of anything; the Sep 3 +5% leg happened when Waller
   hinted at *holding* (hike odds fell), and the give-back happened when CPI pushed hike odds back
   up. The asset was tracking rate *expectations* the whole time.
3. **Then the real drivers of that day**, each checkable: an idiosyncratic catalyst (a Senate vote on
   crypto market-structure legislation), a **flow** story (spot-BTC ETF net inflows, incl. a
   single-day record), a **cross-asset divergence** (BTC up while Nasdaq futures −1.65%, gold down,
   crude +4%), and the standing structural ones.
4. **Structural reasons an asset can rise while hikes are priced**: hikes driven by growth and
   inflation are not the same as cuts driven by stress (cuts often arrive *with* the drawdown); what
   the market trades is the **change in odds**, not their level; the marginal buyer may be a flow
   (ETF/treasury demand) that ignores the policy rate; fiscal/debasement demand can lift hard assets
   regardless of direction; and a regulatory catalyst can outrun macro for a day.

## 4. Reporting shape that works

- **Odds table** (scenario → probability → source/venue), timestamped, with the resolution date.
- **The realized price path** for the asset in question (a short table of daily closes) so the user
  can see whether the premise matches reality.
- **Drivers as a ranked list**, each tagged as measured vs structural vs unverifiable.
- **An explicit "what I could not pull"** line (feed rate-limited, no volume, thin market).
- Keep it short and concrete; this user reads numbers, not prose about them.

## Pitfalls

- **Stale odds are worse than no odds.** Prediction markets move within minutes of a CPI print or a
  Fed speech — always fetch live in the same turn you answer, and print the fetch time.
- **Never quote a probability from a news article as if it were current**; use it only as the dated
  cross-check it is (and prefer the primary venue).
- **A summary table in the user's own words can be inverted** ("rate cut probability is low") — the
  first job is to establish what the market is actually pricing, then answer.
- Don't confuse "P(nothing happens)" with "P(the event I asked about)" — bucket layout differs per
  event and the "No change" market is often the largest one.
- If the question is about the user's own trading, connect it to the engine state only after the
  market facts are on the table (e.g. a scheduled FOMC window is already an entry blackout in
  FlowMetrix — check `data/news_blackout.json` before telling them to pause anything).
