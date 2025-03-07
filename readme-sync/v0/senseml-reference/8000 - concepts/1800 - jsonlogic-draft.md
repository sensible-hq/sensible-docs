---
title: "omit fields, merge objects"
hidden: true
---

*TODO: style guide:* 

- *operation or operator* 

+ *how to relate that to 'rule' , 'condition' or 'logic'? be consistent across this + other topics*

## Omit fields

For an array of fields, removes the specified fields from the array. Takes an array of two items:

- an object to get fields from
- an array of field IDs to omit

```json
{
  "omit_fields": [
    sourceObject,
    ["field_id_1", "field_id_2", "field_id_3"]
  ]
}
```

Edge cases:

- The Omit Fields operator returns an empty object if the source object is empty, null, or undefined
- The Omit Fields operator returns the original source object if it can't find the specified fields to omit.

### Examples

#### Example 1

As a simplified example, given the following extracted fields:

```json
{
  "field_morning": "good morning",
  "field_afternoon": "good afternoon",
  "field_evening": "good evening"
}
```

if you apply the rule:

```json
{
  "omit_fields": [
    // `"var": ""` returns the current context, in this case, the preceding extracted fields
    { "var": "" },
    // the IDs of the fields to be omitted
    ["field_morning"]
  ]
}
```

the rule outputs:

```json
{
  "field_afternoon": "good afternoon",
  "field_evening": "good evening"
}
```

#### Example 2

The following example shows removing extracted IDs from the [postprocessed](doc:postprocessor) output for a W-2 form.

**Config**

```json
{
  "postprocessor": {
    "type": "jsonLogic",
    "rule": {
      "eachKey": {
        "extraction_w_ids_removed": {
          "omit_fields": [
            {
              /* in postprocessor output,
              omit `employers_id` and `employees_ssn`
              from the array of all extracted fields,
              `["state", "state_wages", "state_tax", ...]`
              */
              "var": ""
            },
            [
              "employers_id",
              "employees_ssn"
            ]
          ]
        }
      }
    }
  },
  "fields": [
    {
      "method": {
        "id": "queryGroup",
        "queries": [
          {
            "id": "state",
            "description": "state",
            "type": "string"
          },
          {
            "id": "state_wages",
            "description": "state wages",
            "type": "string"
          },
          {
            "id": "state_tax",
            "description": "state income tax",
            "type": "string"
          },
          {
            "id": "employers_id",
            "description": "employers_id",
            "type": "string"
          },
          {
            "id": "employees_ssn",
            "description": "employees_ssn",
            "type": "string"
          }
        ]
      }
    }
  ]
}
```

**Example document**
The following image shows the example document used with this example config:

![Click to enlarge](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/images/final/omit_fields.png)

| Example document | [Download link](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/pdfs/omit_fields.pdf) |
| ---------------- | ------------------------------------------------------------ |

**Postprocessor output**

```json
{
  "extraction_w_ids_removed": {
    "state": {
      "value": "CA",
      "type": "string",
      "confidenceSignal": "confident_answer"
    },
    "state_wages": {
      "value": "52231.46",
      "type": "string",
      "confidenceSignal": "confident_answer"
    },
    "state_tax": {
      "value": "3461.27",
      "type": "string",
      "confidenceSignal": "confident_answer"
    }
  }
}
```

**Extraction output**

```json
{
  "state": {
    "value": "CA",
    "type": "string",
    "confidenceSignal": "confident_answer"
  },
  "state_wages": {
    "value": "52231.46",
    "type": "string",
    "confidenceSignal": "confident_answer"
  },
  "state_tax": {
    "value": "3461.27",
    "type": "string",
    "confidenceSignal": "confident_answer"
  },
  "employers_id": {
    "value": "12-3456789",
    "type": "string",
    "confidenceSignal": "confident_answer"
  },
  "employees_ssn": {
    "value": "123-45-6789",
    "type": "string",
    "confidenceSignal": "confident_answer"
  }
}
```



=======

**Note:** For the full list of parameters available for this method, see [Global parameters for methods](doc:method#section-global-parameters-for-methods). The following table only shows parameters most relevant to or specific to this method.

## Merge objects

For an array of objects, rreturns a signel object containing t all the fields from each object. 

Edge cases:

- *If passed an empty array, it returns an empty object*
- *If passed an array containing a value that is `null` or `undefined`, ignores that value but still returns an object based on object values that were passed*
- *If passed an array containing a value that is not an object, `null`, or `undefined`, throws an error*
- *If passed multiple fields that use the same key, uses the **last** value that is passed for that key (same rules as when spreading JS objects)*

For example:

```json
{ // todo: example w/o eachKey?
  "merge_objects": [
    { "eachKey": { "field1": "hello" } },
    { "eachKey": { "field2": "world" } }
  ]
}

```



returns:

``` json
{
  "field1": "hello",
  "field2": "world"
}
```



### Examples

#### Example 1

As a simplified example, given the following extracted fields:

```json
{
  "field_morning": "good morning",
  "field_afternoon": "good afternoon",
  "field_evening": "good evening"
}
```

if you apply the rule:

```json
{
  "omit_fields": [
    // `"var": ""` returns the current context, in this case, the preceding extracted fields
    { "var": "" },
    // the IDs of the fields to be omitted
    ["field_morning"]
  ]
}
```

the rule outputs:

```json
{
  "field_afternoon": "good afternoon",
  "field_evening": "good evening"
}
```

#### Example 2

For a complete example, see TODO TBD.