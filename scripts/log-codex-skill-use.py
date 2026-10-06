#!/usr/bin/env python3
"""Log observable Codex skill loads from hook events without storing prompts."""

import datetime
import json
import pathlib
import re
import sys


SKILL_PATH = re.compile(r"(?:^|[/\\])([A-Za-z0-9_.:-]+)[/\\]SKILL\.md\b")
SLASH_SKILL = re.compile(r"^/([A-Za-z0-9_-]+)\b")
CONFIG_DIR = pathlib.Path.home() / ".codex"
LOG_PATH = CONFIG_DIR / "skill-usage.jsonl"


def main() -> None:
    try:
        event = json.load(sys.stdin)
        kind = event.get("hook_event_name")
        skill = None
        source = None
        if kind == "PostToolUse":
            tool_input = event.get("tool_input", {})
            # A path in the tool arguments is observable evidence of loading a skill.
            matches = SKILL_PATH.findall(json.dumps(tool_input, ensure_ascii=False))
            if matches:
                skill = matches[-1]
                source = "skill-file-read"
        elif kind == "UserPromptSubmit":
            match = SLASH_SKILL.match(event.get("prompt", ""))
            if match:
                candidate = match.group(1)
                roots = (
                    CONFIG_DIR / "skills" / candidate / "SKILL.md",
                    pathlib.Path.home() / ".agents" / "skills" / candidate / "SKILL.md",
                    pathlib.Path.home() / "skills" / candidate / "SKILL.md",
                    pathlib.Path(event.get("cwd") or ".") / ".agents" / "skills" / candidate / "SKILL.md",
                )
                if any(path.is_file() for path in roots):
                    skill = candidate
                    source = "slash-command"
        if not skill:
            return
        record = {
            "ts": datetime.datetime.now(datetime.timezone.utc).isoformat(),
            "skill": skill,
            "source": source,
            "cwd": event.get("cwd", ""),
            "session": event.get("session_id", ""),
        }
        with LOG_PATH.open("a", encoding="utf-8") as stream:
            stream.write(json.dumps(record, ensure_ascii=False) + "\n")
    except (OSError, ValueError, TypeError):
        # Telemetry must never interrupt the user's task.
        return


if __name__ == "__main__":
    main()
