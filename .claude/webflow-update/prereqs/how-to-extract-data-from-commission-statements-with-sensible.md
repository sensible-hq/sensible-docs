# How to extract data from commission statements with Sensible

## Introduction: What are commission statements?

Commission statements are carrier-issued documents that detail producer compensation on policies written, renewed, endorsed, or cancelled during a billing period. Reconciling them manually across dozens of carriers introduces keying errors and delays close. Sensible's layout-based extraction targets carrier-specific column structures and returns typed, schema-validated output per commission row through a single API endpoint.  
  
Insurance commission statements are the operational backbone of broker and MGA back-office teams. Every carrier issues one, typically monthly, detailing what each producer earned on each policy transaction during the period. A mid-size brokerage receiving statements from 20 or more carriers each month faces hundreds of line items per statement to process: policy numbers, product types, transaction dates, premium amounts, commission rates, and net commission due. Working through that volume manually is error-prone and slow.  
  
This post uses Sun Life's commission statement as a worked example. Every carrier has its own layout — column ordering, label conventions, subtotal placement — so the right approach is a per-carrier deterministic config: fixed column positions and consistent label text mean the same config extracts reliably every month. For the long tail of smaller carriers, a generalized LLM config handles the same fields without per-carrier work. Both run through the same API.  
‍

## What we'll cover:

  * Extract the statement-level disbursement total
  * Extract commission line items using nested Sections
  * Propagate policy and broker totals into each line item row



##   
Prerequisites

To extract from this document, take the following steps:  
‍

  * Sign up for a [Sensible account](https://app.sensible.so/register/)
  * Add prebuilt extraction support for commission statements to your account. Follow the steps in [Out-of-the-box extractions](https://docs.sensible.so/docs/library-quickstart) and select **commission statements**.
