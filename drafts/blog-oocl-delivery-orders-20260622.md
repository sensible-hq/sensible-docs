# How to extract data from OOCL delivery orders with Sensible

If you're building software for logistics and freight operations, chances are you've come across the delivery order. Issued by ocean carriers when cargo arrives at a destination port, a delivery order authorizes the release of goods to the consignee — and it contains the routing, cargo, and timing details that downstream fulfillment, customs, and inventory systems need. However, companies often lack access to delivery orders in any format other than PDFs, which makes data extraction a potentially difficult problem.

With Sensible you can easily extract key information out of delivery order PDFs using SenseML, Sensible's query language for extracting data from documents. We've written a library of open-source SenseML configurations, so you don't need to write queries from scratch for common documents. From there, your delivery order data is accessible via API, Sensible's UI, or 5,000 other software integrations thanks to Zapier.

## What we'll cover

This blog post briefly walks you through configuring extractions for OOCL delivery orders. By the end, you'll know a couple of SenseML methods and you'll be on your way to extracting any data you choose using our documentation or our prebuilt open-source delivery order configurations.

## Prerequisites

To extract from this document, take the following steps: Sign up for a **Sensible account**. After completing onboarding, click the **Document types** tab and click **Create new document type**. In the dialog, upload the example document below. Leave all defaults as-is except ensure "Auto-generate configuration" is disabled, then click **Create**. [Download OOCL delivery order sample]. Name the document type `oocl_delivery_orders`.

## Write document extraction queries with SenseML

Let's walk through extracting specific pieces of data from a delivery order. Here's an example of an OOCL delivery order PDF with redacted data:

[IMAGE: example OOCL delivery order PDF screenshot]

To keep the example in this post simple, let's extract just the:
- departure date
- cargo line items (marks, package count, description, weight, and measurement)

## Identify and classify incoming delivery orders

Four text conditions uniquely identify the OOCL delivery order format; all must pass before field extraction runs.

```json5
/* Sensible uses JSON5 to support in-line comments*/
{
  "fingerprint": {       /* optional. Sensible skips this config if these tests fail, improving performance when you have multiple configs */
    "tests": [           /* array of match tests; by default all tests must pass for the config to run */
      {
        "type": "startsWith", /* match types: startsWith | endsWith | includes | equals | regex */
        "text": "delivery order" /* string to match */
      },
      {
        "type": "equals", /* match types: startsWith | endsWith | includes | equals | regex */
        "text": "CONSIGNEE", /* string to match */
        "isCaseSensitive": true /* default: false */
      },
      {
        "type": "endsWith", /* match types: startsWith | endsWith | includes | equals | regex */
        "text": "VOYAGE", /* string to match */
        "isCaseSensitive": true /* default: false */
      },
      {
        "type": "includes", /* match types: startsWith | endsWith | includes | equals | regex */
        "text": "PIECE COUNT", /* string to match */
        "isCaseSensitive": true /* default: false */
      }
    ]
  }
}
```

Sensible uses these tests to route each incoming document to the correct config automatically. If a document fails any test, Sensible skips this config and tries the next one — useful when a document type has multiple carrier- or vendor-specific layouts.

[IMAGE: screenshot showing fingerprint tests in Sensible app]

## Extract departure date

See the following screenshot for an overview of how to extract the departure date:

[IMAGE: Extract departure date (left pane: query. middle pane: document. right pane: output)]

The query in the left pane in the preceding image locates the label "DEPARTURE" and reads the date value printed directly below it, then normalizes it to ISO 8601 format. The PDF is displayed in the middle pane, and the extracted date is in the right pane.

To try this out yourself, paste the following query, or "departure", into the left pane of the Sensible app.

```json5
/* Sensible uses JSON5 to support in-line comments*/
{
  "fields": [
    {
      "id": "departure",        /* user-friendly ID for extracted target data */
      "type": "date",           /* Sensible formats extracted data as this data type, or returns null if it doesn't recognize extracted data as the specified type */
      "anchor": {               /* an anchor is text that always occurs in the same position relative to your target data. Without an anchor, Sensible wouldn't know which page to search in for your target data. */
        "match": {              /* locates the anchor line. accepts a single Match object or an array of Match objects */
          "type": "equals",     /* matching line must equal the string exactly */
          "text": "departure"   /* string to match */
        }
      },
      "method": {
        "id": "label",          /* extracts the line directly adjacent to the anchor */
        "position": "below"     /* target data is below the anchor */
      }
    }
  ]
}
```

You'll get this output:

```json
{
  "departure": {
    "source": "Mar 14 2023",
    "value": "2023-03-14T00:00:00.000Z",
    "type": "date"
  }
}
```

Sensible normalizes the raw text `"Mar 14 2023"` to an ISO 8601 timestamp. The `source` field shows what was read from the PDF, making it easy to verify the extraction.

