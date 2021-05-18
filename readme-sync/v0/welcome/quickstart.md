---
title: "Quickstart"
hidden: true
---



DRAFT: UNPUBLISHED
-----


this is a draft version that is not yet included in the table of contents.

Try out the demo
-----


To get a quick demo of how SenseML works:

1. Get an account
2. Check out the playground at  https://dev.sensible.so/editor/?d=senseml_basics&c=senseml_basics&g=new_basics (TODO: need the proper link).

It looks like this:

![image-20210518110114583](C:\Users\franc\AppData\Roaming\Typora\typora-user-images\image-20210518110114583.png)

Make your first config: auto insurance quote example
----

1. Login to your account

2. Click 'create document type' and label it 'auto_insurance_quote'

3. Upload the following document as a 'golden':  (TODO: store in github n make second doc:  https://docs.google.com/document/d/11S7hiNEPqgpAxbXxjpOapPTJxJGcG8n53i7AZdkydak/edit

4. Click 'make config' and label it 'anyco' (for the fictional compnay generating the qutoe).

5. Click the config.

6. Let's say we just want a few pieces of info: x,zy,

7. paste in this config:

8. ```json
   {
     "fields": [
       {
         "id": "policy_number",
         "anchor": {
           "match": [
             {
               "text": "Policy number:",
               "type": "startsWith"
             }
           ]
         },
         "method": {
           "id": "label",
           "position": "right"
         }
       },
       {
         "id": "comprehensive_premium",
         "anchor": "comprehensive",
         "type": "currency",
         "method": {
           "id": "row",
           "tiebreaker": "second"
         }
       },
     ]
   }
   ```

   ANd you'll get:

   ```json
   {
     "policy_number": {
       "type": "string",
       "value": "123456789"
     },
     "comprehensive_premium": {
       "source": "$150",
       "value": 150,
       "unit": "$",
       "type": "currency"
     }
   }
   ```

   

And it will look like this;

![image-20210518122640189](C:\Users\franc\AppData\Roaming\Typora\typora-user-images\image-20210518122640189.png)

Let's talk about how this works:





TODO:

- talk about Integrating w/ your app (API calls + how you'd use the above app stuff to test out configs before doing the API calls...also talk about seeing your extraction run history in the app (sort alike logging?)