# Page gate: specification v0.1.0

## Overview

The page gate checks what readers see on a docs page, and how pages are listed in each folder's `_order.yaml`. Every rule is one a script can decide without judgment, and each comes from a mistake that reached, or nearly reached, the published docs: a `TODO` left in an example's output, `//` comments in a SenseML example, a code fence with junk after the backticks, a new page missing from `_order.yaml`, a page listed out of title order.

`tests.yaml` is the acceptance test. Any implementation must pass every case in it. If this spec and `tests.yaml` disagree, that's a bug in one of them: report it, don't pick one.

## Pages, drafts, and folders

A **page** is a file matching `docs/**/*.md` under the repository root. Its **slug** is its filename without `.md`, except that `index.md` takes the name of the folder it's in.

A **draft** is a page whose slug starts with `draft-`. Drafts are hidden and unfinished, so the gate **doesn't check them at all**: none of the page rules apply to them, and they're skipped by the `_order.yaml` rules (listed or not, anywhere in the list). When a draft is renamed to drop `draft-`, it's checked like any other page.

A **folder** is `docs/` or any folder under it. Its **members** are its pages other than `index.md` (by slug) and its subfolders (by folder name), leaving out drafts and subfolders whose name starts with `draft-`.

## Reading a page

The gate reads the whole file, frontmatter included, as Markdown. Three things matter:

- **Code blocks.** A code block opens at a line that is optional whitespace, then three or more backticks, then the **info string**; its **language** is the info string's first word (empty for a plain fence). It closes at the next line that is optional whitespace, then at least as many backticks, and nothing else. A code block that never closes runs to the end of the file.
- **HTML comments.** Outside code blocks, everything from `<!--` to the next `-->` is hidden, across lines. A fence inside an HTML comment doesn't open a code block. Inside a code block, `<!--` is ordinary text, and ReadMe shows it.
- **Visible text** is everything that isn't inside an HTML comment, including the contents of code blocks.

A **JSON block** is a code block whose language is `json`. Inside one:

- A **string** starts at `"` or `'` and ends at the next unescaped matching quote, or at the end of the line.
- A **block comment** runs from `/*` to the next `*/`, outside strings, and can span lines. Its **text** is what's between the markers, with each run of whitespace turned into one space and the ends trimmed.
- A **line comment** is `//` outside strings and block comments. So `"https://..."` and `/* see https://... */` contain no line comment.
- A **key** is a string followed by optional whitespace and `:`. A **key comment** is a block comment that starts on the same line as, and after, a key; it belongs to the last key before it on that line. In `"id": "row", /* target is on the anchor's line */`, the comment belongs to `id`.
- The **header** is a block comment whose text is exactly `Sensible uses JSON5 to support in-line comments`.

Each JSON block is either an **output block** or a **config block**. It's an output block when its **label** says so. The label is the nearest non-blank line above the opening fence, after removing HTML comments; if that line is another code block's closing fence, there's no label. The label says "output" when, after removing every `*`, `_`, and `#`, the surrounding whitespace, and one trailing `:`, it's `Output` or `Example output`, ignoring case. So `**Output**`, `_Output_`, `## Output`, and `_Example output:_` all mark output blocks; `**Config**`, `returns:`, and no label at all mean a config block. A **commented** config block contains at least one block comment.

## Rules

Each problem has a **rule ID**, a **severity**, the **path** it's reported on, a **line** (for the page rules; none for `unreadable` and the `_order.yaml` rules), and, for some rules, a **subject**.

There are three severities. **Error** blocks a merge. **Warning (error with `--strict`)** is a rule with existing violations in the docs: it warns until they're fixed, then CI adds `--strict`. **Warning** is always a warning, because deciding whether it's really a problem takes judgment.

### Page rules

Reported on the page, at the line where the problem is.

