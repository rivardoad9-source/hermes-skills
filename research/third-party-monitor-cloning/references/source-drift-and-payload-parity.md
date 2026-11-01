# Source drift & payload parity — "kok datanya beda?"

Worked example: **bizyugoscan.com** (Hyperliquid whale tracker, 54 wallets) vs our local
ZemizTracker board. Symptom: user compared the source's numbers to ours and they didn't match.

```
theirs (live 18:21) : 54 wallets · $2.460B · long 57.70% · ETH $1025M/68.2% · BTC $598M/58.8%
ours   (live 18:27) : 54 wallets · $2.313B · long 54.98% · ETH  $876M/62.8% · BTC $615M/60.0%
```

Same source API, same maths — the gap was **wallet-list membership**, because the source
**rotates its 54-wallet list**. Our config was a frozen copy taken hours earlier.

## Rule of thumb: never attribute a gap to methodology before checking list membership

Three candidate causes, cheapest to test first:

| Cause | Test | Verdict this session |
|---|---|---|
| **Snapshot lag** (their push intervals / delayed data) | compare their `lastPush`/`updatedAt` against our snapshot ts | 6 min apart → not it |
| **Methodology** (floor, spot vs perp, field used) | re-sum THEIR raw payload; recompute OUR agg with variants | identical maths → not it |
| **List membership** (their config rotates) | set-diff the two wallet lists + notional per side | **this was it** |

Then the identity check that proves it:
`their_total − our_total ≈ Σ(only-theirs notional) − Σ(only-ours notional)`
Here: 2460 − 2313 = +$147M; only-theirs +$181.4M, only-ours −$32.4M → +$149M. Match.

## 1. Extract the source's embedded payload (Next.js / RSC)

The rendered page text only gives rounded display values. The **exact aggregates** — and, on this
site, every whale's per-position notional — sit in the self-streamed RSC payload
(`self.__next_f.push([1, "...escaped JSON..."])`). That payload is the ground truth for parity and
for re-deriving their method.

```python
import json, urllib.request

req = urllib.request.Request("https://bizyugoscan.com/", headers={"User-Agent": "Mozilla/5.0"})
html = urllib.request.urlopen(req, timeout=30).read().decode("utf-8", "replace")

u = html.replace('\\\\"', '"').replace('\\"', '"')   # unescape RSC-escaped quotes first
i = u.find('"initial":')                             # the payload root key on this site
j = u.find("{", i)

depth = 0; instr = esc = False; end = None            # brace matcher that respects strings
for k in range(j, len(u)):
    c = u[k]
    if instr:
        if esc: esc = False
        elif c == "\\": esc = True
        elif c == '"': instr = False
    else:
        if c == '"': instr = True
        elif c == "{": depth += 1
        elif c == "}":
            depth -= 1
            if depth == 0: end = k + 1; break

d = json.loads(u[j:end])
```

- **Do not use a non-greedy regex** (`{"initial":.*?}`) — nested objects and braces inside strings
  will truncate or corrupt it. Always brace-match with string awareness.
- If `"initial":` isn't found, grep the raw HTML for the largest `\"{` blob or for
  `__next_f.push` and dump the unescaped text to a file, then look for the known key names.
- Alternative when the payload isn't in HTML: check `/_next/data/*.json` and the chunk files
  referenced in `<script src>`.

Payload shape (bizyugoscan):

```
walletCount, totalNotional, pctLongByNotional, lastPush (ISO UTC)
coins[]  : {coin, longNotional, shortNotional, netNotional, whalesLong, whalesShort}
wallets[]: {id, alias, address, accountValue, updatedAt,
            positions[]: {coin, side, size, entryPx, notional, upnl, leverage}}
```

## 2. Prove method identity by re-summing their raw positions

```python
tot = 0.0; per = {}
for w in d["wallets"]:
    for p in w["positions"]:
        n = abs(float(p["notional"]))
        tot += n
        per.setdefault(p["coin"], {"L": 0.0, "S": 0.0})["L" if p["side"] == "long" else "S"] += n
# bizyugoscan: sum == their totalNotional exactly  → perp positions only, NO size floor, same list
```

Their `coins[]` block equals the per-coin sum of the same raw positions → the headline and the
breakdown come from one aggregation. Now do the same for ours and diff per wallet:

```python
only_theirs = [a for a in theirs_set if a not in ours_set]
only_ours   = [a for a in ours_set   if a not in theirs_set]
# print notional + per-coin split for each, then re-aggregate restricted to the common set
```

Result here: 50/54 common; in +4 (Whale #72 $111.9M — **$111.9M of it a single ETH long**, #74
$29.9M, #73 $27.1M, #35 $12.5M), out −4 (#65 $32.4M + three idle $0 wallets).

## 3. Variant testing to rule methodology in/out (cheap, decisive)

Recompute **our own** aggregation under variations before blaming the source:

| Variant | Total | Long % |
|---|---|---|
| floor $100K, perp only (ours) | $2.311B | 55.0 |
| floor $50K, perp only | $2.311B | 55.0 |
| floor $0, perp only | $2.312B | 55.0 |
| floor $0, perp + spot coin units priced at `allMids` | $2.473B | 57.9 |

**Trap learned:** variant 4 landed within 0.5% of the source's headline ($2.46B / 57.6%) and looked
like the answer — it was a **coincidence** (spot was almost all HYPE, ~$161M, which would have lifted
their HYPE row to 63.9% long; their HYPE read 45.8%, matching our perp-only 43.4%). Always check the
**per-coin rows**, not just the headline total/bias, before declaring a methodology match.

Also checked and cleared: sub-accounts (0 of 54 had any), equity-sum vs notional-sum ($0.483B ≠
$2.46B), so neither explains the gap.

## 4. Fix the root cause: mirror the list, don't freeze it

`~/.hermes/scripts/whale_sync.py` (pattern):

1. `fetch_wallets()` — pull the source payload, return `[{label, addr}]`, raise if empty (an empty
   fetch must never wipe the config).
2. Load our config, compare address sets (lowercased), compute `added` / `removed`.
3. **No change → print nothing, exit 0** (silent tick, no LLM, no spam).
4. Change → `shutil.copy(CONFIG, CONFIG.replace('.json', '.bak.json'))`, then write the new list
   while **preserving all our own keys** (thresholds, watchlist, notes); stamp `synced_at`.
5. Print a short delta card (who in / who out) — that stdout IS the cron message.
6. Fetch failure → exit non-zero so a broken sync alerts instead of dying silently.

Registered as `no_agent=true` cron, `0 */6 * * *`, `deliver: origin`, script-only
(see `hermes-cron-automation`). The running server re-reads the config on each scan, so no restart
was needed — verify by hitting the refresh route and re-reading the board.

Post-fix parity (7 min apart):

```
ours   : $2.464B · long 57.70% · ETH $1027M/68.3% · BTC $599M/58.8% · HYPE $293M/45.8%
theirs : $2.460B · long 57.70% · ETH $1025M/68.2% · BTC $598M/58.8% · HYPE $292M/45.8%
```

## 5. Report shape the user accepted

Plain-language root cause, the evidence, the exact wallets swapped, then the fix and its verification
number. No hedging, no "mungkin" — the diagnosis was proven by re-summing the source's own payload,
and that is what made it credible. Keep the "a few 0.1 residue = delay, not error" caveat.
