#!/bin/sh
# Claude Code hook (PostToolUse on Skill, and UserPromptSubmit) that appends each skill use
# to ~/.claude/skill-usage.jsonl. Typed /skill-name commands never go through the Skill
# tool, so they are only caught from the prompt.
# Must print nothing: UserPromptSubmit stdout is injected into the conversation.

input=$(cat)
event=$(printf '%s' "$input" | jq -r '.hook_event_name // empty')
cwd=$(printf '%s' "$input" | jq -r '.cwd // empty')

if [ "$event" = "PostToolUse" ]; then
  skill=$(printf '%s' "$input" | jq -r '.tool_input.skill // empty')
  source=tool
else
  skill=$(printf '%s' "$input" | jq -r '.prompt // "" | capture("^/(?<n>[A-Za-z0-9_-]+)").n // empty')
  source=command
  # Built-in and plugin commands (/model, /clear) share the syntax; keep only real skills.
  [ -f "$HOME/.claude/skills/$skill/SKILL.md" ] || [ -f "$cwd/.claude/skills/$skill/SKILL.md" ] || skill=
fi

[ -n "$skill" ] || exit 0

jq -nc --arg skill "$skill" --arg cwd "$cwd" --arg source "$source" \
  --arg session "$(printf '%s' "$input" | jq -r '.session_id // empty')" \
  '{ts: (now | todate), skill: $skill, source: $source, cwd: $cwd, session: $session}' \
  >> "$HOME/.claude/skill-usage.jsonl" 2>/dev/null
exit 0
