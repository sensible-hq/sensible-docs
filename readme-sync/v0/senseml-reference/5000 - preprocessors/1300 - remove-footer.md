---
title: "Remove footer"
hidden: false
---

Ignores repeating elements at the bottoms of pages. These elements are removed from the direct-text extraction of the document.  

To recognize a footer, this preprocessor starts at the bottom of the page and moves up the page, stopping as soon as it finds a nonrepeating element. 

Sensible recognizes these elements as "repeating":

- Elements whose y-extent doesn't overlap with any variable element on the page
- Positively incrementing page numbers

These elements are *not* recognized as "repeating": 

- Elements that change their alignment on alternate pages (for example, page numbers aligned alternately left and right, as in a book)
- A repeating element that's missing from even one page (for example, from an intentionally blank page). 

Parameters
====

| key            | value   | description                                                      |
| -------------- | ------ | ------------------------------------------------------------ |
| type (**required**) | `removeFooter` | For an example, see the Examples section. |
| startsOnPage | integer. default: 1 | The first page number on which to start checking for repeated elements. Note this is the page *number*, not the page's zero-based index in the pages array. To filter out end pages that lack a repeating element, use the Page Range preprocessor to define an End Page parameter. |

Examples
====

The following example shows:

- A repeating footer with an incrementing page number. Sensible removes this from the direct text extraction.
- A repeating sidebar that overlaps the y-extent of both repeating and variable elements: 
  - Where it overlaps a repeating element, Sensible treats it as repeating and removes it from the direct text extraction.
  - Where it overlaps variable text, Sensible treats it as nonrepeating and includes it in the direct text extraction

**Config**
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
      "id": "all_lines_minus_repeating_bottom_elements",
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

**Example document**

The following images show the example PDF used with this example config:

![Click to enlarge](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/images/final/remove_footer_1.png)

![Click to enlarge](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/images/final/remove_footer_2.png)


| Example PDF | [Download link](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/pdfs/remove_footer.pdf) |
| ------------------------------------------ | ------------------------------------------------------------ |

**Output**

```json
{
  "all_lines_minus_repeating_bottom_elements": {
    "type": "string",
    "value": "This is the body for the 1st page It differs from page to page. . do eiusmod tempor incididunt consectetur adipiscing elit do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco ullamco laboris nisi ut aliquip ex ea commodo consequat uis aute irure dolor in This is a reprehenderit repeating in voluptate velit esse cillum sidebar dolore eu fugiat nulla pariatur. This is the page 2 body. It varies from page to page. Lorem ipsum dolor sit amet. consectetur adipiscing elit. Excepteur sint occaecat cupidatat non proident. sunt in culpa qui officia deserunt mollit anim id est laborum. Sed ut perspiciatis unde omnis iste natus error sit voluptatem Accusantium. doloremque laudantium, totam rem aperiam, eaque ipsa quae ab This is a llo inventore veritatis et quasi repeating quasi architecto beatae vitae. dicta sunt explicabo. sidebar"
  }
}
```

