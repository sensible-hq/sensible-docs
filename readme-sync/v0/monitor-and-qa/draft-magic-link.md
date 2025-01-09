---
title: "Human review configuration"
hidden: true
---

If extractions contain errors, for example as the result of hard-to-read handwriting, you can flag extractions for manual correction by a human reviewer. Flag extractions automatically at scale in production by configuring flagging rules based on [validations](doc:validate-extractions) and [extraction coverage](doc:coverage) and by using webhooks to assign reviews.

## Review lifecycle

The following diagram shows how to integrate human-in-the-loop review into your application: 

![Click to enlarge](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/images/final/human_review_5.png)

1. **Configure review triggers**: Configure extraction quality validation for a document type, for example, tax documents or pay stubs. Any extraction that doesn’t meet your quality validations triggers a human review.
2. **Specify a webhook for each document extraction:** When extracting data from a document using Sensible’s API or SDK, specify a webhook destination URL that receives updates to the extraction’s review status. 
3. **Notify a reviewer**: When the webhook indicates that a completed extraction needs review and correction, notify a reviewer and send them a link to the review interface that they can following without having to log into Sensible.
4. **Ingest corrected extractions**: When the webhook indicates that a reviewer approved an extraction, ingest the document data into your system.



## Configure flagging

In a document type, in the **Human Review** tab, set the criteria for Sensible to flag an extraction for manual review:

![Click to enlarge](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/images/final/human_review_1.png) 

Enable human review for all documents in a type, or set criteria to trigger review. Criteria include:

- [Extraction coverage](doc:coverage)

- [Validation](doc:validate-extractions) errors and warnings, if configured. Select all errors, all warnings, or individual validations. 

  



## Review status

You can check review status for past extractions in one of the following ways:

- **Sensible API/SDK**: If you enable human review for a document type, then set a [webhook](doc:api-tutorial-webhook) for each extraction request in the document type. Sensible pushes the extraction, including any manual corrections the reviewer made and the review status, to the specified webhook when a reviewer approves or rejects an extraction.  You can also filter by extraction status by specifying the `review_statuses` parameter on the [List extractions](reference:list-extractions) endpoint.

- **Sensible app**: Filter past extractions by review status. In the **Extraction history** tab, use the **Review Status** criterion.







To implement sending document extractions for review without requiring reviewers to have a Sensible account or log in, take the following steps:

1. enable human review in their doctype configs (TODO link)

2. Run an extraction that needs reviewing per your criteria (TODO link)

3. identifying you want to assign the review task to somebody (this is totally on the customer side) TODO flesh out theses steps, e.g.: 

   1. use an API endpoint or **webhook** to see what needs review + get the extraction IDs
   2. assign it to someone eg associate an ID to an email for instance

4. Request a new token for that extraction with the following POST. say the extraction ID is `b84bd1c8-113e-4e1e-8462-379f0dde2abf&sd`: (TODO: add /account/auth_tokens to postman + API ref)

   

   ```curl
   curl --location 'https://api.sensible.so/dev/account/auth_tokens' \
   --header 'Content-Type: application/json' \
   --header 'Authorization: BEARER YOUR_API_KEY' \
   --data '{
       "grants": [
           {
               "route": "/documents/{id}",
               "method": "GET",
               "path": {
                   "id": "b84bd1c8-113e-4e1e-8462-379f0dde2abf"
               }
           },
           {
               "route": "/extractions/{id}",
               "method": "PUT",
               "path": {
                   "id": "b84bd1c8-113e-4e1e-8462-379f0dde2abf"
               }
           }
       ],
       "expires": "2025-01-15T22:14:35.720Z"
   }
   
   
   '
   ```

   You'll get back a response like:

   ```json
   {
       "token": "870b8162-c6af-47e3-99c6-61311eaf98e0:9e6432c5-b342-4971-9af7-046f7cd60070",
       "created": "2025-01-07T18:59:57.844Z",
       "expires": "2025-01-15T22:14:35.720Z",
       "grants": [
           {
               "route": "/documents/{id}",
               "method": "GET",
               "path": {
                   "id": "b84bd1c8-113e-4e1e-8462-379f0dde2abf"
               }
           },
           {
               "route": "/extractions/{id}",
               "method": "PUT",
               "path": {
                   "id": "b84bd1c8-113e-4e1e-8462-379f0dde2abf"
               }
           }
       ],
       "usage": []
   }
   ```

   

5. create the URL with data from the response to the previous request as follows:

   ```https://dev.sensible.so/human-review/embedded/?token=870b8162-c6af-47e3-99c6-61311eaf98e0:9e6432c5-b342-4971-9af7-046f7cd60070&extraction=b84bd1c8-113e-4e1e-8462-379f0dde2abf ```

6. give your reviewer the URL. They should be able to edit and review the extraction using the link without logging in. For example, in incognito mode, you can edit and approve or reject the extraction:

   ![Click to enlarge](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/images/final/human_review_magic_link.png) 