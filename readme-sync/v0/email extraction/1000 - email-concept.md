---
"title": "Email data extraction"
"hidden": true
---

## Introduction

You can automatically extract structured data from email bodies and attachments by forwarding them to Sensible. Define [document types](doc:document-type-settings) in the Sensible app to handle the extractions.

The following image shows an overview of  email extraction:



![image-20250617131007756](C:\Users\franc\AppData\Roaming\Typora\typora-user-images\image-20250617131007756.png)

TODO: add image here (email_overview.png)

## Implementation overview

To implement this workflow, take the following general steps:

**Email setup**

1. Determine a set of similar emails that you want to extract from. For example, you're in PropTech and you want to extract data from lease applications sent to a property manager, *Sensible Property*. 
2. Define a Sensible forwarding email address  for the set of emails. For example, *blah*.
3. Set up your email filters so your *blah* emails automatically forward to the Sensible address.

**Data extraction configuration**

1. In the Sensible app, define [document types](doc:document-type-settings) for each email attachment in the similar emails that you want to extract from, and 1 for the email body. For example, *blah blah balh*

**Receive extracted data**

1. Define a webhook to receive the extracted data, or view the extracted data in the Sensible app



TODO: DELETE:

```
---
config:
  layout: dagre
---
flowchart TD
    A["User receives email"] --> B["User fowards email to Sensible"]
    B --> C["Classify attachments"]
    C --> D["Extract data"]
    D --> E["User gets extracted data with webhook"]
    style A fill:#fafaf8,stroke:#000,stroke-width:1px
    style B fill:#fafaf8,stroke:#000,stroke-width:1px
    style C fill:#fafaf8,stroke:#000,stroke-width:1px
    style D fill:#fafaf8,stroke:#000,stroke-width:1px

```





