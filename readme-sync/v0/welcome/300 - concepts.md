---
title: "concepts"
hidden: true
---

SenseML is a query language powered by ML and other techniques that lets you extract structured data from PDF documents. For documents that share a consistent format, you can define a collection of custom SenseML queries as a "config" written in JSON. If you can write basic SQL queries, you can definitely write SenseML queries! 

SenseML concepts
====

A Hello world config
----
A field is the basic SenseML query unit for extracting a piece of document data. The output of a field is a JSON key-value pair that structures the extracted data.  

[**Parameters**](doc:field-query-object#section-parameters)
[**Examples**](doc:field-query-object#section-examples)
[**Notes**](doc:field-query-object#section-notes)

Here is a simple example of a field: 

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

![](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/images/basic_field.png)

As the preceding image shows, this is the output of the example field: 

```json
{
  "name_of_output_key": {
    "type": "string",
    "value": "Below the matching anchor, this is the data to extract. The anchor is a label for this data."
  }
}
```

 For a more complete example, see the [SenseML introduction](doc:senseml-reference-introduction).

Let's explore some SenseML concepts introduced by the preceding example.



TODO: rewrite this stuff:

- The [**field**]() `_driver_name_raw` is a query that finds a driver's name in the quote based on grabbing data below some matched text (`"position": "below"`). Its ID servers as a key for the extracted data. For more information, see [Field query object](doc:field-query-object).
- An **anchor** is matched text that helps narrow down a location in the PDF from which to extract data. In the `"_driver_name_raw"` field, it is simply a string (`"name of driver"`). For information about more complex anchors, see [Anchor object](doc:anchor).
- A **method** defines how to expand out from the anchor and grab data. In the `"_driver_name_raw"` field, the Label method extracts data that is closely positioned below the anchor. For more information about methods, see [Methods](doc:methods).
- The **preprocessor**, `pageRange`, cuts out irrelevant pages of the PDF. For more information about using preprocessors to clean up PDFs before extracting data, see [Preprocessors](doc:preprocessors).
- The **fingerprint** tells Sensible to preferentially run this config if the PDF contains the terms "anyco" or "quoted coverage changes".  For more information about using fingerprints to improve performance, and other configuration settings, see [Configuration Settings](doc:configuration-settings).
- The **computed field** `"driver_name_last"` takes the  output of the `_driver_name_raw` field and extracts the last name from that raw output. For more information about transforming field output, see [Computed field methods](doc:computed-field-methods).

The output of this example config is just one key/value pair: the last name of the driver.  In production scenarios, you can extract just about any text, as well as image coordinates, from a PDF.



PDF extraction concepts
===

To best use SenseML, it's helpful to understand how Sensible represents a PDF.

Lines
----

 A "line" is a rectangular region containing text.  Multiple lines  (shown as gray boxes) can exist on the same horizontal axis; a line is set apart from other lines by any type of whitespace,  not just by newlines.  

![image-20210518095334649](C:\Users\franc\AppData\Roaming\Typora\typora-user-images\image-20210518095334649.png)


Line sorting
----

Lines are sorted primarily by their height on the page (their y-axis position) and secondarily by their left-to-right position (their x-axis position).

For example, this image shows which lines preced and succeed a target line:

![](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/images/lines_sort_example_1.png)

Sometimes, this can be unintuitive, particularly in the case of slightly misaligned text (which oftne happens with handwriting). In the following image, the line in red reads as succeeding the target line, but for Sensible, it precedes the target line:

![](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/images/lines_sort_example_2.png)

To configure this default sorting behavior, see [the XSort parameter](doc:method).

Line grouping
---






TODO: Dots? pixel recognition? 





