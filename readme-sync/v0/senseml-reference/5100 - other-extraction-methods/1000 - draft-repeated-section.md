---
title: "Repeated section"
hidden: true
---

Extracts data from a section of the document that contains repeated elements. Sensible returns an array of  objects containing repeated fields. The following image shows an example of a repeated section:

![](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/images/final/repeated_sections_example.png)

For the preceding example, you can configure Sensible to return a `claims` array, where each object in the array contains a `claim_number`, `claimant_last_name`, `claim_date`, etc. 

[**Parameters**](doc:draft-repeated-section#section-parameters)
[**Examples**](doc:draft-repeated-section#section-examples)



Parameters
====


| key                   | value                                                  | description                                                  |
| --------------------- | ------------------------------------------------------ | ------------------------------------------------------------ |
| id (**required**)     | string                                                 | the id of the section. You can have multiple sections in a document, and you can nest sections inside of other sections. The repeating elements can contain nonrepeating text. |
| range  (**required**) | object                                                 | Specifies to search for repeated elements between matching Start and Stop parameters. Contains these parameters:<br/><br/>**start**-an [Anchor](doc:anchor) or string object that defines both 1. start of the section and 2. the start of the repeating elements within the section. Use this parameter to match the first line in the repeating element.  <br/> For example, if you specify `"start": "claim number"` in the preceding image, Sensible searches for repeating fields from "Claim number" up to the next instance of "Claim number".  Do NOT match on text preceding the repeating elements but not a part of the repeating elements.<br/><br/> **stop**-a string or [Match](doc:match) object or array of Match objects that defines the end of the section. <br/>For example, in the preceding image, `"stop":"claims totals"`.<br/> |
| fields (**required**) | array of [Field objects](doc:field-query-object)       | The fields in each repeating element that you want to extract repeatedly.  If the field anchor matches to data that falls outside the Range parameter, the field returns null. |
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
			"id": "claims_unprocessed_section",
			"range": {

				"start": {
					"type": "startsWith",
					"text": "Claim number",
					"isCaseSensitive": true
				},
				"stop": "claims totals"
			},
			"fields": [{
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
				}
			]
		}
	]
}
```

**PDF**

The following image shows the data extracted by this config for the following example PDF:

![Click to enlarge](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/images/final/tbd_example.png)

| Example PDF | [Download link](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/pdfs/repeated_section_example.pdf) |
| ------------------- | ------------------------------------------------------------ |

**Output**

```json
{
  "example_field_outside_repeated_section": {
    "type": "string",
    "value": "Unprocessed claims section"
  },
  "claims_unprocessed_section": [
    {
      "claim_number_repeats": {
        "source": "1223456789",
        "value": 1223456789,
        "type": "number"
      },
      "last_name_repeats": {
        "type": "string",
        "value": "Diaz"
      }
    },
    {
      "claim_number_repeats": {
        "source": "9876543211",
        "value": 9876543211,
        "type": "number"
      },
      "last_name_repeats": {
        "type": "string",
        "value": "Badawi"
      }
    },
    {
      "claim_number_repeats": {
        "source": "6754329876",
        "value": 6754329876,
        "type": "number"
      },
      "last_name_repeats": {
        "type": "string",
        "value": "Smith"
      }
    },
    {
      "claim_number_repeats": {
        "source": "6785439210",
        "value": 6785439210,
        "type": "number"
      },
      "last_name_repeats": {
        "type": "string",
        "value": "Levy"
      }
    }
  ]
}
```

Notes
-----

