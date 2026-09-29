# Skills repo

## Git
- Work directly on `main`. Never create feature branches.
- Commit often, in small self-contained steps, so any change can be reverted on its own.
- Stage only the files you changed. Leave unrelated uncommitted work alone.

## Skills are live
- Every skill here is symlinked into `~/.claude/skills` and `~/.claude-work/skills` by `scripts/link.sh`, so edits take effect in new sessions immediately. Don't leave a skill half-edited.
- After adding a skill, run `scripts/link.sh`.
