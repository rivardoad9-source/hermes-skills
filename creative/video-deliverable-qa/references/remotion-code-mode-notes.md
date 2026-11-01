# remotion-opus: photo-driven ad in code mode (session notes)

Engine lives at `~/remotion-opus-skill`. These notes are the parts that cost real
render cycles to learn; keep them in sync when the engine changes.

## Why code mode at all
- Stock `ros` spec mode (flythrough/poster/kinetic) renders **typography + fake UI
  only** — it cannot place a real product photo. `prompts/agent.md` for code mode
  says "no assets". A food/product ad therefore needs a bespoke code-mode scene.

## Project shape
```
projects/<slug>/brief.md      # intent, target audience, constraints
projects/<slug>/facts.md      # EVERY number/claim on screen + its source (linter rejects invented numbers)
projects/<slug>/script.json   # mode:"code", slug, language, fps, holdSec, brand, lines[]
projects/<slug>/scene/index.tsx   # the custom scene: photo card + camera kf + beats + lockup
projects/<slug>/out/<slug>-landscape.mp4 + <slug>-portrait.mp4
projects/<slug>/words.json    # per-line dur + word timings, written by the VO step
```
- `node bin/ros.mjs code-check <slug>` → validates the scene (run after every edit).
- `node bin/ros.mjs code-render <slug>` → both aspects, 60fps h264+aac, 1920×1080 +
  1080×1920. `RENDER_CONCURRENCY=2`.
- Cost on a 2-core box: **~10 min per aspect** (~20 min both). Two `chrome-headless`
  workers at ~85% CPU = healthy progress; ~0% on both = stalled.

## VO: reuse the repo's own pipeline
- Spec mode's ElevenLabs path (voice/model/normalisation) is the proven one. Call it
  from a throwaway `tmp_*_audio.ts` at the repo root rather than re-implementing.
- It writes `words.json`; the scene reads cue frames via `vo.cue('m06:lima')` etc.
- Lines are **not** separated by extra pauses: total VO ≈ sum of line durations, and
  cue frames come from that arithmetic — BUT the rendered audio gives each line a
  small lead-in, so real cue frames run **~+0.1s per line** late (6 lines ≈ +0.6s).
  Never trust the computed frame numbers: extract frames and check where content
  actually lands.
- The STT verification reports `brand MISSING` for multi-word brand names (e.g.
  "Mango Cheese", "Fleur de Coco") even when the transcript is perfect — the phonetic
  comparer does not join words. Ignore that specific warning; check the transcript.
- Free-tier limits: `402` for music (no background music at all) and for library
  voices (only premade `Roger`, US accent).

## Scene building lessons
- One continuous world: the "camera" is the card transform (`kf` on cx/cy/size/zoom);
  keep push-ins small (1.0–1.4) or the low-res source gets soft.
- Beats: `{at, to, kicker, head, sub}` + ingredient chips that light up on spoken
  words (`Chip lit={prog(t, c.at, c.at+12)}`). Numbers on screen must exist in
  `facts.md`, including the price.
- Persistent corner labels (product name top-left, price top-right) act like the
  thumbnail: keep them visible from early on, fade them out — not hard-cut — when the
  lockup arrives.
- Lockup = wordmark + tagline + HARGA/price + CTA pill; start it ~0.4s before the
  final VO line and cross-fade the outgoing beat text (see `video-deliverable-qa`
  step 4 on dead air).

## Source photo handling
- Telegram compresses to ~500×500 px. Upscale (Lanczos + light sharpen) to ~1250
  before compositing, and disclose the softness; ask the user for the original as a
  **file/document** for a sharper re-render.
- Illegible label text on the photo (brand/price) must never be OCR-guessed — take
  brand, price, and product name from what the user says in chat.

## Operations
- After killing a render, orphaned `chrome-headless` children keep burning CPU:
  `pkill -f "chrome[-]headless"` (bracket trick, otherwise the pattern matches the
  invoking shell and kills it — exit `-15`).
- Keep `.env` on the working provider (the paid-but-empty Vikey key silently breaks
  the art-director/reviewer path; back it up as `.env.vikey.bak` and point the
  builder/verifier at the working model).
