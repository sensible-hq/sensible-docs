# Template: How to extract data from [DOCUMENT TYPE] with [LLMs and] Sensible

Variables used throughout this template:
- `[doc type]` — singular, lowercase (e.g., "bank statement", "rent roll", "closing disclosure")
- `[doc types]` — plural (e.g., "bank statements", "rent rolls")
- `[doc type variant]` — specific variant used in the post (e.g., "Chase bank statements", "Medicaid EOBs")
- `[industry]` — industry name (e.g., "proptech", "healthcare")
- `[supported variants]` — list of supported variants (e.g., "Medicaid, Tricare, and Cigna EOBs")
- `[field]` — a specific extracted field name (e.g., "date issued", "loan type")
- `[fields]` — bullet list of fields extracted in the post

---

## TITLE

`How to extract data from [doc types] with [LLMs and] Sensible`

Include "with LLMs and Sensible" only for variable-layout documents (resumes, rent rolls). For structured/semi-structured documents, use "with Sensible."

---

## INTRO (2–3 paragraphs, no heading)

**Paragraph 1 — Industry context and pain point:**

Variant A — "If you're building" opener (closing disclosures, EOBs):
> "If you're building software [in / for] [industry], chances are that you've come across the [doc type]. [1–2 sentences describing what it contains and why companies need the data.]"

Examples:
- *"If you're building software in proptech, chances are that you'll have come across the closing disclosure. A closing disclosure contains the final details about the home buyer's mortgage – things like loan terms, projected monthly payments, and the closing cost."*
- *"If you're building software for healthcare providers, chances are that you've come across the explanation of benefits (EOB) document."*

Variant B — direct industry description (bank statements, rent rolls, resumes):
> "[Describe who uses the document and for what. 1–2 sentences on what downstream workflows depend on the data.]"

Examples:
- *"Companies that build lending and mortgage solutions in proptech often need to automate a solution to parse information in bank statements. By extracting and analyzing financial data from bank statements, these companies can more accurately assess an individual's or business's financial health and risk profile to make better lending and mortgage decisions."* (bank statements)
- *"In the real estate industry, rent rolls are key documents used for valuing properties and for evaluating their commercial health. For example, high rents, low vacancy, and long tenure indicate good health; low rents, high vacancy, and short tenure indicate poor health. Companies in the prop tech space need this sort of data to build solutions such as automated rent collection and billing, rent trend analytics, and property ROI analytics."* (rent rolls)
- *"Many companies face challenges when automating hiring and recruitment. Aggregating and analyzing candidate data can improve hiring, but is often a taxing manual process."* (resumes)

Newer posts (commission statements, delivery orders, cyber insurance quotes, dec pages) end paragraph 1 with the format variability characterization — the specific structural detail that motivates which extraction approach Sensible uses. Older posts use this near-verbatim closing line instead:
> "However, they often lack access to [doc types] in any format other than PDFs, which makes data extraction a potentially difficult problem."

Closing disclosures uses a different version:
> "The information found in a [doc type] isn't always easily accessible. [Doc type] data isn't usually available through an API."

**Paragraph 2 — Introduce Sensible + LLM vs. deterministic framing (always required):**

This paragraph is required in every post regardless of which methods the config uses. It introduces Sensible and explains which extraction approach fits this document type, why the document structure makes it well-suited to that approach, and what the complementary method handles. The paragraph opens with "Sensible handles this through [X]" — where "this" refers directly to the variability or volume challenge named in paragraph 1.

The "[Doc types] are well suited to this approach" clause is mandatory in every variant. It must cite a specific structural property of this document type — fixed column positions, consistent label text, stable table structure, or degree of cross-issuer layout variability. Do not write "well suited" without the concrete justification.

All variants end with "Both run through the same API" or equivalent.

**Variant A — Deterministic-primary** (post showcases a carrier- or vendor-specific layout config):

Pattern:
> "Sensible handles this through [carrier / vendor]-specific layout configs. [Doc types] are well suited to this approach: [specific structural reason — e.g., fixed column positions, consistent label text across all [carrier] documents]. For [carriers / vendors] without a dedicated config yet, a generalized LLM config handles the same fields without per-[carrier / vendor] configuration. Both run through the same API."

