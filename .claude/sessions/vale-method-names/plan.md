# Vale: method name style enforcement

## Goal

Enforce human-readable names for identifiers in prose — e.g., "Extra Data method" instead of `` `extraData` ``, "Source IDs parameter" instead of `` `source_ids` ``.

**Exception:** first column of parameter tables in SenseML reference docs — raw code form (`` `extraData` ``) is allowed there.

---

## Decide: approach for the table exception

Vale cannot distinguish "inline code in paragraph" from "inline code in table cell" — `scope: raw` is the only way to catch backtick-wrapped identifiers, but it fires everywhere.

- [ ] **Option 1 — `scope: raw` + inline disable annotations**: add `<!-- vale Sensible.RuleName = NO/YES -->` around each parameter table in SenseML reference files. Precise; annotation burden is ~1 table per reference page.
- [ ] **Option 2 — `scope: raw` + exclude SenseML reference directory**: disable the rule for `docs/Senseml reference/**` in `.vale.ini`. Zero annotation work; loses enforcement in prose sections of those files.
- [ ] **Option 3 — custom script instead of Vale**: parse markdown properly, skip fenced blocks and table rows, check inline code only in paragraphs. Correct semantics, no annotation burden; more setup.
- [ ] **Option 4 — plain-text only (default scope)**: catch `extraData` written as plain text (no backticks) in prose. Doesn't catch the backtick form at all; different half of the same mistake.

---

## Implementation steps

- [ ] Write the Vale rule (existence or substitution, curated identifier list)
- [ ] Decide identifier list scope — enumerate known ones vs. pattern-match all camelCase/snake_case
- [ ] Wire up the table exception (per chosen option above)
- [ ] Smoke-test against a SenseML reference file and a non-reference doc
- [ ] PR
