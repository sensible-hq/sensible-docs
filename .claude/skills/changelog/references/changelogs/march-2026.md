---
title: March 2026
slug: march-2026
date: 2026-03-16
---

In the last month, Sensible added support for extracting data from multi-document email attachments ("portfolios") and for testing email extractions in a development environment. We also updated Anthropic LLM model versions and made minor UX improvements.

## Improvement: Portfolio attachments for email extraction

Sensible now supports data extraction for  [portfolio](doc:portfolio) email attachments, or attachments that contain multiple documents combined in a single file. When you specify portfolio mode for your email processor, Sensible automatically segments each document in a multi-document file attachment by page range, and classifies each one against the document types you configure for the processor. For more information, see [Getting started with email extraction](doc:getting-started-email).

## Improvement: Environment targeting for email extraction

You can now direct email extractions to a specific [environment](doc:environments) by prepending the environment name to your email processor address. For example, to use your development environment's document type configs and webhook, forward emails to `dev.processor_name.account@app.sensible.so`. If you omit the environment prefix, Sensible defaults to the production environment. For more information about configuring your email processor for environments, contact Sensible.

## Improvement: LLM model version updates

Where applicable, Sensible updated the Query Group and NLP Table methods to Claude Haiku 4.5 from Claude 3 Haiku. For more information, see [LLM models](doc:llm-models).

## Improvement: Filter portfolio extractions by configuration

In the **Extractions history** tab, you can now filter portfolio extractions by configuration names:

![Click to enlarge](https://raw.githubusercontent.com/sensible-hq/sensible-docs/v0/assets/images/final/changelog_march2026_ui.png)

Previously, this filter returned results only for single-document extractions. You can use the same filtering option in the [List extractions](ref:list-extractions) endpoint by passing a comma-delimited list of configuration UUIDs to the `configuration_id` parameter.
