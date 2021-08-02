---
title: "types draft"
hidden: false
---
Specify the Type parameter in a [Field object](doc:field-query-object) to capture data of a particular type. 

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

[Accounting Currency](doc:types#accountingcurrency)
[Address](doc:types#address)
[Boolean](doc:types#boolean)
[Currency](doc:types#currency)
[Date](doc:types#date)
[Distance](doc:types#distance)
[Images](doc:types#images)
[Name](doc:types#name)
[Number](doc:types#number)
[Paragraph](doc:types#paragraph)
[Percentage](doc:types#percentage)
[Period Delimited Currency](doc:types#perioddelimitedcurrency) 
[String](doc:types#string)
[Table](doc:types#table)
[Weight](doc:types#weight)



Accounting Currency
----

Returns US dollar numbers. Supports negative numbers.

Recognizes digits in USA decimal notation (i.e., 1,500.06):

- digits are in the format recognized by the [Number](doc:types#number) type
- digits are optionally preceded by a US dollar sign ($) 
- supports negative numbers represented either with parentheses `()` or with the minus sign (`-`)

Examples: 

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
- Digits, Street, City, State, Zip, and variant representations of these elements such as abbreviations   
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

Returns US dollars as absolute values. Recognizes USA decimal notation (i.e., 1,500.06) Recognizes abbreviated quantities such as k for thousand.  For  European decimal notation  (i.e., 1.500,06), see [periodDelimitedCurrency](doc:types#perioddelimitedcurrency)  

Recognizes digits with the following formatting:

- dollar sign, optional commas every three digits, optional cents after period

- commas every three digits, optional cents after period

- no dollar sign, up to six digits without commas as only line contents. Allow up to nine digits if cents are present.


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

Returns date in year-month-days format. Recognizes the following formatting:

-  `MM/DD/YYYY`, and variant representations of these elements such as abbreviations
-  `month name, DD, YYYY`, and and variant representations of these elements such as abbreviations

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

Returns miles and kilometers. Recognizes digits followed optionally by kilometers, miles, or their abbreviations.  For example: 

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

Recognizes names of the formats below, and and variant representations of these elements such as abbreviations:
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

Recognizes digits in USA decimal notation. Recognizes digits as follows:

- one or more digits, optionally followed by:
  - EITHER commas preceding every three digits, optional digits after period 
  - OR by digits after period

For example:

```
-3.1
3,500,053.78
1234567890
```

This type does **not** recognize text such as `3.061.534,45`. Use the Currency or Period Deliminated Currency types instead. 

Example output:

```json
{
    "source": "123456789",
    "value": 123456789,
    "type": "number"
}
```



Paragraph
----

Use with  [Document Range](https://docs.sensible.so/docs/document-range) only, to return paragraphs as output that is separated by newline characters (\n), instead of as a single string. Sensible recognizes paragraphs separated by vertical gaps. Sensible does not recognize paragraphs indicated solely by indented first lines. 

Percentage
----

Returns percent as an absolute value. Recognizes a percent formatted as digits in USA decimal notation (i.e., 1,500.06), followed optionally by a whitespace, followed by a percent sign (%) . 

For example:

```json
20.1 %
20.1%
1,000.05%
```



Example:

```json
 {
    "source": "20.5%",
    "value": 20.5,
    "type": "percentage"
  }
```



Period Delimited Currency
----

Returns numbers as absolute values. Recognizes European decimal formatting (i.e., 1.500,06). Recognizes abbreviated quantities, such as k for thousand.  For  USA decimal formatting (i.e., 1,500.06), see [currency](doc:types#currency)  

Recognizes digits with the following formatting:

- periods every three digits, optional cents after comma

- up to six digits without periods as only line contents. Allow up to nine digits if cents following comma are present.


Recognizes abbreviated and written-out quantities as follows:

- thousand, k
- million, mil, mm, m
- billion, bil, b
- trillion, t

For example: 

```
€1k
5k
1.000.000,056
€5,33
1 mm
3 bil
2 thousand

```

This type **does not** match text such as `one million`  or `123456789`. It does not currently support outputting units of currency.

Example output:

```json
{
    "source": "5,33",
    "value": 5.33,
    "type": "periodDelimitedCurrency"
}
```




String
----

Returns strings.

Example output:

```
{
    "type": "string",
    "value": "3 bil"
}
```

Weight
---

Returns pounds and kilograms. Recognizes digits in USA decimal notation (i.e., 1,500.06):

- digits are in the format recognized by the [Number](doc:types#number) type

- digits are followed optionally by pounds, kilograms, or their abbreviations 

For example: 

```json
1,000.4 kg
1 kilo
5.5 kilograms
6.00 lbs
1 pound
634.83
```


Example output:

```json
{
    "source": "6,000.01 lbs",
    "value": 6000.01,
    "unit": "pounds",
    "type": "weight"
}
```

