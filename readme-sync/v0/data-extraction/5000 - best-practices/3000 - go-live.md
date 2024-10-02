---
title: "Go-live checklist"
hidden: false

---

You've written your configs and tested your reference documents and you're ready to move to production. Here's a handy checklist before you go live:

- [ ] Have you published the latest version of all your configurations across all document types to [production](https://docs.sensible.so/docs/test-before-integrating-configs)? (In the Sensible app, select a document type, select a config, then click **Publish configuration** and select **Production**).
- [ ] If you're working with multiple configurations per document type, is the variable naming consistent across different configurations? (for example, if you extract a field with the ID `customer_full_name` in one config, you shouldn't name it `customer_fullname` in another config).
- [ ] In your code, have you handled the case where a field in the response object can be null?
- [ ] Does your system properly handle an error response from the Sensible API or SDKs? 
- [ ] Do you have logging around which API calls triggered an error response so that you can retry those documents? 

