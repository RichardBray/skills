#!/bin/sh
# A page as a phone shows it: 400 CSS px wide at 2x density (800 px PNG).
# Usage: screenshot.sh <out.png> <url> [height_css=1400] [width_css=400]
set -e
out=$1; url=$2; h=${3:-1400}; w=${4:-400}
bin=$(ls -d "$HOME"/Library/Caches/ms-playwright/chromium_headless_shell-*/chrome-headless-shell-*/chrome-headless-shell 2>/dev/null | sort | tail -1)
[ -n "$bin" ] || { echo "no headless Chromium: bunx playwright install chromium-headless-shell" >&2; exit 1; }
ua="Mozilla/5.0 (iPhone; CPU iPhone OS 18_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/18.0 Mobile/15E148 Safari/604.1"
"$bin" --headless --disable-gpu --hide-scrollbars --force-device-scale-factor=2 \
  --window-size="$w,$h" --virtual-time-budget=9000 --user-agent="$ua" --screenshot="$out" "$url" 2>/dev/null
echo "$out"
