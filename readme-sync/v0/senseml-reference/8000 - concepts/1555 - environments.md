---
title: "Environments"
hidden: false
---

Before integrating existing config updates into your application, test the updates in a Development environment:

1. In the Sensible app, click **Publish configuration** and choose **Development** to save your updates to a development environment.
2. To test your updated config, specify `development` for the Environment parameter in your API, SDK, or Sensible app extraction calls.

## Tips for testing in development

When you test a config in the  `development` environment, your success criteria include:

1. How the new version performs when you run an extraction against it specifically.

2. How the new version [performs](doc:fingerprint) against other configs in the doc type when you run an extraction using the **Auto select** option in the Sensible app's **Extract** tab, or when using an extraction endpoint in which you omit specifying the config, for example, `/extract/{docType}?environment=development` .


For the second criterion, note the following tips:  

- While you're testing, avoid config [classification scoring](doc:fingerprint) surprises by making sure your development environment mimics your production environment. In other words, if the document type contains configs *other* than the ones you're currently testing, ensure those other configs have identical published production and development versions. Note that if you've *never* published a config to development but you have published it to production, then during extraction, Sensible falls back to the config's production version as a convenience.
-  If you publish changes to more than one config in development, then publish them all to production at the same time to avoid classification scoring surprises.  
