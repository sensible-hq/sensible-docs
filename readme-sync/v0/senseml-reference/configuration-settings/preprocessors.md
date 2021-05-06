---
title: "Preprocessors"
hidden: false
---
The following sections describe the type of preprocessors you can use to clean up your document:

* ligature
* pageFilter
* pageRange
* removeHeader
* removeFooter



ligature
----

Intelligently replaces Unicode ligatures in PDF text extraction.

**components**

| item                      | type   | comment                                                      |
| ------------------------- | ------ | ------------------------------------------------------------ |
| `type` (**required**)     | string | "ligature"                                                   |
| `mappings` (**required**) | object | An object mapping strings (e.g., `"\u0000"`) to an array of possible ligature replacements (e.g., `["ff", "ffi", "fi", "fl"]`) |

**example**

This config  includes a  ligature mapping preprocessor and a field that finds a customer name: 

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
      "id": "name_first_last",
      "anchor": "Customer name",
      "method": {
        "id": "label",
        "position": "below"
      }
    }
  ]
}
```

**Notes**

 To find out the ligatures that exist in the extracted text for your PDF, you can extract all the lines in the PDF and search for them. To extract all lines into one key-value pair, you can use a config like:

```
    {
  "fields": [
    
    
    {
      "id": "all_lines_in_doc",
      "method": {
        "id": "documentRange"
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

[!img](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/images/v0/all_lines.png)



mergeLines
---


Merges nearby lines more aggressively than the built-in line merger

**components**

| item                                       | type   | comment                                                      |
| ------------------------------------------ | ------ | ------------------------------------------------------------ |
| `type` (**required**)                      | string | "mergeLines"                                                 |
| `directlyAdjacentThreshold` (**required**) | number | Fraction of line height under which two adjacent lines are merged without a space. For example, at 0.15 two lines will be merged without a space in between their contents when they are less than 15% of the line height apart from one another |
| `adjacentThreshold` (**required**)         | number | Identical to the above, but for mergers with a space in between |
| `yOverlapThreshold`                        | number |                                                              |
| `minXGapThreshold`                         | number |                                                              |







pageFilter
----
Filters out low-scoring pages given a bag of target terms and stop terms. 

**components** 

| component              | type   | comment                                                      |
| ---------------------- | ------ | ------------------------------------------------------------ |
| `type` (**required**)  | string | "pageFilter"                                                 |
| `terms` (**required**) | array  | An array of strings with terms to score positively (e.g., `["number of buildings", "no. of buildings"]`) |
| `stopTerms`            | array  | An array of strings with terms to score negatively (e.g., `["comparables"]`) |
| `maxPages`             | number | The maximum number of highest-scoring pages to pass through the filter |

 


pageRange
---

Filters pages outside the start page and end page

**components** 

| component   | type   | comment                                                      |
| ----------- | ------ | ------------------------------------------------------------ |
| `type`      | string | "pageRange"                                                  |
| `startPage` | number | Zero-based index of the first page to pass through the filter (inclusive).  The default is 0. |
| `endPage`   | number | Zero-based index of the last page to pass through the filter (exclusive). The default is the length of the pages array |

 

removeHeader
----
Removes repeated elements at the start of pages in the document.   

**components** 

| component      | type   | comment                                                      |
| -------------- | ------ | ------------------------------------------------------------ |
| `type`         | string | "removeHeader"                                               |
| `startsOnPage` | number | The first page number on which to start checking for repeated elements. The default is 1.  Note this is the page *number* not  the page's zero-based index in the pages array. The default is 1. |

removeFooter
----

Removes repeated elements at the end of pages in the document.   

**components** 

| component      | type   | comment                                                      |
| -------------- | ------ | ------------------------------------------------------------ |
| `type`         | string | "removeHeader"                                               |
| `startsOnPage` | number | The first page number on which to start checking for repeated elements. The default is 1.  Note this is the page *number* not  the page's zero-based index in the pages array. The default is 1. |

