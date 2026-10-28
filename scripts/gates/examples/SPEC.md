# Example-coverage gate: specification v0.1.0

## Overview

The example-coverage gate checks that every SenseML example a change adds or edits is covered by an inline code test, so it's run against Sensible before it's published. It compares two trees, a **base** and a **head**, and checks only the examples that differ between them, so pages that have no code tests yet don't block a change until someone edits their examples.

Examples have shipped without being run: one went out with a visible `/* TODO: verify */` in its output and was wrong (#718, fixed 8 days later); in another, the output was made up and later replaced with real output (#715); in others, someone checked the examples by hand with the extract API (#729, #730). Code tests (`scripts/doc-detective/README.md`, "Code tests") already run an example's config on its example document and compare the documented output. This gate makes sure changed examples have one, and lists the tests CI must run (see "Running the covering tests").

`tests.yaml` is the acceptance test. Any implementation must pass every case in it. If this spec and `tests.yaml` disagree, that's a bug in one of them: report it, don't pick one.

## Base and head

The gate takes two directory trees: the base (before the change) and the head (after it). For a pull request, the head is the checkout and the base is the merge base, checked out or extracted next to it (for example with `git worktree add --detach` or `git archive`). Directories, not git refs, because:

- the docs workflow can gate an agent's working tree before anything is committed;
- the gate needs no git, so it can't depend on clone depth or which refs were fetched;
- a test case is two small folders, not a git history.

A **page** is a file matching `docs/**/*.md` in a tree; its **path** is relative to the tree's root, with `/`. A **draft** is a page whose filename starts with `draft-`. The gate never checks drafts, so a draft's examples are checked when it's renamed to drop `draft-` (as new blocks, since nothing in the base has its path). A head page's **base page** is the base tree's page with the same path, if there is one. A head page is **changed** if it has no base page or its text differs from its base page's.

## Reading a page

The gate reads a page the way the page gate does (`scripts/gates/page/SPEC.md`, "Reading a page"). The definitions it uses are repeated here so this spec stands alone; if they ever differ, the page gate's are the source and this copy is the bug.

- **Code blocks.** A code block opens at a line that is optional whitespace, then three or more backticks, then the **info string**; its **language** is the info string's first word. It closes at the next line that is optional whitespace, then at least as many backticks, and nothing else. A code block that never closes runs to the end of the file.
- **HTML comments.** Outside code blocks, everything from `<!--` to the next `-->` is a comment, across lines. A fence inside a comment doesn't open a code block. A comment's **text** is what's between `<!--` and `-->`, trimmed.
- A **JSON block** is a code block whose language is `json`. Inside one, a **string** starts at `"` or `'` and ends at the next unescaped matching quote, or at the end of the line; a **block comment** runs from `/*` to the next `*/` outside strings; a **line comment** runs from `//` outside strings to the end of the line; a **key** is a string followed by optional whitespace and `:`, and its name is the string without its quotes.
- A JSON block's **label** is the nearest non-blank line above its opening fence, after removing comments; if that line is another code block's closing fence, there's no label. The label **says output** when, after removing every `*`, `_`, and `#`, the surrounding whitespace, and one trailing `:`, it's `Output` or `Example output`, ignoring case.
- A comment is **directly above** a code block when only whitespace lies between the comment's `-->` and the start of the block's opening fence line. This is where the code-test markers go; it's the rule `code_tests.py` uses to find a marker's block.

## Example blocks

Each JSON block is a config block, an output block, or plain JSON, decided by the first of these that applies:

1. A comment directly above it whose text starts with `inline output` makes it an **output block**, and one starting with `inline config` makes it a **config block**. The test markup says what the block is.
2. A label that says output makes it an **output block**.
3. A key named `fields`, `method`, `preprocessors`, `postprocessor`, `computed_fields`, `fingerprint`, or `sections`, and no key named `parsed_document`, makes it a **config block**.
4. Anything else is **plain JSON**, and the gate never checks it.

Config and output blocks are **example blocks**. Rule 3 is how the gate tells SenseML from other JSON. Measured on `docs/` at v0 (159 pages that aren't drafts, 420 JSON blocks): 110 blocks are output blocks by rules 1 and 2. Of the other 310, 182 have one of the keys, and 4 of those also have `parsed_document`: they're API responses (`"fields"` appears inside them), so 178 are config blocks. The 132 plain JSON blocks are API requests and responses, webhook payloads, `curl` commands in `json` fences, JsonLogic rules and their results, type fragments (`"type": { "id": "date" }`), anchor fragments, and outputs whose label doesn't say output (`This returns:`, `The preceding config returns:`). A field excerpt (`{ "id": ..., "method": ... },`) or a `"fingerprint": {...}` excerpt is a config block, because `code_tests.py` can run both as `inline config` fragments.

## Changed blocks

A JSON block's **content** is its text with block comments and line comments removed, and every whitespace character outside strings removed. So reformatting, and adding or editing `/* */` comments, doesn't change a block; editing a key, a value, or the text of a string does.

Go through a changed head page's JSON blocks in order. A block is **unchanged** if its base page has a JSON block with the same content that isn't already paired; pair them. Otherwise it's **changed**. So:

- A block edited in place, or added, is changed.
- A block moved within a page is unchanged. If the head has more copies of a block than the base, the later copies are changed.
- A block moved to another page, or on a renamed page, is changed: blocks pair only within the same path.
- The kind doesn't take part: relabeling a block, or adding a code test around it, doesn't change it.

The gate checks only **changed example blocks**. Unchanged blocks are never reported, whether or not they're covered, and neither is anything on a page that isn't changed.

## Code tests

The markup is defined in `scripts/doc-detective/README.md` ("Code tests") and read by `scripts/doc-detective/codetests/markup.py`. The gate reads only the parts it needs to decide coverage, and reads them on changed pages only:

- A **code test** opens at a comment whose text is `code test`, optionally followed by whitespace and its **header**, other than `code test end`. It closes at the next comment whose text is exactly `code test end`. If another `code test` comment comes first, or there's none, the test is **unclosed**: it runs up to that comment or the end of the page, and covers nothing. A table test (`<!-- table test ... -->`) isn't a code test. Its rows never cover a code block.
- Its **test ID** is the header's `testId`, when the header is a JSON object whose `testId` is a non-empty string of lowercase letters, digits, and underscores. Otherwise it has none.
- A **marker** is a comment whose text starts with `inline config` or `inline output`, optionally followed by options (such as `{"fragment": "field"}`).
- A block is **covered** by a code test with a test ID when a marker directly above the block is inside that test (between its opening and closing comments).

The gate doesn't run `code_tests.py` or check the rest of the markup (documents, fixtures, `expect`, the blocks' JSON syntax): `code_tests.py --check-syntax` does that, offline, when CI runs the covering tests.

## Exemptions

Some examples can't be code-tested: pseudo-config with placeholders, excerpts that don't run on their own, configs that need a document the test account can't have. To exempt one, put this comment directly above it:

```markdown
<!-- no code test: needs a scanned document with handwriting -->
```

The comment's text must be exactly `no code test`, or start with `no code test:`. The **reason** is the rest after the colon, with each run of whitespace turned into one space and the ends trimmed. An exempted changed block is reported as a warning, with the reason, so reviewers see every exemption. An exemption with no reason is an error. An exemption on an unchanged block or a plain JSON block is ignored.

## Rules

Each problem has a **rule ID**, a **severity**, the **path** of the head page, a **line**, and, for some rules, a **subject**. **Error** blocks a merge; **warning** doesn't.

| Rule | Severity | Subject | When |
| --- | --- | --- | --- |
| `unreadable` | error | — | A head page can't be read or isn't valid UTF-8. No line. Nothing else is checked on it. A base page that can't be read counts as missing. |
| `config-untested` | error | — | A changed config block that isn't covered or exempted. At its opening fence. |
| `output-untested` | error | — | A changed output block that isn't covered or exempted. At its opening fence. |
| `exempt` | warning | the reason | A changed example block with an exemption that has a reason. At its opening fence. |
| `exempt-no-reason` | error | — | A changed example block with an exemption that has no reason. At its opening fence. |
| `test-markup` | error | what's wrong | On a changed page, a code test the gate can't read: `header` (no test ID; at the opening comment), `unclosed` (at the opening comment), `duplicate-id` (a test ID an earlier code test on the page has; at the later opening comment), `marker-outside-test` (a marker that isn't inside a code test; at the marker), or `marker-without-block` (a marker inside a code test with no code block directly below it; at the marker). |

A code test with a `header` or `unclosed` problem covers nothing, so its blocks are also reported as untested if they're changed. A duplicated test ID still covers its blocks.

## Command line

```
example_coverage.py --base DIR --head DIR [--json] [--print-tests]
```

- `--base`: the base tree. If `DIR` isn't a folder, write a one-line error to stderr and exit 2. A base with no `docs/` has no pages, so every head block is new.
- `--head`: the head tree. If `DIR/docs` isn't a folder, write a one-line error to stderr and exit 2.
- `--json`: print JSON instead of text (see below).
- `--print-tests`: print the covering tests (see "Running the covering tests") instead of the problems.

**Exit code:** 0 if there are no errors (warnings allowed), 1 if there's at least one error, 2 if the check couldn't run. `--print-tests` doesn't change it.

**Text output:** one line per problem, sorted by path, then line (problems without a line first), then rule, then subject, then a summary line, always. `<B>` counts the changed example blocks; `<T>` counts the covering tests.

```
<path>[:<line>]: <severity>: <rule>[: <subject>]
example coverage: <E> error(s), <W> warning(s), <B> changed block(s), <T> test(s)
```

**JSON output:** an array of objects with keys `path`, `line` (`null` when there's none), `rule`, `severity`, `subject` (`null` for rules without one), in the same order.

## Running the covering tests

A code test is a **covering test** when it's on a changed head page that isn't a draft, has a test ID, and either covers a changed example block, or its text (from its opening comment's `<!--` to its closing comment's `-->`) doesn't appear in its base page. So an edited or new test runs even if its blocks didn't change. A test ID that appears twice on a page is listed once.

`--print-tests` prints one line per covering test, `<path>`, a tab, then `<testId>`, sorted by path then test ID, with no summary line; nothing when there are none. With `--json`, it prints an array of `{"path": ..., "testId": ...}` objects in that order.

The gate is half of the check. CI, from the head tree's root:

1. Runs the gate. Exit 1 fails the check.
2. For each page in `--print-tests`, runs `scripts/doc-detective/code_tests.py --file <path> --check-syntax --test <id> [--test <id> ...]` with that page's test IDs. This needs no keys or network, so it runs on every pull request.
3. Runs the same command without `--check-syntax`, with the docs test account's keys. Any test that fails fails the check.

This spec doesn't define `code_tests.py`; its README does.

**Anything this spec doesn't cover is implementation-defined.** That includes inputs that don't occur in the docs repo today: tilde fences, line endings, byte-order marks, comments inside a code test's header, a `code test end` with no opening comment, symlinks, `.MD` files, base and head being the same folder, and the exact byte layout of the JSON output. `tests.yaml` pins the behavior that matters; to pin more, add a case there first.

## Testing

`tests.yaml` has a `cases` list. Each case has a `name`, optional `args` (default `[]`), `exit`, and either `expect` (with optional `tests`) or `stdout`.

In a fresh, empty temporary directory, create the folders `base/` and `head/`, then write the case's `base` and `head` mappings (each optional, default empty) into them. Each mapping's key is a slug, written to `docs/s/<slug>.md`, or a path containing `/`, written there; the value is the file's exact text (a string, written as UTF-8) or `{base64: ...}` (written as the decoded bytes). There's no frontmatter. Run the gate as `example_coverage.py --base <tmp>/base --head <tmp>/head` followed by `args`.

**`expect`** lists every problem as `<page> <rule>` or `<page> <rule> <subject>`, separated by single spaces; the subject is the rest of the line. `<page>` is a slug or a path. Severity is `warning` for `exempt` and `error` for the rest. Line numbers aren't compared; the `stdout` cases pin them.

**`tests`** (default `[]`) lists every covering test as `<page> <testId>`.

**Checking a case:**
- `exit` is 2: run with `args` and compare only the exit code.
- `stdout` given: run with exactly `args`; compare stdout and the exit code exactly.
- Otherwise: run with `args` plus `--json`, sort the problems and `expect` by path, rule, and subject, and compare them as lists (so a problem reported twice fails). Check each problem's severity, then the exit code. Then run with `args` plus `--json --print-tests`, and compare the result with `tests`, sorted by path and test ID, as lists; the exit code must be the same.

## Out of scope (v0.1)

- Whether the covering tests pass. That's `code_tests.py`, run by CI as above.
- Whether an exemption is justified. A reviewer reads the warning.
- Outputs whose label doesn't say output (`This returns:`) are plain JSON, so changing only such a block isn't caught. Changing its config is, and the config's code test then needs an `inline output`.
- Removing a code test, or an exemption, from an unchanged block. The block is unchanged, so it's not checked.
- Non-JSON examples (`python`, `node`, `bash`), and the examples under `reference/`.
