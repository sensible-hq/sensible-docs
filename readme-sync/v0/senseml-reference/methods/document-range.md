---
title: "Document Range"
hidden: false
---
Use the Document Range method to grab multiple consecutive lines, for example, paragraphs of legal text. Or, use it to return the coordinates of regions containing images.

Examples
-----

**Paragraphs and lists**

The following config grabs a list of four sworn statements from a W-9 form: 

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

![](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/images/v0/documentrange_sworn.png)

**Images**

The following config grabs two images from an example PDF that lists icons for popular programming languages:

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

The following image shows this example in the Sensible app:

![](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/images/v0/documentrange_icons.png)

For more information on grabbing images, see the **Notes** section on this page.



Parameters
-------
**Note:** For the full list of parameters available for this method, see [Global parameters for methods](doc:method-object#section-global-parameters-for-methods). The following table only shows parameters most relevant to or specific to this method.

| key               | value                         | description                                                  |
| ----------------- | ----------------------------- | ------------------------------------------------------------ |
| id (**required**) | `documentRange`               |                                                              |
| stop              | Match object. default: `none` | A Match object to stop extraction. Not included in the method output.  If unspecified, matches to end of document. |
| includeAnchor     | boolean. default: `false`     | Includes the anchor line in the method output                |
| includeImages     | boolean. default: `false`     | Returns the zero-indexed page number and coordinates of regions containing images in the document range .  **Notes**:<br/>  If you set to `true`,  also set`"type": "images"` in the `field` object (see preceding section for an example). <br/>Returns only image region coordinates, not image bytes or matching lines (i.e., text). |

Notes
----

**Extracting images**

Currently, Document Range is the only method that supports identifying image regions. Sensible returns the image region coordinates rather than the actual encoded bytes of images. If you want to extract the images themselves, you can use a PDF library in your chosen language to follow these general steps:

- Render the page containing the image to a bitmap. Page numbers are zero-indexed in the Sensible output.
- Convert from Sensible's region coordinates to DPI coordinates.  Sensible region coordinates follow these conventions:
  - they are in reference to a 0.0 origin at the *top left* corner of the page (not the bottom left origin, as is for example the convention with the popular PDF.js library)
  - they are in inches (to convert inches to DPI, simply multiply the inches coordinates by your DPI setting. For example, an x-coordinate of 3.156 inches is approximately 227 DPI for a DPI setting of 72 (72 DPI * 3.156 inches).
  - they are ordered clockwise from top left, i.e.: top left, top right, bottom right, bottom left
- Extract a partial bitmap defined by the coordinates from the page.
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



