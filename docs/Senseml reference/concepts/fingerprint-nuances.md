---
title: Fingerprint nuances
hidden: false
metadata:
  description: Learn how Sensible splits document portfolios into sub-documents using
    fingerprint matching conditions and edge cases with practical examples.
---
This topic illustrates edge cases when Sensible splits portfolios into sub documents. Consider the following example:

| Page | Fingerprint matches which config in which document type? (document type/config + fingerprint type) | Split condition?                             | Action                                                       |
| ---- | ------------------------------------------------------------ | -------------------------------------------- | ------------------------------------------------------------ |
| 1    | 1040s/1040_2019 (first)                                      | YES: "first" match                           | start new 'current document/current config'                  |
| 2    | none                                                         | NO                                           | continue 'current document/current config'                   |
| 3    | paystubs/gusto (first)                                       | YES: "first" match                           | end current doc on prev page<br/>start new 'current document/current config' |
| 4    | none                                                         | NO                                           | continue 'current document/config'                           |
| 5    | paystubs/paylocity (every)                                   | YES: new config has been matched             | end current doc on prev. page<br/>start new 'current document/config' |
| 6    | paystubs/paylocity (every)                                   | NO                                           | continue 'current document/config'                           |
| 7    | none                                                         | YES: `every` match for current config failed | end current doc on prev. page. <br/>current documents/configs = null. this page ignored, won't appear in any document range) |
| 8    | none                                                         | NO                                           | page ignored, won't appear in any document range             |
| 9    | bank_statements/boa (first), bank_statments/boa (every)      | YES: "first" match                           | start new current document/config                            |
| 10   | bank_statements/boa (every)                                  | NO                                           |                                                              |
| 11   | none                                                         | YES: "every" match for current config failed | end current document/config on this page.<br/>current docs/configs = null |
| 12   | TODO: show edge case here w/ 2 matching configs here (frm diff. doc types)...worth it to show complexity...? |                                              |                                                              |
| 13   | none                                                         | NO, current doc/config is null               | page ignored, won't appear in any document range             |
| 14   | none. this is the last page of portfolio                     |                                              | page ignored, won't appear in any document range             |

portfolio document types/configs that are tested against in above example:

1040s

-  1040_2018

-   1040_2019

paystubs

-     gusto

-       Paylocity

-       fallback_llm

bank_statments

-       boa