Examples:
- *"This post uses Sun Life's commission statement as a worked example. Every carrier has its own layout — column ordering, label conventions, subtotal placement — so the right approach is a per-carrier deterministic config: fixed column positions and consistent label text mean the same config extracts reliably every month. For the long tail of smaller carriers, a generalized LLM config handles the same fields without per-carrier work. Both run through the same API."* (commission statements)
- *"Sensible handles this through carrier-specific layout configs. Cyber quotes are well suited to this approach: the structured Coverage Schedule tables and endorsement grids provide reliable anchor points that deterministic methods extract precisely, with no LLM calls and no prompt maintenance overhead on high-volume carriers. Each carrier gets its own config anchored to its label text and document structure, returning a normalized output schema across all carriers. For carriers without a layout config yet, a generalized LLM config handles extraction on day one without per-carrier configuration, covering the long tail of carriers that appear at low volume or in one-off submissions."* (cyber insurance quotes)

**Variant B — LLM-primary** (post showcases a generalized LLM config):

Pattern:
> "Sensible handles this with a generalized LLM config. [Doc types] are well suited to this approach: [specific reason why cross-issuer variability makes per-issuer templating impractical]. For [carriers / vendors] appearing at high volume, a [carrier / vendor]-specific layout config delivers deterministic precision — no LLM calls, no prompt maintenance overhead. Both run through the same API."

Example:
- *"Sensible handles this with a two-tier approach. A generalized LLM-powered template covers the long tail of vendor formats out of the box: no per-vendor configuration required, ready to extract on day one. For vendors whose invoices are high-volume or consistently underperforming on the generalized template, a layout-specific template can be built in 15 to 45 minutes depending on field count and document complexity. Both approaches run through the same API. You get breadth from the generalized template and precision where the volume justifies it."* (invoices)

**Variant C — Hybrid** (post showcases both a generalized LLM config and a deterministic layout config):

Pattern:
> "Sensible handles this through two complementary configs. [Doc types] are well suited to this hybrid approach: [explain why long-tail variability requires LLM while high-volume formats reward a dedicated layout config]. A generalized LLM config covers any [carrier / vendor] on day one — no per-format configuration required. A [carrier / vendor]-specific layout config handles high-volume formats deterministically — no LLM calls, consistent output. Both run through the same API."

Examples:
- *"Sensible handles this through two complementary configs. Dec pages are well suited to this hybrid approach: carrier variability across the long tail requires LLM reasoning to handle without per-carrier configuration, while high-volume carriers like GEICO have fixed, predictable field positions that deterministic methods extract precisely. A generalized LLM config uses the Query Group and List methods to extract key fields from any carrier's dec page without prior templates, covering your full carrier mix on day one. A carrier-specific layout config uses deterministic methods (Region and Row) for carriers appearing at high volume, reducing per-document LLM cost and eliminating prompt latency on fields with fixed positions. Both route through the same API endpoint, and Sensible validates each extracted field against its declared type before returning output."* (insurance declaration pages)
- *"Sensible addresses this dual challenge through two complementary approaches. The platform employs a generalized LLM template requiring no per-carrier configuration that works immediately upon implementation. For high-volume carriers with standardized layouts, Sensible can build deterministic templates in under an hour, delivering speed and precision across consistent document sets."* (delivery orders)

**Paragraph 3 (optional) — Additional context:**
Use if the document type needs more background (e.g., explaining what an EOB is, or why closing disclosures matter). Skip for straightforward document types.

---

## What we'll cover

Use this sentence verbatim, adapting bracketed parts:

> "This blog post briefly walks you through configuring extractions for [doc type variant]. By the end, you'll know [a few / a couple of] [SenseML methods / methods for extracting document data using our query language], and you'll be on your way to extracting any data you choose using our documentation or our prebuilt open-source [doc type] configurations[, which currently support [supported variants]]."

- Use "a few" when covering 3+ extraction methods; "a couple of" when covering 2.
- Append the "which currently support" clause when the config library supports multiple named variants.

Examples:
- *"This blog post briefly walks you through configuring extractions for closing disclosures. By the end, you'll know a couple of SenseML methods and you'll be on your way to extracting any data you choose using our documentation or our prebuilt open-source closing disclosure configurations."*
- *"This blog post briefly walks you through configuring extractions for Medicaid EOBs. By the end, you'll know a couple of SenseML methods and you'll be on your way to extracting any data you choose using our documentation or our prebuilt open-source EOB configurations, which currently support Medicaid, Tricare, and Cigna EOBs."*
- *"This blog post briefly walks you through configuring extractions for rent rolls. By the end, you'll know a few methods for extracting document data using our query language, and you'll be on your way to extracting any data you choose using our documentation or our prebuilt open-source configurations."*

