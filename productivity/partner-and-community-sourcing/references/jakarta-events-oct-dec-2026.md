# Verified Jakarta skill-building events, Oct–Dec 2026

Checked live 2026-10-14. The Nov 12 benchmark the user compares against is Web3Week Asia 2026
(w3w.asia, 11–12 Nov, Kuningan City Grand Ballroom, Jakarta).

## Confirmed, dated, free/cheap (best fit for a student)

- 15 Oct — Webinar: Exploring the Future: Technology, Innovation, Opportunities (BlockDev x PBALabs, online) luma.com/8ve4cnyw
- 22 Oct 18:30 — Road to DevFest Monthly Meetup, GDG Cloud Jakarta, Kby. Baru (workshop Harness w/ Antigravity, Alvin
  Prayuda @ Google Cloud; opening Saad Hamid, Google). Bring laptop, Bahasa Indonesia. luma.com/h999lr13
- 24 Oct 13:00 — Bitcoin Indonesia Community Meetup, RECHARGE Green Brew Space, Jakarta. Free.
- 1 Nov — DevFest Jakarta 2026 "Where AI Builders Come Together", TMII, Jakarta. gdgjakarta.org
- 1 Nov 15:00 — Bitcoin Indonesia Meetup Jakarta Barat, Aming Coffee, Tanjung Duren (Eventbrite 2003248797078)
- 7–8 Nov — SpaceXAI Hackathon Indonesia, Jakarta, approval required, date may shift. luma.com/d4b0eg4v
- 10 Nov 18:00 — Indonesia Temporal User Group #2, GoWork Menara Rajawali, Kuningan. luma.com/17sdoj9j
- 26 Nov 11:30 — Qwen Conference Indonesia 2026 (Alibaba Cloud, free, approval required), Raffles Jakarta. luma.com/6xyynocg
- monthly — Bitcoin Indonesia online meetup 19:30 (30 Oct, 29 Nov); events page: bitcoinindonesia.xyz/community/bitcoin-indonesia-events/

Enterprise-grade, paid or CDO/CTO audience (usually not worth it for a student): Indonesia Data & AI
Conference 29 Oct Pullman Thamrin; Indonesia DevOps Conference 28 Oct Pullman Thamrin; digitalCIO Summit
11 Nov; AI Revolution Summit 25 Nov AYANA MidPlaza.

## Programs to watch (windows open and close)

- **BlockDev Builder Program** — 6-week intensive (12 sessions AI / 9 sessions blockchain), free, ends in a final
  project + chance to become city ambassador. Current cohorts are city-based (Gorontalo 5 Oct–14 Nov, closed 3 Oct;
  Ambon 12 Oct–14 Nov, closed 10 Oct). Watch t.me/blockdev_official and linktr.ee/blockdev_org for the Jakarta batch.
- **IBM SkillsBuild National Hackathon** (Hacktiv8 x IBM x Komdigi) — free, students D3–S3, prize Rp40jt,
  AI agents with IBM Bob / Langflow / watsonx. 2026 cycle closed 25 Sep (final 14 Nov); the hackathon class alone
  yields an international IBM SkillsBuild certificate, so catch the next cycle: hacktiv8.com/projects/ibm/hackathon
- **Pintu Goes to Campus x Web3Week Asia** — exchange campus roadshow; watch for the next stop.

## How to find these fast next time (worked 2026-10-14)

1. Luma is the best single source: `luma.com/discover/jakarta` and `luma.com/discover/jakarta/ai` carry the full
   listing with dates in the RENDERED DOM, plus a JSON-LD `ItemList` in the static HTML. `web_extract` on the
   discover page gives names only; `web_extract` on each `luma.com/<shortid>` gives date/venue/price/approval.
   Some Luma pages answer `bot_blocked` to web_extract — then use browser_exec + document.body.innerText.
2. Aggregators: `aisea.builders/en/events` (SEA AI builder events; has an OpenClaw Jakarta community),
   `dev.events/meetups/AS/ID/Jakarta/blockchain`, `blockspot.io/events`, `allevents.in/jakarta/<topic>`.
3. For recurring free meetups the community's own event page beats search: bitcoinindonesia.xyz (40+ monthly
   meetups across Indonesia), gdg.community.dev + gdgjakarta.org (DevFest / Road to DevFest series),
   blockdev.id + Telegram.
4. `linktr.ee/<community>` is the fastest way to harvest a community's real Luma links — extract all <a> hrefs
   with browser_exec, not web_extract (Linktree renders its link list client-side).
