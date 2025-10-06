---
title: "Label"
hidden: false

---

Extracts lines or parts of lines proximate to the anchor point. This method is sensitive to line spacing. 

[**Parameters**](doc:label#parameters)
[**Examples**](doc:label#examples)

Parameters
====

**Note:** For additional parameters available for this method, see [Global parameters for methods](doc:method#global-parameters-for-methods). The following table shows parameters most relevant to or specific to this method.

| Key                     | Value                                                 | Description                                                  |
| ----------------------- | ----------------------------------------------------- | ------------------------------------------------------------ |
| id (**required**)       | `label`                                               | The gap between the borders of the target line and the anchor line must be 0.2 inches or less. |
| position (**required**) | `above`, `below`, `left`, `right`                     | Specifies the direction of the target data relative to the anchor point. <br/>For matching text above or below, by default the left boundary of the target line must align with the left boundary of the anchor line. If it's not aligned, then configure the Text Alignment parameter. <br/>For matching text to the left or right, this method returns the rest of the anchor line. For example, if the anchor line is <br/>`Comprehensive premium:$500` <br/>you can anchor on `"comprehensive premium:"` and return `$500` using`"position": "right"`. |
| stop                    | `first`, `gap`, or a Match object. default: `first`   | Use with  `"position": "below"`. <br/>Specifies to extract consecutive lines succeeding a label, rather than the default first line. <br/>For `gap` ,  the gaps between consecutive lines must be 0.1 inches or less. The method stops when it reaches a vertical gap of 0.2 inches between line boundaries.<br/>For a Match object, this method stops when it reaches a matching line.<br/>.<br/>When you specify this parameter, this method:<br/>1. Matches the first target line.<br/> 2. Continues down the page matching lines aligned to the left boundary of the first matching line, unless you define a different alignment using the Text Alignment parameter. It does **not** match lines positioned to the left or right of matching lines.<br/>3. Stops matching when it finds the specified stop. SenseML doesn't include the line that matches the Stop parameter in the output.<br/><br/>You can use the Tiebreaker parameter in combination with the Stop parameter to target a single nonconsecutive line after a label. |
| textAlignment           | `left`, `right`, or `hangingIndent`. default: `left`. | Use with `"position": "below"` or `"position": "above"`. <br/>Matches lines that align to either the left or right boundaries of the anchor line. <br/> `hangingIndent` applies to  `"position": "below"`.  The vertical gap separating the anchor's and the first indented line's boundaries must be 0.3 inches or less. There are no restrictions in inches for the width of the indent. |
| includeAnchor           | boolean. default: `false`                             | Specifies whether to include the anchor text in the output. The text can be a partial line.  |

Examples
====

The following example shows various labels:

1. The  `simple_label` field extracts a line below a label.
2. The `one_line_label` field extracts text to the right of a label on the same line, and filters out an unwanted string. 
3. The `hanging_indent_label` field extracts consecutive lines of text by using a Stop parameter. The method extracts indented lines (`"textAlignment": "hangingIndent"`) , and the match does **not** include lines to the left or right of matching aligned lines. 
4. The `only_looks_like_a_label` field returns `null` because labels don't work for lines separated by more than 0.2 inches.

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
            "text": "a label can be in one line:"
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
        "position": "below"
      }
    }
  ]
}
```

**Example document**

The following image shows the example document used with this example config:

![Click to enlarge](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/images/final/labels.png)

| Example document | [Download link](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/pdfs/label.pdf) |
| ---------------------------- | ------------------------------------------------------------------------------------------------------------------------------ |


**Output**

```json
{
  "simple_label": {
    "type": "string",
    "value": "And here’s the text below it that we want to grab"
  },
  "one_line_label": {
    "type": "string",
    "value": "grab this text"
  },
  "hanging_indent_label": {
    "type": "string",
    "value": "It’s also called a second-line indent or a negative indent. Multiple lines of text can be indented under the first line of the hanging indent."
  },
  "only_looks_like_a_label": null
}
```

