---
title: "drafts"
hidden: true
---



## detect lines



|                           |                                               |                                                              |
| ------------------------- | --------------------------------------------- | ------------------------------------------------------------ |
| detectMultipleLinesPerRow | boolean<br/>or<br/>object<br/> default: false | If true, Sensible detects table cells containing newlines, rather than the default of treating each newline as a new row. In detail, Sensible detects that a cell contains newlines if the vertical gap between two lines is less than half the height of the second line.<br/><br/>To troubleshoot multiline cell recognition, you can configure a Max Gap parameter that specifies the maximum allowable vertical gap in inches between newlines in a cell. For example, use this parameter to account for varying font sizes in a multi-line cell.  Ensure that the gap you specify is smaller than the vertical gaps between rows. For example, if the vertical gaps between rows are 0.3 inches, specify 0.2 inches as follows: <br/> `"detectMultipleLinesPerRow": {"maxGap": 0.2 }`.<br/>For an example, see TODO - LINK TO EXAMPLE ON PUBLISH |
|                           |                                               |                                                              |
|                           |                                               |                                                              |

## Examples

### Example: Troubleshoot newline recognition

The following example shows handling newlines in a cell with varying font sizes using the Max Gap parameter.

**Config**

```json
{
  "fields": [
    {
      "id": "table_test",
      "anchor": {
        "match": {
          "type": "includes",
          "text": "disability"
        }
      },
      "method": {
        "id": "textTable",
        /* ensures small fonts are recognized as 
        belonging to a cell rather than their own row. To determine the numeric value, measure the gap in inches between the small font-line and the larger-font line that succeeds it, and set this value to be a little larger than that gap */
       "detectMultipleLinesPerRow": { "maxGap": 0.2 },
        "stop": "for more details",
        "columns": [
          {
            "id": "col1",
            "minX": 1,
            "maxX": 2.9
          },
          {
            "id": "col2",
            "minX": 2.9,
            "maxX": 5.7
          },
          {
            "id": "col3",
            "minX": 5.7,
            "maxX": 9
          }
        ]
      }
    }
  ]
}

```

**Example document**
The following image shows the example document used with this example config:

![Click to enlarge](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/images/final/TB_D.png)

| Example document | [Download link](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/pdfs/TB_D.pdf) |
| ---------------- | ------------------------------------------------------------ |

**Output**

```json
{
  "table_test": {
    "columns": [
      {
        "id": "col1",
        "values": [
          null,
          {
            "value": "Employee benefit",
            "type": "string"
          },
          {
            "value": "Common carrier",
            "type": "string"
          },
          {
            "value": "Benefit reduction",
            "type": "string"
          }
        ]
      },
      {
        "id": "col2",
        "values": [
          {
            "value": "Employees paid 100k",
            "type": "string"
          },
          {
            "value": "100% of salary, max $100k After a 3 month waiting period",
            "type": "string"
          },
          {
            "value": "Not included",
            "type": "string"
          },
          {
            "value": "See table C. Not adjusted for inflation",
            "type": "string"
          }
        ]
      },
      {
        "id": "col3",
        "values": [
          {
            "value": "All other employees",
            "type": "string"
          },
          {
            "value": "50% of salary, max $50k After a 3 month waiting period",
            "type": "string"
          },
          {
            "value": "Not included",
            "type": "string"
          },
          {
            "value": "See table C. Not adjusted for inflation",
            "type": "string"
          }
        ]
      }
    ]
  }
}
```

