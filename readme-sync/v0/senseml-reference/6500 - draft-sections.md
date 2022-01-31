---
title: "Sections"
hidden: true
---

Extracts data from a document that contains complex or repeated elements ("sections").  In effect, a "section" defines a repeating document inside a document, with its own fields.

Sensible returns an array of objects corresponding to the sections. The following image shows an example of a document containing repeated "claims" sections:

![Click to enlarge](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/images/final/sections_1.png)

For the preceding example, you can configure Sensible to return an `unprocessed_claims` array, where each object in the array contains a `claim_number`, `claim_date`, `claimant_last_name`, etc. 

Parameters
====


| key                   | value  | description                                                  |
| --------------------- | ------ | ------------------------------------------------------------ |
|                       |        |                                                              |
| range  (**required**) | object | Specifies the range of both:<br/>- a collection of repeated sections in an area of the document <br/>- the start and end of each repeated section.<br/><br/>The collection of sections can span nonrepeating text. For example,  in the preceding image, an "unprocessed_claims" collection of sections could span month headings.<br/><br/>Contains these parameters:<br/><br/>**anchor** (**required**): <br/>  &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;**start**: ignores anything in the document before this line. if undefined, the section collection starts at the beginning of the document<br/>    &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;**match** (**required**): specifies the starting line of each repeating section. For example, in the preceding image, specify `"Claim number"`. If the start of the section lacks an easy-to-match line, you can use the Require Stop and Offset Y parameters to start the section on a line other than the one matched by this parameter.<br/>    &nbsp;&nbsp;&nbsp;&nbsp;**end**: ignores anything in the document after this line. If unspecified, the section collection continues to the end of the document. For example, to extract solely September claims in the preceding image, specify `"October"`.<br/><br/><br/>**stop:** a string, [Match](doc:match) object, or array of Match objects that specifies the end of the repeated section after its anchor. For example, if you specify `"Date of claim"`, then each section ends either when it encounters the next section's starting line, or when it encounters the phrase "Date of claim". Sensible ignores any text after the claimant's last name in each repeating element. <br/> If you leave this parameter unspecified, then the last repeating element in the section continues to the end of the document.<br/><br/><br/>**requireStop:**<br/> If true, the section ends when it matches the Stop parameter, instead of the default behavior of ending at the next starting line specified in the anchor's Match parameter. For example, use this parameter when the starting line repeats in the section, to avoid ending the section before it completes.<br/><br/>**offsetY:** specifies the number of inches to offset the start of the section from the anchor Match parameter. By default a section starts at the top boundary of the matched line. If you specify Offset Y, the section starts at that top boundary plus the offset. This is useful when the section lacks an easy-to-match first line.<br/><br/><br/><br/>**direction**: default: `horizontal`. If set to `vertical`, Sensible searches for repeating sections arranged in columns. See following section for an example.<br/><br/><br/>**columnSelection** : string. use only if `"direction":"vertical"`. default:  `0, -1` (all columns). Select the columns you want to output using zero-based indices or indices ranges. For example, `0-5` for columns 1 through 6, `1,3,-1`  columns 2, 4, and the last column, `1, 3-7` for column 2, and columns 4 through 8 .  Use negative indices to indicate offsetting from the last element of the column array. <br/><br/><br/><br/>**minSpace** : use only if `"direction":"vertical"`.  default: the average line height for all the lines in the section. The number of characters to define a min separation between texts to define a new column otherwise in some cases you will get 1 column split into 2.<br/><br/><br/><br/> |
|                       |        |                                                              |
|                       |        |                                                              |
|                       |        |                                                              |

Examples
====



|  |  |
| ------------------- | ------------------------------------------------------------ |

**Output**

```json

```

