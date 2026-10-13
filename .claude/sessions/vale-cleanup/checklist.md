# Vale cleanup

Claude Code session name: vale-cleanup
Claude Code session ID: 00a5f2b7-bd72-40b2-9b61-8c1475b5d3ff

Goal: replace seven overlapping Vale integrations with two (CI + one PostToolUse hook),
keep the optional vale pane, and add a check that tests the setup the way Claude Code runs it.

## In this branch
- [x] Rewrite `.claude/hooks/vale-check.sh` (jq, finds ~/.local/bin/vale, warnings+ only, lints with the file's own checkout config)
- [x] Wire it as a PostToolUse hook in `.claude/settings.json`
- [x] Delete `.github/workflows/reviewdog.yml` (manual-only duplicate of lint_style.yml)
- [x] Add `scripts/vale-doctor.sh`; all checks pass
- [x] Scope Vale to `docs/` and `reference/` only: hook skips other paths; CI trigger fixed (was the nonexistent `readme-sync/v0/`) and lints only those folders; doctor checks a file outside them is ignored

## Done outside the repo
- [x] Remove `vale` and `vale-mcp` MCP servers (`claude mcp remove`)
- [x] Remove `disableAllHooks` from main checkout's `.claude/settings.local.json`
- [x] Put `~/GitHub/claude-vale-pane` under git; align it (md/mdx only, same Vale lookup as the hook)

## Folded in from the old `vale` worktree
- [x] Moved its unstarted plan for a method-name Vale rule to `.claude/sessions/vale-method-names/` (`plan.md`, `style-guide-draft.md`). Most of the draft is already in `style-guide-overview.md`; the rule itself is still to do.

## Needs Frances (blocked for Claude by auto mode)
- [ ] Delete PreToolUse + UserPromptSubmit Vale hooks from `~/.claude/settings.json`, then `rm ~/.claude/hooks/vale-changed.sh`
- [ ] `rm -rf ~/.local/vale-mcp ~/GitHub/vale-server`; `rmdir ~/.local/share/vale/styles ~/.local/share/vale ~/.config/vale`
- [ ] `claude update`, then try `/vale` and run the pane tests
- [ ] Rerun `scripts/vale-doctor.sh`; no leftover notes expected
