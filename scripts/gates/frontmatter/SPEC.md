# Frontmatter gate: specification v0.4.0

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
| `related` | No | A list of 1 to 5 page slugs (see [Slugs](#slugs)). Pages whose subjects affect each other: they overlap, one is an alternative to the other, or one changes how the other behaves. |

**Absent, null, and empty mean the same thing.** A key that's missing, a key with no value (`related:`, which YAML reads as null), an empty string (`''`), and an empty list (`[]`) are all "not set". So `related: null` and `related: ''` mean no related pages, and `page_type: null` or `page_type: ''` is reported as `missing-page-type`. This applies to `page_type` and `related` only, not to `docops` itself.

No other keys are allowed under `docops:`. Keys outside `docops:` (ReadMe's `title`, `excerpt`, `hidden`, `metadata`, `next`, and so on) are never checked.

## Pages and slugs

A **page** is a file matching `docs/**/*.md` under the repository root. Nothing outside `docs/` is checked or resolved; `reference/` (API reference, linked as `ref:`) is a separate namespace and its pages can't appear in `related`.

A page's **slug** is its filename without `.md`, except that `index.md` takes the name of the folder it's in. These are the slugs ReadMe uses in `(doc:<slug>)` links.

| Path | Slug |
| --- | --- |
| `docs/Senseml reference/preprocessors/remove-lines.md` | `remove-lines` |
| `docs/Senseml reference/preprocessors/index.md` | `preprocessors` |

Slugs compare exactly (case-sensitive). A `related` entry is a bare slug: no `doc:` prefix, no `#anchor`, no `/`, no whitespace.

**Frontmatter** is the text between a first line `---` and the next `---` line, parsed as YAML (safe-load). Frontmatter that isn't valid YAML or isn't a mapping is `bad-yaml`. A subject that isn't a string is reported as YAML wrote it (`2024`).

## Rules

Each problem has a **rule ID**, a **severity** (`error` or `warning`), the **path** of the page it's reported on, and, for some rules, a **subject** (the offending key, value, or slug).

| Rule | Severity | Subject | When |
| --- | --- | --- | --- |
| `unreadable` | error | — | The file can't be read or isn't valid UTF-8 |
| `no-frontmatter` | error | — | The file doesn't start with a `---` line, or has no closing `---` line |
| `bad-yaml` | error | — | The frontmatter isn't valid YAML, or isn't a mapping |
| `missing-docops` | **warning** (error with `--require`) | — | No `docops` key |
| `docops-not-mapping` | error | — | `docops` is present but isn't a mapping (a null `docops:` counts as not a mapping) |
| `unknown-key` | error | the key | A key under `docops:` other than `page_type` or `related` |
| `missing-page-type` | error | — | `page_type` is not set (absent, null, or empty) |
| `bad-page-type` | error | the value | `page_type` isn't one of the four types |
| `related-not-list` | error | — | `related` is set but isn't a list |
| `related-not-string` | error | the value | An entry isn't a string (quote it) |
| `related-too-many` | error | — | `related` has more than 5 entries |
| `related-not-slug` | error | the entry | A string entry is empty, or contains `:`, `#`, `/`, or whitespace |
| `related-duplicate` | error | the slug | The same slug appears more than once |
| `related-self` | error | the slug | An entry is the page's own slug |
| `duplicate-slug` | error | the slug | Two or more pages have the same slug; reported on every one of them |
| `related-unresolved` | error | the slug | No page has that slug, or more than one does |
| `related-asymmetric` | error | the slug | Page A lists B, but B doesn't list A |

Each problem is reported once: problems with the same path, rule, and subject are one problem.

**What a broken page still gets checked for:**
- `unreadable`, `no-frontmatter`, `bad-yaml`, `missing-docops`, or `docops-not-mapping`: nothing else, and other pages treat it as having no `related` list.
- `unknown-key`, `missing-page-type`, or `bad-page-type`: `related` is still checked in full.
- `related-not-list`: the page's `related` is ignored for every later check.
- An entry that fails `related-not-string` or `related-not-slug` is checked for nothing else.

## Command line

```
frontmatter_gate.py [--root DIR] [--require] [--json]
```

- `--root`: the repository root; default `.`. If `DIR/docs` isn't a folder, write a one-line error to stderr and exit 2.
- `--require`: `missing-docops` becomes an error. Use once every page has a `docops:` block.
- `--json`: print the problems as a JSON array of objects with keys `path`, `rule`, `severity`, `subject` (`null` for rules without one), instead of text.

**Exit code:** 0 if there are no errors (warnings allowed), 1 if there's at least one error, 2 if the check couldn't run.

**Text output:** one line per problem, sorted by path, then rule, then subject, then a summary line, always. Paths use `/` and are relative to the root. `<N>` counts every page.

```
<path>: <severity>: <rule>[: <subject>]
frontmatter gate: <E> error(s), <W> warning(s), <N> page(s)
```

**Anything this spec doesn't cover is implementation-defined.** That includes inputs that can't occur in the docs repo today: line endings, byte-order marks, spaces around `---`, repeated YAML keys, `Index.md` or `.MD`, symlinks, which characters count as whitespace, unquoted YAML numbers and booleans as slugs, how symmetry works for slugs that more than one page has, and the exact byte layout of the JSON output. `tests.yaml` pins the behavior that matters; to pin more, add a case there first.

## Testing

`tests.yaml` has a `cases` list. Each case has a `name`, optional `args` (default `[]`), `exit`, and either `expect` or `stdout`. Its files come from `pages`, `files`, or both. Build them in a fresh, empty temporary directory, which is the repository root.

**`pages`** maps a key to a `docops:` value, written to `docs/s/<key>.md` (or to `paths[<key>]`, when the case has `paths`) as:

```
---
title: T
docops: <value as one-line JSON>
---

Body.
```

A mapping without `page_type` gets `page_type: reference` first, so `{related: [b]}` becomes `docops: {"page_type": "reference", "related": ["b"]}`. A null value leaves out the `docops:` line. The key is the page's slug unless `paths` puts it somewhere else, such as an `index.md`.

**`files`** maps a repo-relative path to a string (written as UTF-8) or `{base64: ...}` (written as the decoded bytes), for cases about the file itself.

**`expect`** lists every problem as `<page> <rule>` or `<page> <rule> <subject>`, separated by single spaces; the subject is the rest of the line. `<page>` is a key from `pages` or a path from `files` (which therefore can't contain spaces). Severity is `warning` for `missing-docops` without `--require` in `args`, and `error` otherwise.

**Checking a case:**
- `exit` is 2: run with `args` and compare only the exit code.
- `stdout` given: run with exactly `args`; compare stdout and the exit code exactly.
- Otherwise: run with `args` plus `--json`, sort the problems and `expect` by path, rule, and subject, and compare them as lists (so a problem reported twice fails). Then compare the exit code.

## Out of scope (v0.4)

- Pages under `reference/`, and links between `docs/` and `reference/`.
- Checking that `page_type` matches the page's content. That's a judgment, not a gate.
- Checking ReadMe keeps `docops:` after a sync. That's a separate weekly check.
