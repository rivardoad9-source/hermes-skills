# API key prefix index

## Verified in practice (2026-08)

| Prefix | Provider | Read-only verification endpoint |
|--------|----------|--------------------------------|
| `sk-or-v1-` | OpenRouter | GET `https://openrouter.ai/api/v1/auth/key` → label, is_management_key, limit (spend cap, USD), usage (lifetime/daily/weekly/monthly), is_free_tier, expires_at, creator_user_id. Also GET `https://openrouter.ai/api/v1/credits` → total_credits, total_usage (no account email in the 2026-08 response). Bearer auth. |

## Widely documented formats (confirm against provider docs before relying)

| Prefix | Provider |
|--------|----------|
| `sk-ant-` | Anthropic |
| `sk-proj-` / `sk-svcacct-` | OpenAI (project / service-account keys) |
| `sk-` bare (48+ chars, no suffix) | OpenAI (legacy) — ambiguous, verify |
| `ghp_` / `gho_` / `github_pat_` | GitHub (classic PAT / OAuth / fine-grained PAT) |
| `xai-` | xAI |
| `gsk_` | Groq |
| `AIza...` | Google (API key) |

Generic `sk-` prefixes are shared by many providers — prefix alone is never
identity; always confirm with the provider's metadata endpoint when one
exists.
