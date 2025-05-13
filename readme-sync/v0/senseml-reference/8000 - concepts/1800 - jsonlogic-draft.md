---
title: " style notes"
hidden: true
---

*TODO: style guide:* 

- *operation or operator* 

+ *how to relate that to 'rule' , 'condition' or 'logic'? be consistent across this + other topics*

## Let

 Declares named variables scoped to the Let operator.  This custom operation addresses the limitation that native JsonLogic operators don't support named variable declaration. 

```json
{
"let": [
{ /* 1st arg: initialize named variables using key/value pair syntax */ },
{ /* 2nd arg: operate on the named variables. Sensible evaluates variables in order, and can access previously defined variables  */ }
]
}
```

## Example

```json
{
  "fields": [],
  "postprocessor": {
    "type": "jsonLogic",
    "rule": {
      /* create & operate on named variables scoped to the Let operator */
      "let": [
        {
          /* declare values with key:value pair syntax */
          "a": 5,
          "b": 3,
          /* c is sum of a + b, or 8 */
          "c": {
            "+": [
              {
                "var": "a"
              },
              {
                "var": "b"
              }
            ]
          }
        },
        /* operate on named values (5 * 8) */
        {
          "*": [
            {
              "var": "a"
            },
            {
              "var": "c"
            }
          ]
        }
      ]
    }
  }
}
```

This returns:

```json
/* postprocessor output */
40
```

