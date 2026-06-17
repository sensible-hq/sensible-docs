---
title: January 2022
slug: january-2022
date: 2022-01-03
---

In the last month we released a new document generation API that lets you fill PDF forms, and made several feature improvements.

## New feature: Document Generation API

Sensible is now more than a PDF data extraction tool. With our new document generation API, you can generate PDFs too. To get set up, just email us a template PDF document and a mapping between the IDs for the fillable fields in the PDF and your JSON data. Then, you can fill PDFs and multi-document PDF portfolios with data you send through our new API. 

For more information, contact Sensible.

## Improvement: Split computed method returns arrays

You can use the new Index parameter on the [Split](doc:split) method to split the output of a field, then return all the substrings or a specified substring. 

## Improvement: Preprocessor now splits lines on a delimiter character

When preprocessing your document, you can now [split lines](doc:split-lines) using the new Separator parameter to specify a delimiting character other than the default whitespace.

## Improvement: Define sections with hard-to-find starts

Sometimes [sections](doc:sections) lack an easy-to-find first line. For example, the first line repeats within the section itself. In this case, you can use the new Require Stop parameter so that rather than restarting each section on each matching first line, you restart sections only after matching the Stop parameter.

## Improvement:  Fail individual fields, not entire extractions

Sensible now isolates and reports more granular errors. Instead of failing an entire extraction, the API returns errors for fields and computed fields. 

## Improvement: Date type recognizes "nth" syntax

The [date](doc:types#date) type now recognizes dates formatted with ordinal numbers (digit followed by st/nd/rd/th), for example, "June 9th, 2022."
