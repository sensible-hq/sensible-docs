---
title: "Environments"
hidden: false
---

Before integrating existing config updates into your application, test the updates in a Development environment:

1. In the Sensible app, click **Publish configuration** and choose **Development** to save your updates to a development environment.
2. To test your updated config, specify `development` as the environment in your API, SDK, or Sensible app extraction calls.
3. Publish your config to the `production` environment when you're satisified with the changes.

## Tips for testing in development

When you test a config in the  `development` environment, consider the following questions:

1. Does the new version correctly extract your target fields you run an extraction against it specifically?

2. Does Sensible correctly auto-select the new version when [classifying](doc:fingerprint) a document against other configs in the document type?


For the second question, note the following tips to avoid config [classification](doc:fingerprint) surprises:  

- Ensure your development environment mimics your production environment. In other words, if the document type contains configs *other* than the ones you're currently testing, ensure those other configs have identical published production and development versions. Note that if you published a config to production but never published it to development, Sensible uses the config's production version to mimic the production environment.
-  If you publish changes to more than one config in development, then publish them all to production at the same time.
