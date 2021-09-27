---
title: "SenseML reference introduction"
hidden: false
---

 Use SenseML to write "configs" (collection of queries) to extract structured data from documents, for example, auto insurance quotes or home inspection reports.

See the following pages for reference documentation for the SenseML query language:

- [Field query object](doc:field-query-object)
- [Preprocessors](doc:preprocessors)
- [Methods](doc:methods)
- [Configuration settings](doc:configuration-settings)
- [Computed Field methods](doc:computed-field-methods)

Or, to get started quickly, see:

- [Getting Started](doc:quickstart)

Examples
====

For an overview of the elements in the SenseML schema, see the following image of a short config:



![Click to enlarge](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/images/final/senseml_intro.png)

Try out this example in the Sensible app using the following PDF and config:

| Example PDF | [Download link](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/pdfs/split.pdf) |
| ---------------------------- | ------------------------------------------------------------ |

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

This example config has the following elements:

- The **field** `_driver_name_raw` is a query that extracts a driver's name by searching below some matched text (`"position": "below"`). Its ID is the key for the extracted data.  For more information, see [Field query object](doc:field-query-object).
- An **anchor** is matched text that helps narrow down a location in the PDF from which to extract data. In the `"_driver_name_raw"` field, it is simply a string (`"name of driver"`). For information about more complex anchors, see [Anchor object](doc:anchor).
- A **method** defines how to expand out from the anchor and extract data. In this example field, the Label method tells Sensible to extract data that is closely positioned below the anchor. For more information about methods, see [Methods](doc:methods).
- The **preprocessor**, `pageRange`, cuts out irrelevant pages of the PDF. For more information about using preprocessors to clean up PDFs before extracting data, see [Preprocessors](doc:preprocessors).
- The **fingerprint** tells Sensible to preferentially run this config if the PDF contains the terms "anyco" or "quoted coverage changes".  For more information about using fingerprints to improve performance, and other configuration settings, see [Configuration Settings](doc:configuration-settings).
- The **computed field** `"driver_name_last"` extracts the last name from the raw output of the `_driver_name_raw` field. For more information about transforming field output, see [Computed field methods](doc:computed-field-methods).



The output of this example config is just the name of the driver:

```json
{
    "_driver_name_raw": {
        "type": "string",
        "value": "Petrov, Petar"
    },
    "driver_name_last":{
        "type": "string",
        "value": "Petrov"
    }
}
```



  In production scenarios, you can extract just about any text, as well as image coordinates, from a PDF. Happy extracting! 

