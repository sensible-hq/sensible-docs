---
title: "Choosing a Table method"
hidden: false
---

You can choose from among the following options for extracting tables:

### Overview of table methods

| method      | based on | description                                                  | comments                                                   |
| ----------- | -------- | ------------------------------------------------------------ | ---------------------------------------------------------- |
| NLP Table   | LLMs     | Extracts a table based on your natural-language description of the data you want to extract. | Low code, doesn't require an anchor. Slowest table method. |
| Table       | layout   | Extracts tables based on bag-of-words scoring.               | For tables that have variable column formatting.           |
| Fixed Table | layout   | Extracts tables with a fixed number and layout of columns.   | Faster than Table method.                                  |
| Text Table  | layout   | Extracts tables based on column coordinates in inches.       | Fastest table method.                                      |

### Features supported

| method      | multiple pages                                               | merged cells                                                 | variable column formatting | checkboxes in cells                                          | Tables-in tables, labeled rows, and other complex formatting |
| ----------- | ------------------------------------------------------------ | ------------------------------------------------------------ | -------------------------- | ------------------------------------------------------------ | ------------------------------------------------------------ |
| Table       | ✅<br/>Can extract tables that span multiple pages if the column headings repeat on each page. | ✅ <br />If you specify the Stop parameter, Sensible populates "empty" spanned cells with the spanned value. For an example, see [Merged cell example](doc:table#example-merged-cells). | ✅                          | ✅ <br />If you specify the Stop parameter, Sensible returns the selection status for checkboxes in table cells as `"[true]"` or `"[false]"`. | ❌<br/>Use Sections as an alternative                         |
| Fixed Table | ✅<br />Ignores repeating column headings.                    | ✅<br /> If you specify the Stop parameter, same behavior as for Table method. | ❌                          | ✅ <br />If you specify the Stop parameter, same behavior as for Table method. | ❌<br/>Use Sections as an alternative                         |
| Text Table  | ✅<br />Supported if you specify the Stop parameter           | ❌<br/>Sensible returns the first merged cell's value, and returns subsequent spanned cells as nulls. | ❌                          | ❌                                                            | ❌<br/>Use Sections as an alternative                         |
| NLP Table   | ✅ <br />To troubleshoot intervening non-table text, use the Page Span Threshold parameter. | Indeterminate. Usually supported without additional prompting. | ✅                          | Indeterminate. Try prompting the LLM with an instruction such as `"return [true] for selected checkboxes and [false] for unselected checkboxes"`. | Indeterminate.<br/>Use Sections as an alternative.           |