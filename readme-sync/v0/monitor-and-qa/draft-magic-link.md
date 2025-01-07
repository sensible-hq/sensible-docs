---
title: "implement magic links for human review"
hidden: true
---

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

6. give your reviewer the URL. They should be able to edit and review the extraction using the link without logging in. For example, in incognito mode:

   ![Click to enlarge](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/images/final/human_review_magic_link.png) 