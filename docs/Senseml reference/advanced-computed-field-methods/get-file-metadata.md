---
title: Get file metadata
excerpt: Extract file metadata
deprecated: false
hidden: false
metadata:
  title: ''
  description: 'Extract file metadata'
  robots: index
next:
  description: ''
---
Gets metadata about the document file.

# Parameters

The following parameters are in the computed field's [global Method](doc:computed-field-methods#parameters) parameter: 

| key               | value                                      | description                                                  |
| :---------------- | :----------------------------------------- | :----------------------------------------------------------- |
| id (**required**) | `getFileMetadata`                          |                                                              |
| type              | `filename`,<br/>`contentType`, `pageCount` | If you specify `filename`, outputs the document's filename without the file extension. Sensible gets the filename from the Document Name parameter if you extract through the Sensible API or SDKs, or assigns a document name on upload if you use the Sensible app.<br/>If you specify `contentType`, outputs the document's MIME content type, for example, `image/jpeg` or `application/pdf`.<br/>If you specify `pageCount`, outputs the page count of the document. If the document is part of a [portfolio](doc:portfolio) extraction, outputs the page count of the sub-document in the portfolio. |

# Examples

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

**Example document**\
The following image shows the example document used with this example config:

![Click to enlarge](https://raw.githubusercontent.com/sensible-hq/sensible-docs/v0/assets/images/final/ui_get_file_metadata.png)

| Example document | [Download link](https://raw.githubusercontent.com/sensible-hq/sensible-docs/v0/assets/pdfs/utility_statement_gas_dec_2019.pdf) |
| ---------------- | ----------------------------------------------------------------------------------------------------------------------------------------------- |

**Output**

```json
{
  "doc_filename": {
    "value": "utility_statement_gas_dec_2019",
    "type": "string"
  }
}
```
