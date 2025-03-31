---
title: "Get file metadata"
hidden: false
---
Gets metadata about the document file.

Parameters
====

The following parameters are in the computed field's [global Method](doc:computed-field-methods#parameters) parameter: 


| key               | value             | description                                                  |
| :---------------- | :---------------- | :----------------------------------------------------------- |
| id (**required**) | `getFileMetadata` |                                                              |
| type              | `filename`        | Copies the document's filename without the file extension to the extraction output. Sensible gets the filename from the Document Name parameter if you extract through the API or SDKs, or assigns a document name on upload if you use the Sensible app. |

Examples
====

The following example shows extracting the filename from the example document.

**Config**

```json
{
  "fields": [
    {
      "id": "doc_filename",
      "method": {
        "id": "getFileMetadata",
        "type": "filename"
      }
    }
  ]
}
```

**Example document**
The following image shows the example document used with this example config:

![Click to enlarge](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/images/final/ui_get_file_metadata.png)

| Example document | [Download link](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/pdfs/utility_statement_gas_dec_2019.pdf) |
| ---------------- | ------------------------------------------------------------ |

**Output**

```json
{
  "doc_filename": {
    "value": "utility_statement_gas_dec_2019",
    "type": "string"
  }
}
```
