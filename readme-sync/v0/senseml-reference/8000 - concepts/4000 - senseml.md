---
title: "SenseML"
hidden: false
---



*SenseML* is a query language that lets you extract structured data from documents, for example, from PDFs. A field is the basic SenseML query unit for extracting a piece of document data. The output of a field is a JSON key-value pair that structures the extracted data. 

SenseML contains layout-based and large language model (LLM)-based methods.

## Layout-based fields

Here's a simple example of a layout-based field: 

```json
{

  "fields": [
    {
      "id": "name_of_output_key",
      "anchor": "an anchor is some text to match. An anchor can be an array of matches",
      "method": {
        "id": "label",
         "position": "below"
      }
    },
  ]
}
```

The following image shows this example in the Sensible app:

![Click to enlarge](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/images/final/basic_field.png)

As the preceding image shows, here's the output of the example field: 

```json
{
  "name_of_output_key": {
    "type": "string",
    "value": "Below the matching anchor, this is the data to extract. The anchor is a label for this data."
  }
}
```

This example shows the following key concepts:

| key                             | description                                                  |
| ------------------------------- | ------------------------------------------------------------ |
| [field](doc:field-query-object) | A query that extracts data in relationship to matched text. Its ID is the key for the extracted data. In this example,  `name_of_output_key`. |
| **[anchor](doc:anchor)**        | Matched text that helps narrow down a location in the document from which to extract data. In this example, `"an anchor is some text to match..."`. |
| [method](doc:method)            | Defines how to expand out from the anchor and extract data. In this example, the Label method extracts data that's below the anchor (`"position": "below"`). For a list of methods, see [Methods](doc:methods). |



##


 For more information, see the [SenseML introduction](doc:senseml-reference-introduction).