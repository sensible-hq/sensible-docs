---
title: "Cell Rows"
hidden: true
---

TODO: impacted topics:

- overview
- SenseML reference introduction
- devops platform
- 'alternative to...' (sections? ROW METHOD?? TABLE METHODS TOPIC?)

## parent topic:

 See the following information for a method specific to very long spreadsheets/ for optiizing performance when yo uwant to extract thousands or millions of spreadsheet rows. This method is an alternative to more general-purpose  SenseML methods, which are also compatible with spreadsheets.

See child topics for methods specific to extracting data from spreadsheets.

## Cell rows

Extracts rows from a spreadsheet, where the rows are all under a single row of headings. Use this method as an alternative to more general SenseML methods to optimize speed of extraction for lengthy spreadsheets (i.e. contain thousands or millions of rows). 

TODO: a screenshot here of the typical layout captured + maybe a YAML version of the senseml to capture it

TODO: it kinda seems like Sensible ignores empty rows and columns, right? so note that here *and* in the file-tyes notes

- or maybe it's more complicated? seems like for a moment there they didn't render, but now they do render, but Sensible ignores them. so it must just go to the end of the file for ending the rows

TODO/2q: remember to refer the reader to file-types notes on how Sensible STANDARDIZES spreadsheets?

Parameters
====

TODO: note that this won't work on a spreadsheet converted to a PDF before Sensible got its hands on it. you've got to upload the spreadsheeet as is so that Sensible can do its conversion/standardization process




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

| key               | value                                            | description                                                  |
| ----------------- | ------------------------------------------------ | ------------------------------------------------------------ |
| id (**required**) | `cell`                                           | Extracts all the lines in a cell in a spreadsheet **IN A REPEATING MANNER** -> how to word it? |
| header            | Anchor object (or is it a match object TODO/2do) | *An anchor object that defines an intersection with a column heading in the row specified by the field-level Header Row parameter. <br/*> For the specified column heading (contained in the Header Row), Sensible finds that header cell, then extracts each cell in each row that falls in that column  Sensible works down the column and ends when UNTIL WHEN? empty row cell? |

## Examples

TODO
