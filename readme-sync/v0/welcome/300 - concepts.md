---
title: "Concepts"
hidden: true
---

SenseML is a query language powered by ML and other techniques that lets you extract structured data from PDF documents.

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



Let's explore some SenseML concepts introduced by the preceding example.

- The [**field**]() `name_of_output_key` is a query that finds some text  based on extracting data below some matched text (`"position": "below"`). Its ID is the key for the extracted data. For more information, see [Field query object](doc:field-query-object).
- An **anchor** is matched text that helps narrow down a location in the PDF from which to extract data. Here is simply a string (`"an anchor is some text to match..."`). For information about more complex anchors, see [Anchor object](doc:anchor).
- A **method** defines how to expand out from the anchor and grab data. Here, the Label method extracts data that is closely positioned below the anchor. For more information about methods, see [Methods](doc:methods).

 For a more complete SenseML example, see the [SenseML introduction](doc:senseml-reference-introduction).

PDF extraction concepts
===

To troubleshoot SenseML, it's helpful to understand how Sensible represents a PDF.

Lines
----

 A "line" is a rectangular region containing text.  Readers of left-to-right written languages think of "lines"  as vertically ordered. But for Sensible, multiple lines  (shown as gray boxes) can exist at the same height on the page. In other words, a line is set apart from other lines by any type of whitespace,  not just by newlines:

![](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/images/line_concept.png)


Line sorting
----

Lines are sorted primarily by their height on the page (their y-axis position) and secondarily by their left-to-right position (their x-axis position).

For example, this image shows which lines precede and succeed a target line:

![](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/images/line_sort_example_1.png)

Sorting can be unintutive when text is slightly misaligned vertically (alsooften happens with handwriting). In the following image, a human reader may intepret the red line as succeeding the target line, but for Sensible it precedes the target line:

![](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/images/line_sort_example_2.png)

To configure this default sorting behavior, see [the XSort parameter](doc:method).

Line grouping
---

Sensible groups lines together using whitespace and x- and y-axis positions. Usually these groupings make visual sense to a human reader. It's worth noting that by default, Sensible groups lines separated by vertical space only if they align at the left edge of each line boundary:

![](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/images/line_grouping_example.png)







