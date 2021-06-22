---
title: "API tutorial"
hidden: false
---

Let's get started with extracting structured data from PDF documents using the Sensible API! If you're new to APIs in general, this tutorial is a good starting point.

Prerequisites
====



To follow this tutorial, you'll need:

- An API key (you received this key when your Sensible account was created)
- an example config
-  [Postman](https://www.postman.com/) desktop app (or follow along with cURL in the command line)

**Prerequisite: Create an example config**

1. You need an example config and doc type. If you haven't already done so, follow the steps in [Create a config](doc:quickstart#section-create-the-config) to create an example `anyco` config in an example  `auto_insurance_quote` document type. 
2. **Important!** Remember to click **Publish** in the Sensible app to publish your config, or your requests won't work:  

![](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/images/quickstart_publish_config.png).



**Prerequisite: Download Postman**

For an easy way to run the cURL requests, download the [Postman](https://www.postman.com/) desktop app. 

 

Next steps
====

Try out the endpoints with these tutorial steps:

- [Try synchronous extraction](doc:api-tutorial-sync)
- [Try asynchronous extraction](doc:api-tutorial-async-1)
- [Try a webhook](doc:api-tutorial-webhook)
