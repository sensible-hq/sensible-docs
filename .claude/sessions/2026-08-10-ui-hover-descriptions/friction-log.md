# Friction log — SenseML UI hover text & mini-pages (box)

---

### 1. Wordplay in descriptions

**What happened:** First draft of the box mini-page description included "Works out of the box with light-background, solid-border boxes." User flagged it as too cute given the method is literally called box.

**Rule:** Avoid any wordplay or puns that could distract or confuse in a sales-demo context. Straightforward prose only.

---

### 2. "Tell it" vs "Specify"

**First draft:**
> "Extracts all the text inside a bordered box on your document. Point it at any text inside or near the box as an anchor, and Sensible finds and reads the box automatically."

**Final (after user edits):**
> "Extracts all the text inside a bordered box in your document. Specify a word or phrase that's printed in or near the box, and Sensible finds the box automatically."

**Changes:**
- "on your document" → "in your document"
- "Point it at" / "Tell it" → "Specify"
- "reads the box" → "finds the box" (cleaner verb)
- "anchor" removed as jargon

**Rule:** Use "Specify" as the default imperative verb for hover text. Avoid informal framings like "Tell it" or "Point it at."

---

### 3. "Anchor" is jargon — replace with a plain description

**What happened:** First hover text draft used "anchor" without definition. User redirected: replace with a descriptive phrase like "a word or phrase that's printed near the box." User also noted that the phrasing "a word or phrase printed near X" is more characteristic of nearestCheckbox (omnidirectional search) than box (which uses the border as the extraction boundary). This led to a broader discussion of how each method's defining constraint or advantage should lead the description.

**Rule:** Don't use the term "anchor" in hover text. Describe the concept directly — e.g., "a word or phrase that's printed in or near the box."

---

### 4. Cross-references in hover text ("same as X")

**What happened:** percentOverlapY was drafted as "Same as percentOverlapX but applies to height rather than width." User corrected: spell it out fully.

**Correction:** "Same as percentOverlapX" → full standalone sentence: "Controls how much of a line's height must fall inside the box for Sensible to include it. Lower the default (0.8) if lines near the box edge are being cut off."

**Rule:** Hover text must be fully self-contained. Never use "same as X" cross-references — spell out the full description even if it's nearly identical to a sibling parameter.

---

### 5. "Box search starting point" — simplify compound noun phrases

**What happened:** offsetX and offsetY hover text used the phrase "box search starting point." User flagged it.

**Correction:** "box search starting point" → "starting point"

**Rule:** Avoid stacking nouns into dense compound phrases. Simplify to the shortest clear form.

---

### 6. Syntax example comments: evocative, not just descriptive

**What happened:** First syntax example comments described what the code does technically (e.g., "text near or inside the target box"). User redirected: comments should also give cues about the document context and the extracted data — not just what the parameter is, but what it looks like in a real scenario.

**First draft:**
```json
{
  "id": "rents_income",        /* name for the value you're extracting — e.g. rental income from a 1099 tax form */
  "anchor": "rents",           /* text near or inside the target box */
  "method": {
    "id": "box",               /* grabs everything inside the box borders */
    "position": "right"        /* where to start searching for the border, relative to the anchor */
  }
}
```

**Final (after several rounds):**
```json
{
  "id": "rents_income",
  "anchor": "rents",           /* matches "Rents" printed inside a box on a 1099-MISC, locates the box */
  "type": "currency",          /* formats raw text "4,200.00" into a structured value: { "value": 4200, "unit": "$" } */
  "method": {
    "id": "box",               /* extracts everything else in that box (the anchor itself is excluded) */
    "wordFilters": ["corrected"] /* ignores lines containing "corrected" — e.g. a CORRECTED stamp on an amended 1099 */
  }
}
```

**Changes:**
- Comments now name the specific document (1099-MISC), the specific field ("Rents"), and the specific value ("4,200.00")
- `position` param removed — keep examples minimal; only include params that add instructive value
- `type: currency` and `wordFilters` added to show realistic usage alongside the method
- Anchor comment clarified that the anchor is excluded from output by default
- `id` comment removed — the field name is self-explanatory

**Rule:** Syntax example comments should tell a story: name the document type, the field being extracted, and a plausible value. Avoid params that don't add teaching value. The `id` field rarely needs a comment.

---

### 7. "box-search starting point" — hyphenate, don't drop the modifier

**What happened:** Friction point #5 logged "box search starting point" → "starting point" as a simplification. User's subsequent edit reversed this: "starting point" → "box-search starting point" (hyphenated). The modifier is meaningful — it disambiguates from other kinds of starting points in the description.

**Correction:** "starting point" → "box-search starting point"

**Rule:** The right fix for a dense compound noun is to hyphenate it, not strip the modifier. Don't over-simplify to the point of losing precision.

---

### 8. Problem-first framing for actionable params

**What happened:** `sortLines` was drafted solution-first: "Corrects the reading order of lines whose vertical positions are slightly misaligned…" User rewrote it problem-first: "When misaligned text (like handwriting) gets extracted in the incorrect order, correct it by forcing Sensible to read it left to right."

**My draft:** "Corrects the reading order of lines whose vertical positions are slightly misaligned — for example, handwritten text in a box that Sensible would otherwise sort incorrectly."
**User's final:** "When misaligned text (like handwriting) gets extracted in the incorrect order, correct it by forcing Sensible to read it left to right. Recommended."

**Rule:** For params that fix a specific problem, lead with the problem scenario ("When X happens…"), then the fix. Ending with "Recommended." is appropriate when the param should be the user's default instinct.

---

### 9. Actionable failure condition over vague consequence

**What happened:** percentOverlapX/Y ended with "if lines near the box edge are being cut off." User changed to "if lines overlapping box borders aren't getting extracted."

**Rule:** Describe the failure condition in terms of the extraction outcome ("aren't getting extracted"), not a visual metaphor ("being cut off"). More precise and action-oriented.

---

### 10. Problem-first applies to offset params too, not just toggle params

**What happened:** `offsetX`/`offsetY` for intersection were drafted solution-first ("Shifts the vertical axis left or right by inches. Use when…"). User reversed the order: problem-first ("Use when the target data is slightly offset… Shifts the vertical axis…").

**My draft:** "Shifts the vertical axis left or right by inches. Use when the target value is slightly offset from the column heading's center."
**User's final:** "Use when the target data is slightly offset from the column heading's center. Shifts the vertical axis line left or right by inches."

**Additional correction:** "target value" → "target data"

**Rule:** Problem-first framing (rule #8) applies broadly — not just to enable/disable params like `sortLines`. Any param that's used to fix a specific scenario should lead with that scenario.

---

### 11. Use possessives over verbose relative clauses

**What happened:** `verticalAnchor` and `horizontalAnchor` were drafted with relative clauses: "a heading that appears at the top of it", "a label that appears alongside it." User trimmed to possessives: "its heading", "its label."

**My draft:** "Identifies the column by specifying a heading that appears at the top of it."
**User's final:** "Identifies the column by specifying its heading."

**Rule:** Prefer possessives ("its heading") over relative clauses ("a heading that appears at the top of it") — shorter and less patronizing.

---

### 12. ⚠️ Factual error — typo introduced in user's sortLines edit

**What happened:** User's rewrite of `sortLines` contained a grammatical error: "gets extracts" instead of "gets extracted." Caught and fixed in the same commit.

**Corrected:** "gets extracts" → "gets extracted"

**Note:** This is flagged as a factual/accuracy error rather than a style preference. When incorporating user edits, check for typos before committing.
