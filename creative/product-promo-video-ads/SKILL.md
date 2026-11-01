---
name: product-promo-video-ads
description: "Use when a product photo + price must become a promo video."
version: 1.0.0
metadata:
  hermes:
    tags: [video, promo, ads, umkm, product-photo, remotion, qa]
---

# Product promo video ads (from a photo the user sends)

Trigger: the user drops a product photo (food, drink, dessert jar, service, merch) plus a one-line description
and/or a price, and wants a **promo/ad video** — often for a small business (UMKM) or as a portfolio piece for
selling video services. Deliver **both aspect ratios** (9:16 + 16:9) and a ready-to-post caption.

Related: `remotion-opus` (hub skill) is the engine + `ros` CLI for this class. If installed, read it first and use
it for scaffold/audio/render; this skill covers what it does NOT: real product photography, ad layout, QA loop.

Kalau pertanyaannya bukan "render video ini" tapi "jualan video AI layak nggak, modal dan harga jualnya berapa",
stack + biaya per detik + tangga harga + kurikulum ada di `references/ai-video-generation-economics.md`.
Render berbasis kode (Remotion) dan render berbasis model generatif itu dua jalur biaya berbeda — jangan
campur angka keduanya.

## 1. Facts and claims — the part that gets you in trouble

- **Every number on screen must come from the user or a citable source.** A price the user typed ("manggo cheese
  15rb") is authoritative → render `Rp15.000`. Keep `facts.md` lines as `fact — source, date`.
- **Never invent marketing claims.** No "best seller", "bahan premium", "sejak 2015", no ingredient claims you
  cannot see or the user did not state, no sales/income/revenue figures, ever. Capability and appearance only.
- **The label in the photo is not automatically the client's brand.** A jar lid may read a different brand name,
  and small label text is usually illegible anyway. Ask, or use the product name the user said. When the user's
  words and your reading of the photo disagree (you saw chia pudding, they say "cheese"), **the user's words win** —
  rewrite the copy and re-generate the VO.
- Safe to use: price, product name, and ingredients the user stated or that are unmistakably visible.

## 2. First engineering question: can the engine place a photo at all?

Fixed/spec motion engines in this space render **typography, shapes and fake UI only** — no real photography.
Code mode often documents "no assets" too. Check the engine's asset rules before planning copy. If photos are not
supported, **author a custom scene** (your own component tree) instead of fighting the stock engines.
Component recipe + layout + patch patterns: `references/photo-scene-recipe.md`.

## 3. Source photo prep

- Images arriving through a chat platform are **recompressed** — a "500×500 px" original is common. Upscale with
  Lanczos + light sharpen before compositing so the 1080p card is not mush.
- Also **ask the user to resend as a FILE/document** (not as a photo) for full resolution, and say why: the
  recompressed source is the single biggest quality limiter of the final render. Offer the sharper re-render.
- Name the export limits honestly in the delivery ("source was 500×500, still a bit soft").

## 4. Workflow

1. Scaffold the project, set `language`, `fps`, `brand`.
2. Write `brief.md` (audience, single message, CTA, language) and `facts.md` (every on-screen number + source).
3. Pre-scale the photo into the project's `public/`.
4. Author the scene. Beats that work: hook → what's inside (ingredient chips that light up on the spoken word) →
   **price** → how to eat/use → end-card (name + tagline + price + CTA pill + small production credit). Keep a small
   persistent price badge in the back half so a screenshot of any late frame still carries the price.
5. VO: **reuse the engine's own ElevenLabs pipeline** (a throwaway helper script calling its module) so voice,
   model and normalisation match the proven spec-mode output. Rewrite a line rather than fight a pronunciation.
6. Static check the scene, then render in the **background with notify_on_complete** (~10 min per aspect on 2 cores).
7. QA with the loop in §5, fix, re-render, deliver.

## 5. QA loop — look at the film, twice

```bash
scripts/contact_sheet.sh out/<slug>-landscape.mp4     # 12-frame sheet
scripts/contact_sheet.sh out/<slug>-portrait.mp4
scripts/full_res_frames.sh out/<slug>-portrait.mp4 2.30 12.80 15.50   # verify a suspicion full-res
```

Read the sheets with `vision_analyze`, asking explicitly for defects: photo visible/sharp in every frame, text
clipped or overlapping, price correct and legible, caption-band collisions, empty or broken frames.

Two traps this loop sets for you:

- **A downscaled sheet makes normal text look unreadable and makes a mid-animation partial headline look like
  clipping.** Never "fix" legibility or clipping from a sheet alone — pull that timestamp at full res first. A
  truncated-looking headline is usually a per-character reveal caught mid-flight: harmless.
- **Portrait and landscape are different layouts.** Verify both; a portrait stack can collide (headline vs card)
  where landscape has room. Judge the end-card in both.

## 6. Timeline traps (measured, not theoretical)

- Cue-frame → seconds arithmetic can be **off by ~0.1s per VO line**: each rendered line carries a short lead-in,
  so over 6 lines the film runs ~0.5s longer than the sum of the word timings. Don't trust the arithmetic — extract
  frames and look before concluding a transition is mistimed.
- An engine's STT "brand MISSING" warning is a **false negative for multi-word brand names** ("Mango Cheese") — its
  phonetic match does not join words. Read the transcript: if the STT text clearly heard it, the audio is fine.
- Never hard-cut the last beat into the end-card: the beat text vanishes instantly while the end-card is still
  fading in, leaving a ~0.4s near-empty frame. **Cross-fade** — start the end-card window ~0.4s before the beat's
  fade-out ends and stagger its reveals (wordmark → tagline → price → CTA) so the product name lands on the spoken
  product name. Exact patch pattern in `references/photo-scene-recipe.md`.

## 7. Delivery

- Send **both** files with `MEDIA:/abs/path/...mp4` (9:16 for reels/shorts, 16:9 for feed/YouTube).
- State verified specs (duration, fps, resolutions, VO lines matched) from real `ffprobe` output, not memory.
- **Disclose the shortfalls in the same message**: source resolution, no music if the audio tier blocks it, TTS
  accent, and any claim you deliberately left out because it was unverifiable.
- Add a short ready-to-post caption (2–3 lines, casual, price + "pesan lewat DM"). Never state or imply sales.
- Close with the concrete next step the user can pick (sharper re-render once they send the original file, more
  variants), not with "mau gw buatkan?".

## Pitfalls

| symptom | cause / fix |
| --- | --- |
| product photo impossible in the stock scene | expected — author a custom code-mode scene (§2) |
| render "sudden frame jump" warnings | intentional beat cuts at those frames; confirm with a still, don't panic |
| `pkill -f "chrome-headless"` kills your own command | the pattern matches the shell running it — use `pkill -f "chrome[-]headless"` |
| long render wall-clock | background + `notify_on_complete`; skip other CPU work meanwhile; concurrency ≤ cores |
| blurry 1080p card | source was chat-recompressed → upscale + ask for the original file |
