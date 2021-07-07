---
title: "Method object"
hidden: false
---

A Method object defines how to expand out from an Anchor object and grab data you want to extract. Methods are available within Field objects.

For the full list of methods available, see [Methods](doc:methods). 

Global parameters for methods
-----

The parameters for a method vary based on the method type (defined in the `id` parameter). Following are the parameters common to all methods:

| Key              | Value                                                        | Description                                                  |
| ---------------- | ------------------------------------------------------------ | ------------------------------------------------------------ |
| `id`             | [`box`](doc:box),<br/>[`checkbox`](doc:checkbox),<br/>[`column`](doc:column),<br/>[`documentRange`](doc:document-range),<br/>[`fixedTable`](doc:fixed-table),<br/> [`invoice`](doc:invoice),<br/>[`keyValue`](doc:key-value),<br/>[`label`](doc:label),<br/>[`passthrough`](doc:passthrough),<br/>[`regex`](doc:regex),<br/>[`region`](doc:region),<br/>[`row`](doc:row),<br/>[`signature`](doc:signature),<br/>[`table`](doc:table),<br/>[`textTable`](doc:text-table) | see [Methods](doc:methods).                                  |
| tiebreaker       | `first`, `second`, `third`, `last`, `>`, `<`                 | Which element in the method match is the target. Use the comparisons `>` and `<` to grab maximum and minimum values in the row. By default the comparisons are sorted alphanumerically using [unicode values](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Operators/Less_than).  If you want to compare numeric amounts and ignore non-numbers in the match result,  then add a numeric type like  `type: currency` as a top-level parameter to the field. |
| lineFilters      | Match object                                                 | Filters out the matched lines from the method results. A example is if you’re using a Box method, and there’s a text footer in the box that you don't want to capture, or some additional label to the main anchor label that you don't want to capture. |
| wordFilters      | string array                                                 | Filters out unwanted matched strings from the method results. |
| whitespaceFilter | `spaces`, `all`                                              | Remove extraneous whitespaces. Use `spaces` to remove only extra spaces and `all` to remove all whitespace characters, including new lines and tabs. |
| xRangeFilter     | object                                                       | Excludes lines that do not fall fully between a starting point and an ending point along the x-axis. The starting point is defined by the start parameter plus the offsetX parameter, and the ending point is that starting point plus the width parameter Any line that only partially falls inside the defined area is excluded. Parameters: <br/>`start` - `right` ,`left`  - Adjusts the starting point to the right or left boundary of the anchor line.<br/> `offsetX` - Adjusts the starting point defined by the Start parameter.  <br/> `width` - The width of page portion to capture, in inches. |
| xMajorSort       | boolean                                                      | The X Major Sort parameter orders lines first by their x-axis position, rather than the default behavior of ordering first by the y-axis position. This behavior applies to lines captured by a method, not to lines captured by an anchor. This is useful in cases where the text is not well aligned (notably with handwriting). With badly aligned text, slight jitter in the vertical coordinate of lines can cause Sensible to see two lines that are seemingly on the same Y coordinate as appearing in the reverse order. Use the X Major Sort parameter to fix this problem. |

Examples
====

xMajorSort example
----


In the following example, the handwritten text "Nash" is slightly taller than the text "Steve", so Sensible interprets "Nash" as *preceding* "Steve": 

![](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/images/xmajor_sort_example_1.png)

To eliminate the variability in order caused by short or tall handwriting,  set `"xMajorSort":"true"` so you can reliably capture the first and last name in their order along an x-axis:

![](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/images/xmajor_sort_example_2.png)

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
```

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







