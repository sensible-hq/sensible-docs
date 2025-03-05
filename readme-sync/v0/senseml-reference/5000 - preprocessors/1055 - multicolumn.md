---
title: "Multicolumn"
hidden: true
---

*TODO -*

 *contrast this to:*

- *x range filter*
- *document range*
- *paragraph*
- *readingOrderLeftToRight (? test how it works...shouldn't have an effect)*

*ohh! Add a MULTIMODAL QUERY FOR THE CHARTS!!!*



Use this preprocessor for documents containing columns of text. Ensures that Sensible recognizes column layouts rather than [sorting lines](doc:lines#line-sorting) across the page left-to-right in a way that spans/ignores columns.



[**Parameters**](doc:multicolumn#parameters)
[**Examples**](doc:multicolumn#examples)
[**Notes**](doc:multicolumn#notes)

Parameters
====

| key                 | value              | description                                    |
| ------------------- | ------------------ | ---------------------------------------------- |
| type (**required**) | `multicolumn`      | Recognizes multi-column layouts in documents   |
| minGap              | number. default: 1 | Configures detecting the gaps between columns. |

Configures column recognition by specifying the smallest allowed width of the gutters separating the columns. For an example, see [Table grid example](doc:sections-example-table-grid). Use when text in a column contains whitespace gaps such that Sensible can split one column into two. To avoid this split, set a minimum gap that's larger than the gaps inside the column. The default (0) means that zero-width vertical lines define the column boundaries.



By default, Sensible detects paragraph breaks when the vertical gap between two lines is larger than 40% of the font height of the output line. Use this parameter to change the percentage

If true, Sensible detects table cells containing multiple lines, rather than the default of treating each line as a new row. In detail, Sensible detects that a cell contains multiple lines if the vertical gap between two lines is less than half the height of the second line.<br/>Set this to false if row gutters are narrow. For example, if vertical gaps between lines in the cells are the same height as row gutters, Sensible can incorrectly merge multiple rows into one.

Examples
====

- points to make:
  - pages w 3, 2, and no columns
  - incomplete (in senseml) extract so yeah you should get back incopmlete answer in confidence signasl
  - add in some multimodal examples!! and then link out to them from the Query Group??? ohh, could i add in conditional execution too??
  - `https://dev.sensible.so/editor/instruct/?d=frances_playground&c=multicolumn_preprocessor&g=multicolumn___google_docs`

The following example shows TBD

**Config**

```json
```

**Example document**
The following image shows the example document used with this example config:

![Click to enlarge](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/images/final/TB_D.png)

| Example document | [Download link](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/pdfs/TB_D.pdf) |
| ---------------- | ------------------------------------------------------------ |

**Output**

```json
```
