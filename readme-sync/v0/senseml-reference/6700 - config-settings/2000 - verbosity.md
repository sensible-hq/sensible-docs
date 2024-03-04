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
| `1`             | Adds a `lines` array to each field's output describing the field's source text in the document. Each line includes information about its position in the document, for example,   `page`, and `boundingPoly` metadata. |
| `3`             | - In addition to the  `lines` array: <br/>- Sensible returns `points` and `regions`  arrays as siblings to the `lines` array<br/>- If Sensible extracted a field from OCR'd text, then Sensible adds the following confidence scores to the output: <br/>1. In the field's standardized text metadata, Sensible provides an OCR `confidence` score for each element in the `lines` array. The score is the average score of the "tokens", or words, in the line.<br/>2. In the field output, Sensible outputs OCR  `anchorConfidence` and `valueConfidence` values, which are the averages of their source lines' confidence scores.<br/><br/>Sensible's OCR engines output confidence scores between 0 and 1. For more information about using OCR confidence scores, see [Validate extractions](doc:validate-extractions).<br/><br/> If the verbose output causes the extraction response to exceed 6MB, as can be the case with large documents, then Sensible returns a `413` error. |

Examples
====

If you add `"verbosity": 1,`  as a sibling to the fields array in the [Fixed Table](doc:fixed-table#examples) example, you get the following output:

```json
{
  "agile_risks_table": {
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
                "page": 0,
                "boundingPolygon": [
                  {
                    "x": 0.993,
                    "y": 2.75
                  },
                  {
                    "x": 2.631,
                    "y": 2.753
                  },
                  {
                    "x": 2.63,
                    "y": 3.378
                  },
                  {
                    "x": 0.993,
                    "y": 3.376
                  }
                ]
              }
            ]
          },
          {
            "value": "Poor epic scope definition",
            "type": "string",
            "lines": [
              {
                "text": "Poor epic scope definition",
                "page": 0,
                "boundingPolygon": [
                  {
                    "x": 0.993,
                    "y": 3.376
                  },
                  {
                    "x": 2.63,
                    "y": 3.378
                  },
                  {
                    "x": 2.63,
                    "y": 4.004
                  },
                  {
                    "x": 0.992,
                    "y": 4.001
                  }
                ]
              }
            ]
          },
          {
            "value": "Inadequate scrum master training",
            "type": "string",
            "lines": [
              {
                "text": "Inadequate scrum master training",
                "page": 0,
                "boundingPolygon": [
                  {
                    "x": 0.992,
                    "y": 4.001
                  },
                  {
                    "x": 2.63,
                    "y": 4.004
                  },
                  {
                    "x": 2.63,
                    "y": 4.868
                  },
                  {
                    "x": 0.992,
                    "y": 4.866
                  }
                ]
              }
            ]
          }
        ]
      },
      {
        "id": "col4_rank_last_month",
        "values": [
          {
            "source": "2",
            "value": 2,
            "type": "number",
            "lines": [
              {
                "text": "2",
                "page": 0,
                "boundingPolygon": [
                  {
                    "x": 5.878,
                    "y": 2.758
                  },
                  {
                    "x": 7.512,
                    "y": 2.761
                  },
                  {
                    "x": 7.511,
                    "y": 3.386
                  },
                  {
                    "x": 5.878,
                    "y": 3.383
                  }
                ]
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
                "page": 0,
                "boundingPolygon": [
                  {
                    "x": 5.878,
                    "y": 3.383
                  },
                  {
                    "x": 7.511,
                    "y": 3.386
                  },
                  {
                    "x": 7.511,
                    "y": 4.011
                  },
                  {
                    "x": 5.877,
                    "y": 4.008
                  }
                ]
              }
            ]
          },
          {
            "source": "3",
            "value": 3,
            "type": "number",
            "lines": [
              {
                "text": "3",
                "page": 0,
                "boundingPolygon": [
                  {
                    "x": 5.877,
                    "y": 4.008
                  },
                  {
                    "x": 7.511,
                    "y": 4.011
                  },
                  {
                    "x": 7.511,
                    "y": 4.874
                  },
                  {
                    "x": 5.877,
                    "y": 4.872
                  }
                ]
              }
            ]
          }
        ]
      }
    ],
    "title": {
      "type": "string",
      "value": "Agile software development risk tracking",
      "lines": [
        {
          "text": "Agile software development risk tracking",
          "page": 0,
          "boundingPolygon": [
            {
              "x": 0.994,
              "y": 1.666
            },
            {
              "x": 4.902,
              "y": 1.673
            },
            {
              "x": 4.902,
              "y": 1.886
            },
            {
              "x": 0.994,
              "y": 1.879
            }
          ]
        }
      ]
    },
    "footer": {
      "type": "string",
      "value": "Project managers and technical program managers can expand on the preceding table for risk management in Agile software development.",
      "lines": [
        {
          "text": "Project managers and technical program managers can expand on the preceding table for risk management in Agile software development.",
          "page": 0,
          "boundingPolygon": [
            {
              "x": 0.981,
              "y": 5.161
            },
            {
              "x": 7.447,
              "y": 5.169
            },
            {
              "x": 7.447,
              "y": 5.663
            },
            {
              "x": 0.981,
              "y": 5.655
            }
          ]
        }
      ]
    }
  }
}
```

