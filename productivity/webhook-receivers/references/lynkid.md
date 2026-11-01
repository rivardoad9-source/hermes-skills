# Lynk.id merchant webhook

Lynk.id = Indonesian creator-commerce platform (sell digital products, courses, ebooks; profile URLs like `lynk.id/<username>`, public catalogs readable without login). There is NO public seller API — the only official integration is the merchant **webhook** for successful-transaction notifications (documented in the public Postman collection "Lynk Webhook").

## Signature scheme (custom — NOT HMAC)

Header: `X-Lynk-Signature`

```
signature = sha256( amount + refId + message_id + merchant_key )
```

- `amount` = the `grandTotal` field from the body (string)
- `refId`, `message_id` = body fields
- `merchant_key` = secret; **appears in the seller dashboard ONLY AFTER you save a webhook URL**

Python validation:

```python
expected = hashlib.sha256((amount + ref_id + message_id + key).encode()).hexdigest()
valid = hmac.compare_digest(expected, received_sig.lower())
```

## Dashboard flow

1. Seller dashboard → Settings/Webhook → save the webhook URL.
2. **URL must start with `https://`** — plain `http://` is rejected with "Please enter a valid URL starting with https://".
3. Merchant key is then shown; store it (config file, `chmod 600`) and restart/refresh the receiver (a receiver that re-reads config per request needs no restart).

## Body fields

`refId`, `grandTotal`, `message_id` (signature inputs) plus context like `productName`/`currency`. Exact payload shape varies — log raw bodies during testing.

## Working setup on this machine

- Receiver: `~/.hermes/lynk_webhook/receiver.py` (stdlib http.server, reads Telegram creds from Hermes `.env`, responds 200/400/503, JSONL sales log at `~/.hermes/lynk_webhook/sales.log`)
- Config: `~/.hermes/lynk_webhook/config.json` → `{"merchant_key": "..."}`
- Systemd user services: `lynk-webhook` (port 8645) + `cloudflared-lynk` (quick tunnel → ephemeral `https://...trycloudflare.com/lynk`)
- Business context: user sells AI-tools digital products via `lynk.id/zemiz`; sales notifications go to Telegram.
