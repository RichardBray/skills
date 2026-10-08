---
name: new-project
description: Start a new project on the user's stack and put agent-harness on it. Use when the user asks to create, start, scaffold or bootstrap a new site, app, tool or project.
---

# New project

| Building | Use | Scaffold |
|---|---|---|
| Static site | Astro | `bun create astro@latest <name>` |
| Client-side app with dynamic data | React + Vite | `bun create vite@latest <name> --template react-ts` |
| Desktop app | Electrobun, React UI | `bunx electrobun init <name>` |
| Heavy computation | Rust, as a sidecar binary the app spawns or a cdylib loaded with `bun:ffi` | `cargo new --lib <name>` inside the project |

- Bun for everything. Latest versions, pinned exactly (`bun add --exact`).
- Deploy sites to Cloudflare (`wrangler`) or Vercel.

Then:
1. `~/agent-harness/bin/harness init` in the project root, and run the `run:` commands it prints.
2. If it warns that `.claude/settings.json` is gitignored, fix `.gitignore` as it says.
3. Run `.harness/hooks/check-all.sh`; it must pass before the first commit.
4. Commit.
