---
title: "Email rough draft"
hidden: true
---

Extract from email bodies and attachments by emailing them to Sensible.

The following image shows an overview for the email extraction workflow:



![Click to enlarge](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/images/final/email.png)

How to set up email integration: TODO: probably easier with a fictional example and screenshots in Gmail. TODO: should the fictional example include a couple attachments of different doc types?

1. Create a document type (link to instructions) for the emails you want to extract from.
2. In the document type, create a dedicated email address for receiving the emails to extract from, i.e.,  `UUID@forwarding.sensible.so`.
3. Use filtering rules in your email provider to filter the emails you want to extract from that match the document type you created.    For example, filter emails from a certain domain or those containing specific keywords or specific attachment types.
4. Set up automatic forwarding with your email service provider to send your filtered emails to Sensible.



## Notes

- TODO:  "We need to be transparent and clear with the security implications of the data they’re forwarding and how it’s protected" <-- how much of this is on the docs, how much on the UI, how much on just linking to AWS infra docs??
- For email size limitations, see [Supported file formats] TODO --> link + include the info there



