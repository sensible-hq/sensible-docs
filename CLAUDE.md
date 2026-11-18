# sensible-docs

Project rules for Claude Code. Keep rules here or in the style guides, skills, and `style-rules/registry.yaml`, not in Claude Code's auto memory: a rule in memory is invisible to reviewers, to CI, and to the registry's duplicate and contradiction checks. Don't write to auto memory for this project. When a correction should outlive the session, add it to the file that owns the topic and say which one.

## Docs changes

- Before committing a docs change, do a full style pass: read every file in `.claude/style-guide/` and `.claude/preferences/editorial-preferences.md`, then apply `.claude/skills/revise-doc-style/SKILL.md` to the changed pages. When guides conflict, follow what sibling pages do and say which you chose. <!-- rule: sensible-full-style-pass -->
- Never hand-edit `reference/**/*.md`. It's generated from the OpenAPI specs, so change `reference/*.json` instead. Pages under `docs/` are hand-edited.
- Doc image paths always point to `assets/images/final/`, even before the file exists there. When you add or update a screenshot in `assets/images/screenshots/`, copy it unchanged to `final/` under the same name and commit both. The styling run on merge to `v0` overwrites the `final/` copy.
- Name brief files `.claude/briefs/brief-<slug>.md`, where the slug is the doc's file name without its extension.

## Tests and tooling

- Use `SENSIBLE_TEST_API_KEY` for every Sensible API call, test, and probe. It's the test account's key, and tests create and delete resources. Never fall back to `SENSIBLE_API_KEY`, and never print either key. If the test key is missing, stop and ask.
- Doc-test fixtures live in `scripts/doc-detective/fixtures/<group>/`, one self-contained folder each. Reference a docs PDF in place with `docs_pdf` rather than copying it. `scripts/test/` holds only the older smoke tests and the API contract tests.
- Vale enforcement is deliberately small: the `lint_style.yml` CI check and one hook script, `.claude/hooks/vale_gate.py`, on `PreToolUse` and `PostToolUse`. Don't add other integrations. `scripts/vale-doctor.sh` checks the hook the way Claude Code runs it.
- Avoid AGPL-licensed tools and dependencies; check a new tool's license before adding it and flag GPL, AGPL, or SSPL. Doc Detective is the one exception, and only as an unmodified CLI installed from npm at a pinned version, with `autoUpdate: false` and `telemetry.send: false`. Its agent-tools plugin and hosted MCP server are also AGPL.
- Extract a named schema from a JSON file with `jq '.components.schemas.Name' file.json`, not `grep -A`, which bleeds into the next schema.

## Branches and sessions

- Create a branch as a sibling worktree: `git pull && git worktree add ../sensible-docs-<slug> -b <slug>`, and add the worktree path to `permissions.additionalDirectories` in `.claude/settings.json`.
- When the PR is squashed and merged, remove the worktree and branch, pull `v0`, and remove the path from `additionalDirectories`. The `close-docs-pr` skill does this.
- Keep session checklists in `.claude/sessions/<session-name>/checklist.md`, never only in Claude Code's task list, and commit them on the branch. Put the Claude Code session name and ID at the top of the checklist; the ID is the `.jsonl` file name under `~/.claude/projects/<path-slug>/`.
- Write `.claude-session` to the worktree root as `<session-name> <checklist-path> <session-uuid> <session-directory>`, and commit it.
