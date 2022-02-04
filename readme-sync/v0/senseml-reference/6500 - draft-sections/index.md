---
title: "Sections"
hidden: true
---

Extracts data from a document that contains complex or repeated elements ("sections").  In effect, a "section" defines a repeating document inside a document, with its own fields.

Sensible returns an array of objects corresponding to the section group. The following image shows an example of a document containing a group of "claims" sections:

![Click to enlarge](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/images/final/sections_1.png)

For the preceding example, you can configure Sensible to return an `unprocessed_claims` array, where each object in the array contains a `claim_number`, `claim_date`, `claimant_last_name`, etc. 

Parameters
====


| key                   | value  | description                                                  |
| --------------------- | ------ | ------------------------------------------------------------ |
| id (**required**)     | string | Identifies a group of sections to extract in the document area defined by the Range parameter. You can define an array of section groups, and you can nest sections inside of other sections. |
| range  (**required**) | object | Identifies a group of sections to extract in the document area defined by the Range parameter. You can define an array of section groups, and you can nest sections inside of other sections. The Range parameter specifies both:<br/>- a group of repeated sections in an area of the document <br/>- the start and end of each repeated section.<br/><br/>The sections group can span pages and nonrepeating text. For example,  in the preceding image, an "unprocessed_claims" section group can span month headings.<br/><br/>For Range parameters, see the following table.<br/><br/> |
| sections              |        | Specifies sections inside sections. Use this for complex sections that contain nested repeated elements. Each nested section is scoped by each the parent section's Range parameter. |



**Range parameters**

See the following table for details about the Range object parameters:

| key                   | value                                                        | description                                                  |
| --------------------- | ------------------------------------------------------------ | ------------------------------------------------------------ |
| anchor (**required**) | [Anchor](anchor) object, or array of Match objects           | Anchor parameters have a special meaning in the context of sections, as follows:<br/> **start**: ignores anything in the document before this line. if undefined, the section group starts at the beginning of the document  <br/>**match** (**required**): specifies the repeated starting line of each section. The section's top boundary is a horizontal line defined by the top boundary of this starting line. For example, in the preceding image, specify `"Claim number"`. If the start of the section lacks an easy-to-match line, you can use the Require Stop and Offset Y parameters to start the section on a line other than the one matched by this parameter. <br/>**end**: ignores anything in the document after this line. If unspecified, the section group continues to the end of the document. For example, to extract solely September claims in the preceding image, specify `"October"`. |
| stop                  | [Anchor](anchor) object, or array of Match objects           | Specifies the repeated end of the section after its anchor. For example, if you specify `"Date of claim"`, then each section ends when it encounters the phrase "Date of claim". Sensible ignores any text after the claimant's last name in each section. The section's bottom boundary is a horizontal line defined by the top boundary of this stop line (plus any offset).  If this parameter is unspecified, each section's bottom boundary is a horizontal line defined by the next section's starting line (plus any offset). In this case, the last section in the group continues to the end of the document. |
| requireStop           | Boolean. default: false                                      | If true, the Stop parameter is required, and the section ends when it matches the Stop parameter, instead of the default behavior of ending at the next starting line specified in the anchor's Match parameter. For example, use this parameter when the starting line repeats in the section, to avoid ending the section before it completes. |
| offsetY               | number in inches                                             | Specifies the number of inches to offset the section's top boundary from the anchor Match parameter. By default a section starts at the top boundary of the matched line. If you specify Offset Y, the section starts at that top boundary plus the offset. This is useful when the section lacks an easy-to-match first line, or when you want to exclude non-columnar text from a vertical section. |
| stopOffsetY           | number in inches                                             | specifies the number of inches to offset the section's bottom boundary from the anchor Stop parameter. |
| direction             | `horizontal`, `vertical`. default: `horizontal`              | If set to `vertical`, Sensible searches left-to-right for columns in the document range defined by the first-found text matches for Range parameter, rather than the default behavior of repeatedly searching for text matches for the Range parameter. For an illustration, see [section nuances]doc:section-nuances TODO LINK). Use this, for example, to extract tables nested in tables, tables with row labels,  or other complex data layouts. In the vertical section's Fields object, you can use methods such as the Row method, Label method, and Document Range method. You can't use pixel-recognition based methods such as Table, or coordinate-based methods such as Region or Text Table. See the following section for examples. |
| columnSelection       | integer array. default: capture all columns                  | Use only with vertical sections ( `"direction":"vertical"`). Use to:<br/>- Select the columns you want to output using zero-based indices or indices ranges. <br>-  Specify to treat unselected columns as row labels, by excluding them from the specified indices. The text in unselected columns is "in scope" for each selected column section and can be used as anchors. For an illustration, see section-nuances#column-selection TODO LINK.<br/>For example, `[0-5]` for columns 1 through 6, <br/>`[1,3,-1]`  columns 2, 4, and the second-to-last column,<br/> `[1,3-7]` for column 2, and columns 4 through 8 .<br/> Use negative indices to indicate offsetting from the last element of the column array. <br/>  For more information, see the Examples section. |
| ignoreColumns         | integer array.                                               | TODO: check naming Use only with vertical sections ( `"direction":"vertical"`). Use to remove unwanted columns from both the output and from the SenseML search scope. This is useful, for example, if the columns contain text that interfers with anchoring on other columns. (Note that in contrast the Column Selection parameter removes unselected columns from the output but still makes them available to selected columns for field anchoring purposes.) |
| minColumnGap          | number in inches. default: the average line height for all the lines in the section. | Use only with vertical sections ( `"direction":"vertical"`).   Configures column recognition by specifying the minimum width of the gutters separating the columns. For example, if text in a column contains whitespace gaps such that Sensible can split 1 column into 2, set a minimum gap that is larger than the gaps within the column. Zero means "draw zero width vertical lines between columns to define column boundaries." |





Examples
====

See the following topics:

- [Example 1](doc:sections-example-1)
- [Example 2](doc:sections-example-2)
- [Example 3](doc:sections-example-3)
- [Example 4](doc:sections-example-4)



Notes
===

For details about vertical sections, see section-nuances TODO LINK

