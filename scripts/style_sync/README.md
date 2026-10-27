# Style guide / Vale drift check

A weekly check that the style guide (`.claude/style-guide/`) and the Vale rules (`.github/styles/`) still agree. It runs from `.github/workflows/style_drift.yml` every Monday and on demand (**Actions > Style drift check > Run workflow**).

It is not a PR check and never blocks docs work. When it finds drift, it opens one issue labeled `style-drift`, or updates the open one. When a later run is clean, it closes the issue.

| File | Purpose |
| ---- | ------- |
| `registry.yaml` | Links each style-guide rule to its enforcement, and each custom Vale rule to its guide rule. The header explains how guide rules are identified. |
| `check_drift.py` | The check. Exit code 0 = clean, 1 = drift, 2 = the check could not run. |
| `fixtures/<Rule>/` | Test inputs for `.github/styles/Sensible/<Rule>.yml`. |
| `test/tests/` | Tests for `check_drift.py`. They run in `test-scripts.yml`. |

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
