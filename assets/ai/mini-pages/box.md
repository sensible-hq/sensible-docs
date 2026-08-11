## Box

Extracts every line of text found inside a bordered rectangle on your document. Specify a word or phrase that's reliably printed in or near the box, and Sensible searches outward from that point until it finds the border. Works with light-background, solid-border boxes; dark-background boxes need a threshold adjustment. If the locating text is outside the box, use `offsetX` or `offsetY` to nudge the search starting point inside the border.

**Syntax**
```json
{
  "id": "rents_income",
  "anchor": "rents",           /* matches "Rents" printed inside a box on a 1099-MISC, locates the box */
  "type": "currency",          /* formats raw text "4,200.00" into a structured value: { "value": 4200, "unit": "$" } */
  "method": {
    "id": "box",               /* extracts everything else in that box (the anchor itself is excluded) */
    "wordFilters": ["corrected"] /* ignores lines containing "corrected" — e.g. a CORRECTED stamp on an amended 1099 */
  }
}
```

[Full docs](https://docs.sensible.so/docs/box)
