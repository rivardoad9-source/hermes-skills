#!/usr/bin/env bash
# Build ONE contact sheet (default 12 frames) from a rendered video so an agent can *look* at the film.
# usage: contact_sheet.sh <video.mp4> [frames=12] [out=/tmp/<name>_sheet.jpg]
# Reads duration + orientation via ffprobe; tiles 4x3 for landscape, 3x4 for portrait.
set -euo pipefail
f="${1:?usage: contact_sheet.sh <video.mp4> [frames=12] [out.jpg]}"
n="${2:-12}"
out="${3:-/tmp/$(basename "${f%.*}")_sheet.jpg}"

dur=$(ffprobe -v error -show_entries format=duration -of csv=p=0 "$f")
w=$(ffprobe -v error -select_streams v:0 -show_entries stream=width  -of csv=p=0 "$f" | head -1)
h=$(ffprobe -v error -select_streams v:0 -show_entries stream=height -of csv=p=0 "$f" | head -1)
fps=$(awk -v n="$n" -v d="$dur" 'BEGIN{ if (d<=0) d=1; printf "%.5f", n/d }')

if [ "$w" -ge "$h" ]; then tile=4x3; scale=480:-1; else tile=3x4; scale=-1:420; fi

ffmpeg -y -loglevel error -i "$f" -vf "fps=$fps,scale=$scale,tile=$tile" -frames:v 1 "$out"
echo "$out"
