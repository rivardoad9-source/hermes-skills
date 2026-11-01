# Photo-driven promo scene — component recipe and patch patterns

Context: the fixed engines render text/fake-UI only, so a real product photo needs a bespoke scene. Concrete
instance that shipped: a 18.15s, 60fps, 1920×1080 + 1080×1920 food ad for a dessert jar (photo + Rp15.000),
built on the `remotion-opus` engine's code mode with a custom `projects/<slug>/scene/index.tsx`.

## Scene skeleton (one component tree, one continuous "world")

- **Backdrop**: photo blown up huge + heavy blur + dark brown/warm gradient + vignette; a low-opacity grain
  overlay (`opacity: 0.06`) sells it as film rather than flat vector.
- **Product card**: the real photo in a rounded, bordered card with shadow. The "camera" IS the card transform —
  keyframe card center-x/center-y/size and an inner `zoom`/`offsetX`/`offsetY` (object-position style) so you get
  push-ins onto layers (cream → jelly → mango) without a second asset.
- **Persistent chrome**: product name top-left, small price badge top-right in the back half (so any late-frame
  screenshot still shows the price), production credit bottom-right (never inside the caption band).
- **Caption band**: the spoken line as a bottom pill, current word tinted. Driven by the engine's word timings.
- **End-card**: wordmark, one-line tagline, `HARGA` + price, filled CTA pill, credit. Stagger the reveals.

## Timing model

- All animation values are frame numbers at the project fps (60). `prog(t, a, b)` = 0→1 between frames a and b;
  a reveal of 22 frames ≈ 0.37s feels right for a headline, 12 frames for a chip.
- Cues come from the VO word timings: `vo.cue('m02:mangga')` = the frame the word "mangga" is spoken in line m02 —
  use the SPOKEN text tokens (not the caption spelling) and prefer a token unique to that line.
- Beats array = `{ at, to, kicker, head, sub }` positioned as one panel; chips light up on their own cue.
- **Measured trap**: the rendered film ran ~0.5s longer than the sum of the word timings (≈0.1s lead-in per VO
  line). Cue frames therefore sit ~0.1s-per-line LATER in the wall clock than naive arithmetic suggests. Verify
  transitions by extracting frames, never by computing seconds.

## Cross-fade the last beat → end-card (fixes the empty-frame defect)

Symptom: a hard cut of the beat text (`opacity: lockup ? 0 : 1`) while the end-card is still fading in leaves a
~0.4s frame with almost nothing on screen — the reviewer flags it as "the end-card hasn't assembled yet".

Fix, in one V4A patch over the scene file:

1. Start the lockup window earlier: `const lockup = t >= f6 - 30;` (was `f6 - 10`).
2. Fade out the beat text and the chips slightly earlier than the lockup lands:
   chips `opacity: 1 - prog(t, f6 - 40, f6 - 30)`, corner labels `1 - prog(t, f6 - 38, f6 - 28)`.
3. Stagger the end-card reveals so the product name lands on the spoken product name:
   wordmark `at={f6 - 26}`, tagline `prog(t, f6 - 16, f6 + 4)`, price `prog(t, f6 - 10, f6 + 10)`,
   CTA pill `at={f6 - 4}`, credit `prog(t, f6 + 8, f6 + 28)`.

Result: no empty frame; the old headline ghosts out over ~0.2s while the wordmark fades in — a normal dissolve.

## VO without touching the engine's modules

Write a throwaway `tmp_<slug>_audio.ts` at the repo root that imports the engine's own audio module and calls it
with the same voice/model/normalisation the spec path uses, run it with `npx tsx tmp_<slug>_audio.ts`. It prints
per-line STT hit ratios and writes `words.json` (per-line durations + word offsets) that the scene reads for cues.
Delete the throwaway afterwards. Rewriting one line = re-run the script; keep line ids (`m01`…`m06`) stable.

- Voice picks are constrained by the account tier: a free ElevenLabs tier may refuse library voices and music
  (402). With only a premade US-accent voice available, expect an accent on Indonesian copy — disclose it.
- Keep number phrasing as words in the VO (`lima belas ribu`) and the digits on screen, and put the price in
  `facts.md` in both forms so any number check passes.
- The engine's "brand MISSING" STT warning is a false negative for multi-word brand names — read the transcript
  instead of the flag.

## Report honestly

`ffprobe` both outputs before delivering (codec, resolution, fps, duration) and quote only what it printed. List
what you did NOT do: no music, accent, source resolution, claims you refused to invent.