---

## Prerequisites

Newer posts (delivery orders, cyber insurance quotes) use a standardized step-by-step prerequisites section instead of an inline sentence. Use this format:

> "To extract from this document, take the following steps: Sign up for a **Sensible account**. After completing onboarding, click the **Document types** tab and click **Create new document type**. In the dialog, upload the example document below. Leave all defaults as-is except ensure "Auto-generate configuration" is disabled, then click **Create**. [Download [doc type variant] sample]. Name the document type `[doc_type_slug]`."

Older posts (bank statements, closing disclosures, EOBs) use an inline sentence instead — see examples below. Either is acceptable, but the step-by-step format is the current standard.

Older Pattern A — direct import link (inline):
> "To follow along, you can sign up for a Sensible account, then download an example PDF [for a [doc type variant]] and upload it to the Sensible app, or import the PDF and prebuilt open-source [doc type] configurations directly to the Sensible app."

Older Pattern B — out-of-the-box extractions (inline, used for resumes, rent rolls):
> - Sign up for a **Sensible account**
> - Add prebuilt extraction support for [doc types] to your Sensible account. To add support, follow the steps in **Out-of-the-box extractions** and select [doc types].

---

## Write document extraction queries with SenseML

**Paragraph 1 — Example document:**

> "Let's walk through extracting specific pieces of data from [a / an] [doc type]. Here's an example of a [doc type] PDF with redacted [or dummy] data:"

Examples:
- *"Let's walk through extracting specific pieces of data from a bank statement. Here's an example of a bank statement PDF with redacted or dummy data:"*
- *"Let's walk through extracting specific pieces of data from a mortgage closing disclosure. Here's an example of a closing disclosure PDF with redacted data:"*
- *"Let's walk through extracting specific pieces of data from an explanation of benefits. Here's an example of an EOB PDF with redacted or dummy data:"*

`[Image: example document screenshot]`

**Paragraph 2 — Scope:**

> "To keep the example in this post simple, let's extract just the:"
> - [field 1]
> - [field 2]
> - [field 3]

---

## [CONDITIONAL] Identify and classify incoming [doc types]

Include this section when the config has a `fingerprint`. Place it as the first extraction section, before the individual field sections.

Opening sentence pattern — adapt the count to match the number of tests:
> "[N] text conditions uniquely identify the [doc type variant] format; all must pass before field extraction runs."

Example (delivery orders, 4 tests):
> *"Four text conditions uniquely identify the OOCL delivery order format; all must pass before field extraction runs."*

Follow the opening sentence with the fingerprint code block (JSON5 with inline comments), then 1–2 sentences explaining what fingerprinting does:
> "Sensible uses these tests to route each incoming document to the correct config automatically. If a document fails any test, Sensible skips this config and tries the next one — useful when a document type has multiple carrier- or vendor-specific layouts."

`[Image: screenshot showing fingerprint tests in Sensible app]`

---

## Extract [field] (repeat 2–4 times)

**Step 1 — Screenshot intro:**

> "See the following screenshot for an overview of how to extract [the] [field]:"

`[Image: screenshot]` _(caption: "Extract [field] (left pane: query. middle pane: document. right pane: output)")_

**Step 2 — Post-screenshot description:**

> "The [query / queries] in the left pane in the preceding image [one sentence describing what the query does — what it finds and how]. The PDF is displayed in the middle pane, and the extracted [data] [is / are] in the right pane."

**Step 3 — Try-it-yourself prompt:**

> "To try this out yourself, paste the following [query / queries] into the left pane of the Sensible app."

**Step 4 — SenseML code block:**

