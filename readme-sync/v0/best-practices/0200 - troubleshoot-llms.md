---
title: "Troubleshooting LLM extractions"
hidden: false
---

See the following tips for troubleshooting situations in which large language model (LLM)-based extraction methods return inaccurate responses, nulls, or errors.

### Fix error messages

**Error message**

```
ConfigurationError: LLM response format is invalid
```

**Notes**

Reword the description in simpler terms, and refrain from including the word "return" in your prompts, if possible. Or, add a fallback query to bypass the error if the original query is working for some documents and you're only seeing the error intermittently. See the following section for more information.

Background: Sensible returns this error when the LLM doesn't return its response in the JSON format that Sensible specifies in [full prompts](doc:prompt). This can occur when your `description` parameters prompt the LLM to return data in a specific format that conflicts with the expected JSON format.

### Interpret confidence signals

Confidence signals are an alternative to confidence scores and to error messages. For information about troubleshooting LLM confidence signals, such as `multiple_possible_answers` or `answer_maybe_be_incomplete`, see [Qualifying LLM accuracy](doc:confidence).

### Create fallbacks for null responses

Sometimes an LLM prompt works for the majority of documents in a document type, but returns null for a minority of documents. Rather than rewrite the prompt, create fallbacks targeted at the failing documents.

For example, you parse automotive repair invoices.  For most auto shops' invoices, the prompt `part code` extracts a part number listed in the repairs. For Andy & Son's car shop's invoices, this prompt returns null and you instead need the prompt  `alphanumeric code associated with the part`. To create a fallback field for Andy & Son's shop, create two fields with the same ID:

```json
{
  "fields": [
    /*
    fallback fields in query groups must be defined in
    separate groups, so define two single-member groups
     */
    {
      /* if Sensible doesn't find the anchor text 
          "Andy & Son's" in the invoice,
           it returns null for the part_number field in this group
           and falls back to the part_number in the next group.
           Use this fallback behavior to create a detailed prompt for 
           Andy & Son's invoices and more general prompt
           for all other invoices*/
      "anchor": "Andy & Son's",
      "method": {
        "id": "queryGroup",
        "queries": [
          {
            "id": "part_number",
            "description": "alphanumeric code associated with the part",
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
            part_number field returns null */
            "id": "part_number",
            "description": "part number",
            "type": "string"
          }
        ]
      }
    }
  ]
}
```

Fallback fields can be of any kind. For example, you can fallback from an LLM-based field to a layout-based field, or from a computed field to a section group.

### Locate source text

Locating the source text, or [context](doc:prompt#notes), for an LLM's answer can help you determine if the LLM is misinterpreting the correct text, or targeting the wrong text.

To view the source text for an LLM's answer:

- You can view the source text for an LLM's answer highlighted in the document for the Query Group method. In the Sensible Instruct editor, click the **Location** button in the output of a query field to view its source text in the document. For more information about how location highlighting works and its limitations, see [Location highlighting](doc:query-group#notes).

  ![Click to enlarge](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/images/final/location.png)

- To troubleshoot locating a group's context in the document, ensure that the Page Hinting parameter is enabled, then add location information to a prompt in a group. For more information about the Page Hinting parameter, see [Advanced prompt configuration](doc:prompt).

  **Location relative to page number and position on page**

  - "address in the **top left of the first page** of the document"

  - "What is the medical paid value on the **last claim of the second page**?"

  - "consumer electronics device with highest sales mentioned **near end of document**"

    **Location relative to content in document**

  - "total amount **in the expense table**"

  - "phone number after **section 2**"
