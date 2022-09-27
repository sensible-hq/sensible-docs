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
     - below the next Stop line + Stop Y Offset parameter. 
     - Use an *optional* stop to prevent the last section in the group from extending to the end of the document.
   - If there's a *required* Stop, the next section stops below the next Stop line + Stop Y Offset parameter, and Sensible ignores any intervening anchor matches.
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

**Tip:** To extract repeated vertical section groups, nest them in a parent section group. 

Column Selection
----

Use the Column Selection parameter with vertical sections to:

- exclude columns from output
- use text in excluded columns as anchors for fields in the target columns. For example, if a table has row labels, then configure the Column Selection parameter so that the row labels become available to all target columns.

For example, if you exclude the first and last columns by configuring `"columnSelection": [[1,-2]]` for the table in the following image, then:

1. Sensible selects the Apples and Bananas columns for output.
2. For the Apples column, Sensible creates a section that is a table slice containing:
   1. the Apples column
   2. the Nutrition and Notes, columns available as anchors.
   For example, you can extract the cell containing `95` in the Apples column with:


  ```json
      {
           "id": "fruit_calories",
           "anchor": "calories",
           "method": {
             "id": "row",
             "tiebreaker": "first"
           }
         }
  ```

3. The Banana column has access as the Apple column to anchoring information, in the same spatial layout. For example, you can find the cell containing `105` in the Bananas column using the same `fruit_calories` field as in the preceding step. In other words, you *don't* have to configure `"tiebreaker": "second"`.

![Click to enlarge](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/images/final/vertical_section_column_selection.png)

For more information about this example, see [Labeled rows and labeled columns table example](doc:sections-example-labeled-rows)

Multiple anchors in section
----

You can handle multiple matches for the range's Match parameter inside a section as follows:

- If you want to ignore multiple anchor matches inside the section, use the Require Stop parameter. You don't need to configure this parameter for matches that are on the same horizontal line as the anchor's Match parameter.
- If you want to create sections out of rows or columns, without matching on specific text in those sections, take the following steps :
  - Define a section group with specific text matches for the Start and End parameters of the section group.
  - Specify the anchor's Match parameter using the regular expression `.+`, which matches any characters.

  In this case, Sensible creates sections as follows:
  
  - For horizontal sections, Sensible splits text into "rows" at each newline. 
  - For vertical sections, Sensible splits text into "columns".
  


![Click to enlarge](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/images/final/sections_match_all_anchors.png)

For an example of using the default behavior shown in the preceding images, see [Table grid example](doc:sections-example-table-grid) and [Zip sections example](doc:sections-example-zip).













