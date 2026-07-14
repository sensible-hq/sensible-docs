# Template: Automating Data Extraction from [DOC TYPE]

Variables used throughout this template:
- `[doc type]` — singular, lowercase (e.g., "loss run", "acord form", "certificate of insurance")
- `[doc types]` — plural (e.g., "loss runs", "acord forms")
- `[industry]` — industry name (e.g., "insurance underwriting", "commercial real estate")
- `[use case]` — downstream workflow that depends on the data (e.g., "assess business risk", "evaluate portfolio health")
- `[sensible feature]` — the primary Sensible feature highlighted (e.g., "Sections", "Query Group", "NLP Table")
- `[challenge theme]` — the overarching structural challenge (e.g., "complex repeating structures", "cross-carrier layout variability")

---

## TITLE

`Automating Data Extraction from [Doc Types]`

Do NOT include "with Sensible" in the title — this post style is more editorial than tutorial.
Do NOT use "How to" — that signals a code walkthrough, which this post is not.

---

## BYLINE

`By [Author Name], [Role], Sensible | [N] min read`

Aim for a 4–5 minute read (400–600 words total).

---

## OVERVIEW (1–2 paragraphs, under heading "## Overview")

**Paragraph 1 — What the document is and why it matters:**

> "[Doc types] are [describe what they are — who produces them, what they summarize, what time period they cover]. [1–2 sentences on why companies in [industry] need this data — what decisions or workflows depend on it.]"

Example (loss runs):
> *"Loss runs—reports from insurance carriers summarizing claims made during policy coverage—help carriers assess business risk by reviewing claim types, frequency, and financial impact. Carriers adjust premiums or deny coverage based on perceived risk levels."*

**Paragraph 2 (optional) — Volume or format framing:**

Add if the sheer volume or format inconsistency motivates the need for automation. Skip if paragraph 1 already makes the case clearly.

> "[Doc types] typically arrive as [PDFs / scanned images / multi-page reports]. While manual transcription [seems feasible / works at low volume], [describe why it breaks down — volume, error rate, turnaround time]."

---

## THE CHALLENGE (under heading "## The Challenge")

Open with 1 sentence naming the core problem, then list 3–4 specific extraction challenges as bullets with bold lead phrases.

Opening sentence pattern:
> "[Doc type] [reports / documents] typically appear as [format] with [high-level structural description]. While [seemingly simple alternative], the [volume / variability / complexity] makes it [impractical / error-prone]."

Example (loss runs):
> *"Loss run reports typically appear as PDF files with table-like structures. While manual transcription seems feasible, the volume and error-proneness make it impractical."*

**Bullet format:**
> - **[Bold lead phrase]**: [1 sentence describing the specific challenge]

Example bullets:
> - **Complex table structures**: Single columns contain multiple data points; tables nest within rows
> - **Variable claim counts**: Documents range from zero to many claims requiring complete capture
> - **Multiple policies**: Claims from various policies need proper association with correct policy numbers

Aim for 3–4 bullets. Each should name a concrete structural property of the document — not generic statements like "PDFs are hard to parse."

---

## THE SOLUTION: SENSIBLE [FEATURE] (under heading "## The Solution: Sensible [Feature]")

2–3 paragraphs. Conceptual — no SenseML code blocks. Explain what the feature does and how it maps to the challenges above.

**Paragraph 1 — Introduce the feature:**

> "Sensible [introduced / addresses this with] [Feature] — [one sentence definition]. [1–2 sentences on how users configure it at a high level — what they define, what Sensible handles automatically]."

Example (Sections):
> *"Sensible introduced Sections—a feature designed for parsing complex, repeating document sections. Users define section boundaries (start and end points) and specify target data fields within those bounds."*

**Paragraph 2 — Map the feature to the document:**

> "For [doc types], [describe how the feature is applied — what serves as section boundaries, what fields are extracted within each section, what the output looks like]."

Example (loss runs):
> *"For loss runs, each claim becomes a section starting with 'CWC'-prefixed claim numbers and ending below 'Total.' Sensible's methods extract specific fields: injury dates, descriptions, payout amounts, and more. The output appears as a structured list where each element represents an individual claim with accompanying data."*

**Paragraph 3 (optional) — Additional capability or output shape:**

Use if there's a secondary capability worth calling out before the advantage section. Skip if the advantage section covers it.

---

## [OPTIONAL] [FEATURE] ADVANTAGE (under heading "## [Feature Name] Advantage")

Include when there's a differentiating capability that extends the core feature — typically something that makes the solution more powerful than readers might expect.

1–2 paragraphs. Same conceptual style — no code.

> "[Feature] can [do something beyond the basic case — e.g., nest within other sections, handle zero-count edge cases, combine with computed fields]. [Explain the practical benefit — what problem it solves that the reader would otherwise face]."

Example (Nested Sections):
> *"Sections can nest within other sections, enabling extraction across multiple policies in one document without manual PDF splitting. Each policy becomes a parent section containing individual claims as child sections."*

---

## CONCLUSION (under heading "## Conclusion")

1 paragraph. Brief, direct. Point to next steps — demo, documentation, or sign-up.

Pattern:
> "Sensible continues [developing / improving] [tools / methods] for [doc types with the challenge theme]. [1 sentence on what readers can do next — request a demo, sign up, or read the docs]."

Example:
> *"Sensible continues developing tools for complex documents. Users interested in parsing loss runs should request a demonstration."*

Avoid: salesy superlatives, vague closing lines like "the future of document AI is here."

---

## LENGTH AND TONE NOTES

**Length:** 400–600 words total. Aim for 4–5 minute read. This is not a tutorial — every sentence should earn its place.

**Tone:** Informative but editorial. Third-person or second-person both work; pick one and stay consistent. Not tutorial ("let's walk through…") — save that register for the longer how-to posts.

**What to omit entirely:**
- SenseML code blocks (those belong in the `blog-how-to-parse-x` skill)
- Screenshot placeholders
- "What we'll cover" lead-in
- Prerequisites section
- "Putting it all together" combined config
- FAQ section
- "Connect Sensible to your workflow" integration methods section

**What to keep short:**
- Bullet lists: 3–4 items max, each one sentence
- Paragraphs: 2–4 sentences max
- Section headings: match the examples above — do not add extra H3 subheadings

**When to use this style vs. the how-to style:**
- Use this template when the document type benefits from a conceptual overview rather than a hands-on walkthrough — e.g., when the main story is a Sensible architectural feature (Sections, portfolio extraction) rather than a specific SenseML method.
- Use `blog-how-to-parse-x` when the goal is to walk a developer through a working config with real code and output.
