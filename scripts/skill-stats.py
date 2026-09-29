#!/usr/bin/env python3
"""Count skill usage from the hook log, backfilled from Claude Code transcripts.

Usage: python3 scripts/skill-stats.py [--days N] [--config DIR ...]
"""

import argparse
import json
import re
from collections import Counter
from datetime import datetime, timedelta, timezone
from pathlib import Path

DEFAULT_CONFIGS = [Path.home() / ".claude", Path.home() / ".claude-work"]
REPO = Path(__file__).resolve().parent.parent
COMMAND = re.compile(r"<command-name>/([A-Za-z0-9_-]+)</command-name>")


def parse_ts(value):
    return datetime.fromisoformat(value.replace("Z", "+00:00"))


def read_jsonl(path):
    with path.open(errors="replace") as f:
        for line in f:
            try:
                yield json.loads(line)
            except json.JSONDecodeError:
                continue


def from_log(config):
    log = config / "skill-usage.jsonl"
    if not log.exists():
        return []
    return [(parse_ts(e["ts"]), e["skill"]) for e in read_jsonl(log) if e.get("skill")]


def installed_skills(config):
    dirs = [config / "skills", REPO]
    return {p.parent.name for d in dirs for p in d.glob("*/SKILL.md")}


def from_transcripts(config):
    known = installed_skills(config)
    uses = []
    for path in (config / "projects").rglob("*.jsonl"):
        for entry in read_jsonl(path):
            if "timestamp" not in entry:
                continue
            content = (entry.get("message") or {}).get("content")
            if isinstance(content, str):
                match = COMMAND.search(content)
                if match and match.group(1) in known:
                    uses.append((parse_ts(entry["timestamp"]), match.group(1)))
                continue
            if not isinstance(content, list):
                continue
            for block in content:
                if (
                    isinstance(block, dict)
                    and block.get("type") == "tool_use"
                    and block.get("name") == "Skill"
                    and block.get("input", {}).get("skill")
                ):
                    uses.append((parse_ts(entry["timestamp"]), block["input"]["skill"]))
    return uses


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--days", type=int, help="only count the last N days")
    parser.add_argument("--config", type=Path, nargs="+", default=DEFAULT_CONFIGS,
                        help="Claude config dirs to read (default: ~/.claude ~/.claude-work)")
    args = parser.parse_args()
    configs = [c for c in args.config if c.is_dir()]
    cutoff = args.days and datetime.now(timezone.utc) - timedelta(days=args.days)

    uses, n_logged, n_backfill = [], 0, 0
    for config in configs:
        logged = from_log(config)
        # Transcripts overlap the log once the hook is installed, so only backfill before it.
        log_start = min((ts for ts, _ in logged), default=None)
        backfill = [u for u in from_transcripts(config) if log_start is None or u[0] < log_start]
        if cutoff:
            logged = [u for u in logged if u[0] >= cutoff]
            backfill = [u for u in backfill if u[0] >= cutoff]
        n_logged += len(logged)
        n_backfill += len(backfill)
        uses += [(ts, skill, config.name) for ts, skill in logged + backfill]

    counts = Counter(skill for _, skill, _ in uses)
    per_config = Counter((skill, profile) for _, skill, profile in uses)
    last_used = {}
    for ts, skill, _ in uses:
        last_used[skill] = max(ts, last_used.get(skill, ts))

    names = [c.name for c in configs]
    width = max((len(s) for s in counts), default=5)
    print(f"{'skill':<{width}}  {'total':>5}  " + "  ".join(f"{n:>12}" for n in names) + "  last used")
    for skill, n in counts.most_common():
        cols = "  ".join(f"{per_config[skill, name]:>12}" for name in names)
        print(f"{skill:<{width}}  {n:>5}  {cols}  {last_used[skill]:%Y-%m-%d}")

    repo_skills = {p.parent.name for p in REPO.glob("*/SKILL.md")}
    unused = sorted(repo_skills - {s.split(":")[-1] for s in counts})
    if unused:
        print(f"\nNever used ({len(unused)}): {', '.join(unused)}")

    oldest = min((ts for ts, _, _ in uses), default=None)
    if oldest:
        print(f"\nData since {oldest:%Y-%m-%d} ({n_logged} logged, {n_backfill} from transcripts)")


if __name__ == "__main__":
    main()
