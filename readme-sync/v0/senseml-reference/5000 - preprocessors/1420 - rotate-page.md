---
title: "Rotate page"
hidden: true
---

Rotates page so that a matched anchor becomes horizontal. Use this when Sensible's default and automatic rotation behavior fails to rotate a page, usually because the page contains a mix of horizontally and vertically oriented text. 

Parameters
====

| key                 | value                                  | description                                                  |
| ------------------- | -------------------------------------- | ------------------------------------------------------------ |
| type (**required**) | `rotatePage`                           | Rotates by up to 90 degrees.                                 |
| match               | Match object or array of Match objects | See [Match object](doc:match)                                |
| matchAll            | boolean                                | If true, rotates all pages containing the line specified by the Match parameter. |

Examples
====

The following example shows:

- 

**Config**

```json

```

**Example document**

The following images show the example PDF used with this example config:

![Click to enlarge](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/images/final/rotate-page.png)

| Example PDF | [Download link](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/pdfs/rotate-page.pdf) |
| ------------------------------------------ | ------------------------------------------------------------ |

**Output**

```json

```

Notes
----

- 