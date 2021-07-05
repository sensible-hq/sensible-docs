---
title: "Domain validation introduction"
hidden: true
---

 

Quality control your data extractions by writing document-specific validation tests in  [json logic](https://jsonlogic.com/).  Sensible's extractions are deterministic: a Sensible config always returns the same output for a given PDF input. Given this determinism, confidence intervals don't make any sense as a measure of extraction quality. Instead, use tests like the following example to quantify your extraction quality, then write your own logic based on the tests, for example:

- Pass a PDF extraction automatically through your pipeline if there are no errors and only 10% of warnings tests are triggered
- Flag a PDF extraction for human review if 5% of error tests are triggered

 Example validation:

```
validations: [
    {
      description: "Rate must be a round number",
      condition: { "==": [{ "%": [{ var: "rate\\.value" }, 100] }, 0] },
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

In the preceding example: 

- The "Rate must be a round number" test retrieves the value of an extracted `rate.value` key/value pair to a `var`, use the JsonLogic [modulo operation (%)](https://jsonlogic.com/operations.html#%25/) to divide the rate by 100, and pass if the remainder equals 0.
- The "Zip code must be valid" test uses a Sensible-specific operation (`match`) to test if an extracted zip code value matches the regular expression `"^[0-9]{5}$"`.
- The "Required field broker_contact_name" test uses a Sensible-specific operation (`exists`) to test if a `var`'s value is not null.

Parameters
====

| id                         | value               | notes                                                        |
| -------------------------- | ------------------- | ------------------------------------------------------------ |
| description (**required**) | string              | a description of the test                                    |
| condition                  | JsonLogic operation | Supports all [JsonLogic operations](https://jsonlogic.com/operations.html)  and extends them with the following Sensible operations:<br/> `{ match: [JsonLogic, string] }`, where `string` is a JS-flavor, JSON-escaped regular expression.<br>`{ exists: [JsonLogic] }`, most commonly used with the JsonLogic `var`  operation to test that an output value exists. |
| severity                   | `error`, `warning`  | The severity of the failing test                             |







