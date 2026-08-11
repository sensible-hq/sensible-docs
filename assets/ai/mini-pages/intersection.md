## Intersection

Finds and extracts text at the point where two lines of text cross on the page — one sets the horizontal position, the other sets the vertical. More reliable than the Row method when a table has unpredictably empty cells. It's most commonly used with tables, where the two lines of text are a row label and a column heading, but it works with any layout where text is positioned in a grid-like arrangement. Use `width` and `height` to define a capture region around the crossing point; without them, Sensible extracts anything that touches the exact point. When cells are unpredictably empty, Intersection is more reliable than the Row method, which can return values from the wrong column.

**Syntax**
```json
{
  "id": "bodily_injury_per_occurrence",
  "anchor": "bodily injury",            /* sets the horizontal position — e.g. a row in a policy limits table */
  "method": {
    "id": "intersection",
    "verticalAnchor": "per occurrence", /* sets the vertical position — e.g. a column heading */
    "width": 1.5,                       /* width of the capture region in inches */
    "height": 0.4                       /* height of the capture region in inches — e.g. extracts "$500,000" */
  }
}
```
