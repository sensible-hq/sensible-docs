<!-- status: draft. Agent-written fixture; a human has not reviewed it. -->

The following example shows the Concatenate method:

```json
{
  "fields": [],
  "computed_fields": [
    {
      "id": "full_name",
      "method": {
        "id": "concat",
        "source_ids": ["first_name", "last_name"]
      }
    }
  ]
}
```
