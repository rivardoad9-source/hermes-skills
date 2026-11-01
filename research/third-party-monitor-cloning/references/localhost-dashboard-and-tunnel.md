# Localhost dashboard + quick tunnel + watchdog (the recipe)

Phase 2 of a monitor clone: the CLI works, the user now wants "webnya / localhost yg bisa gw akses".
Validated on ZemizTracker (whale board, 54 Hyperliquid wallets, Oct 2026) — dashboards exposed to the
user's phone over a cloudflared quick tunnel, files under `~/.hermes/scripts/whale_board*.py|html`.

## 1. Server skeleton (stdlib only, no deps)

`~/.hermes/scripts/<tool>_server.py` — `ThreadingHTTPServer` + `BaseHTTPRequestHandler`.

```python
STATE = {"data": None, "wallets": [], "ts": 0.0, "err": None, "fetches": 0}
LOCK  = threading.Lock()
TTL   = int(os.environ.get("<TOOL>_TTL", "60"))

def refresh(force=False):                 # only writer of STATE
    with LOCK:
        if not force and STATE["data"] and (time.time() - STATE["ts"]) < TTL:
            return
        try:
            STATE.update(..., ts=time.time(), err=None)
        except Exception as exc:          # keep serving the last good payload
            STATE["err"] = f"{type(exc).__name__}: {exc}"[:200]

def background():                          # daemon thread started in main()
    while True:
        try: refresh()
        except Exception: pass
        time.sleep(5)

ThreadingHTTPServer(("127.0.0.1", PORT), Handler)   # loopback only
```

Key points that mattered:

- **Import the sibling CLI module, don't duplicate logic** — `importlib.util.spec_from_file_location`
  on `<tool>.py`, then reuse its fetch/aggregate/format functions. Assert `spec and spec.loader`
  before `exec_module` (pyright complains otherwise).
- **Serve HTML from a file read per request** (`<tool>.html` next to the server) so UI edits need no
  process restart; only server-code changes do.
- Snapshot payload carries `ok`, `error`, `age_s`, `ttl_s`, thresholds, `history`, `data` — the UI
  shows staleness, and a failed fetch keeps the previous good numbers with a warning banner.
- Append one line per refresh to `<tool>_history.jsonl` (`ts` + the 1–2 numbers you chart) and keep
  the last N lines; the sparkline then shows real movement instead of a single point.

Routes: `/` + `/<brand>` (dashboard), `/api/board` (JSON), `/api/refresh` (force), `/text`
(plain-text card via the CLI formatter — perfect phone bookmark), `/healthz` (`{ok, age_s}`).
`log_message` override that skips health probes keeps the log readable.

## 2. Tunnel + watchdog (ephemeral URL → delta-only DM)

`~/.hermes/scripts/<tool>_up.sh` — idempotent, safe to run every 10 min from cron:

```bash
exec 9>"$LOGS/<tool>_up.lock"; flock -n 9 || exit 0     # never two watchdogs at once
if ! curl -sf -m 5 "http://127.0.0.1:$PORT/healthz" >/dev/null; then
  pkill -f "[<t]ool_server.py"        # bracket trick, see pitfalls
  setsid nohup env <TOOL>_PORT="$PORT" python3 -u "$SCRIPTS/<tool>_server.py" >>"$LOG" 2>&1 </dev/null &
  for _ in $(seq 1 20); do sleep 1; curl -sf -m 3 ".../healthz" && break; done
fi
pgrep -f "cloudflared tunnel --url http://localhost:$PORT" >/dev/null || {
  : >"$TUN_LOG"; setsid nohup cloudflared tunnel --url "http://localhost:$PORT" --no-autoupdate >>"$TUN_LOG" 2>&1 </dev/null & ...
}
URL="$(grep -ho 'https://[a-z0-9-]*\.trycloudflare\.com' "$TUN_LOG" | tail -1)"
echo "$URL" >"$URL_FILE"
[ "$(cat "$SEEN_FILE" 2>/dev/null)" != "$URL" ] && { echo "$URL" >"$SEEN_FILE"; printf '... %s\n' "$URL"; }
```

