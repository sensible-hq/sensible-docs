---
title: "SenseML reference introduction"
hidden: false
---

The following pages document the schema for the SenseML query language.

- [Field query object](doc:field-query-object)
- [Preprocessors](doc:preprocessors)
- [Methods](doc:methods)
- [Configuration settings](doc:configuration-settings)
- [Computed Field methods](doc:computed-field-methods)



| Object                  | type    |
| ----------------------- | ------- |
| Field query object      | array   |
| preprocessors           | array   |
| Computed Fields         | array   |
| Configuration Settings: | object  |
| - fingerprint           |         |
| -  verbosity            | integer |
| - ocr_level             | integer |
| - shared_anchor_matches | array   |



Examples
====

Use SenseML to write "configs" (a collection of queries) to extract structured data from an document type, for example, auto insurance quotes or home inspection reports. The following image shows a very simple config:

![](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/images/senseml_intro_example.png)

This example uses the following config:

```json
{
  "fingerprint": {
    "tests":[
      "anyco",
      "quoted coverage changes"
    ],
  },
  "preprocessors": [
    {
      "type": "pageRange",
      "startPage": 0,
      "endPage": 2
    }
  ],
  "fields": [
    {
      "id": "_driver_name_raw",
      "anchor": "name of driver",
      "method": {
        "id": "label",
        "position": "below"
      }
    }
  ],
  "computed_fields": [
    {
      "id": "driver_name_last",
      "method": {
        "id": "split",
        "source_id": "_driver_name_raw",
        "separator": ", ",
        "index": 1
      }
    },

  ],
}
```

- The [field](doc:field-query-object) `_driver_name_raw` is a query that finds a driver's name in the quote based on grabbing data below some matched text. It contains an anchor and a method: 
  - The anchor is matched text that helps narrow down a location in the PDF from which to extract data. In this example it is simply a string in this case:  (`"name of driver"`). For more information about complex anchors, see [Anchor object](doc:anchor-object).
  - The method, or way to grab the data, is a Label. The method tells Sensible that the anchor text is a label for the data to grab, and it is below the label. For more information about methods, see [Methods](doc:methods).
  
- The preprocessor cuts out irrelevant pages of the PDF. For more information about using preprocessors to clean up PDFs before extracting data, see [Preprocessors](doc:preprocessors)

- The fingerprint tells Sensible to run this config if the PDF contains the terms "anyco" or "quoted coverage changes".  For more information about using fingerprints to improve performance, and other configuration settings, see [Configuration Settings](doc:configuration-settings).

- The Computed Field `"driver_name_last"` takes the raw output of the `_driver_name_raw` and extracts the last name from that output. For more information about transforming field output, see [Computed field methods](doc:computed-field-methods).

  
