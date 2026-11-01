# Measuring outcomes of our OWN signal systems (labels, joins, thresholds)

Ladder step 10 in SKILL.md says: run the same harness on our own calls. This is the detail
for that step — the rules that keep a self-scorecard from turning into a self-congratulation
machine. All of it comes from a concrete deep dive (28 Sep 2026, low-cap call ledger,
103 outcome rows / 30 calls) where every rule below caught a real error.

## 1. Record the decision-time features, or the question is unanswerable

"Which features separate the winners?" cannot be answered after the fact: reconstructing a
token's state post-hoc is biased and usually impossible. Fix it at the source — the row of
data you already fetched to make the decision gets written to a features file
(`ew_features.jsonl`, ~50-60 fields) with **zero extra API calls**. If a needed field isn't
in that row, add it to the row.

## 2. Honest labels — never a vendor's lifetime ATH

Vendor "all-time high" is **not** the outcome of your call. It is the token's peak since
birth, i.e. mostly *before* you acted.

- Worked example of the trap: token called at MC $16, vendor `ath_mc` implied "peak x14,104"
  → the reported "average peak" became **x489**. Useless number, produced by one dead token.
- Correct label: the **measured peak at your own checkpoints** inside a bounded horizon
  (max multiple over +15m/+30m/+1h/+4h). Discard checkpoints beyond the horizon — after
  that it is market decay, not your call.
- Use **median, not mean**, for peaks; and report **peak AND current state** (a token at
  `x11.6` but −96.9% from its peak must not be labelled "alive").
- Percentages of winners and losers must **sum to 100%** (loss% = `100 − win%`; two separate
  floor divisions produced a scorecard that added to 99% and destroyed its credibility).
- Sanity check that answers "are we early or late?": compare ATH at the **first** checkpoint
  with ATH at the **last** one. Ratio ≈1.00 across the sample means the pump happened
  *before* you entered — an entry-timing problem that no exit rule can patch.

## 3. Join by natural key, not timestamp

Two writers calling `now_iso()` milliseconds apart produce timestamps that never match →
the join silently returns zero rows. Join by the natural id (`address`, lowercased), first
occurrence wins.

Then verify the **real key names** on one raw line (`head -1 file`) before writing the
parser: the outcome ledger used `horizon`, the study read `horizon_h`, and 103 result rows
collapsed to 0 with an empty report and no error. Support both names with a fallback, and
add a regression test naming the real key.

## 4. No conclusions below the n-guard

- ≥8 samples per group before a feature is even discussed; otherwise write "not enough data"
  rather than manufacturing a criterion.
- Call something a "candidate criterion" only past a stated effect size (median differs ≥30%,
  or binary rate differs ≥25 percentage points), and label it a hypothesis.
- **"No candidate criteria yet" is a valid, publishable answer.** 30 calls with 2 winners has
  no statistical power — the honest report says so. An instrument that starts reporting as
  soon as data arrives is the deliverable; conclusions are not.

## 5. Sparse checkpoints understate the upside

With only 4 checkpoints, a spike that pumps and dumps *between* samples is invisible: in the
worked case 20/30 tokens reached a ≥1.5x ATH but only **1/30** ever showed ≥1.5x at a
checkpoint. Consequence: do not simulate exit rules (trailing stop, laddered TP) on sparse
checkpoints — measure dense first (record every cron tick while the position is young), then
simulate. Similarly, "median −28% fifteen minutes after the call" is what tells you the
problem is entry timing, before spending any effort on exit logic.

## 6. Keep the full list reproducible when you trim the message

Trimming what gets *sent* (5 most recent calls + a TOTAL block) is fine; hiding data is not.
Requirements: a `--full` mode, an on-demand report, and raw ledgers. The TOTAL must be
computed over **all** measured calls, not just the rows that fit in the message — a total
that cannot be reproduced from the ledger is a lying report. When a trimmed card shows "last
5", choose them by recency of the call, never by which ones made money.

## 7. Compare cohorts with the n attached

Per-lane medians are worth reporting only alongside n and an explicit caveat
("n small, not a policy input"): e.g. big-cap lane median ≈1.0x (n=6) vs micro-cap lane
≈0.60x (n=22) — directionally interesting, not decisive.

## 8. Every new pipeline gets logged into the SAME ledger

The moment a new source (wallet-following lane, second scanner) is added, its calls go into
the shared call ledger so it is measured by the identical yardstick. A source that skips
the ledger can never lose, and will eventually be trusted for the wrong reason.
