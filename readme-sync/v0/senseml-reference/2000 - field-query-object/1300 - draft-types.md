---
title: currency
hidden: true
---



TODO: mark accounting currency as deprecated AND search for incoming links 

Currency
====

You can define this type using concise syntax, or you can configure options with expanded syntax.

Simple syntax
----

**Syntax example**

`"type": "currency"`

**Output example** 

Returns USA dollars as absolute value. For example,

``` json
{
    "source": "3 bil",
    "value": 3000000000,
    "unit": "$",
    "type": "currency"
  }
```

**Formats recognized** 

Sensible by default recognizes USA decimal notation (for example, 1,500.06). Recognizes abbreviated quantities, such as k for thousand.

To recognize European decimal notation (for example, 1.500,06), see the following configurable syntax section.

Recognizes digits with the following formatting:

- dollar sign, optional commas every three digits, optional cents after period

- commas every three digits, optional cents after period

- no dollar sign, up to six digits without commas as sole line contents. Allow up to nine digits if cents are present.


Recognizes abbreviated and written-out quantities as follows:

- thousand, k
- million, mil, mm, m
- billion, bil, b
- trillion, t

For example: 

```
$1k
5k
1,000,000.056
$5.33
1 mm
3 bil
2 thousand
```

This type **doesn't** match text such as `one million`  or `123456789`.

Configurable syntax
----

Use configurable syntax to change the default recognized formats.

**Example syntax **

```json
"type":
  {
    "id": "currency",
    "currencySymbol": "€",
    "requireCurrencySymbol": true,  
    "thousandsSeparator": ".",
    "decimalSeparator": ",", 
    "maxValue": 10000,
  }
```

**Example output**

```json
{
    "source": "€3.567,01",
    "value": 3567.01,
    "unit": "€",
    "type": "currency"
  }
```

**Parameters**

| key                | value                                                        | description                                                  |
| ------------------ | ------------------------------------------------------------ | ------------------------------------------------------------ |
| id (**required**)  | `currency`                                                   |                                                              |
| accountingNegative | `false`, `anyParentheses`, `bothParentheses`, `suffixNegativeSign` Default: `false` | Replaces the deprecated Accounting Currency type. Specifies to recognize accounting sign conventions for negative numbers.<br/>`false` Sensible recognizes negative numbers as described in the preceding **formats recognized** section<br/>`bothParentheses` -  Sensible assigns a negative value to a number prefixed and suffixed by parentheses.<br/>`anyParentheses` - Sensible assigns a negative value to a number that includes any parentheses as a suffix or prefix. Use this option to handle OCR errors, where an opening or closing parenthesis can be OCR'd as other characters.<br/>`suffixNegativeSign` - Sensible assigns a negative value to number suffixed by a negative sign.<br/> |
| alwaysNegative     | boolean                                                      | If true, Sensible assigns a negative value to a number and ignores sign symbols in the document. For example, use this to capture the negative values in the debit column of an accounting document, where the negative sign is omitted. |
| removeSpaces       | boolean                                                      | Removes space inside a line for better currency recognition. For example, changes the single line `$     12.45` to `$12.45`. |
|                    |                                                              |                                                              |
|                    |                                                              |                                                              |
|                    |                                                              |                                                              |
|                    |                                                              |                                                              |
|                    |                                                              |                                                              |
|                    |                                                              |                                                              |
|                    |                                                              |                                                              |
|                    |                                                              |                                                              |
|                    |                                                              |                                                              |
