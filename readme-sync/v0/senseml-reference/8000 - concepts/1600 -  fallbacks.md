---
title: "Fallback fields"
hidden: false
---

Use fallback fields to handle [document variations](doc:document-variations) in a document type. If a field fails to extract data, you can specify a backup, or fallback field to extract the same data using a different method. To specify fallbacks between fields, specify consecutive fields that use the same ID. 

Fallbacks enable you to use a single config to extract data from similar documents whose formatting can vary. For example, say you want to extract a "total amount" field which appears in a table in document revision A and in a free-text paragraph in document revision B. You can define two fields in one configuration with the same ID (`total_amount`), which use the Row method and the Query Group method, respectively. 

A field evaluates as "failed" and falls back if it returns an empty array, null, or undefined. A field evaluates to "passed" and doesn't fall back if it returns an empty string or 0. Fallback fields can be of any kind. For example, you can fallback from a field, to a computed field, to a section group.<br/>

**Limitations:**

- Fallbacks don't work across nested objects. For example, you can't fall back from a parent section group's field to a child section group's field. Fallbacks work across nested [Conditional](doc:conditional) methods.
- Fallbacks don't work within a Query Group method. To specify fallback fields, define each one in a separate query group.



### Example 1

If a company's explanation of benefits lists the patient name near the phrase "received for" in other cases and near the phrase "claimant" in others, you can write fallbacks like the following:

```json
{
  "fields": [
    {
      /* first look for patient name near phrase "recieved for" */
      "id": "patient_name",
      "anchor": "recieved for"
              "method": {
        "id": "label",
        "position": "right"
      }
    },
    /* if that fails, look for it in a row near the phrase "claimant" */
    {
      "id": "patient_name",
      "anchor": "claimant"
              "method": {
        "id": "row",
        "position": "right"
      }
    },
  ]
}
```


### Example 2: LLM prompt fallbacks

Sometimes a field works for the majority of documents in a document type, but returns null or an inaccurate response (a "false positive") for a minority of documents. This situation is most common with LLM-based methods. Rather than rewrite the LLM prompt, which can cause regressions, create fallbacks targeted at the failing documents. 

LLM-based field fallbacks differ from other field fallbacks, because the failing field can return a non-null false positive. To force a failing field to return null, add an anchor to the field. The field returns `null` if the text isn't present in the document. 

For example, you parse automotive repair invoices. For most auto shops' invoices, the prompt `total parts price` extracts a total price. For Andy & Son's car shop's invoices, this prompt returns `null` or it returns an inaccurate response, for example, a subtotal.  Through experimenting, you find a successful prompt:  `What is the 'total parts price'. The total parts price will be labeled 'total parts' or something semantically similar. It's not a value that can be summed from the line items on the invoice.` To create a fallback field for Andy & Son's shop, create two fields with the same ID:

```json
{
  "fields": [
    /*
       use fallbacks to create a detailed prompt for 
       Andy & Son's invoices and more general prompt
       for all other invoices
       fallback fields in query groups must be defined in
       separate groups, so define two single-member groups
     */
      
    {
      /* if Sensible doesn't find the anchor text 
          "Andy & Son's" in the invoice,
           it returns null for the parts_total_price field in this group
           and falls back to the parts_total_price in the next group.
           Use the anchor to avoid non-null false positives
           */
      "anchor": "Andy & Son's",
      "method": {
        "id": "queryGroup",
        "queries": [
          {
            "id": "parts_total_price",
            "description": "What is the 'total parts price'. The total parts price will be labeled 'total parts' or something semantically similar.  It's not a value that can be summed from the line items on the invoice",
            "type": "string"
          }
        ]
      }
    },
    {
      "method": {
        "id": "queryGroup",
        "queries": [
          {
            /* this field runs only if the previous
            parts_total_price field returns null */
            "id": "parts_total_price",
            "description": "total parts price",
            "type": "string"
          }
        ]
      }
    }
  ]
}
```

Fallback fields can be of any kind. For example, you can fallback from an LLM-based field to a layout-based field, or from a computed field to a section group. For more information, see [Field query object](doc:field-query-object).