Use ` ```json ` (always `json`, never `json5`). Include the `/* Sensible uses JSON5 to support in-line comments*/` header as the first line of the **first two code blocks only** — omit it from all subsequent blocks. Comments (` /* */ `) explain the "why", not the "what." Show a complete runnable snippet — include a full `{ "fields": [...] }` wrapper. Reader should be able to paste and go.

**Step 5 — Output:**

> "You'll get this output:"

JSON output block. For array fields, show at least two objects if the document has them — individual objects can be abbreviated if long. Truncate remaining items with `/* JSON output abbreviated */`. If the document genuinely has only one repeating item, show it and add a sentence noting the config handles multiple.

**Step 6 (optional) — Explanatory sentence:**
Add 1–2 sentences if the output needs context (e.g., explaining `confidenceSignal`, noting that List with `"llmEngine": "thorough"` takes longer).

---

## [CONDITIONAL] Nested sections: H3 subheadings + flattening

Include this pattern when a `sections` field contains nested sub-sections (sections within sections). The commission statements post uses this for a three-level hierarchy (broker → policy → transaction).

**H3 structure:** Add one H3 per nesting level under the parent H2. Name each H3 after the data entity it represents (e.g., "Broker", "Policy", "Transactions"). Each H3 follows the same pattern as a regular extraction section: describe what the section anchors on, show the SenseML for that level's `sections` field, and explain the stop condition.

**"Flattening the nested sections" H3:** Add this final H3 when the config uses `copy_to_section`, `copy_from_sections`, or `customComputation` with path traversal (`../../`) to collapse nested output into a flat top-level array. Explain what each method does in plain language — e.g.:
- `copy_to_section` — stamps a parent-level value (e.g., policy subtotal) onto each child row
- `copy_from_sections` — consolidates arrays from nested sections into one top-level output
- `customComputation` with `../../_field` — climbs section levels to retrieve an ancestor value

Intermediate nested fields suppressed from final output (prefixed with `_`) should be noted but not shown in the output block.

---

## [OPTIONAL] Transform extracted data [: description]

Include when extracted data needs reshaping (e.g., zipping column arrays into row objects with `zip`, validating values with `customComputation`).

- 1 sentence explaining the default output format and why transformation is useful.
- Optional screenshot.
- Try-it-yourself prompt (same pattern as above).
- Code block showing the computed field(s).
- Output block.

---

## [OPTIONAL] Test the extraction template with a second document

Include when a second example document is available to show config portability.

Steps:
1. Publish config: **Publish configuration > Publish to production**
2. Download the second example document (provide download link).
3. Upload via **Add file** in the Sensible Instruct editor view.
4. Note that the extracted data in the right pane updates to reflect the new document.

Include screenshot showing updated output.

---

## Putting it all together

_New section — not present in older published posts. Include in all new posts._

Show a single combined code block containing all fields demonstrated in the post (plus the fingerprint object if the config has one), followed by the full extraction output for that combined config. This gives readers a complete, copy-pasteable starting point and gives the blog writer an easy way to verify the post end-to-end.

**Intro sentence:**
> "Here's the complete SenseML config combining everything we've covered:"

**Code block:** One `json` block with all fields from the individual sections plus `fingerprint` at the top if present. Include the same inline comments as the individual examples. No `/* Sensible uses JSON5 to support in-line comments*/` header (this block is past the first two). Wrap the code block with extraction markers so the config file can be synced from the draft:

```
<!-- CONFIG:START -->
```json
...
```<!-- CONFIG:END -->
```

**Output block:** Real output from running the combined code block itself — not the original source config, which extracts more fields than are shown in the post. Paste the combined block into the Sensible app (or run it via `curl`) and use that response. For array fields, show at least two objects — individual objects can be abbreviated if long — then truncate remaining items with `/* JSON output abbreviated */`.

**App link:** Print the Sensible app URL to the terminal (from `upload_pr_extractor.py` output) for the writer to verify — do NOT embed it in the draft.

---

## Extract more [doc type] data

> "We've covered how to extract a few pieces of data from [a / an] [doc type]. Our prebuilt config extracts much more information. Check it out! In the following screenshot, every [blue / blue-or-green]-outlined line is a piece of extracted data:"

Examples:
- *"We've covered how to extract a few pieces of data from a closing disclosure. Our prebuilt config extracts much more information. Check it out! In the following screenshot, every blue-outlined line is a piece of extracted data."*
- *"We've covered how to extract a few pieces of data from an explanation of benefits (EOB). Our prebuilt config extracts much more information."*

`[Image: full extraction screenshot]`

---

## [OPTIONAL] When to use a layout-specific config vs. a generalized config

Include when the config is carrier- or vendor-specific and the reader may be wondering whether to build their own vs. use an LLM-based generalized approach.

Pattern:
> "A layout-specific config is the right choice when [a carrier / vendor / issuer] appears regularly in your [pipeline / workflow] and the [document] format is consistent across [submissions / instances]. [Explain the tradeoff: layout-specific = no LLM calls, consistent output, one-time build cost. Generalized LLM = handles any variant, less setup, more variability.] Sensible's fingerprint method routes each incoming document to the right config automatically, based on [carrier / vendor]-identifying text in the document."

Example (cyber insurance quotes):
> *"A layout-specific config is the right choice when a carrier appears regularly in your submission pipeline and the quote format is consistent across submissions. The Beazley config above anchors to Beazley's specific label text… No LLM calls, no prompt maintenance, consistent output on every Beazley document that enters the pipeline. For carriers that appear less frequently or whose format you haven't templated yet, a generalized LLM config handles extraction on day one… Both run through the same API endpoint, and Sensible's fingerprint method routes each document to the right config automatically."*

---

## Connect Sensible to your workflow

Newer posts replace the old "Start extracting" CTA with this integration methods section.

Opening sentence pattern:
> "Once your SenseML config is set up, there are several ways to integrate [doc type] extraction into your application or process."

Then list the integration options (use the current names — verify before publishing):
- **Python SDK** — wraps the extraction API; install with pip
- **MCP server** — connects document extraction to AI coding tools like Claude
- **API (synchronous and asynchronous)** — synchronous returns data inline; asynchronous accepts a webhook, recommended for high-volume workflows
- **Zapier** — no-code integration; routes extracted data into Google Sheets, Airtable, Slack, etc.

---

## FAQ

Newer posts end with a Q&A section. Cover 4–6 questions relevant to the document type. Standard questions that appear across posts:

- What fields can be extracted from a [doc type]? (list the core fields)
- How accurate is automated [doc type] extraction? (deterministic = highly accurate; note confidence signals)
- How does Sensible handle [doc types] from multiple [carriers / vendors / issuers]? (fingerprinting + generalized LLM fallback)
- Can Sensible extract from [doc types] bundled with other documents? (portfolio method)
- How long does it take to set up [doc type] extraction? (reference prebuilt config if available; layout-specific typically under an hour)

---

## Start extracting [from your documents]

_Older posts only. Newer posts use "Connect Sensible to your workflow" + "FAQ" instead._

Most older posts use this version:
> "Stop relying on manual data entry. With Sensible, claim back valuable time, your ops team will thank you, and you can deliver a superior user experience. It's a win-win."

Oldest version (EOB post):
> "Congratulations, you've learned some key methods for extracting structured data from [doc type] documents. There's more extraction power for you to uncover. Sign up for a free account ([X] docs a month, no credit card required), check out our prebuilt [doc type] config in our open-source library, and peruse our docs to start extracting data from your own documents."

**Verify current doc count before publishing** — this has changed across posts (100/month, 150/month).

---

## WRITING STYLE NOTES

**Tone:** Practical, tutorial-style. Direct second person ("you", "let's"). Not salesy.

**Formatting:**
- Bold key Sensible terms and product names on first mention per post: **SenseML**, **Sensible Instruct**, etc.
- Bold UI actions: **Create configuration**, **Switch to SenseML**, **Publish configuration**, **Add file**, **Show full output**.

**Screenshots:**
- Every extraction section gets a screenshot.
- Caption format: `Extract [field name] (left pane: query. middle pane: document. right pane: output)` — omit pane descriptions if the screenshot doesn't show all three panes.

**Code blocks:**
- SenseML is JSON5. Use `/* */` comments to explain non-obvious parameters.
- Show complete, runnable snippets. Readers should be able to paste and go.
- Prefix private/intermediate field IDs with `_` (e.g., `_experience`, `_electronic_withdrawals_table_raw`) when they'll be suppressed in output.

**Output blocks:**
- Truncate long JSON with `/* JSON output abbreviated */` or `[...]`.
- Always show at least one complete object so the reader knows the output shape.

**Links (link on first mention per post):**
- "SenseML" → docs
- "open-source SenseML configurations" / "open-source library" → config library
- "documentation" / "docs" → docs homepage
- "API" → API reference
- "Zapier" → Zapier integration page
- "Out-of-the-box extractions" → relevant docs page

**Document type specificity:** Name the specific variant used (e.g., "Chase bank statements", "Medicaid EOBs"). List other supported variants at the end of "What we'll cover."
