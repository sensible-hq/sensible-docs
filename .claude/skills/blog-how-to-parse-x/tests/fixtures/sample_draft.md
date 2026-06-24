# How to extract data from sample documents with Sensible

Some introductory text here.

## Extract the departure date

```json5
/* Sensible uses JSON5 to support in-line comments*/
{
  "id": "departure", /* field name in output */
  "type": "date", /* output as ISO 8601 date */
  "anchor": {
    "match": { "type": "equals", "text": "departure" } /* exact match */
  },
  "method": { "id": "label", "position": "below" } /* grab text below label */
}
```

Output:

```json
{
  "departure": {
    "type": "date",
    "value": "2024-01-15T00:00:00.000Z"
  }
}
```

## Putting it all together

<!-- CONFIG:START -->
```json5
/* Sensible uses JSON5 to support in-line comments*/
{
  "fingerprint": {
    "tests": [
      { "type": "startsWith", "text": "delivery order" }
    ]
  },
  "fields": [
    {
      "id": "departure", /* field name in output */
      "type": "date", /* output as ISO 8601 date */
      "anchor": {
        "match": { "type": "equals", "text": "departure" } /* exact match */
      },
      "method": { "id": "label", "position": "below" } /* grab text below label */
    }
  ]
}
```
<!-- CONFIG:END -->

You'll get this output:

```json
{
  "departure": {
    "source": "Mar 14 2023",
    "value": "2023-03-14T00:00:00.000Z",
    "type": "date"
  }
}
```
