# How to extract data from residential appraisal reports (Form 1004) with Sensible

If you're building software for mortgage lending or real estate finance, chances are you've encountered the residential appraisal report, also known as Form 1004. A Form 1004 is the standard Fannie Mae and Freddie Mac appraisal form for single-family properties. It captures the subject property's characteristics, a neighborhood analysis, up to nine comparable sales, and the appraiser's final value opinion. Lenders need this data to underwrite loans, manage risk, and meet investor delivery requirements. However, they often lack access to appraisal reports in any format other than PDFs, which makes extracting data a potentially difficult problem.

With Sensible you can easily extract key information out of residential appraisal report PDFs using SenseML, Sensible's query language for extracting data from documents. We've written a library of open-source SenseML configurations, so you don't need to write queries from scratch for common documents. From there, your residential appraisal report data is accessible via API, Sensible's UI, or 5,000 other software integrations thanks to Zapier.

## What we'll cover

This blog post briefly walks you through configuring extractions for Form 1004 residential appraisal reports. By the end, you'll know a few SenseML methods and you'll be on your way to extracting any data you choose using our documentation or our prebuilt open-source residential appraisal report configurations.

## Prerequisites

To extract from this document, take the following steps: Sign up for a **Sensible account**. After completing onboarding, click the **Document types** tab and click **Create new document type**. In the dialog, upload the example document below. Leave all defaults as-is except ensure "Auto-generate configuration" is disabled, then click **Create**. Download the Form 1004 sample below. Name the document type `residential_appraisal_reports`.

## Write document extraction queries with SenseML

Let's walk through extracting specific pieces of data from a residential appraisal report. Here's an example of a Form 1004 PDF with redacted data:

[IMAGE: Screenshot of the Brooklyn Form 1004 PDF showing the subject property section, with address and other fields redacted]

To keep the example in this post simple, let's extract just the:

- File number
- Property rights appraised (fee simple, leasehold, or other)
- Comparable sale 1 data (address, sale price, GLA, GLA adjustment, net adjustment, and adjusted sale price)
- Final appraised value and appraisal condition

## Identify and classify incoming residential appraisal reports

One fingerprint test uniquely identifies the Form 1004 format. Two text conditions must both pass before field extraction runs.

```json
/* Sensible uses JSON5 to support in-line comments*/
{
  "fingerprint": {       /* optional. Sensible skips this config if these tests fail, improving performance when you have multiple configs */
    "tests": [
      {
        "page": "every",
        "match": [
          [
            {
              "text": "residential appraisal report", /* string to match */
              "type": "includes"                     /* match anywhere in line. */
            },
            {
              "text": "Form 1004",                   /* string to match */
              "type": "includes"                     /* match anywhere in line. */
            }
          ]
        ]
      }
    ]
  }
}
```

Sensible uses these tests to route each incoming document to the correct config automatically. If a document fails any test, Sensible skips this config and tries the next one. This is useful when a document type has multiple carrier- or vendor-specific layouts. Here, the test runs on every page (`"page": "every"`) and requires both the text "residential appraisal report" and "Form 1004" to appear before the config runs.

[IMAGE: Screenshot of the fingerprint tests in the Sensible app showing the two conditions highlighted in the document]

## Extract the file number

See the following screenshot for an overview of how to extract the file number:

[IMAGE: Screenshot showing the file # field extraction (left pane: query. middle pane: document. right pane: output)]

The query in the left pane in the preceding image uses the anchor text "file #" to locate the label, then extracts text to its left using the Region method. The Word Filters parameter strips the label text from the output, leaving just the numeric file number. The PDF is displayed in the middle pane, and the extracted data is in the right pane.

To try this out yourself, paste the following query into the left pane of the Sensible app.

```json
/* Sensible uses JSON5 to support in-line comments*/
{
  "fields": [
    {
      "id": "file #",          /* user-friendly ID for extracted target data */
      "anchor": {
        "match": {
          "text": "file #",    /* string to match */
          "type": "startsWith" /* line must start with the match */
        }
      },
      "method": {
        "id": "region",          /* extracts lines contained in a defined rectangular region */
        "start": "left",         /* initial coordinates for region's top-left corner relative to anchor's boundaries. enums: above | below | left | right */
        "offsetX": -0.05,        /* horizontally shifts the region's top-left corner specified in the Start parameter by specified number of inches. positive: right, negative: left */
        "offsetY": -0.1,         /* vertically shifts the region's top-left corner specified in the Start parameter by the specified number of inches. positive: down, negative: up */
        "width": 1.3,            /* width of the region in inches */
        "height": 0.17,          /* height of the region in inches */
        "wordFilters": ["file #"] /* filters out the specified strings from the method output */
      }
    }
  ]
}
```

You'll get this output:

```json
{
  "file #": {
    "type": "string",
    "value": "1552474"
  }
}
```

## Extract property rights appraised

See the following screenshot for an overview of how to extract the property rights appraised:

[IMAGE: Screenshot showing the property_rights_appraised field extraction (left pane: query. middle pane: document. right pane: output)]

The queries in the left pane in the preceding image work in two steps. First, three Checkbox method fields detect which of the three options ("Fee Simple," "Leasehold," or "Other") is checked on the form. Then a Pick Values field reads those boolean results and returns the label of the checked option as a string. The PDF is displayed in the middle pane, and the extracted data is in the right pane.

To try this out yourself, paste the following queries into the left pane of the Sensible app.

```json
{
  "fields": [
    {
      "id": "subject",       /* user-friendly ID for extracted target data */
      "type": "sections",    /* extracts repeating sections; returns each section as an object */
      "range": {
        "anchor": {
          "match": {
            "text": "property address", /* string to match */
            "type": "startsWith"        /* line must start with the match */
          }
        },
        "stop": {
          "text": "did not analyze the contract", /* string to match */
          "type": "includes"                      /* match anywhere in line. */
        }
      },
      "fields": [            /* array of fields to extract from each section. can include computed fields */
        {
          "id": "fee simple", /* user-friendly ID for extracted target data */
          "anchor": {
            "match": {
              "text": "Fee Simple", /* string to match */
              "type": "startsWith"  /* line must start with the match */
            }
          },
          "method": {
            "id": "checkbox",
            "position": "left"
          }
        },
        {
          "id": "leasehold", /* user-friendly ID for extracted target data */
          "anchor": {
            "match": {
              "text": "Leasehold", /* string to match */
              "type": "startsWith" /* line must start with the match */
            }
          },
          "method": {
            "id": "checkbox",
            "position": "left"
          }
        },
        {
          "id": "other", /* user-friendly ID for extracted target data */
          "anchor": {
            "match": {
              "text": "other",      /* string to match */
              "type": "startsWith"  /* line must start with the match */
            },
            "end": {
              "text": "assignment type", /* optional. stop searching at this line */
              "type": "startsWith" /* line must start with the match */
            }
          },
          "method": {
            "id": "checkbox",
            "position": "left"
          }
        },
        {
          "id": "property_rights_appraised", /* user-friendly ID for extracted target data */
          "method": {
            "id": "pickValues",
            "match": "one",                              /* use the first occurrence of the anchor */
            "source_ids": ["fee simple", "leasehold", "other"] /* IDs of the checkbox fields to evaluate */
          }
        }
      ]
    }
  ]
}
```

You'll get this output:

```json
{
  "subject": [
    {
      "fee simple": { "type": "boolean", "value": true },
      "leasehold": { "type": "boolean", "value": false },
      "other": { "type": "boolean", "value": false },
      "property_rights_appraised": { "value": "fee simple", "type": "string" }
    }
  ]
}
```

The Checkbox method returns `true` or `false` for each option, and the Pick Values method with `"match": "one"` selects the label of the single checked field and returns it as a string. Form 1004 repeats this Checkbox-plus-Pick Values pattern across more than 30 fields: occupancy status, assignment type, flood zone, zoning compliance, and more. It's the core extraction pattern for the form.

## Extract comparable sale data

Form 1004's sales comparison grid is its most structurally complex section: up to nine comparable sales arranged in side-by-side columns, each with roughly 35 rows of descriptions and dollar adjustments. Sensible handles this with nested Sections and the Intersection method.

See the following screenshot for an overview of how to extract comparable sale 1 data:

[IMAGE: Screenshot showing the comparable_sale_1 section extraction (left pane: query. middle pane: document. right pane: output)]

The queries in the left pane in the preceding image define two levels of sections. The outer `sales_comparison` section anchors to the beginning of the comparable sales grid. Inside it, the `comparable_sale_1` section anchors to the "FEATURE" header row, the row that labels the columns SUBJECT, COMP 1, COMP 2, etc. Within that inner section, each field uses the Intersection method with a Vertical Anchor parameter that matches "sale no. 1" or "sale # 1" (different Form 1004 variants use different column headings) to scope extraction to the Comparable Sale 1 column. The PDF is displayed in the middle pane, and the extracted data is in the right pane.

To try this out yourself, paste the following queries into the left pane of the Sensible app.

```json
{
  "fields": [
    {
      "id": "sales_comparison",   /* user-friendly ID for extracted target data */
      "type": "sections",         /* extracts repeating sections; returns each section as an object */
      "range": {
        "anchor": {
          "match": {
            "text": "comparable properties currently", /* string to match */
            "type": "includes",                       /* match anywhere in line. */
            "editDistance": 2
          }
        },
        "stop": [
          {
            "pattern": "COST APPROACH TO VALUE", /* JavaScript-flavored regex. Double-escape special characters, e.g. \\s not \s. Doesn't support capturing groups */
            "type": "regex",
            "reverse": true
          }
        ]
      },
      "fields": [                 /* array of fields to extract from each section. can include computed fields */
        {
          "id": "comparable_sale_1", /* user-friendly ID for extracted target data */
          "type": "sections",     /* extracts repeating sections; returns each section as an object */
          "range": {
            "anchor": {
              "match": {
                "text": "FEATURE",          /* string to match */
                "type": "equals",           /* matching line must equal the string exactly */
                "isCaseSensitive": true     /* match is case-sensitive */
              },
              "end": {
                "text": "did not research the sale", /* optional. stop searching at this line */
                "type": "includes"                   /* match anywhere in line. */
              }
            },
            "stop": {
              "text": "did not research the sale", /* string to match */
              "type": "includes"                   /* match anywhere in line. */
            },
            "stopOffsetY": -0.1  /* default: 0. shift each section's bottom boundary in inches from stop line. positive: down, negative: up */
          },
          "fields": [            /* array of fields to extract from each section. can include computed fields */
            {
              "id": "address",   /* user-friendly ID for extracted target data */
              "anchor": {
                "match": {
                  "text": "address",   /* string to match */
                  "type": "startsWith" /* line must start with the match */
                }
              },
              "method": {
                "id": "intersection",
                "verticalAnchor": {              /* defines the vertical axis (the column). use horizontalAnchor instead to swap which anchor defines which axis */
                  "match": {
                    "type": "any",               /* boolean or: any sub-match condition must pass */
                    "matches": [
                      { "text": "sale no. 1", "type": "endsWith" },
                      { "text": "sale # 1",   "type": "endsWith" }
                    ]
                  }
                },
                "offsetY": -0.1,       /* default: 0. offset the horizontal line up (negative) or down (positive) in inches */
                "width": 1.87,         /* default: 0. zero creates a point intersection, non-zero creates a horizontal-line region, and in conjunction with Height param, creates a rectangular region. Sensible extracts any line overlapping the point, or any line contained in the region. */
                "height": 0.3,         /* default: 0. same as width, but for height of the intersection region. */
                "percentOverlapX": 0,  /* default: 0.9. fraction of width overlap required for a line to be inside the region defined by Width or Height parameters; 0 accepts any overlap */
                "percentOverlapY": 0,  /* default: 0.8. same as percentOverlapX, but for height */
                "wordFilters": ["Address"] /* filters out the specified strings from the method output */
              }
            },
            {
              "id": "sale_price",   /* user-friendly ID for extracted target data */
              "type": "number",     /* Sensible formats extracted data as this data type, or returns null if it doesn't recognize extracted data as the specified type */
              "anchor": {
                "match": {
                  "text": "sale price", /* string to match */
                  "type": "equals"      /* matching line must equal the string exactly */
                }
              },
              "method": {
                "id": "intersection",
                "verticalAnchor": {    /* defines the vertical axis (the column). use horizontalAnchor instead to swap which anchor defines which axis */
                  "match": {
                    "type": "any",     /* boolean or: any sub-match condition must pass */
                    "matches": [
                      { "text": "sale no. 1", "type": "endsWith" },
                      { "text": "sale # 1",   "type": "endsWith" }
                    ]
                  }
                },
                "width": 0.6,         /* default: 0. zero creates a point intersection, non-zero creates a horizontal-line region, and in conjunction with Height param, creates a rectangular region. Sensible extracts any line overlapping the point, or any line contained in the region. */
                "offsetX": 0.6,       /* default: 0. offset the vertical line left (negative) or right (positive) in inches */
                "percentOverlapX": 0, /* default: 0.9. fraction of width overlap required for a line to be inside the region defined by Width or Height parameters; 0 accepts any overlap */
                "percentOverlapY": 0  /* default: 0.8. same as percentOverlapX, but for height */
              }
            },
            {
              "id": "gross_living_area_description", /* user-friendly ID for extracted target data */
              "type": "number",                      /* Sensible formats extracted data as this data type, or returns null if it doesn't recognize extracted data as the specified type */
              "anchor": {
                "match": {
                  "text": "gross living area", /* string to match */
                  "type": "startsWith"         /* line must start with the match */
                }
              },
              "method": {
                "id": "intersection",
                "verticalAnchor": {    /* defines the vertical axis (the column). use horizontalAnchor instead to swap which anchor defines which axis */
                  "match": {
                    "type": "any",     /* boolean or: any sub-match condition must pass */
                    "matches": [
                      { "text": "sale no. 1", "type": "endsWith" },
                      { "text": "sale # 1",   "type": "endsWith" }
                    ]
                  }
                },
                "offsetX": -0.4,      /* default: 0. offset the vertical line left (negative) or right (positive) in inches */
                "width": 0.8,         /* default: 0. zero creates a point intersection, non-zero creates a horizontal-line region, and in conjunction with Height param, creates a rectangular region. Sensible extracts any line overlapping the point, or any line contained in the region. */
                "percentOverlapX": 0, /* default: 0.9. fraction of width overlap required for a line to be inside the region defined by Width or Height parameters; 0 accepts any overlap */
                "percentOverlapY": 0  /* default: 0.8. same as percentOverlapX, but for height */
              }
            },
            {
              "id": "gross_living_area_adjustment", /* user-friendly ID for extracted target data */
              "type": "number",                     /* Sensible formats extracted data as this data type, or returns null if it doesn't recognize extracted data as the specified type */
              "anchor": {
                "match": {
                  "text": "gross living area", /* string to match */
                  "type": "startsWith"         /* line must start with the match */
                }
              },
              "method": {
                "id": "intersection",
                "verticalAnchor": {    /* defines the vertical axis (the column). use horizontalAnchor instead to swap which anchor defines which axis */
                  "match": {
                    "type": "any",     /* boolean or: any sub-match condition must pass */
                    "matches": [
                      { "text": "sale no. 1", "type": "endsWith" },
                      { "text": "sale # 1",   "type": "endsWith" }
                    ]
                  }
                },
                "offsetX": 0.6,       /* default: 0. offset the vertical line left (negative) or right (positive) in inches */
                "width": 0.65,        /* default: 0. zero creates a point intersection, non-zero creates a horizontal-line region, and in conjunction with Height param, creates a rectangular region. Sensible extracts any line overlapping the point, or any line contained in the region. */
                "percentOverlapX": 0, /* default: 0.9. fraction of width overlap required for a line to be inside the region defined by Width or Height parameters; 0 accepts any overlap */
                "percentOverlapY": 0  /* default: 0.8. same as percentOverlapX, but for height */
              }
            },
            {
              "id": "net_adjustment_sign", /* user-friendly ID for extracted target data */
              "method": {
                "id": "pickValues",
                "match": "one",                          /* use the first occurrence of the anchor */
                "source_ids": ["positive", "negative"]   /* IDs of the checkbox fields to evaluate */
              }
            },
            {
              "id": "net_adjustment",  /* user-friendly ID for extracted target data */
              "type": "number",        /* Sensible formats extracted data as this data type, or returns null if it doesn't recognize extracted data as the specified type */
              "anchor": {
                "match": {
                  "text": "net adjustment", /* string to match */
                  "type": "startsWith"      /* line must start with the match */
                }
              },
              "method": {
                "id": "intersection",
                "verticalAnchor": {    /* defines the vertical axis (the column). use horizontalAnchor instead to swap which anchor defines which axis */
                  "match": {
                    "type": "any",     /* boolean or: any sub-match condition must pass */
                    "matches": [
                      { "text": "sale no. 1", "type": "endsWith" },
                      { "text": "sale # 1",   "type": "endsWith" }
                    ]
                  }
                },
                "offsetX": 0.5,       /* default: 0. offset the vertical line left (negative) or right (positive) in inches */
                "width": 0.75,        /* default: 0. zero creates a point intersection, non-zero creates a horizontal-line region, and in conjunction with Height param, creates a rectangular region. Sensible extracts any line overlapping the point, or any line contained in the region. */
                "percentOverlapX": 0, /* default: 0.9. fraction of width overlap required for a line to be inside the region defined by Width or Height parameters; 0 accepts any overlap */
                "percentOverlapY": 0  /* default: 0.8. same as percentOverlapX, but for height */
              }
            },
            {
              "id": "gross_adjusted_sale_price_amount", /* user-friendly ID for extracted target data */
              "type": "number",                         /* Sensible formats extracted data as this data type, or returns null if it doesn't recognize extracted data as the specified type */
              "anchor": {
                "match": {
                  "text": "of comparables", /* string to match */
                  "type": "startsWith"      /* line must start with the match */
                }
              },
              "method": {
                "id": "intersection",
                "verticalAnchor": {    /* defines the vertical axis (the column). use horizontalAnchor instead to swap which anchor defines which axis */
                  "match": {
                    "type": "any",     /* boolean or: any sub-match condition must pass */
                    "matches": [
                      { "text": "sale no. 1", "type": "endsWith" },
                      { "text": "sale # 1",   "type": "endsWith" }
                    ]
                  }
                },
                "offsetX": 0.5,       /* default: 0. offset the vertical line left (negative) or right (positive) in inches */
                "width": 0.75,        /* default: 0. zero creates a point intersection, non-zero creates a horizontal-line region, and in conjunction with Height param, creates a rectangular region. Sensible extracts any line overlapping the point, or any line contained in the region. */
                "percentOverlapX": 0, /* default: 0.9. fraction of width overlap required for a line to be inside the region defined by Width or Height parameters; 0 accepts any overlap */
                "percentOverlapY": 0  /* default: 0.8. same as percentOverlapX, but for height */
              }
            }
          ]
        }
      ]
    }
  ]
}
```

You'll get this output:

```json
{
  "sales_comparison": [
    {
      "comparable_sale_1": [
        {
          "address": {
            "type": "string",
            "value": "145 ST MARKS AVE BROOKLYN, NY"
          },
          "sale_price": {
            "source": "860,000",
            "value": 860000,
            "type": "number"
          },
          "gross_living_area_description": {
            "source": "2,556",
            "value": 2556,
            "type": "number"
          },
          "gross_living_area_adjustment": {
            "source": "38,640",
            "value": 38640,
            "type": "number"
          },
          "net_adjustment_sign": {
            "value": "positive",
            "type": "string"
          },
          "net_adjustment": {
            "source": "38,640",
            "value": 38640,
            "type": "number"
          },
          "gross_adjusted_sale_price_amount": {
            "source": "898,640",
            "value": 898640,
            "type": "number"
          }
        }
      ]
    }
  ]
}
```

The Vertical Anchor parameter is doing the column-scoping work here: matching "sale no. 1" or "sale # 1" in the column header row defines a vertical line, and each field's intersection with that line extracts only the value from Comparable 1's column. The full config extends this pattern across nine comparables, each with its own Vertical Anchor parameter targeting its respective sale number column header.

## Extract the final appraised value

See the following screenshot for an overview of how to extract the final appraised value:

[IMAGE: Screenshot showing the final_reconciled_value field extraction (left pane: query. middle pane: document. right pane: output)]

The queries in the left pane in the preceding image define three fallback anchors for `final_reconciled_value`. Form 1004 variants differ in how the appraised value sentence is worded. The config tries "The market value" first, then "as of" with the Row method, then "as of" with the Region method. Sensible returns the first non-null result. The PDF is displayed in the middle pane, and the extracted data is in the right pane.

To try this out yourself, paste the following queries into the left pane of the Sensible app.

```json
{
  "fields": [
    {
      "id": "reconciliation",  /* user-friendly ID for extracted target data */
      "type": "sections",      /* extracts repeating sections; returns each section as an object */
      "range": {
        "anchor": {
          "match": {
            "type": "any",     /* boolean or: any sub-match condition must pass */
            "matches": [
              { "text": "indicated value by:", "type": "startsWith" },
              { "text": "indicated valueby:",  "type": "startsWith" }
            ]
          }
        },
        "stop": {
          "text": "form 1004", /* string to match */
          "type": "includes"   /* match anywhere in line. */
        },
        "stopOffsetY": -0.15   /* default: 0. shift each section's bottom boundary in inches from stop line. positive: down, negative: up */
      },
      "fields": [              /* array of fields to extract from each section. can include computed fields */
        {
          "id": "final_reconciled_value",  /* user-friendly ID for extracted target data */
          "type": "number",                /* Sensible formats extracted data as this data type, or returns null if it doesn't recognize extracted data as the specified type */
          "anchor": {
            "match": {
              "text": "The market value", /* string to match */
              "type": "includes"          /* match anywhere in line. */
            }
          },
          "method": {
            "id": "region",                 /* extracts lines contained in a defined rectangular region */
            "start": "left",               /* initial coordinates for region's top-left corner relative to anchor's boundaries. enums: above | below | left | right */
            "offsetX": -0.05,              /* horizontally shifts the region's top-left corner specified in the Start parameter by specified number of inches. positive: right, negative: left */
            "offsetY": -0.1,               /* vertically shifts the region's top-left corner specified in the Start parameter by the specified number of inches. positive: down, negative: up */
            "width": 7.7,                  /* width of the region in inches */
            "height": 0.17,                /* height of the region in inches */
            "wordFilters": [               /* filters out the specified strings from the method output */
              "The market value of the subject property as of",
              "$"
            ]
          }
        },
        {
          "id": "final_reconciled_value", /* user-friendly ID for extracted target data */
          "type": "number",                /* Sensible formats extracted data as this data type, or returns null if it doesn't recognize extracted data as the specified type */
          "anchor": {
            "match": {
              "text": "as of",  /* string to match */
              "type": "includes" /* match anywhere in line. */
            }
          },
          "method": {
            "id": "row",                        /* target data to extract is distributed on same horizontal line as anchor */
            "position": "left",                 /* default: right. target data is to left or right of anchor. enums: left | right. */
            "tiebreaker": "last",               /* extract the line in the second non-empty cell to the left of the anchor. default: returns all cells. */
            "includeAnchor": true,
            "typeFilters": ["date"]
          }
        },
        {
          "id": "final_reconciled_value", /* user-friendly ID for extracted target data */
          "type": "number",                /* Sensible formats extracted data as this data type, or returns null if it doesn't recognize extracted data as the specified type */
          "anchor": {
            "match": {
              "text": "as of",    /* string to match */
              "type": "startsWith" /* line must start with the match */
            }
          },
          "method": {
            "id": "region",        /* extracts lines contained in a defined rectangular region */
            "start": "left",       /* initial coordinates for region's top-left corner relative to anchor's boundaries. enums: above | below | left | right */
            "offsetX": -1.4,       /* horizontally shifts the region's top-left corner specified in the Start parameter by specified number of inches. positive: right, negative: left */
            "offsetY": -0.1,       /* vertically shifts the region's top-left corner specified in the Start parameter by the specified number of inches. positive: down, negative: up */
            "width": 3,            /* width of the region in inches */
            "height": 0.17         /* height of the region in inches */
          }
        },
        {
          "id": "as is.appraisal_condition", /* user-friendly ID for extracted target data */
          "anchor": {
            "match": {
              "text": "as is",   /* string to match */
              "type": "includes" /* match anywhere in line. */
            }
          },
          "method": { "id": "checkbox", "position": "left" }
        },
        {
          "id": "subject to completion.appraisal_condition", /* user-friendly ID for extracted target data */
          "anchor": {
            "match": {
              "text": "subject to completion", /* string to match */
              "type": "startsWith"             /* line must start with the match */
            }
          },
          "method": { "id": "checkbox", "position": "left" }
        },
        {
          "id": "subject to repairs.appraisal_condition", /* user-friendly ID for extracted target data */
          "anchor": {
            "match": {
              "text": "repairs or alterations", /* string to match */
              "type": "includes"                /* match anywhere in line. */
            }
          },
          "method": { "id": "checkbox", "position": "left" }
        },
        {
          "id": "subject to inspection.appraisal_condition", /* user-friendly ID for extracted target data */
          "match": "last",                     /* use the last occurrence of the anchor */
          "anchor": {
            "match": {
              "text": "subject to", /* string to match */
              "type": "includes"    /* match anywhere in line. */
            }
          },
          "method": { "id": "checkbox", "position": "left" }
        },
        {
          "id": "appraisal_condition", /* user-friendly ID for extracted target data */
          "method": {
            "id": "pickValues",
            "match": "one",       /* use the first occurrence of the anchor */
            "source_ids": [
              "as is.appraisal_condition",
              "subject to completion.appraisal_condition",
              "subject to repairs.appraisal_condition",
              "subject to inspection.appraisal_condition"
            ]
          }
        }
      ]
    }
  ]
}
```

You'll get this output:

```json
{
  "reconciliation": [
    {
      "final_reconciled_value": {
        "source": "825,000",
        "value": 825000,
        "type": "number"
      },
      "as is.appraisal_condition": { "type": "boolean", "value": true },
      "subject to completion.appraisal_condition": { "type": "boolean", "value": false },
      "subject to repairs.appraisal_condition": { "type": "boolean", "value": false },
      "subject to inspection.appraisal_condition": { "type": "boolean", "value": false },
      "appraisal_condition": {
        "value": "as is",
        "type": "string"
      }
    }
  ]
}
```

The three `final_reconciled_value` fields with the same ID act as fallbacks: Sensible returns the value from the first field that resolves to a non-null result and ignores the rest. This makes the config robust across Form 1004 variants that phrase the appraised value sentence differently.

## Putting it all together

Here's the complete SenseML config combining everything we've covered:

<!-- CONFIG:START -->
```json
{
  "fingerprint": {       /* optional. Sensible skips this config if these tests fail, improving performance when you have multiple configs */
    "tests": [
      {
        "page": "every",
        "match": [
          [
            {
              "text": "residential appraisal report", /* string to match */
              "type": "includes"                     /* match anywhere in line. */
            },
            {
              "text": "Form 1004", /* string to match */
              "type": "includes"   /* match anywhere in line. */
            }
          ]
        ]
      }
    ]
  },
  "fields": [
    {
      "id": "file #",          /* user-friendly ID for extracted target data */
      "anchor": {
        "match": {
          "text": "file #",    /* string to match */
          "type": "startsWith" /* line must start with the match */
        }
      },
      "method": {
        "id": "region",          /* extracts lines contained in a defined rectangular region */
        "start": "left",         /* initial coordinates for region's top-left corner relative to anchor's boundaries. enums: above | below | left | right */
        "offsetX": -0.05,        /* horizontally shifts the region's top-left corner specified in the Start parameter by specified number of inches. positive: right, negative: left */
        "offsetY": -0.1,         /* vertically shifts the region's top-left corner specified in the Start parameter by the specified number of inches. positive: down, negative: up */
        "width": 1.3,            /* width of the region in inches */
        "height": 0.17,          /* height of the region in inches */
        "wordFilters": ["file #"] /* filters out the specified strings from the method output */
      }
    },
    {
      "id": "subject",       /* user-friendly ID for extracted target data */
      "type": "sections",    /* extracts repeating sections; returns each section as an object */
      "range": {
        "anchor": {
          "match": {
            "text": "property address", /* string to match */
            "type": "startsWith"        /* line must start with the match */
          }
        },
        "stop": {
          "text": "did not analyze the contract", /* string to match */
          "type": "includes"                      /* match anywhere in line. */
        }
      },
      "fields": [            /* array of fields to extract from each section. can include computed fields */
        {
          "id": "fee simple", /* user-friendly ID for extracted target data */
          "anchor": {
            "match": {
              "text": "Fee Simple", /* string to match */
              "type": "startsWith"  /* line must start with the match */
            }
          },
          "method": { "id": "checkbox", "position": "left" }
        },
        {
          "id": "leasehold", /* user-friendly ID for extracted target data */
          "anchor": {
            "match": {
              "text": "Leasehold", /* string to match */
              "type": "startsWith" /* line must start with the match */
            }
          },
          "method": { "id": "checkbox", "position": "left" }
        },
        {
          "id": "other", /* user-friendly ID for extracted target data */
          "anchor": {
            "match": {
              "text": "other",     /* string to match */
              "type": "startsWith" /* line must start with the match */
            },
            "end": {
              "text": "assignment type", /* optional. stop searching at this line */
              "type": "startsWith" /* line must start with the match */
            }
          },
          "method": { "id": "checkbox", "position": "left" }
        },
        {
          "id": "property_rights_appraised", /* user-friendly ID for extracted target data */
          "method": {
            "id": "pickValues",
            "match": "one",                                    /* use the first occurrence of the anchor */
            "source_ids": ["fee simple", "leasehold", "other"] /* IDs of the checkbox fields to evaluate */
          }
        }
      ]
    },
    {
      "id": "sales_comparison",   /* user-friendly ID for extracted target data */
      "type": "sections",         /* extracts repeating sections; returns each section as an object */
      "range": {
        "anchor": {
          "match": {
            "text": "comparable properties currently", /* string to match */
            "type": "includes",                       /* match anywhere in line. */
            "editDistance": 2
          }
        },
        "stop": [
          {
            "pattern": "COST APPROACH TO VALUE", /* JavaScript-flavored regex. Double-escape special characters, e.g. \\s not \s. Doesn't support capturing groups */
            "type": "regex",
            "reverse": true
          }
        ]
      },
      "fields": [                 /* array of fields to extract from each section. can include computed fields */
        {
          "id": "comparable_sale_1", /* user-friendly ID for extracted target data */
          "type": "sections",     /* extracts repeating sections; returns each section as an object */
          "range": {
            "anchor": {
              "match": {
                "text": "FEATURE",        /* string to match */
                "type": "equals",         /* matching line must equal the string exactly */
                "isCaseSensitive": true   /* match is case-sensitive */
              },
              "end": {
                "text": "did not research the sale", /* optional. stop searching at this line */
                "type": "includes"                   /* match anywhere in line. */
              }
            },
            "stop": {
              "text": "did not research the sale", /* string to match */
              "type": "includes"                   /* match anywhere in line. */
            },
            "stopOffsetY": -0.1  /* default: 0. shift each section's bottom boundary in inches from stop line. positive: down, negative: up */
          },
          "fields": [            /* array of fields to extract from each section. can include computed fields */
            {
              "id": "address",   /* user-friendly ID for extracted target data */
              "anchor": {
                "match": {
                  "text": "address",   /* string to match */
                  "type": "startsWith" /* line must start with the match */
                }
              },
              "method": {
                "id": "intersection",
                "verticalAnchor": {              /* defines the vertical axis (the column). use horizontalAnchor instead to swap which anchor defines which axis */
                  "match": {
                    "type": "any",               /* boolean or: any sub-match condition must pass */
                    "matches": [
                      { "text": "sale no. 1", "type": "endsWith" },
                      { "text": "sale # 1",   "type": "endsWith" }
                    ]
                  }
                },
                "offsetY": -0.1,       /* default: 0. offset the horizontal line up (negative) or down (positive) in inches */
                "width": 1.87,         /* default: 0. zero creates a point intersection, non-zero creates a horizontal-line region, and in conjunction with Height param, creates a rectangular region. Sensible extracts any line overlapping the point, or any line contained in the region. */
                "height": 0.3,         /* default: 0. same as width, but for height of the intersection region. */
                "percentOverlapX": 0,  /* default: 0.9. fraction of width overlap required for a line to be inside the region defined by Width or Height parameters; 0 accepts any overlap */
                "percentOverlapY": 0,  /* default: 0.8. same as percentOverlapX, but for height */
                "wordFilters": ["Address"] /* filters out the specified strings from the method output */
              }
            },
            {
              "id": "sale_price",   /* user-friendly ID for extracted target data */
              "type": "number",     /* Sensible formats extracted data as this data type, or returns null if it doesn't recognize extracted data as the specified type */
              "anchor": {
                "match": {
                  "text": "sale price", /* string to match */
                  "type": "equals"      /* matching line must equal the string exactly */
                }
              },
              "method": {
                "id": "intersection",
                "verticalAnchor": {    /* defines the vertical axis (the column). use horizontalAnchor instead to swap which anchor defines which axis */
                  "match": {
                    "type": "any",     /* boolean or: any sub-match condition must pass */
                    "matches": [
                      { "text": "sale no. 1", "type": "endsWith" },
                      { "text": "sale # 1",   "type": "endsWith" }
                    ]
                  }
                },
                "width": 0.6,         /* default: 0. zero creates a point intersection, non-zero creates a horizontal-line region, and in conjunction with Height param, creates a rectangular region. Sensible extracts any line overlapping the point, or any line contained in the region. */
                "offsetX": 0.6,       /* default: 0. offset the vertical line left (negative) or right (positive) in inches */
                "percentOverlapX": 0, /* default: 0.9. fraction of width overlap required for a line to be inside the region defined by Width or Height parameters; 0 accepts any overlap */
                "percentOverlapY": 0  /* default: 0.8. same as percentOverlapX, but for height */
              }
            },
            {
              "id": "gross_living_area_description", /* user-friendly ID for extracted target data */
              "type": "number",                      /* Sensible formats extracted data as this data type, or returns null if it doesn't recognize extracted data as the specified type */
              "anchor": {
                "match": {
                  "text": "gross living area", /* string to match */
                  "type": "startsWith"         /* line must start with the match */
                }
              },
              "method": {
                "id": "intersection",
                "verticalAnchor": {    /* defines the vertical axis (the column). use horizontalAnchor instead to swap which anchor defines which axis */
                  "match": {
                    "type": "any",     /* boolean or: any sub-match condition must pass */
                    "matches": [
                      { "text": "sale no. 1", "type": "endsWith" },
                      { "text": "sale # 1",   "type": "endsWith" }
                    ]
                  }
                },
                "offsetX": -0.4,      /* default: 0. offset the vertical line left (negative) or right (positive) in inches */
                "width": 0.8,         /* default: 0. zero creates a point intersection, non-zero creates a horizontal-line region, and in conjunction with Height param, creates a rectangular region. Sensible extracts any line overlapping the point, or any line contained in the region. */
                "percentOverlapX": 0, /* default: 0.9. fraction of width overlap required for a line to be inside the region defined by Width or Height parameters; 0 accepts any overlap */
                "percentOverlapY": 0  /* default: 0.8. same as percentOverlapX, but for height */
              }
            },
            {
              "id": "gross_living_area_adjustment", /* user-friendly ID for extracted target data */
              "type": "number",                     /* Sensible formats extracted data as this data type, or returns null if it doesn't recognize extracted data as the specified type */
              "anchor": {
                "match": {
                  "text": "gross living area", /* string to match */
                  "type": "startsWith"         /* line must start with the match */
                }
              },
              "method": {
                "id": "intersection",
                "verticalAnchor": {    /* defines the vertical axis (the column). use horizontalAnchor instead to swap which anchor defines which axis */
                  "match": {
                    "type": "any",     /* boolean or: any sub-match condition must pass */
                    "matches": [
                      { "text": "sale no. 1", "type": "endsWith" },
                      { "text": "sale # 1",   "type": "endsWith" }
                    ]
                  }
                },
                "offsetX": 0.6,       /* default: 0. offset the vertical line left (negative) or right (positive) in inches */
                "width": 0.65,        /* default: 0. zero creates a point intersection, non-zero creates a horizontal-line region, and in conjunction with Height param, creates a rectangular region. Sensible extracts any line overlapping the point, or any line contained in the region. */
                "percentOverlapX": 0, /* default: 0.9. fraction of width overlap required for a line to be inside the region defined by Width or Height parameters; 0 accepts any overlap */
                "percentOverlapY": 0  /* default: 0.8. same as percentOverlapX, but for height */
              }
            },
            {
              "id": "net_adjustment_sign", /* user-friendly ID for extracted target data */
              "method": {
                "id": "pickValues",
                "match": "one",                         /* use the first occurrence of the anchor */
                "source_ids": ["positive", "negative"]  /* IDs of the checkbox fields to evaluate */
              }
            },
            {
              "id": "net_adjustment",  /* user-friendly ID for extracted target data */
              "type": "number",        /* Sensible formats extracted data as this data type, or returns null if it doesn't recognize extracted data as the specified type */
              "anchor": {
                "match": {
                  "text": "net adjustment", /* string to match */
                  "type": "startsWith"      /* line must start with the match */
                }
              },
              "method": {
                "id": "intersection",
                "verticalAnchor": {    /* defines the vertical axis (the column). use horizontalAnchor instead to swap which anchor defines which axis */
                  "match": {
                    "type": "any",     /* boolean or: any sub-match condition must pass */
                    "matches": [
                      { "text": "sale no. 1", "type": "endsWith" },
                      { "text": "sale # 1",   "type": "endsWith" }
                    ]
                  }
                },
                "offsetX": 0.5,       /* default: 0. offset the vertical line left (negative) or right (positive) in inches */
                "width": 0.75,        /* default: 0. zero creates a point intersection, non-zero creates a horizontal-line region, and in conjunction with Height param, creates a rectangular region. Sensible extracts any line overlapping the point, or any line contained in the region. */
                "percentOverlapX": 0, /* default: 0.9. fraction of width overlap required for a line to be inside the region defined by Width or Height parameters; 0 accepts any overlap */
                "percentOverlapY": 0  /* default: 0.8. same as percentOverlapX, but for height */
              }
            },
            {
              "id": "gross_adjusted_sale_price_amount", /* user-friendly ID for extracted target data */
              "type": "number",                         /* Sensible formats extracted data as this data type, or returns null if it doesn't recognize extracted data as the specified type */
              "anchor": {
                "match": {
                  "text": "of comparables", /* string to match */
                  "type": "startsWith"      /* line must start with the match */
                }
              },
              "method": {
                "id": "intersection",
                "verticalAnchor": {    /* defines the vertical axis (the column). use horizontalAnchor instead to swap which anchor defines which axis */
                  "match": {
                    "type": "any",     /* boolean or: any sub-match condition must pass */
                    "matches": [
                      { "text": "sale no. 1", "type": "endsWith" },
                      { "text": "sale # 1",   "type": "endsWith" }
                    ]
                  }
                },
                "offsetX": 0.5,       /* default: 0. offset the vertical line left (negative) or right (positive) in inches */
                "width": 0.75,        /* default: 0. zero creates a point intersection, non-zero creates a horizontal-line region, and in conjunction with Height param, creates a rectangular region. Sensible extracts any line overlapping the point, or any line contained in the region. */
                "percentOverlapX": 0, /* default: 0.9. fraction of width overlap required for a line to be inside the region defined by Width or Height parameters; 0 accepts any overlap */
                "percentOverlapY": 0  /* default: 0.8. same as percentOverlapX, but for height */
              }
            }
          ]
        }
      ]
    },
    {
      "id": "reconciliation",  /* user-friendly ID for extracted target data */
      "type": "sections",      /* extracts repeating sections; returns each section as an object */
      "range": {
        "anchor": {
          "match": {
            "type": "any",     /* boolean or: any sub-match condition must pass */
            "matches": [
              { "text": "indicated value by:", "type": "startsWith" },
              { "text": "indicated valueby:",  "type": "startsWith" }
            ]
          }
        },
        "stop": {
          "text": "form 1004", /* string to match */
          "type": "includes"   /* match anywhere in line. */
        },
        "stopOffsetY": -0.15   /* default: 0. shift each section's bottom boundary in inches from stop line. positive: down, negative: up */
      },
      "fields": [              /* array of fields to extract from each section. can include computed fields */
        {
          "id": "final_reconciled_value",  /* user-friendly ID for extracted target data */
          "type": "number",                /* Sensible formats extracted data as this data type, or returns null if it doesn't recognize extracted data as the specified type */
          "anchor": {
            "match": {
              "text": "The market value", /* string to match */
              "type": "includes"          /* match anywhere in line. */
            }
          },
          "method": {
            "id": "region",        /* extracts lines contained in a defined rectangular region */
            "start": "left",       /* initial coordinates for region's top-left corner relative to anchor's boundaries. enums: above | below | left | right */
            "offsetX": -0.05,      /* horizontally shifts the region's top-left corner specified in the Start parameter by specified number of inches. positive: right, negative: left */
            "offsetY": -0.1,       /* vertically shifts the region's top-left corner specified in the Start parameter by the specified number of inches. positive: down, negative: up */
            "width": 7.7,          /* width of the region in inches */
            "height": 0.17,        /* height of the region in inches */
            "wordFilters": [       /* filters out the specified strings from the method output */
              "The market value of the subject property as of",
              "$"
            ]
          }
        },
        {
          "id": "final_reconciled_value", /* user-friendly ID for extracted target data */
          "type": "number",                /* Sensible formats extracted data as this data type, or returns null if it doesn't recognize extracted data as the specified type */
          "anchor": {
            "match": {
              "text": "as of",  /* string to match */
              "type": "includes" /* match anywhere in line. */
            }
          },
          "method": {
            "id": "row",             /* target data to extract is distributed on same horizontal line as anchor */
            "position": "left",      /* default: right. target data is to left or right of anchor. enums: left | right. */
            "tiebreaker": "last",    /* extract the line in the second non-empty cell to the left of the anchor. default: returns all cells. */
            "includeAnchor": true,
            "typeFilters": ["date"]
          }
        },
        {
          "id": "final_reconciled_value", /* user-friendly ID for extracted target data */
          "type": "number",                /* Sensible formats extracted data as this data type, or returns null if it doesn't recognize extracted data as the specified type */
          "anchor": {
            "match": {
              "text": "as of",    /* string to match */
              "type": "startsWith" /* line must start with the match */
            }
          },
          "method": {
            "id": "region",        /* extracts lines contained in a defined rectangular region */
            "start": "left",       /* initial coordinates for region's top-left corner relative to anchor's boundaries. enums: above | below | left | right */
            "offsetX": -1.4,       /* horizontally shifts the region's top-left corner specified in the Start parameter by specified number of inches. positive: right, negative: left */
            "offsetY": -0.1,       /* vertically shifts the region's top-left corner specified in the Start parameter by the specified number of inches. positive: down, negative: up */
            "width": 3,            /* width of the region in inches */
            "height": 0.17         /* height of the region in inches */
          }
        },
        {
          "id": "as is.appraisal_condition", /* user-friendly ID for extracted target data */
          "anchor": {
            "match": {
              "text": "as is",   /* string to match */
              "type": "includes" /* match anywhere in line. */
            }
          },
          "method": { "id": "checkbox", "position": "left" }
        },
        {
          "id": "subject to completion.appraisal_condition", /* user-friendly ID for extracted target data */
          "anchor": {
            "match": {
              "text": "subject to completion", /* string to match */
              "type": "startsWith"             /* line must start with the match */
            }
          },
          "method": { "id": "checkbox", "position": "left" }
        },
        {
          "id": "subject to repairs.appraisal_condition", /* user-friendly ID for extracted target data */
          "anchor": {
            "match": {
              "text": "repairs or alterations", /* string to match */
              "type": "includes"                /* match anywhere in line. */
            }
          },
          "method": { "id": "checkbox", "position": "left" }
        },
        {
          "id": "subject to inspection.appraisal_condition", /* user-friendly ID for extracted target data */
          "match": "last",                     /* use the last occurrence of the anchor */
          "anchor": {
            "match": {
              "text": "subject to", /* string to match */
              "type": "includes"    /* match anywhere in line. */
            }
          },
          "method": { "id": "checkbox", "position": "left" }
        },
        {
          "id": "appraisal_condition", /* user-friendly ID for extracted target data */
          "method": {
            "id": "pickValues",
            "match": "one",       /* use the first occurrence of the anchor */
            "source_ids": [
              "as is.appraisal_condition",
              "subject to completion.appraisal_condition",
              "subject to repairs.appraisal_condition",
              "subject to inspection.appraisal_condition"
            ]
          }
        }
      ]
    }
  ]
}
```
<!-- CONFIG:END -->

You'll get this output:

```json
{
  "file #": {
    "type": "string",
    "value": "1552474"
  },
  "subject": [
    {
      "fee simple": { "type": "boolean", "value": true },
      "leasehold": { "type": "boolean", "value": false },
      "other": { "type": "boolean", "value": false },
      "property_rights_appraised": { "value": "fee simple", "type": "string" }
    }
  ],
  "sales_comparison": [
    {
      "comparable_sale_1": [
        {
          "address": { "type": "string", "value": "145 ST MARKS AVE BROOKLYN, NY" },
          "sale_price": { "source": "860,000", "value": 860000, "type": "number" },
          "gross_living_area_description": { "source": "2,556", "value": 2556, "type": "number" },
          "gross_living_area_adjustment": { "source": "38,640", "value": 38640, "type": "number" },
          "net_adjustment_sign": { "value": "positive", "type": "string" },
          "net_adjustment": { "source": "38,640", "value": 38640, "type": "number" },
          "gross_adjusted_sale_price_amount": { "source": "898,640", "value": 898640, "type": "number" }
        }
      ]
    }
  ],
  "reconciliation": [
    {
      "final_reconciled_value": { "source": "825,000", "value": 825000, "type": "number" },
      "as is.appraisal_condition": { "type": "boolean", "value": true },
      "subject to completion.appraisal_condition": { "type": "boolean", "value": false },
      "subject to repairs.appraisal_condition": { "type": "boolean", "value": false },
      "subject to inspection.appraisal_condition": { "type": "boolean", "value": false },
      "appraisal_condition": { "value": "as is", "type": "string" }
    }
  ]
}
```

## Extract more residential appraisal report data

We've covered how to extract a few pieces of data from a residential appraisal report. Our prebuilt config extracts much more information. Check it out! In the following screenshot, every blue-outlined line is a piece of extracted data:

[IMAGE: Full extraction screenshot showing all highlighted fields across the entire Form 1004 document]

## Connect Sensible to your workflow

Once your SenseML config is set up, there are several ways to integrate residential appraisal report extraction into your application or process.

- **Python SDK** — wraps the extraction API; install with pip to call Sensible from your application code
- **MCP server** — connects document extraction to AI coding tools like Claude
- **API (synchronous and asynchronous)** — synchronous returns data inline; asynchronous accepts a webhook, recommended for high-volume workflows such as bulk appraisal processing
- **Zapier** — no-code integration; routes extracted data into Google Sheets, Airtable, Slack, or any of 5,000 other apps

## FAQ

**What fields can be extracted from a Form 1004 residential appraisal report?**

Sensible's Form 1004 config can extract the full breadth of the form, including: file number, subject property address and legal description, borrower and lender names, neighborhood characteristics (location, growth, property values, supply/demand), site details (zoning, utilities, FEMA flood zone), improvement details (construction type, foundation, HVAC, room counts, gross living area), up to nine comparable sales with descriptions and adjustments for each feature, reconciliation values (cost approach, income approach, sales comparison approach, and final reconciled value), appraisal condition, cost approach inputs and depreciation schedules, income approach estimates, and appraiser certification details.

**How accurate is automated Form 1004 extraction?**

Because the Form 1004 is a standardized, layout-consistent form, Sensible uses deterministic layout-based methods rather than probabilistic LLMs. The extracted values are either exactly right or null, with no hallucination risk. For the document in this post, key fields like the appraised value, property rights, and comparable sale prices all extracted correctly on the first pass.

**How does Sensible handle Form 1004 documents from different software vendors?**

The fingerprint method routes each incoming document to the correct config automatically based on layout-identifying text. The config above targets Fannie Mae Form 1004 PDFs. If your pipeline also includes Form 1073 (condo), Form 1025 (2-4 unit), or Form 2055 (exterior-only), you'd create separate configs for each and Sensible routes them automatically.

**Can Sensible extract from Form 1004s bundled with other documents in a loan package?**

Yes. Sensible's portfolio method splits multi-document PDFs (loan packages, closing binders) into individual documents and routes each to the appropriate config before extraction. This means you can submit an entire loan package and receive structured data for each document type in one API response.

**How long does it take to set up Form 1004 extraction?**

The prebuilt open-source config covers the full form and is ready to use immediately. Customizing it for a specific variant (adding fields, tweaking region coordinates) typically takes under an hour using the Sensible app's visual editor.