Register as `no_agent` cron every 10 min with `deliver: origin` — empty stdout = silent, so the user
only ever sees a message when the URL changed or a service came back. Also add it to the system
crontab (`@reboot` + `*/10 * * * *`) so the board survives a VPS reboot even when the Hermes gateway
isn't up; `flock` makes the two lanes harmless together.

## 3. Token-gated writes (public reads, private edits)

`~/.hermes/data/<tool>_token.txt` (mode 600, `secrets.token_urlsafe(18)`), env var wins over the file.
`do_POST` on `/api/watchlist` requires `k` in body / query / `X-Board-Token`; `503` when no token is
configured, `403` wrong, `400` invalid item, `200` + rewritten JSON on success (then force the next
refresh by zeroing `STATE["ts"]` so the UI reflects it immediately). Reads stay open — the data is
public and the user already has the plain link on their home screen. Hand over the `?k=` link once and
note it can be rotated.

## 4. Verifying a browser-less UI

No browser on the box → render the page's JS in node with a hand-made DOM stub:

```javascript
const ids=[...html.matchAll(/id="([A-Za-z0-9_]+)"/g)].map(m=>m[1]);
const el=()=>({textContent:"",innerHTML:"",style:{},value:"",className:"",
               classList:{toggle(){},add(){},remove(){}},offsetTop:0});
const nodes={}; ids.forEach(i=>nodes[i]=el());
global.document={getElementById:id=>nodes[id]||(nodes[id]=el()),querySelector:()=>el()};
ids.forEach(i=>{ global[i]=nodes[i]; });      // browsers expose ids as globals — mimic that
global.setInterval=()=>0;                      // stop the auto-refresh loop
global.location={search:""}; global.localStorage={getItem:()=>null,setItem:()=>{}};
global.fetch=async()=>({json:async()=>realApiJson});   // feed the REAL /api payload
eval(js + "\n;global.__probe=()=>({...});");   // `let`-scoped vars are unreachable from outside
setTimeout(()=>{ console.log(global.__probe()); }, 400);
```

Gotchas: run `node --check` on the extracted script first; do NOT replace `setTimeout` with an
immediate call (the async `load()` microtask hasn't run yet and every probe reads empty); probe
`tabCur` / row counts / rendered cell text, not just "no exception". Pair it with
`python3 -m py_compile` on the server and an id-existence check (every `getElementById` /
bare-global id must appear in the HTML).

## 5. Agent-tooling traps hit while doing this (all cost real time)

- **`pkill -f "<tool>_server.py"` typed as an inline terminal command murders your own shell** — the
  pattern matches your own command line. Use the bracket trick `pkill -f "[<t]ool_server.py"`, or do
  the kill inside the watchdog script (whose own cmdline is `bash <script>`).
- **Long inline terminal one-liners get hard-blocked** by the command parser ("oversized inline
  payload"): keep inline calls small, or write a `.sh` and run `bash /path/file.sh`.
- **A patch whose anchor is ambiguous can land the new block at EOF** (after `</html>`, after
  `sys.exit(...)`), silently producing valid-looking-but-dead code. After patching HTML or long
  scripts, re-read the tail and confirm placement; prefer small replace-mode patches with unique
  anchors over multi-hunk patches.
- **An "already healthy" old process keeps serving stale code** — the watchdog health-checks first,
  sees 200, and never restarts. After changing server code, kill explicitly (bracket pattern) and let
  the watchdog relaunch, then re-check the new route; `pgrep -af` the exact pid/cmdline to confirm.
- Verify over the tunnel, not just loopback: POSTs through cloudflared (add/remove then revert) prove
  the whole path — body forwarding, token check, file rewrite, UI update.

## 6. Reporting shape for this user

Numbers with units, the exact command/path, and a "cara pakai" line per feature. State what was
verified with real output ("POST tanpa token → 403", "render test: 6 baris") and flag anything you
did NOT verify (e.g. "@reboot belum dites dengan reboot VPS beneran"). Offer the next concrete step
as a priority action, not a menu.
