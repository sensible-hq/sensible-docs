---
title: "draft sdk code"
hidden: true
---




## Code examples

### Extraction example

See the following steps for an overview of the SDK's workflow for extraction:

1. Instantiate an SDK object (`new SensibleSDK()`. 
2. Request a document extraction (`sensible.extract()` with the following required parameters:
   1.  **(required)** Specify the document from which to extract data using the `url` or `file` parameter. 
   2.  **(required)** Specify the user-defined document type or types using the `documentType` or `documentTypes` parameter.
   3.  See the following section for optional parameters.
3. Wait for the result (`sensible.waitFor()`. See the Wait For method for more information.
4. Optionally convert the result or results to Excel using `generateExcel()`. See the Generate Excel method for more information.
5. Consume the document data as JSON or in Excel format.

For example:

```typescript
TODO: a code example that looks a bunch of requests from a file directory, then compiles them into an Excel file and downloads it?
```

### Classification example

See the following steps for an overview of the SDK's workflow for classification:

1. Instantiate an SDK object (`new SensibleSDK("YOUR_API_KEY")`.

2. Request a document classification (`sensible.classify()`.  Specify the document to classify using the `file` parameter. See the Classify method for more information.

3. Consume the document data as JSON

   ```typescript
   import { promises as fs } from "fs";
   import { SensibleSDK } from "sensible-sdk"
   
   const sensible = new SensibleSDK(YOUR_API_KEY);
   const blob = await fs.readFile("./YOUR_DOCUMENT.pdf");
   const request = await sensible.classify({file: blob}); 
   const result = await sensible.waitFor(request);
   console.log(results);
   ```

   

See the following sections for more information about the methods in this workflow.
