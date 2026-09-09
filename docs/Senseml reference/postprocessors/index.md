---
title: Postprocessors
excerpt: Transform extracted data into a custom output schema
deprecated: false
hidden: false
metadata:
  title: ''
  description: 'Transform extracted data into a custom output schema'
  robots: index
next:
  description: ''
---
Use postprocessors to transform Sensible's `parsed_document` output into a custom schema. Postprocessor output is available in the `postprocessorOutput` object in the API response and in the **Postprocessed** tab in the SenseML editor.

Postprocessor output isn't available in [Excel output](doc:excel-reference).

| Postprocessor | Description |
| --- | --- |
| **[JsonLogic](doc:jsonlogic-postprocessor)** | Transform extracted data into an arbitrary output schema using [JsonLogic](doc:jsonlogic) operations. |
| **[XML](doc:xml-postprocessor)** | Transform extracted data into an XML document. |
