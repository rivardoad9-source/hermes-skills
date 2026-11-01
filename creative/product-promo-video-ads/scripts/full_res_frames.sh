#!/usr/bin/env bash
# Extract FULL-RESOLUTION single frames at given timestamps — use to confirm/refute a defect that a
# downscaled contact sheet only *suggested* (legibility, clipped text, layout collision).
# usage: full_res_frames.sh <video.mp4> <t1> [t2 ...]        e.g. full_res_frames.sh out/p.mp4 2.30 12.80 15.50
# writes /tmp/fr_<basename>_<t>.png and prints the paths.
set -euo pipefail
f="${1:?usage: full_res_frames.sh <video.mp4> <t1> [t2 ...]}"; shift
base=$(basename "${f%.*}")
for t in "$@"; do
  out="/tmp/fr_${base}_${t}.png"
  ffmpeg -y -loglevel error -ss "$t" -i "$f" -frames:v 1 "$out"
  echo "$out"
done
