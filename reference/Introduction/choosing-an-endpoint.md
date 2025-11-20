---
title: Introduction
excerpt: ''
deprecated: false
hidden: false
metadata:
  title: ''
  description: ''
  robots: noindex
next:
  description: ''
---
Welcome to Sensible! If you have any questions, please [post to our community](https://community.sensible.so/) or reach out to support@sensible.so and we'd be happy to help you out. 

Sensible provides both synchronous and asynchronous endpoints for you to extract data out of your documents: 

- The majority of our users can use our `/extract` endpoint, which takes a PDF file and returns extracted data synchronously (see "Extract data from a document" below).

- Use the asynchronous endpoints for PDFs that are greater than 4.5MB in size or that require over 30 seconds of processing time. You have two options for asynchronously processing your PDF: extract a doc at a URL you provide, our upload the doc to a Sensible URL.  You can then call the `retreive results` endpoint to get the results, or specify a webhook for Sensible to push the results to as soon as they're ready.

If you're new to APIs, then check out our [API tutorial](doc:api-tutorial) for a step-by-step guide to calling Sensible endpoints.