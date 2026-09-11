# Friction log — xml-postprocessor-docs (PR #715)

PR: https://github.com/sensible-hq/sensible-docs/pull/715
Branch: `fe_xml_postprocessor_docs` | Worktree: `~/GitHub/sensible-docs-fe-xml-postprocessor-docs`

---

### 1. Misread PR comment line number — wrong section edited

**What happened:** The comment "The preceding XML is a transformation of the following `parsed_document` JSON output:" was pinned to line 341 (in the Example 1 output section). I read the diff_hunk body instead of the line field, concluded it was about the intro, and reordered the intro section. User caught it before the main-repo push.

**Correction:** "wait did you pay attention to the line number of the comment?"

**Rule:** Always read the `line` field from the PR comment object first. If `line` is not null, locate that exact line in the current file before deciding what to change. The diff_hunk body shows context from an older version of the file and is not reliable for identifying which section the comment targets.

---

### 2. Misread escaped-chars feedback — applied to wrong parameter

**What happened:** A comment asked for an inline example of XML character escaping. I provided the example under the wrong parameter. User corrected with: "you misread the feedback, it was for escaped chars like `<` and `>`!"

**Rule:** When a comment says "provide an example here," anchor to the specific parameter or sentence the comment thread is attached to. Don't infer which parameter needs the example from the comment text alone.

---

### 3. Python `open()` without `newline=''` corrupted whitespace

**What happened:** Used `open(path)` / `open(path, 'w')` without `newline=''` to replace ` ```text` with ` ```json` fences. Universal newlines mode silently mangled CRLF line endings throughout the file. User reported "whitespaces are ALL off." Had to `git checkout 179f1d447 -- xml-postprocessor.md`.

**Rule:** Always open files with `newline=''` when doing in-place text substitution on files from a mixed-OS repo. Or use the Edit tool instead of Python scripts for single-pattern replacements.

---

### 4. `sed` failed silently on backtick patterns

**What happened:** `sed -i 's/^```text$/```json/'` failed silently on lines containing backticks. The pattern appeared to match but made no changes. Switched to a Python one-liner after the failure.

**Rule:** Don't use `sed` for patterns that contain backticks or other shell-special characters without careful escaping. When in doubt, use Python or the Edit tool.

---

### 5. Style guide pass rejected — not you-centric

**What happened:** Applied a full revise-doc-style pass that changed "you transform..." constructions into "Sensible transforms..." and "the postprocessor outputs..." User reverted the entire commit: "it wasn't user-centric enough for me."

**Correction:** "i want 'you' where possible instead of an object doing an action."

**Rule:** On this project, "you" is the agent — the person with a goal who uses the tool. Don't let style guide passes flip subject from "you" to the feature or platform. When in doubt, keep "you" as the grammatical subject even if the tool is doing the work.

---

### 6. Wrong link target in jsonlogic.md

**What happened:** Updated `[postprocessed](doc:postprocessor)` to `[postprocessed](doc:json-postprocessor)`. User corrected to `doc:postprocessors` (the parent index page) for easier maintenance — so the link doesn't break if the child page is renamed.

**Correction:** "change that to the parent postprocessors page for better maintenance."

**Rule:** When updating cross-references to a renamed page, consider whether a link to the parent index is more durable than a link to the specific child page. Especially for inline body text, the index is often the right target.

---

### 7. Wrong plural/article form in overview.md cross-reference

**What happened:** Proposed `[a postprocessor](doc:postprocessors)` — kept the article "a" from the old text while changing the link target to the plural page. User corrected: using "postprocessors" without the article.

**Correction:** "using 'postprocessors' for this one not 'a postprocessor'."

**Rule:** When changing a link target from a singular to a plural/index page, also update the surrounding article and noun to match. Don't just swap the link destination and leave the article in place.

---

### 8. `attrs` example used a hardcoded constant instead of `var`

**What happened:** The intro example's `attrs` block used a hardcoded string for the `type` attribute. User flagged at line 203: "this should actually be taken from the parsed_doc not a constant... along the lines of `\"eachKey\": { \"type\": { \"var\": \"customer_name.type\" }`."

**Rule:** When showing `attrs` pulling a field's metadata (like `type`), always use `{"var": "field.type"}` to pull from `parsed_document`. Hardcoded attribute values in examples teach the wrong pattern — they suggest the author knows the type at config-write time, which defeats the purpose.
