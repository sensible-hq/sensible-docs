---
title: "(Deprecated) TFIDF"
hidden: true
---
## Deprecated

This method is deprecated. [LLM-based methods](doc:prompt-tips) replace this method.

## Description

Classifies fields by comparing them to sample snippets of free text that you provide. For example, for a source field like this:

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

You can return a classification for each array element as a parallel array , like this:

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

To produce this output, you specify classifications and corresponding example text ("documents") in the TFIDF computed field method. Unlike the preceding simplified example, you can enter examples in the Document parameter. For example, you can list the full text for a restaurant's "meat entrees" rather than a short list of keywords.

Parameters
====

The following parameters are in the computed field's [global Method](doc:computed-field-methods#parameters) parameter: 


| key                      | value        | description                                                  |
| :----------------------- | :----------- | :----------------------------------------------------------- |
| id (**required**)        | `tfidf`      | TFIDF  (term frequency--inverse document frequency) is a technique that determines a category for the extracted text by matching it to a relevant Document parameter. |
| source_id (**required**) | field ID     | For every field you want to classify, create a TFIDF computed field and specify the field ID. If the source field outputs an array, then this method returns the classifications as a parallel array. |
| corpus                   | object array | Array of corpus objects. Each contains the following parameters:<br/>`id`: the category or classification you want applied to an element in the source ID array, if it scores highly against this corpus object. It's best practice to choose categories that are mutually exclusive. If the categories aren't mutually exclusive, then Sensible chooses a winning category using the greatest overlap of rare words between the source field and the document.<br/>`document` - example free text containing the key words against which you want to score the output of the source ID. This parameter has no character limit. |

Examples
====

The following example classifies the items on a restaurant menu. For the sake of concise syntax, the two source fields use `"match":"all"` to return arrays, and the TFIDF computed fields return classifications as parallel arrays to the input arrays.

**Config**

```json
{
  "fields": [
    {
      "id": "dinner_specials",
      "match": "all",
      "anchor": {
        "start": {
          "text": "dinner specials",
          "type": "equals"
        },
        "match": {
          "type": "regex",
          "pattern": "^~ [A-Z].*$"
        },
        "end": {
          "text": "dessert specials",
          "type": "startsWith"
        }
      },
      "method": {
        "id": "passthrough"
      }
    },
    {
      "id": "dessert_specials",
      "match": "all",
      "anchor": {
        "start": {
          "text": "dessert specials",
          "type": "equals"
        },
        "match": {
          "type": "regex",
          "pattern": "^~ [A-Z].*$"
        }
      },
      "method": {
        "id": "passthrough"
      }
    }
  ],
  "computed_fields": [
    {
      "id": "classified_dinners",
      "method": {
        "id": "tfidf",
        "source_id": "dinner_specials",
        "corpus": [
          {
            "id": "meat_entree",
            "document": "Seared beef with fingerling potatoes and asparagus, Chicken breast stuffed with asiago cheese, with scalloped potatoes, apricot-braised lamb shank with couscous and mixed greens, curried lamb with peas, carrots, and flatbread, chicken, pork, veal, beef, duck, goose, turkey, breast, leg, sirloin"
          },
          {
            "id": "fish_entree",
            "document": "Grilled salmon with almond rice pilaf and spinach with pine nuts, sea bass with root vegetables and peas, trout with almonds and rice pilaf, buttered seared shrimp puffs, scallops, crab, fish, flounder, tuna, swordfish, catfish, crayfish, mussels, herring, lox "
          }
        ]
      }
    },
    {
      "id": "classified_desserts",
      "method": {
        "id": "tfidf",
        "source_id": "dessert_specials",
        "corpus": [
          {
            "id": "french_desserts",
            "document": "creme brulee, Strawberry tart with creme patissiere and caramel sauce, brioche bread pudding with chocolate glaze, mille-feuille, madeleine, crepe, palmiers, souffle"
          },
          {
            "id": "italian_desserts",
            "document": "tiramisu with raspberries, cannoli cake with candied lavender, mascarpone cheesecake with blueberry ice cream, panettone, panna cotta, semifreddo, biscotti "
          }
        ]
      }
    }
  ]
}
```

