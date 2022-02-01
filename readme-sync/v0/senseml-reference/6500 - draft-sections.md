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
| range  (**required**) | object | Specifies the range of both:<br/>- a group of repeated sections in an area of the document <br/>- the start and end of each repeated section.<br/><br/>The sections group can span pages and nonrepeating text. For example,  in the preceding image, an "unprocessed_claims" section group could span month headings.<br/><br/>Contains these parameters:<br/><br/>**anchor** (**required**): <br/>  &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;**start**: ignores anything in the document before this line. if undefined, the section group starts at the beginning of the document<br/>    &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;**match** (**required**): specifies the repeated starting line of each section. The section's top boundary is a horizontal line defined by the top boundary of this starting line. For example, in the preceding image, specify `"Claim number"`. If the start of the section lacks an easy-to-match line, you can use the Require Stop and Offset Y parameters to start the section on a line other than the one matched by this parameter.<br/>    &nbsp;&nbsp;&nbsp;&nbsp;**end**: ignores anything in the document after this line. If unspecified, the section group continues to the end of the document. For example, to extract solely September claims in the preceding image, specify `"October"`.<br/><br/><br/>**stop:** a string, [Match](doc:match) object, or array of Match objects that specifies the repeated end of the section after its anchor. The section's bottom boundary is a horizontal line defined by the top boundary of this stop line. For example, if you specify `"Date of claim"`, then each section ends when it encounters the phrase "Date of claim". Sensible ignores any text after the claimant's last name in each section. <br/> If unspecified, each section's bottom boundary is a horizontal line defined by the next section's starting line (plus any offset). In this case, the last section in the group continues to the end of the document.<br/><br/><br/>**requireStop:**<br/> If true, the section ends when it matches the Stop parameter, instead of the default behavior of ending at the next starting line specified in the anchor's Match parameter. For example, use this parameter when the starting line repeats in the section, to avoid ending the section before it completes.<br/><br/>**offsetY:** specifies the number of inches to offset the section's top boundary from the anchor Match parameter. By default a section starts at the top boundary of the matched line. If you specify Offset Y, the section starts at that top boundary plus the offset. This is useful when the section lacks an easy-to-match first line.<br/><br/><br/><br/>**direction**: default: `horizontal`. If set to `vertical`, Sensible searches left-to-right for columns in the vertical document range defined by the first-found text matches for Range parameter, rather than repeatedly searching for text matches for the Range parameter. For an illustration, see TODO LINK section nuances. Use this, for example, to extract tables nested in tables, tables with both column and row labels,  or other complex data layouts. See following section for examples.<br/><br/><br/>**columnSelection** :  number array. use only with vertical sections ( `"direction":"vertical"`). default:  `[0, -1]` (all columns). Select the columns you want to output using zero-based indices or indices ranges. For example, `[0-5]` for columns 1 through 6, `[1,3,-1]`  columns 2, 4, and the last column, `[1, 3-7]` for column 2, and columns 4 through 8 .  Use negative indices to indicate offsetting from the last element of the column array. <br/><br/><br/><br/>**minSpace** : use only with vertical sections ( `"direction":"vertical"`).  default: the average line height for all the lines in the section. The number of characters to define a min separation between texts to define a new column, otherwise in some cases you will get 1 column split into 2.<br/><br/><br/><br/> |
| sections              |        | Specifies sections inside sections. Use this for complex sections that contain nested repeated elements. Each nested section is scoped by each the parent section's Range parameter. |
|                       |        |                                                              |
|                       |        |                                                              |

Examples
====



Vertical sections: complex tables
----

vertical_section_table_in_table.pdf










Vertical sections: overviews
----

To give a broad overview of other possible uses of vertical sections:

![Click to enlarge](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/images/final/vertical_sections_col_sect.png)





In the preceding image, to capture both the Sections and their Columns, 1 define a section then 2.  define a nested vertical section.  Using abbreviated YML notation to give a brief idea of the more complex SenseML JSON: 

```yml
sections:
  - id: parentSections
    range:
      anchor: Section
    fields:
      - id: sectionTitle
        anchor: Section
        method:
          id: passthrough
   sections:
     - id: nestedColumns
       range:
         direction: vertical
         anchor: column
       fields:
         - id: columnTitle
           anchor: column
           method:
             id: passthrough
     
      
```

With this approach, you can output something like the following, using abbreviated YML notation to give a brief idea of the more complex JSON API response:
```yml
parentSections:
  - sectionTitle: Section 1
    nestedColumns:
      columnTitle: Column A
      columnTitle: Column B
      columnTitle: Column C
 - sectionTitle: Section 2
    nestedColumns:
      columnTitle: Column A
      columnTitle: Column B
      columnTitle: Column C  
   
```

Notes
===

To better understand vertical sections, see section-nuances.
