---
title: "Field extraction order"
hidden: true
---

**Note:** If you're familiar with Sensible, this advanced topic is for you. 

Default field extraction order
----


 Sensible adds each field to the output array sequentially after extracting it. By default you can specify fields, computed fields, and sections as sibling arrays, like this:

```
{
 "fields": [],
 "computed_fields": [],
 "sections": []
}
```

In which case Sensible extracts by default in the following order: 

1. Run fields array.
2. Run computed fields, which transform fields output.
3. Run sections (“documents inside documents”). Cordons off a document range and extract fields or computed fields from it independently. Suited to complex repeating data.

4. Return all fields, computed fields, and sections

Configurable extraction order
----


You can use the following alternative syntax to change the order in which to extract fields:

```json
{
    "fields": 
    [
        /* include all fields, computed fields, and sections in one array. Add "type": "sections" to section group field IDs,
           otherwise syntax is unchanged. */
    ]
    
}
```

This syntax alternative allows you to change execution order. For example if you specify:



````json
{
    "fields": 
    [
       {/* sections_ID_1 */},
       {/* sections_ID_2 */},
       {/* zip_computed_field_ID that uses first two sections as sources */}, 
       {/* suppressOutput_computed_field_ that suppresses first two source sections for cleaner outpu */} 
    ]
    
}
````



 With the default execution order, the previous syntax would fail, because the computed fields would execute before the sections, so the first two sections would be suppressed from the output and the zipped computed field would return null.  QUESTION TODO: so if you specified a computed field BEFORE its source fields in the fields array, that would fail too right?  For an example of using this behavior, see TODO LINK sections-example-zip.

