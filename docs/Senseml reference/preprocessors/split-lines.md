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

The following example shows using the Range parameter to split lines in specified sections of a typewritten, scanned musical instrument cover order form. 

**PROBLEM**

Without the Split Lines preprocessor, the OCR preprocessor merges the lines too aggressively, so that the Nearest Checkbox method can't recognize which checkbox belongs to which label in the Length and Circumference sections of the document:

![Click to enlarge](https://raw.githubusercontent.com/sensible-hq/sensible-docs/v0/assets/images/final/split_lines_range_1.png)

However, if you apply Split Lines preprocessor to the entire document, Sensible splits lines too aggressively, so that individual words are split into letters:

![Click to enlarge](https://raw.githubusercontent.com/sensible-hq/sensible-docs/v0/assets/images/final/split_lines_range_2.png)

**SOLUTION**

Two Split Line preprocessors use the Range parameter to specify only the Length and Circumference sections, leaving the rest of the document unaffected.

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
      // starting after "Cover Length" and ending before "Cover Circumference"
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
      "id": "_length_section",
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
        {
          "id": "contents",
          "method": {
            "id": "documentRange",
            "includeAnchor": true
          }
        },
        {
          "id": "10in",
          "anchor": {
            "match": {
              "text": "10in",
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
          "id": "10.5in",
          "anchor": {
            "match": {
              "text": "10.5in",
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
          "id": "11in",
          "anchor": {
            "match": {
              "text": "11in",
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
          "id": "11.5in",
          "anchor": {
            "match": {
              "text": "11.5in",
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
          "id": "12in",
          "anchor": {
            "match": {
              "text": "12in",
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
          "id": "12.5in",
          "anchor": {
            "match": {
              "text": "12.5in",
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
        {
          "id": "18in",
          "anchor": {
            "match": {
              "text": "18in",
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
          "id": "18.5in",
          "anchor": {
            "match": {
              "text": "18.5in",
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
          "id": "19in",
          "anchor": {
            "match": {
              "text": "19in",
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
          "id": "19.5in",
          "anchor": {
            "match": {
              "text": "19.5in",
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
          "id": "20in",
          "anchor": {
            "match": {
              "text": "20in",
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
          "id": "length",
          "method": {
            "id": "pickValues",
            "source_ids": [
              "10in",
              "10.5in",
              "11in",
              "11.5in",
              "12in",
              "12.5in",
              "13in",
              "13.5in",
              "14in",
              "14.5in",
              "15in",
              "15.5in",
              "16in",
              "16.5in",
              "17in",
              "17.5in",
              "18in",
              "18.5in",
              "19in",
              "19.5in",
              "20in"
            ],
            "match": "one"
          }
        }
      ]
    },
    {
      "id": "_circumference_section",
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
        {
          "id": "contents",
          "method": {
            "id": "documentRange",
            "includeAnchor": true
          }
        },
        {
          "id": "11.5in",
          "anchor": {
            "match": {
              "text": "11.5in",
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
          "id": "12in",
          "anchor": {
            "match": {
              "text": "12in",
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
          "id": "12.5in",
          "anchor": {
            "match": {
              "text": "12.5in",
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
        {
          "id": "18in",
          "anchor": {
            "match": {
              "text": "18in",
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
          "id": "18.5in",
          "anchor": {
            "match": {
              "text": "18.5in",
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
          "id": "19in",
          "anchor": {
            "match": {
              "text": "19in",
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
          "id": "19.5in",
          "anchor": {
            "match": {
              "text": "19.5in",
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
          "id": "20in",
          "anchor": {
            "match": {
              "text": "20in",
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
          "id": "circumference",
          "method": {
            "id": "pickValues",
            "source_ids": [
              "11.5in",
              "12in",
              "12.5in",
              "13in",
              "13.5in",
              "14in",
              "14.5in",
              "15in",
              "15.5in",
              "16in",
              "16.5in",
              "17in",
              "17.5in",
              "18in",
              "18.5in",
              "19in",
              "19.5in",
              "20in"
            ],
            "match": "one"
          }
        }
      ]
    },
    {
      "id": "_side_section",
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
        {
          "id": "contents",
          "method": {
            "id": "documentRange",
            "sortLines": "readingOrderLeftToRight",
            "includeAnchor": true
          }
        },
        {
          "id": "left",
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
          "id": "right",
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
          "id": "side",
          "method": {
            "id": "pickValues",
            "source_ids": ["left", "right"],
            "match": "one"
          }
        }
      ]
    },
    {
      "id": "length",
      "method": {
        "id": "customComputation",
        "jsonLogic": {
          "var": "_length_section.0.length.value"
        }
      }
    },
    {
      "id": "circumference",
      "method": {
        "id": "customComputation",
        "jsonLogic": {
          "var": "_circumference_section.0.circumference.value"
        }
      }
    },
    {
      "id": "side",
      "method": {
        "id": "customComputation",
        "jsonLogic": {
          "var": "_side_section.0.side.value"
        }
      }
    },
    {
      "id": "length_contents",
      "method": {
        "id": "customComputation",
        "jsonLogic": {
          "var": "_length_section.0.contents.value"
        }
      }
    },

    {
      "id": "circumference_contents",
      "method": {
        "id": "customComputation",
        "jsonLogic": {
          "var": "_circumference_section.0.contents.value"
        }
      }
    },

    {
      "id": "side_contents",
      "method": {
        "id": "customComputation",
        "jsonLogic": {
          "var": "_side_section.0.contents.value"
        }
      }
    },

    {
      "id": "clean",
      "method": {
        "id": "suppressOutput",
        "source_ids": {
          "pattern": "^_.*"
        }
      }
    }
    /*{
      "id": "clean",
      "method": {
        "id": "suppressOutput",
        "source_ids": [
          "design_contents",
          "length_contents",
          "circumference_contents",
          "side_contents",
          "design"
        ]
      }
    }*/
  ]
}

```

**Example document**

In sections 2 and 3, OCR collapses measurement labels and their checkboxes into a single merged line. The `range` parameter targets only those sections for splitting.

![Click to enlarge](https://raw.githubusercontent.com/sensible-hq/sensible-docs/v0/assets/images/final/split_lines_range.png)

| Example document | [Download link](https://raw.githubusercontent.com/sensible-hq/sensible-docs/v0/assets/pdfs/split_lines_range.pdf) |
| ---------------- | ------------------------------------------------------------------------------------------------------------------ |

**Output**

```json
{
  "length": {
    "value": "13.5in",
    "type": "string"
  },
  "circumference": {
    "value": "16in",
    "type": "string"
  }
}
```
