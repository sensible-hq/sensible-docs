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
- [Sections](doc:sections)

Or, for a getting started tutorial, see:

- [Getting Started](doc:getting-started)

Examples
====

For an overview, see the following example of a short config:

![Click to enlarge](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/images/final/senseml_intro.png)

Try out this example in the Sensible app using the following PDF and config:

| Example PDF | [Download link](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/pdfs/split.pdf) |
| ---------------------------- | ------------------------------------------------------------ |

This example uses the following config:


```json
{
    "fingerprint": { // preferentially run this config if doc contains the test strings
        "tests": [ 
            "anyco",
            "quoted coverage changes"
        ]
    },
    "preprocessors": [{
        "type": "pageRange", // cuts out irrelevant doc pages before extraction
        "startPage": 0,
        "endPage": 2
    }],
    "fields": [{
        "id": "_driver_name_raw", // ID for extracted target data
        "anchor": "name of driver", // search for target data near text "name of driver" in doc
        "method": {
          "id": "label", // target to extract is a single line near anchor line
          "position": "below" // target is below anchor line
        }
    }],
    "computed_fields": [{ // target data is a transformation of already extracted data
            "id": "driver_name_last", // ID for transformed target data
            "method": {
                "source_id": "_driver_name_raw", // extracted data to transform
                "id": "split", // target data is substring in extracted data 
                "separator": ", ", // use commas to split the extracted data into substring array 
                "index": 1 // target is 2nd element in substring array
            }
        }

    ]
}
```

This example config has the following elements:

- The **field** `_driver_name_raw` is a query that extracts a driver's name by searching below some matched text (`"position": "below"`). Its ID is the key for the extracted data. For more information, see [Field query object](doc:field-query-object).
- An **anchor** is matched text that helps narrow down a location in the document from which to extract data. In the `"_driver_name_raw"` field, Sensible matches a string (`"name of driver"`). For information about more complex anchors, see [Anchor object](doc:anchor).
- A **method** defines how to expand out from the anchor and extract data. In this example field, the Label method tells Sensible to extract data that's below and close to the anchor. For more information about methods, see [Methods](doc:methods).
- The **preprocessor**, `pageRange`, cuts out irrelevant pages of the document. For more information about using preprocessors to clean up documents before extracting data, see [Preprocessors](doc:preprocessors).
- The **fingerprint** tells Sensible to preferentially run this config if the document contains the terms "anyco" or "quoted coverage changes." For more information about using fingerprints to improve performance, and other configuration settings, see [Configuration Settings](doc:configuration-settings).
- The **computed field** `"driver_name_last"` extracts the last name from the raw output of the `_driver_name_raw` field. For more information about transforming field output, see [Computed field methods](doc:computed-field-methods).  You can also capture the full name as typed output. See [types](doc:types).



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

  In production scenarios, you can extract just about any text, as well as image coordinates, from a document. Happy extracting! 

