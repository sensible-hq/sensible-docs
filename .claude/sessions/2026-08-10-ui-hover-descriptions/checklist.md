# Session: SenseML UI Hover Descriptions
Date: 2026-08-10

## Goal
Generate two levels of UI-friendly descriptions for SenseML methods and parameters:
1. **Hover text** — 1–2 sentences, context-independent, newbie-friendly, sales-demo safe
2. **Mini-page** — expanded description + syntax example with inline comments (for accordion/tab UI)

Output: `senseml-descriptions.json` (hover text) + `senseml-descriptions/*.md` (mini-pages)

---

## Checklist

### Phase 1 — Determine scope
- [ ] Export real customer configs from production and save to a working file
- [ ] Analyze configs for most-used methods (aim for top ~5)
- [ ] Analyze configs for most-used parameters (aim for top ~10)
- [ ] Flag any parameters/methods used in ways that differ from documented intent (jerry-rigged patterns)
- [ ] Finalize list of targets: methods + parameters to describe

> **PoC shortcut**: skipping config analysis for now. Using all methods that have a "Syntax example" section as a proxy for high-value targets:
> - Layout-based: box, intersection, region, row
> - LLM-based: query-group, list, nlp-table
> - Also: sections (sections/index.md), types (field-query-object/types.md)
> - Global params: sortLines, tiebreaker, xRangeFilter

### Phase 2 — Write hover text (JSON)
- [ ] For each target: read the primary doc page + all linked pages referenced in its description
- [ ] Draft 1–2 sentence hover text using the prompt template below
- [ ] Review against criteria: standalone (no link required), jargon-free, sales-safe
- [ ] Populate `senseml-descriptions.json`

### Phase 3 — Write mini-pages (MD)
- [ ] For each target: write brief expanded description (3–5 sentences)
- [ ] Write plausible syntax example (real-looking values, not `foo`/`bar`)
- [ ] Add inline comments to syntax example explaining each part
- [ ] Save to `senseml-descriptions/<name>.md`

### Phase 4 — Review
- [ ] Run docs-checker on any prose
- [ ] Confirm examples are syntactically valid SenseML
- [ ] Commit and push

---

## Prompt Template: Hover Text

**System:**
You are writing one-line hover descriptions for a code editor UI. The audience is a non-technical prospective customer watching a live product demo — they have no prior knowledge of the system and will not click any links. Your description must be completely self-contained.

**Rules:**
- 1–2 sentences maximum
- No jargon without inline definition
- No phrases like "see also", "refer to", or any link-dependent context
- Focus on what the parameter *does for the user*, not what it *is* technically
- Plain English; avoid gerunds at the start ("Extracts…" not "Extracting…")

**Input format:**
```
PARAMETER: <name>
TYPE: <string | number | boolean | object | array>
DOC EXCERPT: <paste the description from the docs page>
LINKED CONTEXT: <paste relevant excerpts from any linked pages>
USAGE NOTES: <any observed real-world usage patterns that differ from docs>
```

**Output format:**
```
HOVER TEXT: <1–2 sentences>
```

---

## Prompt Template: Mini-Page

**System:**
You are writing a compact help panel for a code editor sidebar. The audience is a new user who is actively building their first configuration. They can read 5–7 sentences and one code example before losing attention.

**Rules:**
- Description: 3–5 sentences. Cover what it does, when to use it, and one thing to watch out for.
- Syntax example: show a realistic, plausible snippet (not abstract placeholders). Use actual document field names that make sense for the method's common use case.
- Inline comments: add a `//` comment on each non-obvious line of the example explaining *why*, not just *what*.
- No links. No "see also". No cross-references.

**Input format:**
```
METHOD/PARAMETER: <name>
TYPE: <type>
DOC EXCERPT: <full doc section>
LINKED CONTEXT: <relevant linked page excerpts>
USAGE NOTES: <real-world patterns>
EXAMPLE FROM FIELD: <paste a real or representative config snippet if available>
```

**Output format:**
```
## <Name>

<Description paragraph>

**Syntax**
\`\`\`json
<example with inline comments>
\`\`\`
```

---

## Notes
- Jerry-rigged usage patterns should inform the hover text (describe what it's actually used for, not just the official intent)
- If a parameter behaves differently depending on context (e.g., belongs to method vs. object), note this in the mini-page but keep hover text universal
- Sales-safe = avoid implementation details that raise concerns (performance, limits, known gaps)
