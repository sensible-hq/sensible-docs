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

The following example config shows blah blah:

```json
{
  "fields": [
    {
      "id": "certification",
      "anchor": "penalties of perjury",
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

When you use this config with the following PDF:

| Example PDF for TBD | [Download link](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/pdfs/TBD_example.pdf) |
| ------------------- | ------------------------------------------------------------ |
The Sensible app visually represents this config in the rendered PDF as:

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



**EXAMPLE 2 - excerpt from GSG**

The config is represented visually in the PDF in the Sensible app as follows:

![](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/images/style/pdf_2.png)   

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



**EXAMPLE 3 - REWRITE UI GUIDE:**



***Green points*** represent the following:

-  a starting point for recognizing a box or checkbox

-  a starting point for defining the coordinates of a region

Green points can be useful for troubleshooting. For example, in the following config and PDF, Sensible can't recognize the box: 

| Example PDF | TBD  |
| ----------- | ---- |

```json
{
  "fields": [
    {
      "id": "box_test",
      "anchor": "big anchor text that",
      "method": {
        "id": "box",
        "position": "left",
        "wordFilters":["cramped"]
      }
    }
  ]
}
```

The Sensible app represents this config as follows:

![](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/images/style/pdf_3.png)

The green dot provides a visual clue about why this field returns null: the green dot is *on* the box border itself as specified by `"position": "left"` .



If you change the preceding config to find the box borders by starting from the right edge of the anchor line's boundaries (`"position": "right"`), the green dot is far enough inside the borders for Sensible to recognize the box:

![](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/images/style/pdf_4.png)

And the output of the modified config is:

```json
{
  "box_test": {
    "type": "string",
    "value": "with some text we want to grab"
  }
}
```

FULL WIDTH with drop shadow
---
![](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/images/style/full_width_1.png)





FULL PDFS
----

**half screen on a 2560 x 1440 monitor**

![](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/images/style/full_pdf_1.png)

And:

![](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/images/style/full_pdf_2.png)

And:

![](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/images/style/full_pdf_3.png)

and:

![](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/images/style/full_pdf_4.png)



