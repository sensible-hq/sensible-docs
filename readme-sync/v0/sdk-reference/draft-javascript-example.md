---
title: "draft sdk code"
hidden: true
---



ideas:

- (fndkt) -- suppoose you're a fintech that connects Spotify and other webcommerce businesses to funding (**direct funder for merchant cash advances**). Your app requires the business applicant to upload 3 recent bank statements. Then you need to parse them: OR! So you're qualifying them for a loan to buy or rent solar panels. You to qualify them, you want to see their recent bank statements AND their homeowners policy dec page, among other things... 
- (mddsk) You look at registration records to verify a business
- maybe you serve real estate investors and you want 

TODO: look at this example from fndkt by H:

```
import { promises as fs } from "fs";
import { SensibleSDK } from "sensible-api";
import got from "got";
const apiKey = process.env.SENSIBLE_APIKEY;
const sensible = new SensibleSDK(apiKey);
const dir = process.argv[2];
const files = (await fs.readdir(dir)).filter((file) => file.match(/\.pdf$/));
const extractions = await Promise.all(
  files.map(async (filename) => {
    const file = await fs.readFile(`${dir}/${filename}`);
    return sensible.extract({
      file,
      documentType: "bank_statements",
    });
  })
);
await Promise.all(
  extractions.map((extraction) => sensible.waitFor(extraction))
);
const excel = await sensible.generateExcel(extractions);
console.log(excel);
const excelFile = await got(excel.url);
await fs.writeFile(`${dir}/output.xlsx`, excelFile.rawBody);
```







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
5. Consume the data.

For example:

```javascript
 a code example that looks a bunch of requests from a file directory, then compiles them into an Excel file and downloads it?
```

### Classification example

See the following steps for an overview of the SDK's workflow for classification:

1. Instantiate an SDK object (`new SensibleSDK("YOUR_API_KEY")`.

2. Request a document classification (`sensible.classify()`.  Specify the document to classify using the `file` parameter. See the Classify method for more information.

3. Consume the data.

   ```javascript
   import { promises as fs } from "fs";
   import { SensibleSDK } from "sensible-api"
   
   const sensible = new SensibleSDK(YOUR_API_KEY);
   const blob = await fs.readFile("./YOUR_DOCUMENT.pdf");
   const request = await sensible.classify({file: blob}); 
   const result = await sensible.waitFor(request);
   console.log(results);
   ```

   

See the following sections for more information about the methods in this workflow.
