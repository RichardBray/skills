#!/bin/sh
# Symlink every skill in this repo into each Claude Code config dir, so edits here are live
# with no install or sync step. Rerun after adding a skill.
#
# Usage: scripts/link.sh [config-dir ...]   (default: ~/.claude ~/.claude-work)

repo=$(cd "$(dirname "$0")/.." && pwd)
[ $# -gt 0 ] || set -- "$HOME/.claude" "$HOME/.claude-work"

for config in "$@"; do
  [ -d "$config" ] || { echo "skip $config (not found)"; continue; }
  mkdir -p "$config/skills"
  for skill_md in "$repo"/*/SKILL.md; do
    name=$(basename "$(dirname "$skill_md")")
    target="$config/skills/$name"
    if [ -d "$target" ] && [ ! -L "$target" ]; then
      echo "skip $target (real directory, move it aside first)"
      continue
    fi
    ln -sfn "$repo/$name" "$target"
  done
  echo "linked $config/skills"
done

# `npx skills update` would reinstall these from GitHub over the links, so stop it tracking them.
lock="$HOME/.agents/.skill-lock.json"
if [ -f "$lock" ] && command -v jq >/dev/null; then
  jq '.skills |= with_entries(select(.value.source != "RichardBray/skills"))' "$lock" > "$lock.tmp" \
    && mv "$lock.tmp" "$lock"
fi
