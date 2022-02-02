---
title: "Section nuances"
hidden: true
---

**Note:** If you're familiar with Sensible, this detailed topic is for you. If you're new to Sensible, see [sections](doc:sections).



The following images show the differing behaviors of sections vs vertical sections:

Sections
-----

![Click to enlarge](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/images/final/sections_concept_horizontal.png)

Sensible:

1. Finds the vertical range (y-extent) for a section in the group using Match and Stop lines. Range can span pages. if no Stop, next section's range starts at next Anchor:Match +yOffset. This ensures sections’ ranges never overlap. 
2.  (repeats) Continues finding ranges for sections, searching down the page and across page breaks.
3. Extracts fields from each section in the group. Extract anything the y-extent (can include tables or other complex data); usually the data is in a repeated structure

 

Vertical sections
-----



![Click to enlarge](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/images/final/sections_concept_vertical.png)

Sensible:

1. Finds the vertical range (y-extent) in which to recognize columns using Match and Stop lines. Range can span pages.  Ignores any non-column text above or below columns in the range, except if the Stop parameter is unspecified, uses non-column text as a criteria to end the range. 
2. (repeats) Recognizes columns based on whitespace, searching left-to-right. 

TODO: talk about how STOP parameter can influence column recognition??? if that's a thing?

Column Selection
----

Use the Column Selection paramter with vertical sections to:

- exclude columns from output
- use text in excluded columns as anchors for fields in the target columns. For example, if a table has row labels, then configure the Column Selection parameter so that the row labels become available to all target columns.


For example, if you configure `"columnSelection": [1,2]` for the following table, then the Apples and Bananas columns both:

- have the Nutrition and Notes columns available as anchors, where the anchors retain the spacial layout of the original table in relationship to the target columns

-  ignore other target columns when processing the current target column.

![Click to enlarge](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/images/final/vertical_section_column_selection.png)

For example, you can specify a field in the vertical section like:

```
   {
        "id": "calories",
        "anchor": "calories",
        "method": {
          "id": "row",
          "tiebreaker": "first"
        }
      }
```

And return something like:

 ```
 {
   "fruit": [
     {
       "calories": 95,
     {
       "calories": 105,
     }
   ]
 }
 ```



