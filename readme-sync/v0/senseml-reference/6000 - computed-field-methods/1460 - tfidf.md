---
title: "TFIDF"
hidden: true
---
Classifies the output of source fields against how closely they are related to sample snippets of text that you provide. Outputs classifications of the source fields.  For example, an array of source fields like this:

```json
{
 "menu_items": [
     {
         "type":"string",
         "value":"blackberry sorbet"
     },
     {
         "type":"string",
         "value":"seared steak with fingerling potatos "
     },
          {
         "type":"string",
         "value":"chocolate cake with rasberry glaze"
     }
     
 ]   
    
}
```

You can use the TFIDF computed field method to output:

```json
{
 "classified_menu_items": [
     {
         "id":"dessert",
         "document":"sorbet, cake, ice cream, custard, creme brulee, pudding"
     },
     {
         "id":"meat_entree",
         "value":"steak, chicken, lamb, pork, beef, turkey, goat"
     },
          {
         "type":"dessert",
         "value":"sorbet, cake, ice cream, custard, creme brulee, pudding"
     }
     
 ]   
    
}
```





Parameters
====

The following parameters are contained in the computed field's [global Method](doc:computed-field-methods#parameters) parameter: 


| key                      | value        | description                                                  |
| :----------------------- | :----------- | :----------------------------------------------------------- |
| id (**required**)        | `tfidf`      |                                                              |
| source_id (**required**) | field ID     | Usually, you use the `match:all` parameter to extract an array of values for a single field, then run those values through the TFIDF computed field method. |
| corpus                   | object array | Array of corpus objects. Each contains the following parameters:<br/>`id`: the category/classification you want applied to any text from the source ID output that scores highly against this corpus object.<br/>`document` - a short string of example free text containing the key words against which you want to score the output of the source ID. |

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
