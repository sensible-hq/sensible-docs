## Box

Extracts every line of text found inside a bordered rectangle on your document. You point it at a word or phrase that's reliably printed in or near the box — Sensible searches outward from that point until it finds the border. Works with light-background, solid-border boxes; dark-background boxes need a small threshold adjustment. If the locating text is outside the box, use `offsetX`/`offsetY` to nudge the search starting point inside the border.

**Syntax**
```json
{
  "id": "rents_income",        /* name for the value you're extracting — e.g. rental income from a 1099 tax form */
  "anchor": "rents",           /* a word printed on the form near the target box — e.g. the label "Rents" */
  "method": {
    "id": "box",               /* tells Sensible to grab everything printed inside that bordered box */
    "position": "right"        /* start looking for the box border to the right of the anchor text */
  }
}
```
