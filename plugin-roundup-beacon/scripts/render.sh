#!/bin/bash
# usage: [SCENES="hook s1 ..."] render.sh <video-dir>
# Renders every [data-layer] of each page to its own PNG and measures it into rects-<scene>.json.
# The hook runs twice: the first pass measures the "N noun." text, the second sizes the black bar to it.
set -e
HERE="$(cd "$(dirname "$0")" && pwd)"
DIR="$(cd "${1:?video dir}" && pwd)"
cd "$DIR"
cp -n "$HERE"/assets/* . 2>/dev/null || true
export AGENT_BROWSER_SESSION="roundup-$$"

shoot() {
  for f in "$@"; do
    agent-browser open "file://$DIR/$f.html" >/dev/null; sleep 0.9
    agent-browser eval "document.querySelectorAll('[data-layer]').forEach(e=>e.style.visibility='hidden')" >/dev/null
    agent-browser screenshot "$DIR/$f-base.png" >/dev/null
    ids=$(agent-browser eval "JSON.stringify([...document.querySelectorAll('[data-layer]')].map(e=>e.dataset.layer))" | tr -d '"\\' | sed 's/^\[//;s/\]$//' | tr ',' ' ')
    for id in $ids; do
      agent-browser eval "document.querySelectorAll('[data-layer]').forEach(e=>e.style.visibility=e.dataset.layer=='$id'?'visible':'hidden')" >/dev/null
      agent-browser screenshot "[data-layer=$id]" "$DIR/$f-$id.png" >/dev/null
    done
    agent-browser eval "document.querySelectorAll('[data-layer]').forEach(e=>e.style.visibility='visible');JSON.stringify([...document.querySelectorAll('[data-layer]')].map(e=>{const r=e.getBoundingClientRect();return [e.dataset.layer,Math.round(r.x*10)/10,Math.round(r.y*10)/10,Math.round(r.width*10)/10,Math.round(r.height*10)/10]}))" | tr -d '\\' | sed 's/^"//;s/"$//' > "rects-$f.json"
  done
}

rm -f rects-hook.json
node "$HERE/core.mjs" "$DIR"
agent-browser set viewport 1080 1920 >/dev/null
shoot hook
node "$HERE/core.mjs" "$DIR"
REST=" ${SCENES:-s1 s2 s3 s4 s5 end} "; REST="${REST// hook / }"
shoot hook $REST
agent-browser close >/dev/null 2>&1 || true
ls *.png | wc -l
