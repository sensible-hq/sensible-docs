---
name: revise-doc-style
description: Revise a SenseML reference doc draft to match the house style. Applies rules for intro sentences, metadata, examples structure, JSON5 comment placement, and parameter descriptions.
argument-hint: <path/to/draft.md>
disable-model-invocation: true
allowed-tools: Read, Edit, Write
---

Revise the doc at **$ARGUMENTS** to match the house style. Read the file first, then apply the rules below, then write it back. Report what you changed and flag any TODOs or unresolved questions you found (don't remove them — leave them in place for the author).

---

## Style rules

### Opening sentence

- **One or two sentences max.** State what the feature does, then optionally add a concrete use case.
- Pattern: `[Feature] [what it does]. For example, [use case].`
  - ✅ `Removes lines that match the specified text from all pages in the document. For example, use this preprocessor to remove watermarks.`
  - ❌ `Removes lines that match a configurable pattern. Unlike the Remove Header and Remove Footer preprocessors, which remove lines relative to a match position, this preprocessor removes the matched lines themselves.`
- Don't open with a comparison to other features. Only mention related features if the distinction is the *primary* thing to understand about this feature (and even then, put it in a **Note** or after the first sentence).
- Use present tense, active voice, third-person ("Removes…", not "Use this to remove…" as the *first* sentence).

### metadata.description

- Should be a useful search snippet — specific enough to distinguish this feature from similar ones.
- Include the key behavior detail, e.g. "from all pages in a document", "using regex or string matching".
- ✅ `Remove lines matching a pattern from all pages in a document`
- ❌ `Remove lines matching a pattern`

### Examples structure

- **Separate `##` subheadings** for each conceptually distinct use case. Don't merge separate scenarios into one config to keep the page shorter.
  - ✅ `## Remove page number lines` and `## Remove rotated watermarks` as separate examples
  - ❌ One combined config that does both, described with a bullet list
- Exception: if two things are *always* used together and don't make sense independently, a single example is fine.
- `##` heading names should be short verb phrases naming the use case (e.g. `## Remove page number lines`, `## Handwriting OCR`), not descriptions of the parameters used.

### Example intro sentence

- **One sentence.** "The following example [verb phrase]."
- Don't add a bullet list or paragraph when a single sentence suffices.
  - ✅ `The following example removes lines matching the pattern `page x of y` across all pages.`
  - ❌ `The following example shows using two preprocessors together to clean up an academic transcript before extraction:` followed by bullets

### JSON5 comments in code blocks

**Placement:** Comments go *inside* the relevant nested object — next to the key or value they describe — not above the parent object.
- ✅ Comment inside the `match` object, next to the `pattern` key
- ❌ Comment above the `{ "type": "removeLines", ... }` object

**Content:** Make comments concrete. Include an example of the matched or produced value, not just a label.
- ✅ `/* remove all page number lines, e.g., 'page 2 of 5' */`
- ❌ `/* remove "page N of N" lines */`

**Field comments:** When a field in the example exists mainly to *demonstrate* or *verify* the feature (not because it's a typical extraction field), add a comment explaining why it's there.
- ✅ `/* to verify lines were removed, print out the document text */`
- ❌ (no comment, leaving the reader to wonder why `documentRange` is used)

**Don't over-comment.** Only add comments where the purpose or value isn't immediately obvious. Don't comment every key.

### Parameter descriptions

- Use "For example" to illustrate concrete behavior inline.
- Be precise about *what* is matched/removed — "Sensible removes all lines that contain the matched text" vs "all lines that equal the matched text" are different behaviors; use the right one.
- If the exact behavior is uncertain, leave the TODO rather than guessing.

### Before/after examples

When showing the effect of a preprocessor (i.e., what the document looks like without vs with it), use **PROBLEM** / **SOLUTION** structure rather than just showing the "after" state.

### Framing: scenario-first over mechanism-first

- Lead with what the user experiences or achieves, not with internal structure (specs, matchers, selectors, config keys, etc.).
- Use concrete scenarios to anchor the reader before introducing the mechanism.
  - ✅ `an applicant might attach a single combined PDF containing both a paystub and a signed lease`
  - ❌ `configure an attachment spec to use portfolio extraction`
- Drop implementation contrasts (e.g. "unlike the direct API…", "unlike the X preprocessor…") unless the distinction is the *primary* thing the reader needs to act on. If needed, put it in a **Note** rather than the main flow.

### General

- Don't add content that isn't in the draft — this skill revises style, not substance.
- Don't resolve TODOs or fill in missing information. Leave TODOs in place and report them.
- Preserve all existing links, images, and download table references.
- Don't change `##` to `#` or restructure the Parameters/Examples/Notes section ordering.
