## Box

Extracts every line of text found inside a bordered rectangle on your document. You anchor it to any text that reliably appears near the box — Sensible searches outward from that point until it finds the border. Works with light-background, solid-border boxes; dark-background boxes need a small threshold adjustment. If your anchor text is outside the box, use `offsetX`/`offsetY` to nudge the search starting point inside the border.

**Syntax**
```json
{
  "id": "rents_income",
  "anchor": "rents",          /* text near or inside the target box */
  "method": {
    "id": "box",              /* grabs everything inside the box borders */
    "position": "right"       /* where to start searching for the border, relative to the anchor */
  }
}
```
