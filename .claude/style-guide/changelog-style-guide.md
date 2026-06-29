# Sensible Changelog Style Guide

Derived from analysis of published changelogs (2024–2026). Use this to calibrate tone, structure, and voice when writing a monthly product changelog.

---

## Voice and tone

- **Intro paragraph**: Third person — "Sensible released", "Sensible added", "Sensible improved". Not "we released".
- **Section bodies**: Second person — "you can now", "use this to", "for example, you can configure".
- **Factual, present tense**: Describe what the feature does, not what was built. "You can now extract…" not "We built extraction for…"
- **No marketing fluff**: No "excited to announce", no "powerful new", no "seamlessly". Just what it does and why it's useful.

---

## Structure

### Title
`Month YYYY` (e.g., `March 2026`)

### Intro paragraph (no heading)
One paragraph, pattern: `"In the last month, Sensible [summary of 2–4 highlights]."`

- No doc links
- Mentions the most significant changes
- Neutral and factual

**Examples:**
> In the last month, Sensible added deterministic methods for removing unwanted text from documents and for matching rotated text, such as watermarks. We also added advanced transformation logic for large spreadsheet extractions.

> In the last month, Sensible released several major new features. We introduced email-driven document extraction for automated processing of email attachments, significantly expanded our auto-generated extraction schemas to handle larger and more complex documents, and added new troubleshooting capabilities for multimodal extractions.

### Sections
One section per feature (or group closely related items):

```
## [Type]: [Short descriptive title]

Body text.
```

**Ordering**: Lead with the most significant features. Group by theme if it helps readability.

---

## Section heading types

Use exactly these strings (casing matters):

| Type | When to use |
|------|-------------|
| `New feature:` | Net-new functionality that didn't exist before |
| `Improvement:` | New config option or enhancement to existing feature |
| `UX improvement:` | Single UI/UX change in the Sensible app |
| `UX improvements:` | Multiple UI/UX changes grouped in one section |
| `Deprecation:` | Something being deprecated or removed |

**Do not use** `Update:` — phased out as of 2025.

---

## Section body

- 2–5 sentences, prose style
- Use bullets only when listing multiple parallel sub-items
- First sentence: what was added or changed
- Subsequent sentences: usage context, an example, or what problem it solves

**Short improvement:**
> With the new [Remove Lines](doc:remove-lines) preprocessor, you can now remove matched text from all pages in a document. For example, use this preprocessor to remove watermarks or page numbers. This preprocessor is an alternative to the Remove Header and Remove Footer preprocessors and can remove text that varies in position on the page.

**Improvement with inline code:**
> When you want to match the nth occurrence of a string or regular expression, the new Repeat match object is a more concise alternative to a [match array](doc:match-arrays). For example, to find the fifth occurrence of "customer account", you can specify:
> ```json
> "match": [{ "type": "repeat", "times": 5, "match": { "type": "startsWith", "text": "customer account" } }]
> ```

**Feature with bulleted sub-items:**
> Sensible added support for automated extraction from email documents. Key features include:
> * LLM-based attachment classification against specified document types
> * Support for multiple attachments per email
> * Optional email body extraction
> * Webhook delivery of extraction results with metadata and download links

---

## Doc links

Use readme short-link format — not full URLs. The prefix depends on which directory the file lives in, and the slug is the filename minus `.md`:

- Pages in `docs/` → `[link text](doc:slug)`
- Pages in `reference/` → `[link text](reference:slug)`

Examples:
- `docs/Senseml reference/preprocessors/remove-lines.md` → `[Remove Lines](doc:remove-lines)`
- `docs/Senseml reference/methods/query-group.md` → `[Query Group](doc:query-group)`
- `reference/Extraction/document-1/extract-data-from-a-document.md` → `[Extract document](reference:extract-data-from-a-document)`
- `reference/Classification/document/classify-document.md` → `[Classify document](reference:classify-document)`

For `#` anchors, append them: `(doc:match#global-parameters)`

---

## Images

Always use JSX `<Image>` (not markdown `![alt](url)`):

```jsx
<Image alt="Click to enlarge" border={false} src="URL" />
```

Only include images if URLs are explicitly provided. No trailing `<br />` unless it immediately precedes an image.

---

## Length calibration

| Feature type | Typical length |
|---|---|
| Simple config param | 2–3 sentences |
| New method or preprocessor | 3–5 sentences, possibly with code example |
| Major UX feature | Longer, multiple images and sub-bullets OK |
| Deprecation | 1–2 sentences, link to replacement |

A typical changelog has 3–6 sections.
