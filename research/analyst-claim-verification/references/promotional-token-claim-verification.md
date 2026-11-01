# Verifying a single promotional token claim (worked case: $WLD, 28 Sep 2026)

Companion to the "ONE promotional claim" variant in SKILL.md. Use this when the user drops a
single X/Threads link about a token — usually a "BREAKING NEWS" / "baru memasuki fase baru" post
— with no explicit question. Deliverable: a **claim ledger**, a vault note, and an operational
verdict. Not a corpus scan; the hit-rate ladder does not apply.

## The input

- Post: `https://x.com/DombaEth27/status/2104207777610801638`, posted 27 Sep 2026 13:53 UTC = 20:53 WIB
- Claim: World ID 4.0 lets applications pay fees for proof-of-human while end users stay free,
  therefore "usage naik = fee/revenue terbentuk → value ekosistem ikut meningkat … Good News"
- Token address quoted in the post: `0x163f8c2467924be0ae7b5347228cabf260318753`

## Step 1 — age gap (the first finding)

| Date | Event |
|---|---|
| 15 Feb 2025 | Worldcoin Foundation **first** announces World ID protocol fees (testnet Q2 2025) |
| 30 Apr 2025 | Official blog "Introducing World ID Fees" — fees payable in WLD |
| 16–17 Apr 2026 | Blog "The Revenue Potential from World ID" (World ID 4.0 + fees) |
| 15 Jun 2026 | Re-reported by media (BitcoinWorld / CryptoRank) |
| **27 Sep 2026** | Post labelled **"BREAKING NEWS"** |

Narrative age **19 months**; the specific source post **~5 months**. Get the post's own
`created_at` from the syndication route — it is the only way to show the *post* is new while the
*news* is not.

## Step 2 — the value-accrual gap (quote the hedging)

Verbatim from `world.org/blog/announcements/world-id-fees-the-revenue-potential-from-world-id`:

> "Each credential issuer will have discretion over how to use their credential fees. Protocol
> fees can be programmatically allocated according to pre-defined onchain mechanisms. Such a
> mechanism **may** direct a portion of the protocol fees toward the network's operations, or it
> **may** burn a share of the fees. **Initially, the World Foundation will program the
> configuration of this mechanism.**"

And from `world.org/blog/announcements/introducing-world-id-fees` (30 Apr 2025):

> "The community **may** choose to direct a portion of the fees toward continued network growth —
> for example, by **supporting Operators or funding the User Tokens** — or **even decide to**
> burn a share of the fees."

Read for: `may` not `will` (no committed burn); the **first-listed** use is *funding the User
Tokens* = spending on emissions, not reducing supply; burn is last and softened to "even decide
to"; the configuration is held by the Foundation, not the community. Conclusion: **no mechanism
guarantees fee revenue reaches WLD holders** — the post's "value ekosistem ikut meningkat" has no
bridge.

## Step 3 — realised vs potential

- 30 Apr 2025: "The Foundation is **currently working on** the protocol changes necessary…"
- 16 Apr 2026 (a year later): "**Once fees are enabled**, an application's wallet must be pre-funded…"
- Blog title itself: "The Revenue **Potential** from World ID". The post says "**peluang**" too.
- **No published revenue figure found anywhere.** Zoom / Tinder / Razer / Match Group / Hakuhodo
  all sit at pilot / exploring / trialing.

## Step 4 — emission vs revenue (use the project's own numbers)

Inputs: CoinGecko 28 Sep 2026 — price $0,5591, circulating 3,72B of 10B (**37,2%**), mcap $2,08B,
FDV $5,59B. Unlock rate from the project's own tokenomics post: **2,9M WLD/day** since 24 Jul 2026
(down 43% from 5,1M/day; community −50% 3,2→1,6M, team+investor −32% 1,9→1,3M; **no cliffs**,
linear daily to the final tranche ~Jul 2038). Project's own fee example: **$0,40 per verified
user per month** (= $4,80/yr).

| Quantity | Value |
|---|---|
| New sellable supply | 2,9M WLD/day · 87M/month · 1.058M/year |
| In USD | **$1,6jt/day · $48,6jt/month · $591,8jt/year** |
| Dilution vs circulating | **28,5%/year** |
| Unreleased overhang | 6,28B WLD = **1,69×** circulating |

Payers required to offset emissions, assuming the most bullish case (100% of protocol fees burned
**and** all fees paid in WLD):

| Burn share | Verified users needed continuously |
|---|---|
| 100% | **123,3 juta** |
| 30% | 37 juta |
| 10% | 12 juta |

World has **~18 juta** users ever Orb-verified ⇒ ~14,6% of the requirement, under an assumption
the official blog contradicts (it only says the community "may" burn "a share"). Label this as a
balance check, not a forecast.

## Step 5 — why now, and who

CoinMarketCap on the move: "**Renewed attention** on how World ID fees will be charged in WLD has
strengthened the token's value accrual narrative… the best explanation… is a combination of **soft
but identifiable catalysts**: a refreshed focus… framing it as a 'falling wedge' breakout, and
**sizeable leveraged positions on Binance futures and subsequent liquidations**. While there is
**no single hard event** like a listing or lawsuit that fully explains the move."

Price context at the time of the post: Δ7d **+24,2%**, Δ30d **+43,7%**, Δ1y **−56,2%**,
**−95,2%** from ATH $11,74 (9 Mar 2024). The run preceded the post.

Account profile: Twitter Score **3,01/1000**; posts "ALTCOIN GEMS FOR 2027… **How to Subscribe**"
⇒ subscription seller; hindsight brag *"$BTW +1.445% Harusnya bulan lalu all in $BTW gak perlu
cape riset on-chain sana sini wkwkwk"*; no position disclosure.

## Claim ledger (the deliverable shape)

| Claim | Status |
|---|---|
| Address `0x163f…8753` is WLD | ✅ BENAR |
| World ID 4.0 exists | ✅ BENAR |
| Applications pay, end users free | ✅ BENAR (mechanism description accurate) |
| Fees paid in WLD | ✅ BENAR (blog 30 Apr 2025) |
| "BREAKING NEWS" | ❌ SALAH — 19-month narrative |
| "revenue terbentuk" | ⚠️ BELUM — "once fees are enabled", zero public figures |
| "value ekosistem meningkat" | ❌ NO MECHANISM — burn is "may", Foundation-configured |
| Reason to buy | ❌ NOT SUPPORTED — 28,5%/yr dilution against zero revenue |

Verdict phrasing that worked: **"mekanismenya bener, framing-nya menyesatkan"** and
"bukan token sampah — produknya nyata, tapi tweet ini bukan alasan buat masuk".

## Transferable rules

- A promo post's **mechanism description can be accurate while the framing is misleading**.
  Verify both separately; do not let "the facts are right" launder the "BREAKING" label.
- Always ask **"does the revenue reach this token, and is that committed?"** Revenue for a
  foundation ≠ value for a token holder. Look for buyback/burn language and its modality.
- **Prefer the project's own published numbers** for the dilution-vs-revenue ratio — it is far
  harder to argue with than your own assumptions.
- Do the arithmetic in `terminal`, label assumptions explicitly, and name the most bullish case
  you are granting before showing it still falls short.
- Save the vault note — the user's standing rule is a note per link, with the ledger and the
  source quotes preserved.
