---
title: Image processing
excerpt: ''
deprecated: false
hidden: false
metadata:
  title: ''
  description: Extract images and image data from documents
  robots: index
next:
  description: ''
---
You have the following options for processing non-text images in documents:

| Use case                                                                                                                                                                                                                                                                                              | Method                                                                                            |
| ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------- |
| Extract structured data from an image with an LLM. For example, extract facts about a photo of a building, such as its color and whether it's multistory-story or single-story.                                                                                                                       | Use the [Query Group](doc:query-group) method with the Multimodal Engine parameter configured.    |
| Extract an image from a known region as an encoded string. For example, use this option when your documents contain complex charts, from which neither LLM-based nor layout-based methods can reliably extract structured data. Extract the chart as an image and render it for a human to interpret. | Use the [Region](doc:region) method with the As Image parameter configured.                       |
| Search for non-labeled, non-text images in a range. For example, search for unlabeled photos of houses in a real estate document, and extract the images' coordinates. This option returns images' coordinates, which you can then use to render the images yourself.                                 | Use the [Document Range](doc:document-range) method with the Include Images parameter configured. |

## Notes

- Sensible's rectangular coordinates for images follow these conventions:

  - they're in reference to a 0.0 origin at the _top left_ corner of the page (not the bottom left origin, as is for example the convention with the popular PDF.js library)

  - they're in inches (to convert inches to pixels, multiply the inches coordinates by your PPI setting. For example, an x-coordinate of 3.156 inches is \~227 pixels for a PPI setting of 72 (72 PPI \* 3.156 inches)).

  - they're ordered clockwise from top left: (top left), (top right), (bottom right), (bottom left)

- This topic is about processing non-text images. For information about processing text images, see [OCR](doc:ocr).

<br />
