---
title: "dashboard"
hidden: true
---







![Click to enlarge](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/images/final/dashboard_count.png)



![Click to enlarge](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/images/final/dashboard_coverage.png)



![Click to enlarge](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/images/final/dashboard_coverage.png)





TODO - start adding screenshots and explaining (+ understanding) dashboard

Quality statistics (separate topic?)
---

You can get individual and aggregate statistics about the quality of extractions.

**Quality buckets**

You can filter extractions by the following 12 “buckets” of aggregated extraction quality scores.  For example, the following image shows that 15 document extractions scored 100% quality scores in a given time range for a given config, and 7 fell into the lowest 0-10% quality bucket.



THIS STUFF IS ALREADY IN THE API:

- [0, 10)

- [10, 20)

- [20, 30)

- [30, 40)

- [40, 50)

- [50, 60)

- [60, 70)

- [70, 80)

- [80, 90)

- [90, 95)

- [95, 100)

- [100] 

  `[` denotes inclusive and `)` denotes exclusive

For example, a document extraction with a quality score of .85, or 85%, falls into the  [80, 90) bucket.

You can view scores in the Sensible app or through the Sensible API. 

