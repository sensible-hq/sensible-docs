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
                   "id": "b84bd1c8-113e-4e1e-8462-379f0dde2abf&sd"
               }
           },
           {
               "route": "/extractions/{id}",
               "method": "PUT",
               "path": {
                   "id": "b84bd1c8-113e-4e1e-8462-379f0dde2abf&sd"
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
       "token": "e84057ab-bf38-4c9a-9c7d-5a2ec24b00fc:e91e77c1-d1a3-456c-9465-07b2bc654eb0",
       "created": "2025-01-07T18:40:14.038Z",
       "expires": "2025-01-15T22:14:35.720Z",
       "grants": [
           {
               "route": "/documents/{id}",
               "method": "GET",
               "path": {
                   "id": "b84bd1c8-113e-4e1e-8462-379f0dde2abf&sd"
               }
           },
           {
               "route": "/extractions/{id}",
               "method": "PUT",
               "path": {
                   "id": "b84bd1c8-113e-4e1e-8462-379f0dde2abf&sd"
               }
           }
       ],
       "usage": []
   }
   ```

   

5. create the URL with data from the response to the previous request as follows:

   ```https://dev.sensible.so/human-review/embedded/?token=e84057ab-bf38-4c9a-9c7d-5a2ec24b00fc:e91e77c1-d1a3-456c-9465-07b2bc654eb0&extraction=b84bd1c8-113e-4e1e-8462-379f0dde2abf&sd ```

6. give your reviewer the URL. They should be able to edit and review the extraction using the link without logging in. For example:

   