---
title: "Remove header"
hidden: false
---

Removes repeated elements at the tops of pages from the direct text extraction of the pages.   

To recognize a header, this preprocessor starts at the top of the page and moves down the page, stopping as soon as it finds a nonrepeating element. 

These elements are recognized as "repeating":

- Elements whose y-extent does not overlap with any variable element
- Positively incrementing page numbers

These elements are not recognized as "repeating": 

- Elements that change their alignment on alternate pages (for example, page numbers aligned alternately left and right, as in a book)
- A repeating element that is missing from even one page (for example, from an intentionally blank page). 

Parameters
====

| key                 | value               | description                                                  |
| ------------------- | ------------------- | ------------------------------------------------------------ |
| type (**required**) | `removeFooter`      | For an example, see the Examples section.                    |
| startsOnPage        | integer. default: 1 | The first page number on which to start checking for repeated elements. The default is 1.  Note this is the page *number*, not the page's zero-based index in the pages array. To filter out end pages that lack a repeating element, use the Page Range preprocessor to define an End Page parameter. |

Examples
====

The following images show:

- A repeating header with an incrementing page number. This element is removed from the direct text extraction.
- A repeating sidebar that overlaps the y-extent of both repeating and variable elements: 
  - Where it overlaps a repeating element, it is also treated as repeating and is removed from the direct text extraction.
  - Where it overlaps variable text, it is not considered repeating and is still included in the direct text extraction

![](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/images/remove_header_example_1.png)

![](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/images/remove_header_example_2.png)


You can try out this example yourself in the Sensible app using the following downloadable PDF and config:

| Example PDF for Remove Header preprocessor | [Download link](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/pdfs/![](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/images/remove_header_example.pdf) |
| ------------------------------------------ | ------------------------------------------------------------ |

This example uses the following config:

```json
{
  "preprocessors": [
    {
      "type": "pageRange",
      "endPage": 2
    },
    {
      "type": "removeHeader",
      "startsOnPage": 1
    }
  ],
  "fields": [
    {
      "id": "all_lines_minus_repeating_top_elements",
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

