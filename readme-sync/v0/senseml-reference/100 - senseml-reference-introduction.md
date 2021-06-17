---
title: "SenseML reference introduction"
hidden: false
---

 Use SenseML to write "configs" (a collection of queries) to extract structured data from an document type, for example, auto insurance quotes or home inspection reports.

See the following pages for reference documentation for the SenseML query language:

- [Field query object](doc:field-query-object)
- [Preprocessors](doc:preprocessors)
- [Methods](doc:methods)
- [Configuration settings](doc:configuration-settings)
- [Computed Field methods](doc:computed-field-methods)

Or, to get started quickly, see our quickstart:

- [Quickstart](doc:quickstart)

Examples
====

For an overview of the elements in the SenseML schema, see the following image of a short config:

![](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/images/senseml_intro_example.png)





You can try out this example yourself in the Sensible app using the following downloadable PDF and config:

| Example SenseML Overview PDF | [Download link](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/pdfs/split_example.pdf) |
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

- The **field** `_driver_name_raw` is a query that finds a driver's name in the quote based on grabbing data below some matched text. It contains an id (which serves as a key for the extracted data), an anchor, and a method.  For more information, see [Field query object](doc:field-query-object)
- The **anchor** is matched text that helps narrow down a location in the PDF from which to extract data. In this example it is simply a string:  (`"name of driver"`). For more information about complex anchors, see [Anchor object](doc:anchor-object).
- The **method**, or way to grab the data, is a Label. The method tells Sensible that the anchor text is a label for the data to grab, and it is below the label. For more information about methods, see [Methods](doc:methods).
- The **preprocessor** cuts out irrelevant pages of the PDF. For more information about using preprocessors to clean up PDFs before extracting data, see [Preprocessors](doc:preprocessors).
- The **fingerprint** tells Sensible to preferentially run this config if the PDF contains the terms "anyco" or "quoted coverage changes".  For more information about using fingerprints to improve performance, and other configuration settings, see [Configuration Settings](doc:configuration-settings).
- The **computed field** `"driver_name_last"` takes the raw output of the `_driver_name_raw` and extracts the last name from that output. For more information about transforming field output, see [Computed field methods](doc:computed-field-methods).

The output of this example config is just one key/value pair: the last name of the driver.  In production scenarios, you can extract just about any text, as well as image coordinates, from a PDF as structured data. As a next step, check out our [Quickstart](doc:quickstart), or see the topics in this SenseML reference. Happy extracting! 

