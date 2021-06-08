---
title: "Preprocessors"
hidden: false
---


Removes repeated elements at the end of pages in the document from the direct text extraction of the page.   

Parameters
====

| key            | value   | description                                                      |
| -------------- | ------ | ------------------------------------------------------------ |
| type (**required**) | `removeHeader` | To recognize a footer, this preprocessor starts at the bottom of the page and moves up the page, stopping as soon as it finds a nonrepeating element.  Page numbers are ignored.   For an example, see the Examples section. |
| startsOnPage | integer. default: 1 | The first page number on which to start checking for repeated elements. The default is 1.  Note this is the page *number*, not the page's zero-based index in the pages array. |

Examples
====

The following images show:

- A repeating footer with an incrementing page number. This footer is removed from the direct text extraction.
- A repeating sidebar that overlaps the y-extent of both repeating and variable elements: 
  - Where it overlaps a repeating footer, it is also treated as a footer and is removed from the direct text extraction.
  - Where it overlaps variable text, it is not considered a footer and is still included in the direct text extraction

![](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/images/remove_footer_example_1.png)

![](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/images/remove_footer_example_2.png)


You can try out this example yourself in the Sensible app using the following downloadable PDF and config:

| Example PDF for Remove Footer preprocessor | [Download link](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/pdfs/![](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/images/remove_footer_example.png).pdf) |
| ------------------------------------------ | ------------------------------------------------------------ |

This example uses the following config:

```json
{
  "preprocessors": [
    {
      "type": "removeFooter",
      "startsOnPage": 1
    }
  ],
  "fields": [
    {
      "id": "all_lines_minus_repeating_footer_elements",
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