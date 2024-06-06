---
title: "Remove page"
hidden: true
---

Removes pages that match the specified text.

Parameters
====

| key                  | value              | description                                                  |
| -------------------- | ------------------ | ------------------------------------------------------------ |
| type (**required**)  | string             | "removePage"                                                 |
| match (**required**) | Match object       | Sensible removes each pages that contain this match. **questions: what if there were a match array, where item 0 matches page 2 and item 1 matches page 3 -- would we remove page 3? or would you have to have everything in the array be on the same page, then use a pageOffset?  **  To remove a single page offset from the first page of the document, rather than offset from matched text,` specify `"match": { "type": "first" }`. |
| matchAll             | boolean            | If true, removes all pages containing the line specified by the Match parameter. |
| pageOffset           | number. default: 0 | The zero-indexed number of the page to remove, counting from the page number of the text matched by the Match parameter. |

Examples
====

The following example shows removing all pages with an Appendix A header in order to get information  from Appendix B.

**Config**

```json
{
  "preprocessors": [
    {
      /* remove all pages containing 
         the large-font header "Appendix A" */
      "type": "removePage",
      "match": {
        "type":"equals",
      "text": "Appendix A",
      "minimumHeight": 0.2
      },
      "matchAll": true
    }
  ],
  "fields": [
    /* get the Rider A in appendix B,
       not Appendix A */
    {
      "id": "rider_A",
      "anchor": "rider a",
      "type": "currency",
      "method": {
        "id": "label",
        "position": "right",
      }
    }
  ]
}
```

**Example document**

![Click to enlarge](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/images/final/remove_page.png)

| Example document | [Download link](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/pdfs/remove_page.pdf) |
| ------------------------------------------ | ------------------------------------------------------------ |

**Output**

```json
{
  "rider_A": {
    "source": "$600",
    "value": 600,
    "unit": "$",
    "type": "currency"
  }
}
```

