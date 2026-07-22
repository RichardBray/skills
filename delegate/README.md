# delegate

A [Claude Code](https://claude.com/claude-code) skill that turns the main agent into an orchestrator.
It splits a task into subtasks and routes each one to the cheapest model that meets the quality bar - GLM 5.2, GPT via Codex, Grok 4.5 via Grok Build, or Claude subagents (including Fable 5) - then verifies the results before integrating them.

## What's inside

- `SKILL.md` - the skill: a model routing table (cost / intelligence / taste), routing rules, invocation mechanics, and a six-step orchestration workflow.
- `agents/glm-runner.md`, `agents/codex-runner.md`, `agents/grok-runner.md`, and `agents/fable-runner.md` - courier agents.
  Thin Haiku subagents that wrap the external CLIs so they behave like first-class Claude Code subagents: agent UI, background runs, parallelism, follow-up messages.
  `fable-runner` is the exception - Fable 5 is a Claude model, so it runs the task directly via `model: fable` rather than relaying to an external CLI.

## Prerequisites

- [opencode](https://opencode.ai) CLI authenticated with a Z.AI coding plan (for GLM 5.2).
- [codex](https://github.com/openai/codex) CLI logged in with a ChatGPT plan or OpenAI API key (for GPT).
- [Grok Build](https://x.ai) CLI (`grok`) logged in with an xAI plan (for Grok 4.5).
- Missing one? The skill routes around it with the models you have.

## Install

Via [skills.sh](https://skills.sh):

```bash
npx skills add https://github.com/RichardBray/skills --skill delegate
```

Or manually:

```bash
git clone https://github.com/RichardBray/skills
ln -s "$(pwd)/skills/delegate" ~/.claude/skills/delegate
cp skills/delegate/agents/*.md ~/.claude/agents/
```

Start a new Claude Code session and the skill plus all couriers register automatically.

## Usage

Say things like:

- "delegate: migrate these 40 test files to vitest"
- "have glm implement the endpoints from this spec"
- "get codex to review this diff as a second opinion"
- "escalate this one to fable, it's a hard debugging problem"

The routing table assumes flat-rate subscriptions on all providers.
If your billing differs (e.g. per-token API keys), adjust the cost column in `SKILL.md` - it's a starting hypothesis, not gospel.

## Live sessions (wezterm panes)

Couriers are the default: fire-and-forget, one prompt in, one bounded answer back, backgroundable and parallelizable.
For a genuinely different job - a persistent, visible session you (or the orchestrator) talk to turn-by-turn instead of one-shot - spin up the model's own interactive CLI in a real terminal pane via [WezTerm](https://wezterm.org)'s `wezterm cli`:

```bash
wezterm cli split-pane --right --percent 40 -- claude --model claude-fable-5        # Fable 5
wezterm cli split-pane --right --percent 40 -- opencode -m zai-coding-plan/glm-5.2  # GLM 5.2
```

The orchestrator can drive it (`send-text` to type, `get-text` to read the rendered pane back - this just reads wezterm's terminal buffer, it's not app-aware) or you can type into it directly. It stays open until you close it with `wezterm cli kill-pane --pane-id <id>`. See `SKILL.md` for the full mechanics and why this isn't the default.

`get-text` works identically no matter what's running in the pane - `claude`, `opencode`, a plain shell. Wezterm's mux server keeps a screen buffer per pane: a grid of characters (plus color/style) that mirrors exactly what's currently drawn on screen, updated as the program inside writes to it. `get-text` just serializes that grid to plain text. It has no awareness of the app running inside - it's reading the terminal, not the process - so a Claude Code pane and a GLM pane are read the exact same way.

Example prompt:

> Open a live GLM 5.2 session in a wezterm pane, split to the right. Don't close it until I say so.

That's a request for the pane shape specifically - as opposed to "have glm do X," which stays a normal one-shot courier call.

**Drawback:** `get-text` reads scrollback too (`--start-line`/`--end-line`, negative values reach backwards), so a whole session's history can be pulled in one call. But TUIs like `claude`/`opencode`/`codex` redraw the same screen rows each turn instead of appending linearly, so older turns in scrollback can come back partial or overwritten, and anything past wezterm's scrollback depth is gone for good. For a long-running session, trust the app's own history (`claude --resume`, `opencode session`) over the scraped buffer.

## Calibrating the table

The table self-corrects from real work: the workflow's last step proposes score changes when a model repeatedly fails or aces a task type.
To deliberately benchmark a new model, run a bake-off:

> Delegate this same task to glm, gpt, and \<new model\> in parallel.
> Compare the outputs on correctness, completeness, and how much fixing each needed.
> Report a comparison table and suggest routing-table score changes.

Run it on two or three tasks representative of your actual work - that beats synthetic benchmarks for deciding your routing.
