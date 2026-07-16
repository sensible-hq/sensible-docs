# How to capture the long tail when extracting data from paystubs

## The Challenge of Paystub Processing at Scale

  
In the world of document processing, the Pareto principle often applies: 80% of your document volume comes from 20% of vendors or providers, while the remaining 20% of volume spans across dozens of smaller, regional, and niche vendors. This principle holds true whether you’re extracting transaction information from bank statement PDFs, energy use from utility bills, or coverages from insurance declaration pages.  
  
In this tutorial, we'll implement an 80/20 data extraction approach for paystub document processing. For the 20% of high-volume providers like ADP, Paylocity, and Gusto, it makes perfect sense to invest in tailor-made, document-data extraction configurations that can handle their consistent document formats with speed and accuracy. But what about the long tail? Companies like BizChecks Payroll (Cape Cod regional) or OnPay (agriculture/nonprofit specialist) each have their own unique formatting that would be impractical to support with individually tailored extraction configurations.  
  
Enter SenseML, Sensible's query language for document automation. With SenseML, you can create dedicated [layout-based](https://docs.sensible.so/docs/layout-based-methods) extraction configs tailored to your high-volume providers, then intelligently handle the long tail with an [LLM-based](https://docs.sensible.so/docs/llm-based-methods) extraction config. Whether you're processing paystub data for lending applications, expense management, or compliance reporting, you can then use Sensible to enforce a consistent data output schema of your choice across all documents. From there, your extracted data is accessible via API, the platform UI, or thousands of other software integrations through Zapier.

‍

## What We'll Cover

  
This tutorial focuses on comparing layout-based and LLM-based document data extraction methods, showing you how each approach handles the same data points differently and when to use each strategy. We’ll focus on a couple of major vendors (Paylocity and ADP) and use a generic paystub example for the long tail.  
  


_Sensible app showing layout-based queries, sample ADP document, and extracted document field_

‍

 _Sensible app showing LLM-based queries, sample generic document, and extracted document field_

‍  
Sensible’s prebuilt support for paystub data extraction is comprehensive. To keep it simple, this blog post will walk you through extracting a couple key data points from paystubs using different approaches:  
‍

  * **Employee address**  
  * **Regular pay for this pay period  
‍**



We’ll use the following example documents:  
  


_High-volume format: Paylocity paystub_

‍

 _High-volume format: ADP paystub_

‍

 _Longtail formats: Generic paystub handled by LLM methods_

  
By the end, you'll understand several [SenseML ](https://docs.sensible.so/docs/senseml-reference-introduction)methods, you’ll understand strategies for extracting data from major vendors’ documents versus the long tail, and you'll be on your way to extracting any data you choose using our documentation or our prebuilt open-source configurations.

‍

## **‍** Prerequisites

‍

To follow along, you can sign up for a Sensible account, then import paystub PDFs and prebuilt open-source configurations directly to the Sensible app using the [ Out-of-the-box extractions](https://docs.sensible.so/docs/library-quickstart) tutorial.

‍
