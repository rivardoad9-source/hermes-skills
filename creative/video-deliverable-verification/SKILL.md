---
name: video-deliverable-verification
description: "Use before shipping a rendered video: verify frames."
version: 1.0.0
author: Hermes Agent
license: MIT
platforms: [linux, macos]
prerequisites:
  commands: [ffmpeg, ffprobe]
metadata:
  hermes:
    tags: [video, qa, ffmpeg, remotion, deliverables]
    related_skills: [remotion-opus, manim-video, ascii-video, data-chart-rendering]
---

# Verifying a rendered video before you ship it

Trigger: any moment you are about to deliver a rendered video (Remotion, manim, ffmpeg/ASCII
pipelines, slideshow-to-MP4) to the user. The renderer's exit code says nothing about whether the
film is right. Deliver only after the checks below, and report the checks as evidence.

Rule of thumb: **the rendered clock is not your computed clock.** Everything here follows from that.

## 1. Machine facts first (`ffprobe`, per format)

```bash
ffprobe -v error -show_entries stream=codec_type,codec_name,width,height,r_frame_rate,duration \
        -show_entries format=duration,size -of default=noprint_wrappers=1 out.mp4
```

Confirm resolution, fps, video duration, **and that an audio stream exists**. Deliver every aspect
ratio the brief asked for (portrait + landscape ship together for social). Compare the measured
duration against the script's expectation (VO length + hold) — a mismatch is the first hint of
timeline drift, not a rounding error.

## 2. Locate boundaries empirically — never from cue-frame arithmetic

VO-driven timelines insert a small lead-in per line (observed ~0.1s on the Remotion/ElevenLabs
pipeline: a 6-line film rendered ~0.6s longer than `sum(line durations) + hold`). So a frame
extracted at a *computed* cue timestamp shows the **previous** line's caption/text, and it reads as
"content missing / mis-timed" when the film is fine.

- Extract frames bracketing the computed time (±0.5s, step ~0.3s) and find the transition by eye.
- Only after that, judge the transition. Never "fix" a timing bug you inferred from arithmetic alone.
- Confirm the end state: final frames of the film (end card complete, CTA and price legible).

## 3. Contact sheet for composition, full-res for legibility

`scripts/frame_sheet.sh <file> [sheet_out.jpg] [aspect] [t1 t2 …]` builds a 4×3 sheet plus
full-resolution frames. Use both, in that order:

- **Sheet** (scaled to ~400px tall): spotting gross defects — overlaps, clipped text, dead frames,
  a missing end card.
- **Full-res frame**: anything about small text. A sheet makes captions/chips look unreadable; that
  is a downscaling artifact, and calling it a defect wastes a full re-render.

## 4. Defects worth a re-render vs non-defects

| Looks wrong, isn't | Actually wrong → fix + re-render |
|---|---|
| a partial word mid-frame ("MA" of "MANGA") — the per-character reveal | a ~0.4s near-empty frame where the beat text fades out before the end-card text lands → cross-fade: start the lockup ~0.5s before the last VO cue instead of hard-cutting |
| a "sudden frame jump" warning at a beat boundary — your intentional cut | the final caption restating the CTA button text verbatim → reword the caption, keep the subtitle |
| one frame glimpsed through a fade | price/CTA/tagline clipped at an edge, or a caption bar overlapping the end card |
| text "missing" at a computed timestamp | text present at the wrong time (real drift) → re-render, then re-verify with §2 |

## 5. Content gates (do not ship without them)

- **Every on-screen number traces to a sourced fact** (facts file with source + date). No invented
  figures, no income/profit/sales claims, no superlatives a source doesn't support. An engine linter
  that rejects an unsourced number is reporting a real error, not an obstacle to route around.
- **Product name/price come from the user**, never from OCR of a blurry label.
- Any limitation the renderer cannot fix (voice accent, missing music, an upscaled/low-res source
  photo) goes into the delivery message as a disclosed limitation — not silently omitted.

## 6. Report shape

Lead with the artifact facts (duration, formats, fps, audio present), then what you personally
verified (frames inspected, transitions checked), then the honest limitations, then the file. Offer a
re-render only when a real defect exists, and say exactly which frame/segment is wrong.

## Pitfalls

- Extract **several** frames around a boundary — one frame is not evidence of a timing defect.
- A render still writing shows a partial file size (`ls`); wait for the process to exit before
  probing, or you will "verify" a truncated MP4.
- Multiple aspects render sequentially and can take ~10 min each on a 2-core box: start the render
  in the background with completion notification, and QA the finished aspect while the other renders.
- Re-rendering invalidates every frame already checked — verify the exact file you deliver.
