---
title: "draft sdk code"
hidden: true
---

```
import { promises as fs } from "fs";
import { SensibleSDK } from "sensible-sdk";
import got from "got";
const apiKey = process.env.SENSIBLE_APIKEY;
const sensible = new SensibleSDK(apiKey);
const dir = process.argv[2];
const files = (await fs.readdir(dir)).filter((file) => file.match(/\.pdf$/) && file.includes('mortgage_application')); // find all bundled mortgage application files (multi-document 'portfolio' files)
const extractions = await Promise.all(
  files.map(async (filename) => {
    const path = `${dir}/${filename}`;
    return sensible.extract({
      path,
      documentTypes: ["tax_forms", "pay_stubs", "bank_statements"], //each mortgage_application file contains multiple doc types
    });
  })
);

// TODO: handle the returned extractions. Each portfolio returns multiple Excel files, 1 for each sub-document
// what would be the nicest way to save each file?  IE could we combine all the 'bank statements' across all portfolio extractions into 1 file, etc for all the tax forms and pay stubs?
// or do we want to show something completely different like sending the info to an Airtable?
```



## Example: Extract from multi-document file and output Excel files
