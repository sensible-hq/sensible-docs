---
title: "API tutorial"
hidden: false
---

Get started with extracting structured data from PDF documents using the Sensible API.

If you're new to APIs in general, this tutorial is a good starting point. Or, if you're familiar with APIs, see the [quickstart](doc:quickstart) to get a sample API response.

Prerequisites
====

To follow this tutorial, you need:

- An API key (you receive this key when you sign up for a [Sensible account](https://app.sensible.so/register)) 
-  [Postman](https://www.postman.com/) desktop app (or follow along with cURL in the command line)
-  An example config. See the following section.

**Prerequisite: Create an example config**

1. Follow the steps in [Create a config](doc:quickstart#create-the-config) to create an example `anyco` config in an example  `auto_insurance_quote` document type. 
2. **Important!** Remember to click **Publish** in the Sensible app to publish your config. The API calls in these tutorials fail without the published example config.

![Click to enlarge](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/images/final/quickstart_publish_config.png).

 

Next steps
====

Try out the endpoints with these tutorials:

- [Try synchronous extraction](doc:api-tutorial-sync)
- [Try asynchronous extraction](doc:api-tutorial-async-1)
- [Try a webhook](doc:api-tutorial-webhook)
