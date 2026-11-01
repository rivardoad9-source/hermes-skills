# Release-hour reaction base rates: FOMC minutes vs decision, and the "priced in" test

Measured 7 Okt 2026 with `scripts/release_reaction_study.py` (Binance 1h klines, base = open of the
release-hour candle; FOMC releases 18:00 UTC = 01:00 WIB). Reproduce with the script before quoting —
extend the year's sets as releases happen. **Small n: always print the n when you use these.**

## 1. Raw rows

FOMC **minutes** 2026 (n=5):

| Release | +1h | +4h | +24h | range 1 jam |
|---|---|---|---|---|
| 18 Feb 2026 | −1,50% | −1,16% | −0,23% | 1,53% |
| 8 Apr 2026 | −0,79% | −1,15% | 0,00% | 1,12% |
| 20 Mei 2026 | +0,13% | −0,08% | −0,23% | 0,30% |
| 8 Jul 2026 | +0,28% | +0,36% | +1,79% | 0,49% |
| 19 Agt 2026 | +0,34% | +1,56% | **+6,21%** | 0,60% |

FOMC **decisions** 2026 (n=3): 18 Mar −0,73 / −0,62 / −2,48% · 17 Jun −2,73 / −2,73 / **−5,14%** ·
16 Sep +0,41 / −0,12 / +1,06%.

Control — ordinary hours, same clock, no release (n=5): 3 Mar +0,17 / +0,01 / +7,87% · 14 Jul −0,08 /
+0,37 / +0,37% · 25 Agt −0,40 / −0,44 / −0,97% · 22 Sep −0,44 / −0,52 / −2,59% · 29 Sep +0,62 / +0,64
/ +1,05%.

## 2. Summary

| Class | n | mean \|+1h\| | mean \|+4h\| | mean \|+24h\| | mean 1h range | direction 24h |
|---|---|---|---|---|---|---|
| minutes | 5 | 0,61% | 0,86% | 1,69% | 0,81% | 2 up / 2 down / 1 flat (40% hit) |
| decision | 3 | 1,29% | 1,16% | 2,89% | 1,81% | 1 up / 2 down (67% hit) |
| ordinary hour | 5 | 0,34% | 0,40% | 2,57% | 0,66% | — |

Readings that survived scrutiny:

- **Decision ≈ 1,7x minutes at 24 jam.** A minutes night is a *smaller* event than the meeting it
  documents; say so up front rather than letting the user brace for a decision-sized move.
- **A minutes release hour is not more volatile than an ordinary hour** (0,81% vs 0,66% = +0,15 pts).
  The loudest ordinary hour sampled (1,37%) nearly matches the loudest minutes hour (1,53%).
  So "impact-nya nggak ngaruh" is usually right — and provable, which is what this user wants.
- **Direction has no edge on either class** (hit rate at or below coin). Do not sell a direction call
  off this table; sell magnitude + levels.

## 3. The "harganya udah price in" test

The claim is checkable, so check it instead of debating it:

1. Run `release_reaction_study.py` for that event class → realized |move| at 1h/4h/24h.
2. Run `price_ladder_distribution.py` for that date → market-implied **IQR half-width**.
   Realized inside the band ⇒ the market's own range already contained the move: claim survives.
   Realized breaks the band ⇒ the print added information: claim fails.
3. Hand back a falsifiable line so tomorrow settles it: *"kalau besok BTC masih di band $82,5–85k,
   lu menang argumen"* — market priced ≈60% for that band (8 Okt 2026 ladder).

Worked, both directions:
- **Priced in (claim survives):** 16 Sep 2026 decision, hike priced **88,5%**, vote 12-0 unanimous →
  BTC +0,41 / −0,12 / +1,06%. Consensus at that level buys the *absence* of a reaction.
- **Not priced (claim fails):** 17 Jun 2026 decision → −5,14% at 24h. Least-anticipated meeting of the
  three, biggest move.

## 4. Caveats to state when quoting this

- n=5 / n=3 / n=5 — one outlier (19 Agt +6,21% at 24h) drags the minutes mean; 24h magnitude on
  minutes is **median 0,23%**, which is closer to the truth of a typical night.
- Single venue (Binance spot BTCUSDT), single asset. ETH/alt reactions are typically a multiple of BTC's.
- The 24h window captures *whatever else happened that day*, not only the release — that is why the
  ordinary-hour control exists, and why a big 24h print needs its own driver checked before it is
  credited to the Fed.
- Attribution discipline: separate the scheduled event from the day's real driver. On 7 Okt 2026 the
  −3,1% move (high $86.699 → low $83.442) happened *before* the minutes, driven by Hormuz tanker
  attacks (Brent $101,63) and 10Y at 5,307%.
