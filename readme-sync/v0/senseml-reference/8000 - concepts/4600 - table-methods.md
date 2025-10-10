---
title: "Table methods"
hidden: false
---

You can choose from among the following options for extracting tables:

### Overview of table methods

| method      | based on | description                                                  | comments                                                   |
| ----------- | -------- | ------------------------------------------------------------ | ---------------------------------------------------------- |
| NLP Table   | large language models (LLM)s     | Extracts a table based on your prompt to an LLM. | Low code, doesn't require an anchor. Slowest table method. |
| Fixed Table | layout   | Extracts tables with a fixed number and layout of columns.   | Faster than NLP Table method.                              |
| Text Table  | layout   | Extracts tables based on column coordinates in inches.       | Fastest table method.                                      |

### Features supported

| method      | multiple pages                                               | merged cells                                                 | variable column formatting | checkboxes in cells                                          | Tables-in tables, labeled rows, and other complex formatting |
| ----------- | ------------------------------------------------------------ | ------------------------------------------------------------ | -------------------------- | ------------------------------------------------------------ | ------------------------------------------------------------ |
| Fixed Table | ✅<br />Omits repeating column headings from output.<sup>1</sup> | ✅<br /> If you specify the Stop parameter, Sensible populates "empty" spanned cells with the spanned value. For an example, see [Merged cell example](doc:fixed-table#example-merged-cells). | ❌                          | ✅ <br />If you specify the Stop parameter, Sensible returns the selection status for checkboxes in table cells as `"[true]"` or `"[false]"`. | ❌<br/>Use Sections as an alternative                         |
| Text Table  | ✅<br />Supported if you specify the Stop parameter.<br/>Omits repeating column headings from output.<sup>1</sup> | ❌<br/>Sensible returns the first merged cell's value, and returns subsequent spanned cells as nulls. | ❌                          | ❌                                                            | ❌<br/>Use Sections as an alternative                         |
| NLP Table   | ✅ <br />To troubleshoot intervening non-table text, use the Page Span Threshold parameter. | Indeterminate. Usually supported without additional prompting. | ✅                          | Indeterminate.                                               | Indeterminate.<br/>Use Sections as an alternative.           |

### Notes

1.  For multi-page tables, the Text Table and Fixed Table methods omit any rows that precede repeated column headings after the first page. To prevent Sensible from omitting these rows, use the Text Table's Y Offset parameter to ensure the first row of table data is one that doesn't repeat in the table. For example, use a negative Y Offset parameter value to capture the table's title as the first row.
2. The Table method is deprecated. To duplicate this method's function, use the [NLP Table](doc:nlp-table) method and set the Rewrite Table parameter to false. For information about the Table method, see [(Deprecated) Table method](doc:deprecated-table).
3. For large spreadsheets that contain tens of thousands of rows, use [Cell Rows](doc:cell-rows) as an alternative to table or section methods.
