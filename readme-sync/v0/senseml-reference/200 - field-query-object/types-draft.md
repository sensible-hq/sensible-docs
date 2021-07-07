---
title: "types draft"
hidden: true
---
accountingCurrency
----

Recognizes numbers formatted in accounting format, for example, "56,999" or ""-$527.01".  Currently supports only US dollars.

Example output:


```json
{
  source: "-$56,237",
  type: "accountingCurrency",
  unit: "$",
  value: -56237,
}
```



Address
----
Recognizes only USA-based addresses only, for example:

```123 Waverly Pl
San Francisco, CA 94110
```

and

```PO BOX 1058 San Francisco, CA 94110```

If multiple addresses are listed consecutively in a single extracted key/value  pair, Sensible correctly parses them into multiple addresses. 

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

Recognizes true for the following case-insensitive strings:

```json
true
yes
y
```

Recognizes false for the following case-insensitive strings:

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

