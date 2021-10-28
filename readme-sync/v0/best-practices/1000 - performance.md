---
title: "Optimizing extraction performance"
hidden: false

---

To improve extraction performance, you can optimize:

- document performance
- document type performance

Note that the number of documents you submit for extraction has no noticeable effect on performance. Each document gets its own worker in parallel.

Document performance
----


In an ideal performance scenario, you extract data from digitally generated PDFs using text-based or coordinate-based Sensible methods, such as Label, Row, Region, Text Table, and Document Range.

In order of slowest to quickest, these factors add seconds to the ideal document processing time:

**Over 10 seconds per document**

| Factor                                   | Notes                                                        |
| ---------------------------------------- | ------------------------------------------------------------ |
| whole-document OCR for scanned documents | Sensible takes 10 seconds or more to OCR an entire document. You can speed OCR up for documents that are 5 pages and shorter by choosing Sensible's Google OCR option for a document type. |
| whole-document table recognition         | Avoid configuring Sensible to search a whole document for tables. Instead, configure a table stop. For examples, see any of the Table [methods](doc:methods). |

 **Under 5 seconds per document**

| Factor                                               | Notes                                                        |
| ---------------------------------------------------- | ------------------------------------------------------------ |
| selective OCR                                        | Some documents mix digital text with text images, for example by embedding scanned pages in a digital PDF. Speed this up by OCRing select pages, not the whole document. For more information, see the [OCR preprocessor](doc:ocr). |
| selective table recognition, Nearest Checkbox method | Sensible process tables that include a stop in less than 5 seconds. Or, convert to the faster [Fixed table](doc:fixed-table) method, which skips table recognition. |

 **Under 1 second per document**

Some Sensible methods use pixels, for example to recognize borders. Pixel recognition requires rendering a PDF page, which can take a couple hundred milliseconds. To improve processing time, use coordinate-based alternatives to these methods. 

| Factor                                                       | Notes                                                        |
| ------------------------------------------------------------ | ------------------------------------------------------------ |
| Box method                                                   | To improve processing speed, convert the more flexible Box method to the strictly coordinate-based Region method. |
| Signature method, Checkbox method, and image coordinate extraction | These methods have no alternatives. See the following section for ways to avoid running these methods except when necessary. |

Document type performance
----


By default, Sensible runs all the configs in a document type before choosing the best one for a given document. If your document type contains configs with computationally expensive methods such as Table or Box, you can improve performance by selectively running and skipping configs.  Use fingerprints to test whether documents contain matching text before skipping or running configs. For more information, see [fingerprint](doc:fingerprint).
