---
title: "Section nuances"
hidden: true
---

**Note:** If you're familiar with Sensible, this detailed topic is for you. If you're new to Sensible, see [sections](doc:sections).

The following images show the differing behaviors of sections and vertical sections:

Sections
-----

![Click to enlarge](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/images/final/sections_concept_horizontal.png)

Sensible finds the sections as follows:

1. Finds the range, or y-extent, for each section using Match and Stop lines.  Sections’  ranges never overlap, and ranges can span pages. In detail:
   - If there's *no* Stop parameter, the current section's range stops above the next anchor's Match + Y Offset parameters. 
   - If there's an *optional* Stop parameter, the current section stops either:
     -  above the next anchor's Match + Y Offset parameter, *or*
     - below the next Stop line + Stop Y Offset parameter. 
     - Use an *optional* stop to prevent the last section in the group from extending to the end of the document.
   - If there's a *required* Stop, the next section stops below the next Stop line + Stop Y Offset parameter, and Sensible ignores any intervening anchor matches.
2. (repeats) Continues finding ranges for the group of sections, searching down the page and across page breaks, until the last section ends at the End parameter or at the end of the document.
3. Extracts fields from each section. Sensible expects but doesn't require that the data is in a repeated structure for each section.

 

Vertical sections
-----



![Click to enlarge](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/images/final/sections_concept_vertical.png)

Sensible:

1. (one time) Finds the vertical document range in which to recognize columns using Match and Stop lines. The range can span pages.
2. (repeats) Recognizes columns inside the range, based on whitespace gutters and searching left-to-right. If non-columnar text is present in the range, it can affect column recognition as follows:

   - If there's a Stop parameter, Sensible adds the non-column text to each column. Each column then has a nonlinear, irregular shape. For example, this allows each column to use a table title that spans multiple columns as an anchor. 

   - If there's no Stop parameter, any non-columnar text in the range breaks column recognition. Exclude the text from the range using the offset parameters or the Lines Filter parameter.
3. Extracts fields from each column in the range. Sensible expects but doesn't require that the data is in a repeated structure for each column.

**Tip:** To define multiple vertical ranges in which to extract columnar sections, nest the sections in a parent section group.  For an example, see [Advanced: nested columns example](doc:sections-example-nested-columns).

Column Selection
----

By default, Sensible creates a section from each column it detects. You can configure Sensible to handle columns in the following ways:

- "Selected" columns: Sensible creates a section for each column specified in the Column Selection parameter.

- "Kept" columns: If you configure the Column Selection parameter, Sensible adds the lines in any *unspecified* columns to each section.
- "Ignored" columns:  Sensible ignores any columns specified in the Ignored Columns parameter, including excluding them from the "kept" columns.

For example, if you select the "Apple" and "Banana" columns by configuring `"columnSelection": [[1,-2]]` for the table in the following image, then:

1. Sensible detects four columns. Sensible targets two columns to create sections from: the Apple column and the Banana column.
2. For the Apple column, Sensible creates a section that is a table slice containing:
   - A  "selected" column: the Apple column
   
   - "kept" columns: the Nutrition and Notes columns. The lines in these columns are then available as anchoring or output data in this section.
     For example, you can extract the cell containing `95` in the Apple column with:


  ```json
      {
           "id": "fruit_calories",
           /* anchor on data in the first column, a "kept" column */
           "anchor": "calories",
           "method": {
             /* returns 95 for the first section and 105 for the second section */  
             "id": "row",
             "tiebreaker": "first"
           }
         }
  ```

3. The Banana section contains the Banana, Nutrition, and Notes columns. For example, you can find the cell containing `105` in the Bananas column using the same `fruit_calories` field as in the preceding step. In other words, you *don't* have to configure `"tiebreaker": "second"`.  

![Click to enlarge](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/images/final/vertical_section_column_selection.png)

As steps 2 and 3 in the previous image illustrate, the varying gap sizes between columns in each section mean that you can't use coordinate-based methods such as the Region method for fields in these sections.

For more information about this example, see [Labeled rows and labeled columns table example](doc:sections-example-labeled-rows)

Multiple anchors in section
----

See the following options for handling a section that contains multiple matches for the range's Match parameter.

**Ignore multiple anchors**

If you want to ignore multiple anchor matches inside the section, use the Require Stop parameter. You don't need to configure this parameter for matches that are on the same horizontal line as the anchor's Match parameter.

**Match on all text**

For horizontal sections, you can create a section starting at each newline if you match on all text for the Match parameter. Take the following steps:

- Define a section array with specific text matches for the Start and End parameters of the sections.

- Specify the anchor's Match parameter using the regular expression `.+`, which matches any characters.

In this case, Sensible creates sections by splitting text into "rows" at each newline. For more information about the behavior shown in the following image, see the  [Zip sections example](doc:sections-example-zip).


![Click to enlarge](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/images/final/sections_match_all_anchors.png)

For vertical sections, specifying the regular expression `".+"`   for the Match parameter can be useful for repeating vertical sections that lack good anchor match candidates. In these situations, you must also nest the sections in a parent section group. For more information, see [Table grid example](doc:sections-example-table-grid).

















