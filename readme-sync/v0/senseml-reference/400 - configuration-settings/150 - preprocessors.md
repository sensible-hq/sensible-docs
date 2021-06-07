---
title: "Preprocessors"
hidden: false
---
The following sections describe the value of preprocessors you can use to clean up your document:

* ligature
* pageFilter
* pageRange
* removeHeader
* removeFooter



Ligature
===

Intelligently replaces Unicode ligatures in PDF text extraction.  For more information about ligatures, see the Notes section.

Parameters
----

| key                       | value   | description                                                      |
| ------------------------- | ------ | ------------------------------------------------------------ |
| `type` (**required**)     | `ligature` |                                                    |
| `mappings` (**required**) | object | An object mapping ligature strings (e.g., `"\u0000"`) to an array of possible ligature replacements (e.g., `["ff", "ffi", "fi", "fl"]`). Sensible uses a dictionary in the target language to choose replacements that lead to known words. Currently Sensible supports American English (en-us). This approach is conservative and may leave some Unicode characters in proper names or other non-word data. |

Examples
----

This config  includes a ligature mapping preprocessor and shows the output of the whole document in order to check the ligature replacement accuracy: 

```
{
  "preprocessors": [
    {
      "type": "ligature",
      "mappings": {
        "\u0013": [
          "gg"
        ],
        ",": [
          "fi"
        ]
      }
    }
  ],
  "fields": [
    {
      "id": "all_lines_in_doc",
      "method": {
        "id": "documentRange",
        "includeAnchor": true
      },
      "anchor": {
        "match": {
          "type": "first"
        }
      }
    }
  ]
}
```





Notes
----

*Ligatures* are two or more letters joined together into a sign glyph. They appear to be garbage Unicode characters in your direct text extraction, like this:

```json
….incinerating or composting toilets; \u0000re suppression systems; water softeners, conditioners or \u0000ltering systems; over\u0000ow drains for tubs and sinks; back\u0000ow prevention devices...
```

Even if the PDF rendering looks fine, ligatures can still exist in the extracted text. In the preceding example, `fi`, `fl` and others are joined together and appear as `\u0000` in the raw text, so that you see `\u0000re` instead of `fire` and `over\u0000ow` instead of `overflow`.

To find out if ligatures exist in the extracted text for your PDF, you can extract all the lines in the PDF and search for unicode characters. To extract all lines into one key-value pair, you can use a config like:

```
{
  "fields": [
     
    {
      "id": "all_lines_in_doc",
      "method": {
        "id": "documentRange",
        "includeAnchor": true
      },
      "anchor": {
        "match": {
          "type":"first"
        }
      }
    }
  ],
}
```

The following image shows an example of capturing all the lines of text in a W-9 form:

![](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/images/all_lines.png)



mergeLines
====


Merges nearby lines more aggressively than the built-in line merger

Parameters
----


| key                                        | value   | description                                                      |
| ------------------------------------------ | ------ | ------------------------------------------------------------ |
| `type` (**required**)                      | string | "mergeLines"                                                 |
| `directlyAdjacentThreshold` (**required**) | number | Fraction of line height under which two adjacent lines (i.e., horizontally distributed along an x-axis)  are merged without a space. For example, at 0.15 two lines are merged without a space in between their contents when they are less than 15% of the line height apart from one another. |
| `adjacentThreshold` (**required**)         | number | Identical to the above, but for mergers with a space in between. |
| `yOverlapThreshold`                        | number | Y overlap is the portion of the joint y-axis range of two lines that is occupied by both lines. For example, if two lines share the same minimum and maximum y-axis values, they will have an overlap of 1. If one line’s extent is from 0 to 10 and the other line’s extent is from 2 to 12 on the y-axis, they will have an overlap of .667 (8 / 12). The yOverlapThreshold is the y overlap above which mergeLines will merge two adjacent lines |
| `minXGapThreshold`                         | number |                                                              |



   



pageFilter
====
Filters out low-scoring pages given a bag of target terms and stop terms. 

Parameters
----


| key                    | value   | description                                                      |
| ---------------------- | ------ | ------------------------------------------------------------ |
| `type` (**required**)  | string | "pageFilter"                                                 |
| `terms` (**required**) | array  | An array of strings with terms to score positively (e.g., `["number of buildings", "no. of buildings"]`) |
| `stopTerms`            | array  | An array of strings with terms to score negatively (e.g., `["comparables"]`) |
| `maxPages`             | number | The maximum number of highest-scoring pages to pass through the filter |

 


pageRange
====

Filters pages outside the start page and end page

Parameters
----


| key         | value   | description                                                      |
| ----------- | ------ | ------------------------------------------------------------ |
| `type`      | string | "pageRange"                                                  |
| `startPage` | number | Zero-based index of the first page to pass through the filter (inclusive).  The default is 0. |
| `endPage`   | number | Zero-based index of the last page to pass through the filter (exclusive). The default is the length of the pages array |

 

removeHeader
====
Removes repeated elements at the start of pages in the document.   

Parameters
----

| key            | value   | description                                                      |
| -------------- | ------ | ------------------------------------------------------------ |
| `type`         | string | "removeHeader"                                               |
| `startsOnPage` | number | The first page number on which to start checking for repeated elements. The default is 1.  Note this is the page *number* not  the page's zero-based index in the pages array. The default is 1. |

removeFooter
====

Removes repeated elements at the end of pages in the document.   

Parameters
----

| key            | value   | description                                                      |
| -------------- | ------ | ------------------------------------------------------------ |
| `type`         | string | "removeHeader"                                               |
| `startsOnPage` | number | The first page number on which to start checking for repeated elements. The default is 1.  Note this is the page *number* not  the page's zero-based index in the pages array. The default is 1. |

