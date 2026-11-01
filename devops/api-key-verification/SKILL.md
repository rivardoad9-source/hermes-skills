---
name: api-key-verification
description: "Identify pasted API keys by prefix and verify liveness."
---

# API Key Identification & Verification

Use when: the user pastes an API key/token and asks "what is this?", "is this valid?", "whose account is this?". Goal: identify the provider from the key's prefix, verify it is live, and report usage/limits/ownership — without printing the secret.

## Steps

1. Identify the provider from the key prefix. Index: `references/providers.md`. Prefix alone is not identity for generic prefixes (many providers use `sk-`); confirm with a metadata call.
2. Probe the provider's read-only metadata/credits endpoint with the key as a Bearer token. These calls have no side effects — never "test" a key against a state-mutating endpoint (no setWebhook-style calls just to check).
3. Report: valid? label, expiry, spend limit, usage, remaining credits, creator id. Never echo the full key in your reply — it is already in the transcript, don't amplify it; refer to it as `<prefix>…<last4>`.
4. Warn when a live credential was pasted into chat: recommend rotating/revoking it at the provider's keys page if it may have leaked anywhere.

## Pitfalls

- A default/masked label (the key itself truncated) means the owner never named the key — not that it's fake.
- Usage figures are in USD.
- 401 from the metadata endpoint = invalid or revoked. Say so; don't retry-hammer.
- `limit: null` = no spend cap set; `expires_at: null` = no expiry. Both are normal, not anomalies.

## Verified example: OpenRouter (`sk-or-v1-`)

```bash
curl -s https://openrouter.ai/api/v1/auth/key -H "Authorization: Bearer $KEY"
# → label, is_management_key, limit, usage (lifetime/daily/weekly/monthly, USD),
#   is_free_tier, expires_at, creator_user_id
curl -s https://openrouter.ai/api/v1/credits -H "Authorization: Bearer $KEY"
# → total_credits, total_usage  (no account email in the 2026-08 response)
```

Prefix index for other providers: `references/providers.md`.
