---
title: September 2024
slug: september-2024
date: 2024-08-29
---

In the last, month we made both an improvement and a breaking change to our support for extracting from Excel documents. We also updated our large language model (LLM) support for the List method and Query Group method in response to end-of-life GPT versions.

## Improvement: Standardization for Excel extractions

To improve efficiency and consistency, Sensible introduced breaking changes to our support for extracting from XLSX documents. 

Now, Sensible standardizes the size and formatting of the text and cell grid in the spreadsheet, then extracts the text directly. Sensible no longer converts the Excel document to a PDF to perform the extraction. Methods that are less commonly used for spreadsheets (pixel- and OCR-based methods) are no longer supported. If you currently extract data from Excel sheets, check your configs for regressions. For more information, see [File types](doc:file-types). 

## Improvement: update from GPT-3.5 Turbo to GPT-4o mini

Sensible updated its default large language model (LLM) engine for the Query Group method and List method from an end-of-life version (GPT-3.5 Turbo) to GPT-4o mini. As part of this change, query groups that contain a single field no longer route to the deprecated Query method, which was formerly a strategy for maintaining backward compatibility with this deprecated method. Also, any existing Query methods in your configs now route to the Query Group method. Test your existing configs for changed output if they use the Query Group method, Query method, or List method.

## New feature: SSO sign-in support

Sensible now offers single sign-on (SSO) implementation for logging into your Sensible account using your company's account. Contact Sensible if you're interested in this feature.

![Click to enlarge](https://raw.githubusercontent.com/sensible-hq/sensible-docs/v0/assets/images/final/changelog_sept2024_sso.png)
