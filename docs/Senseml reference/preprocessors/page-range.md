---
title: Page range
excerpt: Learn how to configure the pageRange preprocessor to limit document extraction
  to specific pages using startPage and endPage parameters.
deprecated: false
hidden: false
metadata:
  title: ''
  description: Learn how to configure the pageRange preprocessor to limit document
    extraction to specific pages using startPage and endPage parameters.
  robots: index
next:
  description: ''
---
Ignores pages outside the start page and end page.

**Note**: To configure a page range on a field-by-field basis for LLM-based methods, see each method's Page Range parameter.

## Parameters

| key       | value                      | description                                     |
| --------- | -------------------------- | ----------------------------------------------- |
| type      | `pageRange`                |                                                 |
| startPage | number. default: 0         | Zero-based index of the first page (inclusive). |
| endPage   | number. default: last page | Zero-based index of the last page (exclusive).  |
