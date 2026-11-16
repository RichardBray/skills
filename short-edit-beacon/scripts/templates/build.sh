#!/bin/sh
# usage: build.sh <gfx dir with the page and its raw/ assets> <page name without .html> <seconds>
# Renders the page frame by frame and encodes ../<name>.mp4 next to the gfx dir.
set -e
G=$1; n=$2; d=$3
B=/Users/robray/beacon/packages/engine/third-party/out/bin
S=/Users/robray/skills/short-edit-beacon/scripts
rm -rf "$G/frames/$n"
bun "$S/render-html.ts" "$G/$n.html" "$G/frames/$n" "$d" >/dev/null
"$B/ffmpeg" -v error -y -framerate 30 -i "$G/frames/$n/f%04d.png" -c:v hevc_videotoolbox -q:v 80 -tag:v hvc1 -pix_fmt yuv420p "$G/../$n.mp4" && echo "$n done"
