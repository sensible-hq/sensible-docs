# How to extract data from cyber insurance quotes with Sensible

## Introduction**‍**

Cyber insurance quotes are carrier-issued pricing proposals summarizing what coverage a carrier will offer and at what price: aggregate limits per coverage category, per-incident retentions, sublimits for specific risk types, total premium, and commission. Brokers and MGAs receive competing quotes from multiple carriers for every submission, and the comparison work (matching limits, retentions, and sublimits across different carrier formats) is a manual bottleneck at volume.

‍

The extraction challenge compounds in two ways:  
‍

  1. **Carrier format variability.** Beazley structures its cyber quote differently from Coalition, Chubb, or AXA XL, and a config built for one carrier's label conventions breaks on another.**‍**
  2. **Document density.** Cyber quote PDFs are often multi-page documents where the actual quote data sits in the first few pages, followed by carrier services guides and endorsement documentation. Extracting only the relevant fields requires anchoring precisely to the right sections.



  
Sensible handles this through carrier-specific layout configs. Cyber quotes are well suited to this approach: the structured Coverage Schedule tables and endorsement grids provide reliable anchor points that deterministic methods extract precisely, with no LLM calls and no prompt maintenance overhead on high-volume carriers. Each carrier gets its own config anchored to its label text and document structure, returning a normalized output schema across all carriers. For carriers without a layout config yet, a generalized LLM config handles extraction on day one without per-carrier configuration, covering the long tail of carriers that appear at low volume or in one-off submissions.  
‍

This post walks through a Beazley cyber quote using a deterministic layout config. The same approach applies to cyber quotes from any carrier, and to other commercial lines quote types: GL, E&O, D&O, property, and umbrella.

‍

Cyber insurance quotes are multi-page carrier proposals summarizing aggregate limits, per-incident retentions, coverage sublimits, and premium for each coverage option presented. At volume, manual extraction across competing carrier formats is the primary bottleneck in submission comparison workflows. Sensible's carrier-specific layout config extracts the fields that matter for comparison deterministically, returning a consistent schema regardless of which carrier issued the quote.

‍

**What we'll cover:  
‍**

  * How to extract named insured using the [Row](https://docs.sensible.so/docs/row) method
  * How to extract aggregate limits for two coverage options using tiebreakers
  * How to extract premium with a case-sensitive anchor
  * How to extract sublimits by coverage using the [Row](https://docs.sensible.so/docs/row) and [Zip](https://docs.sensible.so/docs/zip) methods



‍

## Prerequisites**‍**

To extract from this document, take the following steps:  
‍

  * Sign up for a [Sensible account  
](https://app.sensible.so/register/)
  * After completing onboarding, click the **Document types** tab and click **Create new document type**. In the dialog, upload the example document below. Leave all defaults as-is except ensure "Auto-generate configuration" is disabled, then click **Create.**  
[Download Beazley cyber quote sample](https://raw.githubusercontent.com/sensible-hq/sensible-docs/v0/assets/pdfs/blog/beazley-cyber-quote-sample.pdf)‍
  * Name the document type `cyber_insurance_quote`



‍
