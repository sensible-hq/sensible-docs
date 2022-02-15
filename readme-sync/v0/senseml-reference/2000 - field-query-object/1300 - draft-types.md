---
title: "Types"
hidden: true
---


Name
====

You can define the Name type using concise syntax, `"type":"name"`, or you can use expanded syntax and configure the following parameters:

**Parameters**

| key               | value                                                        | description                                                  |
| ----------------- | ------------------------------------------------------------ | ------------------------------------------------------------ |
| id (**required**) | `name`                                                       |                                                              |
| capitalization    | `allCaps`, `firstLetter`. default: no change to source capitalization | Formats the output in all uppercase, or with only the first letter of each word capitalized. |



Returns one or more names. Doesn't recognize a list of names more than 6 lines long. 

Recognizes names of the formats below, and variant representations of these elements such as abbreviations. 

\- first last
\- first1 last1 and first2 last2
\- last, first1 and first2
\- first1 and first2 last



**Example input**

```json
John R. Smith Sr
Richard & Ann Spangenberg
DuBois, Renee and Lois 
```

This type does **not** recognize lists of three or more names such as `last1, last2, & last3`

Example output:

```json
{
  "source": "Richard & Ann Spangenberg",
  "type": "name",
  "value": [
      "Richard Spangenberg",
      "Ann Spangenberg"
}
```

Currency
====

TODO BEFORE PUBLISH: remove periodDelimitedCurrency



You can define this type using concise syntax,  or you can configure options with expanded syntax.

Simple syntax
----

**Syntax example**

`"type":"currency"`

**Output example** 

Returns US dollars as absolute values.  For example,

``` json
{
    "source": "3 bil",
    "value": 3000000000,
    "unit": "$",
    "type": "currency"
  }
```

**Formats recognized** 

Sensible by default recognizes USA decimal notation (for example, 1,500.06). Recognizes abbreviated quantities, such as k for thousand. For default recognition of European decimal notation (for example, 1.500,06), see [periodDelimitedCurrency](doc:types#perioddelimitedcurrency)  

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

| key                       | value      | description                                                  |
| ------------------------- | ---------- | ------------------------------------------------------------ |
| id (**required**)         | `currency` |                                                              |
| requireCurrencySymbol     | boolean    | Requires a currency symbol preceeding the amount.            |
| currencySymbol            | string     | The currency symbol to require, for example €. The symbol must precede the amount. |
| requireThousandsSeparator | boolean    | Requires a thousands separator in numbers with a thousands place. |
| thousandsSeparator        | string     | The separator to require, for example `,` or `.`             |
| decimalSeparator          | string     | Fo numbers with a decimal place, specify the separator, for example `,` or `.` |
| maxValue                  | number     | The maximum currency amount to recognize. Use this to extract an amount with a known range. For example, use it as an alternative to the Tiebreaker parameter, or to extract one amount among several returned by a method like the Document Range or Box method. |
| minValue                  | number     | The minimum currency amount to recognize. Use this to extract an amount with a known range. |

Custom
====

Defined a custom type using regular expressions. For example, define types for zip codes, time durations, customer IDs, social security numbers, invoice numbers, etc.

**Example syntax**

```
"type":
  {
    "id": "custom",
    "pattern": "^[0-9][0-9]:[0-9][0-9]$",
    "type": "time_24_hr_military"
  }
```

**Example output**

This type outputs strings. For example:

```json
{
    "source": "14:01",
    "value": "14:01",
    "type": "time_24_hr_military"
  }
```

**Parameters**

| key                    | value                    | description                                                  |
| ---------------------- | ------------------------ | ------------------------------------------------------------ |
| id (**required**)      | `custom`                 |                                                              |
| pattern (**required**) | Valid JS regex           | Javascript-flavored regular expression. This parameter doesn't support capturing groups. See the [Regex method](doc:regex) instead.<br/>Double escape special characters since the regex is in a JSON object (for example, `\\s`, not `\s` , to represent a whitespace character. |
| flags                  | JS-flavored regex flags. | Flags to apply to the regex. for example: "i" for case-insensitive. |

