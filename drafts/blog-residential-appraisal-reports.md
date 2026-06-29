# How to extract data from residential appraisal reports (Form 1004) with Sensible

If you're building software for mortgage lending or real estate finance, chances are you've encountered the residential appraisal report, also known as Form 1004. A Form 1004 is the standard Fannie Mae and Freddie Mac appraisal form for single-family properties. It captures the subject property's characteristics, a neighborhood analysis, up to nine comparable sales, and the appraiser's final value opinion. Lenders need this data to underwrite loans, manage risk, and meet investor delivery requirements.  However, they often lack access to appraisal reports in any format other than PDFs, which makes extracting data a potentially difficult problem.

With Sensible you can easily extract key information out of residential appraisal report PDFs using SenseML, Sensible's hybrid deterministic and LLM-based query language for extracting data from documents. We've written a library of open-source SenseML configurations, so you don't need to write queries from scratch for common documents. From there, your residential appraisal report data is accessible via API, Sensible's UI, or 5,000 other software integrations thanks to Zapier.

In this post, you'll learn to extract appraisal report data using deterministic methods. Because Form 1004 is a government-standardized form, its field positions and label text are consistent across all lenders and appraisers. Therefore, Sensible handles this data extraction through a layout-specific config. Form 1004 reports are well suited to this approach: the form's field positions and label text are fixed by Fannie Mae and Freddie Mac specifications, giving reliable anchor points that deterministic methods extract precisely — no LLM calls, no prompt maintenance overhead. For non-standardized appraisal formats such as narrative appraisals or state-specific hybrid forms, a generalized LLM config handles extraction on day one without per-format configuration. Both run through the same API.

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
- Final appraised value

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
              "text": "Form 1004",
              "type": "includes"
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

The outer `subject` field uses the Sections method to scope the checkbox queries to a specific region of the document. The Sections method can extract repeating data — like line items in a table — but it's also useful for scoping queries to a single, well-defined region of a complex document. Form 1004 reuses identical checkbox labels ("Fee Simple," "Leasehold," "other") in multiple places, so the `range` parameter narrows extraction to the area between "property address" and "did not analyze the contract," where the property rights checkboxes appear.

To try this out yourself, paste the following queries into the left pane of the Sensible app.

