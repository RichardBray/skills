#!/bin/bash
# usage: recolor-pink.sh <folder> <scene> <layer>  -> <folder>/s<scene>-<layer>-orange.png
set -e
d=$1; i=$2; id=$3
cd "$d"
sed -e 's/\.stk{position:absolute;background:#ff6fa8;color:#141414;/.stk{position:absolute;background:#fa5d19;color:#ffffff;/' -e 's/background:#ff6fa8;color:#141414;/background:#fa5d19;color:#ffffff;/g' s$i.html > s$i-orange.html
read x y w h < <(python3 -c "import json;r=[a for a in json.load(open('rects-s$i.json')) if a[0]=='$id'][0];print(*r[1:])")
export AGENT_BROWSER_SESSION=rc$$
agent-browser set viewport 1080 1920 >/dev/null
agent-browser open file://$PWD/s$i-orange.html >/dev/null; sleep 0.9
for bg in white black; do
  agent-browser eval "document.getElementById('bg').style.visibility='hidden';document.body.style.background='$bg';document.querySelectorAll('[data-layer]').forEach(e=>e.style.visibility=e.dataset.layer=='$id'?'visible':'hidden')" >/dev/null
  agent-browser screenshot $PWD/rc-$bg.png >/dev/null
  ffmpeg -loglevel error -y -i rc-$bg.png -vf "crop=$w:$h:$x:$y" rcc-$bg.png
done
agent-browser close >/dev/null 2>&1
ffmpeg -loglevel error -y -i rcc-white.png -i rcc-black.png -filter_complex "[0:v]format=gray[w];[1:v]format=gray[b];[w][b]blend=all_expr='255-(A-B)'[a];[1:v]format=rgb24[c];[c][a]alphamerge" s$i-$id-orange.png
echo "$d/s$i-$id-orange.png ${w}x${h}"
