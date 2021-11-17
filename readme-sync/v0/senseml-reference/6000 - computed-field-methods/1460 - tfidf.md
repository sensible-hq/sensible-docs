---
title: "TFIDF"
hidden: true
---
Classifies the output of other fields against how closely they are related to sample snippets of text.

Parameters
====

The following parameters are contained in the computed field's [global Method](doc:computed-field-methods#parameters) parameter: 


| key                      | value        | description                                                  |
| :----------------------- | :----------- | :----------------------------------------------------------- |
| id (**required**)        | `tfidf`      |                                                              |
| source_id (**required**) | field ID     | Usually, you use the match:all method to extract an array of values for a single field, then run those values through the TFIDF computed field method. |
| corpus                   | object array | Array of corpus objects. Each contains the following parameters:<br/>`id`: the category/classification you want applied to any text from the Source ID output that scores highly against this corpus object.<br/>`document` - a short string of example free text containing the key words against which you want to score the output of the Source ID. |

Examples
====



**Config**

```json

```

**PDF**

The following image shows the example PDF used with this example config:

![Click to enlarge](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/images/final/tfidf.png)

| Example PDF | [Download link](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/pdfs/tfidf.pdf) |
| ---------------------- | ------------------------------------------------------------ |

**Output**

```json

```
