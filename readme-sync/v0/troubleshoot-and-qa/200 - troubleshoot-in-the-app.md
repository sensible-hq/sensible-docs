---
title: "Troubleshoot in the app"
hidden: false
---

 The Sensible app offers you several ways to troubleshoot your config.

Validate SenseML
====
The SenseML pane has a built-in linter for both JSON and the SenseML model. If you see a warning about  invalid JSON, then hover over the red-underlined JSON to see an error message:

![Click to enlarge](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/images/linter_SenseML.png)

You can also use the linter to autocomplete parameters.

Inspect SenseML
====

The Sensible app visually represents SenseML queries in rendered PDFs using colored symbols. For more information, see [UI guide](doc:ui-guide).

Inspect lines and fields
====

You can inspect a line to see:

- the extracted text (this text might not match the text in the rendered PDF)
- dimensions of the line boundaries
- which fields interact with that line:

![Click to enlarge](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/images/line_details_example.png)

Inspect all extracted text
====

Sometimes, the text you see in the rendered PDF does not match the direct text extraction. To inspect all the text Sensible extracted from a document, use the following config:

```json
{  
  "fields": [
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





