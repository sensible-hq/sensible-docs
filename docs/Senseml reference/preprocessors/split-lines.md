---
title: Split lines
excerpt: ''
deprecated: false
hidden: false
metadata:
  title: ''
  description: 'Split merged text lines'
  robots: index
next:
  description: ''
---
Splits lines distributed along a horizontal axis. This preprocessor is most useful for typewriter-style documents that use whitespaces for formatting. 

# Parameters

**Note:** For additional parameters available for this method, see [Global parameters for methods](doc:method#global-parameters-for-methods). The following table shows parameters most relevant to or specific to this method.

| key                      | value                                                        | description                                                  |
| ------------------------ | ------------------------------------------------------------ | ------------------------------------------------------------ |
| type (**required**)      | `splitLines`                                                 | splits lines distributed along a horizontal axis.            |
| minSpaces (**required**) | number                                                       | The number of consecutive whitespace characters (` `) at or above which to split lines. |
| separator                | string                                                       | Modifies the Min Spaces parameter to split on the specified character, for example "-", instead of the default whitespace character. For example, if you specify `"-"` for this parameter and `2` for the Min Spaces parameter, then Sensible splits lines when it finds `--`. |
| match<br/>or<br/>range   | A [Match](doc:match) object or array of Match objects<br/><br/>or<br/><br/>Range object | Specifies the matching pages or repeating document ranges ("sections") in which to run this preprocessor.<br/><br/>`match`: Sensible runs this preprocessor on each page containing the matched text.<br/><br/>`range`: Sensible runs this preprocessor in the specified repeating document ranges, leaving lines outside the range unchanged. For information about this option's parameters, see the [Range](doc:sections#range-parameters) parameters for horizontal sections. For an example, see [Example 2](doc:split-lines#example-2). |

#### Limitations

When you configure the Split Lines preprocessor, the Sensible app's [line](doc:line) rendering is approximate and can be inaccurate. To accurately view a line's raw text, [select](doc:color#purple-box) the line.

# Examples

## Example 1

The following example shows solving undersplit lines in a "typewritten" style document. The Split Lines preprocessor preserves columns and rows in this document.

**PROBLEM**

Without the Split Lines preprocessor, Sensible merges the lines too aggressively:

![Click to enlarge](https://raw.githubusercontent.com/sensible-hq/sensible-docs/v0/assets/images/final/split_lines_2.png)

**SOLUTION**

**Config**

```json
{
  "preprocessors": [
    {
      "type": "splitLines",
      "minSpaces": 3
    }
  ],
  "fields": [
    {
      "id": "policy_number",
      "method": {
        "id": "row",
      },
      "anchor": "policy number",
    }
  ]
}
```

**Example document**

The following image shows the example document used with this example config:

![Click to enlarge](https://raw.githubusercontent.com/sensible-hq/sensible-docs/v0/assets/images/final/split_lines.png)

| Example document | [Download link](https://raw.githubusercontent.com/sensible-hq/sensible-docs/v0/assets/pdfs/split_lines.pdf) |
| ---------------- | ---------------------------------------------------------------------------------------------------------------------------- |

**Output**

```json
{
  "policy_number": {
    "type": "string",
    "value": "18-376-190"
  }
}
```

## Example 2

The following example shows using the Range parameter to split lines in specified sections of a typewritten, scanned musical instrument cover order forms. This configuration enables you to extract repeating data from multiple order forms.

**PROBLEM**

Without the Split Lines preprocessor, the OCR preprocessor merges the lines too aggressively, so that the Nearest Checkbox method can't recognize which checkbox belongs to which label in the Length and Circumference sections of the document:

![Click to enlarge](https://raw.githubusercontent.com/sensible-hq/sensible-docs/v0/assets/images/final/split_lines_range_1.png)

However, if you apply Split Lines preprocessor to the entire document, Sensible splits lines too aggressively, so that individual words are split into letters:

![Click to enlarge](https://raw.githubusercontent.com/sensible-hq/sensible-docs/v0/assets/images/final/split_lines_range_2.png)

**SOLUTION**

Two Split Line preprocessors use the Range parameter to specify only the Length and Circumference sections, splitting the overmerged sections and leaving the rest of the document unaffected.

**Config**

```json
{
  "preprocessors": [
    // override the default OCR settings and ensure specific OCR engine for consistent
    // line splitting behavior
    {
      "type": "ocr",
      "matchAll": true,
      "match": "",
      "engine": "amazon"
    },

    // if you apply splitLines with minSpaces:1 to the entire document,
    // Sensible oversplits many sections
    // (to observe this oversplitting, sub "match": ""
    // for the "range" param in each Split Lines preprocessor,
    // then observe lines rendered on the PDF in the Sensible app)
    // so use ranges to split lines only in the target sections

    {
      // target the "Cover Length" section,
      // starting before "Cover Length" and ending after "Cover Circumference"
      // without this split lines, Sensible merges length labels (10 in, 10.5 in, etc)
      // into one line, so the Nearest Checkbox method fails
      // (to observe this overmerging, remove all Split Lines preprocessors)
      "type": "splitLines",
      "minSpaces": 1,
      "range": {
        "anchor": {
          "match": {
            "type": "includes",
            "text": "cover length"
          }
        },
        "stop": {
          "type": "includes",
          "text": "cover circumference"
        }
      }
    },

    {
      "type": "splitLines",
      "minSpaces": 1,
      "range": {
        "anchor": {
          "match": {
            "type": "includes",
            "text": "cover circumference"
          }
        },
        "stop": {
          "type": "includes",
          "text": "cover shape"
        }
      }
    }
  ],
  "fields": [
    {
      // extract the selected checkbox value for cover length
      "id": "_length_sections",
      "type": "sections",
      "range": {
        "anchor": {
          "match": {
            "text": "length",
            "type": "includes"
          }
        },
        "stop": {
          "text": "circumference",
          "type": "includes"
        },
        "stopOffsetY": -0.1
      },
      "fields": [
        // uncomment to double check split line representation
        /*
        {
          "id": "_contents",
          "method": {
            "id": "documentRange",
            "includeAnchor": true
          }
        }, */
        // abbreviated; in production, start at 10 inches
        {
          "id": "13in",
          "anchor": {
            "match": {
              "text": "13in",
              "type": "equals"
            }
          },
          "method": {
            "id": "nearestCheckbox",
            "position": "left",
            "offsetY": -0.25
          }
        },
        {
          "id": "13.5in",
          "anchor": {
            "match": {
              "text": "13.5in",
              "type": "equals"
            }
          },
          "method": {
            "id": "nearestCheckbox",
            "position": "left",
            "offsetY": -0.25
          }
        },
        {
          "id": "14in",
          "anchor": {
            "match": {
              "text": "14in",
              "type": "equals"
            }
          },
          "method": {
            "id": "nearestCheckbox",
            "position": "left",
            "offsetY": -0.25
          }
        },
        {
          "id": "14.5in",
          "anchor": {
            "match": {
              "text": "14.5in",
              "type": "equals"
            }
          },
          "method": {
            "id": "nearestCheckbox",
            "position": "left",
            "offsetY": -0.25
          }
        },
        {
          "id": "15in",
          "anchor": {
            "match": {
              "text": "15in",
              "type": "equals"
            }
          },
          "method": {
            "id": "nearestCheckbox",
            "position": "left",
            "offsetY": -0.25
          }
        },
        {
          "id": "15.5in",
          "anchor": {
            "match": {
              "text": "15.5in",
              "type": "equals"
            }
          },
          "method": {
            "id": "nearestCheckbox",
            "position": "left",
            "offsetY": -0.25
          }
        },

        {
          "id": "COVER_LENGTH",
          "method": {
            "id": "pickValues",
            "source_ids": [
              "13in",
              "13.5in",
              "14in",
              "14.5in",
              "15in",
              "15.5in"
            ],
            "match": "one"
          }
        },
        // clean up output: remove all "inch" boolean values and only
        // output the selected checkbox
        {
          "id": "clean",
          "method": {
            "id": "suppressOutput",
            "source_ids": {
              "pattern": "^.*in$"
            }
          }
        }
      ]
    },
    {
      // extract the selected checkbox value for cover circumference
      "id": "_circumference_sections",
      "type": "sections",
      "range": {
        "anchor": {
          "match": {
            "text": "circumference",
            "type": "includes"
          }
        },
        "stop": {
          "text": "cover shape",
          "type": "includes"
        },
        "stopOffsetY": -0.2
      },
      "fields": [
        // uncomment to double check split line representation
        /*
        {
          "id": "_contents",
          "method": {
            "id": "documentRange",
            "includeAnchor": true
          }
        }, */

        // abbreviated; in production, start at 11.5 inches
        {
          "id": "15.5in",
          "anchor": {
            "match": {
              "text": "15.5in",
              "type": "equals"
            }
          },
          "method": {
            "id": "nearestCheckbox",
            "position": "left",
            "offsetY": -0.25
          }
        },
        {
          "id": "16in",
          "anchor": {
            "match": {
              "text": "16in",
              "type": "equals"
            }
          },
          "method": {
            "id": "nearestCheckbox",
            "position": "left",
            "offsetY": -0.25
          }
        },
        {
          "id": "16.5in",
          "anchor": {
            "match": {
              "text": "16.5in",
              "type": "equals"
            }
          },
          "method": {
            "id": "nearestCheckbox",
            "position": "left",
            "offsetY": -0.25
          }
        },
        {
          "id": "17in",
          "anchor": {
            "match": {
              "text": "17in",
              "type": "equals"
            }
          },
          "method": {
            "id": "nearestCheckbox",
            "position": "left",
            "offsetY": -0.25
          }
        },
        {
          "id": "17.5in",
          "anchor": {
            "match": {
              "text": "17.5in",
              "type": "equals"
            }
          },
          "method": {
            "id": "nearestCheckbox",
            "position": "left",
            "offsetY": -0.25
          }
        },
        // abbreviated; in production, continue up to 20in
        {
          "id": "COVER_CIRCUMFERENCE",
          "method": {
            "id": "pickValues",
            "source_ids": [
              // abbreviated; in production, start at 11.5 inches and end at 20in
              "15.5in",
              "16in",
              "16.5in",
              "17in",
              "17.5in"
            ],
            "match": "one"
          }
        },
        // clean up output: remove all "inch" boolean values and only
        // output the selected checkbox
        {
          "id": "clean",
          "method": {
            "id": "suppressOutput",
            "source_ids": {
              "pattern": "^.*in$"
            }
          }
        }
      ]
    },
    {
      // extract the selected checkbox value for LEFT/RIGHT side
      "id": "_side_sections",
      "type": "sections",
      "range": {
        "anchor": {
          "match": {
            "text": "cover shape",
            "type": "includes"
          }
        },
        "stop": {
          "text": "main color",
          "type": "includes"
        },
        "stopOffsetY": -0.2
      },
      "fields": [
        // uncomment to double check split line representation
        /*
        {
          "id": "contents",
          "method": {
            "id": "documentRange",
            "sortLines": "readingOrderLeftToRight",
            "includeAnchor": true
          }
        }, */
        {
          "id": "left_side",
          "method": {
            "id": "nearestCheckbox",
            "position": "left"
          },
          "anchor": {
            "match": {
              "text": "left",
              "type": "equals"
            }
          }
        },
        {
          "id": "right_side",
          "method": {
            "id": "nearestCheckbox",
            "position": "left"
          },
          "anchor": {
            "match": {
              "text": "right",
              "type": "equals"
            }
          }
        },
        {
          "id": "LEFT_RIGHT",
          "method": {
            "id": "pickValues",
            "source_ids": ["left_side", "right_side"],
            "match": "one"
          }
        },
        // clean up output: remove all "_side" boolean values and only
        // output the selected checkbox
        {
          "id": "clean",
          "method": {
            "id": "suppressOutput",
            "source_ids": {
              "pattern": "^.*_side$"
            }
          }
        }
      ]
    },
    // zip the sections so each order form's data is grouped together
    {
      "id": "order_selections",
      "method": {
        "id": "zip",
        "source_ids": [
          "_length_sections",
          "_circumference_sections",
          "_side_sections"
        ]
      }
    },
    // clean the output:
    // remove the source sections fields and only output the zipped sections
    {
      "id": "clean",
      "method": {
        "id": "suppressOutput",
        "source_ids": {
          "pattern": "^_.*$"
        }
      }
    }
  ]
}

```

**Example document**

The following image shows the example document used with this example config:

![Click to enlarge](https://raw.githubusercontent.com/sensible-hq/sensible-docs/v0/assets/images/final/split_lines_range.png)

| Example document | [Download link](https://raw.githubusercontent.com/sensible-hq/sensible-docs/v0/assets/pdfs/split_lines_range.pdf) |
| ---------------- | ------------------------------------------------------------------------------------------------------------------ |

**Output**

```json
{
  "order_selections": [
    {
      "COVER_LENGTH": {
        "value": "15in",
        "type": "string"
      },
      "COVER_CIRCUMFERENCE": {
        "value": "17.5in",
        "type": "string"
      },
      "LEFT_RIGHT": {
        "value": "right_side",
        "type": "string"
      }
    },
    {
      "COVER_LENGTH": {
        "value": "13.5in",
        "type": "string"
      },
      "COVER_CIRCUMFERENCE": {
        "value": "16in",
        "type": "string"
      },
      "LEFT_RIGHT": {
        "value": "left_side",
        "type": "string"
      }
    }
  ]
}
```
