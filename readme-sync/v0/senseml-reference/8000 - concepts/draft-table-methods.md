---
title: "Choosing a Table method"
hidden: true
---

You can choose from among the following options for extracting tables, depending on your needs:

### Overview of table methods

| method      | based on | description                                                  | comments                                                   |
| ----------- | -------- | ------------------------------------------------------------ | ---------------------------------------------------------- |
| NLP Table   | LLMs     | Extracts a table based on your natural-language description of the data you want to extract. | Low code, doesn't require an anchor. Slowest table method. |
| Table       | layout   | Extracts tables based on bag-of-words scoring.               | For tables that have variable column formatting.           |
| Fixed Table | layout   | Extracts tables with a fixed number and layout of columns.   | Faster than Table.                                         |
| Text Table  | layout   | Extracts tables based on column coordinates in inches.       | Fastest table method, relies solely on text alignment.     |

### Features supported

| method      | multiple pages                                               | merged cells                                                 | variable column formatting | checkboxes in cells                                          | Tables-in tables, labeled rows, and other complex formatting |
| ----------- | ------------------------------------------------------------ | ------------------------------------------------------------ | -------------------------- | ------------------------------------------------------------ | ------------------------------------------------------------ |
| Table       | ✅<br/>Can extract tables that span multiple pages if the column headings repeat on each page. | ✅ <br />If you specify a Table Stop, Sensible populates "empty" spanned cells with the spanned value. For an example, see [Merged cell example](doc:table#example-merged-cells). | ✅                          | ✅ <br />If you specify a Table Stop, Sensible returns Boolean values for checkboxes. | ❌<br/>Use Sections as an alternative                         |
| Fixed Table | ✅<br />Ignores repeating column headings.                    | ✅<br /> If you specify a Table Stop, same behavior as for Table method. | ❌                          | ✅ <br />If you specify a Table Stop, same behavior as for Table method. | ❌<br/>Use Sections as an alternative                         |
| Text Table  | ❌ (?TODO check)                                              | ❌<br/>Sensible returns the first merged cell's value, and returns subsequent spanned cells as nulls. | ❌                          | ❌                                                            | ❌<br/>Use Sections as an alternative                         |
| NLP Table   | ✅ <br />To troubleshoot intervening non-table text, use the Page Span Threshold parameter. | Indeterminate                                                | ✅                          | Indeterminate                                                | Indeterminate.<br/>Use Sections as an alternative            |





### Table

Extracts tables based on bag-of-words scoring and returns their collated column contents. Anchor either on the table title or on a table column heading.

Use the Table method for tables that have variable column formatting. This method can extract tables that span multiple pages if the column headings repeat on each page.

If tables always have the same column layout (same column headings in the same order, same number of columns), use the [Fixed Table method](https://docs.sensible.so/docs/fixed-table) instead.

To extract complex tables, for example tables inside tables or tables with labeled rows and columns, see [Sections](https://docs.sensible.so/docs/sections#examples).

- TODO MERGED CELLS:



![Click to enlarge](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/images/final/table_merged_cells.png)



### Fixed Table

Extracts tables with a fixed number of columns and returns their collated column contents. Anchor either on the table title or on a table column heading.

Use the Fixed Table method for tables in the same document type that always have the same column layout (same headings in the same order, same number of columns). This method can extract tables that span multiple pages and ignores repeated column titles on subsequent pages.

### Text Table

Matches tables based on coordinates in inches and returns their collated column contents. Anchor on the table title, or use a negative Offset Y parameter to enable anchoring on a column heading.

This method's advantages are:

- It's faster than other Table methods because it doesn't use table recognition.
- It can extract unusally formatted tables that other Table methods can't recognize.

Its disadvantage is that it's more limited than other table methods, because it relies on line alignment to find the table. 

### NLP Table

Extracts a table based on your natural-language description of the data you want to extract. This method can extract tables that span multiple pages.

**Advantages**

- Low code.
- Can reformat or filter extracted column data based on your natural-language instructions.
- Doesn't require an [anchor](https://docs.sensible.so/docs/anchor).

**Limitations**

- Can have a moderate impact on performance. For more information, see [Optimizing extraction performance](https://docs.sensible.so/docs/performance).
- Suited to tables that have a header row, where each row is a data element. Not suited to tables where the header is in the first column and the columns are data elements.

**Alternatives**

- [Fixed Table](https://docs.sensible.so/docs/fixed-table) or [Text Table](https://docs.sensible.so/docs/text-table) methods.
- To extract complex tables, for example sub-tables inside tables or tables with labeled rows and columns, see [Sections](https://docs.sensible.so/docs/sections#examples).