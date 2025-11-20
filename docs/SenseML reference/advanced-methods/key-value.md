---
title: Key/Value
excerpt: ''
deprecated: false
hidden: false
metadata:
  title: ''
  description: ''
  robots: noindex
next:
  description: ''
---
Finds the most promising two-column tabular key/value pair in a single page of the source document. This single page and the winning key are those that score highest on the `terms` and `stopTerms`.

<Table align={["left","left","left"]}>
  <thead>
    <tr>
      <th style={{ textAlign: "left" }}>
        key
      </th>

      <th style={{ textAlign: "left" }}>
        value
      </th>

      <th style={{ textAlign: "left" }}>
        description
      </th>
    </tr>
  </thead>

  <tbody>
    <tr>
      <td style={{ textAlign: "left" }}>
        id
      </td>

      <td style={{ textAlign: "left" }}>
        `keyValue`
      </td>

      <td style={{ textAlign: "left" }}>

      </td>
    </tr>

    <tr>
      <td style={{ textAlign: "left" }}>
        terms
      </td>

      <td style={{ textAlign: "left" }}>
        Array of strings
      </td>

      <td style={{ textAlign: "left" }}>
        An array of terms to score positively. For more information about the NLP approach, see [bag of words](doc:bag-of-words).
      </td>
    </tr>

    <tr>
      <td style={{ textAlign: "left" }}>
        stopTerms
      </td>

      <td style={{ textAlign: "left" }}>
        Array of strings
      </td>

      <td style={{ textAlign: "left" }}>
        optional. An array of terms to score negatively. For more information about the NLP approach, see [bag of words](doc:bag-of-words).
      </td>
    </tr>
  </tbody>
</Table>
