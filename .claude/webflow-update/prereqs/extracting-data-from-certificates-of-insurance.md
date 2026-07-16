# Extracting data from certificates of insurance

### Introduction

In this tutorial you'll use SenseML to extract structured data from a certificate of liability insurance PDF. 

### Why extract data from an insurance certificate?

Certificates of liability insurance PDFs are everywhere — they’re generated almost any time companies want to work together in the physical world. Companies then have a burden of proving compliance. For example, a construction firm might have to prove minimum coverage requirements for their subcontractors. Often, this means an actual human has to open a PDF, read it, and verify compliance.

But what if you could skip the human step and extract the compliance information automatically from the PDF? Enter Sensible.

### What's SenseML?

SenseML**** is Sensible’s JSON-formatted query language for extracting information from PDFs. SenseML is powered by a mix of techniques, including machine learning, heuristics, and rules. If you can write basic SQL queries, you can write SenseML queries!

### What we'll cover

At Sensible, we provide our customers with customizable SenseML queries to extract data from insurance certificates and other documents. In this post, you’ll learn to write your own "configs" (SenseML queries) for your own documents, as well as modify any configs we provide you with.

### Prerequisites

  * You’ll need an account for[ Sensible](https://www.sensible.so/get-early-access).  Or, read along for a rough idea of how things work.
  * You’ll need to download an [**example insurance certificate PDF**](https://github.com/sensible-hq/sensible-docs/raw/main/readme-sync/assets/v0/pdfs/acord_25_test.pdf)**.**



The example insurance certificate is sparsely populated with some placeholder data:

Example insurance certificate

‍
