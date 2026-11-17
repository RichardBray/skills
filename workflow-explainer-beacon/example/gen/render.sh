#!/bin/bash
cd "$(dirname "$0")/.."; node gen/build.mjs
export AGENT_BROWSER_SESSION="jh-$$"
agent-browser set viewport 1080 1920 >/dev/null
N=$(python3 -c "import json;print(len(json.load(open('scenes.json'))))")
for ((i=0;i<N;i++)); do
  f=s$i
  agent-browser open file://$PWD/$f.html >/dev/null; sleep 0.9
  agent-browser eval "JSON.stringify([...document.querySelectorAll('[data-layer]')].map(e=>{const r=e.getBoundingClientRect();return [e.dataset.layer,r.x,r.y,r.width,r.height]}))" | tr -d '\\' | sed 's/^"//;s/"$//' > raw-$f.json
  python3 - $f <<'PY'
import json,sys,math
f=sys.argv[1]; raw=json.load(open(f'raw-{f}.json')); out=[]
for id,x,y,w,h in raw:
    x0=max(0,math.floor(x-8)); y0=max(0,math.floor(y-8)); x1=min(1080,math.ceil(x+w+24)); y1=min(1920,math.ceil(y+h+24))
    out.append([id,x0,y0,x1-x0,y1-y0])
json.dump(out,open(f'rects-{f}.json','w'))
open(f'crops-{f}.txt','w').write('\n'.join(f'{a} {b} {c} {d} {e}' for a,b,c,d,e in out)+'\n')
PY
  agent-browser eval "document.querySelectorAll('[data-layer]').forEach(e=>e.style.visibility='hidden')" >/dev/null
  agent-browser screenshot $PWD/$f-base.png >/dev/null
  while read id x y w h; do
    for bg in white black; do
      agent-browser eval "document.getElementById('bg').style.visibility='hidden';document.body.style.background='$bg';document.querySelectorAll('[data-layer]').forEach(e=>e.style.visibility=e.dataset.layer=='$id'?'visible':'hidden')" >/dev/null
      agent-browser screenshot $PWD/tmp-$bg.png >/dev/null
      ffmpeg -loglevel error -y -i tmp-$bg.png -vf "crop=$w:$h:$x:$y" tmpc-$bg.png
    done
    ffmpeg -loglevel error -y -i tmpc-white.png -i tmpc-black.png -filter_complex "[0:v]format=gray[w];[1:v]format=gray[b];[w][b]blend=all_expr='255-(A-B)'[a];[1:v]format=rgb24[c];[c][a]alphamerge" $PWD/$f-$id.png
  done < crops-$f.txt
done
agent-browser close >/dev/null 2>&1; rm -f tmp-white.png tmp-black.png tmpc-white.png tmpc-black.png raw-*.json crops-*.txt; ls s*-*.png | wc -l
