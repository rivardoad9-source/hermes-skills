# Understated work: verify project history from the project's own ledger

Companion to `references/honest-attribution-and-claims.md`. That file covers claims the user cannot
defend because they are too strong (§1 stack names, §2 self-rated levels). This file covers the
opposite direction — somebody's own shipped work described as **less** than it was — and the
verification that settles it.

## The correction (10 Oct 2026, second pass on the same CV)

The draft CV described a trading project as "a zero-capital paper-trading engine". The user:

> "yg flow metrix bukan cuma paper trading dan udh real jalan kok"

He was right. The engine had traded **live with real money** and the draft had under-sold his own
work, because one document (the repo README) said paper-only. Rule: never accept *or* dismiss a claim
about the user's own project from memory or from a single document. Go read the ledger.

## Where the truth lives (in order of authority)

| Source | What it proved |
|---|---|
| DB tables (`data/flowmetrix.db`): `live_execution_attempts`, `simulated_positions` | 15 live attempts from 11 Sep 2026; rows carry `execution_mode = LIVE`, `position_address`, `open_signature` / `close_signature`, `deposited_sol_lamports = 900000000` (0,9 SOL per position) |
| Repo-side export (`exports/trades.csv`) | 8 closed positions, engine v1.1, entry SOL ~$99-102 — the same repo whose README claimed no live code path |
| Handoff doc (`docs/HANDOFF-*-PAUSE-*.md`) | operator ledger: $288,27 → $314,91, **+$26,64 realised**, 8 trades, 75% win rate, 6,67% max DD, wallet drained at shutdown |
| Incident docs (`docs/incidents/*.md`) | real failures (≈$6,33 lost to failed live opens) — cite the failure side next to any win rate, or the line reads like marketing |

Quick probe pattern that found it (read-only, no engine access needed):

```python
import sqlite3
c = sqlite3.connect('data/flowmetrix.db')
for t in ('live_execution_attempts', 'simulated_positions'):
    cols = [r[1] for r in c.execute(f"pragma table_info({t})")]
    n = c.execute(f"select count(*) from {t}").fetchone()[0]
    print(t, n, cols)
```

`execution_mode`, `*_signature` and `wallet_lamports_before/after` columns are the giveaway: a
paper-only system has no signature columns to fill.

## The corrected line (numbers only from the ledger)

```
FlowMetrix — screener likuiditas Solana DLMM & mesin LP otomatis
Menyaring pool Meteora DLMM lalu membuka dan menutup posisi likuiditas otomatis dengan modal nyata di
Solana: 8 posisi ditutup, semuanya bertanda tangan on-chain, hasil tercatat +26,64 dolar dari modal
awal 288 dolar di buku engine. Ukuran posisi dan pagar risiko diatur lewat konfigurasi.
```

EN twin: *"Screens Meteora DLMM pools and opens and closes liquidity positions automatically: ran live
with real capital on Solana, 8 positions closed on-chain, +$26.64 realised on $288 starting capital."*

## One claim set, again

Propagate in the same pass to: CV ID, CV EN, profile README project table, Pages portfolio card, and —
after asking — the project's own README. Any surface left behind becomes the next contradiction the
user gets asked about.

## When a repo's README contradicts its own data

The README said "No real funds are ever deployed … live execution is not implemented" while
`exports/trades.csv` in the same repo listed live signatures and the code carried real signing
modules. Do not rewrite a public claim unilaterally:

1. Show both artefacts with paths, no lecture.
2. Offer options (fix honestly / leave the public claim / soften to a technical note) and let the
   user choose. He chose honesty.
3. Implement in a throwaway clone (`git clone` to `/tmp`, edit, commit, push) — never in a
   production/live worktree that an engine or cron depends on.
4. Write the fix as history **plus** current state, both checkable: "this baseline is paper-only" and
   "the deployed engine traded live in Sep 2026: 8 positions, +$26,64 on $288,27, stopped, capital
   withdrawn", citing the artefact paths, failures included.
5. Verify the rendered file, not the push response:
   `curl -s https://raw.githubusercontent.com/O/R/main/README.md | sed -n '1,20p'`.

## Page-budget trim order (verified)

Rewriting an understated bullet usually makes it longer. When the CV goes to 2 pages: drop stack
names from one-line project bullets, shorten project bullets and the italic note, and only then
tighten layout (`BODY leading` 11,6 → 11,1, `spaceAfter` 2 → 1,8, margins 1,05/0,9 → 1,0/0,8 cm).
Verified: back to exactly 1 page with every keyword intact, twice, in the same session.

Verification snippet (note the whitespace normalisation — a phrase wrapped across PDF lines still
extracts, but a raw `in` test on the unnormalised string fails):

```python
import pypdf, re
r = pypdf.PdfReader("CV_Rivardo_ID.pdf")
t = re.sub(r"\s+", " ", "".join(p.extract_text() for p in r.pages))
assert len(r.pages) == 1 and "+26,64" in t
```
