---
title: "Method object"
hidden: false
---

A Method object defines how to expand out from an Anchor line and extract target data. Methods are available in Field objects.

For the full list of methods available, see [Methods](doc:methods). 

[**Parameters**](doc:method#section-parameters)
[**Examples**](doc:method#section-examples)

Parameters
-----

The following global parameters available to all methods:

| Key              | Value                                                        | Description                                                  |
| ---------------- | ------------------------------------------------------------ | ------------------------------------------------------------ |
| `id`             | [`box`](doc:box),<br/>[`checkbox`](doc:checkbox),<br/>[`column`](doc:column),<br/>[`documentRange`](doc:document-range),<br/>[`fixedTable`](doc:fixed-table),<br/> [`invoice`](doc:invoice),<br/>[`keyValue`](doc:key-value),<br/>[`label`](doc:label),<br/>[`passthrough`](doc:passthrough),<br/>[`regex`](doc:regex),<br/>[`region`](doc:region),<br/>[`row`](doc:row),<br/>[`signature`](doc:signature),<br/>[`table`](doc:table),<br/>[`textTable`](doc:text-table) | see [Methods](doc:methods).                                  |
| tiebreaker       | `first`, `second`, `third`, `last`, `>`, `<`                 | If the method returns multiple elements (for example, a Row method), which element to extract. <br/>Use `>` and `<` to extract maximum and minimums elements [sorted](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Operators/Less_than) alphanumerically. To compare numeric amounts and ignore non-numbers in the match result, add a numeric type, for example `type: currency`, as a top-level parameter to the field. |
| lineFilters      | Match object                                                 | Filters out the specified lines from the method match. For example, the Box method extracts all lines from a box, but you can use this parameter to filter out unwanted footer text in the box. |
| wordFilters      | string array                                                 | Filters out the specified strings from the method results.   |
| whitespaceFilter | `spaces`, `all`                                              | Remove extra whitespaces.<br/> `spaces` - remove only extra spaces <br/> `all` - remove all whitespace characters, including newlines and tabs. |
| xRangeFilter     | object                                                       | Defines left and right boundaries in which to capture lines. For example, in combination with the Document Range method, the X Range Filter parameter defines a "column" that is bounded at the top and bottom by text.  Any line that only partially falls inside the defined rectangular region is excluded. Parameters: <br/>`start` - `right`,`left`  - Defines the starting point of the "column" at either the right or left boundary of the anchor line.<br/> `offsetX` - Adjusts the horizontal position of the starting point defined by the Start parameter.  <br/> `width` - The width of the page portion to capture, in inches.<br/><br/> For an example, see the Examples section. |
| xMajorSort       | boolean                                                      | Use this parameter to correctly sort text that unexpectedly varies in height and vertical position (such as handwriting).  In such badly aligned text, slight jitter in the vertical positions of lines can cause Sensible to incorrectly sort lines that a human reader interprets as following left to right.  The X Major Sort parameter corrects the problem by sorting lines primarily by their horizontal position, rather than primarily by their vertical position (the default). <br/><br/> For an example, see the Examples section. |

Examples
====

X Major Sort example
----


In the following example, the handwritten text "Nash" is slightly taller than the text "Steve", so Sensible interprets "Nash" as *preceding* "Steve" (reversing the order interpreted by a human reader): 

![Click to enlarge](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/images/final/xmajor_sort_example_1.png)

To reliably capture the first and last name in their left-to-right order,  set `"xMajorSort":"true"` :

![Click to enlarge](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/images/final/xmajor_sort_example_2.png)

Try out this example in the Sensible app using the following PDF and config:

| Example PDF | [Download link](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/pdfs/merge_lines_ocr_example.pdf) |
| ----------- | ------------------------------------------------------------ |

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
```

X Range Filter example
----

In combination with the Document Range method, the X Range Filter parameter defines a "column" that is bounded at the top and bottom by text.

The following image shows using this parameter to extract a "cell" of text that doesn't easily fit other methods:

![Click to enlarge](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/images/final/xrange_filter_example.png)



In this example, the X Range Filter parameter is the best option:

- Document Range by itself is not a good option, because it captures the address of the importer as well as the supplier. 
- The Fixed Table and Table methods are not the best options, because the table formatting is hard to recognize.
- The Text Table method is not the best option, because it splits multi-line rows.

Try out this example in the Sensible app using the following PDF and config:

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







