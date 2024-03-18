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

| Key                         | Value                                                        | Description                                                  |
| --------------------------- | ------------------------------------------------------------ | ------------------------------------------------------------ |
| `id`                        | see [Methods](doc:methods) and [Natural-language methods](doc:llm-based-methods). | see [Methods](doc:methods) and [Natural-language methods](doc:llm-based-methods). |
| tiebreaker                  | integer (zero-based index)<br/> or<br/>ordinal (`first`, `second`, `third`, `last`)<br/>or <br/> comparison (`>`, `<`)<br/>or<br/>`join`<br/> Default: `join` | If the method returns multiple elements (for example, a Row method), specifies which element to extract in the returned array. <br/><br/>**integer**: Returns the zero-indexed nth element in the returned lines array, using Sensible's [default line sorting](doc:lines#line-sorting). For example, 0 returns the first line, -1 returns the last line, and -2 returns the second-to-last line in the array.<br/><br/>**ordinal:** Returns the `first`, `second`,`third` or `last` element, using Sensible's [default line sorting](doc:lines#line-sorting).<br/><br/>**comparison:**  Returns the first or last element, sorted [alphanumerically](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Operators#relational_operators)  using Unicode values.<br/> If you want to compare numeric amounts and ignore non-numbers,  then add a numeric [type](doc:types) such as  `type: currency` as a top-level parameter to the field.<br/><br/>**join**: Returns all elements in the returned array as a single string, delimited by whitespaces. |
| lineFilters                 | Match object                                                 | Filters out the specified lines from the method match. For example, if the Box method extracts unwanted footer lines from a box, you can filter out the lines  with this parameter. |
| typeFilters                 | array of [Types](doc:types)                                  | Filters out the specified types from the method results. For example, for a target box containing a delivery date, a street address, and delivery notes, you can filter out the lines containing Date and Address types in order to extract the delivery notes. Note that less strict types, such as Name and Currency types, are less useful in this filter than stricter types such as the Phone Number type.<br/>For an example, see the Examples section. |
| wordFilters                 | string array                                                 | Filters out the specified strings from the method results.   |
| whitespaceFilter            | `spaces`, `all`                                              | Remove extra whitespaces.<br/> `spaces` - remove solely extra spaces.<br/> `all` - remove all whitespace characters, including newlines. |
| xRangeFilter                | object                                                       | Defines left and right boundaries in which to capture lines. For example, in combination with the Document Range method, the X Range Filter parameter defines a "column" that's bounded at the top and bottom by text matches.  This column excludes any lines that partially fall outside the defined rectangular region. Contains the following parameters: <br/>`start` - `right`,`left`  - Defines the starting point of the "column" at either the right or left boundary of the anchor line.<br/> `offsetX` - Adjusts the horizontal position of the starting point defined by the Start parameter. <br/> `width` - The width of the page region to capture, in inches.<br/><br/> For an example, see the Examples section. |
| **(Deprecated)** xMajorSort | boolean                                                      | **Deprecated:** Use the Sort Lines parameter instead.        |
| sortLines                   | `readingOrderLeftToRight`                                    | Set this parameter to `readingOrderLeftToRight` to sort lines whose height and vertical position are misaligned. For example, with misaligned handwritten text, slight jitter in the vertical positions of lines can cause Sensible to incorrectly sort lines that a human reader interprets as following left to right. The Sort Lines parameter corrects this problem by sorting lines by their likely reading order. |

Examples
====

Sort Lines example
----

**PROBLEM**

In the following example, the handwritten text "Nash" is slightly taller than the text "Steve", so Sensible interprets "Nash" as *preceding* "Steve" (reversing the order interpreted by a human reader) and outputs `"Nash Steve"` as the name:

![Click to enlarge](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/images/final/xmajor_sort_1.png)

**SOLUTION**

To reliably capture the first and last name in their left-to-right order,  set `"sortLines": "readingOrderLeftToRight"`.

*Config*

```json
{
  "fields": [
    {
      "id": "_name_joint_owner_raw",
      "match": "last",
      "anchor": {
        "match": {
          "type": "startsWith",
          "text": "Name",
          "isCaseSensitive": true
        }
      },
      "method": {
        "id": "region",
        "sortLines": "readingOrderLeftToRight",
        "start": "left",
        "width": 2.5,
        "height": 0.4,
        "offsetX": 0.2,
        "offsetY": -0.45
      }
    }
  ]
}
```

*Example document*

The following image shows the example document used with this example config:

![Click to enlarge](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/images/final/sort_lines_2.png)

| Example document | [Download link](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/pdfs/xmajor_sort.pdf) |
| ----------- | ------------------------------------------------------------ |

To run this example, verify the document type uses Google OCR (click the gear icon for the Document Type and select **Google**): 

![Click to enlarge](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/images/final/merge_lines_ocr_1.png)

*Output*

```json
{
  "_name_joint_owner_raw": {
    "type": "string",
    "value": "Steve Nash"
  }
}
```

Type Filters example
----

The following example shows using the Type Filters parameter to extract delivery notes from a box.

**Config**

```json
{
  "fields": [
    {
      "id": "delivery_notes",
      "type": "string",
      "anchor": "delivery information",
      "method": {
        "id": "box",
        "offsetY": 1,
        "typeFilters": [
          "address",
          {
            "id": "date",
            "format": "%b_%D_%y"
          }
        ]
      }
    }
  ]
}
```

**Example document**
The following image shows the example document used with this example config:

![Click to enlarge](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/images/final/types_filter.png)

| Example document | [Download link](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/pdfs/types_filter.pdf) |
| ----------- | ------------------------------------------------------------ |

**Output**

```json
{
  "delivery_notes": {
    "type": "string",
    "value": "Please leave package at door"
  }
}
```



X Range Filter example
----

In combination with the Document Range method, the X Range Filter parameter defines a "column" that's bounded at the top and bottom by text.

The following image shows using this parameter to extract a "cell" of text:

![Click to enlarge](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/images/final/xrange_filter.png)



In this example, the X Range Filter parameter is an alternative to:

- The Document Range method without the X Range Filter parameter. Without the parameter, this method extracts unwanted information such as the address of the importer. 
- The Fixed Table method. This method doesn't recognize the table's formatting.

Alternatives to using the X Range Filter parameter in this example include:

- The Text Table method with `"detectMultipleLinesPerRow": true` configured.
- LLM-powered methods, such as the NLP Table method.

Try out this example in the Sensible app using the following document and config:

| Example document | [Download link](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/pdfs/xrange_filter.pdf) |
| ------------------------------ | ------------------------------------------------------------ |

This example uses the following config:

```json
{
  "fields": [
    {
      "id": "mailing_address_supplier",
      "anchor": {
        "match": {
          "text": "supplier",
          "type": "startsWith"
        }
      },
      "method": {
        "id": "documentRange",
        "xRangeFilter": {
          "start": "left",
          "offsetX": -0.5,
          "width": 2
        },
        "stop": {
          "text": "type of business",
          "type": "includes"
        }
      }
    }
  ]
}
```







