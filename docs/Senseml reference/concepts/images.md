

```
title: Extracting from images
excerpt: ''
deprecated: false
hidden: false
metadata:
  title: ''
  description: 'Extract images and image data from documents'
  robots: index
next:
  description: ''
```


You have the following options for processing non-text images in documents:

- To use an LLM to extract structured data from an image, use the [Query Group](doc:query-group) method with the Multimodal Engine parameter configured. For example, extract facts about a photo of a building, such as whether it's multistory-story or single-story.
- To extract an image from a known region as an encoded string, use the [Region](doc:region) method's As Image parameter. For example, extract a complex chart image that neither LLM-based nor layout-based method can reliably extract from, render it for an end-user to review.
- To search for a non-text image in a range, use the [Document Range](doc:document-range) method. This option returns images' coordinates, which you can then use to render the image yourself.  For example, search for unlabeled photos of houses in a real estate document, and extract their coordinates.