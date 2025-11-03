---
title: "draft Linearize"
hidden: true
---



DRAFT

**Note:** This is advanced. for most use cases, see Multicolumn. TODO look up other wordings

Use this preprocessor for documents containing columns of text that the Multicolumn (TODO LINK) preprocessor can't recognize. 

Ensures that Sensible [sort lines](doc:lines#line-sorting) into the specified, coordinate-based blocks,  rather than the default behavior of sorting lines left to right across the page.

[**Parameters**](doc:linearize#parameters)
[**Examples**](doc:linearize#examples)
[**Notes**](doc:linearize#notes)

Parameters
====

| key                    | value                                                        | description                                                  |
| ---------------------- | ------------------------------------------------------------ | ------------------------------------------------------------ |
| type (**required**)    | `linearize`                                                  | *Recognizes multi-column layouts in documents and sorts lines into blocks in whatever or you specify.* |
| match<br/>or<br/>range | [Match](doc:match) object or array of Match objects<br/><br/>or<br/><br/>Range object TODO LINK? | Specifies the matching pages or repeating sections ("ranges") in which to run this preprocessor.<br/>`match`: TODO HOW TO FORMAT?<br/>or<br/>`range`:<br/>See the the Range parameter table, horizontal sections column. TODO REWORD |
| blocks                 | array of objects                                             | TODO: blocks specify BLAH BLAH. Each rectangular block object in the array has the following parameters: TODO which required? To visually determine the following coordinates, click a point in the document in the Sensible app, then drag to display inch dimensions.<br/>`minX`: default: 0 <br/>Specifies the left boundary of the block, in inches from the left edge of the page. <br/>`maxX`: default: 0<br/>Specifies the right boundary of the block, in inches from the left edge of the page. <br/> `minY`: default: page's width in inches<br/>Specifies the top boundary of the block, in inches from the top edge of the page.<br/>`maxY`: default: page's height in inches<br/>Specifies the bottom boundary of the block, in inches from the top edge of the page. |

### LINEARIZE Horizontal Section Range parameters



TODO: figure this out and define it better!!  WITH A NICE PICTURE?



Horizontal sections: repeating stacked blocks of text in a defined range, *which can be discontinous/interrupted by other igored text???*

Vertical sections: columns of text containing repeated text in a defined range, *which doesn't itself repeat and which can't be discontinious??*.

RANGE contains repeating sections (blocks)



See the following table for details about the Range object parameters:

| comment TODO DELETE | key                   | value                                                        | description for horizontal sections                          | description  for LINEARIZED BLOCKS                           | description for vertical sections                            |
| ------------------- | --------------------- | ------------------------------------------------------------ | ------------------------------------------------------------ | ------------------------------------------------------------ | ------------------------------------------------------------ |
| Y b                 | direction             | `horizontal`, `vertical`. default: `horizontal`              | If set to `horizontal`, Sensible searches for horizontal sections. For an illustration of this behavior, see [section nuances](doc:section-nuances). |                                                              | If set to `vertical`, Sensible detects columnar sections in a single document area defined by the Range parameter. <br/>TODO REDUCE REDUNDANCY<br/>Use `"direction":"vertical"` in the Range object to define a "vertical" sections group, where each section is a column-like layout. For example, use vertical sections to extract tables nested in tables, tables with row labels, or other complex text layouts. <br/>In detail, Sensible searches  left-to-right for columns in the first-found document area defined by the Range parameter. For an illustration of this behavior, see [section nuances](doc:section-nuances). |
| y B                 | anchor (**required**) | [Anchor](anchor) object, or array of Match objects           | Contains the following parameters:<br/><br/> **start**: Ignores anything in the document before this line. if undefined, Sensible starts the search for the Match parameter at the beginning of the document.<br/><br/>**match** (**required**): <br/>&nbsp;&nbsp;&nbsp; Specifies the repeated starting line of each section. For example, in the preceding image, specify `"Claim number"`. Each section starts at the top boundary of this starting line, and excludes text to the right of the line. If sections lack an easy-to-match starting line, use the Require Stop and Offset Y parameters to start each section above or below the line matched by this parameter. <br/><br/>&nbsp;&nbsp; **end**: Ignores anchor matches in the document after this line. For example, to extract solely September claims in the preceding image, specify `"October"`. | **match** (**required**): <br/>Specifies the starting line of each section in which to run the *Blocks* preprocessor. | TODO REWORD: Same behavior as for horizontal sections, with the following exception:<br/>The Match parameter specifies the horizontal line that defines the  shared top boundary of  all the columnar sections.  For more information about column recognition, see [Section nuances](doc:section-nuances#vertical-sections).<br/> |
|                     |                       |                                                              |                                                              |                                                              |                                                              |
| H                   | stop                  | [Anchor](anchor) object, or array of Match objects           | Specifies the bottom boundary of each section. In the [Claims loss run example](doc:sections-example-loss-run), if you specify `"Date of claim"`, then each section stops at a horizontal line below the bottom boundary of the stop line "Date of claim".<br/>Sensible defines the Stop horizontal line by finding the top boundary of the stop line if found, or the top boundary of the next section's starting line, then applies a default offset of 0.08" down or up the page, respectively.<br/>If you don't specify this parameter, each section stops at the top boundary of the next section's starting line. In this case, the last section continues to the end of the document. |                                                              | Specifies the horizontal line that defines the shared bottom boundary of all the columnar sections.  If not specified, Sensible ends the columns at the first line that spans multiple columns. If specified, Sensible ignores lines that span multiple columns. If the spanning lines occur mid-column, you can configure the Line Filters parameter as an alternative to this parameter.<br/>For more information, see [Section nuances](doc:section-nuances#vertical-sections). |
| y B                 | offsetY               | number in inches. Positive values offset down the page, negative values offset up the page. | Specifies the number of inches by which to offset each section's top boundary from the anchor's Match parameter. <br/>By default each section starts at the top boundary of the line specified by the anchor's Match parameter. If you specify Offset Y, each section starts at that top boundary plus the offset. For example, configure this when each section lacks an easy-to-match first line. |                                                              | Specifies the number of inches by which to offset the columns' shared top boundary from the anchor's Match parameter. <br/>For example, configure this when when you want to exclude non-columnar text from columnar sections. |
| y B                 | stopOffsetY           | number in inches. Positive values offset down the page, negative values offset up the page. | Specifies the number of inches by which to offset each section's bottom boundary from the horizontal line specified by the Stop parameter. |                                                              | Specifies the number of inches by which to offset the columns' shared bottom boundary from the horizontal line specified by the Stop parameter. <br/> TODO DOUBLE CHECK THIS WORDING, provide an example of why you might want to? |
| y B                 | tolerance             | number in inches. default: 0.08                              | Configure this for your Stop parameter if the stop line and its immediately preceding and succeeding lines are an unusual font size.<br/> For example, if your font size is a tiny 1.44 pt (0.02 inches), set this parameter to 0.01.<br>In detail, Sensible defines the Stop horizontal line by finding the top boundary of the stop line, or if unspecified the top boundary of the next section's starting line, then applies a default offset of 0.08" down or up the page, respectively. This parameter configures the default offset. |                                                              | TODO: QUESTION: what's the effect here? wouldn't it be pretty much inapplicable?<br/> |
|                     |                       |                                                              | **Parameters specific to horizontal sections**               |                                                              |                                                              |
| H                   | externalRange         | object                                                       | (Advanced) Enables anchoring on text that's external to the sections in the sections' field anchors.  For example, use the external range with the [Intersection](doc:intersection) method when sections lack internal anchoring candidates.<br/>The external range defines a vertical range anywhere in the document. You can configure the external range to be static, or to repeat relative to each section.<br/>Contains the following parameters:<br/><br/>`anchor`  (**required**):  An [Anchor](https://docs.sensible.so/docs/anchor) object. The external range starts at the top boundary of this starting line, and the range's scope includes text to the left of this line. If the range lacks an easy-to-match first line, you can use the Offset Y parameter to start the range above or below the line matched by this parameter. <br/><br/>`anchorIsAbsolute`: (default: false).  If false, Sensible creates dynamic external ranges, each relative to a section start. For example, configure dynamic external ranges if you want to anchor each section's fields on variably positioned page headings. For more information, see [Dynamic external range example](doc:sections-example-external-range#example-dynamic). Sensible starts searching for dynamic external ranges in the lines succeeding the start of each section. To search for dynamic external ranges that precede each section, use  `"reverse":"true"`  on the external range's anchor. <br/>If the Anchor Is Absolute option is set to true, Sensible creates one static external range in the document, searching from the start of the document. For an example of a static dynamic range, see [Static external range example](doc:sections-example-external-range#example-static).<br/><br/>`stop`: (Match object) (**required**) A Match object defining the end of the external range. Sensible defines the Stop horizontal line by finding the top boundary of the stop line, then applies a default offset of 0.08" down the page.<br/><br/>`offsetY`: Specifies the number of inches to offset the range's top boundary from the anchor's Match parameter.<br/><br/>`stopOffsetY`: Specifies the number of inches to offset from the Stop parameter.<br/> |                                                              | not supported                                                |
|                     |                       |                                                              |                                                              |                                                              |                                                              |
| H                   | requireStop           | Boolean. default: false                                      | If true, each section ends when it matches the Stop parameter, instead of the default behavior of ending at the next starting line specified in the anchor's Match parameter.<br/>**Note:**  Configure this parameter for horizontal sections when the starting line repeats in each section, to avoid prematurely ending each section.<br/>You don't need to configure this parameter for matches that are on the same horizontal line as the anchor's Match parameter. For more information, see [Multiple anchors in section](doc:section-nuances#multiple-anchors-in-section). |                                                              | not supported                                                |
|                     |                       |                                                              |                                                              |                                                              |                                                              |
|                     |                       |                                                              |                                                              |                                                              |                                                              |
|                     |                       |                                                              |                                                              |                                                              |                                                              |
|                     |                       |                                                              | **Parameters specific to vertical (columnar) sections**      |                                                              |                                                              |
| V                   | ignoredColumns        | integer array.                                               | not supported                                                |                                                              | Removes unwanted columns from both the output *and* from the SenseML search scope. For example, this is useful if the columns contain text that interferes with anchoring on other columns. |
| V                   | columnSelection       | array of index selections where each "index selection" can be:<br/>- a column index or comma-delimited indices<br/><br/>- an array with two comma-delimited indices, meaning all the columns in the indices range<br/><br/> default: capture all columns (`[]`) |                                                              |                                                              | Use to configure which columns to treat as sections. Sensible appends *unselected* columns to each section, for example so that they can be used as anchor candidates. For an illustration, see [Section nuances](doc:section-nuances#column-selection).<br/>Example syntax:<br/> `[[0,5]]` selects 1st through 6th columns as sections. Sensible adds the lines from any other columns to each section. <br/>`[1,3,-1]`  selects the 2nd, 4th, and the last column. <br/>  `[[0, -2]]` selects 1st through 2nd-to-last columns.<br/> `[1,[3,7]]` selects the 2nd column and the 4th through 8th columns. |
| V                   | minColumnGap          | number in inches. default: 0                                 | not supported                                                |                                                              | Configures column recognition by specifying the smallest allowed width of the gutters separating the columns. For an example, see [Table grid example](doc:sections-example-table-grid). Use when text in a column contains large whitespace gaps that cause Sensible to mistakenly split one column into two. To avoid this split, set a minimum gap that's larger than the gaps inside the column. The default (0) specifies that zero-width vertical lines define the column boundaries. |
| V                   | lineFilters           | Match object, or array of Match objects                      | not supported                                                |                                                              | Use to ignore lines that span columns and break column recognition. For example, if the lines occur mid-column, use this parameter rather than a Stop parameter to exclude the lines. Sensible excludes the lines both from the output and from the SenseML search scope.<br/>You don't need to configure this parameter if you specify a Stop parameter. For more information, see [Section nuances](doc:section-nuances#vertical-sections). |
| V                   | lineSelection         | Matcher[]                                                    |                                                              |                                                              | TODO DID I MISS THIS ONE??                                   |



Examples
====

## Example 1

The following example shows TBD.

**Config**

```json
{
  "preprocessors": [
    {
      // todo: show outline of blocks in screenshot markup in docs
      "type": "linearize",
      // page identifier
      "match": "some header text",
      "blocks": [
        {
          /* block 1 */
          "minX": 1,
          "maxX": 4.4,
          "minY": 2.5,
          "maxY": 8.5
        },
        {
          /* block 2 */
          "minX": 4.5,
          // TODO: question
          // these are strict, not like Region I believe; if even a little of a line out of range, it's NOT contained in block
          "minY": 2.5,
          "maxY": 8.5
        },
        {
          /* block 3 */
          "maxY": 2.4
        }
      ]
    }
  ],
  "fields": [
    {
      /* outputs all lines of the document to check block order
         note footer text is excluded since no block coordinates capture it; that text is unavailble for output from SenseML queries */
      "id": "all_lines_in_doc",
      "method": {
        "id": "documentRange",
        "includeAnchor": true
      },
      "anchor": {
        "match": {
          "type": "first"
        }
      }
    }
  ]
}

```

**Example document**
The following image shows the example document used with this example config:

![Click to enlarge](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/images/final/linearize_1.png)

| Example document | [Download link](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/pdfs/linearize_1.pdf) |
| ---------------- | ------------------------------------------------------------ |

**Output**

```json
{
  "all_lines_in_doc": {
    "type": "string",
    "value": "block 1 header block 1 text block 1 end block 2 header block 2 text block 2 end Some header text Block 3 block 3 spans page width"
  }
}
```