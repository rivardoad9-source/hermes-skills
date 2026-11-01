# Case: adopting `morluto/rea` (reverse-engineering MCP toolkit) — 7 Okt 2026

Worked example of this skill end to end. Repo: https://github.com/morluto/rea · npm `rea-agents@4.1.0` ·
MIT · TypeScript · homepage morluto.github.io/rea ·
GitHub API: 11.994 ⭐ · 1.283 fork · created 2026-04-14 · pushed the same day it was vetted · 185 commits
(`--depth 50`) · 24 MB (src 16 MB / tests 3,2 MB / docs 2 MB / scripts 1,3 MB / bridge 296 KB / skills 48 KB).
5 third-party submodules (binwalk, unblob, jadx-headless-mcp, ghidra-nativeaot, wakaru) — not vendored, so not
a copy-paste repo.

Supply-chain read: no telemetry/analytics (grepped `telemetry|analytics|sentry|posthog` — only internal
comments plus `DOTNET_CLI_TELEMETRY_OPTOUT=1` in its own test scripts), no `postinstall` (only a husky
`prepare`), outbound URLs in src limited to json-schema.org and www.hopperapp.com, and `install.sh` only
resolves a GitHub release while Hopper stays an explicitly consented optional download.

## What running it produced

- `--version` → `4.1.0`; `--help` → **~70 subcommands** (analyze / decompile / trace / inspect / compare /
  capture / evidence-export …).
- `doctor --json` → `healthy:false`, and the detail matters: node 26.7 ✓ · host ubuntu 24.04 ✓ · `hopper` ❌ ·
  `ghidra` ❌ (`GHIDRA_INSTALL_DIR` unset) · `ida-registration` ❌ · `skill:identity` ❌ (no agent registration
  it recognizes; Hermes is not one of its supported clients).
- `capabilities --json` → live providers `rea-artifact-graph`, `rea-dotnet-static`; dead ghidra/hopper/ida;
  `capture_native_ui_scenario` → `unsupported_host` ("Native macOS utilities require macOS").
- **Static JavaScript needs no engine** — the key to the whole verdict:
  `analyze-javascript-application /…/systray2 --json` (12 MB target, `NODE_OPTIONS=--max-old-space-size=1400`)
  → exit 0, **67 MB** evidence JSON: 50 relevant files · 42 JS files parsed · **17.424 AST nodes** · 308 findings
  · 0 parse failures · graph = 42 javascript-asset + 9 artifact + 6 electron-main + 1 electron-renderer + 1 endpoint.
  Its own stated limitation: *"JavaScript and HTML were parsed as inert text; bundle bootstrap code was never
  executed."* → findings are static, never runtime proof.
- 5 MB target (`gmgn-cli`, a big browser bundle) → **OOM crash** at the default 1 GB heap
  (`FATAL ERROR: Ineffective mark-compacts near heap limit`). Host at the time: 1,9 GB RAM, 875 MB swap used.
- **Web** — requires its own loopback CDP browser (`list-browser-targets <endpoint>` then
  `analyze-web-bundle <endpoint> <target_id>`):
  - `lynk.id/…` → target showed only `Just a moment...` plus a `challenges.cloudflare.com` iframe →
    **Cloudflare blocks plain headless** (target limitation, not tool breakage).
  - `zemizdigital.vercel.app` (our own site, chosen on purpose to ground-truth accuracy) → 1 script (8.208 B,
    sha256), 1.130 AST nodes, **0 endpoints**, completeness `complete`, confidence `observed` → matched reality
    (static page, small inline JS, no API calls). It reports unknowns instead of guessing.
- **APK**: `inspect-android-package app.apk` (real 12,5 MB F-Droid APK) →
  `{"code":"capability_unavailable","details":{"provider_id":"jadx","reason":"Set REA_JADX_MCP_JAR to the
  absolute path of a caller-supplied jadx-headless-mcp 0.7.1 JAR. REA does not download or install it."}}`.
  Host had no Java (`java: command not found`) → the APK path needs Java + the jadx JAR first.
- **MCP**: `npx -y rea-agents@4.1.0 mcp` → handshake OK, `serverInfo {name: rea, version: 4.1.0}`,
  protocolVersion `2024-11-05`, **125 tools at runtime** (catalog/README claims 131 → npm release differs).
  `hermes mcp list` was empty and `hermes mcp catalog | grep -i rea` had no entry → manual registration:
  `hermes mcp add rea --command npx --args -y rea-agents@4.1.0 mcp`.

## Verdict delivered

Worth it, but only for one narrow job, stated explicitly: **"third-party artifacts before we trust them"** —
breaking open someone else's tool/app/web bundle (endpoints + graph) instead of trusting their claims. Explicit
NOT-use-cases: the trading engine (Python + EVM on-chain, a different world), content/video, Threads. Do not
install native engines on the live box; do not run big-bundle analysis on the box that also serves the
production engine. Recommended cheapest reversible step: register the MCP server with only the JS/web tools
enabled, plus its bundled skill — with the per-session context cost stated.

## Transferable lessons

- Evidence payloads are huge (67 MB for a 12 MB target) → save to file, summarise with `jq`, use filter flags.
- `capabilities`/`doctor` first, before promising APK/native capability to the user.
- Raise the heap with `NODE_OPTIONS=--max-old-space-size=…` only after checking `free -m`.
- `pkill -f "chrome-headless"` kills its own shell (the pattern matches the shell command line) → use
  `pkill -f "chrome[-]headless"`.
- Driving a headless browser for CDP capture: `--headless=new --no-sandbox --disable-gpu
  --disable-dev-shm-usage --remote-debugging-port=… --user-data-dir=…` (Playwright chromium lives at
  `~/.cache/ms-playwright/chromium-*/chrome-linux64/chrome`).
- Clean up afterwards and prove it: kill the browser/server you spawned, delete giant evidence files and temp
  profiles, then show `ps -eo pcpu,rss` + `free -m` — leave nothing hanging on a production host.