## Extract cargo line items

See the following screenshot for an overview of how to extract the cargo line items:

[IMAGE: Extract goods (left pane: query. middle pane: document. right pane: output)]

The queries in the left pane in the preceding image use the sections method to find each cargo row in the goods table, then use intersection queries to pluck each cell value from its column. The PDF is displayed in the middle pane, and the extracted cargo items are in the right pane.

To try this out yourself, paste the following queries, or "goods", into the left pane of the Sensible app.

```json5
/* Sensible uses JSON5 to support in-line comments*/
{
  "fields": [
    {
      "id": "goods",             /* ID for the extracted array of sections */
      "type": "sections",       /* extracts repeating sections; returns each section as an object */
      "range": {
        "externalRange": {      /* scopes the section group to the goods table only */
          "anchor": { "type": "equals", "text": "description of goods" },
          "stop": { "type": "equals", "text": "description of goods" },
          "offsetY": -0.05,     /* shift the scope's top boundary up slightly */
          "stopOffsetY": 0.05,  /* shift the scope's bottom boundary down slightly */
          "anchorIsAbsolute": true /* offsets are relative to the page top-left, not the anchor */
        },
        "anchor": {             /* required. defines which lines start each section */
          "match": {            /* required. repeated text marking the start of each section */
            "type": "all",      /* all sub-matches must pass */
            "matches": [
              {
                "type": "not",
                "match": { "type": "equals", "text": "total:" } /* exclude the totals row */
              },
              { "type": "regex", "pattern": "\\d+\\s?(kg|g)", "flags": "ig" } /* match lines containing a weight value */
            ]
          },
          "end": { "type": "equals", "text": "piece count" } /* optional. stop looking for sections after this line */
        },
        "stop": { "type": "equals", "text": "piece count" }, /* optional. text marking each section's bottom boundary */
        "stopOffsetY": -0.1     /* shift each section's bottom boundary up slightly */
      },
      "fields": [               /* array of fields to extract from each section */
        {
          "id": "marks",        /* user-friendly ID for extracted target data */
          "anchor": {           /* an anchor is text that always occurs in the same position relative to your target data. */
            "match": { "type": "equals", "text": "marks" }
          },
          "method": {
            "id": "intersection",
            "horizontalAnchor": {
              "match": { "type": "regex", "pattern": "\\d+\\s?(kg|g)" } /* defines the horizontal axis (row): the weight value line */
            },
            "width": 1,         /* default: 0. zero creates a point intersection, non-zero creates a horizontal-line region */
            "offsetX": -0.1     /* default: 0. offset the vertical line left (negative) or right (positive) in inches */
          }
        },
        {
          "id": "package",      /* user-friendly ID for extracted target data */
          "anchor": { "match": { "type": "equals", "text": "package" } },
          "method": {
            "id": "intersection",
            "horizontalAnchor": {
              "match": { "type": "regex", "pattern": "\\d+\\s?(kg|g)" }
            },
            "width": 1,
            "offsetX": -0.1,
            "percentOverlapX": 0.5 /* default: 0.9. fraction of width overlap required for a line to be "inside" the region defined by Width or Height parameters; 0 accepts any overlap */
          }
        },
        {
          "id": "description_of_goods", /* user-friendly ID for extracted target data */
          "anchor": {
            "match": { "type": "equals", "text": "description of goods" }
          },
          "method": {
            "id": "intersection",
            "horizontalAnchor": {
              "match": { "type": "regex", "pattern": "\\d+\\s?(kg|g)" }
            },
            "width": 2,
            "height": 2,        /* default: 0. same as width, but for height of the intersection region */
            "offsetY": 0.8,     /* default: 0. offset the horizontal line up (negative) or down (positive) in inches */
            "wordFilters": ["description of goods"] /* exclude the column header text from the extracted value */
          }
        },
        {
          "id": "weight",       /* user-friendly ID for extracted target data */
          "type": "weight",     /* Sensible formats extracted data as this data type, or returns null if it doesn't recognize extracted data as the specified type */
          "anchor": { "match": { "type": "equals", "text": "weight" } },
          "method": {
            "id": "intersection",
            "horizontalAnchor": {
              "match": { "type": "regex", "pattern": "\\d+\\s?(kg|g)" }
            },
            "width": 1,
            "offsetX": -0.2,
            "percentOverlapX": 0.5
          }
        },
        {
          "id": "measurement",  /* user-friendly ID for extracted target data */
          "anchor": { "match": { "type": "equals", "text": "measurement" } },
          "method": {
            "id": "intersection",
            "horizontalAnchor": {
              "match": { "type": "regex", "pattern": "\\d+\\s?(kg|g)" }
            },
            "width": 0.8,
            "offsetX": -0.1
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
  "goods": [
    {
      "marks": {
        "type": "string",
        "value": "N/M"
      },
      "package": {
        "type": "string",
        "value": "235 Packages"
      },
      "description_of_goods": {
        "type": "string",
        "value": "MESH BAGS FREIGHT PREPAID"
      },
      "weight": {
        "source": "16200 KG",
        "value": 16200,
        "unit": "kilograms",
        "type": "weight"
      },
      "measurement": {
        "type": "string",
        "value": "68 CBM"
      }
    }
  ]
}
```

