# Frontmatter gate: specification v0.3.0

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

## Pages

A **page** is a regular file whose path matches `docs/**/*.md` under the repository root, with `.md` lowercase. Hidden files and folders count. Symbolic links are not followed. Nothing outside `docs/` is checked or resolved; in particular, `reference/` (API reference, linked as `ref:`) is a separate namespace and its pages can't appear in `related`.

### Slugs

A page's slug is its filename without `.md`, except that a file named exactly `index.md` takes the name of the folder it's in (`docs/index.md` has slug `docs`). These are the slugs ReadMe uses in `(doc:<slug>)` links.

| Path | Slug |
| --- | --- |
| `docs/Senseml reference/preprocessors/remove-lines.md` | `remove-lines` |
| `docs/Senseml reference/preprocessors/index.md` | `preprocessors` |

Slugs compare exactly (case-sensitive). A `related` entry is a bare slug: no `doc:` prefix, no `#anchor`, no `/`, no whitespace.

## Parsing conventions

- **Encoding:** files are UTF-8. A leading byte-order mark is ignored. A file that isn't valid UTF-8, or can't be read, gets `unreadable` and nothing else.
- **Lines:** `\n`, `\r\n`, and `\r` all end a line.
- **Frontmatter** is the text between a first line that is exactly `---` and the next line that is exactly `---`. "Exactly" means nothing else on the line, not even trailing spaces.
- **YAML** is parsed as YAML 1.1 safe-load, so unquoted `yes`, `no`, `on`, `off`, `true`, `false`, `null`, numbers, and dates are not strings. A slug like that must be quoted (`related: ["2024"]`). Frontmatter that parses to anything but a mapping, including empty frontmatter, is `bad-yaml`. When a key repeats, the last value wins.
- **Subjects** are always strings. A non-string value is rendered as: `null`, `true` / `false`, decimal numbers as YAML wrote them (`3`, `2.5`), dates as `YYYY-MM-DD`, and anything else as compact JSON with sorted keys.

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
| `related-not-list` | error | — | `related` is set (not absent, null, or empty) but isn't a list |
| `related-not-string` | error | the value | An entry isn't a string (quote it) |
| `related-too-many` | error | — | `related` has more than 5 entries, counting every entry as written |
| `related-not-slug` | error | the entry | A string entry is empty, or contains `:`, `#`, `/`, or any Unicode whitespace |
| `related-duplicate` | error | the slug | The same valid slug appears more than once |
| `related-self` | error | the slug | An entry is the page's own slug |
| `duplicate-slug` | error | the slug | Two or more pages have the same slug; reported on **every** one of them |
| `related-unresolved` | error | the slug | No page has that slug, or more than one does |
| `related-asymmetric` | error | the slug | Page A lists B, but B doesn't list A (see [Symmetry](#symmetry)) |

**Each problem is reported once.** Problems with the same path, rule, and subject are one problem, however many times the cause appears.

**What a broken page still gets checked for:**
- `unreadable`, `no-frontmatter`, or `bad-yaml`: nothing else, and other pages treat it as having no `related` list.
- `missing-docops` or `docops-not-mapping`: nothing else.
- `unknown-key`, `missing-page-type`, or `bad-page-type`: `related` is still checked in full.
- `related-not-list`: the page's `related` is ignored for every later check, including symmetry.
- An entry that fails `related-not-string` or `related-not-slug` is checked for nothing else. `related-too-many` stops nothing: every entry is still checked.

### Symmetry

Symmetry is checked only between pages whose slugs are unique. For each page A, each entry B that's a valid, distinct, non-self slug resolving to exactly one page:

- B **lists A** if B's `related` (when checked at all, per the list above) has an entry equal to A's slug.
- If it doesn't, A gets `related-asymmetric` with subject B.

An entry naming a slug that more than one page has is `related-unresolved` and is never checked for symmetry. And if A's own slug is shared, nobody's entry can resolve to A, so the pages that list it get `related-unresolved` instead.

## Command line

```
frontmatter_gate.py [--root DIR] [--require] [--json]
```

- `--root`: the repository root; default `.`. If `DIR/docs` doesn't exist or isn't a folder, write a one-line error to stderr, write nothing to stdout, and exit 2.
- `--require`: `missing-docops` becomes an error. Use once every page has a `docops:` block.
- `--json`: print the problems as one JSON array instead of text.

**Exit code:** 0 if there are no errors (warnings allowed), 1 if there's at least one error, 2 if the check couldn't run.

**Text output:** one line per problem, then a summary line, always. `<N>` counts every page, broken ones included. Paths use `/` and are relative to the root.

```
<path>: <severity>: <rule>[: <subject>]
frontmatter gate: <E> error(s), <W> warning(s), <N> page(s)
```

**JSON output:** an array of objects with keys in the order `path`, `rule`, `severity`, `subject` (`null` for rules without one), indented 2 spaces, non-ASCII characters written as-is, ending with a newline. No summary line.

**Order:** problems sorted by path, then rule ID, then subject (no subject sorts first), comparing strings by Unicode code point. The same tree always gives the same bytes.

**Anything this spec doesn't cover is implementation-defined.** That includes inputs that can't occur in the docs repo today, such as symlinked folders, control characters, and numbers in non-decimal notation. `tests.yaml` pins the behavior that matters; to pin more, add a case here first.

## Testing

`tests.yaml` has one entry per case:

```yaml
- name: short description
  args: [--require]            # optional; default []
  files:                       # repo-relative path → content; build these in an empty temp dir
    docs/a/remove-lines.md: |  # a string is written as UTF-8
      ---
      docops:
        page_type: reference
      ---
    docs/a/bad.md:
      base64: /w==             # raw bytes, for files that aren't valid UTF-8
  exit: 0
  problems: []                 # {path, rule, severity, subject?}
  stdout: |                    # optional; when present, compare the text output exactly
    ...
```

Run each case in a fresh temporary directory containing exactly its `files`. Without `stdout`, run with `--json`, and compare the problems to `problems` as lists after sorting both by path, rule, and subject. Duplicates count, so a problem reported twice fails. With `stdout`, run with exactly the case's `args` (so `--json` only if listed) and compare stdout exactly. A missing `subject` means `null`. When `exit` is 2, compare only the exit code.

## Out of scope (v0.3)

- Pages under `reference/`, and links between `docs/` and `reference/`.
- Checking that `page_type` matches the page's content. That's a judgment, not a gate.
- Checking ReadMe keeps `docops:` after a sync. That's a separate weekly check.
