---
title: "Outline doc"
hidden: true
---



#### Todo before publish

- create an LLM preprocessor category and rename existing to laytoub-ased preprocessor
- fixed LINKS in outline



Creates an outline of the document that helps with downstream data extraction that includes:

- a table of contents with numbered sections.
- references to figures and diagrams and tables

It's not meant for end-user use but if you want to view it, you can set verbosity = 3 in the config, then see it in the API response in an `outline` object.

[**Parameters**] (doc:outline-doc#parameters)
[**Examples**] (doc:outline-doc#examples)
[**Notes**] (doc:outline-doc#notes)

# Parameters


| key                       | value   | description                                                      |
| ------------------------- | ------ | ------------------------------------------------------------ |
| type (**required**)     | `outlineDoc` |  |
| multimodal | boolean.<br/>default: false | ??? |

# Examples

for:

https://dev.sensible.so/editor/?d=frances_playground&c=outline_doc_preprocessor&g=contextual_document_embeddings_withmetadata&v= 

  ```json
          "outline": [
              {
                  "level": 0,
                  "title": "Loss Run Report (Policy Term: 10/1/2020 - 10/1/2021)",
                  "first_line": {
                      "lineIndex": 0,
                      "pageIndex": 0
                  },
                  "section_number": null,
                  "referenced_tables": [],
                  "referenced_figures": [],
                  "summary": "Report for policy H02222222, term 10/1/2020 - 10/1/2021, insured SENSIBLE. Contains claim summaries and details."
              },
              {
                  "level": 1,
                  "title": "Claim 011111",
                  "first_line": {
                      "lineIndex": 16,
                      "pageIndex": 0
                  },
                  "section_number": null,
                  "referenced_tables": [],
                  "referenced_figures": [],
                  "summary": "Claim 011111, adjuster John Smith, supervisor Jane Doe, details of the claim event, loss, and payments."
              },
              {
                  "level": 1,
                  "title": "Claim 022222",
                  "first_line": {
                      "lineIndex": 69,
                      "pageIndex": 0
                  },
                  "section_number": null,
                  "referenced_tables": [],
                  "referenced_figures": [],
                  "summary": "Claim 022222, adjuster John Smith, supervisor Jane Doe, details of the claim event, loss, and payments."
              },
              {
                  "level": 1,
                  "title": "Claim 033333",
                  "first_line": {
                      "lineIndex": 123,
                      "pageIndex": 0
                  },
                  "section_number": null,
                  "referenced_tables": [],
                  "referenced_figures": [],
                  "summary": "Claim 033333, adjuster John Smith, supervisor Jane Doe, details of the claim event, loss, and payments. Includes multiple sub-claims (A, B, C, D) for different claimants."
              },
              {
                  "level": 2,
                  "title": "Sub-claim A (033333)",
                  "first_line": {
                      "lineIndex": 156,
                      "pageIndex": 0
                  },
                  "section_number": null,
                  "referenced_tables": [],
                  "referenced_figures": [],
                  "summary": "Sub-claim A for claim 033333, details of the event, claimant, and payment."
              },
              {
                  "level": 2,
                  "title": "Sub-claim B (033333)",
                  "first_line": {
                      "lineIndex": 173,
                      "pageIndex": 0
                  },
                  "section_number": null,
                  "referenced_tables": [],
                  "referenced_figures": [],
                  "summary": "Sub-claim B for claim 033333, details of the event, claimant, and payment."
              },
              {
                  "level": 2,
                  "title": "Sub-claim C (033333)",
                  "first_line": {
                      "lineIndex": 14,
                      "pageIndex": 1
                  },
                  "section_number": null,
                  "referenced_tables": [],
                  "referenced_figures": [],
                  "summary": "Sub-claim C for claim 033333, details of the event, claimant, and payment."
              },
              {
                  "level": 2,
                  "title": "Sub-claim D (033333)",
                  "first_line": {
                      "lineIndex": 31,
                      "pageIndex": 1
                  },
                  "section_number": null,
                  "referenced_tables": [],
                  "referenced_figures": [],
                  "summary": "Sub-claim D for claim 033333, details of the event, claimant, and payment."
              },
              {
                  "level": 1,
                  "title": "Subtotal (Policy Term: 10/1/2020 - 10/1/2021)",
                  "first_line": {
                      "lineIndex": 46,
                      "pageIndex": 1
                  },
                  "section_number": null,
                  "referenced_tables": [],
                  "referenced_figures": [],
                  "summary": "Subtotal for all claims under policy term 10/1/2020 - 10/1/2021."
              },
              {
                  "level": 0,
                  "title": "Loss Run Report (Policy Term: 10/1/2021 - 10/1/2022)",
                  "first_line": {
                      "lineIndex": 0,
                      "pageIndex": 2
                  },
                  "section_number": null,
                  "referenced_tables": [],
                  "referenced_figures": [],
                  "summary": "Report for policy H02222222, term 10/1/2021 - 10/1/2022, insured SENSIBLE. Contains claim summaries and details."
              },
              {
                  "level": 1,
                  "title": "Claim 055555",
                  "first_line": {
                      "lineIndex": 16,
                      "pageIndex": 2
                  },
                  "section_number": null,
                  "referenced_tables": [],
                  "referenced_figures": [],
                  "summary": "Claim 055555, adjuster John Doe, supervisor Jane Smith, details of the claim event, loss, and payments."
              },
              {
                  "level": 1,
                  "title": "Claim 066666",
                  "first_line": {
                      "lineIndex": 69,
                      "pageIndex": 2
                  },
                  "section_number": null,
                  "referenced_tables": [],
                  "referenced_figures": [],
                  "summary": "Claim 066666, adjuster John Doe, supervisor Jane Smith, details of the claim event, loss, and payments."
              },
              {
                  "level": 1,
                  "title": "Claim 077777",
                  "first_line": {
                      "lineIndex": 122,
                      "pageIndex": 2
                  },
                  "section_number": null,
                  "referenced_tables": [],
                  "referenced_figures": [],
                  "summary": "Claim 077777, adjuster John Doe, supervisor Jane Smith, details of the claim event, loss, and payments."
              },
              {
                  "level": 1,
                  "title": "Subtotal (Policy Term: 10/1/2021 - 10/1/2022)",
                  "first_line": {
                      "lineIndex": 172,
                      "pageIndex": 2
                  },
                  "section_number": null,
                  "referenced_tables": [],
                  "referenced_figures": [],
                  "summary": "Subtotal for all claims under policy term 10/1/2021 - 10/1/2022."
              },
              {
                  "level": 1,
                  "title": "Grand Total",
                  "first_line": {
                      "lineIndex": 177,
                      "pageIndex": 2
                  },
                  "section_number": null,
                  "referenced_tables": [],
                  "referenced_figures": [],
                  "summary": "Grand total for all claims and policy terms in the report."
              }
          ]
  ```







