---
title: "Mapper"
hidden: false
---
Maps output from the source field using a lookup table

Parameters
====

| key       | value                                   | description                                                  |
| :-------- | :-------------------------------------- | :----------------------------------------------------------- |
| id        | `mapper`                                |                                                              |
| source_id | a field id in the current configuration | The id of the field to map                                   |
| mappings  | object                                  | An object with mappings from strings or numbers to output strings represented as key/value pairs, e.g., `{ "03/04": "March 4th" }` |

Examples
====
