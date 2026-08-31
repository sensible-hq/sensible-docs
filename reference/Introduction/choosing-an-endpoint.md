---
title: API Introduction
excerpt: Overview of Sensible's API endpoints for extracting structured data from documents,
  including async/sync extraction, Excel conversion, portfolio extraction, and document
  classification.
deprecated: false
hidden: false
metadata:
  title: ''
  description: API introduction and endpoint overview
  robots: index
next:
  description: ''
---
Welcome to Sensible! If you have any questions, please reach out by chat or [support@sensible.so](mailto:support@sensible.so) and we'd be happy to help you out.

To get started, see the following endpoints for extracting structured data from documents. Or, see other [integration](doc:integrate)  options including the Sensible [SDKs](doc:sdk-guides) .

<Table align={["left","left","left"]}>
  <thead>
    <tr>
      <th>
        Endpoints
      </th>

      <th>
        Links
      </th>

      <th>
        Notes
      </th>
    </tr>
  </thead>

  <tbody>
    <tr>
      <td>
        Document extraction (asynchronous)
      </td>

      <td>
        - [Extract doc at a Sensible URL](ref:generate-an-upload-url) <br />
        - [Extract doc at your URL](ref:extract-from-url)
      </td>

      <td>
        Takes a document file, such as a PDF, and returns extracted data asynchronously. Use the asynchronous endpoints in production.  You have two options for asynchronously extracting from your document:<br /> - extract a doc at a URL you provide<br />- upload and extract the doc at a Sensible URL. <br />You can then call the [Retrieve extraction](ref:retrieving-results)  endpoint to get the results, or specify a webhook for Sensible to push the results to as soon as they're ready.<br />
      </td>
    </tr>

    <tr>
      <td>
        Document extraction (synchronous)
      </td>

      <td>
        [Extract data from a document](ref:extract-data-from-a-document)
      </td>

      <td>
        Returns extracted document data synchronously. Use this endpoint for testing.
      </td>
    </tr>

    <tr>
      <td>
        Get Excel from PDFs
      </td>

      <td>
        [Get Excel extraction](ref:get-excel-extraction)
      </td>

      <td>
        Get well-structured Excel files converted from PDF documents. This endpoint also supports documents formatted as images, for example, PNG or JPEG.
      </td>
    </tr>

    <tr>
      <td>
        Portfolio extraction (asynchronous)
      </td>

      <td>
        - [Extract portfolio at a Sensible URL](ref:generate-upload-url-portfolio) <br /> - [Extract portfolio at your URL](ref:extract-from-url-portfolio)
      </td>

      <td>
        Use these endpoints with multiple documents that are packaged into one PDF file (a PDF "portfolio").
      </td>
    </tr>

    <tr>
      <td>
        Document type classification
      </td>

      <td>
        [Classify document by type](ref:classify-document-sync)
      </td>

      <td>
        Classifies a document by its similarity to document types you define in your Sensible account.
      </td>
    </tr>
  </tbody>
</Table>

<br />