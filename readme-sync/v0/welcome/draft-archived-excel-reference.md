---
title: "excel reference"
hidden: true
---

This topic describes how Sensible converts documents such as PDFs into Excel sheets. To get Excel output structured as labeled columns, Sensible transforms its JSON API extraction output using the following rules:



- "simple" fields that output single values, output into column label/value pairs in a `fields` sheet. Like this:

  <iframe src="https://docs.google.com/spreadsheets/d/e/2PACX-1vRJO_nwPRVe84ZdAi-gc6mny0zhRO9iz4nclfEKSBFQWHotARcgUkwfcinpGJTzPM4GIoIvf6PcN7zv/pubhtml?widget=true&amp;headers=false"></iframe>

- fields with array output get handled a few different ways:

  - For fields configured with a  type that *always* output an array, for example a field with `"type": "name"` specified, the output turns into a stringifed array in the `fields` sheet. Like this:
    ![image-20220523133956948](C:\Users\franc\AppData\Roaming\Typora\typora-user-images\image-20220523133956948.png)

  - A field with `"match":"all` configured gets its own sheet. For example a `covered_cars`  field with  `"match":"all`  gets a `covered_car` sheet that lists all the cars found. Liked this (IMAGE)
  
- Fields that output objects with nested structures get their own sheets. For example, tables and sections. 

- Invoices are a special case. Sensible outputs one Excel file per invoice. (TODO verify)

Examples
====

The following example document and extraction:



- simple fields
- table
- section + fields array
- nested sections








simple fields
====


- "simple" fields with no nested info structures, like labels, boxes, regions, etc, convert to a "fields" sheet like this:



**notes**

- Any extra information except the value gets stripped out.  For example, a field like this:

``` json
  {
      "id": "total_percentage_sold",
   "source": "20.5%",
      "value": 20.5,
      "type": "percentage"
    }
```

Would get output in the excel/csv sheet simply as:

```csv
total_percentage_sold	20.5
```



- Arrays get handled in a variety of ways:
  - For types that *always* output an array, for example the name type, the output turns into a stringifed array.  For example, this output:



```json
{
"source": "Richard & Ann Spangenberg",
  "type": "name",
  "value": [
      "RICHARD SPANGENBERG",
      "ANN SPANGENBERG"
}

```

turns into (TODO: make it RICHARD SPANGENBERG, ANN SPANGENBERG:

![image-20220523133956948](C:\Users\franc\AppData\Roaming\Typora\typora-user-images\image-20220523133956948.png)

- For fields that output an array as a result of `"match":"all"`, each field gets its own sheet (TODO: example/verify)

Tables 
===

Each table gets its own CSV or Excel sheet.

Invoice
====

Since sensible expects one invoice per PDF, each invoice gets its own Excel document with no other sheets, or 1 CSV with no other CSVs.

Sections
===

Sections are output as:

- a fields sheet/csv for all the 'simple fields'
- each table or other complex field gets its own sheet/csv

**EXAMPLES**

**Simple fields output**

TODO: iframes or just links?? 

[Row](docs:row)

<iframe here>

</iframe>

[Box](docs:box)

<iframe here>
TODO convert to table, some have examples, some don't??? 

- Box

- Checkbox

- (document range?? passthrough?)

- Intersection

- Invoice `metadata` output

- Label

- Nearest Checkbox

- Regex

- Region

- Row(?)

- **computed**

- Concatenate

- Constant

- Mapper

- (pick values?)

- Split

  

For more examples, see the following: 

| simple fields    | TODO: use when adding docs to topics                         |                                                              |
| ---------------- | ------------------------------------------------------------ | ------------------------------------------------------------ |
| anyco            | https://docs.google.com/spreadsheets/d/1S5W9NO-5W51xxif29Aws6sojBiitONUpb-g4-6ANtaA/edit?usp=sharing | [Getting started][getting-started](doc:getting-started#csv-output) |
| invoice metadata | https://docs.google.com/spreadsheets/d/1vIiiFGwLYjT6CLx9BHBZdur9PdZ50lY-G3ae2CoPf9w/edit#gid=0 | [Invoice][doc:invoice#csv-output]                            |
|                  |                                                              |                                                              |
