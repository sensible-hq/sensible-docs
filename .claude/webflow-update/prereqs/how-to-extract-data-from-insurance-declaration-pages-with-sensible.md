# How to extract data from insurance declaration pages with Sensible

## Introduction**‍**

Insurance declaration pages summarize what a policy actually covers: named insured, covered vehicles or properties, coverage types, limits, deductibles, and premium. Underwriters, claims teams, and insurance platforms pull this data continuously for renewals, coverage verification, intake workflows, and loss analysis.  
‍

Dec pages exist for every line of insurance: auto, homeowners, renters, commercial property, umbrella, and more. This post focuses on auto dec pages, but the same two-config approach applies to any line of insurance.  
‍

The extraction challenge is carrier variability. GEICO formats its auto dec page differently from USAA, which formats it differently from Progressive, which formats it differently from Travelers. A templated approach that works for one carrier breaks the moment a new carrier enters the pipeline.  
‍

Sensible handles this through two complementary configs. Dec pages are well suited to this hybrid approach: carrier variability across the long tail requires LLM reasoning to handle without per-carrier configuration, while high-volume carriers like GEICO have fixed, predictable field positions that deterministic methods extract precisely. A generalized LLM config uses the [Query Group](https://docs.sensible.so/docs/query-group) and [List](https://docs.sensible.so/docs/list) methods to extract key fields from any carrier's dec page without prior templates, covering your full carrier mix on day one. A carrier-specific layout config uses deterministic methods ([Region](https://docs.sensible.so/docs/region) and [Row](https://docs.sensible.so/docs/row)) for carriers appearing at high volume, reducing per-document LLM cost and eliminating prompt latency on fields with fixed positions. Both route through the same API endpoint, and Sensible validates each extracted field against its declared type before returning output.  
‍  
  
This post walks through both approaches using USAA (generalized) and GEICO (layout-specific) as examples.  
‍

Insurance declaration pages are carrier-issued policy summaries listing named insured, coverage limits, deductibles, vehicles, and premium amounts. At scale, manual extraction across a multi-carrier pipeline breaks on format variability. Sensible's hybrid config approach handles the full carrier mix through a single API: a generalized LLM template on day one, carrier-specific layout templates for high-volume formats.

‍

**What we'll cover:  
‍**

  * How Sensible identifies the carrier and routes to the right config using the [Fingerprint](https://docs.sensible.so/docs/fingerprint) method
  * How to extract named insured and address with [Query Group](https://docs.sensible.so/docs/query-group) (generalized) and [Region](https://docs.sensible.so/docs/region) (GEICO layout)
  * How to extract the policy period using Region with coordinate offsets
  * How to extract coverage details and liability limits using the List and Row methods
  * How to extract vehicle information
  * When to build a carrier-specific layout template vs. relying on the generalized config



‍  
‍

## Prerequisites

To extract from this document, take the following steps:  
‍

  * Sign up for a [Sensible account](https://app.sensible.so/register/)
  * Add prebuilt extraction support for insurance declaration pages to your account. Follow the steps in [Out-of-the-box extractions](https://docs.sensible.so/docs/library-quickstart) and select insurance declaration pages.
