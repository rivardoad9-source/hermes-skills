#!/usr/bin/env bash
# frame_sheet.sh — QA pass for a rendered video: one contact sheet (composition) + full-res frames
# (legibility) around a given timestamp.
#
#   bash frame_sheet.sh <file.mp4> [sheet_out.jpg] [aspect] [t1 t2 t3 ...]
#
# Default: 4x3 sheet across the whole film + full-res frames at 1/3 and 2/3 of the runtime.
# For a transition, pass the computed cue time and its neighbours, e.g.:
#   bash frame_sheet.sh out/land.mp4 /tmp/tr.jpg land 11.9 12.2 12.5 12.8
#
# Why: the rendered clock drifts from cue-frame arithmetic (~0.1s lead-in per VO line), so always
# look at SEVERAL frames around a boundary before calling it a defect.
set -euo pipefail

F="${1:?usage: frame_sheet.sh <file.mp4> [sheet_out.jpg] [aspect] [t...]}"
SHEET="${2:-/tmp/sheet.jpg}"
ASPECT="${3:-land}"
shift || true; shift || true; shift || true
TS=("$@")

command -v ffmpeg  >/dev/null || { echo "ffmpeg missing"; exit 1; }
command -v ffprobe >/dev/null || { echo "ffprobe missing"; exit 1; }

DUR=$(ffprobe -v error -show_entries format=duration -of csv=p=0 "$F")
W=$(ffprobe -v error -select_streams v -show_entries stream=width  -of csv=p=0 "$F" | head -1)
H=$(ffprobe -v error -select_streams v -show_entries stream=height -of csv=p=0 "$F" | head -1)
FPS=$(ffprobe -v error -select_streams v -show_entries stream=r_frame_rate -of csv=p=0 "$F" | head -1)
HAS_AUDIO=$(ffprobe -v error -select_streams a -show_entries stream=codec_name -of csv=p=0 "$F" | head -1)

echo "file   : $F"
echo "video  : ${W}x${H} @ ${FPS} fps · ${DUR}s"
if [ -z "$HAS_AUDIO" ]; then echo "audio  : *** NO AUDIO STREAM ***"; else echo "audio  : $HAS_AUDIO"; fi

# 1) composition pass — 12 frames tiled 4x3
ffmpeg -y -loglevel error -i "$F" \
  -vf "fps=12/${DUR},scale=480:-1,tile=4x3" -frames:v 1 "$SHEET"
echo "sheet  : $SHEET  (composition only; small text is NOT judgeable here)"

# 2) legibility pass — full-resolution frames
if [ "${#TS[@]}" -eq 0 ]; then
  TS=("$(awk -v d="$DUR" 'BEGIN{printf "%.2f", d/3}')" "$(awk -v d="$DUR" 'BEGIN{printf "%.2f", 2*d/3}')")
fi
for t in "${TS[@]}"; do
  out="/tmp/${ASPECT}_${t}.png"
  ffmpeg -y -loglevel error -ss "$t" -i "$F" -frames:v 1 "$out"
  echo "frame  : $out   (t=$t)"
done

# 3) end state — last frame, where the CTA/price/wordmark must be complete and unclipped
tail_t=$(awk -v d="$DUR" 'BEGIN{printf "%.2f", (d>0.4)? d-0.25 : 0}')
ffmpeg -y -loglevel error -ss "$tail_t" -i "$F" -frames:v 1 "/tmp/${ASPECT}_end.png"
echo "end    : /tmp/${ASPECT}_end.png  (t=$tail_t)"

cat <<'NOTE'

Now inspect: sheet for overlaps / clipping / dead frames; full-res frames for legibility; end frame
for a complete CTA. A single frame is not evidence of a timing defect — check the neighbours too.
NOTE
