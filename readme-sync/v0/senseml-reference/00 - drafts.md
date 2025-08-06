---
title: "drafts"
hidden: true
---



## detect lines



|                           |                                               |                                                              |
| ------------------------- | --------------------------------------------- | ------------------------------------------------------------ |
| detectMultipleLinesPerRow | boolean<br/>or<br/>object<br/> default: false | If true, Sensible detects table cells containing multiple lines, rather than the default of treating each line as a new row. In detail, Sensible detects that a cell contains multiple lines if the vertical gap between two lines is less than half the height of the second line.<br/>Set this to false if row gutters are narrow. For example, if vertical gaps between lines in the cells are the same height as row gutters, Sensible can incorrectly merge multiple rows into one.<br/><br/>To configure the vertical gap, you can set `"detectMultipleLinesPerRow": {"maxGap": /* fraction_of_inches */ } `. If configured, Sensible considers multiple lines to belong to the same cell if the vertical gap between each line in the cell is less than or equal to the specified number in inches. Configure this parameter to account for varying font sizes in a multi-line cell. Make sure that the gap you specify is smaller than the vertical gap between rows. Specify the maxiumum allowable vertical gap between newlines in a cell; above that threshold, Sensible identifies a vertical gap as seprating rows from each other than than newlines in a single cell. TODO: "line" could mean sensible-specific or it could mean newline; specify it means NEWLINES. |
|                           |                                               |                                                              |
|                           |                                               |                                                              |

## Examples

## TBD example

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

