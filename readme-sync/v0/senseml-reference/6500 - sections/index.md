---
title: "Sections"
hidden: false
---

Extracts data from a document that contains complex or repeated elements ("sections").  In effect, a "section" defines a repeating document inside a document, with its own fields.

The following image shows an example of a document containing "claims" sections, where each section starts with `claim number` and ends below `date of claim`:

![Click to enlarge](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/images/final/sections_1.png)

For the preceding example, you can configure Sensible to return a `claims` array, where each object in the array contains a `claim_number`, `claim_date`, `claimant_last_name`, and other fields.  For more information, see [Claims loss run example](doc:sections-example-loss-run).



You can define "horizontal" sections (`"direction": "horizontal"`), as shown in the preceding image, or you can define columnar sections (`"direction":"vertical"`). 

**Horizontal sections:**

The following image shows horizontal sections. For more information, see the following Parameters section, and see [Section nuances](doc:section-nuances).

![Click to enlarge](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/images/final/sections_concept_horizontal.png)

**Vertical sections:**

The following image shows columnar vertical sections.  For more information, see the following Parameters section, and see [Section nuances](doc:section-nuances).

![Click to enlarge](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/images/final/sections_concept_vertical.png)



Parameters
====


| key                   | value                                                  | description                                                  |
| --------------------- | ------------------------------------------------------ | ------------------------------------------------------------ |
| id (**required**)     | string                                                 | Specifies a field ID for an array of sections to extract in the document area defined by the Range parameter. |
| type                  | `sections`                                             | Specifies that this field extracts sections.                 |
| range  (**required**) | object                                                 | Specifies the document area from which to extract an array of sections.<br/> **horizontal sections:**  The sections can span pages and non-section text. For example, in the preceding claims image, sections can interleave with month headings.<br/><br/> **vertical sections:** The sections can span pages. By default, they can't span text that breaks the column format.<br/>For the Range object's parameters, see the following table. |
| sections              |                                                        | Specifies sections inside sections. Use this for complex sections that contain nested repeated elements, for example, [a grid of tables](doc:sections-example-table-grid). Each nested section searches for its range inside each parent section's range. |
| display               | boolean. Default: true                                 | Specifies to display the start and end of each section as brackets overlaid on the rendered document in the Sensible app. Use the brackets to visually troubleshoot sections. |
| requiredFields        | object                                                 | Array of field IDs that must be non-null for Sensible to return a section.<br/> In the [Claims loss run example](doc:sections-example-loss-run), add the following code to the sections to omit claims that lack a phone number: <br/> `"requiredFields": ["phone_number"],`<br/>With the preceding code, Sensible omits claim number `9876543211`  from the example output. |
| fields                | array of [fields](doc:field-query-object)              | Specifies fields to extract information that you expect to repeat in each section. |
| computed_fields       | array of [computed fields](doc:computed-field-methods) | Specifies to output computed fields to each section. The computed fields have access to each section's fields. To get access to and transform the output of fields that aren't in the sections' range, use the [Copy To Section](doc:copy-to-section) method. |

### Range parameters

See the following table for details about the Range object parameters:

