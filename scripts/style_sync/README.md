# Style guide / Vale drift check

**To review the rule mapping, read [REVIEW.md](REVIEW.md)**, a generated table of every style-guide rule and how it's enforced. Edit `registry.yaml`, then run `python scripts/style_sync/review_table.py`.

A weekly check that the style guide (`.claude/style-guide/`) and the Vale rules (`.github/styles/`) still agree. It runs from `.github/workflows/style_drift.yml` every Monday and on demand (**Actions > Style drift check > Run workflow**).

It is not a PR check and never blocks docs work. When it finds drift, it opens one issue labeled `style-drift`, or updates the open one. When a later run is clean, it closes the issue.

| File | Purpose |
| ---- | ------- |
| `registry.yaml` | Links each style-guide rule to its enforcement, and each custom Vale rule to its guide rule. The header explains how guide rules are identified. |
| `check_drift.py` | The check. Exit code 0 = clean, 1 = drift, 2 = the check could not run. |
| `fixtures/<Rule>/` | Test inputs for `.github/styles/Sensible/<Rule>.yml`. |
| `agent_lines.py` | Lints only the lines an agent added, with the agent-only rules. See [Agent-only rules](#agent-only-rules). |
| `test/tests/` | Tests for `check_drift.py` and `agent_lines.py`. They run in `test-scripts.yml`. |

## Run it locally

```bash
vale sync            # once, to fetch the Google package
python3 scripts/style_sync/check_drift.py
```

You need Python 3, PyYAML, and Vale 3.14.1 on your `PATH` (or pass `--vale /path/to/vale`). The check writes a temporary Vale config, so your own Vale settings don't affect it.

## What it checks

Each problem prints as one line that starts with a code:

| Code | Meaning | Usual fix |
| ---- | ------- | --------- |
| `ORPHAN-VALE-RULE` | A rule in `.github/styles/Sensible/` has no registry entry. | Add an entry that points at the guide rule it enforces, or a `basis:` if there is none. |
| `MISSING-VALE-RULE` | A registry `vale:` target doesn't exist. | Fix the name, or update the entry if the rule was removed. |
| `DISABLED-VALE-RULE` | A registry `vale:` target is turned off for `*.md` in `.vale.ini`. | Re-enable the rule, or change the entry's enforcement. |
| `AGENT-ONLY-ENABLED` | A rule under `agent_only_rules:` is turned on for `*.md` in `.vale.ini`, so it flags human-written lines too. | Set it to `NO` in `.vale.ini`, or take it off the list. |
| `DANGLING` | A registry location no longer resolves: the file, heading anchor, bold-lead item, or table row is gone. | Update `at`/`item`/`row` after a rename. Keep the `id`. |
| `UNMAPPED-GUIDE-RULE` | The guide has a heading, bold-lead item, or glossary row with no registry entry. | Add a `rules:` entry, or a `not_rules:` entry if it isn't a rule. |
| `NO-TESTS` | A custom Vale rule has no failing or no passing test case. | Add a fixture, or an Avoid/Prefer example in the guide. |
| `TEST-FAIL` | An Avoid example or `fail` fixture doesn't trigger its rule, or a Prefer example or `pass` fixture does. | Decide whether the guide or the rule is right, and change that one. If the gap is acceptable, list the example under the entry's `known_gaps:`. |
| `ORPHAN-FIXTURE` | A `fixtures/<Rule>/` folder has no matching rule. | Rename or delete the folder. |
| `STALE-KNOWN-GAP` | A `known_gaps:` entry is no longer an Avoid example in the guide. | Delete it. |
| `UNPINNED-PACKAGE` | `.vale.ini` installs a package without a pinned version, so `vale sync` can change rules without a commit. | Pin it to a release URL. |
| `GOOGLE-OVERRIDES` | The `Google.*` overrides in `.vale.ini` don't match the registry's `google.overrides`. | Update whichever is out of date. |
| `SCHEMA` / `MISSING-GUIDE-FILE` | The registry is malformed. | Fix the registry. |

The Google package is treated as one inherited group, not mapped rule by rule. A guide entry can still point at a single Google rule (for example `vale: Google.EmDash`) when that rule enforces it.

## Add a style-guide rule

1. Write the rule in one of the files listed under `scan:` in `registry.yaml`, as an H2/H3 heading or a bold-lead paragraph (`**Rule name:** ...`).
2. Add an entry under `rules:` with a new `id`, the location, and exactly one enforcement:
   - `vale: Sensible.<Rule>` (or a `Google.<Rule>`, or `vocab:Sensible/reject`) when Vale enforces it,
   - `human: <why Vale can't check it>`,
   - `none-yet: <note>` when it could be automated but isn't.
3. If you give examples, write them as `- Avoid: "..."` and `- Prefer: "..."`. For a `vale:` entry, the check runs them through Vale automatically.

## Add a Vale rule

1. Add `.github/styles/Sensible/<Rule>.yml`.
2. Point the matching guide entry at it with `vale: Sensible.<Rule>`. If no guide rule exists, add an entry with `vale:` and a `basis:` explaining why the rule exists.
3. Add tests (next section). The check reports `NO-TESTS` until the rule has at least one failing and one passing case.

## Add a test

Two sources of test cases, and every custom rule needs at least one fail case and one pass case from either:

- **Guide examples (preferred).** Avoid/Prefer lines in the guide section an entry points at, and the Avoid/Use columns of glossary rows. These test the guide and the rule against each other: if one changes without the other, the check reports `TEST-FAIL`. The registry header describes the extraction rules.
- **Fixtures.** For rules whose guide section has no examples, add `fixtures/<Rule>/fail.md` (must trigger `Sensible.<Rule>`) and `fixtures/<Rule>/pass.md` (must not). More files are fine: any `fail*.md` or `pass*.md` in the folder counts. Only alerts from the rule under test count, so other rules firing on a fixture don't matter.

## Draft mappings

Entries marked `status: draft` were proposed by an agent and haven't been reviewed. Check the mapping, then delete the `status` line. `status: mechanical` means the Vale rule's own message restates the guide text. Agent-written fixtures start with a `status: draft` HTML comment; delete it after review.

## Agent-only rules

Some rules apply only to text an agent writes. Today that's `Sensible.EmDash`: agents overuse em dashes, but a person's em dash is their call (Frances, 2026-10-28). Vale can't tell who wrote a line, so:

- `.vale.ini` turns these rules off (`Sensible.EmDash = NO`), so CI lint (`lint_style.yml`) and your own Vale runs never flag them.
- `agent_lines.py` runs them on the lines added or changed since a base commit, which in an agent session are the agent's lines.
- They're listed once, under `agent_only_rules:` in `registry.yaml`. Their registry entries still need tests, and `check_drift.py` runs those with the rule turned on explicitly. It expects an agent-only rule to be off in `.vale.ini`, and reports `AGENT-ONLY-ENABLED` if it's on.

To make a rule agent-only, add it to `agent_only_rules:` and set it to `NO` in `.vale.ini`.

### Who calls it

- **The edit hook.** `.claude/hooks/vale-check.sh` runs after Claude writes or edits a doc. It runs `agent_lines.py --base HEAD <file>` and hands its alerts to Claude with Vale's. Uncommitted changes count as the agent's.
- **The docs workflow (planned).** At its writing stage it will run `agent_lines.py --base <branch point>`, where the branch point is `git merge-base origin/v0 HEAD`, so every line written on the branch is checked, committed or not. The run should fail on exit 1 or 2.

### Spec

```
agent_lines.py --base REF [--root DIR] [--vale PATH] [FILE ...]
```

- `--base REF` (required): any git revision. A line is **added** when it's in the working-tree copy of a file and `git diff REF` reports it as added or changed. That includes staged and unstaged changes. A line that keeps its em dash but changes in any other way counts. A file that doesn't exist at `REF` (untracked, or new since `REF`) is all added lines.
- `--root DIR`: the repository root; default: the git top level of the current directory. `.vale.ini`'s settings aren't used; only `DIR/.github/styles` and `DIR/scripts/style_sync/registry.yaml` are.
- `--vale PATH`: the Vale binary; default `vale` on `PATH`, then `~/.local/bin/vale`.
- `FILE`: paths, absolute or relative to the current directory. Without any, the files are every `.md` or `.mdx` file under `docs/` or `reference/` that's changed since `REF` or untracked (and not ignored). Files that don't exist, aren't `.md` or `.mdx`, or are outside the root are skipped.

**How it lints:** Vale runs once on all the files, with a temporary config that turns on only the rules in `agent_only_rules:` (the Sensible styles path, `--no-global`, JSON output). Code blocks, frontmatter, and other markup are scoped the way Vale scopes them by default. An alert counts only when its line is an added line.

**Output:** one line per alert, sorted by path and line, in Vale's `--output=line` format: `<path>:<line>:<column>:<rule>:<message>`. The path is as given, or relative to the root for files it found itself.

**Exit code:** 0 no alerts, 1 alerts, 2 it couldn't run (not a git repo, an unknown `REF`, no Vale, an unreadable registry, or Vale failed). On 2, a one-line error goes to stderr.

The tests in `test/tests/test_agent_lines.py` are the acceptance tests for this spec.
