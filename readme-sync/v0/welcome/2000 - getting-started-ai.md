---
title: "Get started with AI-powered extractions"
hidden: false
---

In this tutorial, you'll learn to extract data out of a collection of similar documents using an AI-powered visual authoring tool, Sensible Instruct. You'll use natural language to instruct Sensible about which data to extract from a set of similar documents, as if you were chatting with an AI bot. Sensible Instruct uses large-language models (LLMs) such as GPT-4 to extract your target information.

You can then save your descriptions as a "config." Publish your config as an API endpoint, and use the endpoint to automate extracting from similar documents.  

Note that you can mix and match SenseML methods with Sensible Instruct methods. SenseML is a a JSON-formatted, layout-based query language, and Sensible Instruct is an AI-powered subset of SenseML that you can author in the app, no JSON required. Use SenseML for advanced document extraction, for example, for complex document layouts. For simpler document extraction, author AI-powered extraction configurations using Sensible Instruct. 

Use this tutorial if you want a guided tour of configuring AI-powered document extractions in the Sensible app. Or see the following links:

- For more information about SenseML versus Sensible Instruct, see [Choosing extraction strategy](doc:author). For authoring in SenseML, see [Get started extracting with SenseML](doc:getting-started).
- If you instead want to explore without much explanation, then [sign up](https://app.sensible.so/register) for an account and check out our interactive in-app tutorials:  TODO these links if possible.

Get structured data from an auto insurance quote
===

Let's get started with Sensible Instruct!

If you can chat with an AI bot, then you can configure document extractions. 

 In this tutorial, you'll:





- *[Write a collection of queries ( a "config")](doc:getting-started#create-a-config) to [extract structured data](doc:getting-started#extract-data) from an example auto insurance PDF* 
- *[Learn how the config works](doc:getting-started#how-it-works), including key concepts like lines, anchors, and methods*
- *[Test the config](doc:getting-started#test-the-config) by running your config against a second, similar auto insurance PDF*
- *[Use the API](doc:getting-started#integrate-with-your-application) to integrate your Sensible config with your application*
- *[Validate extractions in production](doc:getting-started#validate-extractions-in-production) by using JsonLogic to define expected extracted values and flag unexpected values as warnings or errors*

Get an account
====

1. Get an account at [sensible.so](https://app.sensible.so/register).  If you don't have an account, you can still read along to get a rough idea of how things work.

2. Log into the [Sensible app](https://app.sensible.so/signin/).

Configure the extraction
====





Publish the extraction
===

blah

TODO: explain that this is now an API ENDPOINT
===

blah



 