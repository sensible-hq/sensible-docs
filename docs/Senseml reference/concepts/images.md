---
title: Image processing
excerpt: ''
deprecated: false
hidden: false
metadata:
  title: ''
  description: Extract non-text images and image data from documents
  robots: index
next:
  description: ''
---
You have the following options for processing non-text images in documents:

| Use case                                                     | Example                                                      | Method                                                       |
| ------------------------------------------------------------ | ------------------------------------------------------------ | ------------------------------------------------------------ |
| Extract structured data from an image with an LLM.           | Extract facts about a photo of a building, such as its color and whether it's multistory-story or single-story. | Use the [Query Group](doc:query-group) method with the Multimodal Engine parameter configured. |
| Extract an image from a known region as an encoded string.   | Your documents contain complex charts, from which neither LLM-based nor layout-based methods can reliably extract structured data. Extract the chart as an image and render it for a human to interpret. | Use the [Region](doc:region) method with the As Image parameter configured. |
| Search for non-labeled, non-text images in a range. This option returns images' coordinates, which you can then use to render the images. | Search for unlabeled photos of buildings in a real estate document. | Use the [Document Range](doc:document-range) method with the Include Images parameter configured. |

Note that this topic is about processing non-text images. For information about processing text images, see [OCR](doc:ocr).

## Notes

Sensible's convention is to provide coordinates for images, lines, and other objects as rectangular regions. Coordinate are:

- in reference to a 0,0 origin at the *top* left corner of the page.
- in inches. To convert inches to pixels, multiply the inches coordinates by your PPI setting. For example, an x-coordinate of 3.156 inches is \~227 pixels for a PPI setting of 72 (72 PPI \* 3.156 inches).
- ordered clockwise from top left: (top left), (top right), (bottom right), (bottom left).

For example, the following coordinates define a region whose top left corner is 2.208 inches down from the top edge of the page and 1.021 inches from the left edge of the page, with a width of 2.135 inches (3.156 - 1.021) and a height of 2.125 inches (4.333 - 2.208):

```json
"boundingPolygon": [
          {
            "x": 1.021,
            "y": 2.208
          },
          {
            "x": 3.156,
            "y": 2.208
          },
          {
            "x": 3.156,
            "y": 4.333
          },
          {
            "x": 1.021,
            "y": 4.333
          }
        ]
```





