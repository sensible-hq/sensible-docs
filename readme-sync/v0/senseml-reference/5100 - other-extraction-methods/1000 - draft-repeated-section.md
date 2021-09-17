---
title: "Repeated Section"
hidden: true
---

Extracts data from a section of the document that contains repeated elements. Sensible returns an array of  objects containing repeated fields. The following image shows an example of a repeated section:

![](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/images/final/repeated_sections_example.png)

For the preceding example, you can configure Sensible to return a `claims` array of objects, where each object contains a `claim_number`, `claimant_last_name`, `claim_date`, etc.

Parameters
====


| key                   | value                                                  | description                                                  |
| --------------------- | ------------------------------------------------------ | ------------------------------------------------------------ |
| id (**required**)     | string                                                 | the id of the section. You can have multiple sections in a document, and you can nest sections inside of other sections. |
| range  (**required**) | object                                                 | Specifies to search for repeated elements between matching Start and Stop parameters. Contains these parameters:<br/><br/>**start**-an [Anchor](doc:anchor) or string object that defines both 1. start of the section and 2. the start of the repeating elements within the section. Use this parameter to match the first line in the repeating element.  <br/> For example, if you specify `"start": "claim number"` in the preceding image, Sensible searches for repeating fields from "Claim number" up to the next instance of "Claim number". <br/><br/> **stop**-a string or [Match](doc:match) object or array of Match objects that defines the end of the section. <br/>For example, in the preceding image, `"stop":"claims totals"`.<br/> |
| fields (**required**) | array of [Field objects](doc:field-query-object)       | The fields in each repeating element that you want to extract repeatedly.  If the field anchor doesn't correspond to a repeating element, or if it matches to data that falls outside the Range parameter, the field returns null. |
| computedFields        | array of [Computed fields](doc:computed-field-methods) | Transform the output of the fields.                          |

Examples
====

**Config**

```json
{
	"fields": [{
		"id": "example_field_outside_repeated_section",
        "anchor": "unprocessed claims section",
		"method": {
			"id": "passthrough"
		}
	}],
	"repeatedSections": [

		{
			"id": "claims_unprocessed",
			"range": {

				"start": {
					"type": "startsWith",
					"text": "Claim number",
					"isCaseSensitive": true
				},
				"stop": "claims totals"
			},
			"fields": [

				{
					"id": "claims_unprocessed_repeats",
					"range": {

						"start": {
							"match": {
								"type": "startsWith",
								"text": "Claim number",
								"isCaseSensitive": true
							}
						},
						"stop": {
							"type": "startsWith",
							"text": "grand totals"
						}
					},
					"fields": [{
							"id": "last_name_repeats",
							"method": {
								"id": "label",
								"position": "right"
							},
							"anchor": {
								"match": {
									"type": "startsWith",
									"text": "claimant last name:"
								}
							}
						},
						{
							"id": "claim_number_repeats",
							"type": "number",
							"anchor": {
								"match": {
									"type": "startsWith",
									"text": "Claim number",
									"isCaseSensitive": true
								}
							},
							"method": {
								"id": "label",
								"position": "right"
							}
						},
						{
							"id": "claim_date_repeats",
							"type": "date",
							"anchor": {
								"match": {
									"type": "startsWith",
									"text": "Date of claim",
									"isCaseSensitive": true
								}
							},
							"method": {
								"id": "row",
								"position": "right",
								"tiebreaker": "first"
							}
						}
					]
				}
			]
		}
	}
}
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

