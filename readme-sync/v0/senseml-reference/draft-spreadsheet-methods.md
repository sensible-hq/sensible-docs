---
title: "Cell Rows"
hidden: true
---

## parent topic:

Spreadsheet methods

See child topics for methods specific to extracting data from spreadsheets.

## Cell rows

Extracts rows from a spreadsheet, where the rows are all under a single row of headings. Use this method as an alternative to more general SenseML methods to optimize speed of extraction for lengthy spreadsheets (i.e. contain thousands or millions of rows). 

TODO: a screenshot here of the typical layout captured.



TODO/2q: remember to refer the reader to file-types notes on how Sensible STANDARDIZES spreadsheets?

Parameters
====


| key                      | value                                                        | description                                                  |
| ------------------------ | ------------------------------------------------------------ | ------------------------------------------------------------ |
| id (**required**)        | string                                                       | Specifies an ID for a group of rows to extract in the spreadsheet area under the area defined by the Header Row anchor.  TODO: how does the area stop?? how to recognize a new Header Row? |
| type  (**required**)     | `cellRows`                                                   | Specifies that this field extracts spreadsheet rows.         |
| headerRow (**required**) | object                                                       | Specifies an anchor that matches any line in the header row. Contains the following parameters:<br/>-`match`: A [Match](doc:match) object or array of Match objects<br/>TODO: is there a way to specify the end of the row? I assume it just goes to the end of the spreadsheet horizontally |
| fields                   | array of [computed fields](doc:computed-field-methods) or  spreadsheet-specific fields | Specifies either:<br/>- fields that use a spreadsheet-specific method. For more information, see the following section.<br/>- fields that use [computed fields methods](doc:computed-field-methods) |

## Spreadsheet-specific methods

In a Cell Rows field, you can use the following spreadsheet-specific method:



QUESTION: can you use global parameters for methods? NO YOU CANNOT; how to phrase it??

Note: The [method](doc:method) object's global parameters aren't available for this method.

| key               | value                                                      | description                                                  |
| ----------------- | ---------------------------------------------------------- | ------------------------------------------------------------ |
| id (**required**) | `cell`                                                     | Extracts all lines in a cell in a spreadsheet.               |
| header            | A [Match](doc:match) object or array of Match objects<br/> | Use this parameter to fine tune box recognition. Defines the starting point for the box recognition relative to the anchor. For example, `right` specifies starting at the midpoint of the anchor line's right boundary, and `below` specifies starting at the midpoint of the anchor line's bottom boundary.  Sensible searches outward from this point until it finds dark pixels signifying the box border. <br/> For an example of how to use this parameter, see the following [Examples section](doc:box#examples). |

## Examples

TODO
