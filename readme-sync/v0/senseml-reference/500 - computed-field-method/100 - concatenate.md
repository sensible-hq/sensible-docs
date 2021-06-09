---
title: "Concatenate"
hidden: false
---
Concatenates the output of two or more fields:

	- If the fields are all strings, the output is a single string.
	- If any field is an arrays, the output is an array if the array lengths match, and a string if they don't (using the first element of each array).
	- If a string is present in the fields among arrays, its value is repeated for every element of the output.



Parameters
====


| key                       | value                | description                                                  |
| :------------------------ | :------------------- | :----------------------------------------------------------- |
| id (**required**)         | `concat`             |                                                              |
| source_ids (**required**) | array of field IDs   | a list of field `id`s to concatenate in the current config   |
| delimiter                 | string. default: " " | The delimiter with which to join the output of the source fields |

Examples
====

