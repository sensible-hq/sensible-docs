---
title: "Conditional execution"
hidden: true
---

TODOs before publish:

- overview/ devops platform
- senseml reference introduction?



Extracts alternate sets of fields based on whether a [JsonLogic](doc:jsonlogic) rules passes or fails. TODO: example use cases. (frm real life)

TODO: simple example here w screenshot??

```json
id: conditional
rule: if 
fieldsOnPass:
fieldsOnFail:
```



## Parameters

TODO: look at Query Group parameters and see how they compare

### METHOD PARAMETERS (how to describe that?)

| key               | value                                     | description                                                  |
| ----------------- | ----------------------------------------- | ------------------------------------------------------------ |
| id (**required**) | `conditional`                             | TBD this field type `if...then...else` conditional structure for extracting alternate lists of fields. |
| rule              | [JsonLogic](doc:JsonLogic)                | evaluates to a boolean (true = pass, false = fail). Usually depends on evaluating extracted data from the document which determines what appropriate fields to extract. |
| fieldsOnPass      | array of [fields](doc:field-query-object) | Specifies fields to extract if the rule passes.              |
| fieldsOnFail      |                                           | Specifies fields to extract if the rule fails.               |