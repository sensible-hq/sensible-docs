---
title: "draft annotate"
hidden: true
---

Paragraph
====

Use with methods that return paragraphs, for example  [Document Range](https://docs.sensible.so/docs/document-range) or [Paragraph](doc:paragraph), to format the returned paragraph or paragraphs. By default, returns paragraphs formatted with newline characters (\n), instead of formatted as a single string. 

Simple syntax
----

**Syntax example**

`"type": "paragraph"`

**Output example**

Currency
====

You can define this type using concise syntax, or you can configure options with expanded syntax.

Simple syntax
----

**Syntax example**

`"type": "paragraph"`

**Output example** 

``` json
Thereafter, it shall be month-to-month on the same terms and conditions as stated herein plus $80.00 month to month charge, save any changes made pursuant to law, until terminated by notice of at least 30 days.\n Landlord shall send notice of new terms 30 days before current terms end. Proper 30 day notice (in writing or email) must be received by the Landlord.\n
```

**Formats recognized** 

Sensible recognizes paragraphs separated by vertical gaps. Sensible doesn't recognize paragraphs indicated solely by indented first lines. 

Configurable syntax
----

Use configurable syntax to change the output formatting of the text.

**Example syntax **

```json
"type":
  {
    "id": "paragraph",
    "annotateSuperscriptAndSubscript": true
  }
```

**Example output**

For the following PDF:

![Click to enlarge](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/images/final/annotate_superscript_and_subscript.png) 

Setting `"annotateSuperscriptAndSubscript": true` results in the following annotations for the footnote symbols:

```json
{
  "lease_duration": {
    "type": "string",
    "value": "12/31/2023 [^1] . Thereafter, it shall be month-to-month on the same terms and conditions as stated herein plus $80.00 month to month charge, save any changes made pursuant to law, until terminated by notice of at least 30 days. [^2]\n[^1] Landlord shall send notice of new terms 30 days before current terms end. [^2] Proper 30 day notice (in writing or email) must be received by the Landlord."
  }
}
```

**Parameters**

| key                             | value                   | description                                                  |
| ------------------------------- | ----------------------- | ------------------------------------------------------------ |
| id (**required**)               | `paragraph`             |                                                              |
| annotateSuperscriptAndSubscript | Boolean. default: false | When true, Sensible annotates subscript and superscript text with `[^...]` and `[_...]`, respectively. |
