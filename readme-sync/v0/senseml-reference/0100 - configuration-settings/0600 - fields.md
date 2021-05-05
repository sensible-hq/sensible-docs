---
title: "Fields"
slug: "fields"
hidden: false
createdAt: "2021-03-22T21:58:46.408Z"
updatedAt: "2021-04-06T16:33:22.568Z"
---
[block:parameters]
{
  "data": {
    "h-0": "key",
    "h-1": "value",
    "h-2": "description",
    "0-0": "id",
    "0-2": "A string that identifies the field in the `parsed_document` output from the API",
    "0-1": "string",
    "1-0": "type",
    "1-2": "optional, default: `string`\nA built in Sensible type",
    "1-1": "`address`, `boolean`, `currency`, `distance`, `name`, `paragraph`, `string`, `weight`",
    "2-0": "match",
    "2-2": "optional, default: `first`\n- `first`: Return the first matched value (that passes eduction) in anchor order\n- `all`: Return an array of values, one per matched anchor",
    "2-1": "`first`, `all`",
    "3-0": "method",
    "3-1": "[Methods](ref:methods)",
    "3-2": "The method to use to extract the field from the document",
    "4-0": "anchor",
    "4-1": "[AnchorComponent](ref:anchorcomponent)",
    "4-2": "A string or object that determines the global positions in the document where the engine will attempt to extract data using the above methods"
  },
  "cols": 3,
  "rows": 5
}
[/block]
Types
- `address`: Matches PO boxes and street addresses that start with a number represented in digits
- `boolean`: Matches Yes/No, Y/N, and True/False
- `currency`: Currently supports currencies in dollars. 
- `date`: Dates of the format MM/DD/YYYY and variants, or month name DD, YYYY and variants
- `distance`: Currently supports miles and kilometers
- `images`: Image metadata (can only be used with [Document Range](ref:documentrange))
- `name`: Names of the formats below and variants
                - First Last
                - First1 Last1 and First2 Last2
                - Last, First1 and First2
                - First1 and First2 Last
- `paragraph`: A string with newlines at paragraph breaks (to be used with [Document Range](ref:documentrange) only)
- `string`
- `weight`: Currently supports pounds and kilograms

Anchor
- If `anchor` is a string, the engine will transform it into `{ match: { text: "THE_STRING", type: "includes" } }` — a standard includes matcher with no start or end
- `start` (optional, defaults to the first line in the document)
    - An [AnchorComponent](ref:anchorcomponent)  that sets the inclusive start point in the document for matches
- `match`
    - An [AnchorComponent](ref:anchorcomponent)  that specifies the match criteria for the field
    - The engine passes an array of all the lines that match the criteria to extraction method (and by default the method will return the first non-empty result, see `match` above)
- `end` (optional, defaults to no endpoint)
    - An [AnchorComponent](ref:anchorcomponent)  that sets the exclusive endpoint in the document for matches
    - `includesEnd` (optional, defaults to false): If true the endpoint is inclusive rather than exclusive