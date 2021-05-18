---
title: "Field"
hidden: true
---





Here's a top-level view of a config that has 1 field (i.e. 1 query):

```json
{
    
  "fields": [
    {
      "id": "name_of_output_key",
      "anchor": "some text to match. You can have multiple text matchers",
      "method": {
        "id": "label",
         "position": "below"
      }
    },
  ]
}
		
```

Field parameters
----


Top-level components for a Field object are as follows:

| Parameter             | Value                                                        | Description                                                  |
| --------------------- | ------------------------------------------------------------ | ------------------------------------------------------------ |
| id (**required**)     | string                                                       | The ID is the name of the field, which SenseML uses as a key in the structured output. |
| anchor (**required**) | object                                                       | The anchor identifies one or more lines of *text* in the document where we start method execution. Can be a string, [Match object](https://docs.sensible.so/docs/matcher) or array of [Match objects](https://docs.sensible.so/docs/matcher) |
| method (**required**) | object                                                       | The method describes how we want to expand from that anchor and grab your target data. |
| type                  | `accountingCurrency`, `address`, `boolean`, `currency`, `date`, `distance`, `images`, `name`, `number`, `paragraph`, `percentage`, `string`, `table`, `weight` | The type of data we're looking for, which is also specified in the structured output |
| match                 | `first`,`last`,`all`                                         | If there are multiple matches for the anchor, which to use.  **todo: verify** |



Example
----
TODO: show a field example that uses all the top-level parameters