---
title: "Quality control extractions"
hidden: true
---

TODO: update the 'quality control' link in the GSGs to here

You have the following options for quality control of your extracted document data:

|                         |                          | notes                                                        |
| ----------------------- | ------------------------ | ------------------------------------------------------------ |
| Custom validation logic | doc:validate-extractions | throw errors and warnings based on your own custom rules, for example, use a regex expression to throw a`zip code is invalid` error  for a field `customer_zip_code` |
| Monitor in real time    | doc:metrics              | Real-time dashboard in the Sensible app. Track all your document extraction metrics in one place, in real time. Aggregate performance summaries, monitor configuration success, track usage at the document type level, and view historic performance data for all production deployments. |
| Human review            |                          | humans in the loop                                           |

