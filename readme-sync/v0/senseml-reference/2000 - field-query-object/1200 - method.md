---
title: "Method object"
hidden: false
---

A Method object defines how to expand out from an Anchor line and extract target data. The following methods are available in Field objects.

For a list of methods, see [Methods](doc:methods). 

[**Parameters**](doc:method#parameters)
[**Examples**](doc:method#examples)

Parameters
-----

The following global parameters available to all methods:

| Key                                                          | Value                                                        | Description                                                  |
| ------------------------------------------------------------ | ------------------------------------------------------------ | ------------------------------------------------------------ |
| `id`                                                         | [box](doc:box),<br/>[checkbox](doc:checkbox),<br/>[column](doc:column),<br/>[documentRange](doc:document-range),<br/>[fixedTable](doc:fixed-table),<br/>[intersection](doc:intersection),<br/> [invoice](doc:invoice),<br/>[keyValue](doc:key-value),<br/>[label](doc:label),<br/>[nearestCheckbox](doc:nearest-checkbox),<br/>[passthrough](doc:passthrough),<br/>[regex](doc:regex),<br/>[region](doc:region),<br/>[row](doc:row),<br/>[signature](doc:signature),<br/>[table](doc:table),<br/>[textTable](doc:text-table)<br/>[topic](doc:topic) | see [Methods](doc:methods).                                  |
| tiebreaker                                                   | integer (zero-based index)<br/> or<br/>ordinal (`first`, `second`, `third`, `last`)<br/>or <br/> comparison (`>`, `<`) | If the method returns multiple elements (for example, a Row method), specifies which element to extract in the returned array. <br/><br/>**integer**: Returns the nth element in the returned array, sorted by Sensible's [default line sorting](doc:lines#line-sorting). For example, 0 returns the first item, -1 returns the last item, -2 returns the second-to-last element in the array.<br/><br/>**ordinal:** Returns the `first`, `second`,`third` or `last` element, sorted by Sensible's [default line sorting](doc:lines#line-sorting).<br/>**comparison:**  Returns the first or last element, sorted [alphanumerically](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Operators#relational_operators)  using unicode values. If you want to compare numeric amounts and ignore non-numbers,  then add a numeric [type](doc:types) such as  `type: currency` as a top-level parameter to the field.<br/><br/> |
| TODO: update for document-range, row, getting started (update with index examples) |                                                              |                                                              |
|                                                              |                                                              |                                                              |
|                                                              |                                                              |                                                              |
|                                                              |                                                              |                                                              |
|                                                              |                                                              |                                                              |
|                                                              |                                                              |                                                              |
|                                                              |                                                              |                                                              |

|  |  |
| ------------------------------ | ------------------------------------------------------------ |

This example uses the following config:

```json

  ]
}
```







