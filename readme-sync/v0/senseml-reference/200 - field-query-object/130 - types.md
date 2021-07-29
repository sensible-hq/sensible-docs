---
title: "types draft"
hidden: true
---
Specify the Type parameter in a [Field object](doc:field-query-object) to capture data of a particular type. 

For example, the following field returns null unless it finds data that Sensible recognizes as a number: 

```json
{
  "fields": [
    {
      "id": "example_field",
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

[accountingCurrency](doc:types#section-accountingcurrency)
[address](doc:types#section-address)
[boolean](doc:types#section-boolean)
[currency](doc:types#section-currency)
[date](doc:types#section-date)
[distance](doc:types#section-distance)
[images](doc:types#section-images)
[name](doc:types#section-name)
[number](doc:types#section-number)
[paragraph](doc:types#section-paragraph)
[percentage](doc:types#section-percentage)
[string](doc:types#section-string)
[table](doc:types#section-table)
[weight](doc:types#section-weight)

accountingCurrency
----

Returns US dollar numbers. Supports negative numbers.

Recognizes digits ( decimal places, comma-delimitated thousands) optionally preceded by a US dollar sign ($). Supports negative numbers represented either with parentheses `()` or with the minus sign (`-`). Examples: 

```
56,999
-$527.01
(1,000)
($400.567)
```

Example output:


```json
 {
    "source": "($400.567)",
    "value": -400.567,
    "unit": "$",
    "type": "accountingCurrency"
  }
```

Address
----
Returns USA-based addresses. Matches:

- City, State, Zip, and variant representations of these elements such as abbreviations
- Digits, Street, City, State, Zip, and variant representations of these elements such as abbreviations .  TODO: According to my test, something lacking zip like 11 Center Street, Amherst, MA isn't recognized, is that right? see https://dev.sensible.so/editor/?d=test_playground_frances&c=types&g=test_types 
- PO boxes with a number represented in digits

For example:

```123 Waverly Pl
San Francisco, CA 94110
123 Waverly Pl San Francisco, CA 941104123
PO BOX 1058 San Francisco, CA 94110
```

If multiple consecutive addresses are captured in a single extracted key/value  pair, Sensible correctly returns multiple addresses. 

This type **does not** match text  that lacks a zip code, such as `11 Center Street, Amherst, MA`.

Example output:
```json
 {
    "value": "123 Waverly Pl San Francisco, CA 941104123",
    "type": "address"
  }
```



Boolean
----

Returns true for the following case-insensitive strings:

```json
true
yes
y
```

Returns false for the following case-insensitive strings:

```json
false
no
n
```

Example output:

```json
{
  source: "YES",
  type: "boolean",
  value: true,
}
```

Currency
----

Returns US dollars as absolute values. Recognizes numbers represented as digits with the thousand place value represented with commas (common in the USA) or periods (common in Europe). 

Recognizes digits as follows:

- dollar sign, optional commas every three digits, optional cents

- no dollar sign, commas every three digits, optional cents

- digits with periods every three digits, optional cents after comma

- Optional dollar sign, up to six digits without commas as only line contents. Allow up to nine digits if cents are present

- No dollar sign, up to six digits without commas as only line contents. Allow up to nine digits if cents are present

  

Recognizes abbreviated and written-out quantities as follows:

- thousand, k
- million, mil, mm, m
- billion, bil, b
- trillion, t

For example: 

```
2 thousand
$1k
5k
1.000.000,05
$1,000,000.05
1 mm
3 bil
$5.33

```

This type **does not** match text such as `one million`  or `123456789`.

Example output:

```json
 {
    "source": "3 bil",
    "value": 3000000000,
    "unit": "$",
    "type": "currency"
  }
```

Date
-----

Returns date in year-month-days format. Recognizes:

- Dates formatted as `MM/DD/YYYY`, and variant representations of these elements such as abbreviations
- Dates formatted as `month name, DD, YYYY`, and and variant representations of these elements such as abbreviations

For example:

```
5/17/2018
november 30, 1955
Feb 1, 21

```

This type does **not** recognize text such as `12/20`.

Example output:

```json
{
    "source": "Feb 1, 21",
    "value": "2021-02-01T00:00:00.000Z",
    "type": "date"
}

```



Distance
----

Returns miles and kilometers. Recognizes numbers represented as digits followed optionally by kilometers, miles, or their abbreviations.  For example: 

```
3,001.5 kilometers
2 km
1.5 kms
1 mile
4 mi
45
```

Example output:

```json
 {
    "source": "3,001.5 kilometers",
    "value": 3001.5,
    "unit": "kilometers",
    "type": "distance"
  }
```

Images
---

Can only be used with [Document Range](https://docs.sensible.so/docs/document-range) to return image metadata.


Name
----

Returns one or more names. Does not recognize a list of names more than 6 lines long. 

Recognizes names of the formats below and and variant representations of these elements such as abbreviations:
\- First Last
\- First1 Last1 and First2 Last2
\- Last, First1 and First2
\- First1 and First2 Last

For example:

```json
John R. Smith
Richard & Ann Spangenberg
DuBois, Renee and Lois 


```

This type does not recognize text such as `Last1, Last2, & Last3`

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



Number
----

Recognizes numbers represented as digits and optionally:

- using commas to represent the thousand place value
- using a period to represent the decimal place

For example:

```
-3.1
3,500,053.78
1234567890
```

Example output:

```json
{
    "source": "123456789",
    "value": 123456789,
    "type": "number"
}
```

LEFT OFF

Paragraph
----

A string with newlines at paragraph breaks (to be used with [Document Range](https://docs.sensible.so/docs/document-range) only. TODO: why is it necessary to specify this/why useful?

Percentage
----

looks like it recognizes any number comma-deliminated and including decimal point.

/(\b\d+(?:(?:,\d{3})*)(?:\.\d+)?|\.\d+)\s?%/gi

QUESTION/to test: looks like maybe it doesn't recognize negative #s? (-)

String
----

Returns strings.

Example output:

```
{
  source: "report",
  value: "report",
  type: "string",
}
```

Weight
---

Returns pounds and kilograms. Recognizes numbers represented as digits followed optionally by pounds, kilograms, or their abbreviations. For example: 

```json
1,00.4 kg
1 kilo
5.5 kilograms
6,00 lbs
1 pound
6.83
```

Example output:

```json
{
  source: "1,123,451 pounds",
  type: "weight",
  unit: "pounds",
  value: 1123451,
}
```

Example output:

```json
{
  source: "1,123,451",
  type: "weight",
  value: 1123451,
}
```

