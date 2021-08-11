---
title: "visual draft"
hidden: true
---

ORIGINAL STYLE
---


![](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/images/documentrange_sworn.png)

CSS MOD -1 
----

- no scrollbars, col-span 3-5-4, chrome zoom 150%

  ![](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/images/style/150.png)

ALTERNATIVE - RENDERED PDF ONLY:
----

**Example 1** 

The following example config:

```json
{
  "fields": [
    {
      "id": "certification",
      "anchor": "perjury",
      "method": {
        "id": "documentRange",
        "stop": {
          "type": "startsWith",
          "text": "Certification instructions",
          "isCaseSensitive": true
        }
      }
    },
  ]
}
```

Displays in the Sensible app as:

![](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/images/style/pdf_only_1.png)

The output is:

```
{
  "certification": {
    "type": "string",
    "value": "1. The number shown on this form is my correct taxpayer identification number (or I am waiting for a number to be issued to me); and 2. I am not subject to backup withholding because: (a) I am exempt from backup withholding, or (b) I have not been notified by the Internal Revenue Service (IRS) that I am subject to backup withholding as a result of a failure to report all interest or dividends, or (c) the IRS has notified me that I am no longer subject to backup withholding; and 3. I am a U.S. citizen or other U.S. person (defined below); and 4. The FATCA code(s) entered on this form (if any) indicating that I am exempt from FATCA reporting is correct."
  }
}
```



**EXAMPLE 2**

The config is represented visually in the PDF in the Sensible app:

![](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/images/pdf_2.png)   

You should see the following extracted data in the right pane of the Sensible app:

```json
{
  "policy_number": {
    "type": "string",
    "value": "123456789"
  },
  "policy_period": {
    "type": "string",
    "value": " April 14, 2021 - Oct 14, 2021"
  },
  "comprehensive_premium": {
    "source": "$150",
    "value": 150,
    "unit": "$",
    "type": "currency"
  }
}
```

Congratulations! 







