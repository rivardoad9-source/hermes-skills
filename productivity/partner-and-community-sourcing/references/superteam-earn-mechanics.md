# Superteam Earn — mechanics, verified 10 Oct 2026

Data pulled live from the platform's own API, not from marketing pages.

## Listings API (the whole market in one call)

```bash
curl -s 'https://superteam.fun/api/listings?take=200'        # 21 open items on 10 Oct 2026
```

Useful fields per item: `type` (`bounty` = competition, `project` = freelance, both pay),
`rewardAmount` + token (`USDC` 9 / `USDG` 11 / `SKR` 1), `deadline`, `status` (`OPEN`),
`submissions` (entry count), `agentAccess` (`HUMAN_ONLY` 20 / `AGENT_ALLOWED` 1), slug.

Quirk: the API **ignores query filters** (type/region params are silently dropped and the
same payload comes back). Filter in Python, not in the URL.

## Read `submissions` as the real difficulty signal

Reward size says nothing about odds; the entry count does. On 10 Oct 2026:

| Listing | Reward | Entries |
|---|---|---|
| TokenGems — try a Solana project, give feedback | 350 USDC (5 winners: 100/75/75/50/50) | 133 |
| Create content, El Encuentro Madrid | 2,000 USDG | 110 |
| Road to Colosseum — builders reflect & share | 1,000 USDC | 69 |
| Create X content (Mentioned) | 500 USDG | 43 |
| Pitch & demo at Demo Day | 1,800 USDG | 13 |
| Arf x Superteam Türkiye University Track | 2,500 USDG | 0 |
| Vaultline security audit grants | up to 40,000 USDC | 5 |

Pattern to tell the user plainly: **the cheap, easy bounties are the crowded ones; the
expensive, skill-gated ones sit near empty.** So the beginner strategy is to find the
empty-but-deliverable listing, not to queue in the crowd. Always fetch the count before
recommending a listing — never recommend on prize size alone.

## Money reality (published by the platform)

- Superteam Indonesia sponsor page: **USD 678,055 paid, 100% completion rate**.
- The Touching Grass Fund (Indonesia-only grant): up to **500 USDG** cheque, average
  **USD 427**, 6 recipients, ~1 week response time, contact `wijaya.steven93@gmail.com`,
  skills tagged Other/Growth/Community — **requires Superteam membership first**, so it is
  a reward for being in, not an entry point. Say so instead of dangling it.

## Payment and rules

1. Submit (bounty) or apply (project) → judged by the sponsor, or by the Superteam brain
   trust when the sponsor runs out of bandwidth.
2. **Submissions cannot be edited after sending.** Deadlines only move if the sponsor moves them.
3. Superteam/Solana-sponsored listings: payment form, paid **within 7 days**, **KYC required**.
   External sponsors: payout to the wallet linked to the Earn account; they may want their own
   invoice/KYC.
4. Plagiarism **>15%** = immediate disqualification; repeats = permanent ban. Also ban for
   outsourcing/jokying a submission.
5. Teams: the lead submits once and the payout lands in **one** wallet. Agree the split
   *before* submitting, not after winning.

## Reputation ladder (why winning once matters more than the prize)

Win → XP (1st 80, 2nd 60, 3rd 50), but XP is granted only once you are invited as a
member/contributor. Membership then unlocks the regional grants (Touching Grass) and the
Superteam Talent job board. Sequence: win something small → be seen → get invited → job board
and grants open. That is the honest 1–3 month shape; frame it as a reputation/partner lane,
not this-month income.

## Agent lane (for users who work with AI agents)

Official API for agents exists: register agent → `apiKey` + `claimCode` + agent profile →
submit only listings flagged `AGENT_ALLOWED` / `AGENT_ONLY` via API. An agent **cannot** do
KYC, sign a wallet, or OAuth, so a human opens `superteam.fun/earn/claim/<claimCode>` to
complete the talent profile and claim. On 10 Oct 2026 only **1 of 21** open listings was
agent-eligible (a 2,000 USDG content bounty, deadline 24 Oct) — real lane, thin pipeline.
Never present it as an income source; present it as one extra door.

## Cash-out and guards

Paid in crypto on Solana → Solana wallet (Phantom etc.) → sell via the exchange the user
already uses (Binance / Indodax / Tokocrypto / Pintu); KYC on both sides. Guards to include
in every deliverable: never pay to register or "unlock" a listing, never use a submission
jockey (permanent ban), never share seed phrase/private key with anyone claiming to be
Superteam staff.

## Channels

`https://superteam.fun/earn/regions/indonesia/` · Telegram `t.me/SuperteamId` · X `@SuperteamINDO`.