```json
{
  "fields": [
    {
      "id": "subject",       /* user-friendly ID for extracted target data */
      "type": "sections",    /* scopes child fields to a defined region of the document; returns each section as an object */
      "range": {
        "anchor": {
          "match": {
            "text": "property address", /* string to match */
            "type": "startsWith"        /* line must start with the match */
          }
        },
        "stop": {
          "text": "did not analyze the contract",
          "type": "includes"                      /* match anywhere in line. */
        }
      },
      "fields": [            /* array of fields to extract from each section. can include computed fields */
        {
          "id": "fee simple",
          "anchor": {
            "match": {
              "text": "Fee Simple",
              "type": "startsWith"
            }
          },
          "method": {
            "id": "checkbox",          /* returns true if checked, false if unchecked */
            "position": "left"         /* direction to search for checkbox from anchor. enums: left | right */
          }
        },
        {
          "id": "leasehold",
          "anchor": {
            "match": {
              "text": "Leasehold",
              "type": "startsWith"
            }
          },
          "method": {
            "id": "checkbox",
            "position": "left"
          }
        },
        {
          "id": "other",
          "anchor": {
            "match": {
              "text": "other",
              "type": "startsWith"
            },
            "end": {
              "text": "assignment type", /* optional. stop searching at this line */
              "type": "startsWith"
            }
          },
          "method": {
            "id": "checkbox",
            "position": "left"
          }
        },
        {
          "id": "property_rights_appraised",
          "method": {
            "id": "pickValues",
            "match": "one",                              /* default: all. one: for mutually exclusive groups; returns null if none or more than one matches */
            "source_ids": ["fee simple", "leasehold", "other"] /* IDs of the fields to evaluate */
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

## Extract the final appraised value

See the following screenshot for an overview of how to extract the final appraised value:

[IMAGE: Screenshot showing the final_reconciled_value field extraction (left pane: query. middle pane: document. right pane: output)]

The query in the left pane in the preceding image extracts `final_reconciled_value` by anchoring on "The market value" and reading the number to its right using the Region method. The PDF is displayed in the middle pane, and the extracted data is in the right pane.

To try this out yourself, paste the following queries into the left pane of the Sensible app.

```json
{
  "fields": [
    {
      "id": "reconciliation",  /* user-friendly ID for extracted target data */
      "type": "sections",      /* scopes child fields to a defined region of the document; returns each section as an object */
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
          "id": "final_reconciled_value",
          "type": "number",                /* Sensible formats extracted data as this data type, or returns null if it doesn't recognize extracted data as the specified type */
          "anchor": {
            "match": {
              "text": "The market value",
              "type": "includes"
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
      "final_reconciled_value": { "source": "825,000", "value": 825000, "type": "number" }
    }
  ]
}
```

The full config adds fallback anchors for Form 1004 variants where the appraised value sentence is worded differently — Sensible returns the first non-null result across all anchors.

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
              "text": "Form 1004",
              "type": "includes"
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
          "text": "file #",
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
      "id": "subject",
      "type": "sections",    /* scopes child fields to a defined region of the document; returns each section as an object */
      "range": {
        "anchor": {
          "match": {
            "text": "property address",
            "type": "startsWith"
          }
        },
        "stop": {
          "text": "did not analyze the contract",
          "type": "includes"
        }
      },
      "fields": [            /* array of fields to extract from each section. can include computed fields */
        {
          "id": "fee simple",
          "anchor": {
            "match": {
              "text": "Fee Simple",
              "type": "startsWith"
            }
          },
          "method": { "id": "checkbox", "position": "left" } /* returns true if checked, false if unchecked. position enums: left | right */
        },
        {
          "id": "leasehold",
          "anchor": {
            "match": {
              "text": "Leasehold",
              "type": "startsWith"
            }
          },
          "method": { "id": "checkbox", "position": "left" }
        },
        {
          "id": "other",
          "anchor": {
            "match": {
              "text": "other",
              "type": "startsWith"
            },
            "end": {
              "text": "assignment type", /* optional. stop searching at this line */
              "type": "startsWith"
            }
          },
          "method": { "id": "checkbox", "position": "left" }
        },
        {
          "id": "property_rights_appraised",
          "method": {
            "id": "pickValues",
            "match": "one",                                    /* default: all. one: for mutually exclusive groups; returns null if none or more than one matches */
            "source_ids": ["fee simple", "leasehold", "other"] /* IDs of the fields to evaluate */
          }
        }
      ]
    },
    {
      "id": "reconciliation",
      "type": "sections",
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
          "text": "form 1004",
          "type": "includes"
        },
        "stopOffsetY": -0.15   /* default: 0. shift each section's bottom boundary in inches from stop line. positive: down, negative: up */
      },
      "fields": [
        {
          "id": "final_reconciled_value",
          "type": "number",                /* Sensible formats extracted data as this data type, or returns null if it doesn't recognize extracted data as the specified type */
          "anchor": {
            "match": {
              "text": "The market value",
              "type": "includes"
            }
          },
          "method": {
            "id": "region",
            "start": "left",
            "offsetX": -0.05,
            "offsetY": -0.1,
            "width": 7.7,
            "height": 0.17,
            "wordFilters": [
              "The market value of the subject property as of",
              "$"
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
  "reconciliation": [
    {
      "final_reconciled_value": { "source": "825,000", "value": 825000, "type": "number" }
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

Because the Form 1004 is a standardized, layout-consistent form, Sensible uses deterministic layout-based methods rather than probabilistic LLMs. The extracted values are either exactly right or null, with no hallucination risk. For the document in this post, key fields like the appraised value and property rights all extracted correctly on the first pass.

**How does Sensible handle Form 1004 documents from different software vendors?**

The fingerprint method routes each incoming document to the correct config automatically based on layout-identifying text. The config above targets Fannie Mae Form 1004 PDFs. If your pipeline also includes Form 1073 (condo), Form 1025 (2-4 unit), or Form 2055 (exterior-only), you'd create separate configs for each and Sensible routes them automatically.

**Can Sensible extract from Form 1004s bundled with other documents in a loan package?**

Yes. Sensible's portfolio method splits multi-document PDFs (loan packages, closing binders) into individual documents and routes each to the appropriate config before extraction. This means you can submit an entire loan package and receive structured data for each document type in one API response.

**How long does it take to set up Form 1004 extraction?**

The prebuilt open-source config covers the full form and is ready to use immediately. Customizing it for a specific variant (adding fields, tweaking region coordinates) typically takes under an hour using the Sensible app's visual editor.
