---
title: "drafts"
hidden: true
---

## Repeat match


Matches the nth consecutive occurrence of a string.

**Parameters**

| key                  | values   | description                                                  |
| -------------------- | -------- | ------------------------------------------------------------ |
| type (**required**)  | `repeat` |                                                              |
| times (**required**) | integer  | Number of times the string must consecutively occur. TODO: how to say it must be startsWith |

**Example**

```json
{
    "type": "repeat",
    "times": 5,
    "match": {
        "type": "startsWith",
        "text": "Value:"
    }
}
```



expands to:

```json
[
          { "type": "startsWith", "text": "Value:" },
          { "type": "startsWith", "text": "Value:" },
          { "type": "startsWith", "text": "Value:" },
          { "type": "startsWith", "text": "Value:" },
          { "type": "startsWith", "text": "Value:" }
]
```



https://dev.sensible.so/editor/?d=frances_playground&c=repeat_matcher&g=repeat&om=2



![image-20250804115220053](C:\Users\franc\AppData\Roaming\Typora\typora-user-images\image-20250804115220053.png)



## detect



|                           |                                               |                                                              |
| ------------------------- | --------------------------------------------- | ------------------------------------------------------------ |
| detectMultipleLinesPerRow | boolean<br/>or<br/>object<br/> default: false | If true, Sensible detects table cells containing multiple lines, rather than the default of treating each line as a new row. In detail, Sensible detects that a cell contains multiple lines if the vertical gap between two lines is less than half the height of the second line.<br/>Set this to false if row gutters are narrow. For example, if vertical gaps between lines in the cells are the same height as row gutters, Sensible can incorrectly merge multiple rows into one.<br/><br/>To configure the vertical gap, you can set `"detectMultipleLinesPerRow": {"maxGap": /* fraction_of_inches */ } `. If configured, Sensible considers multiple lines to belong to the same cell if the vertical gap between each line in the cell is less than or equal to the specified number in inches. Configure this parameter to account for varying font sizes in a multi-line cell. Make sure that the gap you specify is smaller than the vertical gap between rows. Specify the maxiumum allowable vertical gap between newlines in a cell; above that threshold, Sensible identifies a vertical gap as seprating rows from each other than than newlines in a single cell. TODO: "line" could mean sensible-specific or it could mean newline; specify it means NEWLINES. |
|                           |                                               |                                                              |
|                           |                                               |                                                              |

**EXAMPLE**

TODO: make it into a footnote for the smaller font?

https://dev.sensible.so/editor/?d=frances_playground&c=text_table_multi_gap&g=multicolumn&om=2 

![image-20250804113716033](C:\Users\franc\AppData\Roaming\Typora\typora-user-images\image-20250804113716033.png)
