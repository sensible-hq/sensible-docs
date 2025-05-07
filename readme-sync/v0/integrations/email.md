---
title: "Email rough draft"
hidden: true
---



# See readme dash v5





*You can extract data from email bodies and attachments by emailing them to Sensible.*

*The following image shows an overview for the email extraction workflow:*



```
graph TD;
    A[User receives email] --> B[User sends email to Sensible]
    B --> C[Email is classified into an email type]
    C -->|If there are attachments| D[Documents classified and extracted]
    C --> E[Email is extracted]
    D --> F[Extracted data is sent and appears in the extractions history]
    E --> F
```







*![Click to enlarge](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/images/final/email.png)*

*How to set up email integration: TODO: probably easier with a fictional example and screenshots in Gmail. TODO: should the fictional example include a couple attachments of different doc types?*

1. *Create a document type (link to instructions) for the emails you want to extract from.*
2. *In the document type, create a dedicated email address for receiving the emails to extract from, i.e.,  `UUID@forwarding.sensible.so`.*
3. *Use filtering rules in your email provider to filter the emails you want to extract from that match the document type you created.    For example, filter emails from a certain domain or those containing specific keywords or specific attachment types.*
4. *Set up automatic forwarding with your email service provider to send your filtered emails to Sensible.*

## *Configuring attachment extractions*

*Not all attachments in an email will need to be extracted. To prevent triggering an extraction on irrelevant documents, we should allow users to configure the criteria for documents that need to be extracted. These filters should include:*

- *Classification score slider (ex. if the highest score returned is <x, don’t extract the document)*
- *File name (ex. only extract files that contain “1040” in the title)*
- *File types (ex. only extract PDFs)*



## *Notes*

- *TODO:  "We need to be transparent and clear with the security implications of the data they’re forwarding and how it’s protected" <-- how much of this is on the docs, how much on the UI, how much on just linking to AWS infra docs??*
- *For email size limitations, see [Supported file formats] TODO --> link + include the info there*



