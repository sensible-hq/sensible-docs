---
title: "Label"
hidden: false

---

Return text or lines proximate to the anchor point. This method is sensitive to font sizes and line spacing. 

Unlike many other methods (such as Document Range), the Label method can return data that is in the *same* line as the anchor line. You can do so by specifying `position: left` or `position: right` in the Label method.

[**Parameters**](doc:label#section-parameters)
[**Examples**](doc:label#section-examples)

Parameters
====

**Note:** For the full list of parameters available for this method, see [Global parameters for methods](doc:method#section-global-parameters-for-methods). The following table only shows parameters most relevant to or specific to this method.

| Key                     | Value                                                 | Description                                                  |
| ----------------------- | ----------------------------------------------------- | ------------------------------------------------------------ |
| id (**required**)       | `label`                                               |                                                              |
| position (**required**) | `above`, `below`, `left`, `right`                     | What direction the target data is relative to the anchor point. <br> For matching text above or below, by default the left boundary of the target line must be aligned with the left boundary of the anchor line. If it is not aligned, then configure the Text Alignment parameter. <br/>For horizontal matching (`"position": "left"` or `"position": "right"`), this method returns the remainder of the anchor line. For example, if the anchor line is <br/>"Comprehensive premium: $500" <br/>and the anchor's Match object is<br/> `{ "type": "includes", "text": "premium: " }`<br/> The Label method returns "$500" for `"position": "right"`. |
| stop                    | `first`, `gap`, or a Match object. default: `first`   | Use with  `"position": "below"`.  <br/>Specifies to grab multiple lines following a label, rather than the default first line.  When you specify this parameter, this method matches the first line in the specified position relative to the anchor, and then continues down the page until it meets the specified stop.  SenseML does not include the line that matches the Stop parameter in the output.<br/>Only matches lines that are distributed on a y-axis that passes through the left boundary of the first matching line, unless you define a different alignment method using  the Text Alignment parameter. The match does **not** include lines that are positioned to the left or right of matching lines. <br/>For `gap` , this method stops when it reaches a vertical gap of 0.2 inches between line boundaries, and for a Match object, this method stops when it reaches a matching line. |
| textAlignment           | `left`, `right`, or `hangingIndent`. default: `left`. | Only applies to `"position": "below"` or `"position": "above"`. <br/>Determines whether to match lines distributed along an y-axis that passes through either the left or right anchor line boundary. <br/> `hangingIndent` only applies to  `"position": "below"`.  The anchor's and the first indented line's boundaries must be separated by a vertical gap of 0.3 inches or less.  There are no restrictions in inches for the width of the indent. |
| includeAnchor           | boolean. default: `false`                             | Whether to include the anchor text in the output. For example, if you specify a single line using the Starts With and Ends With parameters in a match array in the anchor,  SenseML returns `null` unless you set this parameter to true. |

Examples
====

The following image shows examples of various labels in the Sensible app: 

![](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/images/label_examples.png)

You can try out this example yourself in the Sensible app using the following downloadable PDF and config:

| Example PDF for label method | [Download link](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/pdfs/label_example.pdf) |
| ---------------------------- | ------------------------------------------------------------------------------------------------------------------------------ |

This example uses the following config:

```json
{
  "fields": [
    {
      "id": "simple_label",
      "anchor": "Here is a good candidate",
      "method": {
        "id": "label",
        "position": "below"
      }
    },
    {
      "id": "one_line_label",
      "anchor": {
        "match": [
          {
            "type": "startsWith",
            "text": "A label can be in one line:"
          }
        ]
      },
      "method": {
        "id": "label",
        "position": "right",
        "wordFilters": [
          "but filter out this extra text"
        ]
      }
    },
    {
      "id": "hanging_indent_label",
      "anchor": "Here is the first line of a hanging indent",
      "method": {
        "id": "label",
        "position": "below",
        "textAlignment": "hangingIndent",
        "stop": "gap"
      }
    },
    {
      "id": "only_looks_like_a_label",
      "anchor": "This also looks",
      "method": {
        "id": "label",
        "position": "below",
      }
    },
    {
      "id": "doc_range_alternative",
      "anchor": "This also looks",
      "method": {
        "id": "documentRange",
        "stop": {
          "text": "to work",
          "type": "startsWith"
        }
      }
    },
  ]
}
```


The preceding example shows fields that do the following:

1. The  `simple_label` field grabs a line below a label.
2. The `one_line_label` field grabs text to the right of a label on the same line, and filters out an unwanted string. 
3. The `hanging_indent_label` field grabs multiple lines of text by using a Stop parameter.  The method grabs indented lines (`"textAlignment": "hangingIndent"`) , and the match does **not** include lines to the left or right of matching aligned lines. For example, in the PDF, the line "But lines to the left or right aren't matched" is ignored, because it isn't distributed on the same y-axis as other matching lines. 
4. The `only_looks_like_a_label` field demonstrates that labels are sensitive to font size differences by returning `null`.
5. The `doc_range_alternative` fields shows an alternate way to grab the line targeted by `only_looks_like_a_label`.

