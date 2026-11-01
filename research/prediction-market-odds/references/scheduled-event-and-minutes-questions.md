# Scheduled-event questions ("news nanti malam, predict lu gmn") — and minutes ≠ decision

Worked 7 Okt 2026: asked ~6 hours before the FOMC **minutes** release, on a book that was −8 % and fully
alt-beta. Companion to `fed-decision-base-rate.md` (base rates) and `btc-price-ladder-implied-distribution.md`.

## 1. Confirm the event, its date AND its clock from the primary venue

- Fed's own month page — `federalreserve.gov/newsevents/<year>-<month>.htm` — lists the item explicitly
  ("FOMC Minutes — Meeting of September 15-16 — 7, 2:00 p.m."). Cross-check a year-at-a-glance schedule table.
- Conversion: **2:00 PM ET = 01:00 WIB the next day**. A wrong timestamp invalidates the whole answer; the
  user is planning around "nanti malam".
- **Minutes ≠ decision**: released ~3 weeks after the meeting, backward-looking, normally a *smaller* move
  than the decision itself. Say that before projecting anything, otherwise the framing oversells the event.

## 2. Answer shape for "predict lu gmn"

It is still a distribution answer, never a direction call:

1. **Bucket odds of the next decision** from Polymarket — pull every bucket (they must sum ~1). Worked:
   hold 82,5 % / hike25 16,5 % / cut25 0,4 % (fetched 18:53 WIB, per-bucket 24h vol $91k–261k).
2. **The daily strike ladder for the next 1–2 days** — median, IQR, P(> spot), P(> the liquidation cluster).
   Worked 8-Oct: median $83.606 vs spot $83.634 (−0,0 %), IQR $82.447–$84.971 (3,0 %), P(> spot) 49,4 %,
   P(> $86k) 7,5 % ⇒ "pasar bilang nggak kemana-mana".
3. **Base rates that kill the direction question** (our 24-combo event study = NO_EDGE_DETECTED; BTC fell 48 h
   after 7 of 8 2025 FOMC meetings) → then give scenario probabilities **explicitly labelled as your own
   judgment**, each with its driver.
4. **Levels on both sides**: liquidation clusters both ways (worked $82,6k below vs $87,4k above ⇒ the
   downside path is shorter), funding sign (negative = shorts crowded = squeeze fuel), ETF-flow direction
   (worked: −$89,9 M on 5 Okt, then +$118,8 M on 6 Okt).
5. Punchline shape that landed: *"arah 50:50, tapi risiko ada di sisi bawah"* + what it means for his own
   positions (which coin sits on which trigger level).

## 3. Honesty markers this user rewards

- Figures you could not fetch directly are **second-hand** — label them. Worked: 10Y 5,307 % and Brent
  $101,63 came via Reuters through a crypto outlet; Yahoo/stooq were unusable from this host that day.
- Separate **the day's actual driver** from the scheduled event: the 7 Oct dump came from Hormuz tanker
  attacks + yields near multi-decade highs, not from the Fed. Naming that gap is the value-add.

## 4. Handoff

If the follow-up message is a risk decision ("cut all position or biarin aja"), do not answer it from this
skill — go to `crypto-portfolio-advisory` → `references/pre-event-binary-risk-decisions.md` for the
four-option matrix and the recovery-math reframe.
