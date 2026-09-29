#!/bin/sh
# One-time: install puppeteer-core into a private cache (Chrome itself is used from /Applications).
set -e
d="$HOME/.cache/short-skill"
[ -d "$d/node_modules/puppeteer-core" ] && { echo "ready: $d"; exit 0; }
mkdir -p "$d"; cd "$d"; [ -f package.json ] || npm init -y >/dev/null
npm i puppeteer-core >/dev/null 2>&1
echo "installed: $d"
