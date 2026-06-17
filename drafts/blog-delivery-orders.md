# How to extract data from delivery orders with Sensible

Delivery orders are foundational documents in international freight and logistics. Issued by a carrier or shipping agent to authorize the release of cargo to a consignee, a delivery order contains critical shipment details — vessel and voyage information, ports of loading and discharge, estimated arrival dates, and itemized cargo descriptions with weights and measurements. Companies building logistics software, freight forwarding platforms, or customs brokerage tools need this data to automate cargo tracking, invoice reconciliation, and compliance workflows.

However, they often lack access to delivery orders in any format other than PDFs, which makes data extraction a potentially difficult problem.

With Sensible you can easily extract key information out of delivery order PDFs using SenseML, Sensible's query language for extracting data from documents. We've written a library of open-source SenseML configurations, so you don't need to write queries from scratch for common documents. From there, your delivery order data is accessible via API, Sensible's UI, or 5,000 other software integrations thanks to Zapier.

## What we'll cover

This blog post briefly walks you through configuring extractions for OOCL delivery orders. By the end, you'll know a few SenseML methods and you'll be on your way to extracting any data you choose using our documentation or our prebuilt open-source delivery order configurations.

## Write document extraction queries with SenseML

Let's walk through extracting specific pieces of data from a delivery order. Here's an example of a delivery order PDF with redacted or dummy data:

[IMAGE: example OOCL delivery order PDF screenshot]

To follow along, you can sign up for a Sensible account, then download an example PDF for an OOCL delivery order and upload it to the Sensible app, or import the PDF and prebuilt open-source delivery order configurations directly to the Sensible app.

To keep the example in this post simple, let's extract just the:

- departure date
- port of discharge
- goods line items (description and weight)

## Extract departure date

See the following screenshot for an overview of how to extract the departure date:

[IMAGE: screenshot of departure date extraction in Sensible app] *(caption: "Extract departure date (left pane: query. middle pane: document. right pane: output)")*

The query in the left pane in the preceding image finds the "departure" label and extracts the date value printed directly below it. The PDF is displayed in the middle pane, and the extracted date is in the right pane.

To try this out yourself, paste the following query, or "departure," into the left pane of the Sensible app.

```json5
/* Sensible uses JSON5 to support in-line comments*/
{
  "fields": [
    {
      "id": "departure",           /* user-friendly ID for extracted target data */
      "type": "date",              /* Sensible formats extracted data as this data type, or returns null if it doesn't recognize extracted data as the specified type */
      "anchor": {                  /* an anchor is text that always occurs in the same position relative to your target data. */
        "match": {               /* locates the anchor line. accepts a single Match object or an array of Match objects */
          "type": "equals",        /* matching line must equal the string exactly */
          "text": "departure"      /* string to match */
        }
      },
      "method": {
        "id": "label",             /* target data is labeled by nearby text in the document */
        "position": "below"        /* target data appears below the anchor label */
      }
    }
  ]
}
```

You'll get this output:

```json
{
  "departure": {
    "source": "15 MAR 2024",
    "value": "2024-03-15T00:00:00.000Z",
    "type": "date"
  }
}
```

## Extract port of discharge

See the following screenshot for an overview of how to extract the port of discharge:

[IMAGE: screenshot of port of discharge extraction in Sensible app] *(caption: "Extract port of discharge (left pane: query. middle pane: document. right pane: output)")*

The query in the left pane in the preceding image locates the "port of discharge" label and returns the text printed below it. The PDF is displayed in the middle pane, and the extracted port name is in the right pane.

To try this out yourself, paste the following query, or "port_of_discharge," into the left pane of the Sensible app.

```json5
/* Sensible uses JSON5 to support in-line comments*/
{
  "fields": [
    {
      "id": "port_of_discharge",   /* user-friendly ID for extracted target data */
      "anchor": {                  /* an anchor is text that always occurs in the same position relative to your target data. */
        "match": {               /* locates the anchor line. accepts a single Match object or an array of Match objects */
          "type": "equals",        /* matching line must equal the string exactly */
          "text": "port of discharge" /* string to match */
        }
      },
      "method": {
        "id": "label",             /* target data is labeled by nearby text in the document */
        "position": "below"        /* target data appears below the anchor label */
      }
    }
  ]
}
```

You'll get this output:

```json
{
  "port_of_discharge": "LOS ANGELES, CA"
}
```

## Extract goods line items

Delivery orders list multiple cargo line items in a table — each row contains a cargo description, weight, and measurement. The **sections** method lets you split this table into individual line items and extract fields from each one. Within each section, the **intersection** method targets a specific cell by locating both a column heading (the vertical anchor) and a row anchor simultaneously.

See the following screenshot for an overview of how to extract the goods line items:

