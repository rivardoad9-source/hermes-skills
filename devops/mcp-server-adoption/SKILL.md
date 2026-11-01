---
name: mcp-server-adoption
description: "Use when adopting an external MCP server or agent CLI."
---

# Adopting an external MCP server / agent CLI into Hermes

Trigger: the user drops a repo or a tool and asks *"apakah ini bagus buat di-apply ke kita?"*, or wants an
external tool plugged into Hermes. This is a different class from general repo vetting (`external-repo-vetting`
covers library/strategy repos, upstream diffing, token/on-chain checks — read it too). Here the question is:
**does this thing actually run on our host, can it attach to Hermes, and what will it cost us per session?**

## 1. Run the binary before reading anything else

```bash
npx -y <pkg>@latest --version ; npx -y <pkg>@latest --help | head -80
```

Count the command surface. Agent-oriented repos usually ship a CLI **and** an MCP server; the MCP tools are
what our agent would actually use.

## 2. Readiness gate — which providers are ALIVE on this host

```bash
npx -y <pkg>@latest doctor --json       > /tmp/doctor.json
npx -y <pkg>@latest capabilities --json | head -c 1500
```

Never promise a capability before this. Typical findings: native engines (ghidra / hopper / ida) `not configured`,
macOS-only paths returning `unsupported_host`, some providers healthy with **zero** engines installed (static
analysis paths). An audit-wide `healthy:false` is often normal — read `scope_checks` / `capabilities` entries
instead of the headline flag, and report the dead providers explicitly rather than silently skipping them.

## 3. Probe the MCP handshake ourselves (evidence, not README)

```bash
python3 scripts/mcp_handshake_probe.py npx -y <pkg>@<exact-version> mcp
```

Prints `initialize ok`, `serverInfo`, protocolVersion and the **runtime** tool list. Marketing numbers drift
from reality (a repo advertising a 131-tool catalog advertised 125 at runtime) — quote the runtime number.
Pin one exact version for any persistent registration; `@latest` on every launch makes the tool a moving target.

## 4. Wire it into Hermes — and narrow it

```bash
hermes mcp list                                  # what's already attached
hermes mcp catalog | grep -i <name>              # is it one-click installable?
hermes mcp add <name> --command <cmd> --args <args...>
hermes mcp test <name>                           # verify the connection
hermes mcp configure <name>                      # toggle which tools are exposed
```

**Always recommend the subset.** Every advertised tool is schema the agent pays for in *every future session*;
125 tools for one occasional use case is a bad trade. Pick the handful tied to the actual use case.

## 5. Run one real job end-to-end (smallest sensible target first)

The whole point is executed evidence. Order matters on a small host:

```bash
free -m                                     # headroom BEFORE anything heavy
TARGET=<smallest interesting target>         # 12 MB target worked; a 5 MB target OOM'd at a 1 GB heap
NODE_OPTIONS=--max-old-space-size=1400 <cmd> --json > /tmp/out.json 2>/tmp/out.err
jq -r 'keys_unsorted' /tmp/out.json; jq -r '.normalized_result.statistics' /tmp/out.json
```

Analysis tools emit enormous evidence payloads (67 MB JSON for a 12 MB target) — always to a file, always
summarise with `jq`, and prefer the tool's own `--filter-output key.path` / `--token-limit` when an agent
consumes the result. Never pipe a long analysis through `head`/`tail` (it masks the exit code) and don't rely
on piped output for progress — poll the process instead.

## 6. Ground-truth the accuracy before trusting it on an unknown target

Run it against something whose contents you already know (your own site, your own artifact) and compare its
findings with reality. "0 endpoints" on a page you know has none, reported alongside limitations instead of
guesses, is a *positive* accuracy signal — say so. If findings contradict known reality, that is the headline
finding of the whole evaluation.

## 7. Host safety (this box also serves live systems)

Heavy analyses must not run on the box that runs the production engine/gateway: a 5 MB target OOM-crashed at
the default 1 GB heap on a 1.9 GB host. Check `free -m` and swap first, start with the smallest target, raise
the heap only with real headroom, and prefer running the tool on the user's own machine with Hermes attached
over MCP if the workload is big. Clean up afterwards (kill the browser/server you spawned, delete the giant
evidence files, remove temp profiles) and **show** the box is clean (`ps -eo pcpu,rss`, `free -m`) — never
leave processes hanging on a production host.

## 8. Verdict shape (Indonesian, casual, decision-ready)

1. **Verdict first** — worth it / worth it only for one narrow job / skip.
2. What it IS (one line + license, stars, activity, who maintains it).
3. **What we proved by running it** — every claim with a real number.
4. What is **blocked or missing** (engines, runtimes, host limits) — as `capability_unavailable`-style facts
   plus the exact remediation, never as "the tool is broken".
5. Use cases **and explicit NOT-use-cases** for our lanes.
6. Supply-chain read: license, telemetry/analytics greps, install hooks, outbound URLs, optional downloads.
7. Cheapest reversible next step (register MCP with a subset / install the skill) with its cost stated
   (context per session) — then let the user decide. End with the decision, not with "mau gw buatkan?".

## Pitfalls

- Don't judge from the README, and don't let the README's tool count stand in for the runtime count.
- `capability_unavailable` + `remediation` is a *quality* signal: report it as the boundary plus what to
  install. Do not install JREs, engines, or system packages on the live box without asking.
- `pkill -f "chrome-headless"` also kills the shell running it (the pattern matches its own command line) —
  use `pkill -f "chrome[-]headless"`.
- Cloudflare-protected sites ("Just a moment…") cannot be captured by a plain headless browser; that is a
  target limitation, not tool breakage.
- If the user already owns a repo-vetting skill, put the *repo* learnings there and keep this skill focused on
  adoption mechanics (readiness, wiring, subset, cost).
- Support file: `references/rea-adoption-case.md` — a full worked case with real numbers and commands.
