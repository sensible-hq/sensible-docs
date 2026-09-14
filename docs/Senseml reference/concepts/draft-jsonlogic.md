---
title: jsonlogic draft
excerpt: ''
deprecated: false
hidden: true
metadata:
  title: ''
  description: ''
  keywords:
    - custom computation
  robots: index

next: # Optional "what's next" recommendations
  description: custom computation
  pages:
    - type: basic
      slug: custom-computation
      title: custom computation

---

## Is Array

Returns `true` for arrays, including empty arrays. Returns `false` for `null`, objects, strings, and numbers.

```json
{ "is_array": JsonLogic }
```

For example, use Is Array to iterate over fields that can be either arrays or scalar values. When you iterate over all extracted fields with the [Map Object](doc:jsonlogic#map-object) operation using `{"var":""}`, `{"var":"value.value"}` returns null for fields that return arrays, because those fields have no `value` property. Use Is Array to detect those fields and handle them differently. For an example use case, see the [XML postprocessor](doc:xml-postprocessor).

### Example

The following example shows using Is Array with Map Object to transform values from a mix of scalar and array fields.

```json
/* Sensible uses JSON5 to support in-line comments*/
{
  "fields": [
    {
      "id": "transformed_fields", /* user-friendly ID for extracted target data */
      "method": {
        "id": "customComputation",
        "jsonLogic": {
          "mapObject": [
            {
              /*
                In practice, use {"var":""} to iterate over the entire parsed_document.
                This example uses preserve to supply hardcoded values for demonstration.
              */
              "preserve": {
                "order_status": { "value": "shipped", "type": "string" },
                "line_items": ["keyboard", "mouse"]
              }
            },
            {
              "if": [
                { "is_array": { "var": "value" } }, /* condition: true for array fields (e.g., line_items), false for scalar fields */
                { "map": [{ "var": "value" }, { "cat": [{ "var": "" }, "_processed"] }] }, /* then: transform each array element */
                { "cat": [{ "var": "value.value" }, "_processed"] } /* else: transform scalar field value */
              ]
            }
          ]
        }
      }
    }
  ]
}
```

The preceding code sample returns the following output:

```json
/* TODO: verify that Sensible wraps object results from customComputation the same way as scalar results */
{
  "transformed_fields": {
    "value": {
      "order_status": "shipped_processed",
      "line_items": ["keyboard_processed", "mouse_processed"]
    }
  }
}
```

## To Lower

Converts a string to lowercase. Takes as input:
- a string value: `{ "toLower": { "var": "field.value" } }`
- a string value wrapped in a single-element array: `{ "toLower": [{ "var": "field.value" }] }`

Returns null if the input is null or missing. Throws a configuration error if the input is not a string.

### Example

The following example shows using To Lower to compare an extracted state code case-insensitively.

```json
/* Sensible uses JSON5 to support in-line comments*/
{
  "fields": [
    {
      "id": "state_code", /* user-friendly ID for extracted target data */
      "method": {
        /*
          In practice, you'd extract this field from the document
          with a layout-based or LLM-based method.
          This example uses `constant` to supply a fixed value for demonstration.
        */
        "id": "constant",
        /* a document might output "CA", "ca", or "Ca" */
        "value": "Ca"
      }
    },
    {
      "id": "is_california", /* user-friendly ID for extracted target data */
      "method": {
        "id": "customComputation",
        "jsonLogic": {
          "==": [
            { "toLower": { "var": "state_code.value" } },
            "ca"
          ]
        }
      }
    }
  ]
}
```

The preceding code sample returns the following output:

```json
{
  "state_code": {
    "value": "Ca",
    "type": "string"
  },
  "is_california": {
    "value": true,
    "type": "boolean"
  }
}
```

## To Upper

Converts a string to uppercase. Follows the same conventions as [To Lower](doc:jsonlogic#to-lower) for input and output.

### Example

The following example shows using To Upper to normalize an extracted approval status to uppercase.

```json
/* Sensible uses JSON5 to support in-line comments*/
{
  "fields": [
    {
      "id": "approval_status", /* user-friendly ID for extracted target data */
      "method": {
        /*
          In practice, you'd extract this field from the document
          with a layout-based or LLM-based method.
          This example uses `constant` to supply a fixed value for demonstration.
        */
        "id": "constant",
        /* a document might say "approved", "APPROVED", or "Approved" */
        "value": "approved"
      }
    },
    {
      "id": "normalized_status", /* user-friendly ID for extracted target data */
      "method": {
        "id": "customComputation",
        "jsonLogic": {
          "toUpper": { "var": "approval_status.value" }
        }
      }
    }
  ]
}
```

This returns:

```json
{
  "approval_status": {
    "value": "approved",
    "type": "string"
  },
  "normalized_status": {
    "value": "APPROVED",
    "type": "string"
  }
}
```

<br />
