# Frontmatter gate: specification v0.1.0

## Overview

Docs pages in `docs/` carry a `docops:` block in their YAML frontmatter. ReadMe strips frontmatter from the published Markdown, so readers never see it; agents and scripts read it from GitHub. The gate checks that every `docops:` block is well formed and that pages' `related` lists agree with each other.

`tests.yaml` is the acceptance test. Any implementation must pass every case in it. If this spec and `tests.yaml` disagree, that's a bug in one of them: report it, don't pick one.

## The `docops:` block

```yaml
---
title: Remove lines
excerpt: ...
docops:
  page_type: reference
  related: [rotate-page, remove-text]
---
```

| Key | Required | Value |
| --- | --- | --- |
| `page_type` | Yes, when `docops:` is present | One of `tutorial`, `how-to`, `reference`, `explanation` ([Diátaxis](https://diataxis.fr/)) |
| `related` | No | A list of 1 to 5 page slugs (see [Slugs](#slugs)). Pages whose subjects affect each other: they overlap, one is an alternative to the other, or one changes how the other behaves. An empty list is the same as leaving the key out. |

No other keys are allowed under `docops:`. Keys outside `docops:` (ReadMe's `title`, `excerpt`, `hidden`, `metadata`, `next`, and so on) are not the gate's business and are never checked.

## Pages

A **page** is any file matching `docs/**/*.md` under the repository root. Nothing outside `docs/` is checked or resolved; in particular, `reference/` (API reference, linked as `ref:`) is a separate namespace and its pages can't appear in `related`.

A page's **frontmatter** is the text between a first line that is exactly `---` and the next line that is exactly `---`. It must parse as a YAML mapping.

### Slugs

A page's slug is its filename without `.md`, except that `index.md` takes the name of the folder it's in. These are the slugs ReadMe uses in `(doc:<slug>)` links.

| Path | Slug |
| --- | --- |
| `docs/Senseml reference/preprocessors/remove-lines.md` | `remove-lines` |
| `docs/Senseml reference/preprocessors/index.md` | `preprocessors` |

Slugs compare exactly (case-sensitive). A `related` entry is a bare slug: no `doc:` prefix, no `#anchor`, no `/`, no whitespace.

## Rules

Each problem has a **rule ID**, a **severity** (`error` or `warning`), the **path** of the page it's reported on, and, for some rules, a **subject** (the offending key, value, or slug, as a string).

| Rule | Severity | Reported on | Subject | When |
| --- | --- | --- | --- | --- |
| `no-frontmatter` | error | the page | — | The file doesn't start with a `---` line, or has no closing `---` line |
| `bad-yaml` | error | the page | — | The frontmatter isn't valid YAML, or isn't a mapping |
| `missing-docops` | **warning** (error with `--require`) | the page | — | No `docops` key |
| `docops-not-mapping` | error | the page | — | `docops` is present but isn't a mapping |
| `unknown-key` | error | the page | the key | A key under `docops:` other than `page_type` or `related` |
| `missing-page-type` | error | the page | — | `docops:` has no `page_type` |
| `bad-page-type` | error | the page | the value, as a string | `page_type` isn't one of the four types |
| `related-not-list` | error | the page | — | `related` isn't a list, or an entry isn't a string |
| `related-too-many` | error | the page | — | `related` has more than 5 entries |
| `related-not-slug` | error | the page | the entry | An entry contains `:`, `#`, `/`, or whitespace, or is empty |
| `related-duplicate` | error | the page | the slug | The same slug appears more than once (reported once per repeated slug) |
| `related-self` | error | the page | the slug | An entry is the page's own slug |
| `duplicate-slug` | error | **every** page sharing the slug | the slug | Two or more pages have the same slug |
| `related-unresolved` | error | the page | the slug | No page has that slug |
| `related-asymmetric` | error | the page that lists the slug | the slug | Page A lists B, but B's `related` doesn't list A (including when B has no `docops:` block or no `related`) |

**Order of checks for one page.** A page with `no-frontmatter` or `bad-yaml` gets no other problems, and is treated as having no `related` list when other pages are checked against it. When `related-not-list` applies, the page's `related` is ignored for every later check. An entry that fails `related-not-slug` is reported only for that rule. Only valid, distinct, non-self entries are checked for `related-unresolved` and `related-asymmetric`, and for those two checks a duplicated slug (`duplicate-slug`) counts as unresolved: it's reported as `related-unresolved`, never asymmetric.

`related-too-many` doesn't stop the other checks: each entry is still checked.

## Command line

```
frontmatter_gate.py [--root DIR] [--require] [--json]
```

- `--root`: the repository root; default `.`. If `DIR/docs` doesn't exist, print an error and exit 2.
- `--require`: `missing-docops` becomes an error. Use once every page has a `docops:` block.
- `--json`: print the problems as one JSON array instead of text (see below).

**Exit code:** 0 if there are no errors (warnings allowed), 1 if there's at least one error, 2 if the check couldn't run.

**Text output:** one line per problem, then a summary line. Paths use `/` and are relative to the root.

```
<path>: <severity>: <rule>[: <subject>]
frontmatter gate: <E> error(s), <W> warning(s), <N> page(s)
```

**JSON output:** an array of objects `{"path": ..., "rule": ..., "severity": ..., "subject": ...}`, where `subject` is `null` for rules without one. No summary line.

**Order:** problems are sorted by path, then rule ID, then subject (a missing subject sorts first). Output is deterministic: the same tree always gives the same bytes.

## Testing

`tests.yaml` has one entry per case:

```yaml
- name: short description
  args: [--require]            # optional; default []
  files:                       # repo-relative path → file content; build these in an empty temp dir
    docs/a/remove-lines.md: |
      ---
      docops:
        page_type: reference
      ---
  exit: 0
  problems: []                 # compared as an unordered set of {path, rule, severity, subject?}
  stdout: |                    # optional; when present, compare the text output exactly
    ...
```

A missing `subject` in an expected problem means `null`. When `exit` is 2, only the exit code is compared. Run each case against a fresh temporary directory containing exactly its `files`, with `--json` unless the case has `stdout`, in which case run without `--json` and compare stdout exactly.

## Out of scope (v0.1)

- Pages under `reference/`, and links between `docs/` and `reference/`.
- Checking that `page_type` matches the page's content. That's a judgment, not a gate.
- Checking ReadMe keeps `docops:` after a sync. That's a separate weekly check.
