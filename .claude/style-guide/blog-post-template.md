# Template: How to extract data from [DOCUMENT TYPE] with [LLMs and] Sensible

---

## TITLE

`How to extract data from [document type (plural)] with [LLMs and] Sensible`

Include "with LLMs and Sensible" only for variable-layout documents (resumes, rent rolls). For structured/semi-structured documents, use "with Sensible."

---

## INTRO (2–3 paragraphs, no heading)

**Paragraph 1 — Industry context and pain point:**
Describe what the document is, what industry uses it, and what downstream workflows depend on the data. Give 2–3 concrete examples of what companies build with this data (e.g., analytics, automation, risk assessment). Establish that the data is hard to get because it only exists as PDFs.

Pattern:
> "If you're building software in [industry], chances are you've come across the [document type]. [Document type] [describes what it contains]. [Companies in this space] need this data to [build X, Y, Z]. However, they often lack access to [document type] in any format other than PDFs, which makes data extraction a potentially difficult problem."

**Paragraph 2 — Introduce Sensible:**
Introduce Sensible and SenseML. Mention the open-source config library. List the access methods (API, SDK, app, Zapier).

Boilerplate to adapt:
> "Enter Sensible. With Sensible you can easily extract key information out of [document type] PDFs using [**SenseML**](link), Sensible's query language for extracting data from documents. We've written a library of [**open-source SenseML configurations**](link), so you don't need to write queries from scratch for common documents. From there, your [document] data is accessible via [API](link), Sensible's UI, or 5,000 other software integrations thanks to [Zapier](link)."

**Paragraph 3 (optional) — Additional context:**
Use if the document type needs more background (e.g., explaining what an EOB is, or why closing disclosures matter for the mortgage market).

---

## ## What we'll cover

1–2 sentences. Name the document type variant being used (e.g., "Chase bank statements", "Medicaid EOBs"). State what SenseML methods will be demonstrated and that readers will be able to extract whatever they want using the docs or prebuilt configs.

Pattern:
> "This blog post briefly walks you through configuring extractions for **[document type]**. By the end, you'll know [a few / a couple of] methods for extracting document data using our query language, and you'll be on your way to extracting any data you choose using our **documentation** or our prebuilt open-source **configurations**[, which currently support X, Y, and Z]."

---

## ## Write document extraction queries with SenseML

**Paragraph 1 — Example document:**
One sentence introducing the example PDF.

Pattern:
> "Let's walk through extracting specific pieces of data from a [document type]. Here's an example of a [document type] PDF with redacted [or dummy] data:"

`[Image: example document screenshot]`

**Paragraph 2 — Prerequisites:**
Sign-up steps as a bullet list.

Pattern A (when importing directly to the app is available):
> "To follow along, you can sign up for a Sensible account, then **download an example PDF** and upload it to the Sensible app, or import the PDF and prebuilt open-source configurations directly to the **Sensible app**."

Pattern B (when linking to out-of-the-box extractions):
> - Sign up for a **Sensible account**
> - Add prebuilt extraction support for [document type] to your Sensible account. To add support, follow the steps in **Out-of-the-box extractions** and select [document type].

**Paragraph 3 — Scope:**
Note that the prebuilt config is comprehensive but this post keeps it simple. List what will be extracted as a bullet list (2–4 items).

Pattern:
> "Our **configurations for [document type]** are comprehensive. To keep the example in this post simple, let's [just] extract [the]:"
> - [Field 1]
> - [Field 2]
> - [Field 3]

---

## ## Extract [field or feature name]

Repeat this section 2–4 times, one per field or extraction technique demonstrated.

**Step 1 — Screenshot + overview sentence:**

Pattern:
> "See the following screenshot for an overview of how to extract [the field]:"
>
> `[Image: screenshot]` _(caption: "Extract [field name] (left pane: query. middle pane: document. right pane: output)")_
>
> "The [query/queries] in the left pane in the preceding image [one sentence describing what the query does — what it finds and how]. The PDF is displayed in the middle pane, and the extracted [data] [is/are] in the right pane."

**Step 2 — Try-it-yourself prompt:**

Pattern:
> "To try this out yourself, paste the following [query / queries / field], or "field[s]" into the left pane of the Sensible app [in the `fields` array]:"

**Step 3 — SenseML code block:**

JSON5 (supports `/* comments */`). Comments explain the "why", not the "what." Show a complete runnable snippet — reader should be able to paste and go. Include a full `{ "fields": [...] }` wrapper unless demonstrating an incremental addition to a config already established earlier in the post.

**Step 4 — Output:**

Pattern:
> "You'll get this output:" or "You'll get back the following output:"

JSON output block. Truncate long outputs with `/* JSON output abbreviated */` or `[...]`. Always show at least one complete object so the reader knows the shape.

**Step 5 (optional) — Explanatory sentence:**
If the output needs context (e.g., explaining `confidenceSignal`, noting that the List method can take several minutes with `"llmEngine": "thorough"`, or pointing to where to see full output in the UI), add 1–2 sentences after the output block.

---

## [OPTIONAL] ## Transform extracted data [: description]

Include when extracted data needs reshaping — e.g., zipping column arrays into row objects using `computed_fields` with the `zip` method, or validating values with `customComputation`.

- 1 sentence explaining the default output format and why transformation is useful.
- Optional screenshot.
- Try-it-yourself prompt.
- Code block showing the computed field(s).
- Output block.

---

## [OPTIONAL] ## Test the extraction template with a second document

Include when a second example document is available to show config portability.

Steps:
1. Publish config: **Publish configuration > Publish to production**
2. Download the second example document (provide download link).
3. Upload via **Add file** in the Sensible Instruct editor view.
4. Note that the extracted data in the right pane updates to reflect the new document.

Include screenshot showing updated output.

---

## ## Extract more [document type] data

Point readers to the prebuilt config for more comprehensive extraction. Include a screenshot showing full extraction coverage (all blue/green-outlined lines = extracted fields).

Pattern:
> "We've covered how to extract a few pieces of data from [document type]. Our prebuilt config extracts much more information. Check it out! In the following screenshot, every blue[-or green]-outlined line is a piece of extracted data:"
>
> `[Image: full extraction screenshot]`

---

## ## Start extracting [from your documents]

CTA closing section. Congratulate the reader. Mention the free account tier — **verify current doc count before publishing** (has changed across posts: 100/month, 150/month). Link to account signup, open-source library, and docs.

Pattern:
> "Congratulations, you've learned some key methods for extracting structured data from [document type] documents. There's more extraction power for you to uncover. **Sign up for a free account** **(X docs a month, no credit card required),** check out our prebuilt **[document type] config in our open-source library**, and peruse our **docs** to start extracting data from your own documents."

---

## WRITING STYLE NOTES

**Tone:** Practical, tutorial-style. Direct second person ("you", "let's"). Not salesy.

**Formatting:**
- Bold key Sensible terms and product names on first mention per post: **SenseML**, **Sensible Instruct**, **Switch to SenseML**, etc.
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
