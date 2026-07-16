# How to extract data from employment verification forms with Sensible

##   
What we'll cover  
‍

This blog post will walk you through extracting data from two different employment verification providers: Truework and Equifax:  
‍

 _Sensible app showing queries, sample document, and extracted document field  
_

‍

We'll examine how the same information requires different extraction approaches based on each provider's document layout. Here are the example documents we’ll use with dummy data:  
  


_Truework employment verification document_

‍

 _Equifax employment verification document_

‍

By the end, you'll understand several SenseML methods and you'll be on your way to extracting any data you choose using our documentation or our prebuilt open-source configurations.

‍

## Prerequisites  
‍

To follow along, you can sign up for a Sensible account, then import example employment verification PDFs and prebuilt open-source configurations directly to the Sensible app using the [ Out-of-the-box extractions](https://docs.sensible.so/docs/library-quickstart) tutorial.

Our[ configurations for employment verification extractions](https://github.com/sensible-hq/sensible-configuration-library/tree/main/templates/Financial%20Services/Employment%20Verification) are comprehensive. To keep the example in this post simple, let's extract solely the following:  
‍

  * employee name
  * employer address
  * second-year base pay
  * And show how fingerprints identify document subtypes
