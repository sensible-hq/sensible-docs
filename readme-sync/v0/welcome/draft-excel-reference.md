---
title: "excel reference"
hidden: true
---

DEMO IFRAME:



[block:html]
{
  "html": "<div>\n  <iframe width=\"800\" height=\"200\" scrolling=\"auto\"  src=\"https://docs.google.com/spreadsheets/d/e/2PACX-1vTKF1zRWnckY3ujq0I7treACgOtSmUuhTDdbzoD7FY3LdMFTYYvK409nLb1MjtT_KOSWj2i6DxZPP90/pubhtml?widget=true&amp;headers=false\"></iframe>\n</div>\n"
}
[/block]


QUESTIONS:

- how does a whole stringified row (no tiebreaker) or column get handled?
- how about the arrays from https://docs.sensible.so/docs/pick-values ? 
- how about https://docs.sensible.so/docs/key-value ? (I don't know what it outputs, single value?)
- how about handling the zipped output of table methods into row objects? https://docs.sensible.so/docs/zip 

How does the data convert from the JSON extraction to excel sheets?

simple fields
====


- "simple" fields with no nested info structures, like labels, boxes, regions, etc, convert to a "fields" sheet like this:

![image-20220523133444762](C:\Users\franc\AppData\Roaming\Typora\typora-user-images\image-20220523133444762.png)

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

