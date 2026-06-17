---
title: January 2026
slug: january-2026
date: 2026-01-07
---

In the last month, Sensible updated Anthropic model versions for LLM-based methods, released multi-language support for date types, and introduced advanced configuration options for table data transformation.

## Improvement: LLM model version updates

Where applicable, Sensible updated the Query Group and List methods to Claude 4.5 Sonnet from Claude 3.7 Sonnet, and to Claude Haiku 4.5 from Claude Haiku 3.5. For more information, see [LLM models](doc:llm-models).

## Improvement:  Multi-language date type support

With the new Language parameter for the [Date](doc:types#date)  type, Sensible now recognizes Spanish and Italian dates.  For example, Sensible recognizes `21 marzo 2021` and `7 de enero de 2018`.

## Improvement: Advanced transformation of extracted tables

When you transform extracted table data, you can now use conditional logic for field execution and output multiple fields using custom JsonLogic. In detail,  the [Add Computed Fields](doc:add-computed-fields) method now supports the [Conditional](doc:conditional)  method and the [Custom Computation Group Field](doc:custom-computation-group)  method.

## Improvement: Advanced checkbox recognition configuration

With the [Nearest Checkbox](doc:nearest-checkbox)  method's new Max Y Distance parameter,  you can now specify the maximum number of inches Sensible searches up or down the page for a checkbox from a starting point.  For example, configure this parameter to restrict the checkbox search in successive rows of tightly spaced checkboxes.
