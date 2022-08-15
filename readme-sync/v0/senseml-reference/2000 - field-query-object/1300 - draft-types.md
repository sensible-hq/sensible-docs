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



Address 
====
Returns USA-based addresses.  



Simple syntax
----

**Syntax example**

`"type": "address"`

**Output example** 

``` json
{
    {
      "type": "address",
      "value": "4010 San Amaro Drive\nCoral Gables, FL\n33146"
    }
  }
```

**Formats recognized** 

Recognizes address in block format, where lines are:

-  optionally separated by newlines and 
- the lines contain no text other than the address text.

Recognizes these formats: 

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

Configurable syntax
----

Use configurable syntax to change the default recognized formats.

**Example syntax **

```json
      "type": {
        "id": "address",
        "block_format": false
      }
```

**Example output**

```json
    {
      "type": "address",
      "value": "4010 San Amaro Drive\nCoral Gables, FL 33146"
    }
```

**Parameters**

| key               | value                  | description                                                  |
| ----------------- | ---------------------- | ------------------------------------------------------------ |
| id (**required**) | `currency`             |                                                              |
| block_format      | boolean. Default: true | If set to false, Sensible recognizes addresses embedded in non-address text, such as in paragraphs. The lines containing the address can contain preceding or succeeding non-address text, and must not contain intervening non-address text. <br/> If true, Sensible solely recognizes addresses in consecutive lines, with no preceding, intervening, or succeeding non-address text in those lines. |

