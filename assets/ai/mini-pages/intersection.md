## Intersection


Finds and extracts the value at the point where a row and a column cross in a table, like looking up a cell in a spreadsheet by naming both its row and column. More reliable than the Row method when a table has unpredictably empty cells. Can be used outside tables in any grid-like layout: finds and extracts text at the point where a horizontal line and a vertical line drawn through two anchor phrases intersect on the page. Use `width` and `height` to define a capture region around the intersection point.

**Syntax**
```json
{
  "id": "bodily_injury_per_occurrence", /* extracts a dollar amount in a table labeled by "bodily injury" and "per occurrence", e.g., extracts "$500,000"*/
  "anchor": "bodily injury",            /* sets the horizontal line  — e.g. a row in a policy limits table */
  "method": {
    "id": "intersection",
    "verticalAnchor": "per occurrence", /* sets the vertical line  — e.g. a column heading */
    "width": 1.5,                       /* width of the capture region at the intersection point in inches */
    "height": 0.4                       /* height of the capture region at the intersection point in inches */
  }
}
```

[Full docs](https://docs.sensible.so/docs/intersection)
