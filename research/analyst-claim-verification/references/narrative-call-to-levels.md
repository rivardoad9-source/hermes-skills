# From a narrative call to a levels-and-sizing answer (worked case: ALICE / GameFi, 29 Sep 2026)

Companion to the "Shape: the narrative call" section in SKILL.md. Trigger: the user sends a chart
screenshot plus a tip from someone they trust — *"secara technical X seksi bgt, dan gw dpt call dari
<mentor> katanya eyes on <narrative>"*. They are not asking for a verdict on the mentor. They are asking
**should I, where, and how big**. Deliver: theme verified or not (with numbers), ticker's rank inside the
theme, level map, R:R at market vs on a pullback, invalidation, size.

## What arrived

TradingView weekly screenshot, ALICE/USDT, 0,1714 (+8,07% at the moment of capture), EMA13/21/33/50/100/200
in the legend, plus an auxiliary vision read of the same image. The vision read quoted the *price axis*
numbers as if they were the EMA values (it "saw" EMA13 = 0,1733) — wrong by ~23%. Never quote indicator
values read off a screenshot.

## 1. Verify the theme as a basket (the claim was real)

Binance spot, 24h/7d/30d/90d pulled keyless (`api.binance.com/api/v3/klines?interval=1d&limit=400`) for
11 gaming proxies + BTC/ETH/SOL:

| bucket | 30d | 7d |
|---|---|---|
| median of the gaming basket (GALA, IMX, AXS, ILV, ALICE, MANA, ENJ, PIXEL, SAND, APE, MAGIC) | **+27,6%** | +2,4% |
| BTC | +7,9% | −2,8% |
| ETH | +12,3% | −1,5% |
| SOL | +18,4% | +1,5% |

All 11 proxies beat BTC at 30d ⇒ the rotation is a fact, not an opinion. Report the **median plus the
range** (worked: range +16,0% .. +42,5%) so the user sees dispersion, not just a headline.

## 2. Leader or passenger

ALICE 7d **+14,6% vs basket median +2,4%**, 24h +12,3% vs +3,6% ⇒ money is picking this ticker, not just
the sector. That distinction decides whether the tip is ticker-specific or just beta — say which.

## 3. Read the chart from fetched candles

Computed from weekly klines (limit 300, EMA on closes; a 300-bar window makes the seeding error
irrelevant):

| | value | price vs it |
|---|---|---|
| price | 0,1712 | — |
| EMA13w | 0,1406 | +21,8% above |
| EMA21w | 0,1400 | above |
| EMA33w | 0,1552 | above |
| EMA50w | 0,2035 | **−15,9% below** |
| EMA100w / EMA200w | 0,4968 / 1,8059 | −65% / −90,5% |
| RSI14 weekly / daily | 57,6 / 67,3 | room / stretched |
| dist from ATH | **−99,7%** ($60) | — |

Volume confirmed the breakout week (21 Sep: 9,88M vs 2,86M the prior week) and this week was still open
(4,12M on Tuesday). Framing that worked: *"reversal dari dasar, bukan uptrend"* — above the short weekly
stack, still under EMA50w.

## 4. Crowding check (tells you if it's "early" or "late")

Binance futures: funding **+0,005%/8h** (≈ +5,5%/yr), open interest 22,1M ALICE (~$3,8M), 24h vol $16M
futures / $3,4M spot. Mild funding + small OI ⇒ not crowded yet — both the opportunity and the warning
(a thin market inflates fast in both directions).

## 5. The level map and the R:R arithmetic (the actual answer)

| | level | why |
|---|---|---|
| resistance | 0,1750 → 0,1816 → 0,2035 | week high → Aug high → EMA50w |
| support | 0,1552 → 0,1456 → 0,1400 | EMA33w → prior week low → EMA13/21w cluster |

- At market 0,1710 with stop 0,1440: risk 15,8%, target 0,2035 = +19% ⇒ **1,2 : 1**.
- Pullback 0,1540–0,1570 with stop 0,1430: risk ~8% ⇒ +16% to first target = **1:2**, +30% to second = **1:3,8**.

That pair of numbers is what converts "seksi" into "don't chase; this is the entry". Invalidation:
weekly close below 0,1400 (a level, never "kalau jelek cut"). Sizing: high-beta theme sleeve 3–5% of the
portfolio, hard stop, no averaging down, with the liquidity sanity check (24h spot + futures volume vs
the intended order size).

## 6. What to split off as unverifiable

The theme was verified; the mentor's entry/stop/target cannot be. Ask for his invalidation level in one
line — a call without one is a hope. Keep the theme verdict and the trade plan as separate paragraphs so
a correct theme is never read as an endorsement of the entry price.

## Chart that carried it

Two panels: (A) weekly candles, log scale, 4 EMAs, dashed level lines with labels right-anchored in the
margin; (B) 30d performance bars, gaming green / majors grey / the named ticker highlighted, each bar
labelled with both 30d and 7d. Data-only labels (no "our engine" phrasing) — see `data-chart-images`.
