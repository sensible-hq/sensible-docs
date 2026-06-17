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

All posts end paragraph 1 (or lead into paragraph 2) with this near-verbatim line:
> "However, they often lack access to [doc types] in any format other than PDFs, which makes data extraction a potentially difficult problem."

Closing disclosures uses a different version spread across two sentences:
> "The information found in a [doc type] isn't always easily accessible. [Doc type] data isn't usually available through an API."

**Paragraph 2 — Introduce Sensible:**

This paragraph is highly consistent. Use this verbatim, adapting bracketed parts:

> "[Fortunately, ]With Sensible you can easily extract key information out of [doc type] PDFs using SenseML, Sensible's query language for extracting data from documents. We've written a library of open-source SenseML configurations, so you don't need to write queries from scratch for common documents. From there, your [doc type] data is accessible via API, Sensible's UI, or 5,000 other software integrations thanks to Zapier."

"Fortunately, " prefix used in closing disclosures only.

Examples:
- *"Fortunately, with Sensible you can easily extract key information out of closing disclosure PDFs using SenseML, Sensible's query language for extracting data from documents. We've written a library of open-source SenseML configurations, so you don't need to write queries from scratch for common documents. From there, your closing disclosure data is accessible via API, Sensible's UI, or 5,000 other software integrations thanks to Zapier."* (closing disclosures)
- *"With Sensible you can easily extract key information out of EOB PDFs using SenseML, Sensible's query language for extracting data from documents. We've written a library of open-source SenseML configurations, so you don't need to write queries from scratch for common documents. From there, your EOB data is accessible via API, Sensible's UI, or 5,000 other software integrations thanks to Zapier."* (EOBs)

For LLM-based posts (resumes, rent rolls), add this sentence after the SenseML intro sentence:
> "SenseML uses a combination of layout-based rules and LLM prompts to extract from the full spectrum of free-form to structured documents."

Example (rent rolls):
- *"Enter Sensible, which offers intelligent document automation. With Sensible you can easily extract key information out of documents using SenseML, Sensible's query language. SenseML uses a combination of layout-based rules and LLM prompts to extract from the full spectrum of free-form to structured documents. We've written a library of open-source SenseML configurations, so you don't need to write queries from scratch for common documents. From there, the document data is accessible via Sensible's API, SDK, app, or 5,000 other software integrations thanks to Zapier."*

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

## Write document extraction queries with SenseML

**Paragraph 1 — Example document:**

> "Let's walk through extracting specific pieces of data from [a / an] [doc type]. Here's an example of a [doc type] PDF with redacted [or dummy] data:"

Examples:
- *"Let's walk through extracting specific pieces of data from a bank statement. Here's an example of a bank statement PDF with redacted or dummy data:"*
- *"Let's walk through extracting specific pieces of data from a mortgage closing disclosure. Here's an example of a closing disclosure PDF with redacted data:"*
- *"Let's walk through extracting specific pieces of data from an explanation of benefits. Here's an example of an EOB PDF with redacted or dummy data:"*

`[Image: example document screenshot]`

**Paragraph 2 — Prerequisites:**

Pattern A — direct import link available:
> "To follow along, you can sign up for a Sensible account, then download an example PDF [for a [doc type variant]] and upload it to the Sensible app, or import the PDF and prebuilt open-source [doc type] configurations directly to the Sensible app."

Pattern B — link to out-of-the-box extractions (used for resumes, rent rolls):
> - Sign up for a **Sensible account**
> - Add prebuilt extraction support for [doc types] to your Sensible account. To add support, follow the steps in **Out-of-the-box extractions** and select [doc types].

**Paragraph 3 — Scope:**

> "To keep the example in this post simple, let's extract just the:"
> - [field 1]
> - [field 2]
> - [field 3]

---

## Extract [field] (repeat 2–4 times)

**Step 1 — Screenshot intro:**

> "See the following screenshot for an overview of how to extract [the] [field]:"

`[Image: screenshot]` _(caption: "Extract [field] (left pane: query. middle pane: document. right pane: output)")_

**Step 2 — Post-screenshot description:**

> "The [query / queries] in the left pane in the preceding image [one sentence describing what the query does — what it finds and how]. The PDF is displayed in the middle pane, and the extracted [data] [is / are] in the right pane."

**Step 3 — Try-it-yourself prompt:**

> "To try this out yourself, paste the following [query / queries], or "[field / fields]" into the left pane of the Sensible app."

**Step 4 — SenseML code block:**

JSON5 (supports `/* comments */`). Comments explain the "why", not the "what." Show a complete runnable snippet — include a full `{ "fields": [...] }` wrapper. Reader should be able to paste and go.

**Step 5 — Output:**

> "You'll get this output:"

JSON output block. Truncate long outputs with `/* JSON output abbreviated */` or `[...]`. Always show at least one complete object so the reader knows the output shape.

**Step 6 (optional) — Explanatory sentence:**
Add 1–2 sentences if the output needs context (e.g., explaining `confidenceSignal`, noting that List with `"llmEngine": "thorough"` takes longer).

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

## Extract more [doc type] data

> "We've covered how to extract a few pieces of data from [a / an] [doc type]. Our prebuilt config extracts much more information. Check it out! In the following screenshot, every [blue / blue-or-green]-outlined line is a piece of extracted data:"

Examples:
- *"We've covered how to extract a few pieces of data from a closing disclosure. Our prebuilt config extracts much more information. Check it out! In the following screenshot, every blue-outlined line is a piece of extracted data."*
- *"We've covered how to extract a few pieces of data from an explanation of benefits (EOB). Our prebuilt config extracts much more information."*

`[Image: full extraction screenshot]`

---

## Start extracting [from your documents]

Most posts use this version:
> "Stop relying on manual data entry. With Sensible, claim back valuable time, your ops team will thank you, and you can deliver a superior user experience. It's a win-win."

Older version (EOB post):
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
