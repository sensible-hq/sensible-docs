---
title: "Test before integrating configs"
hidden: true
---

Before integrating existing config updates into your application, test the updates in a Development environment:

1. In the Sensible app, click **Publish** and choose **Development** to save your updates to a development environment.
2. Add the query parameter `?environment=development` to your extraction [API calls](https://docs.sensible.so/reference) to test your updated config.

Fallback behavior
----

When you  specify `?environment=development` in an API endpoint, Sensible falls back to the production version for each configuration if it can't find a development version.

To understand fallback behavior, let's say the document type `test_doc_type` has the following config versions, which fit a `document_a` with varying degrees of accuracy:

```
configA_v1_inprod_best_fit
configA_v2_indev_bad_fit
configB_v1_inprod_ok_fit
```

If you specify `?environment=development`, Sensible searches for a best fit across both production and development by comparing:

 -  `configA_v1_inprod_best_fit` in development
 -   `configB_v1_inprod_ok_fit` in production 

And returns output from  `configB` in production. 

If you don't specify an environment, Sensible ignores development versions and compares:

- `configA` in production
- `configB` in production

And returns output from `configA` in production.

