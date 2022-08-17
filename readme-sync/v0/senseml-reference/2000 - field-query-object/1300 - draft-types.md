---
title: "Types"
hidden: true
---


Address 
====
Returns USA-based addresses.  By default, Sensible recognizes  single- or multi-line addresses isolated from other lines in "block" format, for example the formatting on a shipping label. For example:

![Click to enlarge](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/images/final/type_address_block.png)

Use the `"block_format": "false"` parameter to recognize addresses embedded in non-address lines, for example in a paragraph: 

![Click to enlarge](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/images/final/type_address_paragraph.png)

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

Recognizes address in block format, such as the formatting on a shipping label,  where lines are:

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
    {
      "type": "address",
      "value": "4010 San Amaro Drive\nCoral Gables, FL\n33146"
    }
  }
```

**Parameters**

| key               | value                  | description                                                  |
| ----------------- | ---------------------- | ------------------------------------------------------------ |
| id (**required**) | `currency`             |                                                              |
| block_format      | boolean. Default: true | If set to false, Sensible recognizes addresses embedded in non-address text, such as in paragraphs. The lines containing the address can contain preceding or succeeding non-address text, and must not contain intervening non-address text. <br/> If true, Sensible solely recognizes addresses in consecutive lines, with no preceding, intervening, or succeeding non-address text in those lines. |

