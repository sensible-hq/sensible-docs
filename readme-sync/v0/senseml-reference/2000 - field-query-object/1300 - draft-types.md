---
title: "Types"
hidden: true
---
Filter and format extracted data using the Type parameter in a [Field object](doc:field-query-object). 

For example, the following field returns null unless it finds data that Sensible recognizes as a number: 

```json
{
  "fields": [
    {
      "id": "typed_field",
      "type": "number",
      "anchor": "duration in years:",
      "method": {
        "id": "label",
        "position": "right"
      }
    },
  ]
}
```

The following types are available:

[Accounting Currency](doc:types#accounting-currency)
[Address](doc:types#address)
[Boolean](doc:types#boolean)
[Currency](doc:types#currency)
[Custom](doc:types#custom)
[Date](doc:types#date)
[Distance](doc:types#distance)
[Images](doc:types#images)
[Name](doc:types#name)
[Number](doc:types#number)
[Paragraph](doc:types#paragraph)
[Percentage](doc:types#percentage)
[Period Delimited Currency](doc:types#period-delimited-currency) 
[Phone Number](doc:types#phone-number)
[String](doc:types#string)
[Table](doc:types#table)
[Weight](doc:types#weight)



Address Unformatted
====
Returns USA-based addresses.  Whitespace insensitive, including newlines.

- City, State, Zip, and variant representations of these elements such as abbreviations
- Digits, Street, City, State, Zip, and variant representations of these elements such as abbreviations   
- PO boxes with a number represented in digits
- Lists of addresses in the preceding formats

For example:

```123 Waverly Pl
San Francisco, CA 94110

123 Waverly Pl San Francisco, CA 941104123

PO BOX 1058 San Francisco, CA 94110

123 Waverly Pl
San Francisco, CA
941104123

```

This type **doesn't** match text  that lacks a zip code, such as `11 Center Street, Amherst, MA`.



