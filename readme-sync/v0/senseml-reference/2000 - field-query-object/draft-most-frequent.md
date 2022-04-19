---
title: "draft-most-frequent"
hidden: true
---



Parameters
----

The Field object has the following top-level parameters:

| Parameter | Value                                | Description                                                  |
| --------- | ------------------------------------ | ------------------------------------------------------------ |
|           |                                      |                                                              |
|           |                                      |                                                              |
|           |                                      |                                                              |
|           |                                      |                                                              |
| match     | `first`,`last`,`all`, `mostFrequent` | If there are multiple matches for the anchor, specifies which one to use. This parameter applies to the anchor's Match parameter, not to the Start or Stop parameters.<br/>`all` returns an array of matched values under a single key. For example, something like:  <br/>{<br/>  "name_of_output_key": [<br/>    {<br/>      "type": "string",<br/>      "value": "extracted data for first match"<br/>    },<br/>    {<br/>      "type": "string",<br/>      "value": "extracted data for second match"<br/>    } ]<br/>}<br/><br/>`mostFrequent` returns the most frequently matched value. This is useful for OCR text, like poor-quality scans or photographs. For example, if a scanned document contains repeated data for a field anchored on  "1 Wages", but due to OCR errors the matched values are `21050.20`, `21850.20`, `21850.20` and `21850.58,`  this option returns the most frequent, and therefore the mostly likely correct value,  `21850.20`. /home/franc/Github/corex-internal/versions/5.0/corex.yaml |

