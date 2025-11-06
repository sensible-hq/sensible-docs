---
title: "draft Linearize"
hidden: true
---



DRAFT

**Note:** This is advanced. for most use cases, see Multicolumn. TODO look up other wordings

Use this preprocessor for documents containing columns of text that the Multicolumn (TODO LINK) preprocessor can't recognize. 

Ensures that Sensible [sort lines](doc:lines#line-sorting) into the specified, coordinate-based blocks,  rather than the default behavior of sorting lines left to right across the page.

[**Parameters**](doc:linearize#parameters)
[**Examples**](doc:linearize#examples)
[**Notes**](doc:linearize#notes)

Parameters
====

| key                    | value                                                        | description                                                  |
| ---------------------- | ------------------------------------------------------------ | ------------------------------------------------------------ |
| type (**required**)    | `linearize`                                                  | *Recognizes multi-column layouts in documents and sorts lines into blocks in whatever or you specify.* |
| match<br/>or<br/>range | [Match](doc:match) object or array of Match objects<br/><br/>or<br/><br/>Range object TODO LINK? | Specifies the matching pages or repeating sections ("ranges") in which to run this preprocessor.<br/>`match`: TODO HOW TO FORMAT?<br/>or<br/>`range`:<br/>See the the Range parameter table, horizontal sections column. TODO REWORD |
| blocks                 | array of objects                                             | TODO: blocks specify BLAH BLAH. Each rectangular block object in the array has the following parameters: TODO which required? To visually determine the following coordinates, click a point in the document in the Sensible app, then drag to display inch dimensions.<br/>TODO: DO NOT mention it messes up section visualization, not worth it`minX`: default: 0 <br/>Specifies the left boundary of the block, in inches from the left edge of the page. <br/>`maxX`: default: 0<br/>Specifies the right boundary of the block, in inches from the left edge of the page. <br/> `minY`: default: page's width in inches<br/>Specifies the top boundary of the block, in inches from the top edge of the page.<br/>`maxY`: default: page's height in inches<br/>Specifies the bottom boundary of the block, in inches from the top edge of the page. |

### LINEARIZE Horizontal Section Range parameters



TODO: figure this out and define it better!!  WITH A NICE PICTURE?



Horizontal sections: repeating stacked blocks of text in a defined range, *which can be discontinous/interrupted by other igored text???*

Vertical sections: columns of text containing repeated text in a defined range, *which doesn't itself repeat and which can't be discontinious??*.f

RANGE contains repeating sections (blocks)



Examples
====

## Example 1

The following example shows TBD.

**Config**

```json
{
  "preprocessors": [
    {
      // todo: show outline of blocks in screenshot markup in docs
      "type": "linearize",
      // page identifier
      "match": "some header text",
      "blocks": [
        {
          /* block 1 */
          "minX": 1,
          "maxX": 4.4,
          "minY": 2.5,
          "maxY": 8.5
        },
        {
          /* block 2 */
          "minX": 4.5,
          // TODO: question
          // these are strict, not like Region I believe; if even a little of a line out of range, it's NOT contained in block
          "minY": 2.5,
          "maxY": 8.5
        },
        {
          /* block 3 */
          "maxY": 2.4
        }
      ]
    }
  ],
  "fields": [
    {
      /* outputs all lines of the document to check block order
         note footer text is excluded since no block coordinates capture it; that text is unavailble for output from SenseML queries */
      "id": "all_lines_in_doc",
      "method": {
        "id": "documentRange",
        "includeAnchor": true
      },
      "anchor": {
        "match": {
          "type": "first"
        }
      }
    }
  ]
}

```

**Example document**
The following image shows the example document used with this example config:

![Click to enlarge](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/images/final/linearize_1.png)

| Example document | [Download link](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/pdfs/linearize_1.pdf) |
| ---------------- | ------------------------------------------------------------ |

**Output**

```json
{
  "all_lines_in_doc": {
    "type": "string",
    "value": "block 1 header block 1 text block 1 end block 2 header block 2 text block 2 end Some header text Block 3 block 3 spans page width"
  }
}
```

## Example 2

The following example shows TBD

**Config**

```json
{
  "preprocessors": [
    {
      "type": "linearize",
      /* linearize columns in repeating sections */
      "range": {
        "anchor": "date",
        "stop": "do not",
        "stopOffsetY": -0.1 // without this,
      },
      /* define two columuar blocks within the repeating ranges 
         so col 1 text preceeds col 2 text
         otherwise, Sensible orders the text in rows across columns
         and the output in the following passthrough field would be 
         jan 2, jan 1, jan 4, jan 3 ... not
         jan 1, jan 2, jan 3, jan 4 ... */
      "blocks": [
        {
          "minX": 0.5,
          "maxX": 4.2
        },
        {
          "minX": 4.21
        }
      ]
    }
  ],
  "fields": [
    {
      "id": "dates_chronological_order",
      "match": "all",
      "anchor": "jan",
      "method": {
        "id": "passthrough"
      }
    },
    {
      "id": "all_lines_in_doc",
      "method": {
        "id": "documentRange",
        "includeAnchor": true
      },
      "anchor": {
        "match": {
          "type": "first"
        }
      }
    }
  ]
}

```

**Example document**
The following image shows the example document used with this example config:





TODO: UPDATE THIS SCREENSHOT ("DO NOT")

![Click to enlarge](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/images/final/linearize_2.png)

| Example document | [Download link](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/pdfs/linearize_2.pdf) |
| ---------------- | ------------------------------------------------------------ |

**Output**

```json
{
  "dates_chronological_order": [
    {
      "type": "string",
      "value": "Jan 1"
    },
    {
      "type": "string",
      "value": "Jan 2"
    },
    {
      "type": "string",
      "value": "Jan 3"
    },
    {
      "type": "string",
      "value": "Jan 4"
    },
    {
      "type": "string",
      "value": "Jan 5"
    },
    {
      "type": "string",
      "value": "Jan 6"
    }
  ],
  "all_lines_in_doc": {
    "type": "string",
    "value": "Do not linearize this text. Phone line 1 data Customer name: Sandy Sanchez Customer account: xxx-xxx-1234 date charge Jan 1 _1 2 3 4 Donʼt linearize this text. Phone line 2 data Customer name: Sam Sanderson Customer account: xxx-xxx-5678 ...continued Jan 2 5 6 7 _8 date charge Jan 3 _9 2 3 4 ...continued Jan 4 5 6 7 _10 Do not linearize this text. Phone line 4 data Customer name: Salma al Saad Customer account: xxx-xxx-9123 date charge Jan 5 _11 2 3 4 ...continued Jan 6 5 6 7 _12"
  }
}
```