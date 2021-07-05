---
title: "Domain validation introduction"
hidden: true
---

 

Quality control your data extractions by writing document-specific tests in  [json logic](https://jsonlogic.com/). For example:

```
validations: [
    {
      description: "Rate must be a round number",
      condition: { "==": [{ "%": [{ var: "rate.value" }, 100] }, 0] },
      severity: "warning",
    },
    {
      description: "Zip code must be valid",
      condition: {
        match: [{ var: "delivery\\.zip\\.code.0.value" }, "^[0-9]{5}$"],
      },
      severity: "error",
    },
    {
      description: "Required field rate",
      condition: { exists: [{ var: "rate" }] },
      severity: "error",
    },
    {
      description: "Required field broker_contact_name",
      condition: { exists: [{ var: "broker_contact_name" }] },
      severity: "error",
    },
    {
      description: "Required field delivery_zip_code",
      condition: { exists: [{ var: "delivery\\.zip\\.code" }] },
      severity: "error",
    },
  ],
};
```

Sensible's extractions are deterministic: a Sensible config always returns the same output for a given PDF input. In that sense, confidence intervals don't make any sense as a measure of extraction quality. Instead, use tests like the preceding to test your extraction quality, then write your own logic based on the tests, for example:

- Pass a PDF extraction automatically through your pipeline if there are no errors and only 10% of warnings tests are triggered
- Flag a PDF extraction for human review if 5% of error tests are triggered



