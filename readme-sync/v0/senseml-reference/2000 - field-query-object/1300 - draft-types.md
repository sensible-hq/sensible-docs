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

| key                       | value                                                        | description                                                  |
| ------------------------- | ------------------------------------------------------------ | ------------------------------------------------------------ |
| id (**required**)         | `currency`                                                   |                                                              |
| accountingNegative        | `false`, `prefix`, `any`, `both`, `suffix` . Default: `false` | Replaces the deprecated Accounting Currency type. Specifies to recognize accounting sign conventions for negative numbers.<br/>`false` Sensible recognizes negative numbers as described in the preceding **formats recognized** section<br/>`prefix` - Number line prefixed by opening parenthesis, "(", is negative.<br/>`any` - Number line that includes any parenthesis as a suffix or prefix is negative.<br/>`both` - Number  prefixed and suffixed by parenthesis is negative.<br/> |
| requireCurrencySymbol     | boolean. Default: false                                      | Requires a currency symbol preceding the amount.             |
| currencySymbol            | string. Default: `$`                                         | The currency symbol to require, for example €. The symbol must precede the amount. This parameter sets the `unit` parameter in the output. |
| requireThousandsSeparator | boolean.  Default: false                                     | Requires a thousands separator in numbers with a thousands place. |
| thousandsSeparator        | string. Default: `,`                                         | The separator to require, for example `.`                    |
| decimalSeparator          | string. Default: `.`                                         | For numbers with a decimal place, specify the separator, for example `,`. |
| maxDecimalDigits          | number. Default: 4                                           | The maximum number of decimal digits to recognize.           |
| maxValue                  | number. Default: infinity                                    | The maximum currency amount to recognize. Use this to extract an amount with a known range. For example, use it as an alternative to the Tiebreaker parameter, or to extract one currency amount among several returned by a method like the Document Range or Box method. |
| minValue                  | number. Default: infinity                                    | The minimum currency amount to recognize. Use this to extract an amount with a known range. |
| relaxedWithCents          | Boolean. default: false                                      | Use this parameter when poor-quality scans or photographed documents result in erroneous OCR output for the decimal separator or thousands separator.  <br/> If true, Sensible overrides all other Currency type parameters, outputs USD currency, and recognizes the following number format as a currency:<br/><br/>- any number of digits mixed with `<fuzzySeparator>` characters, followed by<br/>- one `<fuzzySeparator>` character, followed by<br/>- two digits (for the cents)<br/><br/>where a `<fuzzySeparator>` character is any of the following common erroneous OCR outputs for a period or comma: <br/>`.,;: _ `  (period, comma, semicolon, colon, space, underscore)<br/><br/>For example, if you set this parameter to true, then for the erroneous OCR output  `"7.859:36"`, Sensible returns: <br>{"source": "7.859:36",<br/>"type": "currency",<br/>"unit": "$",<br/>"value": 7859.36} |
