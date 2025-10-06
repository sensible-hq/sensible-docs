---
title: "Sections"
hidden: false
---

Extracts data from a document that contains complex or repeated elements ("sections").  In effect, a "section" defines a repeating document inside a document, with its own fields.

The following image shows an example of a document containing a group of "claims" sections:

![Click to enlarge](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/images/final/sections_1.png)

For the preceding example, you can configure Sensible to return an `unprocessed_claims` array, where each object in the array contains a `claim_number`, `claim_date`, `claimant_last_name`, and other fields.  For more information, see [Claims loss run example](doc:sections-example-loss-run).



You can define "horizontal" section groups, as shown in the preceding image, or you can define "vertical" section groups (`"direction":"vertical"`), which use column layout detection rather than text matches to define sections. 

**Horizontal sections:**

The following image shows horizontal sections. For more information, see the following Parameters section, and see [Section nuances](doc:section-nuances).

![Click to enlarge](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/images/final/sections_concept_horizontal.png)

**Vertical sections:**

The following image shows vertical sections.  For more information, see the following Parameters section, and see [Section nuances](doc:section-nuances).

![Click to enlarge](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/images/final/sections_concept_vertical.png)

**Tip:** To extract repeated vertical section groups, nest them in a parent section group.  For an example, see [Advanced: nested columns example](doc:sections-example-nested-columns).

Parameters
====


| key                   | value                                                  | description                                                  |
| --------------------- | ------------------------------------------------------ | ------------------------------------------------------------ |
| id (**required**)     | string                                                 | Specifies an ID for a group of sections to extract in the document area defined by the Range parameter. You can define an array of section groups, and you can nest sections inside of other sections. |
| type                  | `sections`                                             | Specifies that this field extracts sections.                 |
| range  (**required**) | object                                                 | Specifies the document area from which to extract a group of sections. The Range parameter specifies both:<br/>- a group of repeated sections in an area of the document <br/>- the start and end of each repeated section.<br/><br/> **horizontal sections:**  The sections group can span pages and nonrepeating text. For example, in the preceding image, an "unprocessed_claims" section group can span month headings.<br/><br/> **vertical sections:** The section group can span pages. By default, the group can't span text that breaks the column format.<br/>For the Range object's parameters, see the following table. |
| sections              |                                                        | Specifies sections inside sections. Use this for complex sections that contain nested repeated elements, for example, [a grid of tables](doc:sections-example-table-grid). Each nested section searches for its range inside the parent section's range. |
| display               | boolean. Default: true                                 | Specifies to display  the start and end of each section in a section group as brackets overlaid on the rendered document in the Sensible app. Use the brackets to visually troubleshoot sections. |
| requiredFields        | object                                                 | Array of field IDs that must be non-null for Sensible to return a section.<br/> In the [Claims loss run example](doc:sections-example-loss-run), add the following code to the sections group to omit claims that lack a phone number: <br/> `"requiredFields": ["phone_number"],`<br/>With the preceding code, Sensible omits claim number `9876543211`  from the example output. |
| fields                | array of [fields](doc:field-query-object)              | Specifies fields to extract information that you expect to repeat in each section in the section group. |
| computed_fields       | array of [computed fields](doc:computed-field-methods) | Specifies to output computed fields to each section in the section group. The computed fields have access to each section's fields. To get access to and transform the output of fields that aren't in the section group's range, use the [Copy To Section](doc:copy-to-section) method. |

### Range parameters

See the following table for details about the Range object parameters:

