## Box

Extracts every line of text found inside a bordered rectangle on your document. You point it at a word or phrase that's reliably printed in or near the box — Sensible searches outward from that point until it finds the border. Works with light-background, solid-border boxes; dark-background boxes need a small threshold adjustment. If the locating text is outside the box, use `offsetX`/`offsetY` to nudge the search starting point inside the border.

**Syntax**
```json
{
  "id": "rents_income",
  "anchor": "rents",           /* matches "Rents" printed inside the box on the 1099 — locates the box */
  "method": {
    "id": "box"                /* grabs everything else in that box — e.g. "4,200.00" from the Rents field on a 1099-MISC (the anchor itself is excluded) */
  }
}
```
