---
title: October 2025
slug: october-2025
date: 2025-10-02
---

In the last month, Sensible released advanced configuration options for layout-based extraction methods and added support for extracting from XLSM files.

## Improvement: Preprocessor now splits lines on matched pages

When preprocessing your document, you can now [split lines](doc:split-lines)  on matching pages using the new Match parameter. For example, use this parameter to target typewritten pages in a document that otherwise contains pages with digital fonts.

## Improvement: Advanced configurability for Box method

For the [Box](doc:box)  method, you can now relax the criteria by which Sensible determines that a box  "contains" lines. For example, use the new Percent Overlap X and Percent Overlap Y parameters to extract poorly aligned box contents:

<Image border={false} alt="Click to enlarge" src="https://raw.githubusercontent.com/sensible-hq/sensible-docs/v0/assets/images/final/box_overlap.png" />

## Improvement: Output document's file type

With the Get File Metadata method's new Content Type enum, you can output the document's MIME content type to the extraction's `parsed_document` output. For example, you can use the [Conditional](doc:conditional)  method to extract a set of fields based on whether a document's file type is `image/jpeg`.  For more information, see the [Get File Metadata](doc:get-file-metadata) method.

## Improvement: Reduce large output size when postprocessing

When you specify a completely custom schema for your extracted document data using a JsonLogic [postprocessor](doc:postprocessor), you can now suppress outputting data in the default `parsed_document` schema.  For example, if you want to reduce the size of the extracted output or you're interested solely in the postprocessor output, you can set the new Keep Parsed Document parameter in the postprocessor to false.  Setting it to false disables human review and Excel output.

## New feature: Support for XLSM documents

Sensible now supports data extraction and classification for XLSM documents. For more information, see [Supported file types](doc:file-types).
