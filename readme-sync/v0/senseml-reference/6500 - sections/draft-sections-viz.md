---
title: "Sections"
hidden: true
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


| key                   | value                  | description                                                  |
| --------------------- | ---------------------- | ------------------------------------------------------------ |
| id (**required**)     | string                 | Specifies an ID for a group of sections to extract in the document area defined by the Range parameter. You can define an array of section groups, and you can nest sections inside of other sections. |
| range  (**required**) | object                 | Specifies the document area from which to extract a group of sections. The Range parameter specifies both:<br/>- a group of repeated sections in an area of the document <br/>- the start and end of each repeated section.<br/><br/> **horizontal sections:**  The sections group can span pages and nonrepeating text. For example,  in the preceding image, an "unprocessed_claims" section group can span month headings.<br/><br/> **vertical sections:** The section group can span pages. By default, the group can't span text that breaks the column format.<br/>For the Range object's parameters, see the following table.<br/><br/> |
| sections              |                        | Specifies sections inside sections. Use this for complex sections that contain nested repeated elements, for example, [a grid of tables](doc:sections-example-table-grid). Each nested section searches for its range inside the parent section's range. |
| display               | boolean. Default: true | Specifies to display the sections' ranges as overlays on the rendered PDF in the Sensible app. Useful for troubleshooting.<br/> |

- TODO: update the "color coding" docs w/ red brackets for DISPLAY



SCREENSHOTS
----

ready to update: 

sections_2

vertical_section_table_grid_1



NOT UPDATING YET:



- buggy: vertical_sections_labeled_rows.png 
- buggy: vertical_sections_table_in_table.png 
- suprress output problem (pending fix?):  vertical_sections_zip.png
- supress output: copy_from_sections.png 
