---
name: product-ad-from-photo
description: "Use when a product photo must become a promo video."
---

# Product ad from a customer photo (Remotion, code mode)

Trigger: the user sends a product photo (often with a one-liner like *"mango cheese 15rb"*) and wants a
promo/ad video — the "jasa video promo UMKM" income lane, or a new portfolio asset.

Engine basics (install, `ros new/run/lint/audio/render`, spec mode, editing `spec.json`, `prompts/builder.md`)
live in the **`remotion-opus`** skill — load it too. This skill covers what that one does not: putting a REAL
product photo on screen and making the result look like a real ad.

## The gap you will hit first

Stock engines are typography/fake-UI only: spec mode has no image widget and the code-mode prompt says
"no assets". A food/product ad without the product is worthless → author a **bespoke code-mode scene**:

```bash
node bin/ros.mjs new <slug>            # scaffold (mode: code in script.json)
# edit projects/<slug>/scene/index.tsx  — own components: photo card, camera push-in, chips, lockup
node bin/ros.mjs code-check <slug>     # validates the scene — after EVERY edit
node bin/ros.mjs code-render <slug>    # renders landscape + portrait
```

Recon the engine for image support once, cheaply, before authoring:
`grep -ril "staticFile\|Img\|assets\|image" src cli prompts` — then stop reading engine source and write the scene.

## Step 1 — facts come from the user's words, not from your reading of the photo

- Ask once, batched: is this your product? exact product name? price? original photo as a **FILE**?
- `facts.md` records every on-screen item with source + date. Name and price come from the user's message
  ("manggo cheese 15rb" → "Mango Cheese", Rp15.000). Never OCR a blurry label.
- If the photo shows something the user did not name (chia, coconut) but they call the product something else
  ("cheese"), **follow the user** and drop the ingredients you cannot confirm from both their words and the
  photo — in the on-screen copy *and* the VO.
- No unsourceable claims: no "best seller", no premium-ingredient claims, no sales/profit numbers.

## Step 2 — photo prep

Chat platforms compress: a Telegram photo arrives ~500×500. Upscale (PIL Lanczos + light sharpen) before
compositing so the 1080p card is not mush, keep the original resolution in `facts.md`, and **tell the user**
the source is soft and that the original sent as a document would sharpen it.

## Step 3 — VO: reuse the engine's own pipeline, never invent a new one

Write a throwaway `tmp_<slug>_audio.ts` at the repo root that imports the repo's own TTS/voice helpers, so the
voice, model and normalisation match the proven spec-mode output. ~6 lines / ~40 words ≈ 15 s of speech.

- Cue the scene off spoken word timings (`vo.cue('m02:mangga')`) so ingredient chips light up *as they are said*.
- Captions must match what is actually spoken. TTS-spelling trap: English words come back garbled to the STT
  check ("cheese", "jelly") — put the phonetic spelling in `text` for the TTS/STT pair and the pretty spelling
  in `caption` (spoken `jeli`, caption `jelly`).
- A multi-word brand name triggers a false "brand MISSING" in the STT check (it compares token by token) —
  read the transcript it prints instead of chasing the warning.

## Step 4 — QA the film with frames, not vibes

`code-render` produces no contact sheet, so build one and look at it:

```bash
ffmpeg -y -i out/<slug>-landscape.mp4 -vf "fps=12/<dur>,scale=480:-1,tile=4x3" -frames:v 1 /tmp/sheet.jpg
```

Ask the vision model for **defects only** (clipped text, overlap, empty frames, illegible price, broken
layout). Then re-extract the suspect timestamps at **full resolution** before changing anything — two traps:

- a headline showing only 2–3 letters is the character-reveal animation mid-flight, not clipping;
- text on a 4x3 sheet downscaled to a few hundred pixels looks illegible while it is perfectly fine at full res.

Finish with `ffprobe` per file (duration, w×h, 60 fps, aac) and report those numbers.

## Step 5 — polish the scene switch (the defect you will actually see)

A hard `opacity: lockup ? 0 : 1` cut leaves a ~0.4 s frame that is almost empty. Fix it by starting the
incoming lockup earlier (e.g. `f6 - 30` instead of `f6 - 10`) so the two scenes **cross-fade**, and fade the
outgoing corner labels instead of cutting them. Keep the final caption from restating the CTA pill verbatim —
write a subtitle that matches the spoken line instead.

**Batch every fix into ONE re-render.** On 2 cores an 18 s film is ~10–12 min per aspect (~20+ min both);
never burn a render cycle on a single tweak.

## Step 6 — delivery

Ship both aspects plus ready-to-post caption text, and state the caveats plainly: no music (ElevenLabs free
tier returns 402), US-accent premade voice, soft source photo, and "every on-screen number came from you".
Don't close by asking whether to make something else — the delivered video is the proof; offer follow-ups
(second variant, service page) as a short line, not as a question that stalls the turn.

## Pitfalls

- Don't touch `src/engine` or `src/widgets` to make one ad work — that changes everyone's films.
- Don't put a number on screen that the facts cannot cite; in code mode there is no linter, so you are the linter.
- Render output going quiet is normal: `code-render` buffered through `tail` shows nothing while it works — poll
  `ps -eo etime,pcpu,comm --sort=-pcpu` to see the two `chrome-headless` workers instead of assuming it hung.
- Support file: `references/fleur-de-coco-case.md` — the worked example (beat/cue map, ffmpeg commands, timings).
