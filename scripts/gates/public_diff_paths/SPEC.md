# Public diff paths gate: specification v0.1.0

## Overview

This repository is public. Some kinds of files belong only in private tooling repos: workflow run folders and run logs, internal specs, design notes, and evaluation labels. The gate fails a change that adds or changes a file at one of those paths, so a copy made by mistake can't merge.

It checks paths only, never file content.

`tests.yaml` is the acceptance test. Any implementation must pass every case in it. If this spec and `tests.yaml` disagree, that's a bug in one of them: report it, don't pick one.

## What it compares: git refs, not folders

The gate takes two git refs, `--base` and `--head`, and checks the files that `head` adds or changes since its merge base with `base` (`git diff BASE...HEAD`, three dots). That is exactly what a pull request adds, whatever `base` has gained since the branch was cut.

Why refs and not two folders: the question is "what does this change add", which git answers directly, including renames and type changes, without two full checkouts or a tree walk. A folder comparison would also need its own rules for ignored and untracked files; a ref has none.

The changed paths are the output of

```
git -C <repo> -c core.quotePath=off diff --name-only --no-renames --diff-filter=d -z BASE...HEAD
```

- `--no-renames`: a rename is a delete plus an add, so a file moved into a forbidden folder is an add there.
- `--diff-filter=d`: deleted files are left out. Removing a forbidden file is always allowed.

## Patterns

A path is **forbidden** when it matches at least one pattern. The patterns are the built-in ones, then the lines of the denylist file, in that order.

**Built-in patterns** (they can't be turned off):

| Pattern | What it keeps out |
| --- | --- |
| `**/runs/` | workflow run folders |
| `**/specs/` | internal specs |
| `**/design/docops/` | design notes for the docs tooling |
| `**/judges/*/labels/` | evaluation labels |
| `*.jsonl` | run logs, and any other JSON Lines file |

**The denylist file** adds patterns, one per line. Leading and trailing whitespace is stripped; blank lines and lines starting with `#` are ignored. A line that is `/`-only, starts with `/`, or has a `..` component is a bad pattern (exit 2). The default file is `denylist.txt` beside the script; it ships with no patterns.

**How a pattern matches** a path (repo-relative, `/`-separated, as git prints it):

- A pattern with no `/` (such as `*.jsonl`) matches the path's last component, at any depth.
- Any other pattern is split on `/` and matched component by component from the repository root. A trailing `/` makes it a **folder pattern**: it matches every path inside a matching folder (at least one more component after the pattern's last one). Without a trailing `/`, the path must have exactly the pattern's components.
- A `**` component matches zero or more whole components. So `**/runs/` matches `runs/a.json` and `docs/x/runs/a.json`.
- In every other component, `*` matches any run of characters (none included), `?` matches one character, and `[...]` matches one character from a set (Python `fnmatch.fnmatchcase`). None of them crosses a `/`.
- Matching is case-sensitive: `Runs/` isn't `runs/`.

## Command line

```
public_diff_paths.py --base REF --head REF [--repo DIR] [--denylist FILE]
```

- `--base`, `--head`: required. Any ref git can resolve to a commit: a branch, a tag, a SHA, `origin/v0`.
- `--repo`: the git checkout; default `.`.
- `--denylist`: the denylist file; default `denylist.txt` beside the script.

**Exit code:** 0 if no changed path is forbidden, 1 if at least one is, 2 if the check couldn't run: a missing argument, `--repo` isn't a git checkout, a ref that isn't a commit, refs with no merge base, a denylist file that can't be read, or a bad pattern. On exit 2, the gate writes a one-line error to stderr starting with `public_diff_paths.py: ` and nothing to stdout.

**Text output:** one line per forbidden path, sorted by path (as strings), then a summary line, always. Each path is reported once, with the first pattern it matches.

```
<path>: error: forbidden-path: <pattern>
public diff paths: <E> error(s), <N> changed path(s)
```

`<N>` counts every changed path (added or changed, not deleted). The problem lines use the form the other public gates use, `<path>: error: <text>`.

## Testing

`tests.yaml` has a `cases` list. Each case has a `name`, `exit`, and either `expect` or `stdout`.

**Building a case**, in a fresh, empty temporary directory `$TMP`:

1. Create a git repo in `$TMP/repo`. Write `base` (a map of repo-relative path to file text, UTF-8) and commit it on a branch named `base`. A case without `base` commits one file, `README.md`, so the branch exists.
2. Create a branch `head` from `base`, write `head` (the same kind of map) over the files, remove each path in `delete`, and commit everything (an empty commit when nothing changed).
3. If the case has `base_after` (the same kind of map), check out `base` again, write it, and commit: `base` moves on after `head` branched.
4. Write `denylist` (a string; default empty) to `$TMP/denylist.txt`.

**Running a case:** from `$TMP/repo`, run the gate with `args`. `args` defaults to `[--base, base, --head, head, --denylist, $TMP/denylist.txt]`; `$TMP` in `args` is the temporary directory.

**Checking a case:**

- `exit` is compared always. On exit 2, stdout must be empty and stderr one line starting with `public_diff_paths.py: `.
- `stdout` given: compared exactly.
- `expect` given: a list of `<path> -> <pattern>`, compared, in order, with the problem lines (all but the summary line) after each is rewritten the same way (`<path>: error: forbidden-path: <pattern>` becomes `<path> -> <pattern>`).

## Out of scope (v0.1)

- File content. A private quote pasted into a page is a content problem; this gate can't see it.
- Files `base` already has. The gate checks what a change adds, not the whole tree.
- Running in CI on every pull request. No workflow runs the gate yet; a caller runs it with the PR's base and head.
