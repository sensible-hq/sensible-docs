---
title: "Section nuances"
hidden: false
---

**Note:** If you're familiar with Sensible, this detailed topic is for you. If you're new to Sensible, see [sections](doc:sections).

The following images show the differing behaviors of sections and vertical sections:

Sections
-----

![Click to enlarge](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/images/final/sections_concept_horizontal.png)

Sensible finds the sections as follows:

1. Finds the range, or y-extent, for a section in the group using Match and Stop lines.  Sections’  ranges never overlap, and ranges can span pages. In detail:
   - If there's *no* Stop parameter, the current section's range stops above the next anchor's Match + Y Offset parameters. 
   - If there's an *optional* Stop parameter, the current section stops either:
     -  above the next anchor's Match + Y Offset parameter, *or*
     - above the next Stop line + Stop Y Offset parameter. 
     - Use an *optional* stop to prevent the last section in the group from extending to the end of the document.
   - If there's a *required* Stop, the next section stops above the next Stop line + Stop Y Offset parameter, and Sensible ignores any intervening anchor matches.
2. (repeats) Continues finding ranges for the group of sections, searching down the page and across page breaks, until the section group ends with the End parameter, or Sensible reaches the end of the document.
3. Extracts fields from each section in the group. Sensible expects but doesn't require that the data is in a repeated structure for each section.

 

Vertical sections
-----



![Click to enlarge](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/images/final/sections_concept_vertical.png)

Sensible:

1. (one time) Finds the section group's range in which to recognize columns using Match and Stop lines. A range can span pages.

2. (repeats) Recognizes columns inside the range, based on whitespace gutters and searching left-to-right. If non-columnar text is present in the range, it can affect column recognition as follows:
   
   - If there's a Stop parameter, Sensible adds the non-column text to each column. Each column then has a nonlinear, irregular shape. For example, this allows each column to use a table title that spans multiple columns as an anchor. 

   - If there's no Stop parameter, any non-columnar text in the range breaks column recognition. Exclude the text from the range using the offset parameters or the Lines Filter parameter.
   
3. Extracts fields from each column in the group. Sensible expects but doesn't require that the data is in a repeated structure for each column.

Column Selection
----

Use the Column Selection parameter with vertical sections to:

- exclude columns from output
- use text in excluded columns as anchors for fields in the target columns. For example, if a table has row labels, then configure the Column Selection parameter so that the row labels become available to all target columns.


For example, if you exclude the first and last columns by configuring `"columnSelection": [[1,-2]]` for the following table, then the Apples and Bananas columns both:

- have the Nutrition and Notes columns available as anchors, where the anchors keep the spatial layout of the original table in relationship to the target columns

- ignore other target columns when processing the current target column.

This behavior means that for the following table, you can specify a field in the vertical section like:

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

  

![Click to enlarge](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/images/final/vertical_section_column_selection.png)

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

For details about this example, see [Labeled rows and labeled columns table example](doc:sections-example-labeled-rows)

Multiple anchors in section
----

You can handle multiple matches for the range's Match parameter inside a section as follows:

- If you want to ignore multiple anchor matches inside the section, use the Require Stop parameter.  Even if you leave this parameter unspecified, Sensible ignores matches that are on the same horizontal line to the left of the anchor's Match parameter.
- Or, you can use Sensible's default behavior to split a section group range containing multiple anchors into sections. For example, assume that the anchor's Match line is the regular expression `.+`, meaning match any characters. In this case, if you already defined the start and end of the section group, then:
  - For sections, Sensible splits text into "rows" at each newline. 
  - For vertical sections, Sensible splits text into "columns".


![Click to enlarge](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/images/final/sections_match_all_anchors.png)

For an example of using the default behavior shown in the preceding images, see [Table grid example](doc:sections-example-table-grid).