The sections method returns an array of objects — one per cargo row. The sample OOCL delivery order has a single cargo line item, but the config handles multiple rows automatically; shipments with several commodity types will produce multiple objects in the `goods` array.

## Putting it all together

Here's the complete SenseML config combining everything we've covered:

<!-- CONFIG:START -->
```json5
/* Sensible uses JSON5 to support in-line comments*/
{
  "fingerprint": {       /* optional. Sensible skips this config if these tests fail, improving performance when you have multiple configs */
    "tests": [           /* array of match tests; by default all tests must pass for the config to run */
      {
        "type": "startsWith", /* match types: startsWith | endsWith | includes | equals | regex */
        "text": "delivery order" /* string to match */
      },
      {
        "type": "equals", /* match types: startsWith | endsWith | includes | equals | regex */
        "text": "CONSIGNEE", /* string to match */
        "isCaseSensitive": true /* default: false */
      },
      {
        "type": "endsWith", /* match types: startsWith | endsWith | includes | equals | regex */
        "text": "VOYAGE", /* string to match */
        "isCaseSensitive": true /* default: false */
      },
      {
        "type": "includes", /* match types: startsWith | endsWith | includes | equals | regex */
        "text": "PIECE COUNT", /* string to match */
        "isCaseSensitive": true /* default: false */
      }
    ]
  },
  "fields": [
    {
      "id": "departure",        /* user-friendly ID for extracted target data */
      "type": "date",           /* Sensible formats extracted data as this data type, or returns null if it doesn't recognize extracted data as the specified type */
      "anchor": {               /* an anchor is text that always occurs in the same position relative to your target data. Without an anchor, Sensible wouldn't know which page to search in for your target data. */
        "match": {              /* locates the anchor line. accepts a single Match object or an array of Match objects */
          "type": "equals",     /* matching line must equal the string exactly */
          "text": "departure"   /* string to match */
        }
      },
      "method": {
        "id": "label",          /* extracts the line directly adjacent to the anchor */
        "position": "below"     /* target data is below the anchor */
      }
    },
    {
      "id": "goods",             /* ID for the extracted array of sections */
      "type": "sections",       /* extracts repeating sections; returns each section as an object */
      "range": {
        "externalRange": {
          "anchor": { "type": "equals", "text": "description of goods" },
          "stop": { "type": "equals", "text": "description of goods" },
          "offsetY": -0.05,
          "stopOffsetY": 0.05,
          "anchorIsAbsolute": true
        },
        "anchor": {             /* required. defines which lines start each section */
          "match": {            /* required. repeated text marking the start of each section */
            "type": "all",      /* all sub-matches must pass */
            "matches": [
              {
                "type": "not",
                "match": { "type": "equals", "text": "total:" }
              },
              { "type": "regex", "pattern": "\\d+\\s?(kg|g)", "flags": "ig" }
            ]
          },
          "end": { "type": "equals", "text": "piece count" }
        },
        "stop": { "type": "equals", "text": "piece count" }, /* optional. text marking each section's bottom boundary */
        "stopOffsetY": -0.1
      },
      "fields": [               /* array of fields to extract from each section */
        {
          "id": "marks",
          "anchor": { "match": { "type": "equals", "text": "marks" } },
          "method": {
            "id": "intersection",
            "horizontalAnchor": {
              "match": { "type": "regex", "pattern": "\\d+\\s?(kg|g)" } /* defines the horizontal axis (row): the weight value line */
            },
            "width": 1,         /* default: 0. zero creates a point intersection, non-zero creates a horizontal-line region */
            "offsetX": -0.1     /* default: 0. offset the vertical line left (negative) or right (positive) in inches */
          }
        },
        {
          "id": "package",      /* user-friendly ID for extracted target data */
          "anchor": { "match": { "type": "equals", "text": "package" } },
          "method": {
            "id": "intersection",
            "horizontalAnchor": {
              "match": { "type": "regex", "pattern": "\\d+\\s?(kg|g)" }
            },
            "width": 1,
            "offsetX": -0.1,
            "percentOverlapX": 0.5 /* default: 0.9. fraction of width overlap required for a line to be "inside" the region defined by Width or Height parameters; 0 accepts any overlap */
          }
        },
        {
          "id": "description_of_goods", /* user-friendly ID for extracted target data */
          "anchor": {
            "match": { "type": "equals", "text": "description of goods" }
          },
          "method": {
            "id": "intersection",
            "horizontalAnchor": {
              "match": { "type": "regex", "pattern": "\\d+\\s?(kg|g)" }
            },
            "width": 2,
            "height": 2,        /* default: 0. same as width, but for height of the intersection region */
            "offsetY": 0.8,     /* default: 0. offset the horizontal line up (negative) or down (positive) in inches */
            "wordFilters": ["description of goods"]
          }
        },
        {
          "id": "weight",       /* user-friendly ID for extracted target data */
          "type": "weight",     /* Sensible formats extracted data as this data type, or returns null if it doesn't recognize extracted data as the specified type */
          "anchor": { "match": { "type": "equals", "text": "weight" } },
          "method": {
            "id": "intersection",
            "horizontalAnchor": {
              "match": { "type": "regex", "pattern": "\\d+\\s?(kg|g)" }
            },
            "width": 1,
            "offsetX": -0.2,
            "percentOverlapX": 0.5
          }
        },
        {
          "id": "measurement",  /* user-friendly ID for extracted target data */
          "anchor": { "match": { "type": "equals", "text": "measurement" } },
          "method": {
            "id": "intersection",
            "horizontalAnchor": {
              "match": { "type": "regex", "pattern": "\\d+\\s?(kg|g)" }
            },
            "width": 0.8,
            "offsetX": -0.1
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
  "departure": {
    "source": "Mar 14 2023",
    "value": "2023-03-14T00:00:00.000Z",
    "type": "date"
  },
  "goods": [
    {
      "marks": {
        "type": "string",
        "value": "N/M"
      },
      "package": {
        "type": "string",
        "value": "235 Packages"
      },
      "description_of_goods": {
        "type": "string",
        "value": "MESH BAGS FREIGHT PREPAID"
      },
      "weight": {
        "source": "16200 KG",
        "value": 16200,
        "unit": "kilograms",
        "type": "weight"
      },
      "measurement": {
        "type": "string",
        "value": "68 CBM"
      }
    }
  ]
}
```

