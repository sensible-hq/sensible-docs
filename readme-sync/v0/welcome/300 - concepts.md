---
title: "Concepts"
hidden: false
---

SenseML is a query language that lets you extract structured data from PDF documents.

SenseML concepts
====

A Hello world config
----
A field is the basic SenseML query unit for extracting a piece of document data. The output of a field is a JSON key-value pair that structures the extracted data.  

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

![Click to enlarge](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/images/final/basic_field.png)

As the preceding image shows, this is the output of the example field: 

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
| **[anchor](doc:anchor)**        | Matched text that helps narrow down a location in the PDF from which to extract data.  In this example, `"an anchor is some text to match..."`. |
| [method](doc:method)            | Defines how to expand out from the anchor and extract data. In this example, the Label method extracts data that is closely positioned below the anchor (`"position": "below"`). For a list of methods, see [Methods](doc:methods). |

 For a more complete SenseML example, see the [SenseML introduction](doc:senseml-reference-introduction).

PDF extraction concepts
===

To troubleshoot SenseML, it's helpful to understand how Sensible represents a PDF.

Lines
----

 A "line" is a rectangular region containing text.  Readers of left-to-right written languages think of "lines"  as vertically ordered. But for Sensible, multiple lines  (shown as gray boxes) can exist at the same height on the page:

![Click to enlarge](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/images/final/line_concept.png)

 In other words, a line is set apart from other lines by any type of whitespace,  not just by newlines.


Line sorting
----

Lines are sorted primarily by their height on the page (their y-axis position) and secondarily by their left-to-right position (their x-axis position).

For example, this image shows which lines precede and succeed a target line:

![Click to enlarge](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/images/final/line_sort_example_1.png)

However, when text is slightly misaligned vertically (often the case with handwriting), line sorting is less intuitive. In the following image, a human reader may intepret the red line as succeeding the target line, but for Sensible it *precedes* the target line because it is higher on the page:

![Click to enlarge](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/images/final/line_sort_example_2.png)

To configure this default sorting behavior, see [the XMajorSort parameter](doc:method).

Line grouping
---

**Label method**

For the Label method, Sensible groups lines together using whitespace and x- and y-axis positions. Sometimes, Sensible's line groups are more restrictive than a human reader might expect. In particular, Sensible groups lines separated by vertical space only if they align at the *left* edge of each line boundary by default:

![Click to enlarge](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/images/final/line_grouping_example.png)

To capture multiple unaligned lines, use the Document Range method.

Ligatures
---

*Ligatures* are two or more letters joined together into a single glyph. They appear to be garbage Unicode characters in your PDF direct text extraction, for example:

```json
….incinerating or composting toilets; \u0000re suppression systems; water softeners, conditioners or \u0000ltering systems; over\u0000ow drains for tubs and sinks; back\u0000ow prevention devices...
```

Even if the rendered PDF looks fine, ligatures can still exist in the extracted text. In the preceding example, `fi`, `fl` and others are joined together and appear as `\u0000` in the raw text, so that you see `\u0000re` instead of `fire` and `over\u0000ow` instead of `overflow`.

To find out if ligatures exist in the extracted text for your PDF, extract all the lines in the PDF and search for Unicode characters. To extract all lines into one key-value pair, use a config like:

```
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
          "type":"first"
        }
      }
    }
  ],
}
```



