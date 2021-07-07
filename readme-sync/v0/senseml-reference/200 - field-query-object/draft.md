---
title: "draft"
hidden: true
---

destined for method object topic
====



xRangeFilter example
----

In combination with the Document Range method, the X Range Filter parameters defines a "column" that is bounded at the top and bottom by text.

The following image shows capturing a cell in a table:

![](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/images/xrange_filter_example.png)



In this example, the X Range Filter parameter is the best option. Other options work less well:

- Document Range by itself is not a good option because it would capture the address of the importer as well as the supplier. 
- The Region method is not a good option because of the variable number of lines. For example, if all addresses were only 3 lines, the "Type of business" text might move up the page, and Sensible might inadvertently capture that text. 
- The Fixed Table and Table methods are not the best options, because the table's formatting is hard to recognize. The Text Table method is not the best option, because each mailing address in the table can have a variable number of lines.



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



xMajorSort example
----


In the following example, the handwritten text "Nash" is slightly taller than the text "Steve", so Sensible interprets "Nash" as *preceding* "Steve": 

![](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/images/xmajor_sort_example_1.png)

To eliminate the variability in order caused by short or tall handwriting,  set `"xMajorSort":"true"` so you can reliably capture the first and last name in their order along an x-axis:

![](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/images/xmajor_sort_2.png)

You can try out this example yourself in the Sensible app using the following downloadable PDF and config:

| Example PDF for xMajorSort | [Download link](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/pdfs/merge_lines_ocr_example.pdf) |
| -------------------------- | ------------------------------------------------------------ |

This example uses the following config:

```json
{
  "fields": [
    {
      "id": "_name_joint_owner_raw",
      "match": "last",
      "anchor": {
        "match": {
          "type": "startsWith",
          "text": "Name",
          "isCaseSensitive": true
        }
      },
      "method": {
        "id": "region",
        "start": "above",
        "width": 2.3,
        "height": 0.4,
        "offsetX": 0.2,
        "offsetY": -0.3,
        "xMajorSort": true
      }
    }
  ]
}