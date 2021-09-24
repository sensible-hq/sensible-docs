---
title: "Sections"
hidden: true
---

Extracts data from a section of the document that contains repeated elements. Sensible returns an array of objects corresponding to the elements. The following image shows an example of a repeated section:

![](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/images/final/repeated_sections.png)

For the preceding example, you can configure Sensible to return a `unprocessed_claims` array of objects, where each object contains a `claim_number`, `claim_date`, `claimant_last_name`, etc.

Parameters
====


| key                   | value                                                  | description                                                  |
| --------------------- | ------------------------------------------------------ | ------------------------------------------------------------ |
| id (**required**)     | string                                                 | the id of the section. You can have multiple sections in a document, and you can nest sections inside of other sections. |
| range  (**required**) | object                                                 | Specifies to search for repeated elements between matching Start and Stop parameters. Contains these parameters:<br/><br/>**anchor**-an [Anchor](doc:anchor) or string object that defines the start of the section. Specify the first line in each repeating element for this element. For example, in the preceding image, specify `"Claim number"`.  <br/> **stop** - a string or [Match](doc:match) object or array of Match objects that defines the end of the section. In the preceding image, for example, `"Claims totals"`.<br/> |
| fields (**required**) | array of [Field objects](doc:field-query-object)       | The fields in each repeating element that you want to extract repeatedly as an array.  If the field anchor doesn't correspond to a repeating element, or if it matches to data that falls outside the Range parameter, the field returns null. In the preceding example, you can extract `date_of_claim` and `phone_number` in a section, but you can extract  `total_unprocessed_claims`  only in the main fields array, not in a section. |
| computedFields        | array of [Computed fields](doc:computed-field-methods) | Transform the output of the fields.                          |

Examples
====

**Config**

```json

```

**PDF**

The following image shows the data extracted by this config for the following example PDF:

![Click to enlarge](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/images/final/tbd.png)

| Example PDF | [Download link](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/pdfs/row_column.pdf) |
| ------------------- | ------------------------------------------------------------ |

**Output**

```json

```

Notes
-----

- You can use a repeating section to: 