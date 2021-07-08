---
title: "types draft"
hidden: true
---
TODO: add quotes to example output keys



accountingCurrency
----

Returns US dollar numbers. 

Recognizes digits ( decimal places, comma-deliminated thousands) optionally preceded by a US dollar sign ($), for example: 

```
56,999
-$527.01
```



Example output:


```json
{
  source: "-$56,237",
  type: "accountingCurrency",
  unit: "$",
  value: -56237,
}
```

TODO: doesn't look like it rounds to 2 decimal places? like it would just return 4.56789798 as is?  

Address
----
Returns USA-based addresses only, for example:

```123 Waverly Pl
San Francisco, CA 94110
```

and

```PO BOX 1058 San Francisco, CA 94110```

If multiple consecutive addresses are captured in a single extracted key/value  pair, Sensible correctly returns multiple addresses. 

Example output:
```json
{
	source: "",
	type: "address",
	value: "123 Waverly Pl\nSan Francisco, CA 941104123",
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

Returns US dollars. Recognizes both written-out numbers and digits,  optionally preceded by a US dollar symbol ($), for example: 

```
2 thousand
$1k
5k
one million
1 mm
3 bil
$5.33

```

Example output:

```json
{
  source: "1 Million",
  type: "currency",
  unit: "$",
  value: 1000000,
}
```

Date
-----

Returns date in year-month-days format. Recognizes a variety of dates in month-day-year format, for example:

```
5/7/2018
november 30, 1955
Feb 1, 21
12/20
```

Example output:

```json
{
  source: "12/20",
  type: "date",
  value: new Date(2020, 12, 1),
}
```



Distance
----

Returns distances in metric and imperial units. Recognizes digits followed optionally by kilometers, miles, or their abbreviations.  For example: 

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
  source: "1,123,451.123 kms",
  type: "distance",
  unit: "kilometers",
  value: 1123451.123,
}
```

Name
----

Returns one or more names. Does not recognize a list of names more than 6 lines long. 

TODO: come back to this one, kinda complex

Number
----

TODO: no test. dig into regex (or just present it??): is it:

positive or negative number optionally deliminated by commas , and optionally followed by a decimal point and decimal component.

const amount = "\\d+(?:(?:,\\d{3})*)(?:\\.\\d+)?|\\.\\d+";

const REGEX = new RegExp(`(-?\\b(?:${amount})\\b)`, "gi");

Paragraph
----

TODO: ask about this one. how does it interact w documentRange? 

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

Returns weights in metric and imperial units. Recognizes digits followed optionally by pounds, kilograms, or their abbreviations. For example: 

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

