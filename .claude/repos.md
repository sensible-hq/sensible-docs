# Repos and paths

The skills don't name repos or local paths directly. They use these environment variables, which `.claude/settings.json` sets for every Bash command in a Claude Code session started in this repo:

| variable | now | upstream value | what it is |
| -------- | --- | -------------- | ---------- |
| `DOCS_REPO` | `fscelliott/sensible-docs-private-test` | `sensible-hq/sensible-docs` | where docs branches, PRs, and issues go |
| `DOCS_DIR` | `/home/franc/GitHub/sensible-docs-private-test` | `/home/franc/GitHub/sensible-docs` | the local clone of `DOCS_REPO`; worktrees go beside it as `$DOCS_DIR-<slug>` |
| `ENGINE_REPO` | `sensible-hq/sensible` | same | engine PRs the skills read |
| `APP_REPO` | `sensible-hq/sensible-app` | same | app PRs the skills read |
| `SOURCE_LABELS` | `off` | `on` | whether `close-docs-pr` swaps `doc_changes_needed` for `docs_done` on engine and app PRs |

The current values point at a private test copy, so the doc skills can be tried on real engine PRs without touching `sensible-hq/sensible-docs`. To point back upstream, set the upstream values and remove the sandbox guard entry from `PreToolUse` in `.claude/settings.json`.

## Sandbox guard

`.claude/hooks/sandbox_guard.py` runs before every Bash command. While `DOCS_REPO` is outside the `sensible-hq` org, it denies commands that would change a `sensible-hq` repo: API writes, gh commands that create, edit, comment on, merge, or label PRs and issues, and pushes to a `sensible-hq` URL. Reads such as `gh pr view --repo "$ENGINE_REPO"` pass. When `DOCS_REPO` is a `sensible-hq` repo, the guard does nothing.

## In prose and links

The shell expands the variables in commands. When a skill writes a repo into text, such as a PR body or a link, run `echo "$DOCS_REPO"` and use the value. References to engine PRs keep the full form `sensible-hq/sensible#<number>`, because the engine repo doesn't change.

## Not covered

The `changelog` skill publishes drafts to readme.com, which these variables don't redirect. Don't run its publish step from a test copy.
