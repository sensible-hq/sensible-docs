---
title: "Environments"
hidden: false
---

Before integrating existing config updates into your application, test the updates in a Development environment:

1. In the Sensible app, click **Publish configuration** and choose **Development** to save your updates to a development environment.
2. To test your updated config, specify `development` for the Environment parameter in your API, SDK, or Sensible app extraction calls.

Environment fallback behavior
----

When you  specify the development environment for an extraction, Sensible falls back to the production version for each configuration if it can't find a development version.

To understand fallback behavior in detail, imagine the document type `test_doc_type` has the following config versions, which fit a `document_a` with varying degrees of accuracy:

| Config  | Version in prod | Version in dev       |
| ------- | --------------- | -------------------- |
| configA | best fit        | bad fit              |
| configB | OK fit          | no published version |

If you specify `?environment=development` and `autoselect`, Sensible searches for a best fit across both production and development by comparing:

 -  `configA` in development (bad fit). Sensible excludes config A (best fit) since you selected `development`
 -   `configB` in production (OK fit).

Sensible returns output from  `configB`  (OK fit) in production. Notice that even though the API call specifies  the Development environment, the call returns output from a *production* config because of fallback behavior.

If you don't specify an environment, Sensible ignores development versions and compares:

- `configA` in production (best fit)
- `configB` in production (OK fit)

And returns output from `configA` (best fit) in production.

