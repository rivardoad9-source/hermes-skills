# Cloudflared quick-tunnel URL discovery + health monitoring

Companion to the cloudflared section of SKILL.md. Written after the 04 Okt 2026 false alarm: the daily
"webhook Lynk.id sehat?" cron alerted *"URL tunnel tidak ditemukan di log"* every morning against a tunnel
that had been up for weeks.

## Symptom and root cause

`journalctl --user -u cloudflared-lynk | grep -oE 'https://[a-z0-9-]+\.trycloudflare\.com'` returned
nothing — not because the tunnel was down, but because cloudflared prints the quick-tunnel URL **once at
startup** and the journal had rotated past that line. A monitor whose only source of truth is a rotating
log reports failure on every healthy run, and the user learns to ignore it.

## Live URL, no log involved

```bash
mport=$(ss -ltnp | grep -i cloudflared | grep -oE '127\.0\.0\.1:[0-9]+' | cut -d: -f2 | head -1)
curl -s "http://127.0.0.1:${mport}/quicktunnel"   # {"hostname":"surgical-vehicle-stripes-international.trycloudflare.com"}
```

The metrics listener lives for the life of the process (random loopback port, `--metrics` can pin it).
`hostname` is the subdomain — prefix `https://` yourself.

**Fallback order: metrics → journal → the last known-good URL in the state file.** Never alert on an empty
URL read while the state file still holds a known-good value; that is how a monitor turns into a nuisance.

## Monitor shape that stays silent when healthy

1. **Two independent facts per run**: receiver alive (`pgrep -f "lynk_webhook/receiver.py"`) *and* tunnel
   alive (`pgrep -f "cloudflared tunnel"`).
2. **Local `/health`**: `curl -s -o /dev/null -w '%{http_code}' http://127.0.0.1:8645/health` == 200. This
   is what separates "receiver dead" from "tunnel dead" — a 404 on `/` proves nothing (the receiver only
   routes `/health` and `/lynk`).
3. **Public `/health`** through the tunnel URL == 200 → proves the whole chain (tunnel → receiver), not
   just that both processes exist.
4. **State-file diff for the two events worth waking the user for**: the tunnel PID changed (restart ⇒ URL
   almost certainly changed) and the URL differs from `tunnel_state.json`. Both carry an action —
   "update the Webhook URL in the provider dashboard" — so they earn an alert.
5. **stdout empty when healthy.** With `no_agent` cron the stdout is delivered verbatim, so no output =
   no message.
6. **Persist state only after a successful read**: `if url empty: url = old_url`. Otherwise one bad read
   erases the baseline and every later run screams "URL berubah".

## Prove both paths before trusting a monitor

Run it healthy (expect 0 bytes) **and** force it to fire: write a stale URL into the state file, run,
confirm the alert text names the correct new URL, then restore the state file from a backup copy. A monitor
you have never seen fire is not a monitor — and neither is one you have never seen stay quiet.

## Note on supervisors

On this machine the quick tunnel is a plain background process, yet the journal still answers for a unit
named `cloudflared-lynk` (and `systemctl --user cat` fails without `XDG_RUNTIME_DIR` /
`DBUS_SESSION_BUS_ADDRESS` exported). `pgrep -f "cloudflared tunnel"` is the authority on which PID is
live; `journalctl` only proves a unit exists.
