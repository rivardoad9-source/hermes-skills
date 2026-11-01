---
name: mcp-server-integration
description: Use when judging or wiring an MCP server into Hermes.
---

# Integrating (or rejecting) an MCP server / agent toolkit

Trigger: user drops a repo or npm package that ships an MCP server ("pelajari ini,
bagus nggak buat kita apply?") or asks to hook a new tool into Hermes. Also fires when
the user hands over a remote MCP endpoint (a URL plus its llms.txt) and asks you to
connect it — for that shape skip straight to §4b. Also fires when the ask is judgment
rather than wiring: "is there a plugin/skill that makes you stronger?", or a
pasted tweet/thread of agent frameworks — see
`references/hermes-plugin-catalog-evaluation.md`. Goal: a verdict backed by
measurements, then the cheapest reversible wiring step.

## 1. Inventory what it really is (measured, not quoted)
- `<cli> --version` + `<cli> --help` → real subcommand count. README badges drift.
- `<cli> doctor --json` and `<cli> capabilities --json` → per-provider
  `available` vs `unsupported_host` **on this host**. A capability that is off is
  usually a missing engine/OS, not a bad repo — separate "capability missing" from
  "workflow missing" before writing the verdict.
- Note which subset works with zero extra installs (often the static/analysis part).

## 2. Prove it with one real run
Run the cheapest real command against a small LOCAL target and record numbers
(files scanned / parsed / nodes / findings / explicit limitations). That is the
evidence; the README is not.

## 3. Measure the MCP surface before trusting the catalog
```bash
python3 scripts/mcp_stdio_probe.py --grep javascript,web,artifact -- npx -y <pkg>@<ver> mcp
```
Prints `serverInfo`, protocolVersion, the real advertised tool count and the tools
matching your lane. README/catalog numbers drift from runtime (seen: catalog 131 vs
125 advertised) — quote the measured number.

## 4. Decide scope, then wire it
- Every registered tool costs context in every session. Register, then subset:
  `hermes mcp add <name> --command <cmd> --args <args...>` → `hermes mcp configure`
  (toggle which tools load) → verify with `hermes mcp list` and `hermes mcp test`.
- Check `hermes mcp catalog` first; a curated entry is a one-liner install.
- Prefer a pinned exact version in the registration for reproducibility.

## 4b. Remote HTTP MCP with OAuth on a headless host
When the server is a URL and the sign-in happens in a browser, `hermes mcp add <name>
--url <url> --auth oauth` is NOT enough on a gateway/VPS box: with no TTY it fails to
build the OAuth provider and saves the entry with **no `auth` key and `enabled: false`**.
Repair it with config sets instead of re-running add:
```bash
hermes config set mcp_servers.<name>.auth oauth
hermes config set mcp_servers.<name>.enabled true
hermes config set mcp_servers.<name>.oauth.timeout 1800   # callback window, default 300 s
hermes config get mcp_servers.<name>                       # confirm the keys landed
```
Then run the login in a **PTY background** session, harvest the authorization URL from
its output, hand that URL to the user in chat, and submit the redirect URL they paste
back into the same waiting process:
```
terminal(command="hermes mcp login <name>", pty=true, background=true)   # then poll for the URL
process_manage(action="submit", session_id=…, data="<redirect URL the user sent>")
```
Check `/.well-known/oauth-authorization-server` first: a `device_authorization_endpoint`
means `hermes mcp login <name> --flow device` is the low-friction path and you never need
the callback. Full recipe, discovery checks, timeout maths and consent/scope rules:
`references/remote-oauth-mcp-headless.md`.

## 5. Resource + supply-chain guardrails (this is where verdicts flip)
- `free -h` + swap BEFORE any analysis. A big bundle OOMs the tool at the default
  ~1GB heap: retry with `NODE_OPTIONS=--max-old-space-size=<n>`.
- If the host also runs live services (trading engine, gateway, cron), heavy
  analysis there can starve them → recommendation becomes "run it off-box, connect
  over remote MCP" instead of local install.
- Output volume: evidence dumps hit tens of MB (67MB JSON for a 12MB app) → always
  `--filter-output` / `--token-limit` when the output feeds an agent's context.
- Before installing: `jq '.scripts' package.json` for `postinstall|preinstall|prepare`,
  grep for `telemetry|analytics|sentry|posthog|mixpanel`, list outbound domains in
  `src/`, read `install.sh` (what it downloads, whether it asks consent), count
  vendored submodules. Those are the real risk surface, not the license.

## 6. Report shape
Verdict first and specific ("worth it for lane X, useless for Y, don't run it on
this box because Z"), then measured evidence, then honest limits, then the reversible
step you recommend. Never say "good repo" without naming a lane it serves.

## Pitfalls
- Don't judge capability by absent engines — say which workflows still work.
- `pkill -f "<pattern>"` matches the shell running the command (self-kill, exit -15).
  Use the bracket trick: `pkill -f "chrome[-]headless"`.
- Long inline one-liners (grep+jq+curl chained) get blocked by the parser → write a
  script file and run that.
- Killing a render/analysis parent leaves orphaned children (e.g. `chrome-headless`)
  eating CPU — clean them up before the next run.
- Set `oauth.timeout` BEFORE starting an interactive login: the flow's bound is
  `max(connect_timeout, oauth.timeout + 15)` read at flow start, so raising it while a
  flow is already waiting changes nothing — kill and restart the login instead.
- Two login flows for the same server cannot coexist: the second fails with "callback
  port already in use". Kill the waiting pty session before retrying.
- `hermes mcp add` is misleading on a headless host (prompts "Save config anyway?" then
  saves a broken, disabled entry). Always `hermes config get mcp_servers.<name>` right
  after adding to confirm `auth` and `enabled` are actually present.
- Never hand-edit or patch `~/.hermes/config.yaml` for any of this: the write is refused
  by the tooling, and `hermes config set <dotted.key> <value>` handles nested keys too.

## Support files
- `scripts/mcp_stdio_probe.py` — stdio handshake + real tool inventory for any MCP server.
- `references/remote-oauth-mcp-headless.md` — registering, authorizing and verifying a
  remote HTTP MCP server with OAuth when the user signs in from their own browser.
- `references/hermes-plugin-catalog-evaluation.md` — judging a plugin or a list of
  frameworks instead of an MCP server: `hermes plugins search --json` (whole catalog),
  shelf filtering by the user's surface, and the framework-list trap.
- `references/hermes-plugin-install-verification.md` — after the verdict: non-interactive
  `hermes plugins install --enable --yes-deps`, telling enabled from live (log grep, not
  `hermes gateway status`), the per-plugin proof for memory-rewind / memory-shield /
  skill-retrieval / toolaria, and their traps (terminal is never rescued; BM25 misses
  Indonesian queries until the skill carries `triggers:`).
