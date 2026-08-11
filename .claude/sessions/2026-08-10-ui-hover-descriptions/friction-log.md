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
