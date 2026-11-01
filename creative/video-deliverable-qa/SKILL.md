---
name: video-deliverable-qa
description: Use before delivering a rendered video; frame QA.
---

# QA a rendered video before delivering it

Trigger: you rendered a promo/ad/explainer video (any engine) and are about to send
it. You cannot watch the file, so verify it frame-by-frame with ffmpeg + vision, then
report specs and honest limits.

## 1. Verify specs with ffprobe (never claim them from memory)
```bash
ffprobe -v error -select_streams v -show_entries stream=width,height,r_frame_rate -of csv=p=0 out.mp4
ffprobe -v error -show_entries format=duration,size -of csv=p=0 out.mp4
```
Resolution, fps, duration, presence of an audio stream. Report these as measured.

## 2. Contact sheet per aspect, reviewed against a defect list
```bash
ffmpeg -y -i out.mp4 -vf "fps=12/<DURATION>,scale=480:-1,tile=4x3" -frames:v 1 /tmp/sheet.jpg
```
Then vision-review with an explicit checklist: text clipped / cut at edges /
overlapping the subject; number (price) present and correct; caption bar collisions;
missing or empty frames; misaligned or "unfinished" end card. 12 frames ≈ enough for
an 18s film; review landscape and portrait separately — defects are per-aspect.

## 3. Re-check every reported defect at full resolution BEFORE changing anything
Contact sheets are downscaled, so vision frequently reports "text too small /
illegible" or "overlap" that does NOT exist at native size. Extract the suspect
timestamps and look again:
```bash
ffmpeg -y -ss <T> -i out.mp4 -frames:v 1 /tmp/f.png
```
Acting on a false positive costs a full re-render. Most "illegible" reports vanish
here; a partial headline ("MAN", "MAnY") is a mid-animation reveal, not a defect.

## 4. Check scene transitions for dead air
Sample t-0.3 / t / t+0.3 around every scene change into one grid. A frame showing
only persistent labels + caption with no content = dead-air frame. Fix with a
cross-fade (start the incoming scene earlier, fade the outgoing text instead of hard
cutting, clear side chips sooner) rather than shifting the whole timeline. Ghosting
of outgoing text during a ~0.2s cross-dissolve is acceptable; an empty frame is not.

## 5. Copy-level checks
- End card: caption bar repeating the CTA button wording reads sloppy ("PESAN LEWAT
  DM" + "pesan lewat DM" in the subtitle) — make the caption complementary.
- Every on-screen number must trace to the brief/facts source. Never invent figures,
  ratings, or claims to fill a frame.
- Confirm captions agree with the spoken text after any script edit.

## 6. Deliver with evidence, not praise
State measured specs, what you checked, and the real limitations (source photo
resolution after upscale, no music, TTS accent, anything unverified). A delivery that
names its own weak points is worth more than one that claims perfect.

## Support files
- `references/remotion-code-mode-notes.md` — engine-specific notes for the
  remotion-opus pipeline (photo-driven code-mode scenes, cue timing drift, render cost).
