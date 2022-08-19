---
title: "Remove header"
hidden: false
---

Ignores repeating elements at the tops of pages.

Sensible recognizes headers in one of two ways:

- (Default)  Sensible searches for repeated text at the top of the page. For more information about automatic recognition, see [Notes](doc:remove-header#notes). 

- (Configurable) To bypass automatic recognition, for example to recognize header text that varies slightly, configure a text match. Sensible removes all text above the top boundary of the matched text. The preprocessor removes text on pages in which it finds the match, and ignores pages missing the match 

Parameters
====

| key                 | value                                               | description                                                  |
| ------------------- | --------------------------------------------------- | ------------------------------------------------------------ |
| type (**required**) | `removeHeader`                                      | For an example, see the Examples section.                    |
| startsOnPage        | integer. default: 1                                 | The first page number on which to start checking for repeated elements. Note this is the page *number*, not the page's zero-based index in the pages array. To filter out end pages that lack a repeating element, use the Page Range preprocessor to define an End Page parameter. |
| match               | [Match](doc:match) object or array of Match objects | Bypasses automatic header recognition.<br/>Removes all text on the page above the top boundary of the matched line. |
| offsetY             | number in inches. default: 0                        | Use with the Match parameter. <br/>Offsets from the top boundary of the matched line to define a new point at which to start text removal. Positive values offset down the page, negative values offset up the page. |

Examples
====

The following example shows:

- A repeating header with an incrementing page number. Sensible removes this.
- A repeating sidebar that overlaps the y-extent of both repeating and variable elements: 
  - Where it overlaps a repeating element, Sensible treats it as repeating and removes it.
  - Where it overlaps variable text, Sensible treats it as nonrepeating and retains it.

  

**Config**

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

**Example document**

The following images show the example PDF used with this example config:

![Click to enlarge](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/images/final/remove_header_1.png)

![Click to enlarge](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/images/final/remove_header_2.png)

| Example PDF | [Download link](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/pdfs/remove_header.pdf) |
| ------------------------------------------ | ------------------------------------------------------------ |

**Output**

```json
{
  "all_lines_minus_repeating_top_elements": {
    "type": "string",
    "value": "This is the body for the 1st page Header on the It differs from page to page. . do eiusmod tempor incididunt y-axis consectetur adipiscing elit do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco ullamco laboris nisi ut aliquip ex ea commodo consequat uis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. This is the page 2 body. Header on the It varies from page to page. Lorem ipsum dolor sit amet. y-axis consectetur adipiscing elit. Excepteur sint occaecat cupidatat non proident. sunt in culpa qui officia deserunt mollit anim id est laborum. Sed ut perspiciatis unde omnis iste natus error sit voluptatem Accusantium. doloremque laudantium, totam rem aperiam, eaque ipsa quae ab llo inventore veritatis et quasi quasi architecto beatae vitae. dicta sunt explicabo."
  }
}
```

Notes
----

**Automatic header recognition**

To recognize a header, this preprocessor starts at the top of the page and moves down the page, stopping as soon as it finds a nonrepeating element. 

Sensible recognizes these elements as "repeating":

- Elements whose y-extent doesn't overlap with any variable element
- Positively incrementing page numbers

These elements aren't recognized as "repeating": 

- Elements that change their alignment on alternate pages (for example, page numbers aligned alternately left and right, as in a book)
- A repeating element that's missing from even one page (for example, from an intentionally blank page).