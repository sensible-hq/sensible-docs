---
title: "Label"
hidden: false

---

Extracts lines or parts of lines proximate to the anchor point. This method is sensitive to font sizes and line spacing. 

[**Parameters**](doc:label#section-parameters)
[**Examples**](doc:label#section-examples)

Parameters
====

**Note:** For the full list of parameters available for this method, see [Global parameters for methods](doc:method#section-global-parameters-for-methods). The following table only shows parameters most relevant to or specific to this method.

| Key                     | Value                                                 | Description                                                  |
| ----------------------- | ----------------------------------------------------- | ------------------------------------------------------------ |
| id (**required**)       | `label`                                               |                                                              |
| position (**required**) | `above`, `below`, `left`, `right`                     | Specifies the direction of the target data relative to the anchor point. <br>For matching text above or below, by default the left boundary of the target line must be aligned with the left boundary of the anchor line. If it is not aligned, then configure the Text Alignment parameter. <br/>For matching text to the left or right, this method returns the remainder of the anchor line. For example, if the anchor line is <br/>`"Comprehensive premium:$500"` <br/>and the anchor's Match object is<br/> `{ "type": "includes", "text": "premium:" }`<br/> The Label method returns `"$500"` for `"position": "right"`. |
| stop                    | `first`, `gap`, or a Match object. default: `first`   | Use with  `"position": "below"`.  <br/>Specifies to extract multiple lines following a label, rather than the default first line. <br/>For `gap` , this method stops when it reaches a vertical gap of 0.2 inches between line boundaries.<br/>For a Match object, this method stops when it reaches a matching line.<br/> <br/>When you specify this parameter, this method:<br/>1. Matches the first target line.<br/> 2. Continues down the page matching lines that are aligned to the left boundary of the first matching line, unless you define a different alignment using the Text Alignment parameter. It does **not** match lines that are positioned to the left or right of matching lines.<br/>3.  Stops matching when it finds the specified stop. SenseML does not include the line that matches the Stop parameter in the output.<br/> |
| textAlignment           | `left`, `right`, or `hangingIndent`. default: `left`. | Use with `"position": "below"` or `"position": "above"`. <br/>Matches lines that align to either the left or right boundaries of the anchor line. <br/> `hangingIndent` only applies to  `"position": "below"`.  The vertical gap separating the anchor's and the first indented line's boundaries must be 0.3 inches or less.  There are no restrictions in inches for the width of the indent. |
| includeAnchor           | boolean. default: `false`                             | Specifies whether to include the anchor text in the output.  |

Examples
====

The following example shows various labels:

1. The  `simple_label` field extracts a line below a label.
2. The `one_line_label` field extracts text to the right of a label on the same line, and filters out an unwanted string. 
3. The `hanging_indent_label` field extracts multiple lines of text by using a Stop parameter.  The method extracts indented lines (`"textAlignment": "hangingIndent"`) , and the match does **not** include lines to the left or right of matching aligned lines. 
4. The `only_looks_like_a_label` field demonstrates that labels are sensitive to font size differences by returning `null`.
5. The `doc_range_alternative` fields shows an alternate way to extract the line targeted by `only_looks_like_a_label`.

**Config**


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

**PDF**

The following image shows the example PDF used with this example config:

![Click to enlarge](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/images/final/label_examples.png)

| Example PDF | [Download link](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/pdfs/label_example.pdf) |
| ---------------------------- | ------------------------------------------------------------------------------------------------------------------------------ |


**Output**

```json
{
  "simple_label": {
    "type": "string",
    "value": "And here’s the text below it that we want to grab"
  },
  "one_line_label": null,
  "hanging_indent_label": {
    "type": "string",
    "value": "It’s also called a second-line indent or a negative indent. Multiple lines of text can be indented under the first line of the hanging indent."
  },
  "only_looks_like_a_label": null,
  "doc_range_alternative": {
    "type": "string",
    "value": "But labels are sensitive to font size (as well as spacing, alignment, etc), so this one happens not to work. Try the Document Range method instead or the Region method."
  }
}
```

