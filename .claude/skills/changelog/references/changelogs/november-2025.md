---
title: November 2025
slug: november-2025
date: 2025-11-04
---

In the last month, Sensible updated an Anthropic model version for LLM-based methods, released UX improvements for authoring SenseML, and switched our default OCR provider for scans and images from Microsoft to Amazon.

## UX improvements: easier SenseML editing with auto-complete and insert values

You can now author SenseML faster in the Sensible app by using new autocomplete suggestions. When you type "template" in the `fields` array, Sensible suggests syntax for several field types, including JsonLogic, sections, and query groups. For example, if you select `template_section`:

<Image border={false} alt="Click to enlarge" src="https://raw.githubusercontent.com/sensible-hq/sensible-docs/v0/assets/images/final/changelog_nov2025_edit_1.png" />

Sensible creates a sections field with optional parameters commented out:

<Image alt="Click to enlarge" border={false} src="https://raw.githubusercontent.com/sensible-hq/sensible-docs/v0/assets/images/final/changelog_nov2025_edit_2.png" />

You can also now insert strings from a PDF into a SenseML query.  Click the SenseML where you want to insert a line from the document, then press **Ctrl** and click a line you want to insert. The following image shows inserting the line "Policy Name" from a document into SenseML:

<Image alt="Click to enlarge" border={false} src="https://raw.githubusercontent.com/sensible-hq/sensible-docs/v0/assets/images/final/changelist_nov2025_insert_1.png" />

<Image alt="Click to enlarge" border={false} src="https://raw.githubusercontent.com/sensible-hq/sensible-docs/v0/assets/images/final/changelist_nov2025_insert_2.png" />

## New feature: Linearize preprocessor

The new Linearize preprocessor is an advanced alternative to the [Multicolumn](doc:multicolumn) preprocessor.  This preprocessor allows you to organize a page into rectangular, coordinate-based blocks before Sensible sorts lines. For example, use this preprocessor when Sensible can't otherwise recognize columns. For more information, see the [Linearize](doc:linearize) preprocessor.

<Image alt="Click to enlarge" border={false} src="https://raw.githubusercontent.com/sensible-hq/sensible-docs/v0/assets/images/final/linearize_1.png" />

## Improvement: LLM model version updates

Where applicable, the Query Group and List methods have been updated to Claude 3.7 Sonnet from Claude 3.5 Sonnet. For more information, see [LLM Models](doc:llm-models). We've also made back-end improvements to the Query Group method's accuracy and reliability.

## Improvement: New OCR default

When you create a new document type, its OCR Engine parameter now defaults to Amazon instead of Microsoft for documents that require OCR on all pages, such as scans and images. Existing document types aren't affected by this change.
