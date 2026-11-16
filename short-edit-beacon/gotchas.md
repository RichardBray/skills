# Gotchas

Beacon tools
- `transaction` runs commands only: `media_import` is refused inside it.
- `media_import` refuses any overlap on the track, even 0.03 s. Import past
  the end of the track, `clip_trim`, then `clip_move`.
- Splitting a clip copies its effects with the same effect ids: remove them
  per clip (`effect_remove` with `clip` and `effect`).
- `clip_split` with `clips` splits those clips and their linked clips only.
- `asset_clips` can return a schema error: use `timeline_clips` instead.
- `transcript_removeSilences` with `quiet` is very tight (0.04 s each side):
  leave it for deliberate cuts, and remove leftover long gaps with
  `timeline_rippleDelete` ranges instead.
- `frames_sheet` can show a one-frame glitch at an exact cut: check with
  `frame_at` just after before treating it as a bug.
- `auphonic_apply` and `broll_generate` spend money or minutes: only when the
  user asked.

Rendering screens
- `render-html.ts` uses one fixed debugging port: render pages one after
  another, never in parallel.
- A render started with `&` inside a background command can be killed when
  the command ends: run renders in the foreground (they take 20-90 s).
- Beacon's ffmpeg has no `tile` filter and no JPEG encoder: save crops as PNG
  and look at frames one by one or with `frames_sheet`.
- `file://` fonts and images work in the pages (`--allow-file-access-from-files`).

Shell
- In zsh, `echo =====` fails ("= not found"): use another separator.
- A two-command `sed -i "s/.../.../; s/.../.../"` failed on macOS: edit files
  with `python3 -I` or the Edit tool.
