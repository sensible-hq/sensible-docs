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
| xRangeFilter     | object                                                       | Excludes the portion of the page to the right of a starting point on the x-axis.  Any line that only partially falls inside the defined area is excluded. Parameters: <br/>`start` - `right` ,`left`  - Adjusts the starting point to the right or left boundary of the anchor line.<br/> `offsetX` - Adjusts the starting point defined by the Start parameter.  <br/> `width` - The width of page portion to capture, in inches. |
| xMajorSort       | boolean                                                      | Orders lines by their x-axis position. Useful in cases where the text is not well-aligned (notably with handwriting). |





