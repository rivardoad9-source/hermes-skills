---
name: webhook-receivers
description: "Use when webhooks need custom signatures or HTTPS exposure."
---

# Standalone Webhook Receivers

Use when an external service pushes webhooks that the Hermes built-in webhook platform can't handle. The built-in platform (see `hermes-agent` skill → `references/webhooks.md`) validates HMAC-SHA256 with the subscription secret — services with **custom signature schemes** (e.g. Lynk.id's `X-Lynk-Signature` = plain `sha256(amount + refId + message_id + key)`) or that **require `https://` URLs** need a standalone receiver. Validated live: Lynk.id merchant webhook → Telegram notification, running 24/7.

## Architecture (all stdlib + systemd, zero dependencies)

1. **Receiver** — Python stdlib `http.server` (ThreadingHTTPServer):
   - Validate the provider's signature per its spec; keys come from a local JSON config file (never hardcode, never in code).
   - Response semantics: `200` valid event, `400` invalid signature, `503` when the secret isn't configured yet (provider retries instead of silently dropping), `GET /health` → ok.
   - Log every event to a JSONL file in the same dir.
2. **Notify** — Telegram bot API `sendMessage` (plain `urllib`, no deps). Chat id: `TELEGRAM_ALLOWED_USERS` from the Hermes `.env` (or explicit `TELEGRAM_CHAT_ID`). Make the receiver read `.env` itself so the service is self-contained.
3. **systemd user service** — unit with `Restart=always`, `WantedBy=default.target`, `Environment=HERMES_HOME=...`. Linger keeps user services alive at boot. **Pitfall:** if the Hermes gateway runs as a SYSTEM service, shells spawned by it have no user bus — `systemctl --user` fails with "Failed to connect to bus: No medium found"; export `XDG_RUNTIME_DIR=/run/user/<uid> DBUS_SESSION_BUS_ADDRESS=unix:path=/run/user/<uid>/bus` first (see `hermes-gateway-ops`).
4. **HTTPS via cloudflared quick tunnel** (needed when the provider rejects `http://` or you can't open inbound ports):
   ```bash
   # its own systemd user service
   ExecStart=/usr/local/bin/cloudflared tunnel --url http://localhost:<port> --no-autoupdate
   # get the URL:
   journalctl --user -u cloudflared-<name> --no-pager | grep -oE "https://[a-z0-9-]+\.trycloudflare\.com"
   ```
   **CAVEAT:** trycloudflare URLs are ephemeral — they CHANGE on every service restart/reboot, so the provider dashboard URL must be updated. For a permanent URL: Cloudflare named tunnel + your own domain, or ngrok's static domain.
   - Install cloudflared: download `cloudflared-linux-amd64` from GitHub releases to `/usr/local/bin`.

## Test & verify

- Local: POST a valid-signed payload (expect 200 + log + Telegram) and a tampered one (expect 400).
- Through the tunnel: same POSTs against the `https://...trycloudflare.com/<path>` URL.
- External reachability: `curl https://r.jina.ai/https://<url>/health` (renders through their proxy) — or ask the user to open the URL on their phone.
- **Cloud security groups (Tencent/AWS/Aliyun) block inbound by default** — direct `http://public-ip:port` webhooks fail with timeouts (error 522 via external fetchers). A tunnel sidesteps this entirely; otherwise the user must open the port in the cloud console.

## Security rules

- No secret configured → `503`, never accept (an exposed unauthenticated endpoint is a spam/abuse magnet).
- Invalid signature → `400`. Always constant-time compare (`hmac.compare_digest`).
- Config file with secrets: `chmod 600`. Never print the merchant key/secret in outputs or chat.
- Test notifications must be clearly labeled (e.g. "🧪 TEST") so the user never mistakes them for real events.

## References

- `references/lynkid.md` — Lynk.id merchant webhook specifics (signature scheme, dashboard flow).
- Working example on this machine: `~/.hermes/lynk_webhook/receiver.py` (systemd user services: `lynk-webhook`, `cloudflared-lynk`; config `config.json`; sales log `sales.log`).
