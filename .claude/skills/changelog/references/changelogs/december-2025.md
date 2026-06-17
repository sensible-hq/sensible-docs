---
title: December 2025
slug: december-2025
date: 2025-11-11
---

In the last month, Sensible released support for Gemini for LLM-based extraction methods and made improvements to the web app.

## New feature: Support for Gemini for LLM-based methods

You can now use Gemini to extract data from documents in addition to Claude and GPT. To use this provider, configure `google` as the provider in the LLM Engine parameter for [LLM-based](doc:llm-based-methods)  methods. Note that Gemini is not yet appropriate for customers who require HIPPA or zero data retention support.

## New feature: Advanced JsonLogic operations

In addition to the existing JsonLogic operators, Sensible released new extended JsonLogic operations for transforming the output schema:

* The Join operator takes two input arrays, joins them by a common key, performs specified operations on them, and outputs a new array.

* The Slice operation selects elements in an array from a starting index up to but not including an ending index.

For more information, see [Join](doc:jsonlogic#join) and [Slice](doc:jsonlogic#slice).

## UX improvement: Batch upload sample documents

For easier config authoring, you can now select multiple sample documents to upload in a batch. This feature is available in existing document types.

<Image alt="Click to enlarge" border={false} src="https://raw.githubusercontent.com/sensible-hq/sensible-docs/v0/assets/images/final/changelog_dec_2025_upload.png" />

## UX improvements: Download CSV extraction

In the **Extraction history** tab, you can now download an extraction as a CSV file in addition to downloading it as an Excel or JSON file.

<Image alt="Click to enlarge" border={false} src="https://raw.githubusercontent.com/sensible-hq/sensible-docs/v0/assets/images/final/changelog_dec_2025_csv_download.png" />

<br />