| key                   | value                                                        | description for horizontal sections                          | description for vertical sections                            |
| --------------------- | ------------------------------------------------------------ | ------------------------------------------------------------ | ------------------------------------------------------------ |
| direction             | `horizontal`, `vertical`. default: `horizontal`              | If set to `horizontal`, Sensible searches for horizontal sections. For an illustration of this behavior, see [section nuances](doc:section-nuances). | If set to `vertical`, Sensible detects columnar sections in a single document area defined by the Range parameter. <br/>In detail, Sensible searches  left-to-right for columns that contain repeated text in the first-found document area defined by the Range parameter. <br/>For example, use vertical sections to extract tables nested in tables, tables with row labels, or other complex text layouts. <br/>For an illustration of vertical section behavior, see [section nuances](doc:section-nuances). |
| anchor (**required**) | [Anchor](anchor) object, or array of Match objects           | Contains the following parameters:<br/><br/> **start**: Ignores anything in the document before this line. If undefined, Sensible starts searching for the Match parameter at the beginning of the document.<br/><br/>**match** (**required**): <br/>&nbsp;&nbsp;&nbsp; Specifies the repeated starting line of each section. In the [Claims loss run example](doc:sections-example-loss-run), specify `"Claim number"`. Each section starts at the top boundary of this starting line, and excludes text to the right of the line. If sections lack an easy-to-match starting line, use the Require Stop and Offset Y parameters to start each section above or below the line matched by this parameter. <br/><br/>&nbsp;&nbsp; **end**: Ignores anchor matches in the document after this line. For example, to extract solely September claims in the preceding image, specify `"October"`. | Same behavior as for horizontal sections, with the following exception:<br/>The Match parameter specifies the horizontal line that defines the  shared top boundary of  all the columnar sections.  For more information about column recognition, see [Section nuances](doc:section-nuances#vertical-sections). |
| stop                  | [Anchor](anchor) object, or array of Match objects           | Specifies the bottom boundary of each section. In the [Claims loss run example](doc:sections-example-loss-run), if you specify `"Date of claim"`, then each section stops at a horizontal line below the bottom boundary of the stop line "Date of claim".<br/>Sensible defines the Stop horizontal line by finding the top boundary of the stop line if found, or the top boundary of the next section's starting line, then applies a default offset of 0.08" down or up the page, respectively.<br/>If you don't specify this parameter, each section stops at the top boundary of the next section's starting line. In this case, the last section continues to the end of the document. | Specifies the horizontal line that defines the shared bottom boundary of all the columnar sections.  If not specified, Sensible ends the columns at the first line that spans multiple columns. If specified, Sensible ignores lines that span multiple columns. If the spanning lines occur mid-column, you can configure the Line Filters parameter as an alternative to this parameter.<br/>For more information, see [Section nuances](doc:section-nuances#vertical-sections). |
| offsetY               | number in inches. Positive values offset down the page, negative values offset up the page. | Specifies the number of inches by which to offset each section's top boundary from the anchor's Match parameter. <br/>By default each section starts at the top boundary of the anchor's Match parameter. If you specify Offset Y, each section starts at that top boundary plus the offset. For example, configure this when each section lacks an easy-to-match first line. | Specifies the number of inches by which to offset the columns' shared top boundary from the anchor's Match parameter. <br/>For example, configure this when you want to exclude non-columnar text from columnar sections. |
| stopOffsetY           | number in inches. Positive values offset down the page, negative values offset up the page. | Specifies the number of inches by which to offset each section's bottom boundary from the horizontal line specified by the Stop parameter. | Specifies the number of inches by which to offset the columns' shared bottom boundary from the horizontal line specified by the Stop parameter. |
| tolerance             | number in inches. default: 0.08                              | Configure this option for your Stop parameter if the stop line and its immediately preceding and succeeding lines are an unusual font size.<br/> For example, if your font size is a tiny 1.44 pt (0.02 inches), set this parameter to 0.01.<br>In detail, Sensible defines the Stop horizontal line by finding the top boundary of the stop line, or if unspecified the top boundary of the next section's starting line, then applies a default offset of 0.08" down or up the page, respectively. This parameter configures the default offset. | not supported                                                |
|                       |                                                              | **Parameters specific to horizontal sections**               |                                                              |
| externalRange         | object                                                       | (Advanced) Enables anchoring on text that's external to the sections in the sections' field anchors.  For example, use the external range with the [Intersection](doc:intersection) method when sections lack internal anchoring candidates.<br/>The external range defines a vertical range anywhere in the document. You can configure the external range to be static, or to repeat relative to each section.<br/>Contains the following parameters:<br/><br/>`anchor`  (**required**):  An [Anchor](https://docs.sensible.so/docs/anchor) object. The external range starts at the top boundary of this starting line, and the range's scope includes text to the left of this line. If the range lacks an easy-to-match first line, you can use the Offset Y parameter to start the range above or below the line matched by this parameter. <br/><br/>`anchorIsAbsolute`: (default: false).  If false, Sensible creates dynamic external ranges, each relative to a section start. For example, configure dynamic external ranges if you want to anchor each section's fields on variably positioned page headings. For more information, see [Dynamic external range example](doc:sections-example-external-range#example-dynamic). Sensible starts searching for dynamic external ranges in the lines succeeding the start of each section. To search for dynamic external ranges that precede each section, use  `"reverse":"true"`  on the external range's anchor. <br/>If the Anchor Is Absolute option is set to true, Sensible creates one static external range in the document, searching from the start of the document. For an example of a static dynamic range, see [Static external range example](doc:sections-example-external-range#example-static).<br/><br/>`stop`: (Match object) (**required**) A Match object defining the end of the external range. Sensible defines the Stop horizontal line by finding the top boundary of the stop line, then applies a default offset of 0.08" down the page.<br/><br/>`offsetY`: Specifies the number of inches to offset the range's top boundary from the anchor's Match parameter.<br/><br/>`stopOffsetY`: Specifies the number of inches to offset from the Stop parameter.<br/> | not supported                                                |
| requireStop           | Boolean. default: false                                      | If true, each section ends when it matches the Stop parameter, instead of the default behavior of ending at the next starting line specified in the anchor's Match parameter.<br/>**Note:**  Configure this parameter for horizontal sections when the starting line repeats in each section, to avoid prematurely ending each section.<br/>You don't need to configure this parameter for matches that are on the same horizontal line as the anchor's Match parameter. For more information, see [Multiple anchors in section](doc:section-nuances#multiple-anchors-in-section). | not supported                                                |
|                       |                                                              | **Parameters specific to vertical (columnar) sections**      |                                                              |
| ignoredColumns        | integer array.                                               | not supported                                                | Removes unwanted columns from both the output *and* from the SenseML search scope. For example, this is useful if the columns contain text that interferes with anchoring on other columns. |
| columnSelection       | array of index selections where each "index selection" can be:<br/>- a column index or comma-delimited indices<br/><br/>- an array with two comma-delimited indices, meaning all the columns in the indices range<br/><br/> default: capture all columns (`[]`) | not supported                                                | Use to configure which columns to treat as sections. Sensible appends *unselected* columns to each section, for example so that they can be used as anchor candidates. For an illustration, see [Section nuances](doc:section-nuances#column-selection).<br/>Example syntax:<br/> `[[0,5]]` selects 1st through 6th columns as sections. Sensible adds the lines from any other columns to each section. <br/>`[1,3,-1]`  selects the 2nd, 4th, and the last column. <br/>  `[[0, -2]]` selects 1st through 2nd-to-last columns.<br/> `[1,[3,7]]` selects the 2nd column and the 4th through 8th columns. |
| minColumnGap          | number in inches. default: 0                                 | not supported                                                | Configures column recognition by specifying the smallest allowed width of the gutters separating the columns. For an example, see [Table grid example](doc:sections-example-table-grid). Use when text in a column contains large whitespace gaps that cause Sensible to mistakenly split one column into two. To avoid this split, set a minimum gap that's larger than the gaps inside the column. The default (0) specifies that zero-width vertical lines define the column boundaries. |
| lineFilters           | Match object, or array of Match objects                      | not supported                                                | Use to ignore lines that span columns and break column recognition. For example, if the lines occur mid-column, use this parameter rather than a Stop parameter to exclude the lines. Sensible excludes the lines both from the output and from the SenseML search scope.<br/>You don't need to configure this parameter if you specify a Stop parameter. For more information, see [Section nuances](doc:section-nuances#vertical-sections). |



Examples
====

See the following topics: 


- [Loss run example](doc:sections-example-loss-run)

- [Labeled rows and labeled columns table example](doc:sections-example-labeled-rows)

- Advanced: [Nested columns example](doc:sections-example-nested-columns)

- Advanced: [Nested table example](doc:sections-example-nested-table)

- Advanced: [Table grid example](doc:sections-example-table-grid)

- Advanced: [Zip sections example](doc:sections-example-zip)

- Advanced: [Zip and flatten nested sections](doc:sections-example-copy-from-sections)

- Advanced: [External anchors for sections](doc:sections-example-external-range)


Notes
===

- For details about vertical sections, see [Section nuances](doc:section-nuances#vertical-sections).
- See the [Copy To Section](doc:copy-to-section) computed field method to add globally applicable document information to sections. 
- See the [Zip](doc:zip) computed field for information about zipping sections together.



