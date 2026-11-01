---
name: partner-and-community-sourcing
description: Use when sourcing a partner dev or builder community.
---

# Partner and community sourcing

Finding the people to build with (co-founder, partner dev, mentor) and the paid entry points (bounties, hackathons, grants) into a target industry.

## When to use

- User asks to "cari partner", "cari co-founder", "cari dev buat dikerjain bareng", find a mentor, or break into a new industry/ecosystem.
- Adjacent but distinct: `job-listing-hunter` (paid roles / internships), `money-radar` (what to sell), `external-repo-vetting` (vetting one repo), `blocked-page-recovery` (page fetch fallbacks).

## Core principle

Nobody credible says yes to "mau jadi partner gw?" from a stranger. The reliable path is a shared room plus one small finished artifact together. So the deliverable is never a list of cold names. It is ranked places where builders self-select, plus the smallest thing the user can ship with someone inside a week.

State this trade-off to the user explicitly. Selling hope here wastes months; the honest version is more useful than a long contact list.

## Rank channels by hit rate (do this before searching)

1. **Team-required competitions** (hackathons with a mandatory team size, e.g. 3-4 people). Highest yield: deadline-driven, collaboration is forced, organisers often run a matching chat.
2. **Bounty / grant platforms of the specific ecosystem.** Paid work plus peer review, and teammates emerge from shipping. Also builds the proof-of-work asset the user needs anyway.
3. **Community hubs of the exact stack** (the local ecosystem org's Telegram/Discord). The group chat, not the marketing page, is where teammates are actually recruited.
4. **Event platforms** (Luma, Eventbrite, Meetup): demo days, hacker houses, campus series. Physical rooms convert far better than DMs.
5. **Explicit matchmaking programmes** (e.g. YC Co-Founder Matching). Free, no idea required, profile private — but check regional density before recommending.
6. **Incubators / accelerators.** Value is mentors and cohort peers, not the cash.
7. **Cold DM of individuals.** Lowest yield. Follow-up move after 1-3, never the opening.

## Workflow

1. **Pin the target complement.** Industry plus what the user is NOT (e.g. "he does product/clients/finance, partner must own engineering and uptime"). Searching for "a partner" without naming the complement produces noise.
2. **Scan channel types in ranking order.** For each candidate record: name, link, status, deadline, team size, whether it is open right now.
3. **Verify liveness** before recommending anything (see below). Label every item open / closed / unverified.
4. **Lead the answer with deadline-sensitive items.** A live registration closing tomorrow outranks ten evergreen links.
5. **Build the ask-asset list.** One working artifact, one 60s demo video, one public repo/portfolio, one sentence on what the user brings. No artifact means no partner.
6. **Write the opening script** (rules below).
7. **Deliver a persistent file** plus a chat summary, and schedule a one-shot reminder for the nearest real deadline.

## Verification (non-negotiable)

- Run `scripts/check_urls.sh` over every link. Report only live ones, and print the final redirect for shorteners — deadlines frequently live in a Google Form behind a `bit.ly`.
- Read JS-rendered pages with `scripts/read_rendered_page.sh` (curl first, headless Chromium `--dump-dom --virtual-time-budget` fallback, JSON-LD extraction). Luma and Next.js event pages carry date, deadline, prize, team size and attendance count in JSON-LD/meta.
- Extract community chat links straight from the page HTML (`t.me/`, `discord.gg`, `linktr.ee`). The chat is the partner pool; the landing page is not.
- Never quote a deadline, prize or team size from a search-result snippet alone. Open the source page.
- When an official social post contradicts a news summary on a deadline, quote the official post and flag the conflict instead of picking one silently.

## Opening script rules

- One message, one specific question. No life story, no CV dump.
- Never ask "be my partner". Offer to take one piece of something that already exists (a bounty, a hackathon track, a PR).
- Lead with evidence of shipping, name the user's own weakness out loud (that reads as credible, not weak), end with a concrete ask tied to what the other person already works on.
- Shape: greeting, who the user is in one line, one shipped artifact, the acknowledged gap, the specific ask.

## Approaching a technical person when the user is the domain expert

This user is the domain side (accounting, reporting, ops) looking for a builder. An engineer's inbox
is full of "gw punya ide, lu yang coding"; the first filter is what the user brings that they cannot
do themselves. Name the three assets before writing a single message: **access to the problem**,
**the numbers language** (hours or rupiah saved per client), **shipped proof** (live artifacts with
checkable results). With none of the three it is a fan message, and say so.

1. Two or three **substantive comments on their work first**: quote the mechanism ("lu handle X pakai
   Y, itu kepakai buat Z"), never "keren". Being recognised precedes being asked.
2. **First message ≤5 lines**: what you noticed in their work, one specific problem you have access
   to, one small ask answerable in a minute. A genuine question ("di tempat lu, proses X masih manual
   atau udah diotomasi?") outperforms a pitch, because it cannot be answered with a template.
3. **First collaboration = one small project**, named roles, defined output. Revenue split after a
   shared artifact, never before. Equity-first ends the conversation.
4. **Bring an artifact, not a deck**: a 5-minute demo of the manual process collapsing (40 min → 6
   min) answers "worth it?" faster than twenty slides. One page of problem + who is hit + hours/money
   lost is the only prep document needed.
5. **Never open with "gw nggak bisa coding"**. Say what is true: writes the spec, tests, decides when
   it ships, directs an AI coding agent. Engineers respect a spec owner/tester and distrust a
   passenger — and the non-technical part surfaces anyway, so hiding it only makes it late.
6. If the goal is learning rather than building, offer an exchange (documentation, number validation,
   hourly pay). Free mentoring requests are ignored.

## Delivery style for this user

- Casual Indonesian, akrab, `gw/lu`, and **no hyphen characters at all** in the chat message; use numbering or line breaks instead of dash bullets.
- Honest framing first, including the low-yield truth about cold outreach, instead of optimistic padding.
- Separate verified facts from advice; mark unverified items.
- Close on an executed action (file written, reminder scheduled), never on "mau gw buatkan?".
- Save the full deliverable as a markdown note in `~/obsidian-vault/` so it is readable on the phone, then summarise the top items in chat.

## Pitfalls

- "These people exist in the field" is not "these people want a partner". Only the top 1-3 channel types are real partner pools; the rest is audience.
- Deadline drift: snippets show older close dates and organisers often extend by a day. Quote the official post.
- Region density: global matchmaking platforms cluster in a few cities. Say so plainly instead of implying local volume.
- Do the outreach for the user, never as the user. Produce the script; they send it.
- Crypto/web3 lane: include scam guards in the deliverable (never pay to join, never share seed phrase or private keys, "collaboration" DMs asking for a deposit are fraud).
- A programme whose deadline already passed is still useful as a rehearsal target for the next edition. Label it "closed, pakai buat latihan" instead of dropping it.
- Don't recommend a person as a partner from a profile read alone. Profiles prove existence, not intent.

## Support files

- `references/indonesia-web3-ai-channels-2026-10.md` — verified channel map (web3 + AI, Indonesia) with links, status and deadlines as of Oct 2026.
- `scripts/check_urls.sh` — liveness and final-redirect check for a batch of URLs.
- `scripts/read_rendered_page.sh` — pull text, JSON-LD and community links out of JS-rendered event pages.