**Example document**

The following image shows the example document used with this example config:

![Click to enlarge](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/images/final/tfidf.png)

| Example document | [Download link](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/pdfs/tfidf.pdf) |
| ---------------------- | ------------------------------------------------------------ |

**Output**

```json
{
  "dinner_specials": [
    {
      "type": "string",
      "value": "~ Grilled salmon with almond rice pilaf and spinach with pine nuts"
    },
    {
      "type": "string",
      "value": "~ Seared beef with fingerling potatoes and asparagus"
    },
    {
      "type": "string",
      "value": "~ Chicken breast stuffed with asiago cheese, with scalloped potatoes and"
    },
    {
      "type": "string",
      "value": "~ Apricot-braised lamb shank with couscous and mixed greens"
    }
  ],
  "dessert_specials": [
    {
      "type": "string",
      "value": "~ Cannoli cake with candied lavender"
    },
    {
      "type": "string",
      "value": "~ Creme brulee"
    },
    {
      "type": "string",
      "value": "~ Tiramisu with raspberries"
    },
    {
      "type": "string",
      "value": "~ Strawberry tart with creme patissiere and caramel sauce"
    }
  ],
  "classified_dinners": [
    {
      "id": "fish_entree",
      "document": "Grilled salmon with almond rice pilaf and spinach with pine nuts, sea bass with root vegetables and peas, trout with almonds and rice pilaf, buttered seared shrimp puffs, scallops, crab, fish, flounder, tuna, swordfish, catfish, crayfish, mussels, herring, lox "
    },
    {
      "id": "meat_entree",
      "document": "Seared beef with fingerling potatoes and asparagus, Chicken breast stuffed with asiago cheese, with scalloped potatoes, apricot-braised lamb shank with couscous and mixed greens, curried lamb with peas, carrots, and flatbread, chicken, pork, veal, beef, duck, goose, turkey, breast, leg, sirloin"
    },
    {
      "id": "meat_entree",
      "document": "Seared beef with fingerling potatoes and asparagus, Chicken breast stuffed with asiago cheese, with scalloped potatoes, apricot-braised lamb shank with couscous and mixed greens, curried lamb with peas, carrots, and flatbread, chicken, pork, veal, beef, duck, goose, turkey, breast, leg, sirloin"
    },
    {
      "id": "meat_entree",
      "document": "Seared beef with fingerling potatoes and asparagus, Chicken breast stuffed with asiago cheese, with scalloped potatoes, apricot-braised lamb shank with couscous and mixed greens, curried lamb with peas, carrots, and flatbread, chicken, pork, veal, beef, duck, goose, turkey, breast, leg, sirloin"
    }
  ],
  "classified_desserts": [
    {
      "id": "italian_desserts",
      "document": "tiramisu with raspberries, cannoli cake with candied lavender, mascarpone cheesecake with blueberry ice cream, panettone, panna cotta, semifreddo, biscotti "
    },
    {
      "id": "french_desserts",
      "document": "creme brulee, Strawberry tart with creme patissiere and caramel sauce, brioche bread pudding with chocolate glaze, mille-feuille, madeleine, crepe, palmiers, souffle"
    },
    {
      "id": "italian_desserts",
      "document": "tiramisu with raspberries, cannoli cake with candied lavender, mascarpone cheesecake with blueberry ice cream, panettone, panna cotta, semifreddo, biscotti "
    },
    {
      "id": "french_desserts",
      "document": "creme brulee, Strawberry tart with creme patissiere and caramel sauce, brioche bread pudding with chocolate glaze, mille-feuille, madeleine, crepe, palmiers, souffle"
    }
  ]
}
```