[IMAGE: screenshot of goods sections extraction in Sensible app] *(caption: "Extract goods line items (left pane: query. middle pane: document. right pane: output)")*

The queries in the left pane in the preceding image define a section for each cargo row in the goods table, then extract the description and weight from each section using intersection queries. The PDF is displayed in the middle pane, and the extracted array of line items is in the right pane.

To try this out yourself, paste the following queries, or "goods," into the left pane of the Sensible app.

```json5
/* Sensible uses JSON5 to support in-line comments*/
{
  "fields": [
    {
      "id": "goods",               /* user-friendly ID for extracted target data */
      "type": "sections",          /* extracts repeating sections; returns each section as an object */
      "range": {
        "anchor": {              /* an anchor is text that always occurs in the same position relative to your target data. */
          "match": {             /* locates the anchor line. accepts a single Match object or an array of Match objects */
            "type": "all",         /* all matches must be true for the anchor to match */
            "matches": [
              {
                "type": "not",     /* equals | startsWith | endsWith | includes | regex | first | any | all | not */
                "match": { "type": "equals", "text": "total:" }
              },
              {
                "type": "regex",   /* match anywhere in line */
                "pattern": "\\d+\\s?(kg|g)",
                "flags": "ig"
              }
            ]
          },
          "end": {               /* optional. stop looking for sections after this line */
            "type": "equals",      /* matching line must equal the string exactly */
            "text": "piece count"  /* string to match */
          }
        },
        "stop": {                /* optional. text marking each section's bottom boundary; if omitted, each section ends where the next starts */
          "type": "equals",        /* matching line must equal the string exactly */
          "text": "piece count"    /* optional. text marking each section's bottom boundary */
        },
        "stopOffsetY": -0.1        /* default: 0. shift each section's bottom boundary in inches from stop line. positive: down, negative: up */
      },
      "fields": [                  /* array of fields to extract from each section */
        {
          "id": "description_of_goods", /* user-friendly ID for extracted target data */
          "anchor": {              /* an anchor is text that always occurs in the same position relative to your target data. */
            "match": { "type": "equals", "text": "description of goods" } /* locates the anchor line. accepts a single Match object or an array of Match objects */
          },
          "method": {
            "id": "intersection",
            "horizontalAnchor": {  /* defines the horizontal axis (the row). Sensible finds the line matching this pattern and uses its vertical position to form the intersection point */
              "match": { "type": "regex", "pattern": "\\d+\\s?(kg|g)" }
            },
            "width": 2,            /* default: 0. non-zero creates a horizontal-line region for extraction */
            "height": 2,           /* default: 0. same as width, but for height of the intersection region */
            "offsetY": 0.8,        /* default: 0. offset the horizontal line down (positive) in inches */
            "wordFilters": ["description of goods"] /* omit these strings from extracted output */
          }
        },
        {
          "id": "weight",          /* user-friendly ID for extracted target data */
          "type": "weight",        /* Sensible formats extracted data as this data type, or returns null if it doesn't recognize extracted data as the specified type */
          "anchor": {              /* an anchor is text that always occurs in the same position relative to your target data. */
            "match": { "type": "equals", "text": "weight" } /* locates the anchor line. accepts a single Match object or an array of Match objects */
          },
          "method": {
            "id": "intersection",
            "horizontalAnchor": {  /* defines the horizontal axis (the row) */
              "match": { "type": "regex", "pattern": "\\d+\\s?(kg|g)" }
            },
            "width": 1,            /* default: 0. non-zero creates a horizontal-line region for extraction */
            "offsetX": -0.2,       /* default: 0. offset the vertical line left (negative) in inches */
            "percentOverlapX": 0.5 /* default: 0.9. fraction of width overlap required for a line to be "inside" the region */
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
      "description_of_goods": "ELECTRONICS - LCD MONITORS",
      "weight": {
        "source": "2450 KG",
        "value": 2450,
        "unit": "kg"
      }
    },
    {
      "description_of_goods": "COMPUTER ACCESSORIES - KEYBOARDS & MICE",
      "weight": {
        "source": "380 KG",
        "value": 380,
        "unit": "kg"
      }
    }
    /* JSON output abbreviated */
  ]
}
```

## Extract more delivery order data

We've covered how to extract a few pieces of data from a delivery order. Our prebuilt config extracts much more information. Check it out! In the following screenshot, every blue-outlined line is a piece of extracted data:

[IMAGE: full delivery order extraction screenshot showing all extracted fields highlighted]

The complete config extracts vessel name and voyage, vessel call sign, port of loading, place of delivery, estimated cargo arrival date, and full goods line items including package type, marks, and measurements — everything your downstream logistics workflow needs.

## Start extracting from your documents

Stop relying on manual data entry. With Sensible, claim back valuable time, your ops team will thank you, and you can deliver a superior user experience. It's a win-win.
