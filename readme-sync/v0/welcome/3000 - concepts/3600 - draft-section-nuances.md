---
title: "Section nuances"
hidden: true
---

TODO before publishing: adjust for new Stop, filterLines, selectLines

**Note:** If you're familiar with Sensible, this detailed topic is for you. If you're new to Sensible, see [sections](doc:sections).

The following images show the differing behaviors of sections and vertical sections:

Sections
-----

![Click to enlarge](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/images/final/sections_concept_horizontal.png)

Sensible finds the sections as follows:

1. Finds the range, or y-extent, for a section in the group using Match and Stop lines. The range  can span pages. if no Stop, next section's range starts at next anchor's Match + yOffset parameters. This behavior ensures sections’ ranges never overlap. 
2.  (repeats) Continues finding ranges for the group of sections, searching down the page and across page breaks, until the section group ends with the End parameter, or Sensible reaches the end of the document.
3. Extracts fields from each section in the group, using any SenseML methods. Sensible expects but doesn't require that the data is in a repeated structure for each section.

 

Vertical sections
-----



![Click to enlarge](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/images/final/sections_concept_vertical.png)

Sensible:

1. Finds the section group's range (y-extent) in which to recognize columns using Match and Stop lines. A range can span pages.

2. (repeats) Recognizes columns inside the range, based on whitespace gutters and searching left-to-right. If non-columnar text is present in the range, it can affect column recognition as follows:
   
   - If any non-columnar text is *below* the columns and if there's no Stop parameter, Sensible uses the non-column text as a criteria to end the range. 

   - If any non-columnar text is *above* the columns in the range, it can break column recognition. Exclude the text from the range using the Offset Y parameter.
   
3. Extracts fields from each column in the group, using a limited subset of SenseML methods. For more information about available methods, see TODO link to the Range parameters table. Sensible expects but doesn't require that the data is in a repeated structure for each column.

Column Selection
----

Use the Column Selection parameter with vertical sections to:

- exclude columns from output
- use text in excluded columns as anchors for fields in the target columns. For example, if a table has row labels, then configure the Column Selection parameter so that the row labels become available to all target columns.


For example, if you configure `"columnSelection": [1,2]` for the following table, then the Apples and Bananas columns both:

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



Multiple anchors in section
----

You can handle multiple matches for the range's Match parameter inside a section as follows:

- If you want to ignore multiple anchor matches inside the section, use the Require Stop parameter.  Even if you leave this parameter unspecified, Sensible ignore matches that are on the same horizontal line to the left of the anchor's Match parameter.
- Or, you can use Sensible's default behavior to split a section group range containing multiple anchors into sections. For example, assume that the anchor's Match line is the regular expression `.+`, meaning match any characters. In this case, if you already defined the start and end of the section group, then:
  - For sections, Sensible splits text into "rows" at each newline
  - For vertical sections, Sensible splits text into "columns".


![Click to enlarge](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/images/final/sections_match_all_anchors.png)

For examples of using the default behavior shown in the preceding images, see TODO: link to specific examples for vertical sections and TODO link for sections.













