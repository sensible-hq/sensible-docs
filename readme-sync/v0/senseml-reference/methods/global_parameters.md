---
title: "Global parameters for methods"
hidden: true
---
The following parameters are valid for all methods.



Global parameters for methods
-----

| Key              | Value                                        | Description                                                  |
| ---------------- | -------------------------------------------- | ------------------------------------------------------------ |
| tiebreaker       | `first`, `second`, `third`, `last`, `>`, `<` | Which element in the method results is the target. Use the comparisons `>` and `<` to grab maximum and minimum values in the row. By default the comparisons are sorted alphanumerically using [unicode values](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Operators/Less_than).  If you want to compare numeric amounts and ignore non-numbers in the match result,  then add `type: number`  or `type: currency` as a top-level parameter to the field. |
| lineFilters      | Match object                                 | Filters out the matched lines from the method results. A example is if you’re using a box method, and there’s a text footer in the box that you don’t want to capture, or some additional label to the main anchor label that you don't want to capture. |
| wordFilters      | string array                                 | Filters out the matched strings from the method results. A example is if you’re using a box method, and there’s a text footer in the box that you don’t want to capture, or some additional label to the main anchor label that you don't want to capture. |
| whitespaceFilter | `spaces`, `all`                              | Remove extraneous whitespaces. Use `spaces` to remove only extra spaces and `all` to remove all whitespace characters, including new lines and tabs. You can also use a `mergeLines` preprocessor for a similar effect. TODO: verify if this is true. |

Examples
----




Notes
-----