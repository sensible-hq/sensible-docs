---
title: "Sections"
hidden: false
---

Extracts data from a document that contains complex or repeated elements ("sections").  In effect, a "section" defines a repeating document inside a document, with its own fields.

The following image shows an example of a document containing "claims" sections, where each section starts with `claim number` and ends below `date of claim`: TODO: UPDATE SCREENSHOT W GREEN BRACKETS and/or red outlines!! 

![Click to enlarge](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/images/final/sections_1.png)

For the preceding example, you can configure Sensible to return an `unprocessed_claims` array, where each object in the array contains a `claim_number`, `claim_date`, `claimant_last_name`, and other fields.  For more information, see [Claims loss run example](doc:sections-example-loss-run).



You can define "horizontal" sections (`"direction": "horizontal"`), as shown in the preceding image, or you can define columnar sections (`"direction":"vertical"`). 

**Horizontal sections:**

The following image shows horizontal sections. For more information, see the following Parameters section, and see [Section nuances](doc:section-nuances).

![Click to enlarge](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/images/final/sections_concept_horizontal.png)

**Vertical sections:**

The following image shows columnar vertical sections.  For more information, see the following Parameters section, and see [Section nuances](doc:section-nuances).

![Click to enlarge](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/images/final/sections_concept_vertical.png)

**Tip:** To extract repeated vertical section groups, nest them in parent sections.  For an example, see [Advanced: nested columns example](doc:sections-example-nested-columns).

Parameters
====


| key                   | value                                                  | description                                                  |
| --------------------- | ------------------------------------------------------ | ------------------------------------------------------------ |
| id (**required**)     | string                                                 | Specifies an ID for a group of sections to extract in the document area defined by the Range parameter. You can define an array of section groups, and you can nest sections inside of other sections. |
| type                  | `sections`                                             | Specifies that this field extracts sections.                 |
| range  (**required**) | object                                                 | Specifies the document area from which to extract a group of sections.<br/> **horizontal sections:**  The sections can span pages and non-section text. For example, in the preceding claims image, sections can interleave with month headings.<br/><br/> **vertical sections:** The sections can span pages. By default, they can't span text that breaks the column format.<br/>For the Range object's parameters, see the following table. |
| sections              |                                                        | Specifies sections inside sections. Use this for complex sections that contain nested repeated elements, for example, [a grid of tables](doc:sections-example-table-grid). Each nested section searches for its range inside each parent section's range. |
| display               | boolean. Default: true                                 | Specifies to display the start and end of each section as brackets overlaid on the rendered document in the Sensible app. Use the brackets to visually troubleshoot sections. |
| requiredFields        | object                                                 | Array of field IDs that must be non-null for Sensible to return a section.<br/> In the [Claims loss run example](doc:sections-example-loss-run), add the following code to the sections to omit claims that lack a phone number: <br/> `"requiredFields": ["phone_number"],`<br/>With the preceding code, Sensible omits claim number `9876543211`  from the example output. |
| fields                | array of [fields](doc:field-query-object)              | Specifies fields to extract information that you expect to repeat in each section. |
| computed_fields       | array of [computed fields](doc:computed-field-methods) | Specifies to output computed fields to each section. The computed fields have access to each section's fields. To get access to and transform the output of fields that aren't in the sections' range, use the [Copy To Section](doc:copy-to-section) method. |

### Range parameters

TODO add new table here

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



