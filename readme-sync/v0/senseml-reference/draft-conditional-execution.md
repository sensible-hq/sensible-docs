---
title: "Conditional execution"
hidden: true
---

*TODOs before publish:*

- *overview/ devops platform*
- *senseml reference introduction?*



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

| key                                                          | value                                     | description                                                  |
| ------------------------------------------------------------ | ----------------------------------------- | ------------------------------------------------------------ |
| id (**required**)                                            | `conditional`                             | TBD this field type `if...then...else` conditional structure for extracting alternate lists of fields. You can nest conditional fields inside conditional fields. TODO better place to put this? |
| rule                                                         | [JsonLogic](doc:jsonlogic)                | evaluates to a boolean (true = pass, false = fail). Usually depends on evaluating extracted data from the document which determines what appropriate fields to extract. |
| fieldsOnPass 2do/todo: is 1 required but not both? either/or/and? check ... might be something to combo into 1 row if same lanugage. | array of [fields](doc:field-query-object) | Specifies fields to extract if the rule passes.              |
| fieldsOnFail                                                 |                                           | Specifies fields to extract if the rule fails. TODO note if you supress output for an invalid JsonLogic field (either through a conditioanl, or through suppress output field)  it will still show up as an error even if the fields pass -- so you can still troubleshoot it. |