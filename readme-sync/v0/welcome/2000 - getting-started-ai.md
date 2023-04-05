---
title: "Getting started with AI-powered extractions"
hidden: false
---

In this tutorial, you'll learn to extract data out of a collection of similar documents using an AI-powered visual authoring tool, Sensible Instruct. You'll use natural language to instruct Sensible about which data to extract from an example document, as if you were chatting with an AI bot. Sensible uses large-language models (LLMs) such as GPT-4 to extract your target information.

You can then save your descriptions as an extraction configuration, or "config." Publish your config to automate extracting from similar documents.  

Use this tutorial if you want a guided tour of configuring AI-powered document extractions in the Sensible app. Or see the following links:

- You can mix and match Sensible Instruct methods with SenseML methods for advanced config authoring.  For more information about SenseML versus Sensible Instruct, see [Choosing extraction strategy](doc:author). For authoring in SenseML, see [Get started extracting with SenseML](doc:getting-started).
- If you instead want to explore without much explanation, then [sign up](https://app.sensible.so/register) for an account and check out our interactive in-app example extractions. For links to the examples, see [AI-powered resources](doc:no-code).

Get structured data from an auto insurance quote
===

Let's get started with Sensible Instruct! Sensible Instruct makes it easy to specify in the data you want to extract from documents. If you can chat with an AI bot, then you can configure document extractions. 

 In this tutorial, you'll:

- Edit a collection of descriptions ("a config") about the data you want to extract from an example PDF
- Test the config against a second, similar PDF
- Download the extracted document data as an Excel sheet. 

Get an account
====

1. Get an account at [sensible.so](https://app.sensible.so/register).  If you don't have an account, you can still read along to get a rough idea of how things work.

2. Log into the [Sensible app](https://app.sensible.so/signin/).

Configure the extraction
====

1. To view an example bank statement PDF extraction, navigate to [https://app.sensible.so/editor/instruct?d=sensible_instruct_basics&c=bank&g=bank](https://app.sensible.so/editor/instruct?d=sensible_instruct_basics&c=bank&g=bank). 

   You'll see a 'config', or list of instructions for extracting from the example menu document (in the left pane), and extracted data in the right pane.

   ![Click to enlarge](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/images/final/quickstart_instruct_1.png)
   
   

2. Take the following steps to edit the config to extract more data from the document.

3. To extract a single data point from the document, click **Query**.

![Click to enlarge](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/images/final/quickstart_instruct_2.png)

  - Edit the query as shown in the following screenshot and click the Send icon:

![Click to enlarge](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/images/final/quickstart_instruct_3.png)

- You should see the extracted account number, `8347-3248`, populate in the **Extracted data** section.

Click **back to fields**

Your new extracted info is at the bottom of the list of extracted info:

![image-20230330145558000](C:\Users\franc\AppData\Roaming\Typora\typora-user-images\image-20230330145558000.png)

Click Publish to save your config as an API endpoint you can use with the API or with the Sensible app.







Test the config against another document
===

1. Navigate to https://dev.sensible.so/editor/instruct/?d=frances_test_playground&c=instruct_gsg&g=copy_of_bank_statement___google_docs&v= to see the config you just edited, tested against a new document in the left pane. You should see that the extracted information has changed for your query:

   TODO: the query that the person authors should change.
   
   ![image-20230330150725410](C:\Users\franc\AppData\Roaming\Typora\typora-user-images\image-20230330150725410.png)


Extract more complex information
===

So far you've just extracted simple facts. Now try extracting a list:

![image-20230330151211148](C:\Users\franc\AppData\Roaming\Typora\typora-user-images\image-20230330151211148.png)





Fill it out as follows:

![image-20230330151646972](C:\Users\franc\AppData\Roaming\Typora\typora-user-images\image-20230330151646972.png)



At the bottom of teh right pane you should see the extracted data: TODO: make sure the field ids don't quite match up to the document

![image-20230330151712459](C:\Users\franc\AppData\Roaming\Typora\typora-user-images\image-20230330151712459.png)



Now, check that your List field works with another document at this link: 

https://dev.sensible.so/editor/instruct/?d=frances_test_playground&c=instruct_gsg&g=bank_statement___google_docs&v=

It should look like this:

![image-20230330151905174](C:\Users\franc\AppData\Roaming\Typora\typora-user-images\image-20230330151905174.png)



Publish the extraction
===

Publish your updated extraction:

![image-20230330152018117](C:\Users\franc\AppData\Roaming\Typora\typora-user-images\image-20230330152018117.png)

(optional) Download the extracted info as excel in the quick Extract pane
===

You've tested your extraction configuration.

Now you can download your extracted data as Excel. You'll get 1 Excel file per document (to combine extractions from multiple documents, use the Sensible API).

Navigate to the [quick extraction tab] at  https://dev.sensible.so/quick-extraction/.



![image-20230330152147986](C:\Users\franc\AppData\Roaming\Typora\typora-user-images\image-20230330152147986.png)



Select your document type, "TBD/TDO". (how to explain about doc types?)



Download this a new document, this one:

| TBD TODO | [Download link](https://github.com/sensible-hq/sensible-docs/blob/main/readme-sync/assets/v0/pdfs/tbd_todo.pdf) |
| -------- | ------------------------------------------------------------ |

Upload it to the quick extract pane:

![image-20230330152355006](C:\Users\franc\AppData\Roaming\Typora\typora-user-images\image-20230330152355006.png)

Run the extraction using the collection of descriptions you just edited, or the "config" (TBD name of config):

You should see JSON results:



![image-20230330152513267](C:\Users\franc\AppData\Roaming\Typora\typora-user-images\image-20230330152513267.png)

Click Download Excel to see the Excel results:



![image-20230330152607384](C:\Users\franc\AppData\Roaming\Typora\typora-user-images\image-20230330152607384.png)



TODO: explain that this is now an API ENDPOINT
===

blah



 