---
title: March 2024
slug: march-2024
date: 2024-02-06
---

In the last month, we released support for extracting data from Excel files and added Google sign-in support to the Sensible app. To teach users how to author LLM-powered queries, we added example extractions to the app. We deprecated the Query method and replaced it with the Query Group method to improve LLM performance, deprecated the Table method and replaced it with the NLP Table method, and made several minor improvements.

## New feature: Extract data from Excel files

Sensible now supports extracting data from Excel files. To extract data, Sensible converts Excel files to PDFs. To style a PDF, Sensible discards truncated text in cells, converts sheets to same-width pages, and adds the sheet name as header on each page. For more information, see [Supported file types](doc:file-types).

## New feature: Sign into the Sensible app with your Google account

We've added a new option for account creation and sign-in. You can now sign up for the Sensible app using your Google account, instead of creating a Sensible-specific account.

## UX improvement: LLM-based examples for common documents

In the Sensible app, you can now view LLM prompt examples for common documents from the Sensible configuration library. Learn best practices from the examples so you can author your own  LLM-powered Query Group, List, and NLP Table methods.

To access the examples, click your account icon, then click **Try sample documents** in the dropdown:

<Image alt="Click to enlarge" border={false} src="https://raw.githubusercontent.com/sensible-hq/sensible-docs/v0/assets/images/final/changelog_march2024.png" />

Select an example document type and click **Get started**:

<Image alt="Click to enlarge" border={false} src="https://raw.githubusercontent.com/sensible-hq/sensible-docs/v0/assets/images/final/changelog_march2024_2.png" />

View the extracted data:

<Image alt="Click to enlarge" border={false} src="https://raw.githubusercontent.com/sensible-hq/sensible-docs/v0/assets/images/final/changelog_march2024_3.png" />

Explore the examples, or upload a document to author your own LLM-powered queries.

## New feature: Query Group replaces Query method

To improve accuracy and speed, you can now bundle together multiple LLM queries using the new Query Group method. Group queries together when their answers are co-located in a document, for example, in the same paragraph. This method deprecates the [Query](doc:deprecated-query)  method. For more information, see the [Query Group](doc:query-group) method's reference topic and [Query Group](doc:query-group-tips)   extraction tips.

## Improvement: Omit sections if fields are null

You can now skip outputting sections that are missing fields using the new Required Fields parameter. For example, omit a claim in a loss run if the telephone number field is null. You can specify an array of required fields using the following syntax:

```json
"requiredFields": ["phone_number", "claim_date"]
```

For more information, see [Sections](doc:sections#parameters).

## Improvement: Consistency between Intersection and Region method

The Intersection method extracts lines that either overlap a point, or that are contained in a rectangular region. Now, Sensible defines "contained" using the same criteria as for the [Region](doc:region) method.

## New feature: Get File Metadata method

With the new Get File Metadata method, you can copy the document's filename to the extraction's `parsed_document` output. For more information, see the [Get file metadata](doc:get-file-metadata) method.

## Deprecation: NLP Table method replaces Table method

The [Table](doc:deprecated-table) method is deprecated. To duplicate this method's function, use the NLP Table method and set the Rewrite Table parameter to false.

## Improvement: Better table title detection for Fixed Table method

Sensible now uses an OCR provider to detect and return table titles and table footers in the output for the [Fixed Table](doc:fixed-table) method.

## Improvement: Recognize and map any text as currency symbols

You can now recognize any text as a currency symbol using new syntax for the Currency type's Currency Symbol parameter. You can map the text to the symbol of your choice in the extracted document output.

For example, the following lookup table recognizes currency codes and symbols for dollars and euros, and outputs symbols to the Unit parameter:

```json
"currencySymbol": {  
"$": "$"  
"€": "€"  
"USD": "$",  
"EUR": "€",  
"default": "€"}
```

For more information, see [Types](doc:types#currency).
