---
title: "Document Range"
hidden: false
---
Extracts multiple consecutive lines succeeding the anchor line, for example, paragraphs of legal text. For the full definition of "succeeding", see [Line sorting](doc:concepts#line-sorting).

Or, use this method to return the coordinates of regions containing images.

[**Parameters**](doc:document-range#section-parameters)
[**Examples**](doc:document-range#section-examples)
[**Notes**](doc:document-range#section-notes)



Parameters
====

**Note:** For the full list of parameters available for this method, see [Global parameters for methods](doc:method#section-global-parameters-for-methods). The following table only shows parameters most relevant to or specific to this method.

| key               | value                         | description                                                  |
| ----------------- | ----------------------------- | ------------------------------------------------------------ |
| id (**required**) | `documentRange`               |                                                              |
| stop              | Match object. default: `none` | A Match object to stop extraction. Not included in the method output.  If unspecified, matches to the end of the document. |
| includeAnchor     | boolean. default: `false`     | Includes the anchor line in the method output                |
| includeImages     | boolean. default: `false`     | Returns the zero-indexed page number and coordinates of regions containing images in the document range .  **Notes**:<br/>  If you set  `true`,  also set`"type": "images"` in the `field` object (see Examples section for an example). <br/>Returns only image region coordinates, not image bytes or text lines. |

Examples
====

Paragraphs and lists
----

The following config extracts a list of four sworn statements from a W-9 form: 

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

The following image shows this example in the Sensible app:

![Click to enlarge](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/images/final/documentrange_sworn.png)

Images
----

The following example extracts two images' coordinates:

![Click to enlarge](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/images/final/documentrange_icons.png)

Try out this example in the Sensible app using the following PDF and config:

| Example PDF | [Download link](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/pdfs/image_coordinates_example.pdf) |
| --------------------------------- | ------------------------------------------------------------ |

This example uses the following config:

```json
{
  "fields": [
    {
      "id": "python_icons",
      "type": "images",
      "anchor": "here are some icons",
      "method": {
        "id": "documentRange",
        "includeImages": true,
        "stop": {
          "type": "startsWith",
          "text": "React",
          "isCaseSensitive": true
        }
      }
    },
  ]
}
```



For information on extracting images rather than image metadata, see the **Notes** section on this page.



Notes
====

Extracting images
----

Document Range is the only method that supports identifying image regions. Sensible returns the image region coordinates rather than the actual encoded bytes of images. If you want to extract the images themselves, you can use a PDF library in your chosen programming language to follow these general steps:

- Render the page containing the image to a bitmap. Page numbers are zero-indexed in the Sensible output.
- Convert from Sensible's region coordinates to DPI coordinates.  Sensible region coordinates follow these conventions:
  - they are in reference to a 0.0 origin at the *top left* corner of the page (not the bottom left origin, as is for example the convention with the popular PDF.js library)
  - they are in inches (to convert inches to DPI, simply multiply the inches coordinates by your DPI setting. For example, an x-coordinate of 3.156 inches is approximately 227 DPI for a DPI setting of 72 (72 DPI * 3.156 inches).
  - they are ordered clockwise from top left, i.e.: top left, top right, bottom right, bottom left
- Extract a partial bitmap defined by the image coordinates from the page.
- Encode the bitmap to bytes in the image format of your choice. 

The following is an example of Sensible image coordinate output:

```json
{
  "my_image_coordinates": {
    "images": [
      {
        "page": 0,
        "boundingPolygon": [
          {
            "x": 1.021,
            "y": 2.083
          },
          {
            "x": 3.156,
            "y": 2.083
          },
          {
            "x": 3.156,
            "y": 4.208
          },
          {
            "x": 1.021,
            "y": 4.208
          }
        ]
      }
    ]
  }
}
```



