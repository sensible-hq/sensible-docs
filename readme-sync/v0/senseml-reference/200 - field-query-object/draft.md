---
title: "draft"
hidden: true
---

destined for method object
====



xRangeFilter 
----

In combination with the Document Range method, the X Range Filter parameters defines a "column" that is bounded at the top and bottom by text.

The following image shows capturing a "cell" in a table:

![](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/images/xrange_filter_example.png)



In this example:

- Document Range by itself is not a good option because it would capture the address of the importer as well as the supplier.
- Table methods are not the best option, because each mailing address in the table can have a variable number of lines.  (TODO: is it really because this is a difficult table to recognize for ML combined with variable lines making it a bad candidate for fixed table?)
- The Region method is not a good option because of the variable number of lines. For example, if all addresses were only 3 lines, the "Type of business" text might move up the page, and we could inadvertently capture that. 



You can try out this example yourself in the Sensible app using the following downloadable PDF and config:

| Example PDF for X Range Filter | [Download link](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/pdfs/xrange_filter_example.pdf) |
| ------------------------------ | ------------------------------------------------------------ |

This example uses the following config:

```json
{
  "fields": [
    {
      "id": "mailing_address_supplier",
      "anchor": {
        "match": {
          "text": "supplier",
          "type": "startsWith"
        }
      },
      "method": {
        "id": "documentRange",
        "xRangeFilter": {
          "start": "left",
          "offsetX": -0.5,
          "width": 2
        },
        "stop": {
          "text": "type of business",
          "type": "includes"
        }
      }
    }
  ]
}
```
