---
title: "Label"
hidden: false
---
Return lines near the anchor point.

Examples
-----



The following image shows examples of various labels in the Sensible app: 



![](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/images/v0/label_examples.png)

The preceding example shows fields that do the following:

1. The  `simple_label` field grabs a line below a label.
2. The `one_line_label` field grabs text to the right of a label on the same line, and filters out an unwanted string. 
3. The `hanging_indent_label` field grabs multiple lines of text by using a `stop` parameter.  The method grabs indented lines (`"textAlignment": "hangingIndent"`) , and the match does **not** include lines to the left or right of matching aligned lines. For example, in the PDF, the text "But lines to the left or right aren't matched" gets parsed as a separate line because of the horizontal gap between it and its adjacent line. 

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
  ]
}
```



Parameters
-----

**Note:** For the full list of parameters available for this method, see [Global parameters for methods](doc:method-object#section-global-parameters-for-methods). The following table only shows parameters most relevant to or specific to this method.

| Key                     | Value                                                        | Description                                                  |
| ----------------------- | ------------------------------------------------------------ | ------------------------------------------------------------ |
| id (**required**)       | `label`                                                      |                                                              |
| position (**required**) | a Direction object (`above`, `below`, `left`, `right`)       | What direction the target data is relative to the anchor point. |
| stop                    | `first`, `gap`, or a Match object. Default: `first`          | Use with  `"position": "below"`, `"position": "left"` and `"position": "right"`.  <br/>This parameter allows you to grab multiple lines following a Label, rather than the default first line.  When you specify this parameter, this method matches the first line in the specified position relative to the anchor, and then continues down the page until it meets the specified `stop`.  The multiple matched lines include those that are aligned to the left edge of the first matching line, unless you define a different alignment method using `textAlignment`. The match does **not** include lines that are positioned to the left or right of matching lines. For `gap` , this method stops when it reaches a vertical gap of 0.2 inches, and for a Match object, this method stops when it reaches a matching line. |
| textAlignment           | HorizontalDirection: `left`, `right`, or `hangingIndent`. Default: `left`. | Only applies to `"position": "below"` or `"position": "above"`. <br/>Determines whether to match lines vertically aligned to the anchor at the `left` edge or the `right` edge of the anchor boundary. <br/> `hangingIndent` only applies to  `"position": "below"`.  The top of the boundary of the hangingIndent candidate needs to be within 0.3 inches of the bottom of the boundary of the matching anchor line.  There is no restriction on the x-axis for the hangingIndent. |
| includeAnchor           | boolean. default: `false`                                    | Whether to include the anchor line in the method output. For horizontal matching (`position: left` or `position: right`) the method returns the remainder of the anchor line if its final `Matcher` didn't match the full line. For example, if the anchor line is "Premium: $500" and the `Matcher` is `{ "type": "startsWith", "text": "Premium: " }`, `label` returns "$500". |



