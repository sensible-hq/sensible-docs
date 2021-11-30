---
title: "TFIDF"
hidden: true
---
Classifies fields by comparing them to sample snippets of text that you provide. Outputs classifications of the source fields as a parallel array.  For example, for an array of source fields like this:

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
         "document":"sorbet, cake, ice cream, custard, creme brulee, pudding, chocolate, cookie, mousse, flan"
     },
     {
         "id":"meat_entree",
         "value":"steak, chicken, lamb, pork, beef, turkey, goat, leg, breast, shank, hamburger, filet"
     },
          {
         "type":"dessert",
         "value":"sorbet, cake, ice cream, custard, creme brulee, pudding, chocolate, cookie, mousse, flan"
     }
     
 ]   
    
}
```

Unlike the preceding simplified example, you can enter natural language in the Document parameter. For example, you can list the full text for all of a restaurant's "meat entrees" rather than a short list of keywords.



Parameters
====

The following parameters are contained in the computed field's [global Method](doc:computed-field-methods#parameters) parameter: 


| key                      | value        | description                                                  |
| :----------------------- | :----------- | :----------------------------------------------------------- |
| id (**required**)        | `tfidf`      | TFIDF  (term frequency--inverse document frequency) is an NLP technique that matches extracted text to a relevant Document parameter. |
| source_id (**required**) | field ID     | The TFIDF method works with a source field that outputs an array. For example, the `match:all` parameter returns an array. |
| corpus                   | object array | Array of corpus objects. Each contains the following parameters:<br/>`id`: the category or classification you want applied to an element in the source ID array, if it scores highly against this corpus object.<br/>`document` - example free text containing the key words against which you want to score the output of the source ID. There is no character limit for this parameter. |

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
