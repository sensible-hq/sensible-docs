---
title: "Remove footer"
hidden: false
---

Ignores repeating elements at the bottoms of pages.

Sensible recognizes footers in one of two ways:

- (Default)  Sensible searches for repeated text at the bottom of the page. For more information about automatic recognition, see [Notes](doc:remove-footer#notes). 

- (Configurable) To bypass automatic recognition, for example to recognize footer text that varies slightly, configure a text match. Sensible removes all text below the bottom boundary of the matched text. The preprocessor removes text on pages in which it finds the match, and ignores pages missing the match. 



Parameters
====

| key            | value   | description                                                      |
| -------------- | ------ | ------------------------------------------------------------ |
| type (**required**) | `removeFooter` | For an example, see the Examples section. |
| startsOnPage | integer. default: 1 | The first page number on which to start checking for repeated elements. Note this is the page *number*, not the page's zero-based index in the pages array. To filter out end pages that lack a repeating element, use the Page Range preprocessor to define an End Page parameter. |
| match | [Match](doc:match) object or array of Match objects | Bypasses automatic footer recognition.<br/>Removes all text on the page below the bottom boundary of the matched line.<br/>If Sensible doesn't find the match, it doesn't perform footer removal. |
| offsetY | number in inches. default: 0 | Bypasses automatic footer recognition.<br/>Defines a point at which to start text removal. Positive values offset down the page, negative values offset up the page.<br/>If used with no Match parameter defined, offsets from the bottom of the page.<br/>If used with the Match parameter, offsets from the bottom boundary of the matched line. <br/> |

Examples
====

The following example shows using automatic footer recognition. The example document contains:

- A repeating footer with an incrementing page number. Sensible removes this.
- A repeating sidebar that overlaps the y-extent of both repeating and variable elements: 
  - Where it overlaps a repeating element, Sensible treats it as repeating and removes it.
  - Where it overlaps variable text, Sensible treats it as nonrepeating and retains it.

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

The following images show the example document used with this example config:

![Click to enlarge](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/images/final/remove_footer_1.png)

![Click to enlarge](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/images/final/remove_footer_2.png)


| Example document | [Download link](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/pdfs/remove_footer.pdf) |
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

Notes
---

**Automatic footer recognition**

To automatically recognize a footer, this preprocessor starts at the bottom of the page and moves up the page, stopping as soon as it finds a nonrepeating element. 

Sensible recognizes these elements as "repeating":

- Elements whose y-extent doesn't overlap with any variable element on the page
- Positively incrementing page numbers

These elements are *not* recognized as "repeating": 

- Elements that change their alignment on alternate pages (for example, page numbers aligned alternately left and right, as in a book)
- A repeating element that's missing from even one page (for example, from an intentionally blank page). 
