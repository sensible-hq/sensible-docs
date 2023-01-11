---
title: "Verbosity"
hidden: false
---
Configures the verbosity of the extraction.

Parameters
====

| Possible Values | Description                                                  |
| :-------------- | :----------------------------------------------------------- |
| `0`             | default                                                      |
| `1`             | adds `lines` array to field output, with  `text`, `page`, and `boundingPoly` metadata describing the text ouput in the field's  `value`. |
| `3`             | adds:<br/> - full standardized text metadata (anchor, lines, points, regions) <br/><br/>-  If Sensible extracted a field from OCR'd text, then Sensible outputs the following confidence scores. Sensible's OCR engines output confidence scores between 0 and 1: <br/>1. In the field's standardized text metadata, Sensible provides a `confidence` score for each element in the `lines` array. The score is the average score of the "tokens", or words, in the line.<br/>2. In the field output, Sensible outputs  `anchorConfidence` and `valueConfidence` values, which are the averages of their source lines' confidence scores.<br/><br/>For more information about using confidence scores, see [Validate extractions](doc:validate-extractions).<br/><br/> If the standardized text metadata causes the extraction response to exceed 6MB, as can be the case with large documents, then Sensible returns a `413` error. |

Examples
====

If you add `"verbosity": 1,`  as a sibling to the fields array in [the Table example](doc:table#examples), you get the following output:

```
{
  "agile_risks_table_updates_monthly": {
    "columns": [
      {
        "id": "col1_risk_description",
        "values": [
          {
            "value": "Poor task point estimation",
            "type": "string",
            "lines": [
              {
                "text": "Poor task point estimation",
                "boundingPolygon": [
                  {
                    "x": 0.992,
                    "y": 2.972
                  },
                  {
                    "x": 2.354,
                    "y": 2.972
                  },
                  {
                    "x": 2.354,
                    "y": 3.882
                  },
                  {
                    "x": 0.992,
                    "y": 3.882
                  }
                ],
                "page": 0
              }
            ]
          },
          {
            "value": "Poor epic scope definition",
            "type": "string",
            "lines": [
              {
                "text": "Poor epic scope definition",
                "boundingPolygon": [
                  {
                    "x": 0.992,
                    "y": 3.882
                  },
                  {
                    "x": 2.354,
                    "y": 3.882
                  },
                  {
                    "x": 2.354,
                    "y": 4.799
                  },
                  {
                    "x": 0.992,
                    "y": 4.799
                  }
                ],
                "page": 0
              }
            ]
          },
          {
            "value": "Inadequate scrum master training",
            "type": "string",
            "lines": [
              {
                "text": "Inadequate scrum master training",
                "boundingPolygon": [
                  {
                    "x": 0.992,
                    "y": 4.799
                  },
                  {
                    "x": 2.354,
                    "y": 4.799
                  },
                  {
                    "x": 2.354,
                    "y": 5.964
                  },
                  {
                    "x": 0.992,
                    "y": 5.964
                  }
                ],
                "page": 0
              }
            ]
          }
        ]
      },
      {
        "id": "rank_this_month",
        "values": [
          {
            "source": "3",
            "value": 3,
            "type": "number",
            "lines": [
              {
                "text": "3",
                "boundingPolygon": [
                  {
                    "x": 6.625,
                    "y": 2.972
                  },
                  {
                    "x": 8.036,
                    "y": 2.972
                  },
                  {
                    "x": 8.036,
                    "y": 3.882
                  },
                  {
                    "x": 6.625,
                    "y": 3.882
                  }
                ],
                "page": 0
              }
            ]
          },
          {
            "source": "1",
            "value": 1,
            "type": "number",
            "lines": [
              {
                "text": "1",
                "boundingPolygon": [
                  {
                    "x": 6.625,
                    "y": 3.882
                  },
                  {
                    "x": 8.036,
                    "y": 3.882
                  },
                  {
                    "x": 8.036,
                    "y": 4.799
                  },
                  {
                    "x": 6.625,
                    "y": 4.799
                  }
                ],
                "page": 0
              }
            ]
          },
          {
            "source": "2",
            "value": 2,
            "type": "number",
            "lines": [
              {
                "text": "2",
                "boundingPolygon": [
                  {
                    "x": 6.625,
                    "y": 4.799
                  },
                  {
                    "x": 8.036,
                    "y": 4.799
                  },
                  {
                    "x": 8.036,
                    "y": 5.964
                  },
                  {
                    "x": 6.625,
                    "y": 5.964
                  }
                ],
                "page": 0
              }
            ]
          }
        ]
      }
    ]
  }
}
```

