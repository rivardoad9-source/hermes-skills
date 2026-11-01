# Case: "Mango Cheese" Rp15.000 dessert-jar ad — worked example (7 Okt 2026)

Deliverable: 18,15 s promo ad, landscape 1920×1080 + portrait 1080×1920, 60 fps h264+aac, Indonesian VO.
Built with the `ros` CLI (remotion-opus engine) in **code mode** with a bespoke scene —
slug `fleur-de-coco`, project files `projects/fleur-de-coco/`.

## Inputs

- Photo the user sent: `~/.hermes/cache/images/img_86010b1bc037.jpg` — glass jar, creamy white base, jelly cubes
  and orange fruit, spoon lifting a piece; the lid label was **illegible**. Original resolution only **500×500 px**
  (Telegram compression) → upscaled to 1250 px with PIL Lanczos + sharpen before compositing.
- User's words: "manggo cheese 15rb" → product name **Mango Cheese**, price **Rp15.000**. The photo's white base
  looked like chia to the eye, but the user called it cheese → the VO/on-screen copy used "mangga + krim lembut"
  and dropped the ingredients the user had not named. No invented claims, no sales numbers.

## Scene structure (single world, camera = card transform)

- Beats keyed off VO cues, one per line: `SEGAR` → `MANGA & KRIM` → `Rp15.000` → `DINGIN` → end-card lockup.
- Ingredient chips (MANGA / KRIM LEMBUT / JELLY KENYAL) appear with the "isi jar" line and light up on the
  spoken word: `vo.cue('m02:mangga')`, `vo.cue('m02:krim')`, `vo.cue('m03:jeli')`.
- Persistent corner labels (product name top-left, price top-right from the price beat) so the price is on screen
  for the back half; they fade out as the lockup arrives.
- End-card lockup: wordmark (`Mango` cream + `Cheese` italic mango), tagline, `HARGA Rp15.000`, CTA pill
  `PESAN LEWAT DM`, and a small credit line.

## VO (6 lines, 39 words, 15,15 s + 2,4 s hold)

Written through a throwaway `tmp_fleur_audio.ts` that reuses the repo's own ElevenLabs helpers (voice `Roger`,
same model/normalisation as spec mode). All 6 lines came back **100% heard on take 1**. Two gotchas hit:

- English words garble the STT check → `text: "Disiram jeli kenyal…"` (phonetic) with
  `caption: "Disiram jelly kenyal…"` (pretty).
- The multi-word brand "Mango Cheese" always warns `brand MISSING` (the checker compares token by token) even
  though the transcript shows it was heard — read the transcript, don't chase the warning.

Cumulative cue map (from `words.json`): m01 0–1,91 · m02 1,91–4,60 · m03 4,60–7,37 · m04 7,37–9,64 ·
m05 9,64–12,46 · m06 12,46–15,15. Rendered film ran 18,15 s (pipeline pads ~0,1 s per line).

## QA commands that mattered

```bash
node bin/ros.mjs code-check fleur-de-coco        # scene validation, after every edit
node bin/ros.mjs code-render fleur-de-coco       # both aspects, ~10-12 min per aspect on 2 cores
ffprobe -v error -select_streams v -show_entries stream=width,height,r_frame_rate,duration -of csv=p=0 out/<f>.mp4
ffmpeg -y -i out/fleur-de-coco-landscape.mp4 -vf "fps=12/18.15,scale=480:-1,tile=4x3" -frames:v 1 /tmp/sheet.jpg
ffmpeg -y -ss 12.86 -i out/fleur-de-coco-landscape.mp4 -frames:v 1 /tmp/f_12.86.png   # suspect frame, full res
```

Vision pass on the contact sheet reported only two things, and both needed full-res verification:

- a headline reading "MAnY"/"MA" → the character-reveal stagger mid-flight, **not** clipping (fine at 12 chars
  when it finished 0,4 s later);
- portrait pills "illegible" → artifact of the sheet being scaled to ~420 px tall; perfectly legible at 1080×1920.

The real defect was a ~0,4 s almost-empty frame at the scene switch (hard `opacity: lockup ? 0 : 1` cut).
Fix: lockup window `f6 - 30` instead of `f6 - 10`, corner labels cross-faded with
`1 - prog(t, f6 - 38, f6 - 28)`, chips cleared by `f6 - 30`, and the arriving elements staggered
(wordmark `f6-26`, tagline `f6-16`, price `f6-10`, CTA `f6-4`). Second fix: the last caption no longer restates
the CTA pill ("Pesan sekarang lewat DM"). Both fixes went into **one** re-render.

## Delivered with

Both aspects + ready-to-post caption text, and disclosed caveats: no music (ElevenLabs free tier → 402
`paid_plan_required`), US-accent premade voice (free tier rejects library voices with 402), source photo soft
because the original was 500×500 — offer to re-render if the user sends the original as a document, and that
every on-screen number came from the user.

Cost/time: engine Vikey path unavailable (Rp0 balance → builder/verifier on DeepSeek instead), so there was no
frame-seeing reviewer: the ffmpeg + vision loop above was the review step.
