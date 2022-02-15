---
title: "Types"
hidden: false
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



Accounting Currency
====

Returns US dollar numbers. Supports negative numbers represented either with parentheses `()` or with the minus sign (`-`).

Recognizes digits in USA decimal notation (for example, 1,500.06):

- digits are in the format recognized by the [Number](doc:types#number) type
- digits are optionally preceded by a US dollar sign ($) 

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
====
Returns USA-based addresses. Matches:

- City, State, Zip, and variant representations of these elements such as abbreviations
- Digits, Street, City, State, Zip, and variant representations of these elements such as abbreviations   
- PO boxes with a number represented in digits

For example:

```123 Waverly Pl
San Francisco, CA 94110

123 Waverly Pl San Francisco, CA 941104123

PO BOX 1058 San Francisco, CA 94110

123 Waverly Pl
San Francisco, CA
941104123

```

If consecutive addresses are captured in a single extracted key/value pair, Sensible returns multiple addresses. 

This type **doesn't** match text  that lacks a zip code, such as `11 Center Street, Amherst, MA`.

Example output:
```json
 {
    "value": "123 Waverly Pl\nSan Francisco, CA\n941104123",
    "type": "address"
  }
```



Boolean
====

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
====

Returns US dollars as absolute values. Recognizes USA decimal notation (for example, 1,500.06). Recognizes abbreviated quantities, such as k for thousand. For European decimal notation  (for example, 1.500,06), see [periodDelimitedCurrency](doc:types#perioddelimitedcurrency)  

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
====
You can define this type using concise syntax,  or you can configure options with expanded syntax.

Simple syntax
----

**Syntax example **

`"type":"date"`

**Output example**

```json
{
    "source": "Feb 1, 21",
    "value": "2021-02-01T00:00:00.000Z",
    "type": "date"
}
```

**Formats recognized**


Sensible recognizes the following date formats by default:

```json
"%m/%d/%Y",
"%m/%d/%y",
"%m/%Y",
"%b %d,? %Y",
"%b %d,? %y",
"%b %dst,? %Y",
"%b %dst,? %y",
"%b %dnd,? %Y", 
"%b %dnd,? %y",
"%b %dth,? %Y",
"%b %dth,? %y",
"%b %drd,? %Y",
"%b %drd,? %y",
"%m-%d-%Y",
"%m-%d-%y",
"%Y-%m-%d",
"%Y%M%D"
```
See the following configurable syntax section for definitions of the field descriptors in the preceding list.

The following are examples of date formats that Sensible recognizes by default:

```
5/17/2018
november 30, 1955
Feb 1, 21
June 7th, 2021
Jan 9th, 09

```


Configurable syntax
---

**Syntax example**

To recognize the date format JAN-01-02, and ignore all default formats, you can specify:

````json
"type":
  {
    "id": "date",
    "format": "%b-%D-%y"   
  }
````

**Output example**

```
{
    "source": "JAN-01-24",
    "value": "2022-01-24T00:00:00.000Z",
    "type": "date"
}
```

**Parameters**

| key               | value                  | description                                                  |
| ----------------- | ---------------------- | ------------------------------------------------------------ |
| id (**required**) | `date`                 | Returns datetime.  Sensible outputs the time as midnight UTC. |
| format            | string or string array | If unspecified, recognizes default date formats. See the following table for a list of the field descriptors you can use to define custom formats. The custom formats override the defaults listed in the simple syntax section. |

The following table lists the field descriptors you can use to define a custom format other than the default formats listed in the simple syntax section.

| **field descriptor** | **meaning**                                                  | **example**                                             |
| -------------------- | ------------------------------------------------------------ | ------------------------------------------------------- |
| `%b`                 | Abbreviated or full month name.                              | Jan, Feb, ..., Dec<br/>January, February, ..., December |
| `%y`                 | Year without century as a zero-padded decimal number. Values in the range 69–99 refer to years in the twentieth century (1969–1999); values in the range 00–68 refer to years in the twenty-first century (2000–2068). | 00, 01, ..., 99                                         |
| `%Y`                 | Year with century as a decimal number.                       | 2013, 2019 etc.                                         |
| `%m`                 | The month number, unpadded or zero-padded                    | 1,...,12<br>01,...,12                                   |
| `%M`                 | The zero-padded month number (01-12)                         | 01,...,12                                               |
| `%d`                 | The day number, unpadded or zero-padded.                     | 1,...,31<br>01,...,31                                   |
| `%D`                 | The zero-padded day number (01-31)                           | 01,...,31                                               |



Distance
====

Returns miles and kilometers. Recognizes digits followed optionally by kilometers, miles, or their abbreviations. For example: 

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
====

Use this solely with the [Document Range](https://docs.sensible.so/docs/document-range) method to return image metadata.


Name
====

Returns one or more names. Doesn't recognize a list of names more than 6 lines long. 

Recognizes names of the formats below, and variant representations of these elements such as abbreviations:
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

This type does **not** recognize text such as `Last1, Last2, & Last3`

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
====

Recognizes digits in USA decimal notation. Recognizes one or more digits, optionally followed either by: 

- commas preceding every three digits, optional digits after period, or by 
- digits after period

For example:

```
-3.1
3,500,053.78
1234567890
```

This type does **not** recognize text such as `3.061.534,45`. Use the Period Delimited Currency type instead. 

Example output:

```json
{
    "source": "123456789",
    "value": 123456789,
    "type": "number"
}
```



Paragraph
====

Use with  [Document Range](https://docs.sensible.so/docs/document-range) solely, to return paragraphs formatted with newline characters (\n), instead of formatted as a single string. Sensible recognizes paragraphs separated by vertical gaps. Sensible doesn't recognize paragraphs indicated solely by indented first lines. 

Percentage
====

Returns percent as an absolute value. Recognizes a percent formatted as digits in USA decimal notation (for example, 1,500.06), followed optionally by a whitespace, followed by a percent sign (%) . 

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
====

Returns numbers as absolute values. Recognizes European decimal formatting (for example, 1.500,06). Recognizes abbreviated quantities, such as k for thousand. For  USA decimal formatting (for example, 1,500.06), see [currency](doc:types#currency). 

Recognizes digits with the following formatting:

- periods every three digits, optional cents after a comma.

- up to six digits without periods as sole line contents. Allow up to nine digits if cents following a comma are present.


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

This type **doesn't** match text such as `one million`  or `123456789`. It doesn't output units of currency.

Example output:

```json
{
    "source": "5,33",
    "value": 5.33,
    "type": "periodDelimitedCurrency"
}
```



Phone Number
====

Returns phone numbers:

- Recognizes USA 10-digit phone numbers either with or without a country calling code. May be optionally formatted with parentheses, dashes, spaces, plus sign (+), or periods. 

- Recognizes international phone numbers if prefixed by a country calling code (for example, +91 for India).

Examples: 

```
1-888-353-9578
+18883539578
888.353.9577
888 353 3264
888 353-3232
(207) 312-6767
+91 9999999999
+91 9999 999999
+91 9999-999999
```

Example output:


```json
{
    "type": "phoneNumber",
    "source": "(855) 786-3246",
    "value": "+18557863246"
}
```

This type does *not* recognize country calling codes formatted with 00, for example, 0091 or 001. 


String
====

Returns strings.

Example output:

```
{
    "type": "string",
    "value": "3 bil"
}
```

Table
====

Use with the Table methods:

- [Invoice](doc:invoice)
- [Fixed Table](doc:fixed-table)
- [Table](doc:table)
- [Text Table](doc:text-table)

Weight
====

Returns pounds and kilograms. Recognizes digits in USA decimal notation (for example, 1,500.06):

- digits are in the format recognized by the [Number](doc:types#number) type

- "pounds", "kilograms", or their abbreviations follow the digits 

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