| Rule | Severity | Subject | When |
| --- | --- | --- | --- |
| `unreadable` | error | — | The file can't be read or isn't valid UTF-8. Nothing else is checked on it. |
| `todo` | error | the token | Visible text contains `TODO`, `FIXME`, or `TBD`: uppercase, and not part of a longer word (no letter, digit, or `_` right before or after). One problem per token per line. |
| `draft-link` | error | the slug | Visible text contains `doc:draft-` followed by a slug: a link to a draft page. The subject is `draft-` and the letters, digits, `-`, and `_` that follow. |
| `fence-language` | error | the language | A code block's language isn't one of: `json`, `xml`, `yaml`, `yml`, `txt`, `bash`, `shell`, `curl`, `node`, `python`, `mermaid`, or empty. Case-sensitive. |
| `fence-unclosed` | error | — | A code block never closes. Reported at its opening fence. |
| `json-line-comment` | warning (error with `--strict`) | — | A JSON block contains a line comment. SenseML examples use `/* */`. Reported once per line. |
| `output-comment` | warning (error with `--strict`) | — | An output block contains a block comment. Real output has no comments. Reported once per block, at its first comment. |
| `json5-header-missing` | warning (error with `--strict`) | — | The page's first commented config block doesn't contain the header. Reported at its opening fence. |
| `json5-header-repeated` | warning (error with `--strict`) | — | A config block contains the header, and an earlier config block (or the same one) already did. The header goes once per page. |
| `json5-comment-repeated` | warning | the key | A key comment in a config block has the same key and the same text as a key comment in an earlier config block on the page. Later examples don't repeat earlier comments, unless the example shows a notably different configuration or behavior, which takes judgment; so this is never an error. Repeats within one block, and comments that aren't on a key, aren't checked. |

### `_order.yaml` rules

Reported on the folder's `_order.yaml` path (whether or not the file exists). A folder with no members and no `_order.yaml` is fine.

An `_order.yaml` is a YAML list of strings, read with safe-load; an empty file means an empty list. Entries that start with `draft-` are ignored.

ReadMe rewrites `_order.yaml` when someone reorders pages in its UI, and it still shows a page that isn't listed (it picks a place for it). So the rules about a folder's contents warn by default.

| Rule | Severity | Subject | When |
| --- | --- | --- | --- |
| `order-missing` | error | — | The folder has members but no `_order.yaml` |
| `order-bad-yaml` | error | — | The file isn't valid YAML, or isn't a list of strings. Nothing else is checked on it. |
| `order-duplicate` | error | the entry | An entry appears more than once. Later copies are otherwise ignored. |
| `order-stale` | warning (error with `--strict`) | the entry | An entry that isn't a member: no page or subfolder by that name. |
| `order-unlisted` | warning (error with `--strict`) | the slug | A member that isn't listed |
| `order-unsorted` | warning (error with `--strict`) | the entry | The folder is alphabetical and its entries aren't in title order (see below). One problem per folder. |

**Alphabetical folders** are listed in `scripts/gates/page/alphabetical-folders.yaml` under the root: a YAML list of folder paths relative to the root, such as `docs/Senseml reference/preprocessors`. If the file doesn't exist, no folder is alphabetical. If it isn't a YAML list of strings, the check can't run (exit 2). A listed folder that doesn't exist is ignored.

**Title order.** Take the folder's entries in file order, leaving out drafts, stale entries, and repeated copies. Each one's **sort key** is its title in lowercase: a page's frontmatter `title`, or for a subfolder, the `title` of its `index.md`. When there's no title (no frontmatter, frontmatter that isn't a YAML mapping, or a `title` that isn't a non-empty string, or no `index.md`), the sort key is the slug. The entries are in title order when the sort keys never decrease. Otherwise, sort the keys, find the first position where the file's key differs from the sorted key, and report the entry at that position. Entries with equal keys can be in either order.

## Command line

```
page_gate.py [--root DIR] [--strict] [--json] [PATH ...]
```

