# Codex CLI troubleshooting (model ids, stale installs)

On codex CLI >= 0.144.x the top model is exposed as `gpt-5.6-sol` (frontier), `gpt-5.6-terra` (balanced), or `gpt-5.6-luna` (fast/cheap).
Bare `gpt-5.6` is not a valid id and 400s with `invalid_request_error`.

Check `codex --version` before assuming a model name works; older installs won't have 5.6 at all.
`-m <model>` skips the interactive `/model` picker that would otherwise show you the current valid ids.

If `codex --version` looks stale, `mise use -g codex@latest` updates it.
But mise's shims can bake a specific version's path into an already-open shell's `$PATH`, so a running session may need the full binary path (`~/.local/share/mise/installs/codex/<version>/codex`) or a fresh shell before it picks up the update.
