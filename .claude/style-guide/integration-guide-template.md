# Integration Guide Template

Use this template when creating a new Sensible integration guide. Replace all `[PLACEHOLDER]` text. Comments in `<!-- -->` are guidance — remove them from the final file.

**File naming and visibility**: New integration guides are created as drafts. Name the file `draft-[slug].md` (e.g., `draft-make-tutorial.md`) and set `hidden: true` in the frontmatter. Remove the `draft-` prefix and change `hidden` to `false` only when the guide is ready to publish.

The shared style conventions (voice, backtick usage, parameter capitalization, cross-reference syntax) are in `style-guide-overview.md` and `sentence-word-guidance.md`. This file covers structure specific to integration guides.

---

## Template

```markdown
---
title: [Integration Name] tutorial
excerpt: ''
deprecated: false
hidden: true
metadata:
  title: ''
  description: '[short phrase, 4–7 words, lowercase except proper nouns]'
  robots: index
next:
  description: ''
---
<!-- Opening sentence: "This topic describes [doing X] using [integration]."
     State what the reader will accomplish and which systems are involved. 1–2 sentences.
     Example: "This topic describes sending extracted data from example documents into an
     Airtable database using Sensible's Zapier integration." -->
[OPENING SENTENCE.]

<!-- Overview image (OPTIONAL): shows the workflow at a high level.
     Place immediately after the opening sentence when the workflow is visual. -->
<!-- ![Click to enlarge](https://raw.githubusercontent.com/sensible-hq/sensible-docs/v0/assets/images/final/[filename].png) -->

<!-- How it works (OPTIONAL): a short numbered or bulleted list explaining the workflow
     before the steps. Use when the guide has multiple Zaps, phases, or non-obvious sequencing.
     Example from advanced Zapier guide:
     "Sensible supports two-step Zapier workflows as follows:
     * The first Zap extracts the document and returns a `WAITING` extraction status.
     * The second Zap triggers when the extraction status is `COMPLETE` and takes action on the extraction." -->

## Prerequisite: [Configure or set up the first thing]

<!-- Use a separate ## Prerequisite: heading for each prerequisite system or task.
     Label with an action phrase: "Configure 1040 extractions in Sensible",
     "Configure accounts", "Create an empty destination database".
     Numbered steps if there's more than one action; prose if just one. -->

1. [First prerequisite step]
2. [Second prerequisite step]

## Prerequisite: [Configure or set up the second thing]

1. [Step]

## [Main section: named for the platform or phase, e.g. "Zap 1: Extract new file in Slack with Sensible"]

<!-- Use ## headings for each major phase or platform. Name them descriptively.
     Introduce each section with "Take the following steps to [do X]:" or
     "See the following steps to configure [Y]:" followed by the numbered list. -->

Take the following steps to [accomplish X]:

1. [First high-level step.]

2. For the [trigger/action/setup], take the following steps:

   1. Setup:
      1. **[UI field label]**: [value or instruction]
      2. **[UI field label]**: [value or instruction]
   2. Configure:
      1. **[UI field label]**: [value or instruction]
      2. **[UI field label]**: [value or instruction]
   3. Test:
      1. [What to do to test this step]
      2. [What to verify]

<!-- UI field labels are always bold: **App**, **Trigger event**, **Account**, **Document type**.
     Values are plain text unless they're exact option names, which can be bold or backtick.
     Images go after a step group to show the configured state: -->
<!-- ![Click to enlarge](https://raw.githubusercontent.com/sensible-hq/sensible-docs/v0/assets/images/final/[filename].png) -->

## [Second main section, e.g. "Zap 2: Upload extraction as spreadsheet to Google Drive"]

Take the following steps to configure [Zap 2 / phase 2 / etc.]:

1. [Step]

## (Optional) Test your integration

<!-- Standard closing section for end-to-end validation. Use this exact heading.
     Congratulatory opener is conventional: "Congratulations, your integration is now
     published and running!" followed by steps to verify it works with real data. -->

Congratulations, your integration is now published and running! Take the following steps to [verify / continue testing]:

1. [Download example documents / trigger a test event / etc.]
2. [Verify the output in the destination system]

# Notes

<!-- Notes is H1, matching SenseML reference pages.
     Use bold inline sub-headers for each topic (not H2/H3).
     Cover limitations, gotchas, and platform-specific constraints. -->

**[Limitations or topic name]**

* [Limitation or note]
* [Limitation or note]

**[Second topic]**

* [Note]
```

---

## Section-by-section guidance

### Opening sentence

- Pattern: "This topic describes [doing X] using [integration]."
- One or two sentences max. State the destination system and the integration platform.
- Don't start with "In this guide" or "This guide will show you."

### Prerequisites

- Two valid patterns for prerequisite headings:
  - `## Prerequisite: [action phrase]` — used in multi-system guides (e.g. advanced Zapier). One heading per system or major setup task.
  - Descriptive action heading without "Prerequisite:" prefix (e.g. `## Create an example Sensible extraction`, `## Create an empty destination database`) — used in simpler single-flow guides.
- The action phrase is imperative and specific: "Configure 1040 extractions in Sensible", not "Sensible setup".
- When a prerequisite requires only a single step (e.g., "Clone this document type"), prose is acceptable. For multi-step setup, use a numbered list.

### Main steps

- Organize by platform or phase (Zap 1 / Zap 2, Configure Sensible / Configure Salesforce / Configure Zapier).
- Each section opens with "Take the following steps to [X]:" or "See the following steps to configure [Y]:".
- A prose sentence can precede the opener when context is needed: "Before you can integrate Sensible with [Platform], you need to [reason]. Take the following steps:"
- **Multi-system guides** (multiple platforms or Zaps to configure): Use the nested Setup → Configure → Test sub-structure, each as a plain inline label (`1. Setup:`) followed by bold UI field/value pairs.
- **Single-flow guides** (one platform, one Zap): Use a flat numbered list with nested sub-steps inline. No Setup/Configure/Test sub-sections.
- UI field names are always bold: `**Document type**`, `**Environment**`, `**Account**`.

### Images

- Place after a configuration block to show the resulting state, not before.
- Always use `![Click to enlarge](https://raw.githubusercontent.com/sensible-hq/sensible-docs/v0/assets/images/final/[filename].png)`.
- No caption text beyond the alt text.

### Optional test section

- Heading is always `## (Optional) Test your integration`.
- Opens with "Congratulations, your integration is now published and running!"
- Numbered steps for downloading examples, triggering the workflow, and verifying output.
- After the test section, simple guides can include a second optional section `## (Optional) Scale up` describing how to extend the workflow to handle more complex or automated scenarios. This section is brief (2–4 sentences or a short list) and ends with a cross-reference to the advanced guide.

### Notes

- `# Notes` — H1, same as SenseML reference pages. (Some existing pages incorrectly use `## Notes`; use H1 for new guides.)
- Bold inline sub-headers for each topic (not `##` or `###`).
- Bullet list of limitations under each sub-header.
- Common topics: general limitations on what the integration supports (single-value vs. multi-value output, single-document vs. portfolio), platform-specific quirks (timing, file age restrictions).

---

## Variation: single-phase integration (no multi-Zap structure)

When the integration is a single workflow (one Zap, one API call, one connection), flatten the structure:

- Omit the "Zap 1 / Zap 2" headings
- Use a single `## Configure [Platform]` section for the main steps
- Still use the Prerequisite → Configure → (Optional) Test → Notes order