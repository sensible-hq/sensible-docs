---
title: "Types"
hidden: true
---


Date
-----

You can define the Date type using concise syntax, `"type":"date"`, or you can use expanded syntax and configure the following parameters:

**Parameters**

| key               | value                  | description                                                  |
| ----------------- | ---------------------- | ------------------------------------------------------------ |
| id (**required**) | `date`                 | Returns datetime.  Sensible outputs the time as midnight UTC. |
| format            | string or string array | If unspecified, recognizes default date formats. See the following table for a list of the field descriptors you can use to define custom formats. The custom formats override the defaults. The default formats Sensible recognizes are: <br/> "%m/%d/%Y"</br> "%m/%d/%y", </br>  "%m/%Y", </br>  "%b %d,? %Y", </br>  "%b %d,? %y", </br>  "%b %dst,? %Y", </br>  "%b %dst,? %y", </br>  "%b %dnd,? %Y", </br>  "%b %dnd,? %y", </br>  "%b %dth,? %Y", </br>  "%b %dth,? %y", </br>  "%b %drd,? %Y", </br>  "%b %drd,? %y", </br>  "%m-%d-%Y", </br>  "%m-%d-%y", </br>  "%Y-%m-%d", </br>  "%Y%M%D" |

The following table lists the field descriptors you can use to define a custom format other than the default formats listed in the preceding table. For example, to recognize the date format JAN-01-02, specify `%b-%D-%y`  in the Format parameter.

| **field descriptor** | **meaning**                                                  | **example**                                             |
| -------------------- | ------------------------------------------------------------ | ------------------------------------------------------- |
| `%b`                 | Abbreviated or full month name.                              | Jan, Feb, ..., Dec<br/>January, February, ..., December |
| `%y`                 | Year without century as a zero-padded decimal number. Values in the range 69–99 refer to years in the twentieth century (1969–1999); values in the range 00–68 refer to years in the twenty-first century (2000–2068). | 00, 01, ..., 99                                         |
| `%Y`                 | Year with century as a decimal number.                       | 2013, 2019 etc.                                         |
| `%m`                 | The month number, unpadded or zero-padded                    | 1,...,12<br>01,...,12                                   |
| `%M`                 | The zero-padded month number (01-12)                         | 01,...,12                                               |
| `%d`                 | The day number, unpadded or zero-padded.                     | 1,...,31<br>01,...,31                                   |
| `%D`                 | The zero-padded day number (01-31)                           | 01,...,31                                               |





**Example input**

The following are examples of date formats that Sensible recognizes by default:

```
5/17/2018
november 30, 1955
Feb 1, 21
June 7th, 2021
Jan 9th, 09

```

**Example output**

```json
{
    "source": "Feb 1, 21",
    "value": "2021-02-01T00:00:00.000Z",
    "type": "date"
}

```

