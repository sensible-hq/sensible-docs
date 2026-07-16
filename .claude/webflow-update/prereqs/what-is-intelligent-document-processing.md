# What is intelligent document processing?

## What Is Intelligent Document Processing?

Intelligent Document Processing (IDP) is a software category that automatically classifies, extracts, validates, and routes structured data from business documents into downstream systems. At scale, manual extraction introduces errors, delays, and gaps in audit coverage. Sensible is a document extraction platform that uses SenseML, a declarative configuration language you version-control, to combine deterministic layout-based extraction with LLM parsing. The result is typed, schema-validated output through a single API endpoint regardless of document format or issuer.

‍

IDP moves information from unstructured sources (PDFs, scanned images, [email attachments](https://docs.sensible.so/docs/getting-started-email), [spreadsheets](https://docs.sensible.so/docs/cell-rows)) into structured formats that business systems can consume: ERP platforms like SAP and NetSuite, CRM systems like Salesforce, loan origination platforms, and downstream APIs. The four-stage pipeline below covers how that happens in production.

‍

## How IDP Works: Four Stages

A complete IDP pipeline covers four stages. A gap in any stage compounds forward.  
‍

### 1\. Ingest

Documents arrive from many sources: email attachments, file uploads, API calls, scanning hardware, shared drives, Slack. The ingest stage normalizes this input: OCR converts image-based pages to searchable text, multi-page PDFs are split or segmented by document type, and spreadsheets undergo format normalization before extraction runs.  
‍

OCR quality is the first reliability problem in IDP. Poor scan resolution, skewed pages, and low-contrast printing degrade text before extraction begins. Sensible's [OCR pipeline](https://docs.sensible.so/docs/ocr) pre-processes images and flags scans below a quality threshold rather than silently returning degraded output.

‍

### 2\. Classify

Documents must route to the right extraction logic before extraction runs. A W-2 and a 1099 contain similar fields in different positions. Running a W-2 through a 1099 config returns incorrect values without raising an error. Classification errors are silent: the system appears to be working until a downstream process fails.  
‍

Classification runs on layout signatures (fixed-position elements unique to a document type), text [fingerprints](https://docs.sensible.so/docs/fingerprint) (specific phrases that reliably identify a format), or [LLM reasoning](https://docs.sensible.so/docs/descriptions) for document types without consistent identifiers. Accurate classification is a prerequisite for accurate extraction.

‍

### 3\. Extract

Extraction is where most of the complexity lives. The extraction stage runs a config against the classified document and returns a structured output object.  
‍

Document variability is the central engineering challenge. Documents vary on two dimensions: structure (how consistently fields appear at predictable positions) and variability (how many format revisions or issuer variants exist in production).

‍

‍

A [W-2](https://www.irs.gov/forms-pubs/about-form-w-2) sits near one extreme: the IRS standardizes the layout, field positions are predictable across all employers, and deterministic extraction handles the full volume without LLM inference. A legal contract sits near the other: no two look alike, clauses appear in different orders, and LLM-based methods handle the variability where deterministic rules cannot. Most business documents (invoices, bank statements, insurance policies) fall between these extremes.

‍

### 4\. Validate and Monitor

Extraction output that looks plausible is not always correct. The validation stage enforces schema rules: type checking (is this field a valid date? a parseable currency value?), cross-field logic (does the invoice total equal the sum of line items?), and range checks.  
‍

In Sensible, extractions that fall below a confidence threshold route to a human review queue rather than propagating wrong values downstream. Production IDP pipelines should also track extraction metrics over time to catch configurations that degrade as document formats evolve.  
‍

**The four stages look straightforward in a demo environment. The difficulty surfaces in production** , where document variability in the long tail, model updates, and silent extraction failures compound over months of operation. That gap is where most IDP evaluations break down.

‍

## IDP vs. OCR vs. RPA

OCR, RPA, and IDP address adjacent problems in document workflows and are frequently conflated, including by vendors selling all three.  
‍

**OCR** (Optical Character Recognition) converts a document image to raw machine-readable text. It does not interpret content. OCR output is a stream of characters with no field labels, no types, and no structure. OCR is a preprocessing step inside most IDP systems, not a substitute for them.  
‍

**RPA** (Robotic Process Automation) automates repetitive interactions with software interfaces: clicking buttons, copying values across screens, filling out forms. RPA moves data between systems once that data exists in structured form, but it cannot extract named fields from unstructured documents on its own. The common architecture pairs both: IDP extracts the data, RPA routes it into Workday, SAP, Epic, or other destination systems.  
‍

**IDP** combines OCR, classification, extraction logic, and validation into a single pipeline. The output is a typed, schema-validated JSON object ready for downstream consumption.

‍

Capability | OCR | RPA | IDP  
---|---|---|---  
Convert image to text | Yes | No | Yes (as a stage)  
Extract named fields | No | No | Yes  
Validate output against schema | No | No | Yes  
Route to downstream systems | No | Yes | Yes (or via integration)  
Handle document variability | No | No | Yes (approach-dependent)  
Extraction provenance (field-to-source mapping) | No | No | Yes (Sensible-specific)  
  
‍

 _Note: Some RPA platforms maintain process audit logs; extraction provenance is a different capability: mapping each extracted field value back to its source coordinates in the original document._

‍  
‍
