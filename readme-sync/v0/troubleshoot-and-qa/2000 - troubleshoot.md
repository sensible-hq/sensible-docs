---
title: "Troubleshoot"
hidden: false
---

Sensible offers you several ways to troubleshoot your configs and extractions.

API logging levels
----

To troubleshoot extractions in API responses, you can add a verbosity level to a config. For more information, see [verbosity](doc:verbosity).


Inspect extracted text
-----

Sometimes, the text you see in the rendered PDF doesn't match the direct text extraction. To inspect all the text Sensible extracted from a document, use the following config:

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

Inspect lines and fields
----

You can inspect a line to see:

- the extracted text (this text might not match the text in the rendered PDF)
- dimensions of the line boundaries
- which fields interact with that line:

![Click to enlarge](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/images/final/line_details.png)

Inspect SenseML
-----

The Sensible app visually represents SenseML queries in rendered PDFs using colored symbols. For more information, see [UI guide](doc:ui-guide).

Lint SenseML
----

The SenseML pane has a built-in linter for both JSON and the SenseML model. If you see a warning about  invalid JSON, then hover over the red-underlined JSON to see an error message:

![Click to enlarge](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/images/final/linter_SenseML.png)

You can also use the linter to autocomplete parameters.



