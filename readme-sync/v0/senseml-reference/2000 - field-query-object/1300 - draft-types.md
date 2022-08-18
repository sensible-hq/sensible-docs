---
title: "Types"
hidden: true
---


Address 
====
Returns USA-based addresses.  By default, Sensible recognizes  single- or multi-line addresses isolated from other lines in "block" format, for example the formatting on a shipping label. For example, `"type":"address"` recognizes address such as:

![Click to enlarge](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/images/final/type_address_block.png)

Use the Block Format parameter to recognize addresses embedded in non-address lines, for example, use:

      "type": {
        "id": "address",
        "block_format": false
      } 

to find text in a paragraph:

![Click to enlarge](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/images/final/type_address_paragraph.png)



**Formats recognized** 

With either block or in-line address, Sensible recognizes these formats: 

- City, State, Zip, and variant representations of these elements such as abbreviations
- Digits, Street, City, State, Zip, and variant representations of these elements such as abbreviations   
- PO boxes with a number represented in digits
- Lists of addresses in the preceding formats



Sensible is less sensitive to non-address text if you configure `"block_format": false`:

|                                                              | Block | In-line |      |
| ------------------------------------------------------------ | ----- | ------- | ---- |
| Newlines optional                                            | yes   | yes     |      |
| Trailing or leading non-address text allowed in starting or ending address lines | no    | yes     |      |
| Non-address text allowed between address elements            | no    | no      |      |

For example:

```123 Waverly Pl
# block format

San Francisco, CA 94110

123 Waverly Pl San Francisco, CA 941104123

PO BOX 1058 San Francisco, CA 94110

123 Waverly Pl
San Francisco, CA
941104123

# inline format

the shipping address is 123 Waverly Pl
San Francisco, CA, 94110. The billing address is the same. 

```

This type **doesn't** match text  that lacks a zip code, such as `11 Center Street, Amherst, MA`.







