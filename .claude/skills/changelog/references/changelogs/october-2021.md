---
title: October 2021
slug: october-2021
date: 2021-10-11
---

The last month marked a large release, with support for extracting multiple documents out of a single PDF, a new feature for extracting complex, repeating documents sections, and several other enhancements.

## New feature: PDF portfolios

You can now extract multiple documents packaged into a single PDF (a PDF "portfolio") using just one API call to multiple document types.  This allows you to write [validations](doc:validate-extractions) for each document in the portfolio separately. Just list the types of documents found in the portfolio, and Sensible returns a list of extracted documents. Sensible automatically parses the portfolio into multiple documents using our newly enhanced fingerprints, which allow you to specify text in start and end pages of a document. For more information, see the [docs](doc:portfolio).

## New feature: Sections

Extract complex, repeating sections from a document using the new Sections feature.  For example, extract an array of `unprocessed_claims` objects from a loss run document: 

![Click to enlarge](https://raw.githubusercontent.com/sensible-hq/sensible-docs/v0/assets/images/final/changelog_oct20201_sections.png)

You can skip missing information in sections, nest sections inside sections, and configure complex starts and stops for the sections and their ranges in the documents, making this feature powerfully configurable. For more information, see the [docs](doc:sections).

## New feature: Any match

We've introduced a new match type, the Any match, in addition to our Regex, Simple, and First matches. With the Any match, you can list an array of matches for synonymous or alternate terms, and return a match for any of the terms. For example:

```json
{
  "fields": [
    {
      "anchor": {
        "match": {
          "type": "any",
          "matches": [
            {
              "type": "equals",
              "text": "load value"
            },
            {
              "type": "regex",
              "text": "cargos? value"
            }
          ]
        }
      },
      "id": "cargo",
      "method": {
        "id": "passthrough"
      }
    }
  ]
}
```

For more information, see the [docs](doc:match#any-match).

## Improvement: Phone number type

We've expanded our existing types to include phone numbers. For more information, see the [docs](doc:types#phone-number).

## Improvement: Web app UX

In the Sensible app, you can search for configurations and reference documents. While editing SenseML, you can now quickly change between configurations:

![Click to enlarge](https://raw.githubusercontent.com/sensible-hq/sensible-docs/v0/assets/images/final/changelog_oct2021_pick_config.png)

## Improvement: Better page rotation detection

We added improvements and bug fixes to how Sensible corrects for rotated pages (in the case where a scanned document is photographed or scanned at an angle). Sensible now handles rotated pages that contain a mix of horizontally aligned and vertically aligned text (for example, vertical bar chart labels).
