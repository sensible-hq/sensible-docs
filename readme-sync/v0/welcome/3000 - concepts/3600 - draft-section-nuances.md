---
title: "Section nuances"
hidden: true
---

**Note:** If you're familiar with Sensible, this detailed topic is for you. If you're new to Sensible, see [sections](doc:sections).





The following images show the differing behaviors of sections vs vertical sections:

Sections
-----

![Click to enlarge](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/images/final/sections_concept_horizontal.png)

Sensible:

1. Finds the vertical range (y-extent) for a section in the group based on text matching. if no Range:Stop, next section's range starts at next Anchor:Match +yOffset. This ensures sections’ ranges never overlap. 
2.  (repeats) Continues finding ranges for sections, searching down the page and across page breaks.
3. Extracts fields from each section in the group. Extract anythingin the y-extent (can include tables or other complex data); usually the data is in a repeated structure

 

Vertical sections
-----



![Click to enlarge](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/images/final/sections_concept_vertical.png)

Sensible:

1. Finds the vertical range (y-extent) in which to recognize columns.  Ignores any non-column text above or below columns in the range, except if the Stop parameter is unspecified, uses non-column text as a criteria to end the range. 
2. (repeats) Recognizes columns based on whitespace, searching left-to-right and across page breaks. If columnSelection is specified, extract only from those target columns, and treat other columns as row labels, whose text is appended to the target columns. Extract anything in the column in the range (can include nested tables or other complex data). Usually it’s in a repeated structure.

