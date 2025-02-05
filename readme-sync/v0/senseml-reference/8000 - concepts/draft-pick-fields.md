---
title: "pick fields draft"
hidden: true
---

Returns the specified fields. Takes an array of two items:

- an object to get fields from
- an array of field IDs to pick

```json
{
  "pick_fields": [
    sourceObject,
    ["field_id_1", "field_id_2", "field_id_3"]
  ]
}
```

The Pick Fields operator returns an empty object if:

- you pass an empty array as the second argument, or if Sensible can't find the specified field IDs
- the source is empty, null, or undefined

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
  "pick_fields": [
    // `"var": ""` returns the current context, in this case, the preceding extracted fields
    { "var": "" },
    // the IDs of the fields to be returned by the rule
    ["field_morning", "field_afternoon"]
  ]
}
```

the rule outputs:

```json
{
  "field_morning": "good morning",
  "field_afternoon": "good afternoon"
}
```

#### Example 2

For a complete example, see [Advanced: Transform sections data](doc:sections-example-copy-to-section).