- `--root`: the repository root; default `.`. If `DIR/docs` isn't a folder, write a one-line error to stderr and exit 2.
- `--strict`: every "warning (error with `--strict`)" rule becomes an error. `json5-comment-repeated` stays a warning.
- `--json`: print the problems as a JSON array of objects with keys `path`, `line` (`null` when there's none), `rule`, `severity`, `subject` (`null` for rules without one), instead of text.
- `PATH`: paths relative to the root, such as the files a pull request changes. Without any, the gate checks every page and every folder under `docs/`. With paths:
  - A path to a page that exists is checked with the page rules.
  - The folder containing each path that ends in `.md` or is named `_order.yaml` gets the `_order.yaml` rules, whether or not the file still exists (so a deleted page's stale entry is caught). For an `index.md`, the parent of its folder does too, since that's where the subfolder is listed.
  - Paths outside `docs/`, other files, and folders that don't exist are ignored. So CI can pass every changed file.

**Exit code:** 0 if there are no errors (warnings allowed), 1 if there's at least one error, 2 if the check couldn't run.

**Text output:** one line per problem, sorted by path, then line (problems without a line first), then rule, then subject, then a summary line, always. Paths use `/` and are relative to the root. `<N>` counts the pages checked, not counting drafts; `<F>` counts the folders checked.

```
<path>[:<line>]: <severity>: <rule>[: <subject>]
page gate: <E> error(s), <W> warning(s), <N> page(s), <F> folder(s)
```

Problems with the same path, line, rule, and subject are one problem.

**Anything this spec doesn't cover is implementation-defined.** That includes inputs that don't occur in the docs repo today: tilde fences, line endings, byte-order marks, backticks inside a fence's info string, `<!--` inside inline code, block comments that never close, keys in single quotes, how non-ASCII titles compare, symlinks, `.MD` files, and the exact byte layout of the JSON output. `tests.yaml` pins the behavior that matters; to pin more, add a case there first.

## Testing

`tests.yaml` has a `cases` list. Each case has a `name`, optional `args` (default `[]`), `exit`, and either `expect` or `stdout`. Build its files in a fresh, empty temporary directory, which is the repository root, and run the gate from there.

**`pages`** maps a slug to a page, written to `docs/s/<slug>.md` (or to `paths[<slug>]`, when the case has `paths`) as:

```
---
title: <title as a JSON string>
---
<body>
```

The value is the body (a string), or a mapping with `title` and `body`. The title defaults to the slug, and the body to `Body.` and a newline.

**`files`** maps a repo-relative path to a string (written as UTF-8) or `{base64: ...}` (written as the decoded bytes), for files written exactly.

**`orders`** maps a folder path to its `_order.yaml`: a list (written as a YAML list), a string (written as is), or null (no `_order.yaml`). Every other folder under `docs/` that the case creates, `docs/` included, gets an `_order.yaml` listing all its pages and subfolders, so cases about page content don't have to set up `_order.yaml`.

**`alphabetical`** is a list written to `scripts/gates/page/alphabetical-folders.yaml`. Without it, that file doesn't exist.

**`expect`** lists every problem as `<page> <rule>` or `<page> <rule> <subject>`, separated by single spaces; the subject is the rest of the line. `<page>` is a slug from `pages` or a path (from `files`, or an `_order.yaml`), which therefore can't contain spaces. Line numbers aren't compared; the `stdout` cases pin them. Severity is `warning` for `json5-comment-repeated`, `warning` for the other "error with `--strict`" rules unless `args` has `--strict`, and `error` otherwise.

**Checking a case:**
- `exit` is 2: run with `args` and compare only the exit code.
- `stdout` given: run with exactly `args`; compare stdout and the exit code exactly.
- Otherwise: run with `args` plus `--json`, sort the problems and `expect` by path, rule, and subject, and compare them as lists (so a problem reported twice fails). Check each problem's severity. Then compare the exit code.

## Out of scope (v0.1)

- Whether a parameter's first appearance on a page has a comment, and whether a comment is worth having. That's a judgment, so it's an eval, graded against the JSON5 comment reference.
- Whether a later example's repeated comment is justified by a notably different configuration. The gate warns; a person decides.
- Whether examples and their output are real. That's the inline code tests' job.
- Pages under `reference/`, frontmatter (the frontmatter gate), links other than `doc:draft-`, and Vale.
