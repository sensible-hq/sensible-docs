---
title: "Core concepts"
hidden: true
---

SenseML is a query language powered by ML and other techniques that lets you extract structured data from PDF documents. For documents that share a consistent format, you can define a collection of custom SenseML queries as a "config" written in JSON. If you can write basic SQL queries, you can definitely write SenseML queries! 

Here's an example of a "hello world" config: 

 

![image-20210518093619500](C:\Users\franc\AppData\Roaming\Typora\typora-user-images\image-20210518093619500.png)

```json
{
  "fields": [
    {
      "id": "hello_text",
      "anchor": "hello world",
      "method": {
        "id": "label",
        "position": "below"
      }
    }
  ]
}
```

This config returns:

```json
{
  "hello_text": {
    "type": "string",
    "value": "Here’s the line of text that we want to grab."
  }
}
```



What's going on here?

1. An an individual query is a `field` object that returns a key-value json pair. 
2. Our query always starts with a text match called an `anchor` that is near some target data we want to grab. We search for text as a starting point, because it's computationally inexpensive. In the preceding example, we define the anchor text to look for as "hello world".
3. Next we use the text anchor as a reference point from which to expand out and grab the data we actually want. We define how we want to grab the data using a `method`. Methods can potentially be more computationally expensive. They are often spatial (i.e., 'look to the right of the anchor'). We have built-in methods to capture many types of data commonly found in documents (tables, boxes, signatures, paragraphs, etc) as well as highly configurable general-purpose methods (region, regex).  In the preceding example, the method treats the anchor as a label and looks below it for the line to grab. 
4. We return the data we grabbed with a key we defined as the `id` in the query. In the preceding example, we defined the key as "hello_text". 

Core concepts
-----

Now let's explore some core concepts introduced by the preceding example.

SenseML works with primarily with lines. A "line" is a rectangular region containing text that is set apart from other text by empty space.  Two "lines" can both be on the same x-axis, and you can tell what SenseML considers a line by looking at the gray boxes in the SenseML app:

![image-20210518095334649](C:\Users\franc\AppData\Roaming\Typora\typora-user-images\image-20210518095334649.png)

A "line" is a type of region. A "box" is another type of region. Under the hood, everything is either a region or a point in space. 





TO DELETE: *By the way, you can work with regions directly as methods when you need a highly configurable way to define a rectangle in space. Why would you want to do so? Again, under hood, SenseML is sensitive to spacing, because a PDF is really just an image -- a bytemap of dots defined in dots per inch, just as an image is a pixelmap under the hood. So sometimes, the built-in "line" method won't work because lines of text are too far apart.*  

In this example, we define a region (TODO: show the dot, show the region, show the orange anchor and the blue match.. which isn't necessarily the same as the returned value). 