## Extract more delivery order data

We've covered how to extract a couple pieces of data from a delivery order. The full OOCL config extracts much more information, including vessel name and voyage, vessel call sign, ports of loading and discharge, place of delivery, and estimated cargo arrival date. In the following screenshot, every blue-outlined line is a piece of extracted data:

[IMAGE: full extraction screenshot showing all highlighted fields]

## When to use a layout-specific config vs. a generalized config

A layout-specific config is the right choice when a carrier appears regularly in your pipeline and the delivery order format is consistent across shipments. The OOCL config above anchors to OOCL's specific label text and table structure — no LLM calls, no prompt maintenance, and consistent output on every OOCL delivery order that enters the pipeline. For carriers that appear less frequently or whose format you haven't templated yet, a generalized LLM config handles extraction on day one without any layout-specific tuning. Both run through the same API endpoint, and Sensible's fingerprint method routes each document to the right config automatically, based on carrier-identifying text in the document.

## Connect Sensible to your workflow

Once your SenseML config is set up, there are several ways to integrate delivery order extraction into your application or process.

- **Python SDK** — wraps the extraction API; install with pip and start extracting in minutes
- **MCP server** — connects document extraction to AI coding tools like Claude
- **API (synchronous and asynchronous)** — synchronous returns data inline; asynchronous accepts a webhook, recommended for high-volume workflows
- **Zapier** — no-code integration; routes extracted data into Google Sheets, Airtable, Slack, and more

## FAQ

**What fields can be extracted from an OOCL delivery order?**

The config demonstrated in this post extracts vessel and voyage, vessel call sign, port of loading, departure date, port of discharge, place of delivery, estimated cargo arrival date, and per-line cargo details including marks, package count, description of goods, weight, and measurement.

**How accurate is automated delivery order extraction?**

The label and intersection methods used here are deterministic — they anchor to fixed label text and column positions that OOCL uses consistently. You can expect high accuracy on any OOCL delivery order that matches the layout.

**How does Sensible handle delivery orders from multiple carriers?**

Each carrier's layout gets its own config. Sensible's fingerprint method reads identifying text in the document to route each incoming document to the right config automatically. For carriers you haven't templated yet, a generalized LLM-based config handles extraction on day one.

**Can Sensible extract from delivery orders bundled with other documents?**

Yes. Sensible's portfolio method lets you extract from multi-document PDFs — for example, a package that includes a bill of lading, a delivery order, and a customs declaration. Sensible classifies each page and applies the appropriate config.

**How long does it take to set up delivery order extraction?**

A layout-specific config like the one in this post typically takes under an hour for a carrier you receive regularly. You anchor to label text and table headers, tune the intersection offsets, and publish. Sensible's editor shows extracted values in real time as you build.
