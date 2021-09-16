---
title: "Repeated Section"
hidden: true
---

Extracts data from a section of the document that contains repeated elements. Sensible returns an array of  objects containing repeated fields. The following image shows an example of a repeated section:

![](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/images/final/repeated_sections_example.png)

For the preceding example, you can configure Sensible to return a `claims` array of objects, where each object contains a `claim_number`, `claim_date`, `claimant_last_name`, etc.

Parameters
====


| key                   | value                                                  | description                                                  |
| --------------------- | ------------------------------------------------------ | ------------------------------------------------------------ |
| id (**required**)     | string                                                 | the id of the section. You can have multiple sections in a document, and you can nest sections inside of other sections. |
| range  (**required**) | object                                                 | Specifies to search for repeated elements between matching Start and Stop parameters. Contains these parameters:<br/><br/>**start**-an [Anchor](doc:anchor) or string object that defines the start of the section. <br/>Match the first line in the repeating element for this parameter.<br/>ALT: Specify the same value for this parameter as for the anchor of the first field you want to extract in each repeating element. <br/>For example, in the preceding image, specify `"start": "claim number"`  .**QUESTION: so if you wanted to skip 'claim number, could you specify 'claimant last name' here, have no "claim number" field and it would work out OK? what would happen if you added the 'claim number' field but didn't have it in the range?** <br/><br/> **stop**-a string or [Match](doc:match) object or array of Match objects that defines the end of the section. <br/>In the preceding image, for example, `"stop":"claims totals"`.<br/> |
| fields (**required**) | array of [Field objects](doc:field-query-object)       | The fields in each repeating element that you want to extract repeatedly as an array.  If the field anchor doesn't correspond to a repeating element, or if it matches to data that falls outside the Range parameter, the field returns null. |
| computedFields        | array of [Computed fields](doc:computed-field-methods) | Transform the output of the fields.                          |

Examples
====

**Config**

```json

```

**PDF**

The following image shows the data extracted by this config for the following example PDF:

![Click to enlarge](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/images/final/tbd_example.png)

| Example PDF | [Download link](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/pdfs/row_column_example.pdf) |
| ------------------- | ------------------------------------------------------------ |

**Output**

```json

```

Notes
-----

- You can use a repeating section to: 