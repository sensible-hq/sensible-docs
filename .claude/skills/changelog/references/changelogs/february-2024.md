---
title: February 2024
slug: february-2024
date: 2024-01-04
---

In the last month, we improved the config-authoring experience in the Sensible app, added advanced features for sections and for the Custom Computation method, and made minor improvements to several SenseML methods. 

## UX improvement:  Batch-upload reference documents

You can now upload multiple reference documents with a single click in the Sensible Instruct editor using the **Add file** button, making it easier to test configs as you edit them.

![Click to enlarge](https://raw.githubusercontent.com/sensible-hq/sensible-docs/v0/assets/images/final/changelog_feb2024_upload.png)

## Improvement: Advanced anchor configuration for sections with new External Range parameter

For sections that lack internal anchoring text, you can now specify anchoring text anywhere in the document using the new External Range parameter.

For example, in the following screenshot, the green brackets denote sections, where each section is a claim. The labels for the claims' content are at the start of the document, under the `Claims contents` heading, so you can define an external range to anchor on these labels. 

![Click to enlarge](https://raw.githubusercontent.com/sensible-hq/sensible-docs/v0/assets/images/final/sections_external_range_2.png)

For more information about this example, see [Advanced: External anchors for sections](doc:sections-example-external-range).

## UX improvement:  Easier LLM prompt authoring with auto-generated field IDs

We've improved the user experience for authoring large-language model (LLM)-powered methods. Sensible now auto-generates IDs for your prompts in the Sensible Instruct editor after you click the **send** icon. You also can edit the IDs manually. In the following screenshot, the IDs were generated automatically from the user's descriptions using LLMs:

![Click to enlarge](https://raw.githubusercontent.com/sensible-hq/sensible-docs/v0/assets/images/final/changelog_feb2024_field_id.png)

## New feature: Replace operator for custom computations

We've extended [JsonLogic](https://jsonlogic.com/) with a new Replace operation. You can use the Replace operation in the Custom Computation method or in extraction validation rules. For example, you can redact all but the last four digits of a customer ID number with syntax like:

```Text json
{
      "id": "replace_regex_test",
      "method": {
        "id": "customComputation",
        "jsonLogic": {
          "replace": {
            "source": {
              "var": "customer_id.value"
            },
            "find_regex": "(\\d{4})(\\d{4})",
            "replace": "xxxx$2",
            "flags": "g"
          }
        }
      }
    }
```

 For more information, see [Replace operation](doc:custom-computation#replace).

## Deprecation: Prompt Introduction parameter

Sensible removed the ability for users to configure the introductions to [full prompts](doc:prompt) that Sensible submits to LLMs. By exercising full control over prompt introductions, Sensible can improve LLM accuracy for Sensible Instruct methods.

## Improvement: NLP table accuracy

Sensible has improved accuracy for NLP tables through better detection of table titles. Sensible now uses the table title detected by the OCR provider to score tables' relevance. Sensible falls back to the previous behavior of relying on text positioning to find a title if the OCR provider doesn't find a title. 

## Improvement: Match text based on left-to-right page positioning

With the new X Range Filter parameter on the  [Match](doc:match) object, you can include horizontal alignment on the page as a text-match criterion. For example, anchor on a line if falls within 1 to 3 inches of the left edge of a page.

## Improvement: Google OCR update

Sensible updated its Google [OCR engine](doc:ocr-engine) from an end-of-life version to the most recent version. This introduces regressions in rare cases, so test your existing configs if they use Google OCR.

## UX improvement: Filter by batch description

In the Sensible app, you can now filter past extractions by batch description or by batch upload date-time. Sensible creates a batch when you use the **Extraction** tab to upload multiple files at once for extraction. 

![Click to enlarge](https://raw.githubusercontent.com/sensible-hq/sensible-docs/v0/assets/images/final/changelog_feb2024_batch_filter.png)  

## Improvement: Troubleshoot table OCR with Detect Table Structure Only parameter

You can now troubleshoot optical character recognition inside tables using the new Detect Table Structure Only parameter. This option allows you to configure your OCR provider for the table, or to bypass OCR and use embedded text. This parameter is available for all table methods except the Text Table method. If setting the parameter results in incorrect line sorting, then set the Annotate Superscript and Subscript parameter to true. For more information, see [Fixed Table](doc:fixed-table#parameters).
