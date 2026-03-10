# Editorial Preferences

This file captures Frances's editorial judgment — corrections made to Claude's doc drafts and the reasoning behind them. The `update-existing-doc` skill reads this file to avoid repeating the same mistakes.

---

## Examples

**Use one example that demonstrates the feature, not a basic + advanced pair.**
When a PR adds a new capability to an existing method, the example should showcase that capability directly. Don't add a "Basic example" first just to warm up — readers can follow a well-structured single example. Two examples side by side create cognitive overhead: readers wonder what's different and why both are needed.

**Truncate output to 2–3 representative rows, then `"..."`.**
Never show the full output when the document has more than 3–4 rows/items. The reader needs to recognize the pattern, not verify every extracted value. Use `"..."` as a placeholder for omitted rows.

**Use realistic, meaningful example data.**
Pick example data that illustrates *why* the feature is useful. A computation that converts sales figures from millions to copies, or derives a boolean flag, is more instructive than `Widget/Gadget` or generic placeholder rows. The example data should help the reader grasp the use case, not just confirm the config runs.

---

## Framing new features

**Scenario-first, not mechanism-first.**
Lead with what the user experiences or what Sensible does, then explain how to configure it. The user's mental model starts with their problem, not the implementation.

- **Preferred:** "Sensible can treat an attachment as a portfolio — a single file containing multiple documents — and extract each one separately."
- **Avoid:** "You can configure an attachment spec to use portfolio extraction, where Sensible treats a single attachment as a multi-document file."

**Don't compare to other Sensible APIs unless the user needs to choose between them.**
Explaining that email portfolio config differs from the direct extraction API creates confusion for readers who haven't encountered the API. Include API comparisons only when the reader is actively choosing between approaches.

---

## Information architecture

**Integrate new features into existing explanatory sections rather than creating new headings.**
When a PR adds a secondary capability (e.g., portfolio support for email processors), add it as a numbered item in an existing list or explanatory section rather than a new `###` heading. Reserve new sections for content with enough substance — 3+ distinct concepts, a full parameter table, or a code example — to stand alone.

**Don't add tables for non-user-configurable behavior.**
If the user can't directly configure a set of values via the API or UI, don't document those values in a table. Mention them in prose if necessary, but a table implies configurability. Example: attachment filter criteria for portfolio specs are communicated to Sensible during processor setup, not configured by the user — so a reference table was misleading and was removed.

**Don't create a section just to hold a single concept.**
If new content is 1–3 sentences that extends an existing topic, work it into the existing section rather than creating a new heading.

---

## Log

### 2026-02 — cell-rows: consolidate examples (branch `fe_cellrows_customcomputationgroup_docs`)

**What Claude did:** Created two separate examples — "Basic example" (plain cell extraction) and "Custom computation group in cellRows" (customComputationGroup usage). Each had its own config, example document reference, and full output (~20 rows).

**What Frances did:** Consolidated into a single example using a bestselling-books dataset. The example demonstrates `customComputationGroup` by converting raw sales values (stored in millions) to actual copy counts and flagging titles with >50M copies sold. Truncated output to 2 rows + `"..."`.

**Why:** Two examples force the reader to mentally compare configs. A single well-chosen example that showcases the new feature teaches both the basic pattern and the advanced usage in one pass. Full output adds length without adding comprehension.

---

### 2026-02 — email extraction: portfolio framing (branch `fe_email_portfolio_docs`)

**What Claude did:** Led with mechanism — "Optionally, you can configure an attachment spec to use portfolio extraction, where Sensible treats a single attachment as a multi-document file and segments it into multiple document types."

**What Frances did:** Reframed to scenario-first — "Optionally, Sensible can treat an attachment as a portfolio — a single file containing multiple documents — and extract each one separately."

**Why:** The scenario-first version meets the reader where they are: they're thinking about their documents, not configuration options.

---

**What Claude did:** Added a table of attachment filter criteria (All attachments / File type / Position / Combined) under the portfolio bullet.

**What Frances did:** Removed the table entirely.

**Why:** These filter criteria aren't configurable by the user via API — they're communicated to Sensible when setting up a processor. A reference table implies the user controls them directly, which is misleading.

---

**What Claude did:** Added `### Environments` as a new H3 section with email address format + webhook routing behavior.

**What Frances did:** Kept as-is.

**Why:** This section has enough distinct content (address format, code example, two behavioral rules) to warrant its own heading.
