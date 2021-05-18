---
title: "Method"
hidden: true
---



A Method object defines how to expand out from an Anchor object and grab data you want to extract. Methods are available within Field objects.

For the full list of methods available, see [Methods](doc:methods). 



Global parameters for methods
-----

The parameters for a method vary based on the method type (defined in the `id` parameter). Following are the parameters common to all methods:

| Key              | Value                                        | Description                                                  |
| ---------------- | -------------------------------------------- | ------------------------------------------------------------ |
| `id`             |                                              |                                                              |
| tiebreaker       | `first`, `second`, `third`, `last`, `>`, `<` | Which element in the method results is the target. Use the comparisons `>` and `<` to grab maximum and minimum values in the row. By default the comparisons are sorted alphanumerically using [unicode values](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Operators/Less_than).  If you want to compare numeric amounts and ignore non-numbers in the match result,  then add `type: number`  or `type: currency` as a top-level parameter to the field. |
| lineFilters      | Match object                                 | Filters out the matched lines from the method results. A example is if you’re using a box method, and there’s a text footer in the box that you don’t want to capture, or some additional label to the main anchor label that you don't want to capture. |
| wordFilters      | string array                                 | Filters out the matched strings from the method results. A example is if you’re using a box method, and there’s a text footer in the box that you don’t want to capture, or some additional label to the main anchor label that you don't want to capture. |
| whitespaceFilter | `spaces`, `all`                              | Remove extraneous whitespaces. Use `spaces` to remove only extra spaces and `all` to remove all whitespace characters, including new lines and tabs. You can also use a `mergeLines` preprocessor for a similar effect. TODO: verify if this is true. |
| xRangeFilter     | object                                       | This filter allows you to grab **TODO**. <br/>`start` - HorizontalDirection <br/> `offsetX` - inches  <br/> `width` - in inches |



-----

