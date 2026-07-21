# Live sessions (wezterm panes)

A live pane is a real, separate, long-lived terminal session running a model's interactive CLI.
Either the user talks to it directly, or the orchestrator drives it via `send-text`/`get-text`.
It is not cold-started per message; it keeps its own conversation state across turns and stays open until explicitly closed.
Works for any interactive CLI, not just Claude models.

## Spawning

```bash
wezterm cli split-pane --right --percent 40 -- claude --model claude-fable-5     # Claude, any model
wezterm cli split-pane --right --percent 40 -- opencode -m zai-coding-plan/glm-5.2  # glm-5.2
wezterm cli spawn --new-window -- <same commands>   # separate window instead of split
```

## Driving it programmatically

`wezterm cli send-text --pane-id <id> --no-paste "<text>"` then a bare `\r` to submit.
The text and the Enter must be sent as two separate calls - a trailing `\r` on the first call does not reliably submit.

`wezterm cli get-text --pane-id <id>` reads the pane back.
`get-text` isn't app-aware - it just dumps wezterm's mux-server copy of the pane's rendered terminal screen (like a scrollback capture).
It works identically regardless of what CLI is running inside, and the app itself has no idea its output is being read.

## Scrollback caveat

`--start-line`/`--end-line` (negative values reach into scrollback) can pull the whole history in one call instead of reading turn-by-turn.
But TUIs that redraw in place (`claude`, `opencode`, `codex`) repaint the same screen rows each turn rather than appending linearly, so older turns in scrollback can be partial or overwritten, and anything past wezterm's configured scrollback depth is gone.
For a long session, the app's own on-disk history (`claude --resume`, `opencode session`, codex's session log) is the more reliable transcript than scraping the buffer.

## Default: never close a pane you opened

`wezterm cli kill-pane --pane-id <id>` only runs when the user explicitly says to close it (or names it by pane id/description) - not automatically after a test, not "since it's done," not as tidy-up at the end of a task.
Leaving it open is the point: the user asked for a persistent session, and persistent means it survives until they end it, not until the orchestrator decides the demo is over.
If several panes pile up and it's unclear which to close, ask which one rather than guessing.

## Why couriers stay the default

- Couriers background and parallelize; N panes means N terminals to poll one `get-text` at a time, burning orchestrator turns.
- Courier output is bounded at the source; a pane streams the full TUI (box-drawing, token/cost counters, MCP status), which is noisy to parse back into a usable answer.
- Couriers work headless (CI, SSH, no GUI); panes need a real terminal mux running locally.

Reach for a pane specifically when the user wants to watch or drive a model live themselves, or explicitly asks for a persistent session - not as a substitute for the couriers in a normal delegation flow.