| key                   | value                                              | description                                                  |
| --------------------- | -------------------------------------------------- | ------------------------------------------------------------ |
| anchor (**required**) | [Anchor](anchor) object, or array of Match objects | Anchor parameters have a special meaning in the context of sections, as follows:<br/><br/> **start**: Ignores anything in the document before this line. if undefined, Sensible searches for the section group starting at the beginning of the document<br/><br/>**match** (**required**): <br/>&nbsp;&nbsp;&nbsp; **horizontal sections:** Specifies both the start of the section group and the repeated starting line of each section. For example, in the preceding image, specify `"Claim number"`. The section starts at the top boundary of this starting line, and the section's scope includes text to the left of this line. If the start of the section lacks an easy-to-match line, you can use the Require Stop and Offset Y parameters to start the section above or below the line matched by this parameter. <br/>&nbsp;&nbsp; **vertical sections:** Specifies the start of the  section group. By default, Sensible recognizes columns as sections automatically. For more information, see [Section nuances](doc:section-nuances#vertical-sections).<br/><br/>**end**: Ignores any anchor matches in the document after this line. For example, to extract solely September claims in the preceding image, specify `"October"`. |
| externalRange         | object                                             | **horizontal sections**:  (Advanced) Enables anchoring on text that's external to the section group range in the sections' field anchors.  For example, use the external range with the [Intersection](doc:intersection) method when sections lack internal anchoring candidates.<br/>The external range defines a vertical range anywhere in the document. You can configure the external range to be static, or to repeat relative to each section.<br/>Contains the following parameters:<br/><br/>`anchor`  (**required**):  An [Anchor](https://docs.sensible.so/docs/anchor) object. The external range starts at the top boundary of this starting line, and the range's scope includes text to the left of this line. If the start of the range lacks an easy-to-match line, you can use the Offset Y parameter to start the range above or below the line matched by this parameter. <br/><br/>`anchorIsAbsolute`: (default: false).  If false, Sensible creates dynamic external ranges, each relative to a section start. For example, configure dynamic external ranges if you want to anchor each section's fields on variably positioned page headings. For more information, see [Dynamic external range example](doc:sections-example-external-range#example-dynamic). Sensible starts searching for dynamic external ranges in the lines succeeding the start of each section. To search for dynamic external ranges that precede each section, use  `"reverse":"true"`  on the external range's anchor. <br/>If this option is set to true, Sensible creates one static external range in the document, searching from the start of the document. For an example of a static dynamic range, see [Static external range example](doc:sections-example-external-range#example-static).<br/><br/>`stop`: (Match object) (**required**) A Match object defining the end of the external range. Sensible defines the Stop horizontal line by finding the top boundary of the stop line, then applies a default offset of 0.08" down the page.<br/><br/>`offsetY`: Specifies the number of inches to offset the range's top boundary from the anchor's Match parameter.<br/><br/>`stopOffsetY`: Specifies the number of inches to offset from the Stop parameter.<br/><br/><br/>**vertical sections:** N/A, external range isn't allowed for vertical sections. |
| stop                  | [Anchor](anchor) object, or array of Match objects | **horizontal sections:**  Specifies the repeated end of the section after its anchor. For example, if you specify `"Date of claim"`, then each section stops at a horizontal line below the bottom boundary of the stop line "Date of claim" (plus any offset you specify).<br/>Sensible defines the Stop horizontal line by finding the top boundary of the stop line if found, or the top boundary of the next section's starting line, then applies a default offset of 0.08" down or up the page, respectively.<br/>If you don't specify this parameter, each section stops at the top boundary of the next section's starting line (plus any offset). In this case, the last section in the group continues to the end of the document.<br/><br/>**vertical sections:** Specifies the end of the section *group*, and ignores lines that span multiple columns. If not specified, Sensible ends the section group at the first line that spans multiple columns. If the spanning lines occur mid-column, you can also configure the Line Filters parameter.<br/>For more information, see [Section nuances](doc:section-nuances#vertical-sections). |
| requireStop           | Boolean. default: false                            | **horizontal sections:**  If true, the Stop parameter is required, and the section ends when it matches the Stop parameter, instead of the default behavior of ending at the next starting line specified in the anchor's Match parameter.<br/>**Note:**  Configure this parameter for horizontal sections when the starting line repeats in the section, to avoid ending the section before it completes. You don't need to configure this parameter if multiple starting line matches lie on one *horizontal* line in the section. In such a case, Sensible ignores any zero-height sections generated by this horizontal line's matches. For more information, see [Multiple anchors in section](doc:section-nuances#multiple-anchors-in-section).<br/><br/>**vertical sections:** N/A, not allowed for vertical sections. |
| offsetY               | number in inches                                   | Specifies an offset from the anchor Match parameter.  Positive values offset down the page, negative values offset up the page. <br/><br/> **horizontal sections:** Specifies the number of inches to offset the section's top boundary from the anchor Match parameter. By default a section starts at the top boundary of the matched line. If you specify Offset Y, the section starts at that top boundary plus the offset. For example, configure this when the section lacks an easy-to-match first line.<br/><br/>**vertical sections:** Specifies the number of inches to offset the section *group's* top boundary from the anchor Match parameter. For example, configure this when when you want to exclude non-columnar text from a vertical section.<br/><br/> |
| stopOffsetY           | number in inches                                   | Specifies the number of inches to offset from the Stop parameter. <br/><br/>**horizontal sections:**  Offsets each section's stop from the Stop horizontal line.<br/><br/>**vertical sections:** Offsets the section *group's* stop from the Stop horizontal line. |
| tolerance             | number in inches. default: 0.08                    | Configure this for your Stop parameter if the stop line and its immediately preceding and succeeding lines are an unusual font size. By default, Sensible defines the Stop horizontal line by finding the top boundary of the stop line if found, or the top boundary of the next section's starting line, then applies a default offset of 0.08" down or up the page, respectively. This parameter configures the default offset.<br/> For example, if your font size is a tiny 1.44 pt (0.02 inches), set this parameter to 0.01. |

### Range parameters for columns

Use `"direction":"vertical"` in the Range object to define a "vertical" sections group, where each section is a column-like layout. For example, use vertical sections to extract tables nested in tables, tables with row labels, or other complex text layouts. 

The following table shows Range parameters specific to vertical sections.

| key             | value                                                        | description                                                  |
| --------------- | ------------------------------------------------------------ | ------------------------------------------------------------ |
| direction       | `horizontal`, `vertical`. default: `horizontal`              | If set to `vertical`, Sensible searches for columns in a sections group. <br/>In detail, Sensible searches  left-to-right for columns in the first-found document area defined by the Range parameter, rather than the default behavior of continuing to search for matches for the Range parameter. For an illustration of this behavior, see [section nuances](doc:section-nuances). |
| columnSelection | array of index selections where each "index selection" can be:<br/>- a column index or comma-delimited indices<br/><br/>- an array with two comma-delimited indices, meaning all the columns in the indices range<br/><br/> default: capture all columns (`[]`) | Use to configure which columns to treat as sections. Sensible adds *unselected* columns to each section, for example so they can be used as anchor candidates. For an illustration, see [Section nuances](doc:section-nuances#column-selection).<br/> `[[0,5]]` selects 1st through 6th columns as sections. Sensible adds the lines from any other columns to each section. <br/>`[1,3,-1]`  selects 2nd, 4th, and the last columns. Use negative indices to offset from the last column. <br/> `[1,[3,7]]` selects the 2nd column and the 4th through 8th columns.<br/>  `[[0, -2]]` selects 1st through 2nd-to-last columns.<br/><br/> |
| ignoredColumns  | integer array.                                               | Removes unwanted columns from both the output *and* from the SenseML search scope. For example, this is useful if the columns contain text that interferes with anchoring on other columns. |
| minColumnGap    | number in inches. default: 0                                 | Configures column recognition by specifying the smallest allowed width of the gutters separating the columns. For an example, see [Table grid example](doc:sections-example-table-grid). Use when text in a column contains whitespace gaps such that Sensible can split one column into two. To avoid this split, set a minimum gap that's larger than the gaps inside the column. The default (0) means that zero-width vertical lines define the column boundaries. |
| lineFilters     | Match object, or array of Match objects                      | Use to ignore lines that span columns and break column recognition. For example, if the lines occur mid-column, use this parameter rather than a Stop parameter to exclude the lines. Sensible excludes the lines both from the output and from the SenseML search scope.<br/>You don't need to configure this parameter if you specify a Stop parameter. For more information, see [Section nuances](doc:section-nuances#vertical-sections). |

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



